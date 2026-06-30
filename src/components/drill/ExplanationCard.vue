<template>
  <div
    class="p-4 rounded-xl border"
    :class="[
      isCorrect
        ? 'bg-success-50 border-success-200 dark:bg-success-900/20 dark:border-success-800'
        : 'bg-danger-50 border-danger-200 dark:bg-danger-900/20 dark:border-danger-800'
    ]"
  >
    <div class="flex items-center gap-2 mb-2">
      <span class="text-lg">{{ isCorrect ? '✅' : '❌' }}</span>
      <h4
        class="text-sm font-bold"
        :class="isCorrect ? 'text-success-800 dark:text-success-300' : 'text-danger-800 dark:text-danger-300'"
      >
        {{ isCorrect ? 'Correct!' : 'Incorrect' }}
      </h4>
    </div>
    <p
      class="text-sm leading-relaxed"
      :class="isCorrect ? 'text-success-700 dark:text-success-400' : 'text-danger-700 dark:text-danger-400'"
    >
      {{ explanation }}
    </p>
  </div>
</template>

<script setup>
/**
 * ExplanationCard — Shows whether the answer was correct and provides an explanation
 */
defineProps({
  isCorrect: { type: Boolean, required: true },
  explanation: { type: String, required: true },
})
</script>
