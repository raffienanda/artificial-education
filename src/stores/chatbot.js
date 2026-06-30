/**
 * Chatbot Store — AI tutor conversation state and message handling
 */
import { defineStore } from 'pinia'
import { ref, nextTick } from 'vue'
import { chatbotService } from '@/services/chatbot'

export const useChatbotStore = defineStore('chatbot', () => {
  // State
  const messages = ref([])
  const isTyping = ref(false)
  const loading = ref(false)

  // Actions
  async function fetchConversation() {
    loading.value = true
    try {
      messages.value = await chatbotService.getConversation()
    } finally {
      loading.value = false
    }
  }

  async function sendMessage(content) {
    if (!content.trim()) return

    // Add user message
    const userMessage = {
      id: `msg-user-${Date.now()}`,
      role: 'user',
      content: content.trim(),
      timestamp: new Date().toISOString(),
    }
    messages.value.push(userMessage)

    // Show typing indicator
    isTyping.value = true

    try {
      // Get AI response (includes simulated delay)
      const aiMessage = await chatbotService.sendMessage(content.trim())
      messages.value.push(aiMessage)
    } catch (err) {
      // Add error message
      messages.value.push({
        id: `msg-error-${Date.now()}`,
        role: 'ai',
        content: 'Maaf, terjadi kesalahan. Silakan coba lagi.',
        timestamp: new Date().toISOString(),
        isError: true,
      })
    } finally {
      isTyping.value = false
    }
  }

  function clearConversation() {
    messages.value = []
  }

  return {
    messages,
    isTyping,
    loading,
    fetchConversation,
    sendMessage,
    clearConversation,
  }
})
