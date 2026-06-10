<script setup>
import { getWebSetting } from "@/utils/websetting"
import { onMounted, ref } from 'vue';
import MessageBoard from './components/MessageBoard.vue';
import MarkdownIt from "markdown-it"
import hljs from "highlight.js"
import "highlight.js/styles/github-dark.css"

const html = ref("")

const md = new MarkdownIt({
  html: true,
  linkify: true,
  highlight(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return `<pre class="hljs"><code>${hljs.highlight(code, { language: lang }).value}</code></pre>`
    }
    return `<pre class="hljs"><code>${md.utils.escapeHtml(code)}</code></pre>`
  }
})

onMounted(async () => {
  const res = await getWebSetting()
  html.value = md.render(res.data.data.about_md)
})
</script>

<template>
    <div class="content">
        <div>
            <div class="about-wrapper" v-html="html"></div>
        </div>
        <div>
            <MessageBoard/>
        </div>
    </div>
    
</template>

<style scoped>
.content {
    padding: 20px;
    min-width: 0;
    border-radius: var(--border-radius);
    background-color: var(--bg-color);
    border: var(--border);
    box-shadow: var(--box-shadow);
}
</style>