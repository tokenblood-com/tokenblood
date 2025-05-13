<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const username = ref('')
const email = ref('')
const errors = ref<{ username?: string; email?: string }>({})

const validateEmail = (email: string) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

const validateForm = () => {
  errors.value = {}
  if (!username.value) {
    errors.value.username = 'Username is required'
  }
  if (!email.value) {
    errors.value.email = 'Email is required'
  } else if (!validateEmail(email.value)) {
    errors.value.email = 'Invalid email format'
  }
  return Object.keys(errors.value).length === 0
}

const handleSubmit = async () => {
  if (!validateForm()) return
  
  const user = await authStore.auth({
    username: username.value,
    email: email.value
  })
  
  if (user) {
    await router.push('/tasks/names_extraction')
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="login-form">
    <div class="input-group">
      <input
        v-model="username"
        type="text"
        placeholder="username"
        :disabled="authStore.isLoading"
        class="auth-input"
      />
      <span v-if="errors.username" class="error">{{ errors.username }}</span>
    </div>
    
    <div class="input-group">
      <input
        v-model="email"
        type="email"
        placeholder="e-mail"
        :disabled="authStore.isLoading"
        class="auth-input"
      />
      <span v-if="errors.email" class="error">{{ errors.email }}</span>
    </div>
    
    <button type="submit" :disabled="authStore.isLoading" class="auth-button">
      {{ authStore.isLoading ? 'Loading...' : 'Enter' }}
    </button>
  </form>
</template>

<style scoped>
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 350px;
  align-items: center;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: 100%;
}

.auth-input {
  width: 100%;
  height: 50px;
  padding: 0 10px;
  background: transparent;
  border: 2px solid var(--accent-color);
  border-radius: 10px;
  color: white;
  font-family: 'Roboto Slab', serif;
  font-size: 18px;
}

.auth-input:focus {
  outline: none;
  border-color: var(--accent-color);
  box-shadow: 0 0 0 2px rgba(220, 20, 60, 0.2);
}

.auth-button {
  width: fit-content;
  min-width: 100px;
  height: 42px;
  padding: 0 20px;
  background: var(--accent-color);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: opacity 0.3s;
  font-family: 'Roboto Slab', serif;
  font-size: 18px;
}

.auth-button:hover:not(:disabled) {
  opacity: 0.9;
}

.auth-button:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

.error {
  color: var(--accent-color);
  font-size: 12px;
}
</style> 