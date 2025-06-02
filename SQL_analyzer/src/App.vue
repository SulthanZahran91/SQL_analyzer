<template>
  <div class="sql-analyzer" :class="`theme-${appStore.theme}`">
    <AppHeader />
    <TabNavigation />

    <div class="tab-content">
      <SqlInputTab v-if="appStore.activeTab === 'SQL Input'" />
      <ResultsTab v-if="appStore.activeTab === 'Results'" />
      <StatisticsTab v-if="appStore.activeTab === 'Statistics'" />
      <DebugLogTab v-if="appStore.activeTab === 'Debug Log'" />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import AppHeader from './components/AppHeader.vue'
import TabNavigation from './components/TabNavigation.vue'
import SqlInputTab from './components/SqlInputTab.vue'
import ResultsTab from './components/ResultsTab.vue'
import StatisticsTab from './components/StatisticsTab.vue'
import DebugLogTab from './components/DebugLogTab.vue'
import { useAppStore } from './stores/appStore'
import { useLogStore } from './stores/logStore'

const appStore = useAppStore()
const logStore = useLogStore()

onMounted(() => {
  logStore.info('SQL Analyzer initialized successfully')
  logStore.debug('All components and stores loaded')
})
</script>

<style scoped>
.sql-analyzer {
  height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.tab-content {
  flex: 1;
  overflow: hidden;
  background: var(--bg-secondary);
}
</style>
