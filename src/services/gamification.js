import api from './api'

export const gamificationService = {
  async getLeaderboard() {
    return api.get('/gamification/leaderboard')
  },

  async getRewards() {
    return api.get('/gamification/rewards')
  },

  async redeemReward(rewardId) {
    return api.post('/gamification/rewards/redeem', { reward_id: rewardId })
  },
}
