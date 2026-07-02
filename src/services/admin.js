import api from './api'

export const adminService = {
  async getPrerequisites() {
    return api.get('/admin/prerequisites')
  },

  async createPrerequisite(payload) {
    return api.post('/admin/prerequisites', payload)
  },

  async updatePrerequisite(id, payload) {
    return api.patch(`/admin/prerequisites/${id}`, payload)
  },

  async deletePrerequisite(id) {
    return api.delete(`/admin/prerequisites/${id}`)
  },

  async getQuestions(params = {}) {
    return api.get('/admin/questions', { params })
  },

  async createQuestion(payload) {
    return api.post('/admin/questions', payload)
  },

  async updateQuestion(id, payload) {
    return api.patch(`/admin/questions/${id}`, payload)
  },

  async deleteQuestion(id) {
    return api.delete(`/admin/questions/${id}`)
  },

  async getSubtopics(params = {}) {
    return api.get('/admin/subtopics', { params })
  },

  async createSubtopic(payload) {
    return api.post('/admin/subtopics', payload)
  },

  async updateSubtopic(id, payload) {
    return api.patch(`/admin/subtopics/${id}`, payload)
  },

  async deleteSubtopic(id) {
    return api.delete(`/admin/subtopics/${id}`)
  },
}
