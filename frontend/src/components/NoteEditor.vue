<script>
import { useEditor, EditorContent} from "@tiptap/vue-3";
import {StarterKit} from "@tiptap/starter-kit";
import axios from 'axios'

const editor = useEditor({
  content: '',
  extensions: [StarterKit],
})

const saveNote = async () => {
  const content = editor.getHTML()
  await axios.post('/api/notes', {content})
  alert('Note saved')
}
</script>

<template>
<div>
  <h2> Create/Edit Note</h2>
  <editor-content: editor="editor" />
  <button @click="saveNote">Save Note</button>
</div>
</template>

<style scoped>

</style>
