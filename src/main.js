import { createApp } from 'vue'
import './style.css'

import App from './App.vue'
import router from './router' // 👈 importing our router setup
createApp(App).use(router).mount('#app') // 👈 enable routing in the app