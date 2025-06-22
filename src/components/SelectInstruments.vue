<!-- src/components/SelectInstruments.vue -->
<script setup>
import { ref } from 'vue'
import { Music } from 'lucide-vue-next'
import { useRoute, useRouter } from 'vue-router'

const checkedNames = ref([])
const route = useRoute()
const router = useRouter()

const filename = route.query.file

async function handleContinue() {
  if (!filename) {
    alert("❌ No file information passed from previous page.")
    return
  }

  const stemMap = {
    "Vocal": "vocals",
    "Drum": "drum",
    "Bass": "bass",
    "Electric Guitar": "electric_guitar",
    "Acoustic Guitar": "acoustic_guitar",
    "Piano": "piano"
  }

  const mappedStems = checkedNames.value.map(name => stemMap[name]).filter(Boolean)

  if (!mappedStems.length) {
    alert("❌ No valid stems selected.")
    return
  }

  try {
    const response = await fetch("http://localhost:8000/split/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        file: filename,
        stems: mappedStems
      })
    })

    const result = await response.json()

    if (response.ok) {
      alert("✅ Audio splitting started! Check your output folder.")
      // Optionally navigate to a results page here
    } else {
      alert(`❌ Error: ${result.message}`)
    }
  } catch (err) {
    console.error("❌ Split request failed:", err)
    alert("❌ Server error occurred.")
  }
}

</script>

<template>
  <div class="w-screen min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col">
    <!-- Background Blobs -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none select-none">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-pink-500/20 rounded-full blur-3xl"></div>
      <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
    </div>

    <!-- Main Content -->
    <div class="relative z-10 flex-1 flex flex-col items-center justify-center px-6 sm:px-10 py-16 w-full">
      <!-- Header -->
      <div class="text-center mb-10">
        <div class="flex items-center justify-center mb-6">
          <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mr-4">
            <Music class="w-8 h-8 text-white" />
          </div>
          <h1 class="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            Choose Instruments
          </h1>
        </div>
        <p class="text-lg text-gray-300 max-w-xl mx-auto">
          Pick the stems you'd like to keep in your chill Lofi track 🎧
        </p>
      </div>

      <!-- Selection Card -->
      <div class="w-full max-w-2xl bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-8 sm:p-10 text-white">
        <!-- Checkboxes Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <label class="flex items-center space-x-3">
            <input type="checkbox" value="Vocal" v-model="checkedNames" class="accent-purple-500 w-5 h-5" />
            <span>Vocal</span>
          </label>
          <label class="flex items-center space-x-3">
            <input type="checkbox" value="Drum" v-model="checkedNames" class="accent-purple-500 w-5 h-5" />
            <span>Drum</span>
          </label>
          <label class="flex items-center space-x-3">
            <input type="checkbox" value="Bass" v-model="checkedNames" class="accent-purple-500 w-5 h-5" />
            <span>Bass</span>
          </label>
          <label class="flex items-center space-x-3">
            <input type="checkbox" value="Electric Guitar" v-model="checkedNames" class="accent-purple-500 w-5 h-5" />
            <span>Electric Guitar</span>
          </label>
          <label class="flex items-center space-x-3">
            <input type="checkbox" value="Acoustic Guitar" v-model="checkedNames" class="accent-purple-500 w-5 h-5" />
            <span>Acoustic Guitar</span>
          </label>
          <label class="flex items-center space-x-3">
            <input type="checkbox" value="Piano" v-model="checkedNames" class="accent-purple-500 w-5 h-5" />
            <span>Piano</span>
          </label>
        </div>

        <!-- Selected Summary + Continue -->
        <div class="mt-10 text-center">
          <p class="text-sm text-purple-200 mb-6">
            <span v-if="checkedNames.length">You selected: {{ checkedNames.join(', ') }}</span>
            <span v-else>No instruments selected yet.</span>
          </p>

          <!-- Aligned Continue Button -->
          <div class="flex justify-center">
            <button
              class="group relative px-10 py-3 rounded-2xl font-bold text-lg transition-all duration-300 transform
                     bg-gradient-to-r from-purple-500 to-pink-500 text-white
                     hover:from-purple-600 hover:to-pink-600 hover:scale-105 hover:shadow-2xl hover:shadow-purple-500/25"
              :disabled="!checkedNames.length"
              :class="{
                'opacity-50 cursor-not-allowed': !checkedNames.length
              }"
              @click="handleContinue"
            >
              Continue →
              <div
                v-if="checkedNames.length"
                class="absolute inset-0 rounded-2xl bg-gradient-to-r from-purple-600 to-pink-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300 -z-10"
              ></div>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
