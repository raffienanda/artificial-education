<template>
  <div
    class="flex items-end gap-2 animate-fade-in-up"
    :class="isUser ? 'flex-row-reverse' : 'flex-row'"
  >
    <!-- AI Avatar -->
    <div
      v-if="!isUser"
      class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center flex-shrink-0 shadow-sm mb-1"
    >
      <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
      </svg>
    </div>

    <!-- Message Bubble -->
    <div class="flex flex-col gap-1 max-w-[85%]">
      <div
        :class="[
          'px-4 py-2.5 shadow-sm',
          isUser ? 'chat-bubble-user' : 'chat-bubble-ai',
        ]"
      >
        <!-- AI message: render markdown -->
        <div v-if="!isUser" class="markdown-body text-[13px] leading-relaxed" v-html="renderedContent"></div>
        <!-- User message: plain text -->
        <p v-else class="text-[13px] leading-relaxed whitespace-pre-wrap">{{ message.content }}</p>
      </div>
      <span
        class="text-[10px] text-gray-400 font-medium px-1"
        :class="isUser ? 'text-right' : 'text-left'"
      >
        {{ timeFormatted }}
      </span>
    </div>
  </div>
</template>

<script setup>
/**
 * ChatBubble — Individual chat message with Markdown rendering for AI messages
 */
import { computed } from 'vue'
import { marked } from 'marked'

const props = defineProps({
  message: { type: Object, required: true },
})

const isUser = computed(() => props.message.role === 'user')

const renderedContent = computed(() => {
  if (isUser.value) return props.message.content
  return marked(props.message.content || '', { breaks: true })
})

const timeFormatted = computed(() => {
  try {
    const d = new Date(props.message.timestamp)
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } catch {
    return ''
  }
})
</script>

<style>
.markdown-body p { margin-bottom: 0.5em; }
.markdown-body p:last-child { margin-bottom: 0; }
.markdown-body strong { font-weight: 600; }
.markdown-body em { font-style: italic; }
.markdown-body ul { list-style-type: disc; padding-left: 1.5em; margin-bottom: 0.5em; }
.markdown-body ol { list-style-type: decimal; padding-left: 1.5em; margin-bottom: 0.5em; }
.markdown-body li { margin-bottom: 0.25em; }
</style>
