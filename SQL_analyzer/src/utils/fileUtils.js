// src/utils/fileUtils.js
export const loadSqlFile = (file) => {
  return new Promise((resolve, reject) => {
    if (!file) {
      reject(new Error('No file provided'))
      return
    }

    const reader = new FileReader()

    reader.onload = (event) => {
      resolve(event.target.result)
    }

    reader.onerror = () => {
      reject(new Error('Failed to read file'))
    }

    reader.readAsText(file)
  })
}

export const loadSqlFileViaApi = async (file) => {
  const API_BASE_URL = 'http://localhost:8000'

  if (!file) {
    throw new Error('No file provided')
  }

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
  return result.content
}

export const exportResults = (content, filename = 'sql_analysis_results.sql') => {
  const blob = new Blob([content], { type: 'text/sql' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}

export const exportAsJson = (data, filename = 'sql_analysis_results.json') => {
  const jsonString = JSON.stringify(data, null, 2)
  const blob = new Blob([jsonString], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}

export const exportCompleteResults = (sqlStore, filename = 'sql_analysis_complete') => {
  if (!sqlStore.lastResponse) {
    throw new Error('No results to export')
  }

  const timestamp = new Date().toISOString()
  const exportData = {
    timestamp,
    sql_query: sqlStore.sqlInput,
    include_subqueries: sqlStore.includeSubqueries,
    results: sqlStore.lastResponse,
    summary: {
      total_components: sqlStore.componentsCount,
      component_types: Object.keys(sqlStore.statistics?.breakdown || {}),
    },
  }

  exportAsJson(exportData, `${filename}.json`)
}

export const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch (error) {
    console.error('Failed to copy to clipboard:', error)
    // Fallback for older browsers
    try {
      const textArea = document.createElement('textarea')
      textArea.value = text
      textArea.style.position = 'fixed'
      textArea.style.opacity = '0'
      document.body.appendChild(textArea)
      textArea.focus()
      textArea.select()
      const result = document.execCommand('copy')
      document.body.removeChild(textArea)
      return result
    } catch (fallbackError) {
      console.error('Fallback copy failed:', fallbackError)
      return false
    }
  }
}
