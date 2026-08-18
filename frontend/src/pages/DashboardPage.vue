<template>
  <div class="h-full w-full overflow-y-auto bg-slate-50/80 p-3 dark:bg-gray-950 sm:p-5 lg:p-6">
    <template v-if="!modulesStore.activeModule && !courseSelected">
      <section class="mx-auto flex min-h-full max-w-6xl flex-col justify-center gap-6 py-6">
        <div class="max-w-3xl">
          <p class="text-sm font-bold text-primary-600 dark:text-primary-300">Learning path adaptif</p>
          <h1 class="mt-2 text-3xl font-black tracking-normal text-gray-950 dark:text-white sm:text-4xl">
            Pilih mata kuliah dulu
          </h1>
          <p class="mt-3 max-w-2xl text-sm leading-relaxed text-gray-500 dark:text-gray-400">
            setelah mata kuliah dipilih, sistem akan menampilkan modul, prasyarat, pre test, quiz subtopik, post test, dan rekomendasi belajar yang sesuai.
          </p>
        </div>

        <div class="grid gap-4 lg:grid-cols-[minmax(0,1fr)_320px]">
          <div
            v-if="modulesStore.loading && courseOptions.length === 1 && courseOptions[0].id === 'loading-course'"
            class="flex min-h-[220px] items-center justify-center rounded-2xl border border-gray-100 bg-white p-8 text-sm font-semibold text-gray-500 shadow-sm dark:border-gray-800 dark:bg-gray-900 dark:text-gray-300"
          >
            <LoadingSpinner class="mr-2 text-primary-600" />
            Memuat mata kuliah...
          </div>
          <div v-else class="grid max-h-[min(560px,calc(100vh-280px))] gap-4 overflow-y-auto pr-1">
            <button
              v-for="course in courseOptions"
              :key="course.id"
              class="group grid w-full gap-4 rounded-2xl border border-gray-100 bg-white p-5 text-left shadow-sm transition hover:-translate-y-0.5 hover:border-primary-200 hover:shadow-card dark:border-gray-800 dark:bg-gray-900 dark:hover:border-primary-800 sm:grid-cols-[56px_minmax(0,1fr)_auto]"
              type="button"
              @click="selectCourse(course)"
            >
              <span class="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary-100 text-primary-700 dark:bg-primary-900/40 dark:text-primary-300">
                <GraduationCap class="h-7 w-7" />
              </span>
              <span class="min-w-0">
                <span class="block text-lg font-black text-gray-950 dark:text-white">{{ course.title }}</span>
                <span class="mt-1 block text-sm leading-relaxed text-gray-500 dark:text-gray-400">
                  {{ course.description || 'Mata kuliah ini berisi modul adaptif dengan pre test, quiz subtopik, post test, q-learning, dan neural gkt.' }}
                </span>
                <span class="mt-4 flex flex-wrap gap-2">
                  <span class="rounded-lg bg-gray-100 px-2.5 py-1 text-xs font-bold text-gray-600 dark:bg-gray-800 dark:text-gray-300">
                  {{ course.module_count || 0 }} modul
                  </span>
                  <span class="rounded-lg bg-primary-50 px-2.5 py-1 text-xs font-bold text-primary-700 dark:bg-primary-950/40 dark:text-primary-300">
                    Adaptive learning
                  </span>
                </span>
              </span>
              <span class="inline-flex items-center gap-1 self-center rounded-xl bg-gray-950 px-4 py-2.5 text-sm font-black text-white transition group-hover:bg-primary-600 dark:bg-white dark:text-gray-950 dark:group-hover:bg-primary-200">
                Pilih
                <ArrowRight class="h-4 w-4" />
              </span>
            </button>
          </div>

          <aside class="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900">
            <p class="text-sm font-black text-gray-950 dark:text-white">Alur setelah memilih</p>
            <div class="mt-4 space-y-4">
              <div
                v-for="(step, index) in courseFlowSteps"
                :key="step"
                class="flex gap-3"
              >
                <span class="flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg bg-gray-100 text-xs font-black text-gray-600 dark:bg-gray-800 dark:text-gray-300">
                  {{ index + 1 }}
                </span>
                <p class="pt-1 text-sm leading-relaxed text-gray-500 dark:text-gray-400">{{ step }}</p>
              </div>
            </div>
          </aside>
        </div>
      </section>
    </template>

    <template v-else-if="!modulesStore.activeModule">
      <section class="mx-auto flex min-h-0 max-w-7xl flex-col gap-5 lg:h-full">
        <div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <p class="text-sm font-bold text-primary-600 dark:text-primary-300">{{ courseTitle }}</p>
            <h1 class="mt-1 text-2xl font-black tracking-normal text-gray-950 dark:text-white sm:text-3xl">
              Dashboard belajar
            </h1>
            <p class="mt-2 max-w-2xl text-sm leading-relaxed text-gray-500 dark:text-gray-400">
              pilih modul dari learning path, cek progres, atau buka menu pendukung tanpa harus masuk lewat sidebar.
            </p>
          </div>

          <div class="flex flex-wrap gap-2">
            <button
              class="inline-flex items-center gap-2 rounded-xl border border-gray-200 bg-white px-4 py-2.5 text-sm font-bold text-gray-700 shadow-sm transition hover:border-gray-300 hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-200 dark:hover:bg-gray-800"
              type="button"
              @click="changeCourse"
            >
              <GraduationCap class="h-4 w-4" />
              Ganti Mata Kuliah
            </button>
            <button
              class="inline-flex items-center gap-2 rounded-xl border border-gray-200 bg-white px-4 py-2.5 text-sm font-bold text-gray-700 shadow-sm transition hover:border-gray-300 hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-200 dark:hover:bg-gray-800"
              :disabled="dashboardRefreshing"
              type="button"
              @click="refreshDashboard"
            >
              <LoadingSpinner v-if="dashboardRefreshing" size="sm" />
              <RefreshCw v-else class="h-4 w-4" />
              {{ dashboardRefreshing ? 'Memuat...' : 'Refresh' }}
            </button>
            <button
              class="inline-flex items-center gap-2 rounded-xl bg-primary-600 px-4 py-2.5 text-sm font-black text-white shadow-sm transition hover:bg-primary-700 disabled:cursor-not-allowed disabled:bg-gray-300"
              :disabled="!nextModule"
              type="button"
              @click="openModule(nextModule)"
            >
              <PlayCircle class="h-4 w-4" />
              {{ nextModule ? moduleActionLabel(nextModule) : 'Tidak ada modul' }}
            </button>
          </div>
        </div>

        <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
          <div class="rounded-xl border border-gray-100 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900">
            <p class="text-xs font-bold text-gray-500 dark:text-gray-400">Rata-rata penguasaan</p>
            <div class="mt-3 flex items-end justify-between gap-3">
              <p class="text-3xl font-black text-gray-950 dark:text-white">{{ progressStore.overallMastery }}%</p>
              <BarChart3 class="h-6 w-6 text-primary-500" />
            </div>
          </div>
          <div class="rounded-xl border border-gray-100 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900">
            <p class="text-xs font-bold text-gray-500 dark:text-gray-400">Level mahasiswa</p>
            <div class="mt-3 flex items-end justify-between gap-3">
              <p class="text-3xl font-black text-gray-950 dark:text-white">{{ userStore.profile.level }}</p>
              <Trophy class="h-6 w-6 text-amber-500" />
            </div>
          </div>
          <div class="rounded-xl border border-gray-100 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900">
            <p class="text-xs font-bold text-gray-500 dark:text-gray-400">Streak belajar</p>
            <div class="mt-3 flex items-end justify-between gap-3">
              <p class="text-3xl font-black text-gray-950 dark:text-white">{{ userStore.profile.currentStreak }}</p>
              <CalendarDays class="h-6 w-6 text-emerald-500" />
            </div>
          </div>
          <div class="rounded-xl border border-gray-100 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900">
            <p class="text-xs font-bold text-gray-500 dark:text-gray-400">Profil kognitif</p>
            <div class="mt-3 flex items-end justify-between gap-3">
              <p class="text-base font-black" :class="cognitiveStore.completed ? 'text-emerald-600 dark:text-emerald-300' : 'text-amber-600 dark:text-amber-300'">
                {{ cognitiveStore.completed ? 'Sudah diisi' : 'Belum diisi' }}
              </p>
              <Brain class="h-6 w-6 text-violet-500" />
            </div>
          </div>
        </div>

        <div
          v-if="!cognitiveStore.completed"
          class="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 dark:border-amber-900/50 dark:bg-amber-950/30"
        >
          <div>
            <p class="text-sm font-black text-gray-950 dark:text-white">Profil kognitif belum diisi</p>
            <p class="mt-0.5 text-xs text-gray-600 dark:text-gray-300">
              instrumen ini dipakai sebagai konteks awal rekomendasi belajar.
            </p>
          </div>
          <RouterLink
            class="inline-flex items-center gap-2 rounded-lg bg-amber-600 px-3.5 py-2 text-xs font-black text-white transition hover:bg-amber-700"
            to="/cognitive-profile"
          >
            Isi Profil
            <ArrowRight class="h-4 w-4" />
          </RouterLink>
        </div>

        <div class="grid min-h-0 flex-1 gap-5 lg:grid-cols-[minmax(0,1fr)_340px]">
          <section class="min-h-0 overflow-hidden rounded-xl border border-gray-100 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-900">
            <div class="flex items-center justify-between gap-3 border-b border-gray-100 px-5 py-4 dark:border-gray-800">
              <div>
                <h2 class="text-base font-black text-gray-950 dark:text-white">Learning path modul</h2>
                <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
                  modul terkunci akan terbuka setelah prasyarat dan evaluasi sebelumnya terpenuhi.
                </p>
              </div>
              <span class="hidden rounded-lg bg-gray-100 px-3 py-1 text-xs font-bold text-gray-500 dark:bg-gray-800 dark:text-gray-300 sm:inline-flex">
                {{ completedModuleCount }}/{{ modulesStore.modules.length }} selesai
              </span>
            </div>

            <div class="max-h-[calc(100vh-360px)] min-h-[320px] overflow-y-auto p-4 sm:p-5">
              <div v-if="modulesStore.loading" class="flex min-h-[280px] flex-col items-center justify-center rounded-xl border border-dashed border-gray-200 bg-gray-50 p-6 text-center dark:border-gray-700 dark:bg-gray-950/40">
                <LoadingSpinner size="lg" class="text-primary-600 dark:text-primary-300" />
                <h3 class="mt-4 text-sm font-black text-gray-950 dark:text-white">Memuat modul...</h3>
                <p class="mt-1 max-w-sm text-xs leading-relaxed text-gray-500 dark:text-gray-400">
                  sistem sedang mengambil data learning path dari server.
                </p>
              </div>
              <div v-else-if="modulesStore.modules.length === 0" class="flex min-h-[280px] flex-col items-center justify-center rounded-xl border border-dashed border-gray-200 bg-gray-50 p-6 text-center dark:border-gray-700 dark:bg-gray-950/40">
                <GraduationCap class="h-10 w-10 text-gray-300 dark:text-gray-600" />
                <h3 class="mt-3 text-sm font-black text-gray-950 dark:text-white">Modul belum tersedia</h3>
                <p class="mt-1 max-w-sm text-xs leading-relaxed text-gray-500 dark:text-gray-400">
                  mata kuliah ini sudah masuk daftar, tapi materi dan assessment-nya belum disusun.
                </p>
              </div>
              <div v-else class="space-y-3">
                <button
                  v-for="(mod, index) in modulesStore.modules"
                  :key="mod.id"
                  class="group grid w-full grid-cols-[44px_minmax(0,1fr)_auto] items-center gap-4 rounded-xl border p-4 text-left transition"
                  :class="moduleCardClass(mod)"
                  :disabled="mod.status === 'locked'"
                  type="button"
                  @click="openModule(mod)"
                >
                  <span class="relative flex h-11 w-11 items-center justify-center rounded-xl text-sm font-black" :class="moduleNumberClass(mod)">
                    <CheckCircle2 v-if="moduleCompleted(mod)" class="h-5 w-5" />
                    <Lock v-else-if="mod.status === 'locked'" class="h-5 w-5" />
                    <span v-else>{{ index + 1 }}</span>
                  </span>

                  <span class="min-w-0">
                    <span class="flex flex-wrap items-center gap-2">
                      <span class="text-sm font-black text-gray-950 dark:text-white">{{ mod.title }}</span>
                      <span class="rounded-md px-2 py-0.5 text-[11px] font-bold" :class="modulePillClass(mod)">
                        {{ moduleStatusLabel(mod) }}
                      </span>
                    </span>
                    <span class="mt-1 block text-xs text-gray-500 dark:text-gray-400">
                      {{ mod.subtopics?.length || 0 }} materi belajar
                    </span>
                    <span class="mt-3 block h-2 overflow-hidden rounded-full bg-gray-100 dark:bg-gray-800">
                      <span class="block h-full rounded-full transition-all" :class="moduleProgressColor(mod)" :style="{ width: moduleProgress(mod) + '%' }" />
                    </span>
                  </span>

                  <span class="hidden items-center gap-1 text-xs font-black text-primary-600 dark:text-primary-300 sm:inline-flex" :class="mod.status === 'locked' ? 'text-gray-400 dark:text-gray-600' : ''">
                    {{ moduleActionLabel(mod) }}
                    <ArrowRight v-if="mod.status !== 'locked'" class="h-4 w-4 transition group-hover:translate-x-0.5" />
                  </span>
                </button>
              </div>
            </div>
          </section>

          <aside class="grid content-start gap-4">
            <div class="rounded-xl border border-gray-100 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900">
              <p class="text-xs font-bold text-gray-500 dark:text-gray-400">Langkah berikutnya</p>
              <h3 class="mt-2 text-lg font-black text-gray-950 dark:text-white">{{ nextStepTitle }}</h3>
              <p class="mt-2 text-sm leading-relaxed text-gray-500 dark:text-gray-400">{{ nextStepDescription }}</p>
              <button
                class="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-xl bg-gray-950 px-4 py-2.5 text-sm font-black text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:bg-gray-300 dark:bg-white dark:text-gray-950 dark:hover:bg-gray-100"
                :disabled="!nextModule"
                type="button"
                @click="openModule(nextModule)"
              >
                Buka langkah ini
                <ArrowRight class="h-4 w-4" />
              </button>
            </div>

            <div class="grid gap-3">
              <RouterLink
                v-for="item in menuItems"
                :key="item.to"
                class="flex items-center gap-3 rounded-xl border border-gray-100 bg-white p-4 shadow-sm transition hover:border-primary-200 hover:bg-primary-50/40 dark:border-gray-800 dark:bg-gray-900 dark:hover:border-primary-800 dark:hover:bg-primary-950/20"
                :to="item.to"
              >
                <span class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-200">
                  <component :is="item.icon" class="h-5 w-5" />
                </span>
                <span class="min-w-0 flex-1">
                  <span class="block text-sm font-black text-gray-950 dark:text-white">{{ item.title }}</span>
                  <span class="mt-0.5 block text-xs leading-relaxed text-gray-500 dark:text-gray-400">{{ item.description }}</span>
                </span>
              </RouterLink>
            </div>
          </aside>
        </div>
      </section>
    </template>

    <template v-else>
      <div
        v-if="!cognitiveStore.completed"
        class="mb-4 flex flex-wrap items-center justify-between gap-3 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 dark:border-amber-900/50 dark:bg-amber-950/30"
      >
        <div>
          <p class="text-sm font-black text-gray-950 dark:text-white">Profil kognitif belum diisi</p>
          <p class="mt-0.5 text-xs text-gray-600 dark:text-gray-300">
            sistem akan memakai hasilnya untuk menyesuaikan rekomendasi belajar.
          </p>
        </div>
        <RouterLink
          class="rounded-lg bg-amber-600 px-3.5 py-2 text-xs font-black text-white transition hover:bg-amber-700"
          to="/cognitive-profile"
        >
          Isi Sekarang
        </RouterLink>
      </div>

      <div
        class="relative grid min-h-0 w-full gap-4 lg:h-full lg:gap-5"
        :class="[
          'grid-cols-1 lg:grid-cols-[1fr_320px] xl:grid-cols-[1fr_360px]',
          uiStore.progressPanelVisible
            ? 'grid-rows-auto lg:grid-rows-[minmax(0,1fr)_340px]'
            : 'grid-rows-auto lg:grid-rows-[minmax(0,1fr)_56px]',
        ]"
      >
        <BaseCard class="min-h-0 flex flex-col overflow-hidden lg:col-start-1 lg:row-start-1" :padding="false">
          <div class="flex h-full min-h-0 flex-col overflow-hidden p-4 sm:p-5 lg:p-6">
            <ModuleViewer />
          </div>
        </BaseCard>

        <BaseCard
          class="min-h-0 flex flex-col overflow-hidden transition-all duration-300 lg:col-start-1 lg:row-start-2"
          :padding="false"
        >
          <div v-if="uiStore.progressPanelVisible" class="flex h-full flex-col overflow-y-auto p-4 scrollbar-hide sm:p-5">
            <ProgressPanel />
          </div>
          <button
            v-else
            class="flex h-full w-full items-center justify-between gap-3 px-4 text-left text-primary-600 transition-colors hover:bg-primary-50 dark:text-primary-300 dark:hover:bg-primary-900/20"
            title="Tampilkan progress modul"
            type="button"
            @click="uiStore.toggleProgressPanel()"
          >
            <span class="flex items-center gap-2">
              <BarChart3 class="h-5 w-5" />
              <span class="text-sm font-bold">Progress Modul</span>
            </span>
            <span class="text-xs font-semibold text-gray-400">Tampilkan</span>
          </button>
        </BaseCard>

        <div class="flex min-h-0 flex-col gap-4 lg:col-start-2 lg:row-span-2 lg:row-start-1">
          <BaseCard
            class="hidden min-h-0 flex-col overflow-hidden border-none transition-all duration-300 lg:flex"
            :class="uiStore.chatbotDesktopVisible ? 'flex-1' : 'h-14 flex-shrink-0'"
            :padding="false"
          >
            <ChatbotPanel v-if="uiStore.chatbotDesktopVisible" />
            <button
              v-else
              class="flex h-full w-full items-center justify-between gap-3 px-4 text-left text-primary-600 transition-colors hover:bg-primary-50 dark:text-primary-300 dark:hover:bg-primary-900/20"
              title="Tampilkan chatbot"
              type="button"
              @click="uiStore.toggleChatbotDesktop()"
            >
              <span class="flex items-center gap-2">
                <MessageCircle class="h-5 w-5" />
                <span class="text-sm font-bold">Chatbot AI</span>
              </span>
              <span class="text-xs font-semibold text-gray-400">Tampilkan</span>
            </button>
          </BaseCard>

          <BaseCard
            class="flex min-h-0 flex-col overflow-hidden"
            :class="uiStore.chatbotDesktopVisible ? 'lg:h-[340px] lg:flex-shrink-0' : 'lg:flex-1'"
            :padding="false"
          >
            <div class="flex h-full min-h-0 flex-col overflow-y-auto p-4 scrollbar-hide sm:p-5">
              <PracticePanel />
            </div>
          </BaseCard>
        </div>
      </div>

      <button
        class="fixed bottom-6 right-6 z-40 flex h-14 w-14 items-center justify-center rounded-full bg-primary-600 text-white shadow-elevated transition-transform hover:scale-105 lg:hidden"
        type="button"
        @click="uiStore.toggleChatbotMobile()"
      >
        <MessageCircle class="h-6 w-6" />
      </button>

      <Teleport to="body">
        <Transition name="slide-up">
          <div
            v-if="uiStore.chatbotMobileOpen"
            class="fixed inset-0 z-50 flex flex-col bg-white dark:bg-gray-900 lg:hidden"
          >
            <ChatbotPanel @close="uiStore.toggleChatbotMobile()" />
          </div>
        </Transition>
      </Teleport>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  ArrowRight,
  BarChart3,
  Brain,
  CalendarDays,
  CheckCircle2,
  GraduationCap,
  Lock,
  MessageCircle,
  PlayCircle,
  RefreshCw,
  Settings,
  Trophy,
  User,
} from 'lucide-vue-next'
import { useModulesStore } from '@/stores/modules'
import { useUiStore } from '@/stores/ui'
import { useProgressStore } from '@/stores/progress'
import { useChatbotStore } from '@/stores/chatbot'
import { useQuizStore } from '@/stores/quiz'
import { useCognitiveStore } from '@/stores/cognitive'
import { useUserStore } from '@/stores/user'

import BaseCard from '@/components/common/BaseCard.vue'
import ModuleViewer from '@/components/module/ModuleViewer.vue'
import ProgressPanel from '@/components/progress/ProgressPanel.vue'
import ChatbotPanel from '@/components/chatbot/ChatbotPanel.vue'
import PracticePanel from '@/components/drill/PracticePanel.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

const modulesStore = useModulesStore()
const uiStore = useUiStore()
const progressStore = useProgressStore()
const chatbotStore = useChatbotStore()
const quizStore = useQuizStore()
const cognitiveStore = useCognitiveStore()
const userStore = useUserStore()
const router = useRouter()
const courseSelected = ref(false)
const dashboardRefreshing = ref(false)

const courseTitle = computed(() => modulesStore.selectedCourse?.title || modulesStore.course?.title || 'Algoritma dan Pemrograman')
const courseOptions = computed(() => (
  modulesStore.courses.length > 0
    ? modulesStore.courses
    : modulesStore.course
      ? [modulesStore.course]
    : [{
        id: 'loading-course',
        title: 'Memuat mata kuliah...',
        description: 'Data mata kuliah sedang dimuat dari server.',
      }]
))
const completedModuleCount = computed(() => modulesStore.modules.filter((mod) => moduleCompleted(mod)).length)
const courseFlowSteps = [
  'pilih mata kuliah yang ingin dipelajari.',
  'pilih modul yang terbuka dari learning path.',
  'kerjakan pre test modul sebagai initial assessment.',
  'belajar subtopik, lalu kerjakan quiz subtopik untuk update q-value.',
  'selesaikan post test untuk melihat rapor dan rekomendasi akhir.',
]
const nextModule = computed(() => (
  modulesStore.modules.find((mod) => mod.status !== 'locked' && !moduleCompleted(mod)) ||
  modulesStore.modules.find((mod) => moduleCompleted(mod)) ||
  null
))
const nextStepTitle = computed(() => {
  if (!nextModule.value) return 'Belum ada modul aktif'
  if (!cognitiveStore.completed) return 'Lengkapi profil kognitif dulu'
  if (!quizStore.hasCompletedPretest(nextModule.value.id)) return `Mulai ${nextModule.value.title}`
  return `Lanjut ${nextModule.value.title}`
})
const nextStepDescription = computed(() => {
  if (!nextModule.value) return 'Data modul belum tersedia atau semua modul masih terkunci.'
  if (!cognitiveStore.completed) return 'profil kognitif membantu sistem membaca konteks belajar sebelum rekomendasi diberikan.'
  if (!quizStore.hasCompletedPretest(nextModule.value.id)) return 'kerjakan pre test modul untuk membuka materi dan membaca kemampuan awal.'
  return 'lanjutkan materi subtopik dan selesaikan quiz agar learning path bergerak.'
})
const menuItems = computed(() => {
  const items = [
    {
      to: '/cognitive-profile',
      title: 'Profil Kognitif',
      description: cognitiveStore.completed ? 'instrumen sudah dikunci.' : 'isi instrumen sebelum belajar.',
      icon: Brain,
    },
    {
      to: '/profile',
      title: 'Profil Mahasiswa',
      description: 'lihat akun, level, poin, dan progres.',
      icon: User,
    },
    {
      to: '/gamification',
      title: 'Leaderboard & Reward',
      description: 'cek peringkat dan penukaran poin.',
      icon: Trophy,
    },
  ]

  if (userStore.currentUser?.role === 'admin') {
    items.push({
      to: '/admin',
      title: 'Admin Pembelajaran',
      description: 'kelola graph, soal, dan materi.',
      icon: Settings,
    })
  }

  return items
})

function moduleStatusLabel(mod) {
  if (moduleCompleted(mod)) return 'selesai'
  if (mod.status === 'locked') return 'terkunci'
  if (quizStore.hasCompletedPretest(mod.id)) return 'sedang belajar'
  return 'belum mulai'
}

function moduleActionLabel(mod) {
  if (!mod) return 'Mulai'
  if (moduleCompleted(mod)) return 'Lihat rapor'
  if (mod.status === 'locked') return 'Terkunci'
  if (quizStore.hasCompletedPretest(mod.id)) return 'Lanjut belajar'
  return 'Mulai belajar'
}

function moduleProgress(mod) {
  if (moduleCompleted(mod)) return 100
  if (mod.status === 'locked') return 0
  if (quizStore.hasCompletedPretest(mod.id)) return 35
  return 8
}

function moduleCardClass(mod) {
  if (mod.status === 'locked') {
    return 'cursor-not-allowed border-gray-100 bg-gray-50 opacity-70 dark:border-gray-800 dark:bg-gray-950/50'
  }
  if (moduleCompleted(mod)) {
    return 'border-emerald-100 bg-emerald-50/50 hover:border-emerald-200 dark:border-emerald-900/40 dark:bg-emerald-950/20'
  }
  return 'border-gray-100 bg-white hover:border-primary-200 hover:bg-primary-50/50 dark:border-gray-800 dark:bg-gray-900 dark:hover:border-primary-800 dark:hover:bg-primary-950/20'
}

function moduleNumberClass(mod) {
  if (mod.status === 'locked') return 'bg-gray-100 text-gray-400 dark:bg-gray-800 dark:text-gray-500'
  if (moduleCompleted(mod)) return 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300'
  return 'bg-primary-100 text-primary-700 dark:bg-primary-900/40 dark:text-primary-300'
}

function modulePillClass(mod) {
  if (mod.status === 'locked') return 'bg-gray-100 text-gray-500 dark:bg-gray-800 dark:text-gray-400'
  if (moduleCompleted(mod)) return 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300'
  return 'bg-primary-100 text-primary-700 dark:bg-primary-900/40 dark:text-primary-300'
}

function moduleProgressColor(mod) {
  if (moduleCompleted(mod)) return 'bg-emerald-500'
  if (mod.status === 'locked') return 'bg-gray-200 dark:bg-gray-700'
  return 'bg-primary-500'
}

function moduleCompleted(mod) {
  return Boolean(mod?.id && mod.status === 'completed' && quizStore.hasPassedModule(mod.id))
}

async function openModule(mod) {
  if (!mod || mod.status === 'locked') return
  if (moduleCompleted(mod)) {
    router.push({ name: 'ModuleReport', params: { moduleId: mod.id } })
    return
  }
  await modulesStore.fetchModuleById(mod.id)
}

async function selectCourse(course) {
  if (!course || course.id === 'loading-course') return
  await modulesStore.selectCourse(course)
  courseSelected.value = true
}

function changeCourse() {
  modulesStore.clearActiveModule()
  courseSelected.value = false
}

async function refreshDashboard() {
  dashboardRefreshing.value = true
  try {
    await Promise.all([
      quizStore.fetchGateStatus(),
      modulesStore.fetchModules(),
      progressStore.fetchAll(),
      cognitiveStore.fetchProfile(),
    ])
  } finally {
    dashboardRefreshing.value = false
  }
}

onMounted(async () => {
  await Promise.all([
    modulesStore.fetchCourse(),
    modulesStore.fetchCourses(),
    progressStore.fetchAll(),
    chatbotStore.fetchConversation(),
    cognitiveStore.fetchProfile(),
  ])
  await Promise.all([
    quizStore.fetchGateStatus(),
    modulesStore.fetchModules(),
  ])
})

watch(
  () => userStore.currentUser?.id,
  () => {
    courseSelected.value = false
  }
)
</script>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
}
</style>
