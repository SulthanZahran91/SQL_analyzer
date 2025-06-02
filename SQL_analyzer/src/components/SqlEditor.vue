<template>
  <div class="sql-editor-container">
    <div class="line-numbers">
      <div v-for="num in lineNumbers" :key="num">{{ num }}</div>
    </div>
    <textarea
      ref="textarea"
      :value="modelValue"
      @input="handleInput"
      class="sql-textarea"
      placeholder="Enter your SQL query here..."
    ></textarea>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue'])

const textarea = ref(null)

const lineNumbers = computed(() => {
  const lines = props.modelValue.split('\n').length
  return Array.from({ length: lines }, (_, i) => (i + 1).toString().padStart(3))
})

const handleInput = (event) => {
  emit('update:modelValue', event.target.value)
}

// Sync scroll between line numbers and textarea
watch(
  () => props.modelValue,
  () => {
    nextTick(() => {
      if (textarea.value) {
        // Auto-resize textarea if needed
        textarea.value.style.height = 'auto'
        textarea.value.style.height = textarea.value.scrollHeight + 'px'
      }
    })
  }
)
</script>

<style scoped>
.sql-editor-container {
  display: flex;
  border: 1px solid var(--border);
  border-radius: 4px;
  overflow: hidden;
  background: var(--code-bg);
  height: 100%;
  min-height: 300px;
}

.line-numbers {
  background: var(--bg-primary);
  color: var(--text-secondary);
  padding: 8px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 12px;
  min-width: 50px;
  text-align: right;
  border-right: 1px solid var(--border);
  user-select: none;
  line-height: 1.4;
}

.sql-textarea {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  color: var(--code-fg);
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 12px;
  padding: 8px;
  resize: none;
  line-height: 1.4;
  overflow-y: auto;
}

.sql-textarea::placeholder {
  color: var(--text-secondary);
  opacity: 0.7;
}
</style>
