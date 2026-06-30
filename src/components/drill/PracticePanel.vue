<template>
  <div class="h-full flex flex-col relative overflow-hidden">
    <!-- Floating XP Animation Container -->
    <Transition name="float-up">
      <div 
        v-if="showFloatingXP" 
        class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 pointer-events-none"
      >
        <span class="text-3xl font-black text-warning-500 drop-shadow-md">+10 XP</span>
      </div>
    </Transition>

    <!-- Header -->
    <div class="flex items-center justify-between mb-4 flex-shrink-0">
      <h2 class="text-base font-bold text-gray-900 dark:text-white flex items-center gap-2">
        Latihan Drill Soal
        <!-- Combo Multiplier Display -->
        <span 
          v-if="combo > 1"
          class="animate-bounce bg-gradient-to-r from-warning-500 to-danger-500 text-white text-xs font-black px-2 py-0.5 rounded-lg shadow-sm"
        >
          {{ combo }}x COMBO! 🔥
        </span>
      </h2>
      <span class="flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary-50 dark:bg-primary-900/20 text-xs font-medium text-primary-600 dark:text-primary-400 border border-primary-200 dark:border-primary-700">
        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25H12" />
        </svg>
        Flashcard
      </span>
    </div>

    <!-- Main Content Area -->
    <div class="flex-1 overflow-y-auto pr-1 -mr-1 scrollbar-hide flex flex-col">
      <div v-if="loading && !currentQuestion" class="flex-1 flex items-center justify-center">
        <SkeletonLoader type="card" width="100%" />
      </div>

      <!-- Quiz Complete -->
      <div v-else-if="isQuizComplete" class="flex-1 flex flex-col items-center justify-center text-center animate-fade-in-up py-6">
        <div class="text-5xl mb-3">🏆</div>
        <h3 class="text-lg font-bold text-gray-800 dark:text-gray-100 mb-2">Drill Selesai!</h3>
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-5">
          Skor kamu: <span class="font-bold text-gray-800 dark:text-gray-200">{{ score }}/{{ totalQuestions }}</span> ({{ scorePercentage }}%)
        </p>
        <BaseButton variant="primary" @click="quizStore.resetQuiz()">
          Latihan Lagi
        </BaseButton>
      </div>

      <!-- Active Question -->
      <div v-else-if="currentQuestion" class="flex-1 flex flex-col">
        <!-- Question number + progress bar + bookmark -->
        <div class="flex items-center gap-3 mb-4">
          <span class="text-sm font-medium text-gray-600 dark:text-gray-400 whitespace-nowrap">
            Soal {{ currentQuestionIndex + 1 }} dari {{ totalQuestions }}
          </span>
          <div class="flex-1 progress-bar h-2 bg-gray-100 dark:bg-gray-700">
            <div class="progress-bar-fill bg-primary-500" :style="{ width: progress + '%' }" />
          </div>
          <button class="text-gray-400 hover:text-warning-500 dark:hover:text-warning-400 transition-colors">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17.593 3.322c1.1.128 1.907 1.077 1.907 2.185V21L12 17.25 4.5 21V5.507c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0111.186 0z" />
            </svg>
          </button>
        </div>

        <!-- Question text -->
        <div class="mb-5">
          <h3 class="text-base font-semibold text-gray-800 dark:text-gray-100 leading-relaxed">
            {{ currentQuestion.question }}
          </h3>
        </div>

        <!-- 2×2 Answer Grid -->
        <div class="grid grid-cols-2 gap-3 flex-1 content-start">
          <OptionButton
            v-for="option in currentQuestion.options"
            :key="option.id"
            :option="option"
            :selected="selectedAnswer === option.id"
            :submitted="isSubmitted"
            :correct="submissionResult?.correctAnswer === option.id"
            @click="quizStore.selectAnswer(option.id)"
          />
        </div>

        <!-- Explanation Panel -->
        <ExplanationCard
          v-if="isSubmitted && submissionResult"
          :is-correct="submissionResult.correct"
          :explanation="submissionResult.explanation"
          class="mt-4 animate-slide-in-up"
        />
      </div>

      <!-- Placeholder -->
      <div v-else class="flex-1 flex flex-col items-center justify-center text-center text-gray-400">
        <div class="text-4xl mb-3 opacity-50">📝</div>
        <p class="text-sm">Pilih modul untuk mulai latihan</p>
      </div>
    </div>

    <!-- Action Buttons -->
    <div v-if="currentQuestion && !isQuizComplete" class="flex-shrink-0 pt-4 mt-3 border-t border-gray-100 dark:border-gray-700 flex items-center justify-between">
      <button
        v-if="!isSubmitted"
        class="flex items-center gap-1.5 px-4 py-2 rounded-xl border border-gray-200 dark:border-gray-600 text-sm font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
        :disabled="!selectedAnswer"
        @click="handleAnswerSubmit"
      >
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 01.865-.501 48.172 48.172 0 003.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z" />
        </svg>
        Pembahasan
      </button>

      <BaseButton
        v-if="isSubmitted"
        variant="primary"
        @click="handleNextOrFinish"
      >
        Soal Berikutnya
        <template #icon>
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
          </svg>
        </template>
      </BaseButton>

      <BaseButton
        v-if="!isSubmitted"
        variant="primary"
        :disabled="!selectedAnswer || loading"
        :loading="loading"
        @click="handleAnswerSubmit"
      >
        Jawab
      </BaseButton>
    </div>
  </div>
</template>

<script setup>
/**
 * PracticePanel — Gamified with XP floating animation and combo system
 */
import { ref, computed, watch } from 'vue'
import { useQuizStore } from '@/stores/quiz'
import { useModulesStore } from '@/stores/modules'
import { useUserStore } from '@/stores/user'
import BaseButton from '@/components/common/BaseButton.vue'
import SkeletonLoader from '@/components/common/SkeletonLoader.vue'
import OptionButton from './OptionButton.vue'
import ExplanationCard from './ExplanationCard.vue'

const quizStore = useQuizStore()
const modulesStore = useModulesStore()
const userStore = useUserStore()

const showFloatingXP = ref(false)

const currentQuestion = computed(() => quizStore.currentQuestion)
const currentQuestionIndex = computed(() => quizStore.currentQuestionIndex)
const totalQuestions = computed(() => quizStore.totalQuestions)
const progress = computed(() => quizStore.progress)
const selectedAnswer = computed(() => quizStore.selectedAnswer)
const isSubmitted = computed(() => quizStore.isSubmitted)
const submissionResult = computed(() => quizStore.submissionResult)
const hasNextQuestion = computed(() => quizStore.hasNextQuestion)
const isQuizComplete = computed(() => quizStore.isQuizComplete)
const score = computed(() => quizStore.score)
const scorePercentage = computed(() => quizStore.scorePercentage)
const loading = computed(() => quizStore.loading)
const combo = computed(() => quizStore.combo)

async function handleAnswerSubmit() {
  await quizStore.submitAnswer()
  
  if (quizStore.submissionResult?.correct) {
    // Show XP animation
    showFloatingXP.value = true
    
    // Add XP to user profile
    const baseXP = 10
    const comboBonus = quizStore.combo > 1 ? (quizStore.combo * 2) : 0
    userStore.addXP(baseXP + comboBonus)
    
    // Hide animation after 1.5s
    setTimeout(() => {
      showFloatingXP.value = false
    }, 1500)
  }
}

function handleNextOrFinish() {
  if (hasNextQuestion.value) {
    quizStore.nextQuestion()
  } else {
    // Mark quiz as complete and award completion XP
    quizStore.nextQuestion()
    userStore.addXP(50) // Module completion bonus
  }
}

watch(() => modulesStore.activeModule, (newMod) => {
  if (newMod && newMod.status !== 'locked') {
    quizStore.fetchQuestions(newMod.id)
  } else {
    quizStore.resetQuiz()
  }
}, { immediate: true })
</script>

<style scoped>
.float-up-enter-active {
  transition: all 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.float-up-leave-active {
  transition: all 0.5s ease-in;
}
.float-up-enter-from {
  opacity: 0;
  transform: translate(-50%, -10%);
}
.float-up-enter-to {
  opacity: 1;
  transform: translate(-50%, -100%);
}
.float-up-leave-to {
  opacity: 0;
  transform: translate(-50%, -150%);
}
</style>
