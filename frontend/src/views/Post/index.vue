<script lang="js" setup>
import { ref, onMounted, nextTick } from "vue"
import { useRoute } from "vue-router"
import { getArticle } from "@/utils/article"
import hljs from "highlight.js"
import "highlight.js/styles/github-dark.css"
import { bus } from "@/utils/eventBus"

const route = useRoute()
const article = ref(null)

onMounted(async () => {
  const slug = route.params.slug
  const res = await getArticle(slug)
  article.value = res.data

  await nextTick()
  bus.emit("article-loaded")
  document.querySelectorAll("pre code").forEach((block) => {
    hljs.highlightElement(block)
  })
})
</script>

<template>
  <div class="post-rightcolumn">
    <div v-if="article" class="article-page">
      <el-tag effect="plain">
        <span>{{ article.date }}</span> |
        <span>{{ article.tags }}</span>
      </el-tag>
      <div class="markdown-body" v-html="article.content"></div>
    </div>

    <div v-else class="loading">正在加载文章...</div>
  </div>
</template>

<style>
.post-rightcolumn {
  border-color: rgba(0, 0, 0, 0.175);
  background-color: #fff;
  flex: 1;
  padding: 10px;
  min-width: 0;
  width: 100%;
  border-radius: 8px;
  /* box-shadow: 2px 2px 5px #000; */
}

.article-page {
  /* max-width: 800px; */

  padding-left: 2rem;
  padding-right: 2rem;
  color: black;
  line-height: 1.8;
}

.cover {
  width: 100%;
  border-radius: 10px;
  margin: 1rem 0;
}

.loading {
  color: #aaa;
  text-align: center;
  margin-top: 2rem;
}

/* 代码块样式 */
.markdown-body pre {
  position: relative;
  background-color: #272822;
  /* color: #d4d4d4; */
  border-radius: 8px;
  padding-top: 32px;
  /* 预留顶部空间放语言标签和圆点 */
  padding: 16px;
  overflow-x: auto;
  margin: 20px 0;
  font-size: 0.9em;
  line-height: 1.6;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 顶部语言标签 */
.markdown-body pre::before {
  content: attr(data-lang);
  position: absolute;
  top: 3px;
  left: 100px;
  font-size: 1em;
  color: #272822;
  font-family: sans-serif;
}

.markdown-body pre::after {
  content: "● ● ●";
  position: absolute;
  top: 6px;
  left: 10px;
  font-size: 1em;
  letter-spacing: 2px;
  background: linear-gradient(90deg, #FFCCCC 0, #FFFF99 33%, #CCCCFF 66%);
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* 内部代码文本 */
.markdown-body pre code {
  background: none !important;
  padding-top: 10px;
  font-family: "Fira Code", Consolas, monospace;
  font-size: 1em;
  display: block;
  white-space: pre;
}

/* 代码块内注释样式 */
.markdown-body pre code .hljs-comment {
  font-family: "LXGW WenKai Mono", "Source Han Serif SC", "SimSun", monospace;
  color: #7d7d7d;
  font-size: 1em;
  opacity: 0.9;
  font-style: normal !important;
}

/* ---------- 表格整体样式 ---------- */
.markdown-body table {
  display: block;
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
.markdown-body thead {
  background-color: #fcbad3;
  color: #333;
  text-align: left;
  font-weight: bold;
}

/* 单元格 */
.markdown-body th,
.markdown-body td {
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  line-height: 1.6;
}

/* 隔行换色 */
.markdown-body tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

/* hover 高亮 */
.markdown-body tbody tr:hover {
  background-color: rgba(142, 140, 216, 0.1);
  transition: background 0.2s ease;
}

/* 单元格内代码 */
.markdown-body td code {
  background: rgba(175, 184, 193, 0.15);
  padding: 2px 4px;
  border-radius: 3px;
  color: #e83e8c;
  font-size: 0.85em;
}

/* ---------- 暗色模式适配 ---------- */
.dark .markdown-body table {
  background-color: #1e1e1e;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
}

.dark .markdown-body thead {
  background-color: #333;
  color: #fcbad3;
}

.dark .markdown-body th,
.dark .markdown-body td {
  border: 1px solid #444;
  color: #ddd;
}

.dark .markdown-body tbody tr:nth-child(even) {
  background-color: #2a2a2a;
}

.dark .markdown-body tbody tr:hover {
  background-color: rgba(142, 140, 216, 0.2);
}

.dark .markdown-body td code {
  background: rgba(255, 255, 255, 0.1);
  color: #ff99cc;
}

@media (max-width: 1000px) {
  .post-leftcolumn {
    display: none;
  }
}

@media (max-width: 768px) {
  .markdown-body table {
    font-size: 0.85em;
  }
}
</style>