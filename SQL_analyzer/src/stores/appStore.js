import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useAppStore = defineStore('app', () => {
  const theme = ref('dark')
  const activeTab = ref('SQL Input')

  // Persist theme to localStorage
  const savedTheme = localStorage.getItem('sql-analyzer-theme')
  if (savedTheme) {
    theme.value = savedTheme
  }

  watch(theme, (newTheme) => {
    localStorage.setItem('sql-analyzer-theme', newTheme)
  })

  const toggleTheme = () => {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
  }

  const setActiveTab = (tab) => {
    activeTab.value = tab
  }

  return {
    theme,
    activeTab,
    toggleTheme,
    setActiveTab,
  }
})
