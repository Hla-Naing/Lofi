import { createRouter, createWebHistory } from 'vue-router'

import HomePage from '../components/Homepage.vue'
import SelectInstruments from '../components/SelectInstruments.vue'
import SoundEffects from '../components/SoundEffects.vue'

const routes = [
  { path: '/', component: HomePage },
  { path: '/select-instruments', name: 'select-instruments', component: SelectInstruments },// 🔧 fixed name
  { path: '/sound-effects', name: 'SoundEffects', component: SoundEffects } // Lazy-loaded sound effects component

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
