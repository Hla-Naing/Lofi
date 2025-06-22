<!-- src/components/SoundEffects.vue -->
<script setup>
import { useForm, useField } from 'vee-validate'
import * as yup from 'yup'

// Define validation schema
const schema = yup.object({
  Reverb: yup
    .number()
    .typeError('Reverb must be a number')
    .required('Reverb is required')
    .min(0, 'Reverb must be at least 0')
    .max(100, 'Reverb must be 100 or less'),

  PitchShift: yup
    .number()
    .typeError('PitchShift must be a number')
    .required('PitchShift is required')
    .min(-12, 'Min is -12')
    .max(12, 'Max is 12'),

  LowpassFilter: yup
    .number()
    .typeError('Lowpass must be a number')
    .required('LowpassFilter is required')
    .min(100, 'Min is 100Hz')
    .max(20000, 'Max is 20000Hz'),

  Distortion: yup
    .number()
    .typeError('Distortion must be a number')
    .required('Distortion is required')
    .min(0, 'Min is 0')
    .max(100, 'Max is 100'),

  Gain: yup
    .number()
    .typeError('Gain must be a number')
    .required('Gain is required')
    .min(-20, 'Min is -20')
    .max(20, 'Max is 20'),

  Speed: yup
    .number()
    .typeError('Speed must be a number')
    .required('Speed is required')
    .min(50, 'Min is 50%')
    .max(150, 'Max is 150%'),
})


// Initialize the form
const { handleSubmit, meta } = useForm({
  validationSchema: schema,
})

// Register fields
const { value: Reverb, errorMessage: ReverbError } = useField('Reverb')
const { value: PitchShift, errorMessage: PitchShiftError } = useField('PitchShift')
const { value: LowpassFilter, errorMessage: LowpassError } = useField('LowpassFilter')
const { value: Distortion, errorMessage: DistortionError } = useField('Distortion')
const { value: Gain, errorMessage: GainError } = useField('Gain')
const { value: Speed, errorMessage: SpeedError } = useField('Speed')

// Handle submit
const onSubmit = handleSubmit(values => {
  console.log('🎛 Validated Values:', values)
  alert('Settings saved!')
})

</script>

<template>
  <div class="min-h-screen w-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white flex items-center justify-center p-6">
    <form @submit.prevent="onSubmit" class="w-full max-w-2xl bg-white/5 backdrop-blur-lg rounded-2xl p-10 border border-white/10 space-y-6">
      <h2 class="text-3xl font-bold text-center mb-4">Customize Sound Effects</h2>

      <!-- Field: Reverb -->
      <div>
        <label class="block mb-1 font-medium">Reverb</label>
        <input v-model="Reverb" type="text" class="w-full p-3 rounded-md bg-white/10 text-white border border-white/20 focus:ring-2 focus:ring-purple-400" />
        <p class="text-red-400 text-sm mt-1">{{ ReverbError }}</p>
      </div>

      <!-- Field: PitchShift -->
      <div>
        <label class="block mb-1 font-medium">PitchShift</label>
        <input v-model="PitchShift" type="text" class="w-full p-3 rounded-md bg-white/10 text-white border border-white/20 focus:ring-2 focus:ring-purple-400" />
        <p class="text-red-400 text-sm mt-1">{{ PitchShiftError }}</p>
      </div>

      <!-- Field: LowpassFilter -->
      <div>
        <label class="block mb-1 font-medium">LowpassFilter</label>
        <input v-model="LowpassFilter" type="text" class="w-full p-3 rounded-md bg-white/10 text-white border border-white/20 focus:ring-2 focus:ring-purple-400" />
        <p class="text-red-400 text-sm mt-1">{{ LowpassError }}</p>
      </div>

      <!-- Field: Distortion -->
      <div>
        <label class="block mb-1 font-medium">Distortion</label>
        <input v-model="Distortion" type="text" class="w-full p-3 rounded-md bg-white/10 text-white border border-white/20 focus:ring-2 focus:ring-purple-400" />
        <p class="text-red-400 text-sm mt-1">{{ DistortionError }}</p>
      </div>

      <!-- Field: Gain -->
      <div>
        <label class="block mb-1 font-medium">Gain</label>
        <input v-model="Gain" type="text" class="w-full p-3 rounded-md bg-white/10 text-white border border-white/20 focus:ring-2 focus:ring-purple-400" />
        <p class="text-red-400 text-sm mt-1">{{ GainError }}</p>
      </div>

      <!-- Field: Speed -->
      <div>
        <label class="block mb-1 font-medium">Speed</label>
        <input v-model="Speed" type="text" class="w-full p-3 rounded-md bg-white/10 text-white border border-white/20 focus:ring-2 focus:ring-purple-400" />
        <p class="text-red-400 text-sm mt-1">{{ SpeedError }}</p>
      </div>

      <!-- Submit Button -->
      <div class="text-center pt-4">
        <button type="submit" :disabled="!meta.valid" class="w-full py-3 rounded-xl font-bold text-lg bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 transition-all duration-300  disabled:opacity-40 disabled:cursor-not-allowed"">
          Save & Continue →
        </button>

      </div>
    </form>
  </div>
</template>

