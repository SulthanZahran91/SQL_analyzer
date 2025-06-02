// src/utils/sqlHighlighter.js
import { SQL_KEYWORDS } from './constants'

export const highlightSql = (code) => {
  if (!code) return ''

  let highlighted = code

  // Highlight keywords
  SQL_KEYWORDS.forEach((keyword) => {
    const regex = new RegExp(`\\b${keyword}\\b`, 'gi')
    highlighted = highlighted.replace(regex, `<span class="sql-keyword">${keyword}</span>`)
  })

  // Highlight strings
  highlighted = highlighted.replace(/'[^']*'/g, '<span class="sql-string">$&</span>')

  // Highlight numbers
  highlighted = highlighted.replace(/\b\d+\b/g, '<span class="sql-number">$&</span>')

  // Highlight comments
  highlighted = highlighted.replace(/--.*$/gm, '<span class="sql-comment">$&</span>')
  highlighted = highlighted.replace(/\/\*[\s\S]*?\*\//g, '<span class="sql-comment">$&</span>')

  // Highlight variables (@variable and #temp)
  highlighted = highlighted.replace(/[@#]\w+/g, '<span class="sql-variable">$&</span>')

  return highlighted
}

export const getSqlTokens = (code) => {
  // Implementation for more advanced syntax analysis
  const tokens = []
  const lines = code.split('\n')

  lines.forEach((line, lineNumber) => {
    const words = line.split(/\s+/)
    words.forEach((word, wordIndex) => {
      if (SQL_KEYWORDS.includes(word.toUpperCase())) {
        tokens.push({
          type: 'keyword',
          value: word,
          line: lineNumber,
          column: wordIndex,
        })
      }
    })
  })

  return tokens
}
  