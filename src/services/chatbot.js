/**
 * Chatbot Service
 * Backend API calls for tutor chatbot.
 */
import api from './api'

export const chatbotService = {
  async getConversation() {
    return api.get('/chatbot/conversation')
  },

  async sendMessage(message) {
    return api.post('/chatbot/message', { message })
  },
}
