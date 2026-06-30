<template>
  <div class="h-full flex flex-col bg-white dark:bg-gray-800 border-l border-gray-100 dark:border-gray-700 shadow-soft z-20">
    <!-- Header -->
    <div class="p-4 border-b border-gray-100 dark:border-gray-700 flex items-center justify-between bg-white dark:bg-gray-800 z-10">
      <div class="flex items-center gap-2.5">
        <h2 class="text-base font-bold text-gray-900 dark:text-white">Chatbot AI</h2>
      </div>
      <div class="flex items-center gap-2">
        <span class="flex items-center gap-1.5 text-xs text-success-500 font-medium">
          <span class="w-2 h-2 bg-success-500 rounded-full"></span>
          Online
        </span>
        <!-- Mobile close -->
        <button class="lg:hidden text-gray-400 hover:text-gray-600 ml-2" @click="$emit('close')">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <!-- Menu dots -->
        <button class="hidden lg:block text-gray-400 hover:text-gray-600">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Messages Area -->
    <div class="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-hide bg-surface-50 dark:bg-gray-900/50" ref="messagesContainer">
      <ChatBubble v-for="msg in messages" :key="msg.id" :message="msg" />

      <!-- Typing indicator -->
      <div v-if="isTyping" class="flex items-end gap-2">
        <div class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center flex-shrink-0">
          <svg class="w-4 h-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
          </svg>
        </div>
        <div class="bg-white dark:bg-gray-800 px-3 py-2 rounded-2xl rounded-bl-none shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-1">
          <span class="typing-dot"></span>
          <span class="typing-dot"></span>
          <span class="typing-dot"></span>
        </div>
      </div>
    </div>

    <!-- Quick Replies -->
    <div class="px-4 pt-3 pb-1 bg-white dark:bg-gray-800 border-t border-gray-50 dark:border-gray-700/50 flex-shrink-0">
      <div class="flex flex-col gap-2">
        <button
          v-for="reply in quickReplies"
          :key="reply.id"
          class="px-3 py-2 rounded-xl border border-primary-200 dark:border-primary-700 text-sm text-primary-600 dark:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors text-left"
          @click="sendMessage(reply.text)"
        >
          {{ reply.text }}
        </button>
      </div>
    </div>

    <!-- Input -->
    <div class="p-3 bg-white dark:bg-gray-800 border-t border-gray-100 dark:border-gray-700 flex-shrink-0">
      <MessageInput :disabled="isTyping" placeholder="Ketik pertanyaanmu di sini..." @send="sendMessage" />
    </div>
  </div>
</template>

<script setup>
/**
 * ChatbotPanel — Redesigned to match reference with Indonesian labels and vertical quick replies
 */
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { useChatbotStore } from '@/stores/chatbot'
import { quickReplies as quickRepliesData } from '@/data/conversations'
import ChatBubble from './ChatBubble.vue'
import MessageInput from './MessageInput.vue'

defineEmits(['close'])

const chatbotStore = useChatbotStore()
const messagesContainer = ref(null)

const messages = computed(() => chatbotStore.messages)
const isTyping = computed(() => chatbotStore.isTyping)
const quickReplies = ref(quickRepliesData)

async function sendMessage(text) {
  await chatbotStore.sendMessage(text)
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

watch(messages, scrollToBottom, { deep: true })
watch(isTyping, scrollToBottom)

onMounted(async () => {
  if (messages.value.length === 0) {
    await chatbotStore.fetchConversation()
  }
  scrollToBottom()
})
</script>
