import { defineStore } from 'pinia'
import { ref } from 'vue'

interface AuthCredentials {
  username: string
  email: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    currentUser: '',
    isAuthenticated: false,
    isLoading: false
  }),
  
  actions: {
    async auth(credentials: AuthCredentials) {
      this.isLoading = true
      try {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // Mock successful authentication
        this.login(credentials.username)
        return { userId: '123', username: credentials.username }
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
      this.isAuthenticated = false
    },

    login(username: string) {
      this.currentUser = username
      this.isAuthenticated = true
    }
  }
}) 