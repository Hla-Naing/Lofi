<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'  // Import useRoute to get route parameters

// Use the query parameter from the route to get the final audio file path dynamically
const audioSrc = ref('')
const audioPlayer = ref(null)
const elapsedTime = ref('0:00')

// Get the audio file path passed from the previous route (through query params)
const route = useRoute()
const finalFilePath = route.query.output_file // Example: 'final_lofi_output.wav'

onMounted(() => {
  if (finalFilePath) {
    // Dynamically set the audio source to the FastAPI served path
    audioSrc.value = `http://localhost:8000/${finalFilePath}`
  }

  // Event listener to show elapsed time in the audio player
  if (audioPlayer.value) {
    audioPlayer.value.addEventListener('timeupdate', () => {
      const minutes = Math.floor(audioPlayer.value.currentTime / 60)
      const seconds = Math.floor(audioPlayer.value.currentTime % 60)
      elapsedTime.value = `${minutes}:${seconds < 10 ? '0' + seconds : seconds}`
    })
  }
})
</script>

<template>
  <div class="min-h-screen w-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white flex flex-col items-center justify-center p-6">
    <h2 class="text-3xl font-bold mb-6">Your Lofi Track is Ready 🎵</h2>

    <!-- Audio Player with Timestamp -->
    <div class="flex flex-col items-center mb-4">
      <audio ref="audioPlayer" controls :src="audioSrc" class="w-full max-w-md mb-4"></audio>
      <p class="text-lg text-gray-300">Elapsed Time: {{ elapsedTime }}</p>
    </div>

    <!-- Download Button -->
    <a :href="audioSrc" download class="px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-semibold text-white transition-all">
      ⬇️ Download Track
    </a>
  </div>
</template>
