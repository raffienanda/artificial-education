/**
 * UI Store — Global UI state management
 * Handles sidebar, dark mode, toasts, modals, and responsive state
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const THEME_PREF_KEY = 'activeThemeByUser'

export const useUiStore = defineStore('ui', () => {
  // Sidebar state
  const sidebarCollapsed = ref(false)
  const sidebarMobileOpen = ref(false)

  // Dark mode
  const darkMode = ref(localStorage.getItem('darkMode') === 'true')
  const activeTheme = ref('default')
  const themeEnabled = ref(false)

  // Toast notifications queue
  const toasts = ref([])

  // Modals
  const settingsModalOpen = ref(false)

  // Mobile chatbot overlay
  const chatbotMobileOpen = ref(false)
  const chatbotDesktopVisible = ref(localStorage.getItem('chatbotDesktopVisible') !== 'false')
  const progressPanelVisible = ref(localStorage.getItem('progressPanelVisible') !== 'false')

  // Loading states
  const globalLoading = ref(false)

  // Toggle sidebar collapse
  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  // Toggle mobile sidebar drawer
  function toggleMobileSidebar() {
    sidebarMobileOpen.value = !sidebarMobileOpen.value
  }

  // Toggle dark mode with persistence
  function toggleDarkMode() {
    darkMode.value = !darkMode.value
    localStorage.setItem('darkMode', darkMode.value)
    if (darkMode.value) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  // Initialize dark mode on app load
  function initDarkMode() {
    if (darkMode.value) {
      document.documentElement.classList.add('dark')
    }
  }

  function syncThemeDocument() {
    if (!themeEnabled.value || activeTheme.value === 'default') {
      delete document.documentElement.dataset.theme
    } else {
      document.documentElement.dataset.theme = activeTheme.value
    }
  }

  function readThemePreferences() {
    try {
      const parsed = JSON.parse(localStorage.getItem(THEME_PREF_KEY) || '{}')
      return parsed && typeof parsed === 'object' && !Array.isArray(parsed) ? parsed : {}
    } catch {
      return {}
    }
  }

  function writeThemePreferences(preferences) {
    localStorage.setItem(THEME_PREF_KEY, JSON.stringify(preferences))
  }

  function getThemePreference(userId) {
    if (!userId) return 'default'
    return readThemePreferences()[String(userId)] || 'default'
  }

  function saveThemePreference(userId, themeId) {
    if (!userId) return
    const preferences = readThemePreferences()
    preferences[String(userId)] = themeId || 'default'
    writeThemePreferences(preferences)
  }

  function applyTheme(themeId, options = {}) {
    activeTheme.value = themeId || 'default'
    if (options.userId) {
      saveThemePreference(options.userId, activeTheme.value)
    }
    syncThemeDocument()
  }

  function applyThemeForUser(userId, redeemedThemeIds = []) {
    const savedTheme = getThemePreference(userId)
    const ownedThemeIds = new Set(redeemedThemeIds)
    const nextTheme = savedTheme === 'default' || ownedThemeIds.has(savedTheme)
      ? savedTheme
      : 'default'

    activeTheme.value = nextTheme
    syncThemeDocument()
  }

  function setThemeEnabled(enabled) {
    themeEnabled.value = Boolean(enabled)
    syncThemeDocument()
  }

  function initTheme(enabled = false) {
    setThemeEnabled(enabled)
  }

  // Show a toast notification
  function showToast(message, type = 'info', duration = 4000) {
    const id = `toast-${Date.now()}`
    toasts.value.push({ id, message, type, duration })
    setTimeout(() => {
      removeToast(id)
    }, duration)
  }

  // Remove a toast by ID
  function removeToast(id) {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }

  // Toggle settings modal
  function toggleSettingsModal() {
    settingsModalOpen.value = !settingsModalOpen.value
  }

  // Toggle mobile chatbot overlay
  function toggleChatbotMobile() {
    chatbotMobileOpen.value = !chatbotMobileOpen.value
  }

  function toggleChatbotDesktop() {
    chatbotDesktopVisible.value = !chatbotDesktopVisible.value
    localStorage.setItem('chatbotDesktopVisible', String(chatbotDesktopVisible.value))
  }

  function toggleProgressPanel() {
    progressPanelVisible.value = !progressPanelVisible.value
    localStorage.setItem('progressPanelVisible', String(progressPanelVisible.value))
  }

  return {
    sidebarCollapsed,
    sidebarMobileOpen,
    darkMode,
    activeTheme,
    themeEnabled,
    toasts,
    settingsModalOpen,
    chatbotMobileOpen,
    chatbotDesktopVisible,
    progressPanelVisible,
    globalLoading,
    toggleSidebar,
    toggleMobileSidebar,
    toggleDarkMode,
    initDarkMode,
    applyTheme,
    applyThemeForUser,
    setThemeEnabled,
    initTheme,
    showToast,
    removeToast,
    toggleSettingsModal,
    toggleChatbotMobile,
    toggleChatbotDesktop,
    toggleProgressPanel,
  }
})
