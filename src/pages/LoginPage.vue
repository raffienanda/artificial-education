<template>
  <main class="min-h-screen bg-surface-50 px-4 py-10 text-gray-800 dark:bg-gray-900 dark:text-gray-100">
    <div class="mx-auto flex min-h-[calc(100vh-5rem)] max-w-5xl items-center">
      <section class="grid w-full gap-8 lg:grid-cols-[1fr_420px]">
        <div class="hidden flex-col justify-center lg:flex">
          <p class="mb-3 text-sm font-bold uppercase tracking-wide text-primary-600">Artificial Education</p>
          <h1 class="max-w-xl text-4xl font-black leading-tight text-gray-950 dark:text-white">
            Learning path adaptif berbasis GKT dan Q-learning.
          </h1>
          <p class="mt-4 max-w-xl text-base leading-relaxed text-gray-500 dark:text-gray-400">
            Masuk untuk menyimpan progress, reward, Q-value, dan rekomendasi belajar personal.
          </p>
        </div>

        <div class="rounded-2xl border border-gray-100 bg-white p-6 shadow-card dark:border-gray-700 dark:bg-gray-800">
          <div class="mb-6">
            <h2 class="text-2xl font-black text-gray-950 dark:text-white">
              {{ isRegisterMode ? 'Buat akun' : 'Masuk' }}
            </h2>
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
              {{ isRegisterMode ? 'Mulai progress belajar baru.' : 'Lanjutkan sesi belajar kamu.' }}
            </p>
          </div>

          <form class="space-y-4" @submit.prevent="submit">
            <label v-if="isRegisterMode" class="block">
              <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">Nama tampilan</span>
              <input
                v-model="displayName"
                class="mt-1 w-full rounded-xl border border-gray-200 bg-white px-4 py-3 text-sm outline-none transition focus:border-primary-500 dark:border-gray-700 dark:bg-gray-900"
                placeholder="Nama kamu"
              >
            </label>

            <label class="block">
              <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">Username</span>
              <input
                v-model="username"
                class="mt-1 w-full rounded-xl border border-gray-200 bg-white px-4 py-3 text-sm outline-none transition focus:border-primary-500 dark:border-gray-700 dark:bg-gray-900"
                placeholder="student_cs"
                autocomplete="username"
              >
            </label>

            <label class="block">
              <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">Password</span>
              <input
                v-model="password"
                type="password"
                class="mt-1 w-full rounded-xl border border-gray-200 bg-white px-4 py-3 text-sm outline-none transition focus:border-primary-500 dark:border-gray-700 dark:bg-gray-900"
                placeholder="Minimal 6 karakter"
                autocomplete="current-password"
              >
            </label>

            <p v-if="userStore.authError" class="rounded-xl bg-danger-50 px-3 py-2 text-sm font-medium text-danger-600">
              {{ userStore.authError }}
            </p>

            <button
              class="w-full rounded-xl bg-primary-600 px-4 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-primary-700 disabled:cursor-not-allowed disabled:opacity-60"
              :disabled="userStore.authLoading"
            >
              {{ userStore.authLoading ? 'Memproses...' : isRegisterMode ? 'Daftar' : 'Masuk' }}
            </button>
          </form>

          <button
            class="mt-4 w-full text-center text-sm font-semibold text-primary-600 hover:text-primary-700"
            @click="isRegisterMode = !isRegisterMode"
          >
            {{ isRegisterMode ? 'Sudah punya akun? Masuk' : 'Belum punya akun? Daftar' }}
          </button>

          <div class="mt-5 rounded-xl bg-gray-50 p-3 text-xs text-gray-500 dark:bg-gray-900/60 dark:text-gray-400">
            Akun demo: <span class="font-bold">student_cs</span> / <span class="font-bold">password123</span>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useModulesStore } from '@/stores/modules'
import { useQuizStore } from '@/stores/quiz'

const router = useRouter()
const userStore = useUserStore()
const modulesStore = useModulesStore()
const quizStore = useQuizStore()

const isRegisterMode = ref(false)
const displayName = ref('')
const username = ref('student_cs')
const password = ref('password123')

async function submit() {
  const ok = isRegisterMode.value
    ? await userStore.register({
      username: username.value,
      password: password.value,
      displayName: displayName.value,
    })
    : await userStore.login({
      username: username.value,
      password: password.value,
    })

  if (ok) {
    modulesStore.clearActiveModule()
    quizStore.resetQuiz()
    router.push('/')
  }
}
</script>
