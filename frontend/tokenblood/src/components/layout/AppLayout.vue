<template>
  <div class="app-layout">
    <nav class="nav-bar">
      <!-- Navigation content will be added later -->
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
  height: 60px;
  background-color: var(--background-color);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  width: 100%;
  flex-shrink: 0;
}

.main-content {
  flex: 1;
  background-color: var(--background-color);
  width: 100%;
  overflow: hidden;
  position: relative;
}
</style> 