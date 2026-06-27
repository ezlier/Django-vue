<script setup lang="ts">
import { useUiStore } from "@/stores/ui"
import { onMounted, ref } from 'vue'
import MarkdownIt from "markdown-it"
import hljs from "highlight.js"
import "highlight.js/styles/github-dark.css"
import { getMessages, createMessage } from '@/api/user'
import CommentSection from '@/components/CommentSection.vue'

const html = ref("")
const messageList = ref<any[]>([])

const uiStore = useUiStore()

const md = new MarkdownIt({
  html: true,
  linkify: true,
  highlight(code: string, lang: string) {
    if (lang && hljs.getLanguage(lang)) {
      return `<pre class="hljs"><code>${hljs.highlight(code, { language: lang }).value}</code></pre>`
    }
    return `<pre class="hljs"><code>${md.utils.escapeHtml(code)}</code></pre>`
  }
})

async function fetchMessages() {
  try {
    const res = await getMessages()
    messageList.value = res.data.data || []
  } catch {
    messageList.value = []
  }
}

async function handleMessage(data: { name: string; text: string; QQ?: string; email?: string }) {
  await createMessage(data as any)
  await fetchMessages()
}

onMounted(async () => {
  await uiStore.fetchWebSetting()
  const mdStr = uiStore.webSetting?.about_md
  if (mdStr) {
    html.value = md.render(mdStr)
  }
  await fetchMessages()
})
</script>

<template>
  <div class="content">
    <div class="about-wrapper" v-html="html"></div>

    <CommentSection title="留言墙" :comments="messageList" @submit="handleMessage" />
  </div>
</template>

<style scoped>
.content {
  width: 100%;
}

.about-wrapper {
  line-height: 1.8;
  color: var(--color-text);
  margin-bottom: 48px;
}

.about-wrapper :deep(h1),
.about-wrapper :deep(h2),
.about-wrapper :deep(h3) {
  color: var(--color-heading);
  margin-top: 24px;
  margin-bottom: 12px;
}

.about-wrapper :deep(p) {
  margin-bottom: 16px;
}

.about-wrapper :deep(pre) {
  border-radius: 8px;
  overflow-x: auto;
}

.about-wrapper :deep(code) {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
}

.about-wrapper :deep(img) {
  max-width: 100%;
  border-radius: 8px;
}

.about-wrapper :deep(blockquote) {
  border-left: 3px solid var(--color-heading);
  padding-left: 16px;
  margin-left: 0;
  color: var(--color-text-mute);
}

.about-wrapper :deep(a) {
  color: var(--color-heading);
  text-decoration: underline;
}
</style>
