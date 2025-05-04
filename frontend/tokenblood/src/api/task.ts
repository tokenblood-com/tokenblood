import { useAuthStore } from '@/stores/auth'

export const evaluatePrompt = async (prompt: string, taskName: string): Promise<string> => {
  const authStore = useAuthStore()
  const username = authStore.currentUser
  
  if (!username) {
    throw new Error('User not authenticated')
  }
  
  // Simulate API call with timeout
  await new Promise(resolve => setTimeout(resolve, 5000))
  
  return '0.76'
} 