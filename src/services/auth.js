import api from './api'

export const authService = {
  async login({ username, password }) {
    return api.post('/auth/login', { username, password })
  },

  async register({ username, password, displayName }) {
    return api.post('/auth/register', {
      username,
      password,
      display_name: displayName,
    })
  },

  async me() {
    return api.get('/auth/me')
  },
}
