<template>
  <div class="article-detail" v-if="article">
    <!-- 头部 -->
    <header class="article-header">
      <div class="article-title">{{ article.title }}</div>
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
    <CommentSection title="评论" :comments="commentList" :on-submit="handleComment" />
  </div>

  <div v-else-if="loading" class="article-loading">
    <span class="loading-spinner"></span>
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: 'ArticleDetail' })

import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
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
  typographer: true,
  highlight: function (str, lang) {
    let html = ''
    const linesLength = str.split(/\n/).length - 1
    // 生成行号
    let linesNum = '<span aria-hidden="true" class="line-numbers-rows">'
    for (let index = 0; index < linesLength; index++) {
      linesNum = linesNum + '<span></span>'
    }
    linesNum += '</span>'
    if (lang && hljs.getLanguage(lang)) {
      try {
        // highlight.js 高亮代码
        const preCode = hljs.highlight(lang, str, true).value
        html = html + preCode

        // 返回高亮后的代码
        return `<pre class="hljs"><code>${html}</code>${linesNum}</pre>`
      } catch (error) {
        console.log(error)
      }
    }

    const preCode = md.utils.escapeHtml(str)
    html = html + preCode
    // 返回高亮后的代码
    return `<pre class="hljs"><code>${html}</code>${linesNum}</pre>`
  }

})

let h1Index = 0
md.renderer.rules.heading_open = function (tokens: any[], idx: number) {
  const token = tokens[idx]
  if (token.tag === 'h1') {
    h1Index++
    return `<h1><span class="h1-number">${h1Index}</span><span class="h1-text">`
  }
  return `<${token.tag}>`
}

md.renderer.rules.heading_close = function (tokens: any[], idx: number) {
  const token = tokens[idx]
  if (token.tag === 'h1') {
    return '</span></h1>'
  }
  return `</${token.tag}>`
}

async function load(slug: string) {
  loading.value = true
  h1Index = 0
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
  await createComment(slug, data as any)
  await fetchComments(slug)
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
  overflow-wrap: break-word;
  word-wrap: break-word;
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
  font-family: "LXGWWenKai";
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

::v-deep .markdown-body {
  font-family: 文楷;
}

::v-deep .markdown-body h1 {
  text-decoration: none !important;
}

::v-deep .h1-number {
  color: var(--text-color);
  font-size: 60px;
  text-decoration: none !important;
  margin-right: 20px;
  font-style: italic;
}

::v-deep .h1-text {
  color: var(--text-color);
  font-size: 20px;
  text-decoration: underline;
  text-underline-offset: 4px;
}

::v-deep .markdown-body img {
  width: 100%;
}

::v-deep .markdown-body code {
  background-color: #2c2c2e;
  padding: 0 5px;
  border-radius: 6px;
  display: inline-flex;
  color: whitesmoke;
}

/* 代码块样式 */
::v-deep pre.hljs {
  padding: 12px 2px 12px 40px !important;
  border-radius: 5px !important;
  position: relative;
  font-size: 14px !important;
  line-height: 22px !important;
  overflow: hidden !important;

  code {
    display: block !important;
    margin: 0 10px !important;
    overflow-x: auto !important;
  }

  .line-numbers-rows {
    padding-top: 10px !important;

    position: absolute;
    pointer-events: none;
    top: 12px;
    bottom: 12px;
    left: 0;
    font-size: 100%;
    width: 40px;
    text-align: center;
    letter-spacing: -1px;
    border-right: 1px solid rgba(0, 0, 0, .66);
    user-select: none;
    counter-reset: linenumber;

    span {
      line-height: 1.583;
      font-size: 1em !important;
      pointer-events: none;
      display: block;
      counter-increment: linenumber;

      &:before {
        content: counter(linenumber);
        color: #999;
        display: block;
        text-align: center;
      }
    }
  }

  b.name {
    position: absolute;
    top: 2px;
    right: 50px;
    z-index: 10;
    color: #999;
    pointer-events: none;
  }

  .copy-btn {
    position: absolute;
    top: 2px;
    right: 4px;
    z-index: 10;
    color: #333;
    cursor: pointer;
    background-color: #fff;
    border: 0;
    border-radius: 2px;
  }
}



::v-deep .article-body pre {
  position: relative;
  background-color: #272822;
  /* color: #d4d4d4; */
  border-radius: 8px;
  padding-top: 16px;
  /* 预留顶部空间放语言标签和圆点 */
  overflow-x: auto;
  font-size: 0.9em;
  line-height: 1.6;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 顶部语言标签 */
::v-deep .article-body pre::before {
  content: attr(data-lang);
  position: absolute;
  top: 3px;
  left: 100px;
  font-size: 1em;
  color: #272822;
  font-family: sans-serif;
}

::v-deep .article-body pre::after {
  content: "● ● ●";
  position: absolute;
  top: 6px;
  left: 10px;
  font-size: 1em;
  letter-spacing: 2px;
  background: linear-gradient(90deg, #f6f6f6 0, #ffe2e2 33%, #ffc7c7 66%);
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* 内部代码文本 */
::v-deep .article-body pre code {
  background: none !important;
  padding-top: 10px;
  font-family: "Fira Code", Consolas, monospace;
  font-size: 1em;
  display: block;
  white-space: pre;
  margin: 0 !important;
}

/* 代码块内注释样式 */
::v-deep .article-body pre code .hljs-comment {
  font-family: "LXGW WenKai Mono", "Source Han Serif SC", "SimSun", monospace;
  color: #7d7d7d;
  font-size: 1em;
  opacity: 0.9;
  font-style: normal !important;
}

/* ---------- 表格整体样式 ---------- */
::v-deep .article-body table {
  width: 100%;
  overflow-x: auto;
  border-collapse: collapse;
  margin: 20px 0;
  font-size: 0.95em;
  background-color: var(--bg-color);
  border-radius: 6px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

/* 表头 */
::v-deep .article-body thead {
  background-color: #fcbad3;
  color: #333;
  text-align: left;
  font-weight: bold;
}

/* 单元格 */
::v-deep .article-body th,
::v-deep .article-body td {
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  line-height: 1.6;
}



/* hover 高亮 */
::v-deep .article-body tbody tr:hover {
  background-color: rgba(142, 140, 216, 0.1);
  transition: background 0.2s ease;
}

/* 单元格内代码 */
::v-deep .article-body td code {
  background: rgba(175, 184, 193, 0.15);
  padding: 2px 4px;
  border-radius: 3px;
  color: #e83e8c;
  font-size: 0.85em;
}

/* ---------- 暗色模式适配 ---------- */
::v-deep .dark .article-body table {
  background-color: #1e1e1e;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
}

::v-deep .dark .article-body thead {
  background-color: #333;
  color: #fcbad3;
}

::v-deep .dark .article-body th,
::v-deep .dark .article-body td {
  border: 1px solid #444;
  color: #ddd;
}

::v-deep .dark .article-body tbody tr:nth-child(even) {
  background-color: #2a2a2a;
}

::v-deep .dark .article-body tbody tr:hover {
  background-color: rgba(142, 140, 216, 0.2);
}

::v-deep .dark .article-body td code {
  background: rgba(255, 255, 255, 0.1);
  color: #ff99cc;
}


.text-nofound {
  width: fit-content;
  height: fit-content;
  display: flex;

  margin-top: 2rem;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.wrapper {
  width: fit-content;
  height: fit-content;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.catContainer {
  width: 100%;
  height: fit-content;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.catbody {
  width: 80px;
}

.tail {
  position: absolute;
  width: 17px;
  top: 50%;
  animation: tail 0.5s ease-in infinite alternate-reverse;
  transform-origin: top;
}

@keyframes tail {
  0% {
    transform: rotateZ(60deg);
  }

  50% {
    transform: rotateZ(0deg);
  }

  100% {
    transform: rotateZ(-20deg);
  }
}

.wall {
  width: 300px;
}

.text1 {
  display: flex;
  flex-direction: column;
  width: 50px;
  position: absolute;
  margin: 0px 0px 100px 120px;
}

.zzz {
  color: black;
  font-weight: 700;
  font-size: 15px;
  animation: zzz 2s linear infinite;
}

.bigzzz {
  color: black;
  font-weight: 700;
  font-size: 25px;
  margin-left: 10px;
  animation: zzz 2.3s linear infinite;
}

@keyframes zzz {
  0% {
    color: transparent;
  }

  50% {
    color: black;
  }

  100% {
    color: transparent;
  }
}

@media (max-width: 768px) {
  ::v-deep .article-body table {
    display: block;
    font-size: 0.85em;
  }
}
</style>
