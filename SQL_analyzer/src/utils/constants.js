// src/utils/constants.js
export const SQL_KEYWORDS = [
  'SELECT',
  'FROM',
  'WHERE',
  'INSERT',
  'INTO',
  'VALUES',
  'UPDATE',
  'DELETE',
  'CREATE',
  'TABLE',
  'WITH',
  'AS',
  'DECLARE',
  'INT',
  'VARCHAR',
  'NVARCHAR',
  'DECIMAL',
  'JOIN',
  'LEFT',
  'RIGHT',
  'INNER',
  'OUTER',
  'ON',
  'AND',
  'OR',
  'NOT',
  'IN',
  'EXISTS',
  'UNION',
  'ALL',
  'ORDER',
  'BY',
  'GROUP',
  'HAVING',
  'CASE',
  'WHEN',
  'THEN',
  'ELSE',
  'END',
  'CTE',
  'TEMP',
  'TEMPORARY',
  'CAST',
  'BIGINT',
  'IDENTITY',
  'DEFAULT',
  'NULL',
  'PRIMARY',
  'KEY',
  'FOREIGN',
]

export const THEMES = {
  dark: {
    bgPrimary: '#0a0a0a',
    bgSecondary: '#141414',
    bgTertiary: '#1a1a1a',
    accent: '#0084ff',
    accentHover: '#0066cc',
    textPrimary: '#ffffff',
    textSecondary: '#b0b0b0',
    border: '#2a2a2a',
    success: '#00d26a',
    error: '#ff3333',
    warning: '#ffa500',
    codeBg: '#0d1117',
    codeFg: '#e6e6e6',
  },
  light: {
    bgPrimary: '#ffffff',
    bgSecondary: '#f6f8fa',
    bgTertiary: '#e1e4e8',
    accent: '#0366d6',
    accentHover: '#0256c7',
    textPrimary: '#24292e',
    textSecondary: '#586069',
    border: '#d1d5da',
    success: '#28a745',
    error: '#d73a49',
    warning: '#f66a0a',
    codeBg: '#f6f8fa',
    codeFg: '#24292e',
  },
}

export const LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR']

export const TABS = ['SQL Input', 'Results', 'Statistics', 'Debug Log']
