/**
 * Progress Service
 * Mock API calls for progress, mastery, and BKT data.
 */
import { delay } from './api'
import { overallMastery, subtopicMastery, radarChartData, recentActivities, weeklyProgress } from '@/data/progress'
import { recommendations } from '@/data/recommendations'

export const progressService = {
  /** Fetch overall mastery percentage */
  async getMastery() {
    await delay(300)
    return { overall: overallMastery, subtopics: [...subtopicMastery] }
  },

  /** Fetch radar chart data */
  async getRadarChartData() {
    await delay(200)
    return { ...radarChartData }
  },

  /** Fetch BKT (Bayesian Knowledge Tracing) data */
  async getBKTData() {
    await delay(300)
    return subtopicMastery.map((s) => ({
      name: s.name,
      ...s.bkt,
    }))
  },

  /** Fetch recent activities */
  async getRecentActivities() {
    await delay(200)
    return [...recentActivities]
  },

  /** Fetch AI recommendations */
  async getRecommendations() {
    await delay(400)
    return { ...recommendations }
  },

  /** Fetch weekly progress data */
  async getWeeklyProgress() {
    await delay(200)
    return [...weeklyProgress]
  },
}
