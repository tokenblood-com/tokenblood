<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getTask, type TaskConfiguration } from '@/types/task'
import { evaluatePrompt } from '@/api/task'
import { validatePrompt } from '@/utils/promptValidation'
import { useErrorStore } from '@/stores/errorStore'

const route = useRoute()
const task = ref<TaskConfiguration | null>(null)
const prompt = ref('')
const isSubmitting = ref(false)
const error = ref('')
const score = ref<number | null>(null)
const errorVisible = ref(false)

watch(error, (newError) => {
  if (newError) {
    errorVisible.value = true
    setTimeout(() => {
      errorVisible.value = false
      setTimeout(() => {
        error.value = ''
      }, 300) // Wait for fade animation to complete
    }, 3000)
  }
})

onMounted(async () => {
  const taskName = route.params.name as string
  task.value = await getTask(taskName)
})

const handleSubmit = async () => {
  const { showError } = useErrorStore()
  
  if (!task.value) {
    showError('No task selected')
    return
  }
  
  const validation = validatePrompt(prompt.value)
  if (!validation.isValid) {
    const errorMessage = validation.error || 'Invalid prompt'
    error.value = errorMessage
    return
  }
  
  error.value = ''
  score.value = null
  isSubmitting.value = true
  try {
    const result = await evaluatePrompt(prompt.value, task.value.backend_name)
    score.value = Number(result.score)
  } catch (err) {
    // evaluatePrompt already shows the error notification
    error.value = err instanceof Error ? err.message : 'Failed to evaluate prompt'
  } finally {
    isSubmitting.value = false
  }
}

const formattedScore = (): string => {
  if (score.value === null) return ''
  return score.value.toFixed(2)
}
</script>

<template>
  <div v-if="task" class="task-container">
    <h1>Task #{{ task.number }}: {{ task.name }}</h1>
    <p class="task-description">{{ task.description }}</p>
    <textarea
      v-model="prompt"
      class="prompt-input"
      placeholder="Enter your prompt"
    ></textarea>
    <div class="button-container">
      <div class="status-container">
        <Transition>
          <div v-if="error && errorVisible" class="error-message">{{ error }}</div>
        </Transition>
      </div>
      <div class="action-container">
        <div v-if="score !== null" class="score-display">
          Score: {{ formattedScore() }}
        </div>
        <button 
          class="submit-button"
          :disabled="isSubmitting"
          @click="handleSubmit"
        >
          {{ isSubmitting ? 'Submitting...' : 'Submit' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.task-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  font-family: 'Roboto Slab', serif;
  font-size: 25px;
  margin-bottom: 20px;
}

.task-description {
  white-space: pre-line;
  font-family: 'Roboto Slab', serif;
  font-size: 16px;
  line-height: 1.5;
  margin-bottom: 20px;
}

.prompt-input {
  width: 100%;
  height: 150px;
  background-color: var(--card-background);
  border: none;
  border-radius: 8px;
  padding: 16px;
  color: var(--prompt-text);
  font-family: 'Roboto Slab', serif;
  font-size: 16px;
  resize: none;
  margin-bottom: 20px;
}

.prompt-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.prompt-input:focus {
  outline: none;
}

.button-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.action-container {
  display: flex;
  align-items: center;
  gap: 20px;
}

.status-container {
  display: flex;
  align-items: center;
}

.error-message {
  color: var(--accent-color);
  font-family: 'Roboto Slab', serif;
  font-size: 16px;
}

.submit-button {
  width: 130px;
  height: 42px;
  background-color: var(--accent-color);
  color: white;
  border: none;
  border-radius: 8px;
  font-family: 'Roboto Slab', serif;
  font-size: 16px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.submit-button:hover:not(:disabled) {
  opacity: 0.9;
}

.submit-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.score-display {
  font-family: 'Roboto Slab', serif;
  font-size: 18px;
  color: var(--accent-color);
  min-width: 100px;
  text-align: right;
}

.v-enter-active,
.v-leave-active {
  transition: opacity 0.2s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style> 