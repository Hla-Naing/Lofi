<script setup>
import { ref, computed } from 'vue'
import { Upload, Music, Youtube, Sparkles, FileAudio, ExternalLink } from 'lucide-vue-next'
// import router inside your <script setup> - so you can user router to go to other pages
import { useRouter } from 'vue-router'

const router = useRouter()
const file = ref(null)
const youtubeUrl = ref('')
const isDragging = ref(false)

const hasInput = computed(() => file.value || youtubeUrl.value.trim())

function handleFileChange(event) {
  file.value = event.target.files[0]
  youtubeUrl.value = '' // Clear YouTube URL if file is selected
}

function handleDrop(event) {
  event.preventDefault()
  isDragging.value = false
  
  const droppedFile = event.dataTransfer.files[0]
  if (droppedFile && droppedFile.type.startsWith('audio/')) {
    file.value = droppedFile
    youtubeUrl.value = ''
  }
}

function handleDragOver(event) {
  event.preventDefault()
  isDragging.value = true
}

function handleDragLeave(event) {
  event.preventDefault()
  isDragging.value = false
}

function clearFile() {
  file.value = null
}

function clearUrl() {
  youtubeUrl.value = ''
}

function convertToLofi() {
  if (file.value) {
    alert(`Converting uploaded file: ${file.value.name} to lofi...`)
    router.push({ name: 'SelectInstruments' })
  } else if (youtubeUrl.value.trim()) {
    alert(`Converting YouTube link: ${youtubeUrl.value.trim()} to lofi...`)
    router.push({ name: 'SelectInstruments' })
  } else {
    alert('Please upload a file or paste a YouTube URL.')
  }
}


  // Example: router.push('/final-step') or save to localStorage

// function convertToLofi() {
//   if (file.value || youtubeUrl.value.trim()) {
//     // ✅ Optional: Save file/youtubeUrl to localStorage or Pinia for later use
//     // localStorage.setItem('youtubeLink', youtubeUrl.value)

//     // ✅ Redirect user to /select-instruments
//     router.push({ name: 'SelectInstruments' })
//   } else {
//     alert('Please upload a file or paste a YouTube URL.')
//   }
// }
</script>

<template>

 <div class="w-screen min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col">

    <!-- Background decoration -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none select-none">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-pink-500/20 rounded-full blur-3xl"></div>
      <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
    </div>

    <div class="relative z-10 flex-1 flex flex-col items-center justify-center px-0 sm:px-8 md:px-16 lg:px-32 xl:px-48 2xl:px-64 py-8 w-full min-h-screen">
      <!-- Header -->
      <div class="text-center mb-12">
        <div class="flex items-center justify-center mb-6">
          <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mr-4">
            <Music class="w-8 h-8 text-white" />
          </div>
          <h1 class="text-5xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            LoFi Converter
          </h1>
        </div>
        <p class="text-xl text-gray-300 max-w-2xl">
          Transform your music into chill lofi vibes. Upload an audio file or paste a YouTube URL to get started.
        </p>
      </div>

      <!-- Main Content -->
      <div class="w-full max-w-4xl">
        <div class="grid md:grid-cols-2 gap-8 mb-8">
          
          <!-- File Upload Section -->
          <div class="bg-white/5 backdrop-blur-lg rounded-2xl p-8 border border-white/10 hover:border-purple-400/50 transition-all duration-300">
            <div class="flex items-center mb-6">
              <Upload class="w-6 h-6 text-purple-400 mr-3" />
              <h2 class="text-2xl font-semibold text-white">Upload Audio File</h2>
            </div>

            <!-- Drop Zone -->
            <div 
              @drop="handleDrop"
              @dragover="handleDragOver"
              @dragleave="handleDragLeave"
              :class="[
                'relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 cursor-pointer',
                isDragging 
                  ? 'border-purple-400 bg-purple-400/10' 
                  : file 
                    ? 'border-green-400 bg-green-400/10' 
                    : 'border-gray-600 hover:border-purple-400 hover:bg-purple-400/5'
              ]"
            >
              <input 
                type="file" 
                accept="audio/*" 
                @change="handleFileChange" 
                class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                id="file-upload"
              />
              
              <div v-if="!file" class="space-y-4">
                <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto">
                  <Upload class="w-8 h-8 text-white" />
                </div>
                <div>
                  <p class="text-white font-medium text-lg mb-2">
                    {{ isDragging ? 'Drop your file here' : 'Drag & drop your audio file' }}
                  </p>
                  <p class="text-gray-400">or click to browse</p>
                  <p class="text-sm text-gray-500 mt-2">Supports MP3, WAV, FLAC, M4A</p>
                </div>
              </div>

              <div v-else class="space-y-4">
                <div class="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto">
                  <FileAudio class="w-8 h-8 text-white" />
                </div>
                <div>
                  <p class="text-green-400 font-medium text-lg">{{ file.name }}</p>
                  <p class="text-gray-400 text-sm">{{ (file.size / 1024 / 1024).toFixed(2) }} MB</p>
                  <button 
                    @click.stop="clearFile"
                    class="mt-2 text-red-400 hover:text-red-300 text-sm underline"
                  >
                    Remove file
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- YouTube URL Section -->
          <div class="bg-white/5 backdrop-blur-lg rounded-2xl p-8 border border-white/10 hover:border-red-400/50 transition-all duration-300">
            <div class="flex items-center mb-6">
              <Youtube class="w-6 h-6 text-red-400 mr-3" />
              <h2 class="text-2xl font-semibold text-white">YouTube URL</h2>
            </div>

            <div class="space-y-4">
              <div class="relative">
                <ExternalLink class="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input 
                  v-model="youtubeUrl" 
                  type="url" 
                  placeholder="https://youtube.com/watch?v=..."
                  :disabled="file"
                  class="w-full pl-12 pr-4 py-4 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300"
                />
                <button 
                  v-if="youtubeUrl && !file"
                  @click="clearUrl"
                  class="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-red-400 transition-colors"
                >
                  ✕
                </button>
              </div>
              
              <div class="bg-red-500/10 border border-red-500/20 rounded-lg p-4">
                <p class="text-red-300 text-sm">
                  <strong>Note:</strong> Paste any YouTube video URL to extract and convert the audio to lofi.
                </p>
              </div>

              <div v-if="youtubeUrl && !file" class="bg-green-500/10 border border-green-500/20 rounded-lg p-4">
                <p class="text-green-300 text-sm flex items-center">
                  <span class="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
                  YouTube URL detected and ready for conversion
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Convert Button -->
        <div class="text-center">
          <button 
            @click="convertToLofi" 
            :disabled="!hasInput"
            :class="[
              'group relative px-12 py-4 rounded-2xl font-bold text-lg transition-all duration-300 transform',
              hasInput 
                ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:from-purple-600 hover:to-pink-600 hover:scale-105 hover:shadow-2xl hover:shadow-purple-500/25' 
                : 'bg-gray-700 text-gray-400 cursor-not-allowed'
            ]"
          >
            <div class="flex items-center justify-center">
              <Sparkles class="w-6 h-6 mr-3" />
              <span>Convert to LoFi</span>
            </div>
            
            <!-- Animated background for enabled state -->
            <div v-if="hasInput" class="absolute inset-0 rounded-2xl bg-gradient-to-r from-purple-600 to-pink-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300 -z-10"></div>
          </button>
          
          <p v-if="!hasInput" class="text-gray-500 text-sm mt-3">
            Please upload a file or enter a YouTube URL to continue
          </p>
          <p v-else class="text-gray-300 text-sm mt-3">
            Ready to transform your music into chill lofi vibes ✨
          </p>
        </div>

        <!-- Features -->
        <div class="mt-16 grid md:grid-cols-3 gap-6">
          <div class="text-center p-6 bg-white/5 backdrop-blur-lg rounded-xl border border-white/10">
            <div class="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center mx-auto mb-4">
              <Music class="w-6 h-6 text-purple-400" />
            </div>
            <h3 class="text-white font-semibold mb-2">High Quality</h3>
            <p class="text-gray-400 text-sm">Preserve audio quality while adding lofi effects</p>
          </div>
          
          <div class="text-center p-6 bg-white/5 backdrop-blur-lg rounded-xl border border-white/10">
            <div class="w-12 h-12 bg-pink-500/20 rounded-lg flex items-center justify-center mx-auto mb-4">
              <Sparkles class="w-6 h-6 text-pink-400" />
            </div>
            <h3 class="text-white font-semibold mb-2">AI Powered</h3>
            <p class="text-gray-400 text-sm">Advanced algorithms for authentic lofi sound</p>
          </div>
          
          <div class="text-center p-6 bg-white/5 backdrop-blur-lg rounded-xl border border-white/10">
            <div class="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center mx-auto mb-4">
              <Upload class="w-6 h-6 text-blue-400" />
            </div>
            <h3 class="text-white font-semibold mb-2">Easy Upload</h3>
            <p class="text-gray-400 text-sm">Drag & drop files or paste YouTube URLs</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, #8b5cf6, #ec4899);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(to bottom, #7c3aed, #db2777);
}

/* Smooth transitions */
* {
  transition: all 0.2s ease;
}

/* Focus states */
button:focus,
input:focus {
  outline: none;
}

/* Gradient text animation */
@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.bg-clip-text {
  background-size: 200% 200%;
  animation: gradient 3s ease infinite;
}
</style>
