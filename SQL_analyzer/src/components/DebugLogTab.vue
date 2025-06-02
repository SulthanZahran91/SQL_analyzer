<template>
  <div class="tab-panel">
    <div class="controls-panel">
      <button @click="logStore.clearLogs" class="btn btn-error">
        <i class="fas fa-trash"></i>
        CLEAR LOG
      </button>

      <div class="select-group">
        <label class="log-level-label">LOG LEVEL:</label>
        <select v-model="logStore.logLevel" class="log-level-select">
          <option v-for="level in logLevels" :key="level" :value="level">
            {{ level }}
          </option>
        </select>
      </div>

      <div class="log-stats">
        {{ logStore.filteredLogs.length }} / {{ logStore.logs.length }} entries
      </div>
    </div>

    <div class="log-container" ref="logContainer">
      <div v-if="logStore.filteredLogs.length > 0" class="log-entries">
        <div
          v-for="log in logStore.filteredLogs"
          :key="log.id"
          class="log-entry"
          :class="`log-${log.level.toLowerCase()}`"
        >
          <i :class="getLogIcon(log.level)" class="log-icon"></i>
          <span class="log-timestamp">{{ log.timestamp }}</span>
          <span class="log-level">{{ log.level }}:</span>
          <span class="log-message">{{ log.message }}</span>
        </div>
      </div>
      <div v-else class="no-logs">No log entries to display.</div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { useLogStore } from '../stores/logStore'
import { LOG_LEVELS } from '../utils/constants'

const logStore = useLogStore()
const logContainer = ref(null)
const logLevels = LOG_LEVELS

const getLogIcon = (level) => {
  switch (level) {
    case 'ERROR':
      return 'fas fa-exclamation-circle'
    case 'WARNING':
      return 'fas fa-exclamation-triangle'
    case 'INFO':
      return 'fas fa-info-circle'
    default:
      return 'fas fa-check-circle'
  }
}

// Auto-scroll to bottom when new logs are added
watch(
  () => logStore.logs.length,
  () => {
    nextTick(() => {
      if (logContainer.value) {
        logContainer.value.scrollTop = logContainer.value.scrollHeight
      }
    })
  }
)
</script>

<style scoped>
.tab-panel {
  height: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.controls-panel {
  background: var(--bg-secondary);
  padding: 15px;
  margin-bottom: 20px;
  border-radius: 4px;
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 15px;
  justify-content: space-between;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.btn-error {
  background: var(--error);
  color: white;
}

.btn-error:hover {
  background: #cc0000;
}

.select-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.log-level-label {
  color: var(--text-secondary);
  font-weight: bold;
}

.log-level-select {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border);
  padding: 8px 12px;
  border-radius: 4px;
  font-family: inherit;
}

.log-stats {
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: bold;
}

.log-container {
  flex: 1;
  background: #000000;
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 15px;
  overflow-y: auto;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 11px;
}

.log-entries {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.log-entry {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 2px 0;
  word-wrap: break-word;
}

.log-icon {
  width: 16px;
  flex-shrink: 0;
}

.log-timestamp {
  color: #888;
  font-size: 10px;
  min-width: 80px;
  flex-shrink: 0;
}

.log-level {
  color: #fff;
  font-weight: bold;
  min-width: 60px;
  flex-shrink: 0;
}

.log-message {
  color: #00ff00;
  flex: 1;
}

/* Log level specific colors */
.log-error .log-level,
.log-error .log-icon {
  color: #ff3333;
}

.log-warning .log-level,
.log-warning .log-icon {
  color: #ffa500;
}

.log-info .log-level,
.log-info .log-icon {
  color: #0084ff;
}

.log-debug .log-level,
.log-debug .log-icon {
  color: #00d26a;
}

.no-logs {
  color: #666;
  text-align: center;
  margin-top: 50px;
  font-size: 14px;
}
</style>
