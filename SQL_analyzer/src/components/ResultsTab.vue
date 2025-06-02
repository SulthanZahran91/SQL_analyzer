<template>
  <div class="tab-panel">
    <div class="controls-panel">
      <div class="controls-left">
        <button @click="copyResults" :disabled="!sqlStore.results" class="btn btn-success">
          <i class="fas fa-copy"></i>
          COPY RESULTS
        </button>

        <button @click="exportResults" :disabled="!sqlStore.results" class="btn btn-secondary">
          <i class="fas fa-download"></i>
          EXPORT SQL
        </button>

        <button @click="exportJson" :disabled="!sqlStore.lastResponse" class="btn btn-secondary">
          <i class="fas fa-file-code"></i>
          EXPORT JSON
        </button>
      </div>

      <span class="results-count">
        {{ resultsCountText }}
      </span>
    </div>

    <div class="results-container">
      <div v-if="sqlStore.results" v-html="highlightedResults"></div>
      <div v-else class="no-results">
        No results to display. Process a SQL query to see results here.
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useSqlStore } from '../stores/sqlStore'
import { useLogStore } from '../stores/logStore'
import { highlightSql } from '../utils/sqlHighlighter'
import {
  exportResults as exportFile,
  exportCompleteResults,
  copyToClipboard,
} from '../utils/fileUtils'

const sqlStore = useSqlStore()
const logStore = useLogStore()

const resultsCountText = computed(() =>
  sqlStore.componentsCount > 0
    ? `Found ${sqlStore.componentsCount} components`
    : 'No components found'
)

const highlightedResults = computed(() => (sqlStore.results ? highlightSql(sqlStore.results) : ''))

const copyResults = async () => {
  if (sqlStore.results) {
    const success = await copyToClipboard(sqlStore.results)
    if (success) {
      logStore.info('Results copied to clipboard')
      alert('Results copied to clipboard!')
    } else {
      logStore.error('Failed to copy results to clipboard')
      alert('Failed to copy to clipboard')
    }
  }
}

const exportResults = () => {
  if (sqlStore.results) {
    exportFile(sqlStore.results)
    logStore.info('Results exported to SQL file')
  }
}

const exportJson = () => {
  if (sqlStore.lastResponse) {
    try {
      exportCompleteResults(sqlStore)
      logStore.info('Complete results exported to JSON file')
    } catch (error) {
      logStore.error(`Export failed: ${error.message}`)
      alert(`Export failed: ${error.message}`)
    }
  }
}
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
  justify-content: space-between;
  align-items: center;
}

.controls-left {
  display: flex;
  gap: 15px;
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

.btn-success {
  background: var(--success);
  color: white;
}

.btn-success:hover:not(:disabled) {
  background: #00a854;
}

.btn-secondary {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--accent);
  color: white;
}

.btn:disabled {
  background: var(--border);
  color: var(--text-secondary);
  cursor: not-allowed;
}

.results-count {
  color: var(--text-secondary);
  font-weight: bold;
}

.results-container {
  flex: 1;
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 20px;
  overflow: auto;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 12px;
  color: var(--code-fg);
  line-height: 1.4;
  white-space: pre-wrap;
}

.no-results {
  color: var(--text-secondary);
  text-align: center;
  font-size: 16px;
  margin-top: 50px;
}
</style>
