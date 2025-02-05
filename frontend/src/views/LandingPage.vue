<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4">
    <h1 class="text-4xl font-bold mb-4">Welcome to NoteRAG</h1>

    <!-- Display answer (from /ask) above the search bar -->
    <div v-if="answer" class="bg-green-100 text-green-800 p-4 rounded mb-4 w-full max-w-lg">
      <strong>Answer:</strong> {{ answer }}
    </div>

    <!-- Query Input -->
    <div class="flex mb-4 w-full max-w-lg">
      <input
          v-model="query"
          type="text"
          placeholder="Enter your query..."
          class="border p-2 rounded-l w-full"
      />
      <button @click="performSearch" class="bg-blue-500 text-white p-2 rounded-r">
        Search
      </button>
    </div>

    <!-- Matching Notes Cards -->
    <div v-if="matchingNotes.length" class="w-full max-w-lg">
      <h2 class="text-2xl font-semibold mb-4">Matching Notes</h2>
      <div class="grid gap-4 sm:grid-cols-2">
        <div
            v-for="note in matchingNotes"
            :key="note.id"
            class="border p-4 rounded shadow hover:shadow-lg bg-white"
        >
          <h3 class="font-bold mb-2">{{ note.title }}</h3>
          <div class="text-sm" v-html="note.content"></div>
          <div class="text-xs text-gray-500">Created at: {{ note.created_at }}</div>
        </div>
      </div>
    </div>

    <!-- Navigation to the Note App -->
    <div class="mt-8">
      <router-link to="/notes">
        <button class="bg-green-500 text-white p-3 rounded">
          My Notes
        </button>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/api'
import { userStore } from '@/composables/useUserStore'

const query = ref('')
const answer = ref('')
const searchNoteIds = ref([])

// For testing, fix user_id = 1.
userStore.userId = 1

// Load all notes using POST /all_notes.
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

// Perform search using POST /ask.
async function performSearch() {
  if (!query.value.trim()) {
    answer.value = ''
    searchNoteIds.value = []
    return
  }

  try {
    const res = await api.post('/ask', {
      user_id: 1,
      query: query.value
    })
    // Expected response: { answer: '...', note_ids: [ ... ] }
    answer.value = res.data.answer
    searchNoteIds.value = res.data.note_ids || []
  } catch (error) {
    console.error('Error performing search:', error)
  }
}

// Compute matching notes by filtering loaded notes using the returned note IDs.
const matchingNotes = computed(() => {
  return userStore.notes.filter(note => searchNoteIds.value.includes(note.id))
})
</script>
