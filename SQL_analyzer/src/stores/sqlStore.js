// src/stores/sqlStore.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

// API configuration
const API_BASE_URL = 'http://localhost:8000'

export const useSqlStore = defineStore('sql', () => {
  const sqlInput = ref('')
  const includeSubqueries = ref(false)
  const isProcessing = ref(false)
  const results = ref('')
  const statistics = ref(null)
  const componentsCount = ref(0)
  const lastComponents = ref([])
  const lastResponse = ref(null)

  // API helper function
  const apiCall = async (endpoint, options = {}) => {
    const url = `${API_BASE_URL}${endpoint}`
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
      },
    }

    const response = await fetch(url, { ...defaultOptions, ...options })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Network error' }))
      throw new Error(errorData.detail || errorData.error || `HTTP ${response.status}`)
    }

    return response.json()
  }

  const processSql = async () => {
    if (!sqlInput.value.trim()) {
      throw new Error('Please enter a SQL query.')
    }

    isProcessing.value = true

    try {
      const requestData = {
        sql_query: sqlInput.value,
        include_subqueries: includeSubqueries.value,
      }

      const response = await apiCall('/api/sql/process', {
        method: 'POST',
        body: JSON.stringify(requestData),
      })

      lastResponse.value = response

      if (response.success) {
        lastComponents.value = response.components
        results.value = response.formatted_results
        statistics.value = response.statistics
        componentsCount.value = response.statistics.total
      } else {
        // Handle API error response
        throw new Error(response.message || 'Processing failed')
      }
    } catch (error) {
      console.error('Processing error:', error)

      // Clear previous results on error
      lastComponents.value = []
      results.value = ''
      statistics.value = { total: 0, breakdown: {} }
      componentsCount.value = 0

      throw error
    } finally {
      isProcessing.value = false
    }
  }

  const validateSql = async () => {
    if (!sqlInput.value.trim()) {
      return { valid: false, error: 'SQL query cannot be empty' }
    }

    try {
      const requestData = {
        sql_query: sqlInput.value,
        include_subqueries: includeSubqueries.value,
      }

      const response = await apiCall('/api/sql/validate', {
        method: 'POST',
        body: JSON.stringify(requestData),
      })

      return response
    } catch (error) {
      console.error('Validation error:', error)
      return { valid: false, error: error.message }
    }
  }

  const loadExamples = async () => {
    try {
      const response = await apiCall('/api/sql/examples')
      return response.examples || []
    } catch (error) {
      console.error('Failed to load examples:', error)
      return []
    }
  }

  const uploadFile = async (file) => {
    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(`${API_BASE_URL}/api/sql/upload`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: 'Upload failed' }))
        throw new Error(errorData.detail || errorData.error || `HTTP ${response.status}`)
      }

      const result = await response.json()

      // Set the uploaded content as the SQL input
      if (result.content) {
        sqlInput.value = result.content
      }

      return result
    } catch (error) {
      console.error('Upload error:', error)
      throw error
    }
  }

  const clearInput = () => {
    sqlInput.value = ''
  }

  const clearResults = () => {
    results.value = ''
    statistics.value = null
    componentsCount.value = 0
    lastComponents.value = []
    lastResponse.value = null
  }

  const clearAll = () => {
    clearInput()
    clearResults()
  }

  // Health check function
  const checkApiHealth = async () => {
    try {
      const response = await apiCall('/health')
      return response
    } catch (error) {
      console.error('API health check failed:', error)
      return { status: 'unhealthy', error: error.message }
    }
  }

  return {
    sqlInput,
    includeSubqueries,
    isProcessing,
    results,
    statistics,
    componentsCount,
    lastComponents,
    lastResponse,
    processSql,
    validateSql,
    loadExamples,
    uploadFile,
    clearInput,
    clearResults,
    clearAll,
    checkApiHealth,
  }
})
