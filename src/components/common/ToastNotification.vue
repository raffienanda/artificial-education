<template>
  <Teleport to="body">
    <TransitionGroup
      name="toast"
      tag="div"
      class="fixed top-4 right-4 z-[9999] flex flex-col gap-3 max-w-sm"
    >
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="[
          'flex items-start gap-3 px-4 py-3 rounded-2xl shadow-elevated border backdrop-blur-sm',
          toastClasses[toast.type],
        ]"
        class="animate-slide-in-right"
      >
        <!-- Icon -->
        <span class="text-lg mt-0.5">{{ toastIcons[toast.type] }}</span>

        <!-- Content -->
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium">{{ toast.message }}</p>
        </div>

        <!-- Close button -->
        <button
          class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors mt-0.5"
          @click="uiStore.removeToast(toast.id)"
        >
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </TransitionGroup>
  </Teleport>
</template>

<script setup>
/**
 * ToastNotification — Slide-in notification toasts with auto-dismiss
 */
import { computed } from 'vue'
import { useUiStore } from '@/stores/ui'

const uiStore = useUiStore()
const toasts = computed(() => uiStore.toasts)

const toastClasses = {
  success: 'bg-success-50/90 border-success-200 text-success-600 dark:bg-success-900/40 dark:border-success-800 dark:text-success-400',
  error: 'bg-danger-50/90 border-danger-200 text-danger-600 dark:bg-danger-900/40 dark:border-danger-800 dark:text-danger-400',
  warning: 'bg-warning-50/90 border-warning-200 text-warning-600 dark:bg-warning-900/40 dark:border-warning-800 dark:text-warning-400',
  info: 'bg-primary-50/90 border-primary-200 text-primary-600 dark:bg-primary-900/40 dark:border-primary-800 dark:text-primary-400',
}

const toastIcons = {
  success: '✅',
  error: '❌',
  warning: '⚠️',
  info: 'ℹ️',
}
</script>

<style scoped>
.toast-enter-active {
  transition: all 0.3s ease-out;
}
.toast-leave-active {
  transition: all 0.2s ease-in;
}
.toast-enter-from {
  transform: translateX(100%);
  opacity: 0;
}
.toast-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>
