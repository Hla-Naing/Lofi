
//this defines all the routes in the application that is available to the user
//this will link to the URL path to the component which is a template

import { createRouter, createWebHistory } from 'vue-router'

import HomePage from '../components/Homepage.vue'
import SelectInstruments from '../components/SelectInstruments.vue'
import SoundEffects from '../components/SoundEffects.vue'
import LoadingPage from '../components/LoadingPage.vue' // Loading page component
import FinalOutput from '../components/ FinalOutput.vue'   // Final output component

const routes = [
  { path: '/', component: HomePage },
  { path: '/select-instruments', name: 'select-instruments', component: SelectInstruments },// 🔧 fixed name
  { path: '/sound-effects', name: 'SoundEffects', component: SoundEffects }, // Lazy-loaded sound effects component
  { path: '/loading',name: 'LoadingPage', component: LoadingPage}, // Loading page route
  { path: '/final-output', name: 'FinalOutput', component: FinalOutput}, // Final output route

]

const router = createRouter({
  history: createWebHistory(),
  routes

})

export default router
