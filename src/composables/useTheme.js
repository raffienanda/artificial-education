/**
 * useTheme Composable
 * Provides reactive dark mode state and toggle functionality
 */
import { computed } from 'vue'
import { useUiStore } from '@/stores/ui'

export function useTheme() {
  const uiStore = useUiStore()

  const isDark = computed(() => uiStore.darkMode)

  function toggle() {
    uiStore.toggleDarkMode()
  }

  function init() {
    uiStore.initDarkMode()
  }

  return {
    isDark,
    toggle,
    init,
  }
}
