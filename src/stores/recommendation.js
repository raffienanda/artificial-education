import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { recommendationService } from '@/services/recommendation'

const actionLabels = {
  show_text: 'Baca ringkasan',
  show_video: 'Tonton video',
  easy_quiz: 'Latihan ringan',
  hard_quiz: 'Tantangan',
  review_previous: 'Ulang materi',
}

const macroLabels = {
  continue: 'Lanjutkan jalur saat ini',
  back_trace: 'Kembali ke prasyarat',
}

export const useRecommendationStore = defineStore('recommendation', () => {
  const current = ref(null)
  const logs = ref([])
  const loading = ref(false)
  const logsLoading = ref(false)
  const error = ref(null)
  const activeLearningAction = ref(null)
  const learningActionTrace = ref([])

  const microAction = computed(() => current.value?.micro_action || 'easy_quiz')
  const microActionLabel = computed(() => actionLabels[microAction.value] || microAction.value)
  const macroActionLabel = computed(() => macroLabels[current.value?.macro_action] || 'Menunggu analisis')
  const shouldBackTrace = computed(() => current.value?.macro_action === 'back_trace')

  async function fetchNext({ userId, currentModuleId, currentSubtopicId }) {
    if (!currentModuleId || !currentSubtopicId) return null

    loading.value = true
    error.value = null

    try {
      const data = await recommendationService.getNextRecommendation({
        userId,
        currentModuleId,
        currentSubtopicId,
      })
      current.value = data
      if (!activeLearningAction.value) {
        activeLearningAction.value = data.micro_action || null
      }
      return data
    } catch (err) {
      error.value = err.message || 'Gagal memuat rekomendasi'
      return null
    } finally {
      loading.value = false
    }
  }

  async function fetchLogs({ userId, limit = 8 } = {}) {
    logsLoading.value = true

    try {
      logs.value = await recommendationService.getInteractionLogs({ userId, limit })
      return logs.value
    } catch (err) {
      error.value = err.message || 'Gagal memuat riwayat adaptasi'
      return []
    } finally {
      logsLoading.value = false
    }
  }

  function setActiveLearningAction(action) {
    activeLearningAction.value = action || null
    if (!action) return
    const lastAction = learningActionTrace.value[learningActionTrace.value.length - 1]
    if (lastAction !== action) {
      learningActionTrace.value.push(action)
    }
  }

  function resetLearningActionTrace(initialAction = null) {
    learningActionTrace.value = []
    activeLearningAction.value = null
    if (initialAction) {
      setActiveLearningAction(initialAction)
    }
  }

  function clear() {
    current.value = null
    error.value = null
    activeLearningAction.value = null
    learningActionTrace.value = []
  }

  return {
    current,
    logs,
    loading,
    logsLoading,
    error,
    activeLearningAction,
    learningActionTrace,
    microAction,
    microActionLabel,
    macroActionLabel,
    shouldBackTrace,
    fetchNext,
    fetchLogs,
    setActiveLearningAction,
    resetLearningActionTrace,
    clear,
  }
})
