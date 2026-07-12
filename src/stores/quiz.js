/**
 * Quiz Store — Practice drill questions, answer submission, and scoring
 * Connected to FastAPI backend via centralized API instance
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useProgressStore } from './progress'
import { useModulesStore } from './modules'
import { useRecommendationStore } from './recommendation'
import { useUserStore } from './user'
import api from '@/services/api'

export const useQuizStore = defineStore('quiz', () => {
  const gateStorageKeys = [
    'completed_pretests',
    'completed_posttests',
    'completed_subtopic_quizzes',
    'passed_modules',
  ]

  function currentUserPrefix() {
    const rawUser = localStorage.getItem('auth_user')
    if (!rawUser) return 'guest'
    try {
      const user = JSON.parse(rawUser)
      return user?.id ? `user_${user.id}` : 'guest'
    } catch {
      return 'guest'
    }
  }

  function scopedGateKey(key) {
    return `${currentUserPrefix()}:${key}`
  }

  function readGateCache(key) {
    return JSON.parse(localStorage.getItem(scopedGateKey(key)) || '{}')
  }

  function writeGateCache(key, value) {
    localStorage.setItem(scopedGateKey(key), JSON.stringify(value))
  }

  function clearLegacyGateCache() {
    gateStorageKeys.forEach((key) => localStorage.removeItem(key))
  }

  // State
  const questions = ref([]) 
  const currentQuestionIndex = ref(0)
  const selectedAnswer = ref(null)
  const isSubmitted = ref(false)
  const submissionResult = ref(null)
  const score = ref(0)
  const totalAnswered = ref(0)
  const quizFinished = ref(false)
  const combo = ref(0)
  const loading = ref(false)
  const error = ref(null)
  const activeQuizAction = ref('easy_quiz')
  const assessmentType = ref('quiz')
  const completedPretests = ref(readGateCache('completed_pretests'))
  const completedPosttests = ref(readGateCache('completed_posttests'))
  const completedSubtopicQuizzes = ref(readGateCache('completed_subtopic_quizzes'))
  const passedModules = ref(readGateCache('passed_modules'))

  // Computed
  const currentQuestion = computed(() =>
    questions.value[currentQuestionIndex.value] || null
  )

  const totalQuestions = computed(() => questions.value.length)

  const progress = computed(() => {
    if (totalQuestions.value === 0) return 0
    return Math.round(((currentQuestionIndex.value + 1) / totalQuestions.value) * 100)
  })

  const hasNextQuestion = computed(() =>
    currentQuestionIndex.value < totalQuestions.value - 1
  )

  const scorePercentage = computed(() => {
    if (totalAnswered.value === 0) return 0
    return Math.round((score.value / totalAnswered.value) * 100)
  })

  // Actions
  function difficultyFromAction(action) {
    if (action === 'easy_quiz') return 'mudah'
    if (action === 'hard_quiz') return 'sedang'
    return null
  }

  async function fetchQuestions(moduleId = null, action = activeQuizAction.value, type = 'quiz', subtopicId = null) {
    loading.value = true
    error.value = null
    questions.value = []
    resetQuiz()
    try {
      if (moduleId) {
        activeQuizAction.value = action || 'easy_quiz'
        assessmentType.value = type || 'quiz'
        const difficulty = difficultyFromAction(activeQuizAction.value)
        const params = { assessment_type: assessmentType.value }
        if (difficulty && ['drill', 'quiz'].includes(assessmentType.value)) {
          params.difficulty = difficulty
        }
        if (subtopicId && ['drill', 'quiz'].includes(assessmentType.value)) {
          params.subtopic_id = subtopicId
        }
        const data = await api.get(`/quiz/${moduleId}`, {
          params,
        })
        questions.value = data
      }
      resetQuiz()
    } catch (error) {
      console.error("Error fetching questions:", error)
      questions.value = []
      resetQuiz()
      const message = error?.response?.data?.detail || error?.message || 'Gagal memuat soal'
      quizStoreError(message)
      throw error
    } finally {
      loading.value = false
    }
  }

  function quizStoreError(message) {
    error.value = message
  }

  async function submitAnswer(questionId, optionId) {
    if (isSubmitted.value) return

    loading.value = true
    selectedAnswer.value = optionId
    const question = questions.value.find(q => q.id === questionId)
    
    if (!question) {
      loading.value = false
      return
    }

    try {
      const userStore = useUserStore()
      const recommendationStore = useRecommendationStore()
      const submittedAction = assessmentType.value === 'quiz'
        ? (recommendationStore.activeLearningAction || recommendationStore.microAction || 'quiz')
        : assessmentType.value
      const actionSequence = assessmentType.value === 'quiz'
        ? recommendationStore.learningActionTrace
        : [assessmentType.value]
      // Call backend via centralized API
      const result = await api.post('/quiz/submit', {
        question_id: questionId,
        selected_option_id: optionId,
        user_id: userStore.userId,
        action: submittedAction,
        action_sequence: actionSequence,
      })

      submissionResult.value = {
        correct: result.correct,
        correctAnswer: result.correct_answer,
        explanation: result.explanation,
        rewardXp: result.reward_xp,
        qValue: result.q_value,
        learningState: result.learning_state,
        nextLearningState: result.next_learning_state,
        action: submittedAction,
        newMastery: result.new_mastery,
      }
      userStore.applyQuizUserUpdate(result.user)

      isSubmitted.value = true
      totalAnswered.value++

      const progressStore = useProgressStore()
      progressStore.updateProgress(question.subtopic_id, result.new_mastery)

      if (result.correct) {
        score.value++
        combo.value++
      } else {
        combo.value = 0
      }

      const modulesStore = useModulesStore()
      if (assessmentType.value === 'quiz' && modulesStore.activeModule?.id && modulesStore.activeSubtopic?.id) {
        recommendationStore.fetchNext({
          userId: userStore.userId,
          currentModuleId: modulesStore.activeModule.id,
          currentSubtopicId: modulesStore.activeSubtopic.id,
        })
        recommendationStore.fetchLogs({ userId: userStore.userId })
      }
    } catch (error) {
      console.error("Error submitting answer:", error)
    } finally {
      loading.value = false
    }
  }

  function nextQuestion() {
    if (hasNextQuestion.value) {
      currentQuestionIndex.value++
      selectedAnswer.value = null
      isSubmitted.value = false
      submissionResult.value = null
    } else {
      quizFinished.value = true
    }
  }

  function resetQuiz() {
    currentQuestionIndex.value = 0
    selectedAnswer.value = null
    isSubmitted.value = false
    submissionResult.value = null
    score.value = 0
    totalAnswered.value = 0
    quizFinished.value = false
    combo.value = 0
  }

  function clearQuestions() {
    questions.value = []
    resetQuiz()
  }

  function markAssessmentDone(moduleId = null) {
    if (!moduleId) return
    if (assessmentType.value === 'pre_test') {
      completedPretests.value[moduleId] = true
      writeGateCache('completed_pretests', completedPretests.value)
    }
    if (assessmentType.value === 'post_test') {
      completedPosttests.value[moduleId] = true
      writeGateCache('completed_posttests', completedPosttests.value)
    }
  }

  function hasCompletedPretest(moduleId) {
    return Boolean(completedPretests.value[moduleId])
  }

  function hasCompletedPosttest(moduleId) {
    return Boolean(completedPosttests.value[moduleId])
  }

  function markSubtopicQuizDone(moduleId, subtopicId) {
    if (!moduleId || !subtopicId) return
    completedSubtopicQuizzes.value[`${moduleId}:${subtopicId}`] = true
    writeGateCache('completed_subtopic_quizzes', completedSubtopicQuizzes.value)
  }

  function hasCompletedSubtopicQuiz(moduleId, subtopicId) {
    return Boolean(completedSubtopicQuizzes.value[`${moduleId}:${subtopicId}`])
  }

  function markModulePassed(moduleId) {
    if (!moduleId) return
    passedModules.value[moduleId] = true
    writeGateCache('passed_modules', passedModules.value)
  }

  function hasPassedModule(moduleId) {
    return Boolean(passedModules.value[moduleId])
  }

  function resetStoreState() {
    questions.value = []
    resetQuiz()
    assessmentType.value = 'quiz'
    activeQuizAction.value = 'easy_quiz'
    error.value = null
    completedPretests.value = {}
    completedPosttests.value = {}
    completedSubtopicQuizzes.value = {}
    passedModules.value = {}
    clearLegacyGateCache()
    gateStorageKeys.forEach((key) => localStorage.removeItem(scopedGateKey(key)))
  }

  function hydrateGateCache() {
    clearLegacyGateCache()
    completedPretests.value = readGateCache('completed_pretests')
    completedPosttests.value = readGateCache('completed_posttests')
    completedSubtopicQuizzes.value = readGateCache('completed_subtopic_quizzes')
    passedModules.value = readGateCache('passed_modules')
  }

  async function fetchGateStatus() {
    try {
      const data = await api.get('/progress/gates')
      completedPretests.value = data.completed_pretests || {}
      completedPosttests.value = data.completed_posttests || {}
      completedSubtopicQuizzes.value = data.completed_subtopic_quizzes || {}
      passedModules.value = data.passed_modules || {}
      clearLegacyGateCache()
      writeGateCache('completed_pretests', completedPretests.value)
      writeGateCache('completed_posttests', completedPosttests.value)
      writeGateCache('completed_subtopic_quizzes', completedSubtopicQuizzes.value)
      writeGateCache('passed_modules', passedModules.value)
    } catch (error) {
      console.error('Error fetching gate status:', error)
    }
  }

  function isModuleUnlocked(module, modules = []) {
    if (!module) return false
    if ((module.order || 1) <= 1) return true
    const previousModule = modules.find((item) => item.order === module.order - 1)
    return Boolean(previousModule && hasPassedModule(previousModule.id))
  }

  function isSubtopicUnlocked(moduleId, subtopics = [], index = 0) {
    if (index <= 0) return true
    const previousSubtopics = subtopics.slice(0, index)
    return previousSubtopics.every((subtopic) =>
      hasCompletedSubtopicQuiz(moduleId, subtopic.id)
    )
  }

  return {
    questions,
    currentQuestionIndex,
    selectedAnswer,
    isSubmitted,
    submissionResult,
    score,
    totalAnswered,
    quizFinished,
    combo,
    activeQuizAction,
    assessmentType,
    error,
    completedPretests,
    completedPosttests,
    completedSubtopicQuizzes,
    passedModules,
    loading,
    currentQuestion,
    totalQuestions,
    progress,
    hasNextQuestion,
    scorePercentage,
    submitAnswer,
    nextQuestion,
    resetQuiz,
    clearQuestions,
    fetchQuestions,
    markAssessmentDone,
    hasCompletedPretest,
    hasCompletedPosttest,
    markSubtopicQuizDone,
    hasCompletedSubtopicQuiz,
    markModulePassed,
    hasPassedModule,
    isModuleUnlocked,
    isSubtopicUnlocked,
    resetStoreState,
    hydrateGateCache,
    fetchGateStatus,
  }
})
