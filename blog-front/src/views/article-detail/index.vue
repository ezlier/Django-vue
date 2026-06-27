<template>
  <div class="article-detail" v-if="article">
    <!-- 封面 -->
    <div v-if="article.cover" class="article-cover">
      <img :src="article.cover" :alt="article.title" />
    </div>

    <!-- 头部 -->
    <header class="article-header">
      <h1 class="article-title">{{ article.title }}</h1>
      <div class="article-meta">
        <span class="article-date">{{ article.created_time }}</span>
      </div>
    </header>

    <!-- 内容 -->
    <article class="article-body" v-html="html"></article>

    <div class="article-tags" v-if="article.tags?.length">
      <span v-for="tag in article.tags" :key="typeof tag === 'string' ? tag : tag.id" class="article-tag">
        {{ typeof tag === 'string' ? tag : tag.name }}
      </span>
    </div>

    <!-- 评论区 -->
    <CommentSection title="评论" :comments="commentList" @submit="handleComment" />
  </div>

  <div v-else-if="loading" class="article-loading">
    <span class="loading-spinner"></span>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useArticleStore } from '@/stores/article'
import { getComments, createComment } from '@/api/user'
import CommentSection from '@/components/CommentSection.vue'

import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/github-dark.css'

const route = useRoute()
const articleStore = useArticleStore()
const article = ref<any>(null)
const html = ref('')
const loading = ref(true)
const commentList = ref<any[]>([])

const md = new MarkdownIt({
  html: true,
  linkify: true,
  highlight(code: string, lang: string) {
    if (lang && hljs.getLanguage(lang)) {
      return `<pre class="hljs"><code>${hljs.highlight(code, { language: lang }).value}</code></pre>`
    }
    return `<pre class="hljs"><code>${md.utils.escapeHtml(code)}</code></pre>`
  },
})

async function load(slug: string) {
  loading.value = true
  try {
    const data = await articleStore.fetchArticle(slug)
    article.value = data
    html.value = data.content ? md.render(data.content) : ''
    await fetchComments(slug)
  } finally {
    loading.value = false
  }
}

async function fetchComments(slug: string) {
  try {
    const res = await getComments(slug)
    commentList.value = res.data.data || []
  } catch {
    commentList.value = []
  }
}

async function handleComment(data: { name: string; text: string; QQ?: string; email?: string }) {
  const slug = route.params.slug as string
  try {
    await createComment(slug, data as any)
    await fetchComments(slug)
    ElMessage.success('评论成功')
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.msg || '评论失败')
  }
}

// 首次加载
const initialSlug = route.params.slug as string
if (initialSlug) {
  load(initialSlug)
}

// 路由参数变化时重新加载
watch(() => route.params.slug, (newSlug) => {
  if (newSlug) {
    load(newSlug as string)
  }
})
</script>

<style scoped>
.article-detail {
  width: 100%;
}

.article-cover {
  width: 100%;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 24px;
}

.article-cover img {
  width: 100%;
  max-height: 480px;
  object-fit: cover;
}

.article-header {
  margin-bottom: 32px;
}

.article-title {
  font-size: 28px;
  font-weight: 800;
  color: var(--color-heading);
  margin: 0 0 12px;
  line-height: 1.3;
}

.article-meta {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: var(--color-text-mute);
  margin-bottom: 12px;
}

.article-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 32px;
  margin-bottom: 16px;
}

.article-tag {
  padding: 3px 12px;
  font-size: 12px;
  border-radius: 100px;
  background: var(--color-background-mute);
  color: var(--color-text-mute);
}

.article-body {
  line-height: 1.8;
  color: var(--color-text);
  font-size: 16px;
}

.article-loading {
  display: flex;
  justify-content: center;
  padding: 64px 0;
}

.loading-spinner {
  width: 28px;
  height: 28px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-heading);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
