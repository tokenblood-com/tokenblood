import { useAuthStore } from '@/stores/auth'

interface EvaluationResult {
  score: number;
}

export const evaluatePrompt = async (prompt: string, taskName: string): Promise<EvaluationResult> => {
  const authStore = useAuthStore()
  const username = authStore.currentUser
  
  if (!username) {
    throw new Error('User not authenticated')
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
    throw new Error(error.detail || 'Failed to evaluate prompt')
  }
  const result = await response.json()
  return {
    score: result.accuracy_score
  }
}