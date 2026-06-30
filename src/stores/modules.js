/**
 * Modules Store — Learning modules, subtopics, and navigation state
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { modulesService } from '@/services/modules'

export const useModulesStore = defineStore('modules', () => {
  // State
  const modules = ref([])
  const activeModule = ref(null)
  const activeSubtopicIndex = ref(0)
  const loading = ref(false)
  const error = ref(null)

  // Computed
  const activeSubtopic = computed(() => {
    if (!activeModule.value?.subtopics) return null
    return activeModule.value.subtopics[activeSubtopicIndex.value] || null
  })

  const activeContent = computed(() => {
    return activeSubtopic.value?.content || null
  })

  const totalSubtopics = computed(() => {
    return activeModule.value?.subtopics?.length || 0
  })

  const hasNextSubtopic = computed(() => {
    return activeSubtopicIndex.value < totalSubtopics.value - 1
  })

  const hasPreviousSubtopic = computed(() => {
    return activeSubtopicIndex.value > 0
  })

  const completedModules = computed(() =>
    modules.value.filter((m) => m.status === 'completed')
  )

  const currentModuleProgress = computed(() => {
    if (!activeModule.value?.subtopics) return 0
    const completed = activeModule.value.subtopics.filter((s) => s.completed).length
    return Math.round((completed / activeModule.value.subtopics.length) * 100)
  })

  // Actions
  async function fetchModules() {
    loading.value = true
    error.value = null
    try {
      const data = await modulesService.getModules()
      modules.value = data
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  async function fetchModuleById(moduleId) {
    loading.value = true
    error.value = null
    try {
      const data = await modulesService.getModuleById(moduleId)
      activeModule.value = data
      activeSubtopicIndex.value = 0
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  function setActiveModule(mod) {
    activeModule.value = mod
    activeSubtopicIndex.value = 0
  }

  function nextSubtopic() {
    if (hasNextSubtopic.value) {
      activeSubtopicIndex.value++
    }
  }

  function previousSubtopic() {
    if (hasPreviousSubtopic.value) {
      activeSubtopicIndex.value--
    }
  }

  function goToSubtopic(index) {
    if (index >= 0 && index < totalSubtopics.value) {
      activeSubtopicIndex.value = index
    }
  }

  return {
    modules,
    activeModule,
    activeSubtopicIndex,
    loading,
    error,
    activeSubtopic,
    activeContent,
    totalSubtopics,
    hasNextSubtopic,
    hasPreviousSubtopic,
    completedModules,
    currentModuleProgress,
    fetchModules,
    fetchModuleById,
    setActiveModule,
    nextSubtopic,
    previousSubtopic,
    goToSubtopic,
  }
})
