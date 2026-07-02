import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { recommendationService } from '@/services/recommendation'

const actionLabels = {
  show_text: 'Baca ringkasan',
  show_video: 'Tonton video',
  easy_quiz: 'Kerjakan quiz mudah',
  hard_quiz: 'Kerjakan quiz tantangan',
  review_previous: 'Review materi sebelumnya',
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

  const microAction = computed(() => current.value?.micro_action || 'easy_quiz')
  const microActionLabel = computed(() => actionLabels[microAction.value] || microAction.value)
  const macroActionLabel = computed(() => macroLabels[current.value?.macro_action] || 'Menunggu analisis')
  const shouldBackTrace = computed(() => current.value?.macro_action === 'back_trace')

  async function fetchNext({ userId = 1, currentModuleId, currentSubtopicId }) {
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
      return data
    } catch (err) {
      error.value = err.message || 'Gagal memuat rekomendasi'
      return null
    } finally {
      loading.value = false
    }
  }

  async function fetchLogs({ userId = 1, limit = 8 } = {}) {
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

  function clear() {
    current.value = null
    error.value = null
  }

  return {
    current,
    logs,
    loading,
    logsLoading,
    error,
    microAction,
    microActionLabel,
    macroActionLabel,
    shouldBackTrace,
    fetchNext,
    fetchLogs,
    clear,
  }
})
