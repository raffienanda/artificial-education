<template>
  <div class="h-full min-h-0 flex flex-col relative overflow-hidden">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4 flex-shrink-0">
      <h2 class="text-base font-bold text-gray-900 dark:text-white flex items-center gap-2">
        Latihan Drill Soal
        <span 
          v-if="combo > 1"
          class="animate-bounce bg-gradient-to-r from-warning-500 to-danger-500 text-white text-xs font-black px-2 py-0.5 rounded-lg shadow-sm"
        >
          {{ combo }}x COMBO! 🔥
        </span>
      </h2>
    </div>

    <!-- Main Content Area -->
    <div class="min-h-0 flex-1 pr-1 -mr-1 flex flex-col overflow-hidden">
      <!-- Quiz Complete -->
      <div v-if="quizFinished" class="flex-1 flex flex-col items-center justify-center text-center animate-fade-in-up py-6">
        <div class="text-5xl mb-3">🏆</div>
        <h3 class="text-lg font-bold text-gray-800 dark:text-gray-100 mb-2">Drill Selesai!</h3>
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-5">
          Skor kamu: <span class="font-bold text-gray-800 dark:text-gray-200">{{ score }}/{{ totalQuestions }}</span> ({{ scorePercentage }}%)
        </p>
        <button class="bg-primary-500 text-white px-4 py-2 rounded" @click="resetQuiz">
          Latihan Lagi
        </button>
      </div>

      <!-- Active Question -->
      <div v-else-if="currentQuestion" class="min-h-0 flex-1 flex flex-col">
        <!-- Progress bar -->
        <div class="flex-shrink-0 flex items-center gap-3 mb-4">
          <span class="text-sm font-medium text-gray-600 dark:text-gray-400 whitespace-nowrap">
            Soal {{ currentQuestionIndex + 1 }} dari {{ totalQuestions }}
          </span>
          <div class="flex-1 h-2 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
            <div class="h-full bg-primary-500 transition-all duration-300" :style="{ width: progress + '%' }" />
          </div>
        </div>

        <div class="min-h-0 flex-1 overflow-y-auto overscroll-contain pr-2 space-y-4 pb-3">
        <!-- Question text -->
        <div class="bg-gray-50 dark:bg-gray-800 p-3 rounded-xl border border-gray-100 dark:border-gray-700">
          <h3 class="text-sm font-semibold text-gray-800 dark:text-gray-100 whitespace-pre-wrap leading-relaxed">
            {{ currentQuestion.question }}
          </h3>
        </div>

        <!-- Answer Grid -->
        <div class="grid grid-cols-1 gap-3">
          <button
            v-for="option in currentQuestion.options"
            :key="option.id"
            :disabled="isSubmitted"
            @click="submitAnswer(currentQuestion.id, option.id)"
            class="min-h-[64px] flex items-start gap-3 p-3 rounded-xl border text-left transition-all duration-200"
            :class="getOptionClasses(option.id)"
          >
            <div 
              class="w-8 h-8 rounded-lg flex flex-shrink-0 items-center justify-center font-bold text-sm"
              :class="getLabelClasses(option.id)"
            >
              {{ option.label }}
            </div>
            <span class="min-w-0 flex-1 whitespace-normal break-words text-sm font-medium leading-relaxed">
              {{ option.text }}
            </span>
            
            <!-- Feedback Icon -->
            <div v-if="isSubmitted && submissionResult?.correctAnswer === option.id" class="flex-shrink-0 text-success-500">
              ✔️
            </div>
            <div v-else-if="isSubmitted && selectedAnswer === option.id && !submissionResult?.correct" class="flex-shrink-0 text-danger-500">
              ❌
            </div>
          </button>
        </div>

        <!-- Explanation Panel -->
          <div v-if="isSubmitted" class="p-4 rounded-xl border" :class="submissionResult.correct ? 'bg-success-50 border-success-200' : 'bg-danger-50 border-danger-200'">
            <h4 class="font-bold mb-1" :class="submissionResult.correct ? 'text-success-700' : 'text-danger-700'">
              {{ submissionResult.correct ? 'Jawaban Benar!' : 'Jawaban Salah!' }}
            </h4>
            <p class="text-sm text-gray-700">{{ submissionResult.explanation }}</p>
          </div>

          <div v-if="isSubmitted" class="rounded-xl border border-sky-100 bg-sky-50/80 p-3 dark:border-sky-900/40 dark:bg-sky-950/20">
            <div class="flex items-center justify-between gap-3 mb-2">
              <h4 class="text-xs font-bold uppercase tracking-wide text-sky-700 dark:text-sky-300">
                Q-learning Update
              </h4>
              <span
                class="rounded-lg px-2 py-0.5 text-xs font-bold"
                :class="submissionResult.rewardXp >= 0 ? 'bg-success-100 text-success-700' : 'bg-danger-100 text-danger-700'"
              >
                Reward {{ signedNumber(submissionResult.rewardXp) }}
              </span>
            </div>

            <div class="grid grid-cols-2 gap-2 text-xs">
              <div class="rounded-lg bg-white p-2 dark:bg-gray-800">
                <p class="text-gray-400">Action</p>
                <p class="font-semibold text-gray-700 dark:text-gray-200">{{ formatAction(submissionResult.action) }}</p>
              </div>
              <div class="rounded-lg bg-white p-2 dark:bg-gray-800">
                <p class="text-gray-400">Q-value</p>
                <p class="font-semibold text-gray-700 dark:text-gray-200">{{ formatNumber(submissionResult.qValue) }}</p>
              </div>
              <div class="rounded-lg bg-white p-2 dark:bg-gray-800">
                <p class="text-gray-400">State awal</p>
                <p class="font-semibold text-gray-700 dark:text-gray-200">{{ submissionResult.learningState || '-' }}</p>
              </div>
              <div class="rounded-lg bg-white p-2 dark:bg-gray-800">
                <p class="text-gray-400">State baru</p>
                <p class="font-semibold text-gray-700 dark:text-gray-200">{{ submissionResult.nextLearningState || '-' }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="flex flex-1 flex-col items-center justify-center rounded-xl border border-dashed border-gray-200 bg-gray-50 p-5 text-center dark:border-gray-700 dark:bg-gray-800/60">
        <div class="mb-3 flex h-12 w-12 items-center justify-center rounded-2xl bg-primary-50 text-primary-600 dark:bg-primary-900/20 dark:text-primary-300">
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3 class="text-sm font-bold text-gray-900 dark:text-white">Pilih materi dulu</h3>
        <p class="mt-1 text-xs leading-relaxed text-gray-500 dark:text-gray-400">
          Drill soal akan muncul setelah kamu memilih modul dan materi dari sidebar.
        </p>
      </div>
    </div>

    <!-- Action Buttons -->
    <div v-if="currentQuestion && isSubmitted && !quizFinished" class="flex-shrink-0 pt-4 mt-3 border-t border-gray-100 dark:border-gray-700 flex justify-end">
      <button
        class="bg-primary-500 hover:bg-primary-600 text-white font-medium px-4 py-2 rounded-xl transition-colors"
        @click="nextQuestion"
      >
        Soal Berikutnya ➔
      </button>
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useQuizStore } from '@/stores/quiz'
import { useModulesStore } from '@/stores/modules'
import { useRecommendationStore } from '@/stores/recommendation'

// Mengonsumsi store menggunakan Composition API
const quizStore = useQuizStore()
const modulesStore = useModulesStore()
const recommendationStore = useRecommendationStore()

// Gunakan storeToRefs agar reaktivitas terjaga saat destructuring
const { 
  currentQuestion, 
  currentQuestionIndex, 
  totalQuestions, 
  progress, 
  selectedAnswer, 
  isSubmitted, 
  submissionResult, 
  quizFinished, 
  score, 
  scorePercentage, 
  combo,
  loading
} = storeToRefs(quizStore)

// Mapping actions (tanpa ref)
const { submitAnswer, nextQuestion, resetQuiz } = quizStore

// Logika kelas CSS untuk visual feedback
function getOptionClasses(optionId) {
  if (!isSubmitted.value) {
    return 'border-gray-200 bg-white hover:border-primary-300 hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800'
  }
  
  const isCorrectOption = submissionResult.value?.correctAnswer === optionId
  const isSelectedOption = selectedAnswer.value === optionId

  if (isCorrectOption) {
    return 'border-success-500 bg-success-50 text-success-700 dark:bg-success-900/10'
  }
  if (isSelectedOption && !isCorrectOption) {
    return 'border-danger-500 bg-danger-50 text-danger-700 dark:bg-danger-900/10'
  }
  
  return 'border-gray-200 bg-white opacity-50 dark:border-gray-700 dark:bg-gray-800'
}

function getLabelClasses(optionId) {
  if (!isSubmitted.value) {
    return 'bg-gray-100 text-gray-500 dark:bg-gray-700 dark:text-gray-400'
  }

  const isCorrectOption = submissionResult.value?.correctAnswer === optionId
  const isSelectedOption = selectedAnswer.value === optionId

  if (isCorrectOption) return 'bg-success-500 text-white'
  if (isSelectedOption && !isCorrectOption) return 'bg-danger-500 text-white'
  
  return 'bg-gray-100 text-gray-400 dark:bg-gray-700'
}

function formatNumber(value) {
  const numericValue = Number(value)
  if (Number.isNaN(numericValue)) return '0.00'
  return numericValue.toFixed(2)
}

function signedNumber(value) {
  const numericValue = Number(value)
  if (Number.isNaN(numericValue)) return '+0'
  return numericValue > 0 ? `+${numericValue}` : `${numericValue}`
}

function formatAction(action) {
  const labels = {
    show_text: 'Baca ringkasan',
    show_video: 'Tonton video',
    easy_quiz: 'Quiz mudah',
    hard_quiz: 'Quiz tantangan',
    review_previous: 'Review sebelumnya',
  }

  return labels[action] || action || '-'
}

import { watch } from 'vue'

watch(() => [modulesStore.activeModule?.id, recommendationStore.microAction], ([moduleId, action]) => {
  const newMod = modulesStore.activeModule
  if (isSubmitted.value) return

  if (newMod && newMod.status !== 'locked') {
    quizStore.fetchQuestions(moduleId, action)
  } else {
    quizStore.resetQuiz()
  }
}, { immediate: true })
</script>
