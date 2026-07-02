<template>
  <main class="min-h-screen bg-surface-50 p-4 text-gray-800 dark:bg-gray-900 dark:text-gray-100 lg:p-8">
    <section class="mx-auto max-w-6xl">
      <div class="mb-6 flex flex-wrap items-center justify-between gap-3">
        <div>
          <p class="text-sm font-bold uppercase tracking-wide text-primary-600">admin panel</p>
          <h1 class="text-2xl font-black text-gray-950 dark:text-white">{{ title }}</h1>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">{{ description }}</p>
        </div>
        <RouterLink
          to="/"
          class="rounded-xl bg-primary-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-primary-700"
        >
          dashboard
        </RouterLink>
      </div>

      <nav class="mb-4 flex flex-wrap gap-2 rounded-2xl border border-gray-100 bg-white p-2 shadow-card dark:border-gray-700 dark:bg-gray-800">
        <RouterLink
          v-for="item in items"
          :key="item.to"
          :to="item.to"
          class="rounded-xl px-4 py-2 text-sm font-bold transition"
          :class="route.path === item.to
            ? 'bg-primary-600 text-white shadow-sm'
            : 'text-gray-600 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-gray-700/50'"
        >
          {{ item.label }}
        </RouterLink>
      </nav>

      <slot />
    </section>
  </main>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()

const items = [
  { to: '/admin', label: 'Graph Prasyarat' },
  { to: '/admin/questions', label: 'Soal' },
  { to: '/admin/materials', label: 'Materi' },
]

const title = computed(() => {
  if (route.path === '/admin/questions') return 'kelola soal quiz'
  if (route.path === '/admin/materials') return 'kelola subtopik'
  return 'atur prasyarat topik'
})

const description = computed(() => {
  if (route.path === '/admin/questions') return 'soal dan difficulty ini dipakai q-learning untuk easy quiz dan hard quiz.'
  if (route.path === '/admin/materials') return 'content json ini langsung dipakai oleh module viewer di dashboard mahasiswa.'
  return 'relasi ini dipakai gkt untuk menentukan back trace learning path.'
})
</script>
