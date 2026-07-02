<template>
  <div class="flex flex-col h-full">
    <!-- Header: Pilihan Materi Modul -->
    <div class="relative p-5 pb-3">
      <h1 class="text-lg font-bold text-gray-900 dark:text-white">Pilih Mata Kuliah</h1>
      <button
        class="mt-2 flex w-full items-center justify-between rounded-xl bg-gray-50 px-3 py-2 text-sm text-gray-700 transition-colors hover:bg-gray-100 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600"
        type="button"
        @click="isCourseDropdownOpen = !isCourseDropdownOpen"
      >
        <span class="truncate pr-2">{{ selectedCourse.title }}</span>
        <svg
          :class="['h-4 w-4 flex-shrink-0 text-gray-400 transition-transform', isCourseDropdownOpen ? 'rotate-180' : '']"
          fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      <div
        v-if="isCourseDropdownOpen"
        class="absolute left-5 right-5 top-[82px] z-30 overflow-hidden rounded-xl border border-gray-100 bg-white shadow-elevated dark:border-gray-700 dark:bg-gray-800"
      >
        <button
          v-for="courseItem in courseOptions"
          :key="courseItem.id"
          type="button"
          class="flex w-full items-center justify-between gap-3 bg-primary-50 px-3 py-2 text-left text-sm font-bold text-primary-700 transition-colors hover:bg-primary-100 dark:bg-primary-900/20 dark:text-primary-300 dark:hover:bg-primary-900/30"
          @click="selectCourse(courseItem)"
        >
          <span class="truncate">{{ courseItem.title }}</span>
          <span class="text-xs font-semibold text-primary-500">aktif</span>
        </button>
      </div>
    </div>

    <!-- Module Roadmap List -->
    <nav class="flex-1 overflow-y-auto px-4 py-2 scrollbar-hide">
      <div class="relative">
        <div v-for="(mod, index) in modules" :key="mod.id">
          <SidebarItem
            :module="mod"
            :number="index + 1"
            :is-active="activeModule?.id === mod.id"
            :is-expanded="isExpanded(mod)"
            :is-last="index === modules.length - 1 && !isExpanded(mod)"
            :collapsed="false"
            @click="toggleModule(mod)"
          />

          <Transition name="subtopic-list">
            <div
              v-if="isExpanded(mod)"
              class="mb-2 ml-[18px] border-l-2 border-gray-100 pb-1 pl-5 dark:border-gray-700"
            >
              <button
                v-for="(subtopic, subtopicIndex) in mod.subtopics || []"
                :key="subtopic.id"
                type="button"
                class="mb-1 flex w-full items-start gap-2 rounded-lg px-2 py-2 text-left text-xs transition-colors"
                :class="activeSubtopic?.id === subtopic.id
                  ? 'bg-primary-50 font-bold text-primary-700 dark:bg-primary-900/20 dark:text-primary-300'
                  : 'text-gray-500 hover:bg-gray-50 hover:text-gray-800 dark:text-gray-400 dark:hover:bg-gray-700/50 dark:hover:text-gray-200'"
                @click="selectSubtopic(mod, subtopic)"
              >
                <span class="mt-0.5 flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full bg-gray-100 text-[10px] font-black text-gray-500 dark:bg-gray-700 dark:text-gray-300">
                  {{ subtopicIndex + 1 }}
                </span>
                <span class="min-w-0 flex-1 leading-snug">{{ subtopic.title }}</span>
              </button>
            </div>
          </Transition>
        </div>
      </div>
    </nav>

    <!-- Bottom: Tujuan Belajar -->
    <div class="p-4 border-t border-gray-100 dark:border-gray-700">
      <div class="bg-gray-50 dark:bg-gray-700/50 rounded-2xl p-4">
        <div class="flex items-center gap-2.5 mb-2">
          <div class="w-8 h-8 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
            <svg class="w-4 h-4 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 3v1.5M3 21v-6m0 0l2.77-.693a9 9 0 016.208.682l.108.054a9 9 0 006.086.71l3.114-.732a48.524 48.524 0 01-.005-10.499l-3.11.732a9 9 0 01-6.085-.711l-.108-.054a9 9 0 00-6.208-.682L3 4.5M3 15V4.5" />
            </svg>
          </div>
          <h3 class="text-sm font-bold text-gray-800 dark:text-gray-100">Tujuan Belajar</h3>
        </div>
        <p class="text-xs text-gray-500 dark:text-gray-400 leading-relaxed mb-3">
          Kuasai semua materi dengan level minimal 80%
        </p>
        <div class="flex items-center gap-2">
          <div class="flex-1 progress-bar h-2 bg-gray-200 dark:bg-gray-600">
            <div class="progress-bar-fill bg-primary-500" style="width: 35%" />
          </div>
          <span class="text-xs font-bold text-gray-600 dark:text-gray-300">35%</span>
        </div>
      </div>
    </div>

    <!-- Collapse toggle (desktop only) — hidden on mobile -->
    <div class="p-3 border-t border-gray-100 dark:border-gray-700">
      <button
        class="mb-2 flex w-full items-center gap-3 rounded-xl px-3 py-2 text-primary-600 transition-colors hover:bg-primary-50 dark:text-primary-300 dark:hover:bg-primary-900/20"
        @click="goToInitialDashboard"
      >
        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l9-9 9 9M5 10v10a1 1 0 001 1h4v-6h4v6h4a1 1 0 001-1V10" />
        </svg>
        <span class="text-sm font-bold">Dashboard Awal</span>
      </button>

      <button
        class="hidden w-full items-center gap-3 rounded-xl px-3 py-2 text-gray-500 transition-colors hover:bg-gray-100 dark:hover:bg-gray-700 xl:flex"
        @click="uiStore.toggleSidebar()"
      >
        <svg
          :class="['w-5 h-5 transition-transform duration-300', collapsed ? 'rotate-180' : '']"
          fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
        </svg>
        <span v-if="!collapsed" class="text-sm">Tutup</span>
      </button>
    </div>

    <!-- Close button (mobile only) -->
    <button
      v-if="showClose"
      class="absolute top-4 right-4 xl:hidden text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
      @click="$emit('close')"
    >
      <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </button>
  </div>
</template>

<script setup>
/**
 * SidebarContent — Numbered module roadmap matching reference design
 */
import { computed, ref, watch } from 'vue'
import { useModulesStore } from '@/stores/modules'
import { useUiStore } from '@/stores/ui'
import { useQuizStore } from '@/stores/quiz'
import SidebarItem from './SidebarItem.vue'
import { onMounted } from 'vue'

const props = defineProps({
  collapsed: { type: Boolean, default: false },
  showClose: { type: Boolean, default: false },
})

const emit = defineEmits(['close'])

const modulesStore = useModulesStore()
const uiStore = useUiStore()
const quizStore = useQuizStore()
const isCourseDropdownOpen = ref(false)

const modules = computed(() => modulesStore.modules)
const activeModule = computed(() => modulesStore.activeModule)
const activeSubtopic = computed(() => modulesStore.activeSubtopic)
const courseOptions = computed(() => (modulesStore.course ? [modulesStore.course] : []))
const selectedCourse = computed(() => modulesStore.course || {
  id: 'loading-course',
  title: 'Memuat mata kuliah...',
  description: '',
  icon: '',
})
const expandedModuleIds = ref(new Set())

onMounted(() => {
  if (!modulesStore.course) {
    modulesStore.fetchCourse()
  }
  if (modulesStore.modules.length === 0) {
    modulesStore.fetchModules()
  }
})

function isExpanded(mod) {
  return expandedModuleIds.value.has(mod.id)
}

async function toggleModule(mod) {
  if (mod.status === 'locked') return

  const next = new Set(expandedModuleIds.value)
  if (next.has(mod.id)) {
    next.delete(mod.id)
  } else {
    next.add(mod.id)
  }
  expandedModuleIds.value = next

  if (activeModule.value?.id !== mod.id) {
    await modulesStore.fetchModuleById(mod.id)
  }
}

async function selectSubtopic(mod, subtopic) {
  if (mod.status === 'locked') return
  await modulesStore.goToModuleSubtopic(mod.id, subtopic.id)
}

function selectCourse(courseItem) {
  isCourseDropdownOpen.value = false
}

function goToInitialDashboard() {
  modulesStore.clearActiveModule()
  quizStore.resetQuiz()
  expandedModuleIds.value = new Set()
  isCourseDropdownOpen.value = false
  if (props.showClose) {
    emit('close')
  }
}

watch(
  () => activeModule.value?.id,
  (moduleId) => {
    if (!moduleId) return
    const next = new Set(expandedModuleIds.value)
    next.add(moduleId)
    expandedModuleIds.value = next
  },
  { immediate: true }
)
</script>

<style scoped>
.subtopic-list-enter-active,
.subtopic-list-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
}
.subtopic-list-enter-from,
.subtopic-list-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
