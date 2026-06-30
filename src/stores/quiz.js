/**
 * Quiz Store — Practice drill state, question navigation, and scoring
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { quizService } from '@/services/quiz'

export const useQuizStore = defineStore('quiz', () => {
  // State
  const questions = ref([])
  const currentQuestionIndex = ref(0)
  const selectedAnswer = ref(null)
  const isSubmitted = ref(false)
  const submissionResult = ref(null)
  const score = ref(0)
  const totalAnswered = ref(0)
  const loading = ref(false)
  const quizFinished = ref(false)
  const combo = ref(0)

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

  const isQuizComplete = computed(() => quizFinished.value)

  // Actions
  async function fetchQuestions(moduleId = null) {
    loading.value = true
    try {
      const data = await quizService.getQuestions(moduleId)
      questions.value = data
      resetQuiz()
    } finally {
      loading.value = false
    }
  }

  async function submitAnswer() {
    if (!currentQuestion.value || selectedAnswer.value === null || isSubmitted.value) return

    loading.value = true
    try {
      const result = await quizService.submitAnswer(
        currentQuestion.value.id,
        selectedAnswer.value
      )
      submissionResult.value = result
      isSubmitted.value = true
      totalAnswered.value++
      
      if (result.correct) {
        score.value++
        combo.value++
      } else {
        combo.value = 0
      }
    } finally {
      loading.value = false
    }
  }

  function selectAnswer(optionId) {
    if (!isSubmitted.value) {
      selectedAnswer.value = optionId
    }
  }

  function nextQuestion() {
    if (hasNextQuestion.value) {
      currentQuestionIndex.value++
      selectedAnswer.value = null
      isSubmitted.value = false
      submissionResult.value = null
    } else {
      // Mark quiz as complete when there are no more questions
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
    loading,
    combo,
    currentQuestion,
    totalQuestions,
    progress,
    hasNextQuestion,
    scorePercentage,
    isQuizComplete,
    fetchQuestions,
    submitAnswer,
    selectAnswer,
    nextQuestion,
    resetQuiz,
  }
})
