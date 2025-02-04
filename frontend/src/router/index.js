import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../components/Dashboard.vue'
import NoteEditor from '../components/NoteEditor.vue'

const routes = [
  { path: '/', component: Dashboard },
  { path: 'edit/:id', component: NoteEditor },

]

const router = createRouter({
  history: createWebHistory(),
  routes,
  }
)
export default router
