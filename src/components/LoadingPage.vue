<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const showButton = ref(false)
const router = useRouter()

onMounted(async () => {
  try {
    await fetch('http://localhost:8000/process-audio', { method: 'POST' })
  } catch (err) {
    console.warn('⚠️ Backend fetch failed. Skipping to button:', err)
  }

  // Always show button after 10 seconds, even if fetch fails
  setTimeout(() => {
    showButton.value = true
  }, 10000)
})

function goToSoundEffects() {
  router.push({ name: 'SoundEffects' })
}
</script>



<template>
  <div class="min-h-screen w-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white flex flex-col items-center justify-center p-6">
    <p class="text-xl mb-4">Processing your audio... 🎧</p>

    <!-- Spinner -->
    <div class="mt-6 animate-spin h-12 w-12 border-4 border-purple-500 rounded-full border-t-transparent"></div>

    <!-- Continue button appears after 10 seconds -->
    <button
      v-if="showButton"
      @click="goToSoundEffects"
      class="mt-10 px-8 py-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl font-bold hover:scale-105 transition-all"
    >
      Continue →
    </button>
  </div>
</template>
