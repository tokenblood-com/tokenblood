<template>
  <div class="app-layout">
    <nav class="nav-bar">
      <img src="@/assets/logo.png" alt="TokenBlood Logo" class="logo" />
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
  align-items: flex-start;
  padding: 20px 0 0 27px;
}

.logo {
  height: 40px;
  width: auto;
  filter: brightness(0) saturate(100%) invert(20%) sepia(100%) saturate(10000%) hue-rotate(340deg);
}

.main-content {
  flex: 1;
  background-color: var(--background-color);
  width: 100%;
  overflow: hidden;
  position: relative;
}
</style> 