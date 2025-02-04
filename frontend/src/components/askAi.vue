<script setup lang="ts">
  import {ref} from "vue";
  import axios from "axios";

  const question = ref('');
  const answer = ref('');

  const askAI = async () => {
    const response = await axios.post('/api/ask', {question: question.value})
    answer.value = response.data.answer;
  }
</script>

<template>
  <div>
    <h2> Ask AI</h2>
    <input v-model="question" placeholder="Ask a question" @input="askAI" />
    <p>{{ answer }}</p>
  </div>
</template>

<style scoped>

</style>
