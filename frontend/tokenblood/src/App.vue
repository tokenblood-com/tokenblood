<script setup lang="ts">
import { RouterView } from 'vue-router'
import AppLayout from './components/layout/AppLayout.vue'
import ErrorNotification from './components/ErrorNotification.vue'
</script>

<template>
  <AppLayout>
    <RouterView />
  </AppLayout>
  <ErrorNotification />
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  background-color: var(--background-color);
  color: white;
}
</style>
