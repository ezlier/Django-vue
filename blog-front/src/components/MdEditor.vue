<template>
  <MdEditor v-model="props.modelValue" height="500px" />
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import MarkdownIt from 'markdown-it'
import { MdEditor } from "md-editor-v3"
import "md-editor-v3/lib/style.css"
import hljs from 'highlight.js'

const props = defineProps<{
  modelValue: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const isFullscreen = ref(false)

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  highlight(str: string, lang: string) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value
      } catch { }
    }
    return ''
  },
})

const renderedHtml = computed(() => md.render(props.modelValue || ''))

function insertMarkdown(before: string, after: string) {
  const textarea = document.querySelector('.md-editor__input') as HTMLTextAreaElement | null
  if (!textarea) return
  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const selected = props.modelValue.substring(start, end)
  const newText =
    props.modelValue.substring(0, start) +
    before +
    selected +
    after +
    props.modelValue.substring(end)
  emit('update:modelValue', newText)
  setTimeout(() => {
    textarea.focus()
    const cursor = start + before.length + selected.length
    textarea.setSelectionRange(cursor, cursor)
  }, 0)
}

function toggleFullscreen() {
  isFullscreen.value = !isFullscreen.value
}
</script>

<style scoped>
.md-editor {
  border: 1px solid var(--color-border, #dcdfe6);
  border-radius: 8px;
  overflow: hidden;
  background: var(--color-background, #fff);
  display: flex;
  flex-direction: column;
}

.md-editor--fullscreen {
  position: fixed;
  inset: 0;
  z-index: 9999;
  border-radius: 0;
  border: none;
}

.md-editor__toolbar {
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 6px 10px;
  border-bottom: 1px solid var(--color-border, #dcdfe6);
  background: var(--color-background-mute, #f5f7fa);
  flex-wrap: wrap;
}

.md-editor__toolbar button {
  padding: 4px 10px;
  border: none;
  border-radius: 4px;
  background: transparent;
  color: var(--color-text, #333);
  font-size: 13px;
  cursor: pointer;
  transition: background 0.15s;
}

.md-editor__toolbar button:hover {
  background: var(--color-border, #e0e3e9);
}

.md-editor__sep {
  width: 1px;
  height: 18px;
  background: var(--color-border, #dcdfe6);
  margin: 0 4px;
}

.md-editor__spacer {
  flex: 1;
}

.md-editor__panes {
  display: flex;
  min-height: 480px;
  flex: 1;
}

.md-editor__input,
.md-editor__preview {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.md-editor__input {
  border: none;
  border-right: 1px solid var(--color-border, #dcdfe6);
  resize: none;
  font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
  font-size: 14px;
  line-height: 1.6;
  color: var(--color-text, #333);
  background: var(--color-background, #fff);
  outline: none;
}

.md-editor__preview {
  background: var(--color-background-mute, #fafbfc);
  font-size: 14px;
  line-height: 1.7;
  color: var(--color-text, #333);
}
</style>

<!-- markdown 预览全局样式 (不使用 scoped) -->
<style>
.markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4 {
  margin: 1em 0 0.5em;
  color: var(--color-heading, #1a1a1a);
}

.markdown-body h1 {
  font-size: 1.6em;
  border-bottom: 2px solid var(--color-border, #eee);
  padding-bottom: 6px;
}

.markdown-body h2 {
  font-size: 1.35em;
  border-bottom: 1px solid var(--color-border, #eee);
  padding-bottom: 4px;
}

.markdown-body h3 {
  font-size: 1.15em;
}

.markdown-body p {
  margin: 0.6em 0;
}

.markdown-body pre {
  background: #282c34;
  color: #abb2bf;
  padding: 14px 18px;
  border-radius: 8px;
  overflow-x: auto;
  font-size: 13px;
  line-height: 1.5;
}

.markdown-body code {
  font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
  font-size: 0.9em;
}

.markdown-body :not(pre)>code {
  background: #f0f0f0;
  color: #e74c3c;
  padding: 2px 6px;
  border-radius: 4px;
}

.markdown-body blockquote {
  border-left: 4px solid var(--color-heading, #42b883);
  margin: 0.8em 0;
  padding: 6px 14px;
  color: #666;
  background: #f9f9f9;
}

.markdown-body ul,
.markdown-body ol {
  padding-left: 1.5em;
}

.markdown-body li {
  margin: 0.3em 0;
}

.markdown-body a {
  color: #42b883;
}

.markdown-body img {
  max-width: 100%;
  border-radius: 6px;
}

.markdown-body table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
}

.markdown-body th,
.markdown-body td {
  border: 1px solid var(--color-border, #ddd);
  padding: 8px 12px;
  text-align: left;
}

.markdown-body th {
  background: var(--color-background-mute, #f5f7fa);
  font-weight: 600;
}
</style>
