import api from './api'

export const cognitiveService = {
  async getItems() {
    return api.get('/cognitive/items')
  },

  async getProfile() {
    return api.get('/cognitive/profile')
  },

  async getResponses() {
    return api.get('/cognitive/responses')
  },

  async submitResponses(responses) {
    return api.post('/cognitive/responses', { responses })
  },
}
