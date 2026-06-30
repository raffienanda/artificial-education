/**
 * API Service — Axios Instance
 * Centralized HTTP client with interceptors, ready for backend integration.
 * All mock calls currently use simulated delays to mimic real API behavior.
 */
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor — attach auth token when available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor — handle common errors
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          console.warn('[API] Unauthorized — redirecting to login')
          break
        case 403:
          console.warn('[API] Forbidden — insufficient permissions')
          break
        case 500:
          console.error('[API] Server error')
          break
      }
    }
    return Promise.reject(error)
  }
)

/**
 * Simulate an API delay for mock data
 * @param {number} ms - Delay in milliseconds
 */
export const delay = (ms = 500) => new Promise((resolve) => setTimeout(resolve, ms))

export default api
