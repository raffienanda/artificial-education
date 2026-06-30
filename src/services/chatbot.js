/**
 * Chatbot Service
 * Mock API calls for AI tutor chatbot with simulated typing delay.
 */
import { delay } from './api'
import { conversationHistory, aiResponses } from '@/data/conversations'

export const chatbotService = {
  /** Fetch conversation history */
  async getConversation() {
    await delay(300)
    return [...conversationHistory]
  },

  /**
   * Send a message and get an AI response.
   * In production, this would call the AI backend.
   */
  async sendMessage(message) {
    // Simulate AI thinking time
    await delay(1200)

    // Check if the message matches a known quick reply
    const knownResponse = aiResponses[message]
    if (knownResponse) {
      return {
        id: `msg-${Date.now()}`,
        role: 'ai',
        content: knownResponse,
        timestamp: new Date().toISOString(),
      }
    }

    // Default AI responses in Indonesian for unrecognized messages
    const defaultResponses = [
      `Pertanyaan yang bagus! 😊\n\nBerdasarkan materi yang sedang kamu pelajari, berikut yang bisa aku jelaskan:\n\nKunci utamanya adalah memahami konsep dasar dan berlatih secara rutin. Mau aku buatkan soal latihan untukmu?`,
      `Aku senang bisa membantu! 🎯\n\nMari kita bahas langkah-langkahnya:\n\n1. **Pahami konsep dasar** — Pastikan kamu memahami aturan dasarnya\n2. **Latihan rutin** — Pengulangan membantu memperkuat pemahaman\n3. **Review kesalahan** — Setiap kesalahan adalah kesempatan belajar\n\nMau aku jelaskan lebih detail?`,
      `Pertanyaan menarik! Mari kita bahas bersama 🔍\n\nDalam matematika, konsep ini berkaitan dengan operasi bilangan. Kuncinya adalah mengikuti aturan secara sistematis.\n\nMau lihat contoh penyelesaian langkah per langkah?`,
    ]

    const randomResponse = defaultResponses[Math.floor(Math.random() * defaultResponses.length)]

    return {
      id: `msg-${Date.now()}`,
      role: 'ai',
      content: randomResponse,
      timestamp: new Date().toISOString(),
    }
  },
}
