<template>
  <div class="relative" ref="dropdownRef">
    <!-- Trigger -->
    <button 
      class="flex items-center gap-2 hover:opacity-80 transition-opacity focus:outline-none"
      @click="isOpen = !isOpen"
    >
      <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-primary-500 to-primary-700 text-white flex items-center justify-center font-bold text-sm shadow-sm">
        {{ profile.initials }}
      </div>
      <div class="hidden sm:block text-left ml-1">
        <p class="text-xs font-bold text-gray-800 dark:text-gray-100 leading-tight">{{ profile.name }}</p>
        <p class="text-[10px] text-gray-500 leading-tight">Lvl {{ profile.level }} Student</p>
      </div>
      <svg class="hidden sm:block w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- Dropdown Menu -->
    <Transition name="dropdown">
      <div 
        v-if="isOpen" 
        class="absolute right-0 top-full mt-2 w-56 bg-white dark:bg-gray-800 rounded-2xl shadow-elevated border border-gray-100 dark:border-gray-700 py-2 z-50 origin-top-right"
      >
        <!-- User Info header -->
        <div class="px-4 py-3 border-b border-gray-100 dark:border-gray-700 mb-2">
          <p class="text-sm font-bold text-gray-800 dark:text-white truncate">{{ profile.name }}</p>
          <p class="text-xs text-gray-500 truncate">{{ profile.email }}</p>
          
          <!-- XP Progress -->
          <div class="mt-3">
            <div class="flex justify-between text-[10px] font-medium text-gray-500 mb-1">
              <span>Level {{ profile.level }}</span>
              <span>{{ profile.xp }} / {{ profile.xpToNextLevel }} XP</span>
            </div>
            <div class="progress-bar h-1">
              <div class="progress-bar-fill bg-warning-400" :style="{ width: userStore.xpProgress + '%' }" />
            </div>
          </div>
        </div>

        <!-- Links -->
        <div class="px-2 space-y-1">
          <RouterLink
            to="/profile"
            class="flex items-center gap-3 px-3 py-2 text-sm text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/50 rounded-lg transition-colors"
            @click="isOpen = false"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
            My Profile
          </RouterLink>

          <RouterLink
            v-if="userStore.currentUser?.role === 'admin'"
            to="/admin"
            class="flex items-center gap-3 px-3 py-2 text-sm text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/50 rounded-lg transition-colors"
            @click="isOpen = false"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
            Admin Panel
          </RouterLink>

          <RouterLink
            to="/gamification"
            class="flex items-center gap-3 px-3 py-2 text-sm text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/50 rounded-lg transition-colors"
            @click="isOpen = false"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.563.563 0 00-.182-.557L3.041 10.385a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345l2.125-5.111z" /></svg>
            Gamifikasi
          </RouterLink>
          
          <button 
            class="w-full flex items-center justify-between px-3 py-2 text-sm text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/50 rounded-lg transition-colors text-left"
            @click="uiStore.toggleDarkMode(); isOpen = false"
          >
            <div class="flex items-center gap-3">
              <svg v-if="uiStore.darkMode" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
              <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" /></svg>
              {{ uiStore.darkMode ? 'Light Mode' : 'Dark Mode' }}
            </div>
          </button>
          
          <button 
            class="w-full flex items-center gap-3 px-3 py-2 text-sm text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/50 rounded-lg transition-colors text-left"
            @click="uiStore.toggleSettingsModal(); isOpen = false"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
            Settings
          </button>
        </div>

        <div class="px-2 mt-2 pt-2 border-t border-gray-100 dark:border-gray-700">
          <button
            class="w-full flex items-center gap-3 px-3 py-2 text-sm text-danger-600 hover:bg-danger-50 dark:hover:bg-danger-900/20 rounded-lg transition-colors text-left"
            @click="handleLogout"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
            Sign Out
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
/**
 * UserProfileDropdown — Avatar button with dropdown menu for user settings
 */
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useUiStore } from '@/stores/ui'

const userStore = useUserStore()
const uiStore = useUiStore()
const router = useRouter()

const profile = computed(() => userStore.profile)
const isOpen = ref(false)
const dropdownRef = ref(null)

// Close on outside click
function handleClickOutside(e) {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target)) {
    isOpen.value = false
  }
}

function handleLogout() {
  userStore.logout()
  isOpen.value = false
  router.push('/login')
}

onMounted(() => {
  document.addEventListener('mousedown', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('mousedown', handleClickOutside)
})
</script>

<style scoped>
.dropdown-enter-active {
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.dropdown-leave-active {
  transition: all 0.15s ease-in;
}
.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-5px);
}
</style>
