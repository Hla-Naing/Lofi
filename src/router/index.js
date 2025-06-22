//this defines all the routes in the application that is available to the user
//this will link to the URL path to the component which is a template


// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// Import views/components that represent pages
import HomePage from '../components/Homepage.vue' // Home page component
import SelectInstruments from '../components/SelectInstruments.vue' // New component for selecting instruments

const routes = [
  { path: '/', component: HomePage }, // Home route
  { path: '/select-instruments', name: 'SelectInstruments', component: SelectInstruments } // New route
]

const router = createRouter({
  history: createWebHistory(), // 👈 uses browser history (no hash in URLs)
  routes, // 👈 pass the routes we defined above
})

export default router
