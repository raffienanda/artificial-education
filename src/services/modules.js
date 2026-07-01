/**
 * Modules Service connected to FastAPI Backend
 * Uses centralized axios instance with interceptors
 */
import api from './api'
import { course } from '@/data/modules' // keeping course static for now

export const modulesService = {
  /** Fetch the course details (mocked) */
  async getCourse() {
    return { ...course }
  },

  /** Fetch all modules */
  async getModules() {
    const data = await api.get('/modules')
    return data
  },

  /** Fetch a single module by ID with full subtopic content */
  async getModuleById(moduleId) {
    const data = await api.get(`/modules/${moduleId}`)
    return data
  },

  /** Fetch subtopic content */
  async getSubtopicContent(moduleId, subtopicId) {
    const data = await api.get(`/modules/${moduleId}/subtopics/${subtopicId}`)
    return data
  },
}
