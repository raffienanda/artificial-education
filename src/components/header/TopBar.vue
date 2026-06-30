<template>
  <header class="h-16 px-4 xl:px-6 bg-white dark:bg-gray-800 border-b border-gray-100 dark:border-gray-700 flex items-center justify-between sticky top-0 z-20">
    <!-- Left: Hamburger & Breadcrumb -->
    <div class="flex items-center gap-4">
      <button
        class="xl:hidden text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 focus:outline-none"
        @click="uiStore.toggleMobileSidebar()"
      >
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      <div class="hidden sm:block">
        <Breadcrumb :items="breadcrumbItems" />
      </div>
    </div>

    <!-- Center/Right: Search, Stats, Actions -->
    <div class="flex items-center gap-3 sm:gap-5">
      <!-- Search -->
      <div class="hidden md:block w-64">
        <SearchBar />
      </div>
      <button class="md:hidden text-gray-500" @click="uiStore.toggleSearchModal()">
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </button>

      <!-- Gamification Stats -->
      <div class="hidden lg:flex items-center gap-5 border-r border-gray-200 dark:border-gray-700 pr-5">
        <!-- Streak 🔥 -->
        <div 
          class="flex items-center gap-1.5 px-2 py-1 rounded-lg transition-all duration-300"
          :class="userStore.dailyGoalProgress >= 100 ? 'bg-warning-50 dark:bg-warning-900/20 shadow-[0_0_15px_rgba(245,158,11,0.2)]' : ''"
          title="Runtutan Belajar"
        >
          <span 
            class="text-lg transition-all duration-1000"
            :class="userStore.dailyGoalProgress >= 100 ? 'animate-pulse drop-shadow-[0_0_8px_rgba(245,158,11,0.8)]' : 'grayscale opacity-50'"
          >🔥</span>
          <span 
            class="text-sm font-black"
            :class="userStore.dailyGoalProgress >= 100 ? 'text-warning-600 dark:text-warning-400' : 'text-gray-400'"
          >{{ profile.currentStreak }}</span>
        </div>
        
        <!-- XP & Level Bar 🌟 -->
        <div class="flex items-center gap-2 group cursor-pointer" title="XP Progress">
          <div class="flex items-center justify-center w-7 h-7 rounded-full bg-gradient-to-br from-warning-400 to-warning-600 text-white font-black text-xs shadow-md border-2 border-white dark:border-gray-800 z-10">
            {{ profile.level }}
          </div>
          <div class="flex flex-col -ml-4 pl-5 bg-gray-50 dark:bg-gray-700/50 rounded-r-full pr-3 py-1 border border-gray-100 dark:border-gray-700">
            <div class="w-24 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden mb-0.5">
              <div 
                class="h-full bg-gradient-to-r from-warning-400 to-warning-500 transition-all duration-1000 ease-out"
                :style="{ width: userStore.xpProgress + '%' }"
              />
            </div>
            <span class="text-[9px] font-bold text-gray-500 tracking-wider uppercase text-right">{{ profile.xp }} / {{ profile.xpToNextLevel }} XP</span>
          </div>
        </div>
      </div>

      <!-- Notifications -->
      <div class="relative">
        <button class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 relative p-1">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
          <!-- Badge -->
          <span 
            v-if="userStore.unreadCount > 0" 
            class="absolute top-0 right-0 w-2 h-2 bg-danger-500 border-2 border-white dark:border-gray-800 rounded-full"
          />
        </button>
      </div>

      <!-- User Profile -->
      <UserProfileDropdown />
    </div>
  </header>
</template>

<script setup>
/**
 * TopBar — Main application header with search, stats, and profile dropdown
 */
import { computed } from 'vue'
import { useUiStore } from '@/stores/ui'
import { useUserStore } from '@/stores/user'
import { useModulesStore } from '@/stores/modules'
import Breadcrumb from '@/components/common/Breadcrumb.vue'
import SearchBar from '@/components/common/SearchBar.vue'
import UserProfileDropdown from './UserProfileDropdown.vue'

const uiStore = useUiStore()
const userStore = useUserStore()
const modulesStore = useModulesStore()

const profile = computed(() => userStore.profile)
const activeModule = computed(() => modulesStore.activeModule)

const breadcrumbItems = computed(() => {
  const items = [
    { label: 'Dashboard', to: '/' }
  ]
  if (activeModule.value) {
    items.push({ label: 'Matematika' })
    items.push({ label: activeModule.value.title })
  }
  return items
})
</script>
