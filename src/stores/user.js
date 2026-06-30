/**
 * User Store — Student profile, streak, achievements, and notifications
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { studentProfile, achievements, notifications, learningHistory } from '@/data/student'

export const useUserStore = defineStore('user', () => {
  const profile = ref({ ...studentProfile })
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

  function clearGamificationEvents() {
    recentLevelUp.value = false
    recentAchievement.value = null
  }

  return {
    profile,
    userAchievements,
    userNotifications,
    history,
    recentLevelUp,
    recentAchievement,
    unreadNotifications,
    unreadCount,
    earnedAchievements,
    dailyGoalProgress,
    xpProgress,
    markNotificationRead,
    markAllNotificationsRead,
    addStudyTime,
    addXP,
    clearGamificationEvents,
  }
})
