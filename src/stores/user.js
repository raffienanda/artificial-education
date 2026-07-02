/**
 * User Store — Student profile, streak, achievements, and notifications
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { studentProfile, achievements, notifications, learningHistory } from '@/data/student'
import { authService } from '@/services/auth'

export const useUserStore = defineStore('user', () => {
  const profile = ref({ ...studentProfile })
  const token = ref(localStorage.getItem('auth_token') || '')
  const currentUser = ref(JSON.parse(localStorage.getItem('auth_user') || 'null'))
  const authLoading = ref(false)
  const authError = ref(null)
  const userAchievements = ref([...achievements])
  const userNotifications = ref([...notifications])
  const history = ref([...learningHistory])
  
  // Gamification triggers
  const recentLevelUp = ref(false)
  const recentAchievement = ref(null)

  // Computed
  const unreadNotifications = computed(() =>
    userNotifications.value.filter((n) => !n.read)
  )

  const unreadCount = computed(() => unreadNotifications.value.length)
  const isAuthenticated = computed(() => Boolean(token.value && currentUser.value))
  const userId = computed(() => currentUser.value?.id || 1)

  const earnedAchievements = computed(() =>
    userAchievements.value.filter((a) => a.earned)
  )

  const dailyGoalProgress = computed(() =>
    Math.min(100, Math.round((profile.value.todayStudyTime / profile.value.dailyGoal) * 100))
  )

  const xpProgress = computed(() =>
    Math.round((profile.value.xp / profile.value.xpToNextLevel) * 100)
  )

  // Actions
  function syncProfile(user) {
    if (!user) return
    const name = user.display_name || user.username
    profile.value = {
      ...profile.value,
      name,
      email: user.username,
      initials: name
        .split(' ')
        .filter(Boolean)
        .slice(0, 2)
        .map((part) => part[0]?.toUpperCase())
        .join('') || 'U',
      xp: user.xp_in_level ?? user.xp ?? 0,
      totalXp: user.xp || 0,
      level: user.level || 1,
      xpToNextLevel: user.xp_to_next_level || 500,
      currentStreak: user.current_streak || 0,
      longestStreak: user.longest_streak || 0,
      combo: user.combo || 0,
      totalScore: user.total_score || 0,
      rewardPoints: user.reward_points || 0,
      redeemedRewards: user.redeemed_rewards || [],
    }
    currentUser.value = user
    localStorage.setItem('auth_user', JSON.stringify(user))
  }

  function setSession(authPayload) {
    token.value = authPayload.access_token
    currentUser.value = authPayload.user
    localStorage.setItem('auth_token', token.value)
    localStorage.setItem('auth_user', JSON.stringify(currentUser.value))
    syncProfile(currentUser.value)
  }

  async function login(credentials) {
    authLoading.value = true
    authError.value = null
    try {
      const data = await authService.login(credentials)
      setSession(data)
      return true
    } catch (error) {
      authError.value = error.response?.data?.detail || 'Login gagal'
      return false
    } finally {
      authLoading.value = false
    }
  }

  async function register(payload) {
    authLoading.value = true
    authError.value = null
    try {
      const data = await authService.register(payload)
      setSession(data)
      return true
    } catch (error) {
      authError.value = error.response?.data?.detail || 'Registrasi gagal'
      return false
    } finally {
      authLoading.value = false
    }
  }

  async function initAuth() {
    if (!token.value) return false
    authLoading.value = true
    try {
      currentUser.value = await authService.me()
      localStorage.setItem('auth_user', JSON.stringify(currentUser.value))
      syncProfile(currentUser.value)
      return true
    } catch {
      logout()
      return false
    } finally {
      authLoading.value = false
    }
  }

  function logout() {
    token.value = ''
    currentUser.value = null
    localStorage.removeItem('auth_token')
    localStorage.removeItem('auth_user')
  }

  function markNotificationRead(notifId) {
    const notif = userNotifications.value.find((n) => n.id === notifId)
    if (notif) notif.read = true
  }

  function markAllNotificationsRead() {
    userNotifications.value.forEach((n) => (n.read = true))
  }

  function addStudyTime(minutes) {
    profile.value.todayStudyTime += minutes
  }

  function addXP(amount) {
    profile.value.xp += amount
    if (profile.value.xp >= profile.value.xpToNextLevel) {
      profile.value.level += 1
      profile.value.xp -= profile.value.xpToNextLevel
      recentLevelUp.value = true
    }
  }

  function applyQuizUserUpdate(user) {
    syncProfile(user)
  }

  function clearGamificationEvents() {
    recentLevelUp.value = false
    recentAchievement.value = null
  }

  return {
    profile,
    token,
    currentUser,
    authLoading,
    authError,
    userAchievements,
    userNotifications,
    history,
    recentLevelUp,
    recentAchievement,
    isAuthenticated,
    userId,
    unreadNotifications,
    unreadCount,
    earnedAchievements,
    dailyGoalProgress,
    xpProgress,
    login,
    register,
    initAuth,
    logout,
    markNotificationRead,
    markAllNotificationsRead,
    addStudyTime,
    addXP,
    syncProfile,
    applyQuizUserUpdate,
    clearGamificationEvents,
  }
})
