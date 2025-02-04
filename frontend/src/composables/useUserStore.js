import { reactive } from 'vue'

export const userStore = reactive({
    userId: null,
    notes: [] // Each note: { id, title, content }
})
