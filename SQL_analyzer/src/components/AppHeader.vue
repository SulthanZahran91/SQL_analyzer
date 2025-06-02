<template>
  <header class="app-header">
    <h1 class="app-title">SQL QUERY ANALYZER</h1>
    <button @click="appStore.toggleTheme" class="theme-toggle">
      <i :class="themeIcon"></i>
      {{ themeText }}
    </button>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useAppStore } from '../stores/appStore'

const appStore = useAppStore()

const themeIcon = computed(() => (appStore.theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon'))

const themeText = computed(() => (appStore.theme === 'dark' ? 'Light Mode' : 'Dark Mode'))
</script>

<style scoped>
.app-header {
  height: 70px;
  background: var(--bg-primary);
  border-bottom: 2px solid var(--accent);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px;
}

.app-title {
  color: var(--accent);
  font-size: 28px;
  font-weight: bold;
}

.theme-toggle {
  background: none;
  border: 1px solid var(--border);
  color: var(--text-primary);
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.2s;
}

.theme-toggle:hover {
  background: var(--bg-secondary);
}
</style>
