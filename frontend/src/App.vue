<template>
  <div class="app-container flex h-screen">
    <!-- Sidebar -->
    <Sidebar :notes="notes" @select-note="selectNote" @new-note="createNote" />

    <!-- Editor area -->
    <div class="flex-1 p-8 overflow-auto">
      <div v-if="selectedNote">
        <NoteEditor :note="selectedNote" @update="updateNote" />
      </div>
      <div v-else class="flex items-center justify-center h-full text-gray-500">
        Select a note to start editing...
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from './components/Sidebar.vue'
import NoteEditor from './components/NoteEditor.vue'

// Sample notes data
const notes = ref([
  { id: 1, title: 'Meeting Notes', content: '<p>Write your meeting notes here...</p>' },
  { id: 2, title: 'Project Ideas', content: '<p>Jot down your project ideas...</p>' },
])

const selectedNote = ref(null)

// Called when a note is selected in the sidebar
function selectNote(note) {
  selectedNote.value = note
}

// Called when the editor emits an update event
function updateNote(updatedContent) {
  if (selectedNote.value) {
    selectedNote.value.content = updatedContent
  }
}

// Create a new note and select it
function createNote() {
  const newNote = {
    id: Date.now(),
    title: 'Untitled Note',
    content: '<p></p>',
  }
  notes.value.push(newNote)
  selectedNote.value = newNote
}
</script>

<style>
/* Optional: add global styles or overrides here */
</style>
