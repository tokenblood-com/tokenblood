<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { LeaderboardEntry } from '@/types/leaderboard'
import { fetchLeaderboard } from '@/api/leaderboard'

const leaderboard = ref<LeaderboardEntry[]>([])
const isLoading = ref(true)
const error = ref<string | null>(null)
const currentUser = 'maxikadze'

async function loadLeaderboard() {
  try {
    isLoading.value = true
    error.value = null
    leaderboard.value = await fetchLeaderboard()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to load leaderboard'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadLeaderboard()
})
</script>

<template>
  <div class="leaderboard">
    <div v-if="isLoading" class="loading">
      Loading...
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else class="leaderboard-table">
      <div
        v-for="entry in leaderboard"
        :key="entry.username"
        class="table-row"
      >
        <div 
          class="rank-username-container"
          :class="{
            'current-user': entry.username === currentUser,
            'red-border': entry.username !== currentUser
          }"
        >
          <div class="rank">{{ entry.rank }}</div>
          <div class="username">{{ entry.username }}</div>
        </div>
        <div 
          class="score-container"
          :class="{
            'current-user-score': entry.username === currentUser
          }"
        >
          <div class="score">{{ entry.score.toFixed(2) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.leaderboard {
  max-width: 800px;
  margin: 0 auto;
  padding: 32px;
  font-family: 'Roboto Slab', serif;
}

.loading, .error {
  text-align: center;
  padding: 32px;
  color: #fff;
  font-size: 18px;
}

.error {
  color: var(--accent-color);
}

.leaderboard-table {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.table-row {
  display: grid;
  grid-template-columns: 1fr 80px;
  background: var(--background-color);
  border-radius: 10px;
  color: var(--accent-color);
  font-size: 18px;
  align-items: center;
  min-height: 48px;
  overflow: visible;
}

.rank-username-container {
  display: grid;
  grid-template-columns: 48px 1fr;
  align-items: center;
  border-radius: 8px;
  min-height: 48px;
  margin-right: -8px;
}

.red-border {
  border: 2px solid var(--accent-color);
}

.current-user {
  border: 2px solid #ffffff;
  color: #ffffff;
}

.rank {
  font-size: 18px;
  padding-left: 24px;
  font-weight: 600;
}

.username {
  padding-left: 16px;
}

.score-container {
  width: 80px;
  height: 100%;
  display: flex;
  align-items: stretch;
  position: relative;
  z-index: 1;
  border-radius: 0 8px 8px 0;
}

.current-user-score {
  border-top: 2px solid #ffffff;
  border-right: 2px solid #ffffff;
  border-bottom: 2px solid #ffffff;
}

.score {
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent-color);
  color: #fff;
  padding: 0 12px;
  font-weight: 500;
  width: 100%;
  border-radius: 0 8px 8px 0;
}
</style> 