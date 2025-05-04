<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const navigateToLeaderboard = () => {
  router.push('/leaderboard')
}

const navigateToTasks = () => {
  router.push('/tasks/names_extraction')
}
</script>

<template>
  <div class="app-layout">
    <nav class="nav-bar">
      <div class="nav-left">
        <img src="@/assets/logo.png" alt="TokenBlood Logo" class="logo" />
      </div>
      <div v-if="authStore.isAuthenticated" class="nav-right">
        <button @click="navigateToTasks" class="nav-button">Tasks</button>
        <button @click="navigateToLeaderboard" class="nav-button">Leaderboard</button>
      </div>
    </nav>
    <main class="main-content">
      <slot></slot>
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
  background-color: var(--background-color);
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.nav-bar {
  height: 86px;
  background-color: var(--background-color);
  width: 100%;
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 27px;
}

.nav-left {
  display: flex;
  align-items: center;
}

.nav-right {
  display: flex;
  gap: 16px;
}

.logo {
  height: 40px;
  width: auto;
  filter: brightness(0) saturate(100%) invert(20%) sepia(100%) saturate(10000%) hue-rotate(340deg);
}

.nav-button {
  height: 42px;
  padding: 0 24px;
  background-color: transparent;
  border: none;
  border-radius: 8px;
  color: var(--accent-color);
  font-family: 'Roboto Slab', serif;
  font-size: 20px;
  cursor: pointer;
  transition: color 0.3s ease;
}

.nav-button:hover {
  color: white;
}

.main-content {
  flex: 1;
  background-color: var(--background-color);
  width: 100%;
  overflow: hidden;
  position: relative;
}
</style> 