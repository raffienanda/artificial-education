<template>
  <div class="h-full overflow-y-auto bg-surface-50 p-4 dark:bg-gray-900 sm:p-6">
    <div class="mx-auto flex min-h-full w-full max-w-4xl flex-col">
      <div class="mb-5 flex flex-wrap items-center justify-between gap-3">
        <div>
          <p class="text-sm font-bold uppercase text-primary-600 dark:text-primary-300">
            {{ assessmentLabel }}
          </p>
          <h1 class="text-2xl font-black text-gray-900 dark:text-white">
            {{ moduleTitle }}
          </h1>
        </div>
        <button
          class="rounded-xl border border-gray-200 px-4 py-2 text-sm font-bold text-gray-600 transition hover:bg-white dark:border-gray-700 dark:text-gray-300 dark:hover:bg-gray-800"
          type="button"
          @click="goBack"
        >
          Kembali
        </button>
      </div>

      <div v-if="loading" class="flex flex-1 items-center justify-center rounded-2xl bg-white p-8 text-sm font-semibold text-gray-500 shadow-card dark:bg-gray-800">
        Memuat soal...
      </div>

      <div v-else-if="pageError" class="flex flex-1 items-center justify-center rounded-2xl bg-white p-8 text-center shadow-card dark:bg-gray-800">
        <div class="max-w-md">
          <div class="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-warning-50 text-warning-600">
            <svg class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h2 class="text-lg font-black text-gray-900 dark:text-white">Asesmen belum bisa dibuka</h2>
          <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
            {{ pageError }}
          </p>
          <button
            class="mt-6 rounded-xl bg-primary-600 px-5 py-3 text-sm font-black text-white transition hover:bg-primary-700"
            type="button"
            @click="goBack"
          >
            Kembali ke Dashboard
          </button>
        </div>
      </div>

      <div v-else-if="!currentQuestion" class="flex flex-1 items-center justify-center rounded-2xl bg-white p-8 text-center shadow-card dark:bg-gray-800">
        <div>
          <h2 class="text-lg font-black text-gray-900 dark:text-white">Soal belum tersedia</h2>
          <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
            Silakan tambahkan soal untuk jenis asesmen ini dari halaman admin.
          </p>
        </div>
      </div>

      <div v-else-if="quizFinished && assessmentType === 'post_test'" class="flex flex-1 items-center justify-center rounded-2xl bg-white p-6 shadow-card dark:bg-gray-800 sm:p-8">
        <div class="w-full max-w-2xl">
          <div class="text-center">
            <p class="text-sm font-bold uppercase text-primary-600 dark:text-primary-300">Rapor Modul</p>
            <h2 class="mt-1 text-2xl font-black text-gray-900 dark:text-white">{{ moduleTitle }}</h2>
            <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
              Rapor ini dipakai sebagai gerbang untuk menentukan apakah modul berikutnya bisa dilanjutkan.
            </p>
          </div>

          <div class="mt-6 grid gap-3 sm:grid-cols-3">
            <div class="rounded-2xl border border-gray-100 bg-gray-50 p-4 text-center dark:border-gray-700 dark:bg-gray-900/50">
              <p class="text-xs font-bold uppercase text-gray-400">Skor Post Test</p>
              <p class="mt-2 text-3xl font-black text-gray-900 dark:text-white">{{ scorePercentage }}%</p>
              <p class="mt-1 text-xs text-gray-500">{{ score }}/{{ totalQuestions }} benar</p>
            </div>
            <div class="rounded-2xl border border-gray-100 bg-gray-50 p-4 text-center dark:border-gray-700 dark:bg-gray-900/50">
              <p class="text-xs font-bold uppercase text-gray-400">Penguasaan Modul</p>
              <p class="mt-2 text-3xl font-black text-gray-900 dark:text-white">{{ moduleMastery }}%</p>
              <p class="mt-1 text-xs text-gray-500">rata-rata subtopik</p>
            </div>
            <div class="rounded-2xl border p-4 text-center" :class="canContinue ? 'border-success-200 bg-success-50' : 'border-warning-200 bg-warning-50'">
              <p class="text-xs font-bold uppercase" :class="canContinue ? 'text-success-600' : 'text-warning-600'">Status</p>
              <p class="mt-2 text-xl font-black" :class="canContinue ? 'text-success-700' : 'text-warning-700'">
                {{ canContinue ? 'Bisa lanjut' : 'Review dulu' }}
              </p>
              <p class="mt-1 text-xs text-gray-600">minimal {{ passThreshold }}%</p>
            </div>
          </div>

          <div class="mt-5 rounded-2xl border p-4" :class="canContinue ? 'border-success-100 bg-success-50/70' : 'border-warning-100 bg-warning-50/80'">
            <p class="text-sm font-bold" :class="canContinue ? 'text-success-700' : 'text-warning-700'">
              {{ reportMessage }}
            </p>
            <div v-if="weakModuleSubtopics.length" class="mt-3">
              <p class="text-xs font-bold uppercase text-gray-500">Materi yang perlu diperkuat</p>
              <div class="mt-2 flex flex-wrap gap-2">
                <span
                  v-for="item in weakModuleSubtopics"
                  :key="item.id"
                  class="rounded-lg bg-white px-3 py-1 text-xs font-bold text-gray-600 shadow-sm dark:bg-gray-800 dark:text-gray-200"
                >
                  {{ item.name }} · {{ item.mastery }}%
                </span>
              </div>
            </div>
          </div>

          <div
            v-if="moduleDiagnosis?.available"
            class="mt-5 rounded-2xl border border-sky-100 bg-sky-50/80 p-4 dark:border-sky-900/40 dark:bg-sky-950/20"
          >
            <div class="flex flex-wrap items-start justify-between gap-3">
              <div>
                <p class="text-xs font-bold uppercase text-sky-600 dark:text-sky-300">Learning Diagnosis Report</p>
                <h3 class="mt-1 text-lg font-black capitalize text-gray-900 dark:text-white">
                  {{ moduleDiagnosis.category }}
                </h3>
              </div>
              <div class="grid grid-cols-2 gap-2 text-right text-xs">
                <div class="rounded-xl bg-white px-3 py-2 shadow-sm dark:bg-gray-800">
                  <p class="font-bold text-gray-400">Effort</p>
                  <p class="font-black capitalize text-gray-800 dark:text-gray-100">{{ moduleDiagnosis.effort_level }}</p>
                </div>
                <div class="rounded-xl bg-white px-3 py-2 shadow-sm dark:bg-gray-800">
                  <p class="font-bold text-gray-400">Hasil</p>
                  <p class="font-black capitalize text-gray-800 dark:text-gray-100">{{ moduleDiagnosis.outcome_level }}</p>
                </div>
              </div>
            </div>

            <p class="mt-3 text-sm font-semibold leading-relaxed text-gray-700 dark:text-gray-200">
              {{ moduleDiagnosis.summary }}
            </p>
            <p
              v-if="moduleDiagnosis.personal_pattern"
              class="mt-2 rounded-xl bg-white px-3 py-2 text-sm font-semibold leading-relaxed text-sky-800 shadow-sm dark:bg-gray-800 dark:text-sky-200"
            >
              {{ moduleDiagnosis.personal_pattern }}
            </p>

            <div class="mt-4 grid gap-2 sm:grid-cols-3">
              <div class="rounded-xl bg-white px-3 py-2 text-xs shadow-sm dark:bg-gray-800">
                <p class="font-bold uppercase text-gray-400">Post Test</p>
                <p class="mt-1 text-lg font-black text-gray-900 dark:text-white">{{ formatPercent(moduleDiagnosis.post_test_score) }}</p>
              </div>
              <div class="rounded-xl bg-white px-3 py-2 text-xs shadow-sm dark:bg-gray-800">
                <p class="font-bold uppercase text-gray-400">Quiz Rata-rata</p>
                <p class="mt-1 text-lg font-black text-gray-900 dark:text-white">{{ formatPercent(moduleDiagnosis.quiz_average) }}</p>
              </div>
              <div class="rounded-xl bg-white px-3 py-2 text-xs shadow-sm dark:bg-gray-800">
                <p class="font-bold uppercase text-gray-400">Profil Kognitif</p>
                <p class="mt-1 text-lg font-black capitalize text-gray-900 dark:text-white">{{ moduleDiagnosis.cognitive_stage }}</p>
              </div>
            </div>

            <div v-if="moduleDiagnosis.weak_subtopics?.length" class="mt-4">
              <p class="text-xs font-bold uppercase text-gray-500">Materi prioritas</p>
              <div class="mt-2 flex flex-wrap gap-2">
                <span
                  v-for="item in moduleDiagnosis.weak_subtopics"
                  :key="item.id"
                  class="rounded-lg bg-white px-3 py-1 text-xs font-bold text-gray-600 shadow-sm dark:bg-gray-800 dark:text-gray-200"
                >
                  {{ item.title }} · {{ formatPercent(item.mastery) }}
                </span>
              </div>
            </div>

            <div v-if="qActionScoreItems.length" class="mt-4">
              <p class="text-xs font-bold uppercase text-gray-500">Q-value strategi belajar</p>
              <div class="mt-2 grid gap-2 sm:grid-cols-2">
                <div
                  v-for="item in qActionScoreItems"
                  :key="item.action"
                  class="flex items-center justify-between gap-2 rounded-xl bg-white px-3 py-2 text-xs shadow-sm dark:bg-gray-800"
                >
                  <span class="font-bold text-gray-600 dark:text-gray-200">{{ labelForAction(item.action) }}</span>
                  <span class="font-black tabular-nums text-sky-700 dark:text-sky-300">{{ formatNumber(item.value) }}</span>
                </div>
              </div>
            </div>

            <div class="mt-4">
              <p class="text-xs font-bold uppercase text-gray-500">Saran personal</p>
              <ul class="mt-2 space-y-2">
                <li
                  v-for="item in personalDiagnosisItems"
                  :key="item"
                  class="rounded-xl bg-white px-3 py-2 text-sm font-semibold leading-relaxed text-gray-700 shadow-sm dark:bg-gray-800 dark:text-gray-200"
                >
                  {{ item }}
                </li>
              </ul>
            </div>
          </div>

          <div class="mt-6 flex flex-wrap justify-center gap-3">
            <button
              class="rounded-xl border border-gray-200 px-5 py-3 text-sm font-black text-gray-600 transition hover:bg-gray-50 dark:border-gray-700 dark:text-gray-300 dark:hover:bg-gray-700"
              type="button"
              @click="reviewModule"
            >
              Review Modul Ini
            </button>
            <button
              class="rounded-xl bg-primary-600 px-5 py-3 text-sm font-black text-white transition hover:bg-primary-700 disabled:cursor-not-allowed disabled:opacity-50"
              type="button"
              :disabled="!canContinue"
              @click="finishAssessment"
            >
              {{ nextModule ? 'Lanjut Modul Berikutnya' : 'Selesai' }}
            </button>
          </div>
        </div>
      </div>

      <div v-else-if="quizFinished" class="flex flex-1 items-center justify-center rounded-2xl bg-white p-8 text-center shadow-card dark:bg-gray-800">
        <div>
          <div class="mb-4 text-5xl">🏆</div>
          <h2 class="text-2xl font-black text-gray-900 dark:text-white">{{ finishedTitle }}</h2>
          <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
            Skor kamu {{ score }}/{{ totalQuestions }} ({{ scorePercentage }}%)
          </p>
          <button
            class="mt-6 rounded-xl bg-primary-600 px-5 py-3 text-sm font-black text-white transition hover:bg-primary-700"
            type="button"
            @click="finishAssessment"
          >
            {{ finishButtonLabel }}
          </button>
        </div>
      </div>

      <div v-else class="flex flex-1 flex-col rounded-2xl bg-white p-5 shadow-card dark:bg-gray-800 sm:p-7">
        <div class="mb-6 flex items-center gap-3">
          <span class="text-sm font-bold text-gray-600 dark:text-gray-300">
            Soal {{ currentQuestionIndex + 1 }} dari {{ totalQuestions }}
          </span>
          <div class="h-2 flex-1 overflow-hidden rounded-full bg-gray-100 dark:bg-gray-700">
            <div class="h-full bg-primary-600 transition-all" :style="{ width: `${progress}%` }" />
          </div>
        </div>

        <div class="rounded-2xl border border-gray-100 bg-gray-50 p-5 dark:border-gray-700 dark:bg-gray-900/50">
          <p class="whitespace-pre-wrap text-base font-bold leading-relaxed text-gray-900 dark:text-gray-100">
            {{ currentQuestion.question }}
          </p>
        </div>

        <div class="mt-5 grid gap-3">
          <button
            v-for="option in currentQuestion.options"
            :key="option.id"
            :disabled="isSubmitted"
            class="flex min-h-[64px] items-start gap-3 rounded-2xl border p-4 text-left transition"
            :class="optionClass(option.id)"
            type="button"
            @click="submitAnswer(currentQuestion.id, option.id)"
          >
            <span
              class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-xl text-sm font-black"
              :class="labelClass(option.id)"
            >
              {{ option.label }}
            </span>
            <span class="text-sm font-semibold leading-relaxed">{{ option.text }}</span>
          </button>
        </div>

        <div
          v-if="isSubmitted"
          class="mt-5 rounded-2xl border p-4"
          :class="submissionResult.correct ? 'border-success-200 bg-success-50' : 'border-danger-200 bg-danger-50'"
        >
          <h3 class="text-sm font-black" :class="submissionResult.correct ? 'text-success-700' : 'text-danger-700'">
            {{ submissionResult.correct ? 'Jawaban benar' : 'Jawaban salah' }}
          </h3>
          <p class="mt-1 text-sm leading-relaxed text-gray-700">{{ submissionResult.explanation }}</p>
        </div>

        <div
          v-if="isSubmitted"
          class="mt-3 rounded-2xl border border-sky-100 bg-sky-50/80 p-4 dark:border-sky-900/40 dark:bg-sky-950/20"
        >
          <div class="flex flex-wrap items-center justify-between gap-2">
            <div>
              <p class="text-xs font-bold uppercase text-sky-600 dark:text-sky-300">Q-Value Update</p>
              <p class="mt-1 text-sm font-semibold text-gray-700 dark:text-gray-200">
                Nilai adaptasi setelah jawaban ini dipakai untuk rekomendasi berikutnya.
              </p>
            </div>
            <div class="rounded-xl bg-white px-3 py-2 text-right shadow-sm dark:bg-gray-800">
              <p class="text-[11px] font-bold uppercase text-gray-400">Action utama</p>
              <p class="text-sm font-black text-gray-900 dark:text-white">
                {{ submissionResult.action }} = {{ formatNumber(submissionResult.qValue) }}
              </p>
            </div>
          </div>

          <div class="mt-3 grid gap-2 sm:grid-cols-2">
            <div class="rounded-xl bg-white px-3 py-2 text-xs shadow-sm dark:bg-gray-800">
              <p class="font-bold uppercase text-gray-400">State Awal</p>
              <p class="mt-1 font-black text-gray-900 dark:text-white">{{ submissionResult.learningState || '-' }}</p>
            </div>
            <div class="rounded-xl bg-white px-3 py-2 text-xs shadow-sm dark:bg-gray-800">
              <p class="font-bold uppercase text-gray-400">State Berikutnya</p>
              <p class="mt-1 font-black text-gray-900 dark:text-white">{{ submissionResult.nextLearningState || '-' }}</p>
            </div>
          </div>

          <div v-if="updatedQValueItems.length" class="mt-3">
            <p class="text-xs font-bold uppercase text-gray-500">Action yang ikut ter-update</p>
            <div class="mt-2 grid gap-2 sm:grid-cols-2">
              <div
                v-for="item in updatedQValueItems"
                :key="item.action"
                class="flex items-center justify-between gap-2 rounded-xl bg-white px-3 py-2 text-xs shadow-sm dark:bg-gray-800"
              >
                <span class="font-bold text-gray-600 dark:text-gray-200">{{ labelForAction(item.action) }}</span>
                <span class="font-black tabular-nums text-sky-700 dark:text-sky-300">{{ formatNumber(item.value) }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-auto flex justify-end pt-6">
          <button
            v-if="isSubmitted"
            class="rounded-xl bg-primary-600 px-5 py-3 text-sm font-black text-white transition hover:bg-primary-700"
            type="button"
            @click="nextQuestion"
          >
            {{ hasNextQuestion ? 'Soal Berikutnya' : 'Lihat Hasil' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useRoute, useRouter } from 'vue-router'
import { useModulesStore } from '@/stores/modules'
import { useQuizStore } from '@/stores/quiz'
import { useProgressStore } from '@/stores/progress'

const route = useRoute()
const router = useRouter()
const modulesStore = useModulesStore()
const quizStore = useQuizStore()
const progressStore = useProgressStore()

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
  hasNextQuestion,
  loading,
} = storeToRefs(quizStore)

const moduleId = computed(() => route.params.moduleId)
const assessmentType = computed(() => route.params.type)
const subtopicId = computed(() => route.query.subtopic_id || null)
const moduleTitle = computed(() => modulesStore.activeModule?.title || 'Asesmen Modul')
const passThreshold = 60
const moduleDiagnosis = computed(() => progressStore.moduleDiagnoses[moduleId.value] || null)
const personalDiagnosisItems = computed(() =>
  moduleDiagnosis.value?.personal_recommendations?.length
    ? moduleDiagnosis.value.personal_recommendations
    : moduleDiagnosis.value?.recommendations || []
)
const updatedQValueItems = computed(() =>
  Object.entries(submissionResult.value?.updatedQValues || {}).map(([action, value]) => ({
    action,
    value,
  }))
)
const qActionScoreItems = computed(() =>
  Object.entries(moduleDiagnosis.value?.q_action_scores || {})
    .map(([action, value]) => ({ action, value }))
    .sort((a, b) => Number(b.value || 0) - Number(a.value || 0))
)
const moduleSubtopics = computed(() => modulesStore.activeModule?.subtopics || [])
const moduleSubtopicMasteries = computed(() => {
  return moduleSubtopics.value.map((subtopic) => {
    const progress = progressStore.subtopicMastery.find((item) => item.topic_id === subtopic.id || item.id === subtopic.id)
    return {
      id: subtopic.id,
      name: subtopic.title,
      mastery: Math.round(progress?.mastery || 0),
    }
  })
})
const moduleMastery = computed(() => {
  if (!moduleSubtopicMasteries.value.length) return 0
  const total = moduleSubtopicMasteries.value.reduce((sum, item) => sum + item.mastery, 0)
  return Math.round(total / moduleSubtopicMasteries.value.length)
})
const weakModuleSubtopics = computed(() =>
  moduleSubtopicMasteries.value.filter((item) => item.mastery < 80).slice(0, 3)
)
const canContinue = computed(() => moduleMastery.value >= passThreshold)
const quizPassed = computed(() => scorePercentage.value >= passThreshold)
const nextModule = computed(() => {
  const currentOrder = modulesStore.activeModule?.order
  if (!currentOrder) return null
  return modulesStore.modules.find((module) => module.order === currentOrder + 1) || null
})
const reportMessage = computed(() => {
  if (canContinue.value) {
    return nextModule.value
      ? `Penguasaan modul sudah melewati threshold ${passThreshold}%, jadi kamu bisa lanjut ke ${nextModule.value.title}.`
      : `Penguasaan modul sudah melewati threshold ${passThreshold}%, dan ini adalah modul terakhir.`
  }

  return `Penguasaan modul masih di bawah threshold ${passThreshold}%, jadi sistem menyarankan review materi sebelum lanjut.`
})

function formatPercent(value) {
  const numericValue = Number(value || 0)
  return `${Math.round(numericValue)}%`
}

function formatNumber(value) {
  const numericValue = Number(value)
  if (Number.isNaN(numericValue)) return '0.00'
  return numericValue.toFixed(2)
}

function labelForAction(action) {
  const labels = {
    show_text: 'Ringkasan',
    show_video: 'Video',
    easy_quiz: 'Latihan ringan',
    hard_quiz: 'Tantangan',
    review_previous: 'Review',
    pre_test: 'Pre test',
    quiz: 'Quiz',
    drill: 'Drill',
    post_test: 'Post test',
  }
  return labels[action] || action
}

const assessmentLabel = computed(() => {
  const labels = {
    pre_test: 'Pre Test',
    quiz: 'Quiz Subtopik',
    post_test: 'Post Test',
  }
  return labels[assessmentType.value] || 'Asesmen'
})

const finishedTitle = computed(() => `${assessmentLabel.value} selesai`)
const isNavigating = ref(false)
const pageError = ref('')

const finishButtonLabel = computed(() => {
  if (assessmentType.value === 'pre_test') return 'Masuk ke Materi'
  if (assessmentType.value === 'quiz' && !quizPassed.value) return 'Review Materi'
  if (assessmentType.value === 'quiz' && route.query.final === '1') return 'Lanjut Post Test'
  if (assessmentType.value === 'quiz') return route.query.next === '1' ? 'Lanjut Subtopik Berikutnya' : 'Kembali ke Materi'
  return 'Kembali ke Dashboard'
})

async function loadAssessment() {
  pageError.value = ''
  isNavigating.value = false
  quizStore.clearQuestions()

  if (modulesStore.modules.length === 0) {
    await modulesStore.fetchModules()
  }

  if (!modulesStore.activeModule || modulesStore.activeModule.id !== moduleId.value) {
    await modulesStore.fetchModuleById(moduleId.value)
  }

  if (modulesStore.activeModule?.status === 'locked') {
    pageError.value = 'Modul ini masih terkunci. Selesaikan modul prasyarat terlebih dahulu.'
    quizStore.clearQuestions()
    return
  }

  if (subtopicId.value) {
    await modulesStore.goToModuleSubtopic(moduleId.value, subtopicId.value)
  }

  const action = assessmentType.value === 'quiz' ? 'subtopic_quiz' : assessmentType.value
  try {
    await quizStore.fetchQuestions(moduleId.value, action, assessmentType.value, subtopicId.value)
  } catch (error) {
    pageError.value = error?.response?.data?.detail || quizStore.error || 'Asesmen belum bisa dibuka.'
  }
}

onMounted(loadAssessment)

function optionClass(optionId) {
  if (!isSubmitted.value) {
    return 'border-gray-200 bg-white hover:border-primary-300 hover:bg-primary-50 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-primary-900/10'
  }

  const correct = submissionResult.value?.correctAnswer === optionId
  const selected = selectedAnswer.value === optionId
  if (correct) return 'border-success-500 bg-success-50 text-success-700'
  if (selected && !correct) return 'border-danger-500 bg-danger-50 text-danger-700'
  return 'border-gray-200 bg-white opacity-50 dark:border-gray-700 dark:bg-gray-800'
}

function labelClass(optionId) {
  if (!isSubmitted.value) return 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300'
  const correct = submissionResult.value?.correctAnswer === optionId
  const selected = selectedAnswer.value === optionId
  if (correct) return 'bg-success-500 text-white'
  if (selected && !correct) return 'bg-danger-500 text-white'
  return 'bg-gray-100 text-gray-400 dark:bg-gray-700'
}

function submitAnswer(questionId, optionId) {
  quizStore.submitAnswer(questionId, optionId)
}

function nextQuestion() {
  quizStore.nextQuestion()
}

function goBack() {
  router.push({ name: 'Dashboard' })
}

async function finishAssessment() {
  if (isNavigating.value) return
  isNavigating.value = true

  quizStore.markAssessmentDone(moduleId.value)

  if (assessmentType.value === 'quiz' && !quizPassed.value) {
    quizStore.clearQuestions()
    router.push({ name: 'Dashboard' })
    return
  }

  if (assessmentType.value === 'quiz' && route.query.next === '1') {
    quizStore.markSubtopicQuizDone(moduleId.value, subtopicId.value)
    quizStore.clearQuestions()
    // Advance to next subtopic, then refresh modules so sidebar shows updated completed status
    modulesStore.nextSubtopic()
    const targetIndex = modulesStore.activeSubtopicIndex
    await modulesStore.fetchModules()
    // Re-fetch the module detail but restore the subtopic index (fetchModuleById resets to 0)
    await modulesStore.fetchModuleById(moduleId.value)
    modulesStore.goToSubtopic(targetIndex)
    router.push({ name: 'Dashboard' })
    return
  }

  if (assessmentType.value === 'quiz' && route.query.final === '1') {
    quizStore.markSubtopicQuizDone(moduleId.value, subtopicId.value)
    quizStore.clearQuestions()
    router.push({
      name: 'Assessment',
      params: {
        moduleId: moduleId.value,
        type: 'post_test',
      },
    })
    return
  }

  if (assessmentType.value === 'post_test' && canContinue.value && nextModule.value) {
    quizStore.markModulePassed(moduleId.value)
    quizStore.clearQuestions()
    await modulesStore.fetchModules()
    await modulesStore.fetchModuleById(nextModule.value.id)
    router.push({ name: 'Dashboard' })
    return
  }

  if (assessmentType.value === 'post_test' && canContinue.value) {
    quizStore.markModulePassed(moduleId.value)
  }

  quizStore.clearQuestions()
  router.push({ name: 'Dashboard' })
}

function reviewModule() {
  if (isNavigating.value) return
  isNavigating.value = true
  quizStore.markAssessmentDone(moduleId.value)
  quizStore.clearQuestions()
  modulesStore.goToSubtopic(0)
  router.push({ name: 'Dashboard' })
}

watch(
  () => [route.params.moduleId, route.params.type, route.query.subtopic_id],
  async (_next, previous) => {
    if (!previous) return
    await loadAssessment()
  }
)

watch(
  () => quizFinished.value,
  async (finished) => {
    if (finished) {
      // Refresh progress data so computed properties (like moduleMastery) update
      await progressStore.fetchAll()
      if (assessmentType.value === 'post_test') {
        await progressStore.fetchModuleDiagnosis(moduleId.value)
      }
    }
  }
)
</script>
