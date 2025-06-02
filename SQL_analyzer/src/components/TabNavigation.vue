<template>
  <nav class="tab-navigation">
    <button
      v-for="tab in tabs"
      :key="tab"
      @click="appStore.setActiveTab(tab)"
      class="tab-button"
      :class="{ active: appStore.activeTab === tab }"
    >
      {{ tab }}
    </button>
  </nav>
</template>

<script setup>
import { useAppStore } from '../stores/appStore'
import { TABS } from '../utils/constants'

const appStore = useAppStore()
const tabs = TABS
</script>

<style scoped>
.tab-navigation {
  display: flex;
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border);
  padding: 5px;
}

.tab-button {
  padding: 12px 24px;
  border: none;
  background: transparent;
  color: var(--text-primary);
  cursor: pointer;
  font-weight: bold;
  margin: 0 2px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.tab-button.active {
  background: var(--accent);
}

.tab-button:hover:not(.active) {
  background: var(--bg-secondary);
}
</style>
