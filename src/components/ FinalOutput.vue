//display Audio player with timestamp, Download button

<script setup>
import { ref, onMounted } from 'vue'

// Replace with actual backend file URL
const audioSrc = ref('http://localhost:8000/static/final.mp3') //this is where the final audio file will be served
</script>

<template>
  <div class="min-h-screen w-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white flex flex-col items-center justify-center p-6">
    <h2 class="text-3xl font-bold mb-6">Your Lofi Track is Ready 🎵</h2>

    <audio controls :src="audioSrc" class="w-full max-w-md mb-4" />

    <a :href="audioSrc" download class="px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-semibold text-white transition-all">
      ⬇️ Download Track
    </a>
  </div>
</template>
