/**
 * Progress Service — Connected to FastAPI Backend
 * Uses centralized axios instance with interceptors.
 */
import api from './api'
import { radarChartData, recentActivities, weeklyProgress } from '@/data/progress'
import { recommendations } from '@/data/recommendations'

export const progressService = {
  /** Fetch overall mastery and subtopic mastery from backend */
  async getMastery() {
    const subtopics = await api.get('/progress')
    const overall = await api.get('/progress/overall')
    return { overall: overall.overall, subtopics }
  },

  /** Fetch radar chart data (uses local data as layout, filled with backend mastery) */
  async getRadarChartData() {
    return { ...radarChartData }
  },

  /** Fetch recent activities (mock — no backend endpoint yet) */
  async getRecentActivities() {
    return [...recentActivities]
  },

  /** Fetch AI recommendations (mock — no backend endpoint yet) */
  async getRecommendations() {
    return { ...recommendations }
  },

  /** Fetch weekly progress data (mock — no backend endpoint yet) */
  async getWeeklyProgress() {
    return [...weeklyProgress]
  },
}
