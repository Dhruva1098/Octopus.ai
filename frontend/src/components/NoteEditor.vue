<template>
  <div>
    <!-- Editable title -->
    <input
        type="text"
        v-model="editorTitle"
        class="w-full text-2xl font-bold mb-4 border-b outline-none focus:border-blue-500"
        placeholder="Note title"
        @blur="updateTitle"
    />

    <!-- tiptap editor content -->
    <EditorContent :editor="editor" class="prose max-w-none mb-4" />

    <!-- Action Buttons -->
    <div class="flex space-x-4">
      <button
          @click="handleSave"
          class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
      >
        Save Note
      </button>
      <button
          @click="handleDelete"
          class="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600"
      >
        Delete Note
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { Editor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  note: {
    type: Object,
    required: true
  }
})
const emit = defineEmits(['save', 'delete'])

// Use a local copy for the note title
const editorTitle = ref(props.note.title)

// Create the tiptap editor instance
const editor = ref(null)
onMounted(() => {
  editor.value = new Editor({
    content: props.note.content,
    extensions: [StarterKit],
    onUpdate({ editor }) {
      // (Optional: auto-save logic can go here)
    }
  })
})
onBeforeUnmount(() => {
  if (editor.value) {
    editor.value.destroy()
  }
})

// When switching between notes, update local title and content.
watch(
    () => props.note,
    (newNote) => {
      editorTitle.value = newNote.title
      if (editor.value && newNote.content !== editor.value.getHTML()) {
        editor.value.commands.setContent(newNote.content)
      }
    },
    { immediate: true }
)

// Update the note's title on blur.
function updateTitle() {
  props.note.title = editorTitle.value
}

// Emit the save event with the updated note (including title and content)
function handleSave() {
  const updatedNote = {
    ...props.note,
    title: editorTitle.value,
    content: editor.value.getHTML()
  }
  emit('save', updatedNote)
}

// Emit a delete event so the parent can handle deletion.
function handleDelete() {
  emit('delete', props.note)
}
</script>

<style scoped>
.prose p {
  margin: 0.5em 0;
}
</style>
