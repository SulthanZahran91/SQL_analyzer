<template>
  <div class="tab-panel">
    <div class="controls-panel">
      <button @click="handleProcess" :disabled="sqlStore.isProcessing" class="btn btn-primary">
        <i class="fas fa-play"></i>
        {{ sqlStore.isProcessing ? 'PROCESSING...' : 'PROCESS SQL' }}
      </button>

      <button @click="clearInput" class="btn btn-secondary">
        <i class="fas fa-undo"></i>
        CLEAR
      </button>

      <label class="btn btn-secondary file-label">
        <i class="fas fa-upload"></i>
        LOAD FILE
        <input type="file" accept=".sql,.txt" @change="handleFileLoad" class="file-input" />
      </label>

      <div class="separator"></div>

      <div class="checkbox-group">
        <input type="checkbox" id="subqueries" v-model="sqlStore.includeSubqueries" />
        <label for="subqueries">Extract Subqueries</label>
      </div>
    </div>

    <SqlEditor v-model="sqlStore.sqlInput" />
  </div>
</template>

<script setup>
import SqlEditor from './SqlEditor.vue'
import { useSqlStore } from '../stores/sqlStore'
import { useAppStore } from '../stores/appStore'
import { useLogStore } from '../stores/logStore'
import { loadSqlFile } from '../utils/fileUtils'

const sqlStore = useSqlStore()
const appStore = useAppStore()
const logStore = useLogStore()

const handleProcess = async () => {
  try {
    logStore.info('Starting SQL processing...')
    await sqlStore.processSql()
    logStore.info(`Processing complete. Found ${sqlStore.componentsCount} components.`)
    appStore.setActiveTab('Results')
  } catch (error) {
    logStore.error(`Processing failed: ${error.message}`)
    alert(error.message)
  }
}

const clearInput = () => {
  sqlStore.clearInput()
  logStore.info('SQL input cleared')
}

const formatSql = () => {
  if (!sqlStore.sqlInput.trim()) {
    alert('Please enter SQL to format')
    return
  }

  // Basic SQL formatting
  let formatted = sqlStore.sqlInput
    .replace(/\bSELECT\b/gi, '\nSELECT')
    .replace(/\bFROM\b/gi, '\nFROM')
    .replace(/\bWHERE\b/gi, '\nWHERE')
    .replace(/\bJOIN\b/gi, '\nJOIN')
    .replace(/\bLEFT JOIN\b/gi, '\nLEFT JOIN')
    .replace(/\bRIGHT JOIN\b/gi, '\nRIGHT JOIN')
    .replace(/\bINNER JOIN\b/gi, '\nINNER JOIN')
    .replace(/\bGROUP BY\b/gi, '\nGROUP BY')
    .replace(/\bORDER BY\b/gi, '\nORDER BY')
    .replace(/\bHAVING\b/gi, '\nHAVING')
    .replace(/\bAND\b/gi, '\n    AND')
    .replace(/\bOR\b/gi, '\n    OR')
    .replace(/,/g, ',\n    ')
    .replace(/\n\s*\n/g, '\n') // Remove double newlines
    .trim()

  sqlStore.sqlInput = formatted
  logStore.info('SQL formatted successfully')
}

const handleFileLoad = async (event) => {
  const file = event.target.files[0]
  if (file) {
    try {
      // Use the store's upload method which calls the API
      await sqlStore.uploadFile(file)
      logStore.info(`Loaded SQL file: ${file.name}`)
    } catch (error) {
      logStore.error(`Failed to load file: ${error.message}`)
      alert(`Failed to load file: ${error.message}`)
    }
    // Clear the input so the same file can be selected again
    event.target.value = ''
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
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
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

.btn-primary {
  background: var(--accent);
  color: white;
}

.btn-primary:hover {
  background: var(--accent-hover);
}

.btn-primary:disabled {
  background: var(--border);
  cursor: not-allowed;
}

.btn-secondary {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border);
}

.btn-secondary:hover {
  background: var(--accent);
  color: white;
}

.file-input {
  display: none;
}

.separator {
  width: 2px;
  background: var(--border);
  height: 40px;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.checkbox-group input[type='checkbox'] {
  width: 18px;
  height: 18px;
}

.checkbox-group label {
  color: var(--text-primary);
  font-weight: bold;
}
</style>
