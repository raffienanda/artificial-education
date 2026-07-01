<template>
  <div class="flex flex-col h-full">
    <!-- Header: Pilihan Materi Modul -->
    <div class="p-5 pb-3">
      <h1 class="text-lg font-bold text-gray-900 dark:text-white">Pilihan Materi Modul</h1>
      <!-- Course Dropdown -->
      <button class="mt-2 w-full flex items-center justify-between px-3 py-2 bg-gray-50 dark:bg-gray-700 rounded-xl text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
        <span>Matematika SMP Kelas 7</span>
        <svg class="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
      </button>
    </div>

    <!-- Module Roadmap List -->
    <nav class="flex-1 overflow-y-auto px-4 py-2 scrollbar-hide">
      <div class="relative">
        <SidebarItem
          v-for="(mod, index) in modules"
          :key="mod.id"
          :module="mod"
          :number="index + 1"
          :is-active="activeModule?.id === mod.id"
          :is-last="index === modules.length - 1"
          :collapsed="false"
          @click="selectModule(mod)"
        />
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
    <div class="hidden xl:block p-3 border-t border-gray-100 dark:border-gray-700">
      <button
        class="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
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
import { computed } from 'vue'
import { useModulesStore } from '@/stores/modules'
import { useUiStore } from '@/stores/ui'
import SidebarItem from './SidebarItem.vue'
import { onMounted } from 'vue'

const props = defineProps({
  collapsed: { type: Boolean, default: false },
  showClose: { type: Boolean, default: false },
})

defineEmits(['close'])

const modulesStore = useModulesStore()
const uiStore = useUiStore()

const modules = computed(() => modulesStore.modules)
const activeModule = computed(() => modulesStore.activeModule)

onMounted(() => {
  if (modulesStore.modules.length === 0) {
    modulesStore.fetchModules()
  }
})

function selectModule(mod) {
  if (mod.status !== 'locked') {
    modulesStore.fetchModuleById(mod.id)
  }
}
</script>
