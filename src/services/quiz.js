/**
 * Quiz Service — Connected to FastAPI Backend
 * Uses centralized axios instance with interceptors.
 */
import api from './api'

export const quizService = {
  /** Fetch quiz questions for a module */
  async getQuestions(moduleId = null) {
    if (moduleId) {
      const data = await api.get(`/quiz/${moduleId}`)
      return data
    }
    return []
  },

  /**
   * Submit an answer and get feedback with BKT update from backend.
   */
  async submitAnswer(questionId, selectedAnswer, userId = 1) {
    const data = await api.post('/quiz/submit', {
      question_id: questionId,
      selected_option_id: selectedAnswer,
      user_id: userId,
    })
    return data
  },
}
