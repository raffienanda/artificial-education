<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="uiStore.settingsModalOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <!-- Backdrop -->
        <div 
          class="absolute inset-0 bg-black/40 backdrop-blur-sm"
          @click="uiStore.toggleSettingsModal()"
        />

        <!-- Modal Dialog -->
        <div class="relative bg-white dark:bg-gray-800 rounded-3xl shadow-elevated w-full max-w-md overflow-hidden flex flex-col max-h-[90vh]">
          <!-- Header -->
          <div class="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex items-center justify-between flex-shrink-0">
            <h2 class="text-lg font-bold text-gray-900 dark:text-white">Settings</h2>
            <button 
              class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 p-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              @click="uiStore.toggleSettingsModal()"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Body -->
          <div class="p-6 overflow-y-auto space-y-6">
            <!-- Appearance -->
            <div>
              <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">Appearance</h3>
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-800 dark:text-gray-200">Dark Mode</p>
                  <p class="text-xs text-gray-500">Toggle dark theme</p>
                </div>
                <button 
                  class="relative w-11 h-6 rounded-full transition-colors duration-200"
                  :class="uiStore.darkMode ? 'bg-primary-500' : 'bg-gray-300 dark:bg-gray-600'"
                  @click="uiStore.toggleDarkMode()"
                >
                  <div 
                    class="absolute top-1 left-1 bg-white w-4 h-4 rounded-full transition-transform duration-200 shadow-sm"
                    :class="uiStore.darkMode ? 'transform translate-x-5' : ''"
                  />
                </button>
              </div>
            </div>

            <hr class="border-gray-100 dark:border-gray-700">

            <!-- Notifications -->
            <div>
              <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">Notifications</h3>
              <div class="space-y-4">
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-sm font-medium text-gray-800 dark:text-gray-200">Daily Reminders</p>
                    <p class="text-xs text-gray-500">Remind me to study daily</p>
                  </div>
                  <button
                    class="relative w-11 h-6 rounded-full transition-colors duration-200"
                    :class="dailyReminders ? 'bg-primary-500' : 'bg-gray-300 dark:bg-gray-600'"
                    @click="dailyReminders = !dailyReminders"
                  >
                    <div
                      class="absolute top-1 left-1 bg-white w-4 h-4 rounded-full shadow-sm transition-transform duration-200"
                      :class="dailyReminders ? 'translate-x-5' : ''"
                    />
                  </button>
                </div>
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-sm font-medium text-gray-800 dark:text-gray-200">Achievement Alerts</p>
                    <p class="text-xs text-gray-500">Notify when I unlock badges</p>
                  </div>
                  <button
                    class="relative w-11 h-6 rounded-full transition-colors duration-200"
                    :class="achievementAlerts ? 'bg-primary-500' : 'bg-gray-300 dark:bg-gray-600'"
                    @click="achievementAlerts = !achievementAlerts"
                  >
                    <div
                      class="absolute top-1 left-1 bg-white w-4 h-4 rounded-full shadow-sm transition-transform duration-200"
                      :class="achievementAlerts ? 'translate-x-5' : ''"
                    />
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Footer -->
          <div class="px-6 py-4 border-t border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 flex justify-end">
            <BaseButton variant="primary" @click="uiStore.toggleSettingsModal()">
              Save Preferences
            </BaseButton>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
/**
 * SettingsModal — Application settings dialog for appearance, notifications, etc.
 */
import { useUiStore } from '@/stores/ui'
import BaseButton from '@/components/common/BaseButton.vue'
import { ref } from 'vue'

const uiStore = useUiStore()
const dailyReminders = ref(true)
const achievementAlerts = ref(true)
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}
.modal-enter-active .relative,
.modal-leave-active .relative {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: scale(0.95) translateY(10px);
}
</style>
