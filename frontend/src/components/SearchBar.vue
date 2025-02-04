<script>
import {ref} from 'vue'
import axios from 'axios'

const query = ref('')
const results = ref([])

const searchNotes = async () => {
  const response = await axios.post('/api/search', {query: query.value})
  results.value = response.data.results
}
</script>
<template>
<div>
  <input v-model="query" placeholder="Search notes" @input="searchNotes" />
  <ul>
    <li v-for="note in results" :key="note.id">{{ note.content }}</li>
  </ul>
</div>
</template>

<style scoped>

</style>

