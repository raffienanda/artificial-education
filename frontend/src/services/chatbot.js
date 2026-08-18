/**
 * Chatbot Service
 * Backend API calls for tutor chatbot.
 */
import api from './api'

export const chatbotService = {
  async getConversation() {
    return api.get('/chatbot/conversation')
  },

  async sendMessage(message, context = {}) {
    return api.post('/chatbot/message', {
      message,
      module_id: context.moduleId || null,
      subtopic_id: context.subtopicId || null,
    })
  },
}
