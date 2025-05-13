import { reactive } from 'vue'

interface ErrorState {
  message: string
  isVisible: boolean
  type: 'error' | 'warning' | 'info'
}

const errorState = reactive<ErrorState>({
  message: '',
  isVisible: false,
  type: 'error'
})

export const useErrorStore = () => {
  const showError = (message: string) => {
    errorState.message = message
    errorState.type = 'error'
    errorState.isVisible = true
    setTimeout(() => {
      errorState.isVisible = false
    }, 5000)
  }

  const hideError = () => {
    errorState.isVisible = false
  }

  return {
    errorState,
    showError,
    hideError
  }
} 