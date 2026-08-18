<template>
  <main class="h-full overflow-y-auto bg-surface-50 px-4 py-5 text-gray-800 dark:bg-gray-900 dark:text-gray-100 sm:px-6">
    <section class="mx-auto w-full max-w-3xl">
      <div class="mb-4 flex items-center justify-between gap-3">
        <RouterLink
          class="inline-flex items-center gap-2 rounded-xl border border-gray-200 bg-white px-3 py-2 text-sm font-bold text-gray-600 transition hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
          to="/"
        >
          <ArrowLeft class="h-4 w-4" />
          Dashboard
        </RouterLink>
        <span class="rounded-full bg-white px-3 py-1 text-xs font-bold text-gray-500 shadow-sm dark:bg-gray-800">
          {{ answeredCount }}/{{ cognitiveStore.items.length || 16 }} terisi
        </span>
      </div>

      <header class="mb-4 rounded-2xl border border-gray-100 bg-white p-5 shadow-card dark:border-gray-700 dark:bg-gray-800">
        <p class="text-xs font-black uppercase tracking-wide text-primary-600 dark:text-primary-300">
          profil kognitif
        </p>
        <h1 class="mt-2 text-2xl font-black leading-tight text-gray-950 dark:text-white">
          instrumen perkembangan kognitif
        </h1>
        <p class="mt-2 text-sm leading-6 text-gray-500 dark:text-gray-400">
          jawab sesuai kondisi kamu. hasil pertama akan dikunci dan dipakai sistem untuk menyesuaikan rekomendasi belajar.
        </p>
        <p v-if="isLocked" class="mt-3 rounded-xl bg-success-50 px-3 py-2 text-xs font-bold text-success-700 dark:bg-success-900/20 dark:text-success-300">
          Profil kognitif sudah diisi dan dikunci.
        </p>

        <div class="mt-4">
          <div class="mb-1 flex items-center justify-between text-xs font-bold text-gray-500">
            <span>progress pengisian</span>
            <span>{{ completionPercent }}%</span>
          </div>
          <div class="h-2 overflow-hidden rounded-full bg-gray-100 dark:bg-gray-700">
            <div class="h-full rounded-full bg-primary-600 transition-all" :style="{ width: `${completionPercent}%` }" />
          </div>
        </div>
      </header>

      <form class="space-y-4 pb-6" @submit.prevent="submitForm">
        <section class="rounded-2xl border border-gray-100 bg-white p-4 shadow-card dark:border-gray-700 dark:bg-gray-800">
          <p class="text-xs font-bold uppercase text-gray-400">keterangan skala</p>
          <div class="mt-3 grid gap-2 sm:grid-cols-5">
            <div
              v-for="option in scaleOptions"
              :key="option.value"
              class="rounded-xl border border-gray-100 bg-gray-50 p-2 text-center dark:border-gray-700 dark:bg-gray-900/60"
            >
              <p class="text-sm font-black text-primary-600 dark:text-primary-300">{{ option.value }}</p>
              <p class="mt-0.5 text-[11px] font-semibold leading-tight text-gray-500 dark:text-gray-400">
                {{ option.label }}
              </p>
            </div>
          </div>
        </section>

        <section v-if="cognitiveStore.profile" class="grid gap-2 sm:grid-cols-5">
          <div class="rounded-2xl border border-primary-100 bg-primary-50 p-3 sm:col-span-2 dark:border-primary-900/40 dark:bg-primary-900/20">
            <p class="text-[11px] font-bold uppercase text-primary-600 dark:text-primary-300">tahap dominan</p>
            <p class="mt-1 text-lg font-black text-gray-950 dark:text-white">{{ cognitiveStore.dominantStageLabel }}</p>
          </div>
          <div
            v-for="score in scoreCards"
            :key="score.label"
            class="rounded-2xl border border-gray-100 bg-white p-3 shadow-sm dark:border-gray-700 dark:bg-gray-800"
          >
            <p class="text-[11px] font-bold uppercase text-gray-400">{{ score.label }}</p>
            <p class="mt-1 text-lg font-black text-gray-950 dark:text-white">{{ score.value }}</p>
          </div>
        </section>

        <div v-if="cognitiveStore.loading && !cognitiveStore.items.length" class="flex items-center justify-center rounded-2xl border border-gray-100 bg-white py-12 text-sm font-semibold text-gray-500 shadow-card dark:border-gray-700 dark:bg-gray-800">
          <LoadingSpinner class="mr-2 text-primary-600" />
          memuat instrumen...
        </div>

        <section v-else class="space-y-3">
          <article
            v-for="item in cognitiveStore.items"
            :key="item.id"
            class="rounded-2xl border border-gray-100 bg-white p-4 shadow-sm dark:border-gray-700 dark:bg-gray-800"
          >
            <div class="mb-3 flex items-start justify-between gap-3">
              <div class="min-w-0">
                <p class="text-[11px] font-black uppercase tracking-wide text-primary-600 dark:text-primary-300">
                  {{ item.code }}
                </p>
                <p class="mt-1 text-sm font-bold leading-6 text-gray-900 dark:text-gray-100">
                  {{ item.statement }}
                </p>
              </div>
            </div>

            <fieldset>
              <legend class="sr-only">{{ item.statement }}</legend>
              <div class="grid grid-cols-5 gap-2">
                <label
                  v-for="option in scaleOptions"
                  :key="`${item.id}-${option.value}`"
                  class="flex h-11 cursor-pointer items-center justify-center rounded-xl border text-sm font-black transition"
                  :class="answers[item.id] === option.value
                    ? 'border-primary-600 bg-primary-600 text-white'
                    : isLocked
                      ? 'border-gray-200 bg-gray-50 text-gray-400 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-500'
                      : 'border-gray-200 bg-gray-50 text-gray-500 hover:border-primary-300 hover:bg-primary-50 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-300 dark:hover:bg-primary-900/20'"
                  :title="option.label"
                >
                  <input v-model.number="answers[item.id]" class="sr-only" type="radio" :name="`item-${item.id}`" :value="option.value" :disabled="isLocked">
                  {{ option.value }}
                </label>
              </div>
              <div class="mt-2 flex justify-between text-[11px] font-semibold text-gray-400">
                <span>sangat tidak setuju</span>
                <span>sangat setuju</span>
              </div>
            </fieldset>
          </article>
        </section>

        <div v-if="cognitiveStore.error" class="rounded-xl border border-danger-100 bg-danger-50 p-3 text-sm font-semibold text-danger-700">
          {{ cognitiveStore.error }}
        </div>

        <div class="sticky bottom-3 rounded-2xl border border-gray-100 bg-white/95 p-3 shadow-elevated backdrop-blur dark:border-gray-700 dark:bg-gray-800/95">
          <p v-if="isLocked" class="rounded-xl bg-gray-50 px-4 py-3 text-center text-sm font-black text-gray-500 dark:bg-gray-900 dark:text-gray-300">
            Profil kognitif sudah terkunci
          </p>
          <button
            v-else
            class="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-primary-600 px-5 py-3 text-sm font-black text-white transition hover:bg-primary-700 disabled:cursor-not-allowed disabled:opacity-50"
            type="submit"
            :disabled="!canSubmit || cognitiveStore.loading"
          >
            <LoadingSpinner v-if="cognitiveStore.loading" size="sm" />
            {{ cognitiveStore.loading ? 'Menyimpan...' : 'Simpan Profil' }}
          </button>
        </div>
      </form>
    </section>
  </main>
</template>

<script setup>
import { computed, onMounted, reactive } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { ArrowLeft } from 'lucide-vue-next'
import { useCognitiveStore } from '@/stores/cognitive'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

const router = useRouter()
const cognitiveStore = useCognitiveStore()
const answers = reactive({})

const scaleOptions = [
  { value: 1, label: 'sangat tidak setuju' },
  { value: 2, label: 'tidak setuju' },
  { value: 3, label: 'netral' },
  { value: 4, label: 'setuju' },
  { value: 5, label: 'sangat setuju' },
]

const answeredCount = computed(() =>
  cognitiveStore.items.filter((item) => Number(answers[item.id]) >= 1 && Number(answers[item.id]) <= 5).length
)

const completionPercent = computed(() => {
  if (!cognitiveStore.items.length) return 0
  return Math.round((answeredCount.value / cognitiveStore.items.length) * 100)
})

const scoreCards = computed(() => {
  const profile = cognitiveStore.profile || {}
  return [
    { label: 'dual', value: formatScore(profile.dualism_score) },
    { label: 'multi', value: formatScore(profile.multiplicity_score) },
    { label: 'relatif', value: formatScore(profile.relativism_score) },
  ]
})

const canSubmit = computed(() =>
  !isLocked.value &&
  cognitiveStore.items.length > 0 &&
  cognitiveStore.items.every((item) => Number(answers[item.id]) >= 1 && Number(answers[item.id]) <= 5)
)

const isLocked = computed(() => cognitiveStore.responses.length > 0)

function formatScore(value) {
  const number = Number(value || 0)
  return number.toFixed(2)
}

async function submitForm() {
  if (!canSubmit.value || isLocked.value) return
  const payload = cognitiveStore.items.map((item) => ({
    item_id: item.id,
    score: answers[item.id],
  }))
  const profile = await cognitiveStore.submit(payload)
  if (profile) {
    router.push('/')
  }
}

onMounted(async () => {
  await Promise.all([
    cognitiveStore.fetchItems(),
    cognitiveStore.fetchProfile(),
    cognitiveStore.fetchResponses(),
  ])
  cognitiveStore.responses.forEach((response) => {
    answers[response.item_id] = response.score
  })
})
</script>
