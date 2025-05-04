import { defineStore } from 'pinia'
import { ref } from 'vue'

interface AuthCredentials {
  username: string
  email: string
}

interface AuthResponse {
  user_id: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    currentUser: '',
    userId: '',
    isAuthenticated: false,
    isLoading: false
  }),
  
  actions: {
    async auth(credentials: AuthCredentials) {
      this.isLoading = true
      try {
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/auth`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(credentials)
        })

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Authentication failed')
        }

        const data = await response.json() as AuthResponse
        this.login(credentials.username, data.user_id)
        return { userId: data.user_id, username: credentials.username }
      } catch (error) {
        console.error('Auth error:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },

    setCurrentUser(username: string) {
      this.currentUser = username
    },

    logout() {
      this.currentUser = ''
      this.userId = ''
      this.isAuthenticated = false
    },

    login(username: string, userId: string) {
      this.currentUser = username
      this.userId = userId
      this.isAuthenticated = true
    }
  }
}) 