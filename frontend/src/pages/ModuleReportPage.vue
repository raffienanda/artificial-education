<template>
  <div class="h-full overflow-y-auto bg-slate-50 p-4 dark:bg-gray-950 sm:p-6">
    <div class="mx-auto w-full max-w-5xl">
      <div class="mb-5 flex flex-wrap items-center justify-between gap-3">
        <div>
          <p class="text-sm font-bold uppercase text-primary-600 dark:text-primary-300">Rapor Modul</p>
          <h1 class="mt-1 text-2xl font-black text-gray-950 dark:text-white">{{ moduleTitle }}</h1>
          <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
            hasil akhir modul dan rekomendasi belajar personal setelah post test.
          </p>
        </div>
        <button
          class="rounded-xl border border-gray-200 bg-white px-4 py-2 text-sm font-bold text-gray-600 transition hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-300 dark:hover:bg-gray-800"
          type="button"
          @click="router.push({ name: 'Dashboard' })"
        >
          Kembali
        </button>
      </div>

      <div v-if="loading" class="flex items-center justify-center rounded-2xl bg-white p-8 text-sm font-semibold text-gray-500 shadow-sm dark:bg-gray-900">
        <LoadingSpinner class="mr-2 text-primary-600" />
        Memuat rapor...
      </div>

      <div v-else-if="!moduleDiagnosis?.available" class="rounded-2xl bg-white p-8 text-center shadow-sm dark:bg-gray-900">
        <h2 class="text-lg font-black text-gray-950 dark:text-white">Rapor belum tersedia</h2>
        <p class="mx-auto mt-2 max-w-md text-sm leading-relaxed text-gray-500 dark:text-gray-400">
          Rapor modul baru muncul setelah semua quiz subtopik dan post test modul selesai.
        </p>
      </div>

      <div v-else class="grid gap-5">
        <section class="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900 sm:p-6">
          <div class="grid gap-3 sm:grid-cols-4">
            <div class="rounded-xl bg-slate-50 p-4 dark:bg-gray-950/60">
              <p class="text-xs font-bold uppercase text-gray-400">Pre Test</p>
              <p class="mt-2 text-2xl font-black text-gray-950 dark:text-white">{{ formatPercent(moduleDiagnosis.pre_test_score) }}</p>
            </div>
            <div class="rounded-xl bg-slate-50 p-4 dark:bg-gray-950/60">
              <p class="text-xs font-bold uppercase text-gray-400">Quiz Rata-rata</p>
              <p class="mt-2 text-2xl font-black text-gray-950 dark:text-white">{{ formatPercent(moduleDiagnosis.quiz_average) }}</p>
            </div>
            <div class="rounded-xl bg-slate-50 p-4 dark:bg-gray-950/60">
              <p class="text-xs font-bold uppercase text-gray-400">Post Test</p>
              <p class="mt-2 text-2xl font-black text-gray-950 dark:text-white">{{ formatPercent(moduleDiagnosis.post_test_score) }}</p>
            </div>
            <div class="rounded-xl bg-slate-50 p-4 dark:bg-gray-950/60">
              <p class="text-xs font-bold uppercase text-gray-400">Profil Kognitif</p>
              <p class="mt-2 text-lg font-black capitalize text-gray-950 dark:text-white">{{ moduleDiagnosis.cognitive_stage || '-' }}</p>
            </div>
          </div>

          <div class="mt-5 rounded-xl border p-4" :class="statusCardClass">
            <p class="text-xs font-bold uppercase" :class="statusTextClass">Rekomendasi Akhir</p>
            <h2 class="mt-1 text-xl font-black capitalize" :class="statusTextClass">
              {{ moduleDiagnosis.category }}
            </h2>
            <p class="mt-2 text-sm font-semibold leading-relaxed text-gray-700 dark:text-gray-200">
              {{ moduleDiagnosis.summary }}
            </p>
            <p
              v-if="moduleDiagnosis.personal_pattern"
              class="mt-3 rounded-lg bg-white px-3 py-2 text-sm font-semibold leading-relaxed text-gray-700 shadow-sm dark:bg-gray-800 dark:text-gray-200"
            >
              {{ moduleDiagnosis.personal_pattern }}
            </p>
          </div>
        </section>

        <section class="grid gap-5 lg:grid-cols-[minmax(0,1fr)_340px]">
          <div class="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900 sm:p-6">
            <h3 class="text-base font-black text-gray-950 dark:text-white">Saran personal</h3>
            <div class="mt-4 grid gap-3">
              <div
                v-for="item in personalDiagnosisItems"
                :key="item"
                class="rounded-xl border border-gray-100 bg-slate-50 px-4 py-3 text-sm font-semibold leading-relaxed text-gray-700 dark:border-gray-800 dark:bg-gray-950/60 dark:text-gray-200"
              >
                {{ item }}
              </div>
            </div>
          </div>

          <aside class="grid content-start gap-5">
            <div class="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900">
              <p class="text-xs font-bold uppercase text-gray-400">Effort vs Hasil</p>
              <div class="mt-3 grid grid-cols-2 gap-3">
                <div class="rounded-xl bg-slate-50 p-3 dark:bg-gray-950/60">
                  <p class="text-xs font-bold text-gray-400">Effort</p>
                  <p class="mt-1 text-sm font-black capitalize text-gray-950 dark:text-white">{{ moduleDiagnosis.effort_level }}</p>
                </div>
                <div class="rounded-xl bg-slate-50 p-3 dark:bg-gray-950/60">
                  <p class="text-xs font-bold text-gray-400">Hasil</p>
                  <p class="mt-1 text-sm font-black capitalize text-gray-950 dark:text-white">{{ moduleDiagnosis.outcome_level }}</p>
                </div>
              </div>
            </div>

            <div v-if="moduleDiagnosis.weak_subtopics?.length" class="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900">
              <p class="text-xs font-bold uppercase text-gray-400">Materi prioritas</p>
              <div class="mt-3 flex flex-wrap gap-2">
                <span
                  v-for="item in moduleDiagnosis.weak_subtopics"
                  :key="item.id"
                  class="rounded-lg bg-slate-100 px-3 py-1.5 text-xs font-bold text-gray-700 dark:bg-gray-800 dark:text-gray-200"
                >
                  {{ item.title }} · {{ formatPercent(item.mastery) }}
                </span>
              </div>
            </div>

            <div v-if="qActionScoreItems.length" class="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900">
              <p class="text-xs font-bold uppercase text-gray-400">Q-value strategi belajar</p>
              <div class="mt-3 grid gap-2">
                <div
                  v-for="item in qActionScoreItems"
                  :key="item.action"
                  class="flex items-center justify-between gap-2 rounded-xl bg-slate-50 px-3 py-2 text-xs dark:bg-gray-950/60"
                >
                  <span class="font-bold text-gray-700 dark:text-gray-200">{{ labelForAction(item.action) }}</span>
                  <span class="font-black tabular-nums text-primary-700 dark:text-primary-300">{{ formatNumber(item.value) }}</span>
                </div>
              </div>
            </div>
          </aside>
        </section>

        <section class="flex flex-wrap justify-end gap-3">
          <button
            class="rounded-xl border border-gray-200 bg-white px-5 py-3 text-sm font-black text-gray-600 transition hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-300 dark:hover:bg-gray-800"
            type="button"
            @click="reviewModule"
          >
            Review Modul
          </button>
          <button
            v-if="canRetakePostTest"
            class="rounded-xl border border-warning-200 bg-warning-50 px-5 py-3 text-sm font-black text-warning-700 transition hover:bg-warning-100"
            type="button"
            @click="retakePostTest"
          >
            Ulang Post Test
          </button>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useModulesStore } from '@/stores/modules'
import { useProgressStore } from '@/stores/progress'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

const route = useRoute()
const router = useRouter()
const modulesStore = useModulesStore()
const progressStore = useProgressStore()
const loading = ref(false)

const moduleId = computed(() => route.params.moduleId)
const moduleDiagnosis = computed(() => progressStore.moduleDiagnoses[moduleId.value] || null)
const moduleTitle = computed(() => modulesStore.activeModule?.title || 'Rapor Modul')
const personalDiagnosisItems = computed(() =>
  moduleDiagnosis.value?.personal_recommendations?.length
    ? moduleDiagnosis.value.personal_recommendations
    : moduleDiagnosis.value?.recommendations || []
)
const qActionScoreItems = computed(() =>
  Object.entries(moduleDiagnosis.value?.q_action_scores || {})
    .map(([action, value]) => ({ action, value }))
    .sort((a, b) => Number(b.value || 0) - Number(a.value || 0))
)
const canRetakePostTest = computed(() => Boolean(moduleDiagnosis.value?.can_retake_post_test))
const statusCardClass = computed(() => {
  const category = moduleDiagnosis.value?.category || ''
  if (category.includes('lanjut')) return 'border-emerald-100 bg-emerald-50/80 dark:border-emerald-900/40 dark:bg-emerald-950/20'
  if (category.includes('pendampingan')) return 'border-rose-100 bg-rose-50/80 dark:border-rose-900/40 dark:bg-rose-950/20'
  return 'border-amber-100 bg-amber-50/80 dark:border-amber-900/40 dark:bg-amber-950/20'
})
const statusTextClass = computed(() => {
  const category = moduleDiagnosis.value?.category || ''
  if (category.includes('lanjut')) return 'text-emerald-700 dark:text-emerald-300'
  if (category.includes('pendampingan')) return 'text-rose-700 dark:text-rose-300'
  return 'text-amber-700 dark:text-amber-300'
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

async function reviewModule() {
  if (moduleId.value) {
    await modulesStore.fetchModuleById(moduleId.value)
  }
  router.push({ name: 'Dashboard' })
}

function retakePostTest() {
  router.push({
    name: 'Assessment',
    params: {
      moduleId: moduleId.value,
      type: 'post_test',
    },
  })
}

onMounted(async () => {
  loading.value = true
  try {
    if (modulesStore.modules.length === 0) {
      await modulesStore.fetchModules()
    }
    if (!modulesStore.activeModule || modulesStore.activeModule.id !== moduleId.value) {
      await modulesStore.fetchModuleById(moduleId.value)
    }
    await progressStore.fetchAll()
    await progressStore.fetchModuleDiagnosis(moduleId.value)
  } finally {
    loading.value = false
  }
})
</script>
