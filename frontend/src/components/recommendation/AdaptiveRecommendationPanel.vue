<template>
  <section class="mb-4 rounded-xl border border-sky-100 bg-sky-50/80 p-3 dark:border-sky-900/40 dark:bg-sky-950/20">
    <div class="flex items-start gap-3">
      <div class="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-lg bg-white text-sky-600 shadow-sm dark:bg-gray-800 dark:text-sky-300">
        <component :is="actionIcon" class="h-5 w-5" />
      </div>

      <div class="min-w-0 flex-1">
        <div class="flex flex-wrap items-center gap-2">
          <h3 class="text-sm font-bold text-gray-900 dark:text-gray-100">Saran belajar</h3>
          <BaseBadge :variant="badgeVariant" size="xs" dot>
            {{ studentBadgeLabel }}
          </BaseBadge>
        </div>

        <p v-if="recommendationStore.loading" class="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Menyiapkan saran belajar...
        </p>
        <p v-else-if="recommendationStore.error" class="mt-1 rounded-lg bg-white/70 px-2.5 py-2 text-xs font-semibold text-gray-500 shadow-sm dark:bg-gray-800/70 dark:text-gray-300">
          Saran belajar belum bisa dimuat. Kamu tetap bisa lanjut belajar dari materi yang sedang dibuka.
        </p>
        <template v-else-if="recommendation">
          <p class="mt-1 text-sm font-semibold leading-relaxed text-gray-800 dark:text-gray-100">
            {{ studentTitle }}
          </p>
          <p class="mt-1 text-xs leading-relaxed text-gray-600 dark:text-gray-300">
            {{ studentReason }}
          </p>

          <div class="mt-3 flex flex-wrap items-center gap-2">
            <span class="inline-flex items-center gap-1.5 rounded-lg bg-white px-2.5 py-1.5 text-xs font-bold text-sky-700 shadow-sm dark:bg-gray-800 dark:text-sky-300">
              <component :is="actionIcon" class="h-3.5 w-3.5" />
              {{ recommendationStore.microActionLabel }}
            </span>
            <span v-if="nextStepLabel" class="rounded-lg bg-white/80 px-2.5 py-1.5 text-xs font-semibold text-gray-600 shadow-sm dark:bg-gray-800/80 dark:text-gray-300">
              {{ nextStepLabel }}
            </span>
            <span class="rounded-lg bg-white/80 px-2.5 py-1.5 text-xs font-bold text-sky-700 shadow-sm dark:bg-gray-800/80 dark:text-sky-300">
              q-value {{ formatNumber(currentActionQValue) }}
            </span>
            <button
              class="rounded-lg border border-sky-200 bg-white/70 px-2.5 py-1.5 text-xs font-bold text-sky-700 transition hover:bg-white dark:border-sky-800 dark:bg-gray-800/70 dark:text-sky-300 dark:hover:bg-gray-800"
              type="button"
              @click="debugOpen = !debugOpen"
            >
              {{ debugOpen ? 'Tutup Q-value' : 'Lihat Q-value' }}
            </button>
          </div>

          <div v-if="debugOpen" class="mt-3 rounded-xl bg-white/80 p-2 shadow-sm dark:bg-gray-800/80">
            <div class="grid gap-1.5 text-xs text-gray-600 dark:text-gray-300 sm:grid-cols-2">
              <div class="rounded-lg bg-gray-50 px-2.5 py-1.5 dark:bg-gray-900/50">
                <span class="font-bold text-gray-400">state</span>
                <p class="mt-0.5 font-semibold">{{ recommendation.state || '-' }}</p>
              </div>
              <div class="rounded-lg bg-gray-50 px-2.5 py-1.5 dark:bg-gray-900/50">
                <span class="font-bold text-gray-400">macro</span>
                <p class="mt-0.5 font-semibold">{{ recommendation.macro_action || '-' }}</p>
              </div>
              <div class="rounded-lg bg-gray-50 px-2.5 py-1.5 dark:bg-gray-900/50">
                <span class="font-bold text-gray-400">macro model</span>
                <p class="mt-0.5 font-semibold">{{ recommendation.macro_model || 'neural_gkt' }}</p>
              </div>
              <div class="rounded-lg bg-gray-50 px-2.5 py-1.5 dark:bg-gray-900/50">
                <span class="font-bold text-gray-400">cognitive</span>
                <p class="mt-0.5 font-semibold">{{ recommendation.cognitive_stage || 'unknown' }}</p>
              </div>
              <div class="rounded-lg bg-gray-50 px-2.5 py-1.5 dark:bg-gray-900/50">
                <span class="font-bold text-gray-400">micro</span>
                <p class="mt-0.5 font-semibold">{{ recommendation.micro_action || '-' }}</p>
              </div>
            </div>

            <div class="mt-2 rounded-lg bg-gray-50 p-2 dark:bg-gray-900/50">
              <div class="mb-1.5 flex items-center justify-between">
                <p class="text-[11px] font-bold uppercase tracking-wide text-gray-500 dark:text-gray-400">
                  nilai adaptasi
                </p>
                <p class="text-[11px] text-gray-400 dark:text-gray-500">
                  mode demo
                </p>
              </div>
              <div class="grid gap-1.5 sm:grid-cols-2">
                <div
                  v-for="item in qValueItems"
                  :key="item.key"
                  class="flex items-center justify-between gap-2 rounded-lg border px-2.5 py-1.5 text-xs"
                  :class="item.selected
                    ? 'border-sky-300 bg-sky-50 text-sky-700 dark:border-sky-800 dark:bg-sky-950/30 dark:text-sky-300'
                    : 'border-gray-100 bg-white text-gray-600 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300'"
                >
                  <span class="truncate font-medium">{{ item.label }}</span>
                  <span class="font-bold tabular-nums">{{ formatNumber(item.value) }}</span>
                </div>
              </div>
            </div>

            <p class="mt-2 text-[11px] leading-relaxed text-gray-400">
              {{ recommendation.reason }}
            </p>
          </div>
        </template>
        <p v-else class="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Pilih subtopik untuk melihat saran belajar.
        </p>
      </div>

      <button
        v-if="canApplyBackTrace"
        class="inline-flex flex-shrink-0 items-center gap-1.5 rounded-lg bg-sky-600 px-3 py-2 text-xs font-semibold text-white shadow-sm transition-colors hover:bg-sky-700"
        @click="applyRecommendation"
      >
        <Route class="h-4 w-4" />
        Buka
      </button>
    </div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'
import { BookOpen, ClipboardCheck, Dumbbell, PlayCircle, RotateCcw, Route } from 'lucide-vue-next'
import BaseBadge from '@/components/common/BaseBadge.vue'
import { useModulesStore } from '@/stores/modules'
import { useRecommendationStore } from '@/stores/recommendation'

const modulesStore = useModulesStore()
const recommendationStore = useRecommendationStore()
const debugOpen = ref(false)

const recommendation = computed(() => recommendationStore.current)
const canApplyBackTrace = computed(() => (
  recommendationStore.shouldBackTrace &&
  recommendation.value?.recommended_module_id &&
  recommendation.value?.recommended_subtopic_id
))

const badgeVariant = computed(() => (
  recommendationStore.shouldBackTrace ? 'warning' : 'info'
))

const studentBadgeLabel = computed(() => (
  recommendationStore.shouldBackTrace ? 'Ulang sebentar' : 'Lanjut belajar'
))

const studentTitle = computed(() => {
  if (isCurrentSubtopicReview.value) {
    return 'Pelajari lagi ringkasan materi ini.'
  }

  const titles = {
    show_text: 'Mulai dari ringkasan materi dulu.',
    show_video: 'Coba tonton video pembelajaran dulu.',
    easy_quiz: 'Coba latihan ringan untuk cek pemahaman.',
    hard_quiz: 'Kamu siap mencoba tantangan yang lebih sulit.',
    review_previous: 'Ulang materi sebelumnya sebentar sebelum lanjut.',
  }

  return titles[recommendationStore.microAction] || 'Ikuti saran belajar berikutnya.'
})

const studentReason = computed(() => {
  if (recommendationStore.shouldBackTrace) {
    return 'Ada materi prasyarat yang sebaiknya diperkuat dulu supaya bagian berikutnya lebih mudah dipahami.'
  }

  if (isCurrentSubtopicReview.value) {
    return 'Karena ini subtopik pertama, kamu bisa ulangi materi yang sedang dibuka dulu sebelum masuk latihan berikutnya.'
  }

  const reasons = {
    show_text: 'Ringkasan membantu kamu menangkap konsep utama sebelum masuk latihan.',
    show_video: 'Video bisa membantu kalau konsepnya lebih mudah dipahami lewat alur visual.',
    easy_quiz: 'Latihan ringan cocok untuk memastikan konsep dasarnya sudah kebaca.',
    hard_quiz: 'Tantangan ini cocok kalau kamu ingin menguji pemahaman dengan soal yang sedikit lebih tinggi.',
    review_previous: 'Review singkat bisa mengurangi kebingungan sebelum lanjut ke materi berikutnya.',
  }

  return reasons[recommendationStore.microAction] || 'Saran ini menyesuaikan progress dan riwayat belajar kamu.'
})

const nextStepLabel = computed(() => {
  if (!recommendation.value) return ''
  if (recommendationStore.shouldBackTrace) return 'buka materi yang disarankan'
  if (isCurrentSubtopicReview.value) return 'baca ulang materi ini'
  return 'ikuti langkah ini dulu'
})

const isCurrentSubtopicReview = computed(() => (
  recommendationStore.microAction === 'review_previous' &&
  !modulesStore.hasPreviousSubtopic &&
  !recommendationStore.shouldBackTrace
))

const actionIcon = computed(() => {
  const icons = {
    show_text: BookOpen,
    show_video: PlayCircle,
    easy_quiz: ClipboardCheck,
    hard_quiz: Dumbbell,
    review_previous: RotateCcw,
  }

  return icons[recommendationStore.microAction] || ClipboardCheck
})

const qValueItems = computed(() => {
  const actions = [
    ['show_text', 'Ringkasan'],
    ['show_video', 'Video'],
    ['easy_quiz', 'Latihan ringan'],
    ['hard_quiz', 'Tantangan'],
    ['review_previous', 'Review'],
    ['pre_test', 'Pre test'],
    ['quiz', 'Quiz'],
    ['drill', 'Drill'],
    ['post_test', 'Post test'],
  ]
  const values = recommendation.value?.q_values || {}
  const valuesByState = recommendation.value?.q_value_states || {}
  const stateEntries = Object.entries(valuesByState)
    .flatMap(([state, stateValues]) =>
      Object.entries(stateValues || {}).map(([action, value]) => ({
        key: `${state}:${action}`,
        action,
        label: `${state} / ${labelForAction(action)}`,
        value,
        selected: state === recommendation.value?.state && action === recommendationStore.microAction,
      }))
    )

  if (stateEntries.length > 0) {
    return stateEntries
  }

  return actions.map(([action, label]) => ({
    key: action,
    action,
    label,
    value: values[action] ?? 0,
    selected: action === recommendationStore.microAction,
  }))
})

const currentActionQValue = computed(() => {
  const stateValues = recommendation.value?.q_value_states?.[recommendation.value?.state] || {}
  return stateValues[recommendationStore.microAction] ?? recommendation.value?.q_values?.[recommendationStore.microAction] ?? 0
})

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

function formatNumber(value) {
  const numericValue = Number(value)
  if (Number.isNaN(numericValue)) return '0.00'
  return numericValue.toFixed(2)
}

async function applyRecommendation() {
  await modulesStore.goToModuleSubtopic(
    recommendation.value.recommended_module_id,
    recommendation.value.recommended_subtopic_id,
  )
}
</script>
