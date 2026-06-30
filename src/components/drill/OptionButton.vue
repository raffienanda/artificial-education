<template>
  <button
    :disabled="submitted"
    class="flex items-center gap-3 p-3 rounded-xl border text-left transition-all duration-200 group relative overflow-hidden focus:outline-none"
    :class="stateClasses"
    @click="$emit('click')"
  >
    <!-- Label Letter -->
    <div
      class="w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm flex-shrink-0 transition-colors"
      :class="labelClasses"
    >
      {{ option.label }}
    </div>

    <!-- Option Text -->
    <span class="flex-1 text-sm font-medium" :class="textClasses">
      {{ option.text }}
    </span>

    <!-- Status Icon -->
    <div v-if="submitted && correct && selected" class="flex-shrink-0">
      <div class="w-6 h-6 rounded-full bg-success-500 flex items-center justify-center">
        <svg class="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
        </svg>
      </div>
    </div>
    <div v-else-if="submitted && selected && !correct" class="flex-shrink-0">
      <div class="w-6 h-6 rounded-full bg-danger-500 flex items-center justify-center">
        <svg class="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </div>
    </div>
  </button>
</template>

<script setup>
/**
 * OptionButton — Answer option for 2×2 grid layout with check/cross icons
 */
import { computed } from 'vue'

const props = defineProps({
  option: { type: Object, required: true },
  selected: { type: Boolean, default: false },
  submitted: { type: Boolean, default: false },
  correct: { type: Boolean, default: false },
})

defineEmits(['click'])

const stateClasses = computed(() => {
  if (!props.submitted) {
    if (props.selected) {
      return 'border-primary-500 bg-primary-50/50 dark:bg-primary-900/10 dark:border-primary-600 ring-1 ring-primary-500'
    }
    return 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:border-primary-300 dark:hover:border-primary-700 hover:bg-gray-50 dark:hover:bg-gray-700/50 cursor-pointer'
  }

  if (props.correct && props.selected) {
    return 'border-success-500 bg-success-50/50 dark:bg-success-900/10 dark:border-success-600 ring-1 ring-success-500'
  }

  if (props.correct && !props.selected) {
    return 'border-success-300 bg-success-50/30 dark:bg-success-900/5 dark:border-success-700'
  }

  if (props.selected && !props.correct) {
    return 'border-danger-500 bg-danger-50/50 dark:bg-danger-900/10 dark:border-danger-600 ring-1 ring-danger-500'
  }

  return 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 opacity-50 cursor-not-allowed'
})

const labelClasses = computed(() => {
  if (!props.submitted) {
    if (props.selected) return 'bg-primary-500 text-white'
    return 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400'
  }

  if (props.correct && props.selected) return 'bg-success-500 text-white'
  if (props.correct) return 'bg-success-100 text-success-600 dark:bg-success-900/30 dark:text-success-400'
  if (props.selected && !props.correct) return 'bg-danger-500 text-white'

  return 'bg-gray-100 dark:bg-gray-700 text-gray-400 dark:text-gray-500'
})

const textClasses = computed(() => {
  if (!props.submitted) {
    if (props.selected) return 'text-primary-700 dark:text-primary-300'
    return 'text-gray-700 dark:text-gray-300'
  }

  if (props.correct) return 'text-success-700 dark:text-success-300'
  if (props.selected && !props.correct) return 'text-danger-700 dark:text-danger-300'

  return 'text-gray-500 dark:text-gray-500'
})
</script>
