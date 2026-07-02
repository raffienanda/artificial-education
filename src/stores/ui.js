/**
 * UI Store — Global UI state management
 * Handles sidebar, dark mode, toasts, modals, and responsive state
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUiStore = defineStore('ui', () => {
  // Sidebar state
  const sidebarCollapsed = ref(false)
  const sidebarMobileOpen = ref(false)

  // Dark mode
  const darkMode = ref(localStorage.getItem('darkMode') === 'true')

  // Toast notifications queue
  const toasts = ref([])

  // Modals
  const settingsModalOpen = ref(false)
  const searchModalOpen = ref(false)

  // Mobile chatbot overlay
  const chatbotMobileOpen = ref(false)
  const chatbotDesktopVisible = ref(localStorage.getItem('chatbotDesktopVisible') !== 'false')

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

  // Toggle search modal
  function toggleSearchModal() {
    searchModalOpen.value = !searchModalOpen.value
  }

  // Toggle mobile chatbot overlay
  function toggleChatbotMobile() {
    chatbotMobileOpen.value = !chatbotMobileOpen.value
  }

  function toggleChatbotDesktop() {
    chatbotDesktopVisible.value = !chatbotDesktopVisible.value
    localStorage.setItem('chatbotDesktopVisible', String(chatbotDesktopVisible.value))
  }

  return {
    sidebarCollapsed,
    sidebarMobileOpen,
    darkMode,
    toasts,
    settingsModalOpen,
    searchModalOpen,
    chatbotMobileOpen,
    chatbotDesktopVisible,
    globalLoading,
    toggleSidebar,
    toggleMobileSidebar,
    toggleDarkMode,
    initDarkMode,
    showToast,
    removeToast,
    toggleSettingsModal,
    toggleSearchModal,
    toggleChatbotMobile,
    toggleChatbotDesktop,
  }
})
