<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
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
  if (email.value && !validateEmail(email.value)) {
    errors.value.email = 'Invalid email format'
  }
  return Object.keys(errors.value).length === 0
}

const handleSubmit = async () => {
  if (!validateForm()) return
  
  await authStore.auth({
    username: username.value,
    email: email.value || undefined
  })
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
      />
      <span v-if="errors.username" class="error">{{ errors.username }}</span>
    </div>
    
    <div class="input-group">
      <input
        v-model="email"
        type="email"
        placeholder="(optional) e-mail"
        :disabled="authStore.isLoading"
      />
      <span v-if="errors.email" class="error">{{ errors.email }}</span>
    </div>
    
    <button type="submit" :disabled="authStore.isLoading">
      {{ authStore.isLoading ? 'Loading...' : 'Enter' }}
    </button>
  </form>
</template>

<style scoped>
.login-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 300px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

input {
  width: 100%;
  height: 50px;
  padding: 0 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 100px;
  height: 42px;
  align-self: center;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

.error {
  color: red;
  font-size: 12px;
}
</style> 