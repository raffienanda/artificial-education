<template>
  <form @submit.prevent="handleSubmit" class="relative flex items-end gap-2">
    <div class="relative flex-1 bg-gray-50 dark:bg-gray-700/50 rounded-xl border border-gray-200 dark:border-gray-600 focus-within:ring-2 focus-within:ring-primary-500/30 focus-within:border-primary-500 transition-all duration-200">
      <textarea
        ref="inputRef"
        v-model="message"
        rows="1"
        :placeholder="placeholder"
        class="w-full bg-transparent text-sm text-gray-800 dark:text-gray-200 placeholder-gray-400 outline-none resize-none py-2.5 px-4 max-h-32 scrollbar-hide block"
        :disabled="disabled"
        @input="autoResize"
        @keydown.enter.prevent="handleEnter"
      />
    </div>

    <button
      type="submit"
      :disabled="!message.trim() || disabled"
      :class="[
        'w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 transition-all duration-200 focus:outline-none',
        message.trim() && !disabled
          ? 'bg-primary-600 text-white hover:bg-primary-700'
          : 'bg-gray-200 text-gray-400 dark:bg-gray-700 dark:text-gray-500 cursor-not-allowed'
      ]"
    >
      <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
      </svg>
    </button>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  disabled: { type: Boolean, default: false },
  placeholder: { type: String, default: 'Ketik pertanyaanmu di sini...' },
})

const emit = defineEmits(['send'])
const message = ref('')
const inputRef = ref(null)

function autoResize() {
  const el = inputRef.value
  if (!el) return
  el.style.height = 'auto'
  el.style.height = Math.min(el.scrollHeight, 128) + 'px'
}

function handleSubmit() {
  if (message.value.trim() && !props.disabled) {
    emit('send', message.value)
    message.value = ''
    if (inputRef.value) inputRef.value.style.height = 'auto'
  }
}

function handleEnter(e) {
  if (!e.shiftKey) handleSubmit()
}

watch(message, (val) => {
  if (!val && inputRef.value) inputRef.value.style.height = 'auto'
})
</script>
