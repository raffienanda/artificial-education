/**
 * Progress Store — Student mastery tracking, radar chart, history, and weekly data
 * Connected to FastAPI backend via centralized API instance
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'
import { useUserStore } from './user'
import { radarChartData as initialRadar } from '@/data/progress' // Keep chart layout/styling

export const useProgressStore = defineStore('progress', () => {
  // State
  const overallMastery = ref(0)
  const subtopicMastery = ref([])
  const radarChartData = ref(JSON.parse(JSON.stringify(initialRadar))) // Clone dummy format
  const recentActivities = ref([])
  const weeklyProgress = ref([])
  const recommendations = ref(null)
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
  function updateProgress(topicId, newMastery) {
    const topicIndex = subtopicMastery.value.findIndex(t => t.topic_id === topicId)

    if (topicIndex !== -1) {
      subtopicMastery.value[topicIndex].mastery = newMastery
    } else {
      subtopicMastery.value.push({ topic_id: topicId, mastery: newMastery, status: 'learning' })
    }

    // Refresh chart
    if (radarChartData.value && radarChartData.value.datasets[0]) {
      radarChartData.value.datasets[0].data = subtopicMastery.value.map(s => s.mastery)
      radarChartData.value = { ...radarChartData.value }
    }

    // Refresh overall
    fetchOverall()
  }

  async function fetchOverall() {
    try {
      const userStore = useUserStore()
      const data = await api.get('/progress/overall', { params: { user_id: userStore.userId } })
      overallMastery.value = data.overall
    } catch (e) {
      console.error(e)
    }
  }

  // Load mastery data from backend
  async function fetchMastery() {
    loading.value = true
    try {
      const userStore = useUserStore()
      const data = await api.get('/progress', { params: { user_id: userStore.userId } })
      subtopicMastery.value = data

      if (radarChartData.value && radarChartData.value.datasets[0]) {
        radarChartData.value.datasets[0].data = data.map(s => s.mastery)
        radarChartData.value = { ...radarChartData.value }
      }

      await fetchOverall()
    } catch (e) {
      console.error("Error fetching progress:", e)
    } finally {
      loading.value = false
    }
  }

  // Load recent learning activities from backend (per user)
  async function fetchHistory() {
    try {
      const userStore = useUserStore()
      const data = await api.get('/progress/history', { params: { user_id: userStore.userId, limit: 10 } })
      recentActivities.value = data
    } catch (e) {
      console.error("Error fetching learning history:", e)
      recentActivities.value = []
    }
  }

  // Load weekly study time from backend (per user)
  async function fetchWeeklyProgress() {
    try {
      const userStore = useUserStore()
      const data = await api.get('/progress/weekly', { params: { user_id: userStore.userId } })
      weeklyProgress.value = data
    } catch (e) {
      console.error("Error fetching weekly progress:", e)
      weeklyProgress.value = []
    }
  }

  // Load dynamic status message from backend (per user)
  async function fetchStatusMessage() {
    try {
      const userStore = useUserStore()
      const data = await api.get('/progress/status-message', { params: { user_id: userStore.userId } })
      recommendations.value = data
    } catch (e) {
      console.error("Error fetching status message:", e)
      recommendations.value = null
    }
  }

  // Fetch all progress data in parallel
  async function fetchAll() {
    await Promise.all([
      fetchMastery(),
      fetchHistory(),
      fetchWeeklyProgress(),
      fetchStatusMessage(),
    ])
  }

  return {
    overallMastery,
    subtopicMastery,
    radarChartData,
    recentActivities,
    weeklyProgress,
    recommendations,
    loading,
    weakSubtopics,
    masteredSubtopics,
    masteryColor,
    updateProgress,
    fetchMastery,
    fetchHistory,
    fetchWeeklyProgress,
    fetchStatusMessage,
    fetchAll,
  }
})
