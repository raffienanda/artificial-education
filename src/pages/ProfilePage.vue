<template>
  <main class="min-h-screen bg-surface-50 p-4 text-gray-800 dark:bg-gray-900 dark:text-gray-100 lg:p-8">
    <section class="mx-auto max-w-5xl">
      <div class="mb-6 flex flex-wrap items-center justify-between gap-3">
        <div>
          <p class="text-sm font-bold uppercase tracking-wide text-primary-600">profil mahasiswa</p>
          <h1 class="text-2xl font-black text-gray-950 dark:text-white">{{ profile.name }}</h1>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">{{ profile.email }}</p>
        </div>
        <RouterLink to="/" class="rounded-xl bg-primary-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-primary-700">
          dashboard
        </RouterLink>
      </div>

      <div class="mb-4 rounded-2xl border border-gray-100 bg-white p-5 shadow-card dark:border-gray-700 dark:bg-gray-800">
        <div class="flex flex-wrap items-center gap-4">
          <div class="flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-tr from-primary-500 to-primary-700 text-2xl font-black text-white">
            {{ profile.initials }}
          </div>
          <div class="min-w-0 flex-1">
            <p class="text-lg font-black text-gray-950 dark:text-white">{{ profile.name }}</p>
            <p class="text-sm text-gray-500">{{ userStore.currentUser?.role || 'student' }}</p>
            <div class="mt-3 max-w-md">
              <div class="mb-1 flex justify-between text-xs font-bold text-gray-500">
                <span>level {{ profile.level }}</span>
                <span>{{ profile.xp }} / {{ profile.xpToNextLevel }} XP</span>
              </div>
              <div class="h-2 overflow-hidden rounded-full bg-gray-100 dark:bg-gray-700">
                <div class="h-full rounded-full bg-warning-400 transition-all" :style="{ width: userStore.xpProgress + '%' }" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="mb-4 grid gap-3 md:grid-cols-4">
        <div v-for="stat in stats" :key="stat.label" class="rounded-2xl border border-gray-100 bg-white p-4 shadow-card dark:border-gray-700 dark:bg-gray-800">
          <p class="text-xs font-bold uppercase text-gray-400">{{ stat.label }}</p>
          <p class="mt-1 text-2xl font-black text-gray-950 dark:text-white">{{ stat.value }}</p>
        </div>
      </div>

      <div class="grid gap-4 lg:grid-cols-2">
        <section class="rounded-2xl border border-gray-100 bg-white p-5 shadow-card dark:border-gray-700 dark:bg-gray-800">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-base font-bold text-gray-900 dark:text-white">reward yang sudah ditukar</h2>
            <RouterLink to="/gamification" class="text-sm font-bold text-primary-600">reward shop</RouterLink>
          </div>

          <div v-if="redeemedRewards.length === 0" class="rounded-xl bg-gray-50 p-4 text-sm text-gray-500 dark:bg-gray-900/50">
            belum ada reward yang ditukar.
          </div>
          <div v-else class="space-y-2">
            <article v-for="reward in redeemedRewards" :key="reward.id" class="rounded-xl border border-gray-100 p-3 dark:border-gray-700">
              <p class="text-sm font-bold text-gray-900 dark:text-white">{{ reward.title }}</p>
              <p class="mt-1 text-xs text-gray-500">{{ reward.description }}</p>
            </article>
          </div>
        </section>

        <section class="rounded-2xl border border-gray-100 bg-white p-5 shadow-card dark:border-gray-700 dark:bg-gray-800">
          <h2 class="mb-4 text-base font-bold text-gray-900 dark:text-white">ringkasan akun</h2>
          <dl class="space-y-3 text-sm">
            <div class="flex justify-between gap-4">
              <dt class="text-gray-500">username</dt>
              <dd class="font-bold text-gray-900 dark:text-white">{{ userStore.currentUser?.username }}</dd>
            </div>
            <div class="flex justify-between gap-4">
              <dt class="text-gray-500">role</dt>
              <dd class="font-bold text-gray-900 dark:text-white">{{ userStore.currentUser?.role }}</dd>
            </div>
            <div class="flex justify-between gap-4">
              <dt class="text-gray-500">total xp</dt>
              <dd class="font-bold text-gray-900 dark:text-white">{{ profile.totalXp || 0 }}</dd>
            </div>
            <div class="flex justify-between gap-4">
              <dt class="text-gray-500">reward points</dt>
              <dd class="font-bold text-gray-900 dark:text-white">{{ profile.rewardPoints || 0 }}</dd>
            </div>
          </dl>
        </section>
      </div>
    </section>
  </main>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useGamificationStore } from '@/stores/gamification'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const gamificationStore = useGamificationStore()
const profile = computed(() => userStore.profile)

const stats = computed(() => [
  { label: 'level', value: profile.value.level || 1 },
  { label: 'streak', value: `${profile.value.currentStreak || 0} hari` },
  { label: 'jawaban benar', value: profile.value.totalScore || 0 },
  { label: 'poin reward', value: profile.value.rewardPoints || 0 },
])

const redeemedRewards = computed(() => {
  const redeemedIds = profile.value.redeemedRewards || []
  return gamificationStore.rewards.filter((reward) => redeemedIds.includes(reward.id))
})

onMounted(() => {
  if (gamificationStore.rewards.length === 0) {
    gamificationStore.fetchAll()
  }
})
</script>
