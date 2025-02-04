import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './index.css'  // If using Tailwind CSS

createApp(App).use(router).mount('#app')
