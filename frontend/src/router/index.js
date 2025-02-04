import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '@/views/LandingPage.vue'
import NoteApp from '@/views/NoteApp.vue'

const routes = [
    {
        path: '/',
        name: 'Landing',
        component: LandingPage
    },
    {
        path: '/notes',
        name: 'Notes',
        component: NoteApp
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
