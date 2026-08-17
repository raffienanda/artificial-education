/**
 * useToast Composable
 * Provides toast notification display functionality
 */
import { useUiStore } from '@/stores/ui'

export function useToast() {
  const uiStore = useUiStore()

  function success(message, duration = 4000) {
    uiStore.showToast(message, 'success', duration)
  }

  function error(message, duration = 5000) {
    uiStore.showToast(message, 'error', duration)
  }

  function info(message, duration = 4000) {
    uiStore.showToast(message, 'info', duration)
  }

  function warning(message, duration = 4500) {
    uiStore.showToast(message, 'warning', duration)
  }

  return {
    success,
    error,
    info,
    warning,
  }
}
