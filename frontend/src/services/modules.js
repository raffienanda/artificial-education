/**
 * Modules Service connected to FastAPI Backend
 * Uses centralized axios instance with interceptors
 */
import api from './api'

export const modulesService = {
  /** Fetch the current course details */
  async getCourse() {
    const data = await api.get('/modules/course/current')
    return data
  },

  /** Fetch all available courses */
  async getCourses() {
    const data = await api.get('/modules/courses')
    return data
  },

  /** Fetch all modules */
  async getModules(courseId = null, userId = null) {
    const data = await api.get('/modules', {
      params: {
        ...(courseId ? { course_id: courseId } : {}),
        ...(userId ? { user_id: userId } : {}),
      },
    })
    return data
  },

  /** Fetch a single module by ID with full subtopic content */
  async getModuleById(moduleId, userId = null) {
    const data = await api.get(`/modules/${moduleId}`, {
      params: userId ? { user_id: userId } : {},
    })
    return data
  },

  /** Fetch subtopic content */
  async getSubtopicContent(moduleId, subtopicId) {
    const data = await api.get(`/modules/${moduleId}/subtopics/${subtopicId}`)
    return data
  },
}
