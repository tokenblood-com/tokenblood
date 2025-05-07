<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getTask, type TaskConfiguration } from '@/types/task'
import { evaluatePrompt } from '@/api/task'
import { validatePrompt } from '@/utils/promptValidation'

const route = useRoute()
const task = ref<TaskConfiguration | null>(null)
const prompt = ref('')
const isSubmitting = ref(false)
const error = ref('')
const score = ref<string | null>(null)

onMounted(async () => {
  const taskName = route.params.name as string
  task.value = await getTask(taskName)
})

const handleSubmit = async () => {
  if (!task.value) return
  
  const validation = validatePrompt(prompt.value)
  if (!validation.isValid) {
    error.value = validation.error || ''
    return
  }
  
  error.value = ''
  score.value = null
  isSubmitting.value = true
  try {
    const result = await evaluatePrompt(prompt.value, task.value.backend_name)
    score.value = result.score.toString()
  } finally {
    isSubmitting.value = false
  }
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
        <div v-if="error" class="error-message">{{ error }}</div>
        <div v-if="score" class="score-display">Score: {{ score }}</div>
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
  margin-top: 20px;
}

.status-container {
  display: flex;
  align-items: center;
  gap: 20px;
}

.error-message {
  color: var(--accent-color);
  font-family: 'Roboto Slab', serif;
  font-size: 14px;
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
  transition: opacity 0.3s;
  margin-left: 20px;
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
}
</style> 