/**
 * Quiz Service
 * Mock API calls for practice drill questions and answer submission.
 */
import { delay } from './api'
import { questions } from '@/data/questions'

export const quizService = {
  /** Fetch quiz questions, optionally filtered by module */
  async getQuestions(moduleId = null) {
    await delay(300)
    if (moduleId) {
      return questions.filter((q) => q.moduleId === moduleId)
    }
    return [...questions]
  },

  /**
   * Submit an answer and get feedback.
   * In production, this would also update BKT probabilities on the server.
   */
  async submitAnswer(questionId, selectedAnswer) {
    await delay(400)
    const question = questions.find((q) => q.id === questionId)
    if (!question) throw new Error(`Question ${questionId} not found`)

    const isCorrect = question.correctAnswer === selectedAnswer
    return {
      correct: isCorrect,
      correctAnswer: question.correctAnswer,
      explanation: question.explanation,
    }
  },

  /** Fetch explanation for a specific question */
  async getExplanation(questionId) {
    await delay(200)
    const question = questions.find((q) => q.id === questionId)
    if (!question) throw new Error(`Question ${questionId} not found`)
    return {
      explanation: question.explanation,
      correctAnswer: question.correctAnswer,
    }
  },
}
