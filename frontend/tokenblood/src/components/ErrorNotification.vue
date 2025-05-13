<template>
  <Transition name="fade">
    <div
      v-if="errorState.isVisible"
      class="error-notification"
      :class="errorState.type"
      @click="hideError"
    >
      <div class="error-content">
        <span class="error-icon" v-if="errorState.type === 'error'">⚠️</span>
        <span class="error-message">{{ errorState.message || 'Internal error' }}</span>
      </div>
      <button class="close-button" @click.stop="hideError">×</button>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { useErrorStore } from '@/stores/errorStore'

const { errorState, hideError } = useErrorStore()
</script>

<style scoped>
.error-notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  min-width: 300px;
  max-width: 400px;
  padding: 16px;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  z-index: 9999;
  cursor: pointer;
  border-left: 4px solid #ff4d4f;
}

.error-content {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.error-icon {
  font-size: 18px;
}

.error-message {
  color: #333;
  font-size: 14px;
  line-height: 1.5;
}

.close-button {
  background: none;
  border: none;
  font-size: 20px;
  color: #999;
  cursor: pointer;
  padding: 0 4px;
  line-height: 1;
}

.close-button:hover {
  color: #666;
}

/* Transition animations */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style> 