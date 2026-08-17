<template>
  <main class="min-h-screen bg-surface-50 p-4 text-gray-800 dark:bg-gray-900 dark:text-gray-100 lg:p-8">
    <section class="mx-auto max-w-6xl">
      <div class="mb-6 flex flex-wrap items-center justify-between gap-3">
        <div>
          <p class="text-sm font-bold uppercase tracking-wide text-primary-600">gamifikasi</p>
          <h1 class="text-2xl font-black text-gray-950 dark:text-white">leaderboard dan tema</h1>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
            xp, streak, dan poin tema bertambah dari aktivitas latihan soal.
          </p>
        </div>
        <RouterLink to="/" class="rounded-xl bg-primary-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-primary-700">
          dashboard
        </RouterLink>
      </div>

      <div class="mb-4 grid gap-3 md:grid-cols-4">
        <div class="rounded-2xl border border-gray-100 bg-white p-4 shadow-card dark:border-gray-700 dark:bg-gray-800">
          <p class="text-xs font-bold uppercase text-gray-400">level</p>
          <p class="mt-1 text-2xl font-black text-gray-950 dark:text-white">{{ profile.level }}</p>
        </div>
        <div class="rounded-2xl border border-gray-100 bg-white p-4 shadow-card dark:border-gray-700 dark:bg-gray-800">
          <p class="text-xs font-bold uppercase text-gray-400">xp</p>
          <p class="mt-1 text-2xl font-black text-gray-950 dark:text-white">{{ profile.xp }} / {{ profile.xpToNextLevel }}</p>
        </div>
        <div class="rounded-2xl border border-gray-100 bg-white p-4 shadow-card dark:border-gray-700 dark:bg-gray-800">
          <p class="text-xs font-bold uppercase text-gray-400">streak</p>
          <p class="mt-1 text-2xl font-black text-gray-950 dark:text-white">{{ profile.currentStreak }} hari</p>
        </div>
        <div class="rounded-2xl border border-gray-100 bg-white p-4 shadow-card dark:border-gray-700 dark:bg-gray-800">
          <p class="text-xs font-bold uppercase text-gray-400">poin tema</p>
          <p class="mt-1 text-2xl font-black text-gray-950 dark:text-white">{{ profile.rewardPoints }}</p>
        </div>
      </div>

      <p v-if="gamificationStore.error" class="mb-4 rounded-xl bg-danger-50 px-3 py-2 text-sm font-medium text-danger-600">
        {{ gamificationStore.error }}
      </p>
      <p v-if="gamificationStore.message" class="mb-4 rounded-xl bg-success-50 px-3 py-2 text-sm font-medium text-success-700">
        {{ gamificationStore.message }}
      </p>

      <div class="grid gap-4 lg:grid-cols-[1fr_420px]">
        <section class="rounded-2xl border border-gray-100 bg-white p-5 shadow-card dark:border-gray-700 dark:bg-gray-800">
          <h2 class="mb-4 text-base font-bold text-gray-900 dark:text-white">leaderboard</h2>
          <div v-if="gamificationStore.loading || gamificationStore.leaderboardLoading" class="py-10 text-center text-sm text-gray-500">memuat data...</div>
          <div v-else class="space-y-2">
            <article
              v-for="entry in gamificationStore.leaderboard"
              :key="entry.id"
              class="flex items-center justify-between gap-3 rounded-xl border border-gray-100 p-3 dark:border-gray-700"
            >
              <div class="flex min-w-0 items-center gap-3">
                <div class="flex h-9 w-9 items-center justify-center rounded-full bg-primary-50 text-sm font-black text-primary-600">
                  {{ entry.rank }}
                </div>
                <div class="min-w-0">
                  <p class="truncate text-sm font-bold text-gray-900 dark:text-white">{{ entry.display_name || entry.username }}</p>
                  <p class="text-xs text-gray-400">level {{ entry.level }} · streak {{ entry.current_streak }} hari</p>
                </div>
              </div>
              <div class="text-right">
                <p class="text-sm font-black text-gray-900 dark:text-white">{{ entry.xp }} XP</p>
                <p class="text-xs text-gray-400">{{ entry.total_score }} benar</p>
              </div>
            </article>
            <div v-if="gamificationStore.leaderboard.length === 0" class="rounded-xl bg-gray-50 p-4 text-center text-sm text-gray-500 dark:bg-gray-900/50">
              belum ada data leaderboard.
            </div>
            <div class="flex items-center justify-between gap-3 pt-3">
              <button
                class="rounded-xl border border-gray-200 px-4 py-2 text-sm font-bold text-gray-600 transition hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-40 dark:border-gray-700 dark:text-gray-300 dark:hover:bg-gray-700"
                :disabled="gamificationStore.leaderboardPage <= 1 || gamificationStore.leaderboardLoading"
                type="button"
                @click="changeLeaderboardPage(gamificationStore.leaderboardPage - 1)"
              >
                sebelumnya
              </button>
              <button
                class="rounded-xl bg-primary-600 px-4 py-2 text-sm font-bold text-white transition hover:bg-primary-700 disabled:cursor-not-allowed disabled:bg-gray-300"
                :disabled="gamificationStore.leaderboardPage >= gamificationStore.leaderboardTotalPages || gamificationStore.leaderboardLoading"
                type="button"
                @click="changeLeaderboardPage(gamificationStore.leaderboardPage + 1)"
              >
                berikutnya
              </button>
            </div>
          </div>
        </section>

        <section class="rounded-2xl border border-gray-100 bg-white p-5 shadow-card dark:border-gray-700 dark:bg-gray-800">
          <h2 class="text-base font-bold text-gray-900 dark:text-white">toko tema</h2>
          <p class="mb-4 mt-1 text-xs text-gray-500">tema yang sudah dibeli bisa dipakai lewat pengaturan.</p>
          <div class="space-y-3">
            <article
              v-for="reward in gamificationStore.rewards"
              :key="reward.id"
              class="rounded-xl border p-3 transition"
              :class="isRedeemed(reward.id)
                ? 'border-primary-300 bg-primary-50/80 shadow-sm dark:border-primary-700 dark:bg-primary-900/20'
                : 'border-gray-100 dark:border-gray-700'"
            >
              <div class="flex items-start justify-between gap-3">
                <div class="flex min-w-0 gap-3">
                  <span class="relative mt-0.5 h-10 w-10 flex-shrink-0 rounded-xl border border-white shadow-sm" :class="themeSwatchClass(reward.id)">
                    <span
                      v-if="isRedeemed(reward.id)"
                      class="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center rounded-full bg-primary-600 text-[11px] font-black text-white shadow-sm"
                    >
                      ✓
                    </span>
                  </span>
                  <div class="min-w-0">
                    <p class="text-sm font-bold text-gray-900 dark:text-white">{{ reward.title }}</p>
                    <p class="mt-1 text-xs leading-relaxed text-gray-500">{{ reward.description }}</p>
                  </div>
                </div>
                <span
                  class="rounded-lg px-2 py-1 text-xs font-black"
                  :class="isRedeemed(reward.id)
                    ? 'bg-primary-600 text-white'
                    : 'bg-warning-50 text-warning-700'"
                >
                  {{ isRedeemed(reward.id) ? 'dimiliki' : `${reward.cost} pts` }}
                </span>
              </div>
              <div
                v-if="isRedeemed(reward.id)"
                class="mt-3 rounded-xl border border-primary-200 bg-white/70 px-3 py-2 text-xs font-semibold text-primary-700 dark:border-primary-700 dark:bg-gray-900/30 dark:text-primary-300"
              >
                tema ini sudah kebeli, aktifinnya lewat pengaturan
              </div>
              <button
                v-else
                class="mt-3 w-full rounded-xl px-3 py-2 text-sm font-bold transition"
                :class="profile.rewardPoints >= reward.cost
                  ? 'bg-primary-600 text-white hover:bg-primary-700'
                  : 'bg-gray-100 text-gray-400 dark:bg-gray-700 dark:text-gray-500'"
                :disabled="profile.rewardPoints < reward.cost || gamificationStore.loading"
                @click="handleThemeAction(reward)"
              >
                beli tema
              </button>
            </article>
          </div>
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

const gamificationStore = useGamificationStore()
const userStore = useUserStore()
const profile = computed(() => userStore.profile)

function isRedeemed(rewardId) {
  return gamificationStore.redeemedRewardIdSet.has(rewardId)
}

function themeSwatchClass(themeId) {
  const classes = {
    'theme-forest': 'bg-emerald-500',
    'theme-ocean': 'bg-cyan-600',
    'theme-violet': 'bg-pink-500',
  }
  return classes[themeId] || 'bg-gray-300'
}

async function handleThemeAction(reward) {
  if (isRedeemed(reward.id)) {
    return
  }
  await gamificationStore.redeem(reward.id)
}

function changeLeaderboardPage(page) {
  gamificationStore.fetchLeaderboard(page)
}

onMounted(() => {
  gamificationStore.fetchAll()
})
</script>
