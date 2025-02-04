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
    <EditorContent :editor="editor" class="prose max-w-none" />
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
    required: true,
  },
})

const emit = defineEmits(['update'])

// Local state for the note title (optional)
const editorTitle = ref(props.note.title)

// Create the editor instance
const editor = ref(null)

onMounted(() => {
  editor.value = new Editor({
    content: props.note.content,
    extensions: [StarterKit],
    onUpdate({ editor }) {
      // Emit the updated HTML content to the parent component
      emit('update', editor.getHTML())
    },
  })
})

// Destroy the editor on unmount
onBeforeUnmount(() => {
  if (editor.value) {
    editor.value.destroy()
  }
})

// If the note content changes from outside, update the editor content
watch(
    () => props.note.content,
    (newContent) => {
      if (editor.value && newContent !== editor.value.getHTML()) {
        editor.value.commands.setContent(newContent)
      }
    }
)

// Optionally, update the note title (this example does not propagate title changes to the parent)
function updateTitle() {
  // Here you might want to emit a title change event or update the note directly
  // For this example, we simply update the note’s title locally:
  props.note.title = editorTitle.value
}
</script>

<style scoped>
/* Optional: add styles for the editor, e.g., for a Notion-like feel */
.prose p {
  margin: 0.5em 0;
}
</style>
