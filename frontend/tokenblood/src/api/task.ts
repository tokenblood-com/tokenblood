import { useAuthStore } from '@/stores/auth'
import { useErrorStore } from '@/stores/errorStore'

export interface EvaluationResult {
  score: number
}

export const evaluatePrompt = async (prompt: string, taskName: string): Promise<EvaluationResult> => {
  const authStore = useAuthStore()
  const username = authStore.currentUser
  console.log(username)
  
  if (!username) {
    const error = new Error('User not authenticated')
    throw error
  }

  console.log(`${import.meta.env.VITE_BACKEND_URL}/models/evaluate`)
  console.log(taskName)
  const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/models/evaluate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      task: taskName,
      prompt: prompt
    })
  })

  if (!response.ok) {
    const error = await response.json()
    if (response.status === 404) {
      console.error('Not found:', error.detail)
    }
    const errorMessage = error.detail || 'Failed to evaluate prompt'
    throw new Error(errorMessage)
  }
  const result = await response.json()
  return {
    score: result.accuracy_score
  }
}