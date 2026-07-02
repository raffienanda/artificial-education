/**
 * Progress Store — Student mastery tracking and radar chart data
 * Connected to FastAPI backend via centralized API instance
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'
import { useUserStore } from './user'
import { radarChartData as initialRadar } from '@/data/progress' // Keep layout

export const useProgressStore = defineStore('progress', () => {
  // State
  const overallMastery = ref(0)
  const subtopicMastery = ref([]) 
  const radarChartData = ref(JSON.parse(JSON.stringify(initialRadar))) // Clone dummy format
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

  // Load data dari backend
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

  // Alias for DashboardPage.vue compatibility
  async function fetchAll() {
    await fetchMastery()
  }

  return {
    overallMastery,
    subtopicMastery,
    radarChartData,
    loading,
    weakSubtopics,
    masteredSubtopics,
    masteryColor,
    updateProgress,
    fetchMastery,
    fetchAll,
  }
})
