import api from './api'

export const recommendationService = {
  async getNextRecommendation({ userId = 1, currentModuleId, currentSubtopicId }) {
    return api.post('/recommendation/next', {
      user_id: userId,
      current_module_id: currentModuleId,
      current_subtopic_id: currentSubtopicId,
    })
  },

  async getInteractionLogs({ userId = 1, limit = 8 } = {}) {
    return api.get('/recommendation/logs', {
      params: {
        user_id: userId,
        limit,
      },
    })
  },
}
