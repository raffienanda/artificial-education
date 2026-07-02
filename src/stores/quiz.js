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
  const activeQuizAction = ref('easy_quiz')

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

  async function fetchQuestions(moduleId = null, action = activeQuizAction.value) {
    loading.value = true
    try {
      if (moduleId) {
        activeQuizAction.value = action || 'easy_quiz'
        const difficulty = difficultyFromAction(activeQuizAction.value)
        const data = await api.get(`/quiz/${moduleId}`, {
          params: difficulty ? { difficulty } : {},
        })
        questions.value = data
      }
      resetQuiz()
    } catch (error) {
      console.error("Error fetching questions:", error)
    } finally {
      loading.value = false
    }
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
      // Call backend via centralized API
      const result = await api.post('/quiz/submit', {
        question_id: questionId,
        selected_option_id: optionId,
        user_id: userStore.userId,
        action: recommendationStore.microAction,
      })

      submissionResult.value = {
        correct: result.correct,
        correctAnswer: result.correct_answer,
        explanation: result.explanation,
        rewardXp: result.reward_xp,
        qValue: result.q_value,
        learningState: result.learning_state,
        nextLearningState: result.next_learning_state,
        action: recommendationStore.microAction,
        newMastery: result.new_mastery,
      }
      userStore.applyQuizUserUpdate(result.user)

      isSubmitted.value = true
      totalAnswered.value++

      if (result.correct) {
        score.value++
        combo.value++
        
        // Update Progress State directly from Backend's returned mastery
        const progressStore = useProgressStore()
        progressStore.updateProgress(question.subtopic_id, result.new_mastery)
      } else {
        combo.value = 0
      }

      const modulesStore = useModulesStore()
      if (modulesStore.activeModule?.id && modulesStore.activeSubtopic?.id) {
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
    loading,
    currentQuestion,
    totalQuestions,
    progress,
    hasNextQuestion,
    scorePercentage,
    submitAnswer,
    nextQuestion,
    resetQuiz,
    fetchQuestions,
  }
})
