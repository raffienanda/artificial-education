import api from './api'

export const recommendationService = {
  async getNextRecommendation({ userId, currentModuleId, currentSubtopicId }) {
    return api.post('/recommendation/next', {
      user_id: userId,
      current_module_id: currentModuleId,
      current_subtopic_id: currentSubtopicId,
    })
  },

  async getInteractionLogs({ userId, limit = 8 } = {}) {
    return api.get('/recommendation/logs', {
      params: {
        user_id: userId,
        limit,
      },
    })
  },
}
