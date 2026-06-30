<template>
  <div class="bg-gray-50 dark:bg-gray-800/80 p-5 rounded-2xl border border-gray-100 dark:border-gray-700">
    <h3 class="text-[15px] font-medium text-gray-800 dark:text-gray-100 leading-relaxed">
      {{ question }}
    </h3>
  </div>
</template>

<script setup>
/**
 * QuestionCard — Displays the text of the current quiz question
 */
defineProps({
  question: { type: String, required: true },
})
</script>
