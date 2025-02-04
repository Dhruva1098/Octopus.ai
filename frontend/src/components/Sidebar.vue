<template>
  <div class="w-64 bg-gray-100 p-4 border-r overflow-y-auto">
    <h2 class="text-xl font-bold mb-4">Notes</h2>
    <ul>
      <li v-for="note in notes" :key="note.id" class="mb-2">
        <button
            class="w-full text-left p-2 rounded hover:bg-gray-200"
            @click="$emit('select-note', note)"
        >
          {{ note.title }}
        </button>
      </li>
    </ul>
    <button
        class="mt-4 w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
        @click="$emit('new-note')"
    >
      + New Note
    </button>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  notes: {
    type: Array,
    required: true
  }
})
</script>
