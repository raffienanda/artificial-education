import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { cognitiveService } from '@/services/cognitive'

const stageLabels = {
  dualism: 'Dualisme',
  multiplicity: 'Multiplisitas',
  relativism: 'Relativisme',
  commitment: 'Komitmen',
}

export const useCognitiveStore = defineStore('cognitive', () => {
  const items = ref([])
  const profile = ref(null)
  const responses = ref([])
  const loading = ref(false)
  const error = ref(null)

  const completed = computed(() => {
    if (!profile.value) return false
    return [
      profile.value.dualism_score,
      profile.value.multiplicity_score,
      profile.value.relativism_score,
      profile.value.commitment_score,
    ].some((score) => Number(score) > 0)
  })

  const dominantStage = computed(() => profile.value?.dominant_stage || 'unknown')
  const dominantStageLabel = computed(() => stageLabels[dominantStage.value] || 'Belum diisi')

  async function fetchItems() {
    if (items.value.length) return items.value
    loading.value = true
    error.value = null
    try {
      items.value = await cognitiveService.getItems()
      return items.value
    } catch (err) {
      error.value = err.response?.data?.detail || 'Gagal memuat instrumen kognitif'
      return []
    } finally {
      loading.value = false
    }
  }

  async function fetchProfile() {
    loading.value = true
    error.value = null
    try {
      profile.value = await cognitiveService.getProfile()
      return profile.value
    } catch (err) {
      error.value = err.response?.data?.detail || 'Gagal memuat profil kognitif'
      return null
    } finally {
      loading.value = false
    }
  }

  async function fetchResponses() {
    loading.value = true
    error.value = null
    try {
      responses.value = await cognitiveService.getResponses()
      return responses.value
    } catch (err) {
      error.value = err.response?.data?.detail || 'Gagal memuat jawaban profil kognitif'
      return []
    } finally {
      loading.value = false
    }
  }

  async function submit(responses) {
    loading.value = true
    error.value = null
    try {
      profile.value = await cognitiveService.submitResponses(responses)
      return profile.value
    } catch (err) {
      error.value = err.response?.data?.detail || 'Gagal menyimpan profil kognitif'
      await fetchProfile()
      await fetchResponses()
      return null
    } finally {
      loading.value = false
    }
  }

  function resetStoreState() {
    items.value = []
    profile.value = null
    responses.value = []
    error.value = null
  }

  return {
    items,
    profile,
    responses,
    loading,
    error,
    completed,
    dominantStage,
    dominantStageLabel,
    fetchItems,
    fetchProfile,
    fetchResponses,
    submit,
    resetStoreState,
  }
})
