import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { gamificationService } from '@/services/gamification'
import { useUserStore } from './user'

export const useGamificationStore = defineStore('gamification', () => {
  const leaderboard = ref([])
  const rewards = ref([])
  const loading = ref(false)
  const error = ref('')
  const message = ref('')

  const redeemedRewardIds = computed(() => useUserStore().currentUser?.redeemed_rewards || [])

  async function fetchAll() {
    loading.value = true
    error.value = ''
    try {
      const [leaderboardData, rewardData] = await Promise.all([
        gamificationService.getLeaderboard(),
        gamificationService.getRewards(),
      ])
      leaderboard.value = leaderboardData
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
      await fetchAll()
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
    rewards,
    loading,
    error,
    message,
    redeemedRewardIds,
    fetchAll,
    redeem,
  }
})
