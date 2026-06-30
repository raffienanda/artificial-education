<template>
  <div class="h-screen w-full flex bg-surface-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100 overflow-hidden font-sans">
    <!-- Sidebar -->
    <TheSidebar />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden relative">
      <!-- Header -->
      <TopBar />

      <!-- Page Content -->
      <main class="flex-1 overflow-hidden relative">
        <RouterView />
      </main>
    </div>

    <!-- Modals & Overlays -->
    <SettingsModal />
    <ToastNotification />
    <ConfettiEffect :active="userStore.recentLevelUp" />
    <AchievementModal 
      :show="userStore.recentLevelUp || !!userStore.recentAchievement" 
      :achievement="userStore.recentAchievement" 
      @close="userStore.clearGamificationEvents()"
    />
  </div>
</template>

<script setup>
/**
 * DashboardLayout — Main application layout wrapper
 * Contains the Sidebar, TopBar, and handles the responsive flex container
 */
import TheSidebar from '@/components/sidebar/TheSidebar.vue'
import TopBar from '@/components/header/TopBar.vue'
import SettingsModal from '@/components/header/SettingsModal.vue'
import ToastNotification from '@/components/common/ToastNotification.vue'
import ConfettiEffect from '@/components/common/ConfettiEffect.vue'
import AchievementModal from '@/components/common/AchievementModal.vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
</script>
