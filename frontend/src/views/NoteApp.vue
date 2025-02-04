<template>
  <div class="app-container flex h-screen">
    <!-- Sidebar (lists notes and a button for new notes) -->
    <Sidebar :notes="userStore.notes" @select-note="selectNote" @new-note="createNote" />

    <!-- Editor area -->
    <div class="flex-1 p-8 overflow-auto">
      <div v-if="selectedNote">
        <NoteEditor :note="selectedNote" @save="saveNote" />
      </div>
      <div v-else class="flex items-center justify-center h-full text-gray-500">
        Select a note to start editing...
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import Sidebar from '@/components/Sidebar.vue'
import NoteEditor from '@/components/NoteEditor.vue'
import { userStore } from '@/composables/useUserStore'

// Currently selected note for editing
const selectedNote = ref(null)

// Called when a note is selected from the sidebar
function selectNote(note) {
  selectedNote.value = note
}

// Create a new note, add it to the global store, and post it to /notes
async function createNote() {
  const newNote = {
    id: Date.now(), // or use a better unique id in a real app
    title: 'Untitled Note',
    content: '<p></p>'
  }
  userStore.notes.push(newNote)
  selectedNote.value = newNote

  try {
    await axios.post('/notes', {
      user_id: userStore.userId,
      content: newNote.content
    })
  } catch (error) {
    console.error('Error creating note:', error)
  }
}

// Save an updated note (triggered from the editor) by posting to /notes
async function saveNote(updatedNote) {
  // Update note content in the global store (if not already updated)
  const idx = userStore.notes.findIndex(note => note.id === updatedNote.id)
  if (idx !== -1) {
    userStore.notes[idx] = updatedNote
  }
  try {
    await axios.post('/notes', {
      user_id: userStore.userId,
      content: updatedNote.content
    })
  } catch (error) {
    console.error('Error saving note:', error)
  }
}
</script>
