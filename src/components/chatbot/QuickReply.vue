<template>
  <button
    class="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-[11px] font-medium text-gray-600 dark:text-gray-300 hover:bg-primary-50 hover:text-primary-600 hover:border-primary-200 dark:hover:bg-primary-900/30 dark:hover:text-primary-300 dark:hover:border-primary-800 transition-colors flex-shrink-0 shadow-sm cursor-pointer"
    @click="$emit('click', reply)"
  >
    <span>{{ reply.icon }}</span>
    <span>{{ reply.text }}</span>
  </button>
</template>

<script setup>
/**
 * QuickReply — Button for suggested chatbot messages
 */
defineProps({
  reply: { type: Object, required: true },
})
defineEmits(['click'])
</script>
