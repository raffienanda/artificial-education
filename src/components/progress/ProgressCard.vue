<template>
  <div class="bg-gray-50 dark:bg-gray-800/50 rounded-xl p-3 border border-gray-100 dark:border-gray-700">
    <div class="flex items-center justify-between mb-2">
      <h4 class="text-sm font-medium text-gray-800 dark:text-gray-200">{{ subtopic.name }}</h4>
      <span class="text-sm font-bold" :class="colorClass">{{ subtopic.mastery }}%</span>
    </div>
    <div class="progress-bar h-1.5 bg-gray-200 dark:bg-gray-700">
      <div class="progress-bar-fill" :class="bgClass" :style="{ width: subtopic.mastery + '%' }" />
    </div>
    <div class="mt-2 flex items-center justify-between text-[10px] text-gray-500">
      <span>P(Know): {{ (subtopic.bkt.pKnown * 100).toFixed(0) }}%</span>
      <span :class="statusClass">{{ statusText }}</span>
    </div>
  </div>
</template>

<script setup>
/**
 * ProgressCard — Individual subtopic mastery card with progress bar
 */
import { computed } from 'vue'

const props = defineProps({
  subtopic: { type: Object, required: true },
})

const colorClass = computed(() => {
  if (props.subtopic.mastery >= 90) return 'text-success-500'
  if (props.subtopic.mastery >= 70) return 'text-primary-500'
  if (props.subtopic.mastery >= 50) return 'text-warning-500'
  return 'text-danger-500'
})

const bgClass = computed(() => {
  if (props.subtopic.mastery >= 90) return 'bg-success-500'
  if (props.subtopic.mastery >= 70) return 'bg-primary-500'
  if (props.subtopic.mastery >= 50) return 'bg-warning-500'
  return 'bg-danger-500'
})

const statusText = computed(() => {
  if (props.subtopic.status === 'mastered') return 'Mastered'
  if (props.subtopic.status === 'proficient') return 'Proficient'
  if (props.subtopic.status === 'learning') return 'Learning'
  return 'Needs Review'
})

const statusClass = computed(() => {
  if (props.subtopic.status === 'mastered') return 'text-success-600 dark:text-success-400 font-medium'
  if (props.subtopic.status === 'proficient') return 'text-primary-600 dark:text-primary-400 font-medium'
  return ''
})
</script>
