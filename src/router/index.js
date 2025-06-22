import { createRouter, createWebHistory } from 'vue-router'

import HomePage from '../components/Homepage.vue'
import SelectInstruments from '../components/SelectInstruments.vue'

const routes = [
  { path: '/', component: HomePage },
  { path: '/select-instruments', name: 'select-instruments', component: SelectInstruments } // 🔧 fixed name
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
