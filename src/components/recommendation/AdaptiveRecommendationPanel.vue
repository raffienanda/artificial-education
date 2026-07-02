<template>
  <section class="mb-4 rounded-xl border border-sky-100 bg-sky-50/80 p-3 dark:border-sky-900/40 dark:bg-sky-950/20">
    <div class="flex items-start gap-3">
      <div class="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-lg bg-white text-sky-600 shadow-sm dark:bg-gray-800 dark:text-sky-300">
        <BrainCircuit class="h-5 w-5" />
      </div>

      <div class="min-w-0 flex-1">
        <div class="flex flex-wrap items-center gap-2">
          <h3 class="text-sm font-bold text-gray-900 dark:text-gray-100">Rekomendasi AI</h3>
          <BaseBadge :variant="badgeVariant" size="xs" dot>
            {{ recommendationStore.macroActionLabel }}
          </BaseBadge>
        </div>

        <p v-if="recommendationStore.loading" class="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Menganalisis jalur belajar...
        </p>
        <p v-else-if="recommendationStore.error" class="mt-1 text-xs text-danger-600 dark:text-danger-300">
          {{ recommendationStore.error }}
        </p>
        <template v-else-if="recommendation">
          <p class="mt-1 text-xs leading-relaxed text-gray-600 dark:text-gray-300">
            {{ recommendation.reason }}
          </p>

          <div class="mt-2 flex flex-wrap items-center gap-2">
            <span class="inline-flex items-center gap-1.5 rounded-lg bg-white px-2.5 py-1 text-xs font-semibold text-gray-700 shadow-sm dark:bg-gray-800 dark:text-gray-200">
              <component :is="actionIcon" class="h-3.5 w-3.5 text-sky-500" />
              {{ recommendationStore.microActionLabel }}
            </span>
            <span class="rounded-lg bg-white px-2.5 py-1 text-xs font-medium text-gray-500 shadow-sm dark:bg-gray-800 dark:text-gray-400">
              State: {{ recommendation.state }}
            </span>
          </div>

          <div class="mt-3 rounded-xl bg-white/80 p-2 shadow-sm dark:bg-gray-800/80">
            <div class="mb-1.5 flex items-center justify-between">
              <p class="text-[11px] font-bold uppercase tracking-wide text-gray-500 dark:text-gray-400">
                Q-values
              </p>
              <p class="text-[11px] text-gray-400 dark:text-gray-500">
                tertinggi dipilih
              </p>
            </div>
            <div class="grid grid-cols-1 gap-1.5 sm:grid-cols-2">
              <div
                v-for="item in qValueItems"
                :key="item.action"
                class="flex items-center justify-between gap-2 rounded-lg border px-2.5 py-1.5 text-xs"
                :class="item.selected
                  ? 'border-sky-300 bg-sky-50 text-sky-700 dark:border-sky-800 dark:bg-sky-950/30 dark:text-sky-300'
                  : 'border-gray-100 bg-gray-50 text-gray-600 dark:border-gray-700 dark:bg-gray-900/40 dark:text-gray-300'"
              >
                <span class="truncate font-medium">{{ item.label }}</span>
                <span class="font-bold tabular-nums">{{ formatNumber(item.value) }}</span>
              </div>
            </div>
          </div>

          <div v-if="recentLogs.length" class="mt-3 rounded-xl bg-white/80 p-2 shadow-sm dark:bg-gray-800/80">
            <div class="mb-1.5 flex items-center justify-between">
              <p class="text-[11px] font-bold uppercase tracking-wide text-gray-500 dark:text-gray-400">
                Riwayat Adaptasi
              </p>
              <p class="text-[11px] text-gray-400 dark:text-gray-500">
                terbaru
              </p>
            </div>
            <div class="space-y-1.5">
              <div
                v-for="log in recentLogs"
                :key="`${log.subtopic_id}-${log.created_at}`"
                class="flex items-center justify-between gap-2 rounded-lg bg-gray-50 px-2.5 py-1.5 text-xs dark:bg-gray-900/40"
              >
                <div class="min-w-0">
                  <p class="truncate font-semibold text-gray-700 dark:text-gray-200">
                    {{ formatAction(log.action) }}
                  </p>
                  <p class="truncate text-[11px] text-gray-400">
                    {{ log.subtopic_id }} | {{ log.state }}
                  </p>
                </div>
                <span
                  class="flex-shrink-0 rounded-lg px-2 py-0.5 font-bold tabular-nums"
                  :class="log.reward >= 0 ? 'bg-success-100 text-success-700' : 'bg-danger-100 text-danger-700'"
                >
                  {{ signedNumber(log.reward) }}
                </span>
              </div>
            </div>
          </div>
        </template>
        <p v-else class="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Pilih subtopik untuk memulai analisis.
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
import { computed } from 'vue'
import { BookOpen, BrainCircuit, ClipboardCheck, Dumbbell, PlayCircle, RotateCcw, Route } from 'lucide-vue-next'
import BaseBadge from '@/components/common/BaseBadge.vue'
import { useModulesStore } from '@/stores/modules'
import { useRecommendationStore } from '@/stores/recommendation'

const modulesStore = useModulesStore()
const recommendationStore = useRecommendationStore()

const recommendation = computed(() => recommendationStore.current)
const canApplyBackTrace = computed(() => (
  recommendationStore.shouldBackTrace &&
  recommendation.value?.recommended_module_id &&
  recommendation.value?.recommended_subtopic_id
))

const badgeVariant = computed(() => (
  recommendationStore.shouldBackTrace ? 'warning' : 'info'
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
    ['show_text', 'Baca ringkasan'],
    ['show_video', 'Tonton video'],
    ['easy_quiz', 'Quiz mudah'],
    ['hard_quiz', 'Quiz tantangan'],
    ['review_previous', 'Review sebelumnya'],
  ]
  const values = recommendation.value?.q_values || {}

  return actions.map(([action, label]) => ({
    action,
    label,
    value: values[action] ?? 0,
    selected: action === recommendationStore.microAction,
  }))
})

const recentLogs = computed(() => recommendationStore.logs.slice(0, 3))

function formatNumber(value) {
  const numericValue = Number(value)
  if (Number.isNaN(numericValue)) return '0.00'
  return numericValue.toFixed(2)
}

function signedNumber(value) {
  const numericValue = Number(value)
  if (Number.isNaN(numericValue)) return '+0'
  return numericValue > 0 ? `+${numericValue.toFixed(0)}` : numericValue.toFixed(0)
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

async function applyRecommendation() {
  await modulesStore.goToModuleSubtopic(
    recommendation.value.recommended_module_id,
    recommendation.value.recommended_subtopic_id,
  )
}
</script>
