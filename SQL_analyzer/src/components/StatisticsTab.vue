<template>
  <div class="tab-panel statistics-panel">
    <h2>Analysis Statistics</h2>
    <div v-if="sqlStore.statistics && sqlStore.statistics.total > 0">
      <p class="total-components">Total Components Analyzed: <strong>{{ sqlStore.statistics.total }}</strong></p>

      <div class="breakdown-section">
        <h3>Breakdown by Component Type:</h3>
        <ul class="statistics-list">
          <li v-for="(count, type) in sqlStore.statistics.breakdown" :key="type" class="statistic-item">
            <span class="component-type">{{ formatComponentType(type) }}</span>
            <span class="component-count">{{ count }}</span>
          </li>
        </ul>
      </div>

      <div v-if="sqlStore.lastComponents && sqlStore.lastComponents.length > 0" class="component-details-section">
          <h3>Extracted Component Names:</h3>
          <ul class="component-names-list">
            <li v-for="component in sqlStore.lastComponents" :key="component.name + component.type" class="component-name-item">
              <strong>{{ formatComponentType(component.type) }}:</strong> {{ component.name }}
            </li>
          </ul>
      </div>

    </div>
    <div v-else class="no-statistics">
      <p>No statistics to display. Please process a SQL query first on the 'SQL Input' tab.</p>
    </div>
  </div>
</template>

<script setup>
import { useSqlStore } from '../stores/sqlStore';

const sqlStore = useSqlStore();

const formatComponentType = (type) => {
  if (!type) return 'Unknown';
  return type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()); // Capitalize each word
};
</script>

<style scoped>
.tab-panel.statistics-panel {
  padding: 25px;
  color: var(--text-primary);
  background-color: var(--bg-primary);
  height: 100%;
  overflow-y: auto;
}

.statistics-panel h2 {
  color: var(--accent);
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 20px;
  border-bottom: 2px solid var(--accent);
  padding-bottom: 10px;
}

.statistics-panel h3 {
  color: var(--text-primary);
  font-size: 18px;
  margin-top: 25px;
  margin-bottom: 15px;
}

.total-components {
  font-size: 1.1em;
  margin-bottom: 20px;
}

.total-components strong {
  color: var(--accent);
  font-size: 1.2em;
}

.breakdown-section, .component-details-section {
  margin-bottom: 25px;
  padding: 15px;
  background-color: var(--bg-secondary);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--border);
}

.statistics-list, .component-names-list {
  list-style-type: none;
  padding-left: 0;
}

.statistic-item, .component-name-item {
  background-color: var(--bg-tertiary);
  padding: 12px 18px;
  margin-bottom: 10px;
  border-radius: var(--border-radius);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-left: 4px solid var(--accent);
}

.component-type {
  font-weight: 500;
  color: var(--text-secondary);
}

.component-count {
  font-weight: bold;
  font-size: 1.1em;
  background-color: var(--accent);
  color: white; /* Ensure text is visible on accent background */
  padding: 4px 10px;
  border-radius: var(--border-radius);
  min-width: 30px; /* Ensure a minimum width for the count badge */
  text-align: center;
}

.component-name-item strong {
  color: var(--text-secondary);
  margin-right: 8px;
}

.no-statistics {
  text-align: center;
  margin-top: 40px;
  padding: 30px;
  background-color: var(--bg-secondary);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--border);
}

.no-statistics p {
  font-size: 1.1em;
  color: var(--text-secondary);
}
</style>
