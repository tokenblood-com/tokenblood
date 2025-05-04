<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getTask, type TaskConfiguration } from '@/types/task'
import { evaluatePrompt } from '@/api/task'

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
  
  if (!prompt.value) {
    error.value = 'Please enter a prompt'
    return
  }
  
  error.value = ''
  score.value = null
  isSubmitting.value = true
  try {
    const result = await evaluatePrompt(prompt.value, task.value.name)
    score.value = result
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
    <div class="error-message" v-if="error">{{ error }}</div>
    <div class="button-container">
      <div v-if="score" class="score-display">
        Score: {{ score }}
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

.error-message {
  color: var(--accent-color);
  font-family: 'Roboto Slab', serif;
  font-size: 14px;
  margin-bottom: 10px;
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
}

.submit-button:hover:not(:disabled) {
  opacity: 0.9;
}

.submit-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.button-container {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-top: 20px;
  gap: 20px;
}

.score-display {
  font-family: 'Roboto Slab', serif;
  font-size: 18px;
  color: var(--accent-color);
}
</style> 