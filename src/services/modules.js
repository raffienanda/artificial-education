/**
 * Modules Service
 * Mock API calls for learning modules. Replace with real API calls when backend is ready.
 */
import { delay } from './api'
import { modules, course } from '@/data/modules'

export const modulesService = {
  /** Fetch the course details */
  async getCourse() {
    await delay(300)
    return { ...course }
  },

  /** Fetch all modules */
  async getModules() {
    await delay(400)
    return modules.map(({ subtopics, ...mod }) => ({
      ...mod,
      subtopicCount: subtopics.length,
    }))
  },

  /** Fetch a single module by ID with full subtopic content */
  async getModuleById(moduleId) {
    await delay(300)
    const mod = modules.find((m) => m.id === moduleId)
    if (!mod) throw new Error(`Module ${moduleId} not found`)
    return { ...mod }
  },

  /** Fetch subtopic content */
  async getSubtopicContent(moduleId, subtopicId) {
    await delay(200)
    const mod = modules.find((m) => m.id === moduleId)
    if (!mod) throw new Error(`Module ${moduleId} not found`)
    const subtopic = mod.subtopics.find((s) => s.id === subtopicId)
    if (!subtopic) throw new Error(`Subtopic ${subtopicId} not found`)
    return { ...subtopic }
  },
}
