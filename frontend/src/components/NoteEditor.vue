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

    <!-- tiptap editor area -->
    <EditorContent :editor="editor" class="prose max-w-none mb-4" />

    <!-- Save Button -->
    <button
        @click="handleSave"
        class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
    >
      Save Note
    </button>
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

const emit = defineEmits(['save'])

// Use a local copy of the title for editing
const editorTitle = ref(props.note.title)

// Create the editor instance
const editor = ref(null)

onMounted(() => {
  editor.value = new Editor({
    content: props.note.content,
    extensions: [StarterKit],
    onUpdate({ editor }) {
      // When content updates, you can choose to emit a save event on demand.
      // Here, we do nothing on every update.
    }
  })
})

onBeforeUnmount(() => {
  if (editor.value) {
    editor.value.destroy()
  }
})

// If the note’s content changes externally, update the editor.
watch(
    () => props.note.content,
    (newContent) => {
      if (editor.value && newContent !== editor.value.getHTML()) {
        editor.value.commands.setContent(newContent)
      }
    }
)

// Update the note title on blur.
function updateTitle() {
  props.note.title = editorTitle.value
}

// Trigger save: emit the note object with updated content.
function handleSave() {
  const updatedNote = {
    ...props.note,
    content: editor.value.getHTML()
  }
  emit('save', updatedNote)
}
</script>

<style scoped>
.prose p {
  margin: 0.5em 0;
}
</style>
