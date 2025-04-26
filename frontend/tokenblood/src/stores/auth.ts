import { defineStore } from 'pinia'

interface LoginFormData {
  username: string
  email?: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoading: false
  }),
  
  actions: {
    async auth(data: LoginFormData) {
      this.isLoading = true
      try {
        console.log('Auth attempt:', data)
        // TODO: Implement actual API call
        await new Promise(resolve => setTimeout(resolve, 1000)) // Simulate API call
      } finally {
        this.isLoading = false
      }
    }
  }
}) 