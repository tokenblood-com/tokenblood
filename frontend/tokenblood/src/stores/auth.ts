import { defineStore } from 'pinia'
import { v4 as uuidv4 } from 'uuid'

interface LoginFormData {
  username: string
  email?: string
}

interface UserState {
  username: string
  userId: string
  email?: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoading: false,
    user: null as UserState | null
  }),
  
  actions: {
    async auth(data: LoginFormData) {
      this.isLoading = true
      try {
        const userId = uuidv4()
        this.user = {
          username: data.username,
          userId,
          email: data.email
        }
        console.log('Creating new user with ID:', this.user)
        return this.user
      } finally {
        this.isLoading = false
      }
    }
  }
}) 