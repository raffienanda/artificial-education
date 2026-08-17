/**
 * Progress Service — Connected to FastAPI Backend
 * All data is now fetched from backend endpoints per user.
 */
import api from './api'

export const progressService = {
  /** Fetch overall mastery and subtopic mastery from backend */
  async getMastery(userId) {
    const subtopics = await api.get('/progress', { params: { user_id: userId } })
    const overall = await api.get('/progress/overall', { params: { user_id: userId } })
    return { overall: overall.overall, subtopics }
  },

  /** Fetch recent learning activities from backend (per user) */
  async getRecentActivities(userId, limit = 10) {
    return api.get('/progress/history', { params: { user_id: userId, limit } })
  },

  /** Fetch weekly study time from backend (per user) */
  async getWeeklyProgress(userId) {
    return api.get('/progress/weekly', { params: { user_id: userId } })
  },

  /** Fetch dynamic status message from backend (per user) */
  async getStatusMessage(userId) {
    return api.get('/progress/status-message', { params: { user_id: userId } })
  },
}
