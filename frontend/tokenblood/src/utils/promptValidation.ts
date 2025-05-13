interface ValidationResult {
  isValid: boolean
  error: string | null
}

export const validatePrompt = (promptText: string): ValidationResult => {
  if (!promptText) {
    return {
      isValid: false,
      error: 'Please enter a prompt'
    }
  }
  
  if (!promptText.includes('{{document}}')) {
    return {
      isValid: false,
      error: 'Prompt must contain {{document}} placeholder'
    }
  }
  
  return {
    isValid: true,
    error: null
  }
} 