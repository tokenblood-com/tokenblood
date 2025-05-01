import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const currentUser = ref('maxikadze')
  const isAuthenticated = ref(true)

  function setCurrentUser(username: string) {
    currentUser.value = username
  }

  function logout() {
    currentUser.value = ''
    isAuthenticated.value = false
  }

  function login(username: string) {
    currentUser.value = username
    isAuthenticated.value = true
  }

  return {
    currentUser,
    isAuthenticated,
    setCurrentUser,
    login,
    logout
  }
}) 