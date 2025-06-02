import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useLogStore = defineStore('log', () => {
  const logs = ref([])
  const logLevel = ref('DEBUG')

  const addLog = (level, message) => {
    const timestamp = new Date().toLocaleTimeString()
    const newLog = {
      id: Date.now() + Math.random(), // Ensure unique IDs
      timestamp,
      level,
      message,
    }
    logs.value.push(newLog)

    // Keep only last 1000 logs to prevent memory issues
    if (logs.value.length > 1000) {
      logs.value = logs.value.slice(-1000)
    }
  }

  const clearLogs = () => {
    logs.value = []
  }

  const setLogLevel = (level) => {
    logLevel.value = level
  }

  const filteredLogs = computed(() => {
    const levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
    const currentLevelIndex = levels.indexOf(logLevel.value)
    return logs.value.filter((log) => {
      const logLevelIndex = levels.indexOf(log.level)
      return logLevelIndex >= currentLevelIndex
    })
  })

  // Convenience methods
  const debug = (message) => addLog('DEBUG', message)
  const info = (message) => addLog('INFO', message)
  const warning = (message) => addLog('WARNING', message)
  const error = (message) => addLog('ERROR', message)

  return {
    logs,
    logLevel,
    filteredLogs,
    addLog,
    clearLogs,
    setLogLevel,
    debug,
    info,
    warning,
    error,
  }
})
