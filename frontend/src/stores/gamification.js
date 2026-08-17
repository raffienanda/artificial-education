import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { gamificationService } from '@/services/gamification'
import { useUserStore } from './user'

export const useGamificationStore = defineStore('gamification', () => {
  const leaderboard = ref([])
  const leaderboardPage = ref(1)
  const leaderboardLimit = ref(5)
  const leaderboardTotal = ref(0)
  const leaderboardTotalPages = ref(1)
  const rewards = ref([])
  const loading = ref(false)
  const leaderboardLoading = ref(false)
  const error = ref('')
  const message = ref('')

  const redeemedRewardIds = computed(() => {
    const rawIds = useUserStore().currentUser?.redeemed_rewards || []
    return Array.isArray(rawIds) ? rawIds : []
  })
  const redeemedRewardIdSet = computed(() => new Set(redeemedRewardIds.value))

  async function fetchLeaderboard(page = leaderboardPage.value) {
    leaderboardLoading.value = true
    error.value = ''
    try {
      const data = await gamificationService.getLeaderboard({
        page,
        limit: leaderboardLimit.value,
      })
      leaderboard.value = data.items || []
      leaderboardPage.value = data.page || page
      leaderboardLimit.value = data.limit || leaderboardLimit.value
      leaderboardTotal.value = data.total || 0
      leaderboardTotalPages.value = data.total_pages || 1
    } catch (err) {
      error.value = err.response?.data?.detail || 'gagal memuat leaderboard'
    } finally {
      leaderboardLoading.value = false
    }
  }

  async function fetchAll() {
    loading.value = true
    error.value = ''
    try {
      const [leaderboardData, rewardData] = await Promise.all([
        gamificationService.getLeaderboard({
          page: leaderboardPage.value,
          limit: leaderboardLimit.value,
        }),
        gamificationService.getRewards(),
      ])
      leaderboard.value = leaderboardData.items || []
      leaderboardPage.value = leaderboardData.page || 1
      leaderboardLimit.value = leaderboardData.limit || leaderboardLimit.value
      leaderboardTotal.value = leaderboardData.total || 0
      leaderboardTotalPages.value = leaderboardData.total_pages || 1
      rewards.value = rewardData
    } catch (err) {
      error.value = err.response?.data?.detail || 'gagal memuat gamifikasi'
    } finally {
      loading.value = false
    }
  }

  async function redeem(rewardId) {
    loading.value = true
    error.value = ''
    message.value = ''
    try {
      const result = await gamificationService.redeemReward(rewardId)
      useUserStore().syncProfile(result.user)
      message.value = result.message
      await fetchLeaderboard()
      return true
    } catch (err) {
      error.value = err.response?.data?.detail || 'gagal menukar reward'
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    leaderboard,
    leaderboardPage,
    leaderboardLimit,
    leaderboardTotal,
    leaderboardTotalPages,
    rewards,
    loading,
    leaderboardLoading,
    error,
    message,
    redeemedRewardIds,
    redeemedRewardIdSet,
    fetchLeaderboard,
    fetchAll,
    redeem,
  }
})
