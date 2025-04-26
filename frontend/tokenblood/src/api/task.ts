import { useAuthStore } from '@/stores/auth'

export const evaluatePrompt = async (prompt: string, taskName: string) => {
  const authStore = useAuthStore()
  const userId = authStore.user?.userId
  
  if (!userId) {
    throw new Error('User not authenticated')
  }
  
  // Mock implementation
  console.log('Evaluating prompt:', {
    prompt,
    taskName,
    userId
  })
} 