<template>
  <div class="app-container flex h-screen">
    <!-- Sidebar: displays all notes and a button for new notes -->
    <Sidebar :notes="userStore.notes" @select-note="selectNote" @new-note="createNote" />

    <!-- Editor area -->
    <div class="flex-1 p-8 overflow-auto">
      <div v-if="selectedNote">
        <NoteEditor
            :note="selectedNote"
            @save="saveNote"
            @delete="deleteNote"
        />
      </div>
      <div v-else class="flex items-center justify-center h-full text-gray-500">
        Select a note to start editing...
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'
import Sidebar from '@/components/Sidebar.vue'
import NoteEditor from '@/components/NoteEditor.vue'
import { userStore } from '@/composables/useUserStore'

// For testing, fix user_id = 1.
userStore.userId = 1

const selectedNote = ref(null)

// Load all notes from the database using POST /all_notes.
onMounted(async () => {
  try {
    const resNotes = await api.post('/all_notes', { user_id: 1 })
    if (resNotes.data.notes) {
      userStore.notes = resNotes.data.notes
    }
  } catch (error) {
    console.error('Error fetching all notes:', error)
  }
})

function selectNote(note) {
  selectedNote.value = note
}

// Create a new note and POST it to /notes.
async function createNote() {
  // Generate a smaller client-side ID (seconds since epoch)
  const newNote = {
    id: Math.floor(Date.now() / 1000),
    title: 'Untitled Note',
    content: '<p></p>',
    created_at: new Date().toISOString()
  }
  userStore.notes.push(newNote)
  selectedNote.value = newNote

  try {
    // On creation, send the new note data (include note_id)
    await api.post('/notes', {
      user_id: 1,
      note_id: newNote.id,
      title: newNote.title,
      content: newNote.content
    })
  } catch (error) {
    console.error('Error creating note:', error)
  }
}

// Save an updated note by POSTing to /notes (includes note_id so backend updates it).
async function saveNote(updatedNote) {
  const idx = userStore.notes.findIndex(note => note.id === updatedNote.id)
  if (idx !== -1) {
    userStore.notes[idx] = updatedNote
  }
  try {
    await api.post('/notes', {
      user_id: 1,
      note_id: updatedNote.id, // Ensures the backend updates the existing note.
      title: updatedNote.title,
      content: updatedNote.content
    })
  } catch (error) {
    console.error('Error saving note:', error)
  }
}

// Delete a note by calling the delete endpoint.
async function deleteNote(note) {
  try {
    await api.post('/notes/delete', { // using POST for deletion
      user_id: 1,
      note_id: note.id
    })
    // Remove the note from the global store.
    userStore.notes = userStore.notes.filter(n => n.id !== note.id)
    // If the deleted note was open, clear the editor.
    if (selectedNote.value && selectedNote.value.id === note.id) {
      selectedNote.value = null
    }
  } catch (error) {
    console.error('Error deleting note:', error)
  }
}
</script>
