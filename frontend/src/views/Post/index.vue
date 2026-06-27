<script lang="js" setup>
import { ref, onMounted, nextTick } from "vue"
import { useRoute } from "vue-router"
import { getArticle } from "@/utils/article"
import hljs from "highlight.js"
import "highlight.js/styles/github-dark.css"
import { bus } from "@/utils/eventBus"
import comment from "./components/comment.vue"
import MarkdownIt from "markdown-it"
import { watch } from "vue"
import ArticleToc from "@/components/ArticleToc.vue"

const html = ref("")

const notFound = ref(false)

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

let h1Index = 0;
md.renderer.rules.heading_open = function (tokens, idx) {
  const token = tokens[idx];
  if (token.tag === 'h1') {
    h1Index++;
    return `<h1><span class="h1-number">${h1Index}</span><span class="h1-text">`;
  }
  return `<${token.tag}>`;
};

md.renderer.rules.heading_close = function (tokens, idx) {
  const token = tokens[idx];
  if (token.tag === 'h1') {
    return '</span></h1>';
  }
  return `</${token.tag}>`;
};

const route = useRoute()
const article = ref(null)

/**
 * 加载文章内容并渲染为HTML
 * 包括Markdown解析、代码高亮和目录更新事件触发
 * @param {string} slug - 文章标识符
 */
const loadArticle = async (slug) => {
  try {
    const res = await getArticle(slug)
    article.value = res.data.data
    html.value = md.render(article.value.content)

    await nextTick()
    // 高亮显示代码块
    document.querySelectorAll("pre code").forEach((block) => {
      hljs.highlightElement(block)
    })
    bus.emit("article-loaded")
  } catch (err) {
    if (err.response && err.response.status === 404) {
      notFound.value = true
    }
  }
}

onMounted(() => {
  loadArticle(route.params.slug)
})

watch(
  () => route.params.slug,
  (newSlug) => {
    if (!newSlug) return
    loadArticle(newSlug)
  }
)

  /**
   * 计算给定日期距离今天的天数差
   * @param {string} dateStr - 日期字符串
   * @returns {string} 格式化后的天数差描述
   */
  function getDaysAgo(dateStr) {
    if (!dateStr) return '未知';
    
    const updateDate = new Date(dateStr);
    const today = new Date();
    
    // 清除时分秒影响，只计算日期差
    updateDate.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);
    
    const diffTime = today.getTime() - updateDate.getTime();
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays <= 0) return '今天更新';
    return `${diffDays} 天前`;
  }

</script>

<template>
  <div class="context">
    <div class="post-leftcolumn">
      <div v-if="article" class="article-page">
        <h1 style="font-size: 50px; font-style: italic;">{{ article.title }}</h1>
        <div class="markdown-body" v-html="html"></div>
        <el-divider content-position="left" class="divider">下面是评论</el-divider>
        <comment/>
      </div>
      <div class="text-nofound" v-if="notFound">
        <p>未找到文章</p>
      </div>

    </div>
    <div class="post-rightcolumn">
      <div class="article-tags" v-if="article">
        <h3 class="tags-title">统计</h3>
        <div class="stat-row">

          <span class="label">标签</span>
          <div class="value">
            <el-tag effect="info" v-for="value in article.tags" :key="value" size="mini">
              {{ value.name }}
            </el-tag>
          </div>
        </div>

        <div class="stat-row">
          <span class="label">字数</span>
          <span class="value">{{ article.content ? article.content.length : 0 }} 字</span>
        </div>

        <div class="stat-row">
          <span class="label">最后更新</span>
          <span class="value">{{ getDaysAgo(article.updated_time) }}</span>
        </div>
      </div>
      <ArticleToc/>
    </div>
  </div>
  
</template>

<style scoped>
.context {
  display: flex;
  gap: 20px;
}

.post-rightcolumn {
  flex: 0 0 25%;
}

.article-tags {
  gap: 5px;
  padding: 20px;
  width: 100%;
  background-color: var(--bg-color);
  border-radius: var(--border-radius);
  border: var(--border);
  box-shadow: var(--box-shadow);
  margin-bottom: 20px;
}

.stat-row {
  display: flex;
  justify-content: space-between; /* 左右分布 */
  align-items: center;
  margin-bottom: 12px;
  font-size: 14px;
}
.label {
  color: #606266; /* 较淡颜色标题 */
  flex-shrink: 0;
}
.value {
  text-align: right;
  color: var(--text-color);
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 4px;
}

.post-leftcolumn {
  background-color: var(--bg-color);
  flex: 1;
  padding: 10px;
  min-width: 0;
  width: 100%;
  border-radius: var(--border-radius);
  border: var(--border);
  box-shadow: var(--box-shadow);

}

.tags-title {
  font-weight: bold;
  font-size: 1.1rem;
  margin-bottom: 0.6rem;
  color: var(--text-color);
  border-bottom: 2px dashed;
  padding-bottom: 0.3rem;
}

.comment-section {
  padding: 20px;
}

.article-page {
  padding-left: 1rem;
  padding-right: 1rem;
  color: var(--text-color);
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

.title {
  font-size: 20px;
  font-style: italic;
  margin-bottom: 1rem;
  padding: 1rem 1rem;
}

::v-deep .markdown-body {
  font-family: 文楷;
}

::v-deep .markdown-body h1 {
  text-decoration: none !important;
}

::v-deep .h1-number{
  font-size: 60px;
  text-decoration: none !important;
  margin-right: 20px;
  font-style: italic;
}

::v-deep .h1-text{
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



::v-deep .markdown-body pre {
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
::v-deep .markdown-body pre::before {
  content: attr(data-lang);
  position: absolute;
  top: 3px;
  left: 100px;
  font-size: 1em;
  color: #272822;
  font-family: sans-serif;
}

::v-deep .markdown-body pre::after {
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
::v-deep .markdown-body pre code {
  background: none !important;
  padding-top: 10px;
  font-family: "Fira Code", Consolas, monospace;
  font-size: 1em;
  display: block;
  white-space: pre;
  margin: 0 !important;
}

/* 代码块内注释样式 */
::v-deep .markdown-body pre code .hljs-comment {
  font-family: "LXGW WenKai Mono", "Source Han Serif SC", "SimSun", monospace;
  color: #7d7d7d;
  font-size: 1em;
  opacity: 0.9;
  font-style: normal !important;
}

/* ---------- 表格整体样式 ---------- */
::v-deep .markdown-body table {
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
::v-deep .markdown-body thead {
  background-color: #fcbad3;
  color: #333;
  text-align: left;
  font-weight: bold;
}

/* 单元格 */
::v-deep .markdown-body th,
::v-deep .markdown-body td {
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  line-height: 1.6;
}

/* 隔行换色 */
::v-deep .markdown-body tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

/* hover 高亮 */
::v-deep .markdown-body tbody tr:hover {
  background-color: rgba(142, 140, 216, 0.1);
  transition: background 0.2s ease;
}

/* 单元格内代码 */
::v-deep .markdown-body td code {
  background: rgba(175, 184, 193, 0.15);
  padding: 2px 4px;
  border-radius: 3px;
  color: #e83e8c;
  font-size: 0.85em;
}

/* ---------- 暗色模式适配 ---------- */
::v-deep .dark .markdown-body table {
  background-color: #1e1e1e;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
}

::v-deep .dark .markdown-body thead {
  background-color: #333;
  color: #fcbad3;
}

::v-deep .dark .markdown-body th,
::v-deep .dark .markdown-body td {
  border: 1px solid #444;
  color: #ddd;
}

::v-deep .dark .markdown-body tbody tr:nth-child(even) {
  background-color: #2a2a2a;
}

::v-deep .dark .markdown-body tbody tr:hover {
  background-color: rgba(142, 140, 216, 0.2);
}

::v-deep .dark .markdown-body td code {
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


@media (max-width: 1000px) {
  .post-rightcolumn {
    display: none;
  }
}

@media (max-width: 768px) {
  ::v-deep .markdown-body table {
    display: block;
    font-size: 0.85em;
  }
}
</style>