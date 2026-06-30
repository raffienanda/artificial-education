/**
 * Progress Store — Mastery data, BKT, radar chart, and recommendations
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { progressService } from '@/services/progress'

export const useProgressStore = defineStore('progress', () => {
  // State
  const overallMastery = ref(0)
  const subtopicMastery = ref([])
  const radarChartData = ref(null)
  const recentActivities = ref([])
  const recommendations = ref(null)
  const weeklyProgress = ref([])
  const loading = ref(false)

  // Computed
  const weakSubtopics = computed(() =>
    subtopicMastery.value.filter((s) => s.mastery < 70)
  )

  const masteredSubtopics = computed(() =>
    subtopicMastery.value.filter((s) => s.mastery >= 90)
  )

  const masteryColor = computed(() => {
    if (overallMastery.value >= 90) return 'text-success-500'
    if (overallMastery.value >= 70) return 'text-primary-600'
    if (overallMastery.value >= 50) return 'text-warning-500'
    return 'text-danger-500'
  })

  // Actions
  async function fetchMastery() {
    loading.value = true
    try {
      const data = await progressService.getMastery()
      overallMastery.value = data.overall
      subtopicMastery.value = data.subtopics
    } finally {
      loading.value = false
    }
  }

  async function fetchRadarChart() {
    try {
      radarChartData.value = await progressService.getRadarChartData()
    } catch (err) {
      console.error('Failed to fetch radar chart data:', err)
    }
  }

  async function fetchRecentActivities() {
    try {
      recentActivities.value = await progressService.getRecentActivities()
    } catch (err) {
      console.error('Failed to fetch recent activities:', err)
    }
  }

  async function fetchRecommendations() {
    try {
      recommendations.value = await progressService.getRecommendations()
    } catch (err) {
      console.error('Failed to fetch recommendations:', err)
    }
  }

  async function fetchWeeklyProgress() {
    try {
      weeklyProgress.value = await progressService.getWeeklyProgress()
    } catch (err) {
      console.error('Failed to fetch weekly progress:', err)
    }
  }

  async function fetchAll() {
    await Promise.all([
      fetchMastery(),
      fetchRadarChart(),
      fetchRecentActivities(),
      fetchRecommendations(),
      fetchWeeklyProgress(),
    ])
  }

  return {
    overallMastery,
    subtopicMastery,
    radarChartData,
    recentActivities,
    recommendations,
    weeklyProgress,
    loading,
    weakSubtopics,
    masteredSubtopics,
    masteryColor,
    fetchMastery,
    fetchRadarChart,
    fetchRecentActivities,
    fetchRecommendations,
    fetchWeeklyProgress,
    fetchAll,
  }
})
