/**
 * API Service - Axios instance for the FastAPI backend.
 */
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
})

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

api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          console.warn('[API] Unauthorized')
          break
        case 403:
          console.warn('[API] Forbidden')
          break
        case 500:
          console.error('[API] Server error')
          break
      }
    }
    return Promise.reject(error)
  }
)

export default api
