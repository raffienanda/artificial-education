<template>
  <div class="h-full flex flex-col relative overflow-hidden">
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
    <div class="flex-1 overflow-y-auto pr-1 -mr-1 flex flex-col">
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
      <div v-else-if="currentQuestion" class="flex-1 flex flex-col">
        <!-- Progress bar -->
        <div class="flex items-center gap-3 mb-4">
          <span class="text-sm font-medium text-gray-600 dark:text-gray-400 whitespace-nowrap">
            Soal {{ currentQuestionIndex + 1 }} dari {{ totalQuestions }}
          </span>
          <div class="flex-1 h-2 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
            <div class="h-full bg-primary-500 transition-all duration-300" :style="{ width: progress + '%' }" />
          </div>
        </div>

        <!-- Question text -->
        <div class="mb-5 bg-gray-50 dark:bg-gray-800 p-4 rounded-xl border border-gray-100 dark:border-gray-700">
          <h3 class="text-base font-semibold text-gray-800 dark:text-gray-100 whitespace-pre-wrap">
            {{ currentQuestion.question }}
          </h3>
        </div>

        <!-- Answer Grid -->
        <div class="grid grid-cols-2 gap-3 flex-1 content-start">
          <button
            v-for="option in currentQuestion.options"
            :key="option.id"
            :disabled="isSubmitted"
            @click="submitAnswer(currentQuestion.id, option.id)"
            class="flex items-center gap-3 p-3 rounded-xl border text-left transition-all duration-200"
            :class="getOptionClasses(option.id)"
          >
            <div 
              class="w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm"
              :class="getLabelClasses(option.id)"
            >
              {{ option.label }}
            </div>
            <span class="flex-1 text-sm font-medium">
              {{ option.text }}
            </span>
            
            <!-- Feedback Icon -->
            <div v-if="isSubmitted && submissionResult?.correctAnswer === option.id" class="text-success-500">
              ✔️
            </div>
            <div v-else-if="isSubmitted && selectedAnswer === option.id && !submissionResult?.correct" class="text-danger-500">
              ❌
            </div>
          </button>
        </div>

        <!-- Explanation Panel -->
        <div v-if="isSubmitted" class="mt-4 p-4 rounded-xl border" :class="submissionResult.correct ? 'bg-success-50 border-success-200' : 'bg-danger-50 border-danger-200'">
          <h4 class="font-bold mb-1" :class="submissionResult.correct ? 'text-success-700' : 'text-danger-700'">
            {{ submissionResult.correct ? 'Jawaban Benar!' : 'Jawaban Salah!' }}
          </h4>
          <p class="text-sm text-gray-700">{{ submissionResult.explanation }}</p>
        </div>
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

// Mengonsumsi store menggunakan Composition API
const quizStore = useQuizStore()
const modulesStore = useModulesStore()

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

import { watch } from 'vue'

watch(() => modulesStore.activeModule, (newMod) => {
  if (newMod && newMod.status !== 'locked') {
    quizStore.fetchQuestions(newMod.id)
  } else {
    quizStore.resetQuiz()
  }
}, { immediate: true })
</script>
