// src/composables/useUserStore.js
import { reactive } from 'vue'

export const userStore = reactive({
    userId: null,
    notes: [] // Each note: { id, content, created_at, ... }
})
