/**
 * Modules Store — Learning modules, subtopics, and navigation state
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { modulesService } from '@/services/modules'
import { useUserStore } from './user'

export const useModulesStore = defineStore('modules', () => {
  // State
  const course = ref(null)
  const courses = ref([])
  const selectedCourse = ref(null)
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
  async function fetchCourse() {
    error.value = null
    try {
      course.value = await modulesService.getCourse()
      if (!selectedCourse.value) selectedCourse.value = course.value
    } catch (err) {
      error.value = err.message
    }
  }

  async function fetchCourses() {
    error.value = null
    try {
      const data = await modulesService.getCourses()
      courses.value = data
      if (!selectedCourse.value) {
        selectedCourse.value = data.find((item) => item.id === course.value?.id) || data[0] || null
      }
      if (!course.value && selectedCourse.value) {
        course.value = selectedCourse.value
      }
    } catch (err) {
      error.value = err.message
      courses.value = course.value ? [course.value] : []
    }
  }

  async function fetchModules(courseId = selectedCourse.value?.id || null) {
    loading.value = true
    error.value = null
    try {
      const userStore = useUserStore()
      const data = await modulesService.getModules(courseId, userStore.currentUser?.id || null)
      modules.value = data
      if (activeModule.value) {
        const freshActiveModule = data.find((module) => module.id === activeModule.value.id)
        if (!freshActiveModule || freshActiveModule.status === 'locked') {
          clearActiveModule()
        } else {
          activeModule.value = freshActiveModule
        }
      }
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
      const userStore = useUserStore()
      const data = await modulesService.getModuleById(moduleId, userStore.currentUser?.id || null)
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

  function clearActiveModule() {
    activeModule.value = null
    activeSubtopicIndex.value = 0
  }

  function resetStoreState() {
    course.value = null
    courses.value = []
    selectedCourse.value = null
    modules.value = []
    activeModule.value = null
    activeSubtopicIndex.value = 0
    loading.value = false
    error.value = null
  }

  async function selectCourse(courseItem) {
    selectedCourse.value = courseItem
    course.value = courseItem
    clearActiveModule()
    await fetchModules(courseItem?.id || null)
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

  async function goToModuleSubtopic(moduleId, subtopicId) {
    if (!activeModule.value || activeModule.value.id !== moduleId) {
      await fetchModuleById(moduleId)
    }

    const targetIndex = activeModule.value?.subtopics?.findIndex((subtopic) => subtopic.id === subtopicId)
    if (targetIndex >= 0) {
      activeSubtopicIndex.value = targetIndex
    }
  }

  return {
    course,
    courses,
    selectedCourse,
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
    fetchCourse,
    fetchCourses,
    fetchModules,
    fetchModuleById,
    setActiveModule,
    clearActiveModule,
    resetStoreState,
    selectCourse,
    nextSubtopic,
    previousSubtopic,
    goToSubtopic,
    goToModuleSubtopic,
  }
})
