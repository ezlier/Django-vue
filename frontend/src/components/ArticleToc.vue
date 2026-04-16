<script setup lang="js">
import { ref, onMounted, onUnmounted, watch, nextTick } from "vue"
import { useRoute } from "vue-router"
import { bus } from "@/utils/eventBus"

const route = useRoute()
const headings = ref([])

/**
 * 从文章内容中提取标题（h1, h2, h3）生成目录
 * 为每个标题生成唯一ID（如果尚未设置），并构建标题层级结构
 */
const extractHeadings = () => {
  const content = document.querySelector(".markdown-body")
  if (!content) return
  const nodes = content.querySelectorAll("h1, h2, h3")
  const temp = []

  nodes.forEach((el) => {
    const id = el.id || el.textContent.trim().replace(/\s+/g, "-")
    el.id = id
    temp.push({
      id,
      text: el.textContent,
      level: parseInt(el.tagName[1]),
    })
  })
  headings.value = temp
}

/**
 * 滚动到指定标题位置
 * @param {string} id - 标题元素的ID
 */
const scrollToHeading = (id) => {
  const el = document.getElementById(id)
  if (el) {
    window.scrollTo({
      top: el.getBoundingClientRect().top + window.scrollY - 80,
      behavior: "smooth",
    })
  }
}

onMounted(() => {
  extractHeadings()

  // 🔥 监听文章加载事件
  bus.on("article-loaded", async () => {
    await nextTick()
    extractHeadings()
  })
})

onUnmounted(() => {
  bus.off("article-loaded")
})

// 如果你文章是通过路由切换加载的，也保持监听
watch(
  () => route.fullPath,
  async () => {
    await nextTick()
    extractHeadings()
  }
)
</script>

<template>
  <div class="toc-container">
    <h3 class="toc-title">📑 目录</h3>

    <div
      class="toc-list"
    >
      <template v-if="headings.length">
        <div
          v-for="(h, index) in headings"
          :key="index"
          class="toc-item"
          :class="[`level-${h.level}`]"
          @click="scrollToHeading(h.id)"
        >
          {{ h.text }}
        </div>
      </template>

      <p v-else class="no-headings">暂无标题</p>
    </div>


  </div>
</template>

<style scoped>
.toc-container {
  position: sticky;
  top:80px;
  background: var(--bg-color);
  padding: 1rem 1.2rem;
  border-radius: 10px;
  max-height: 80vh;
  overflow: hidden;
  transition: all 0.3s ease;
  border: var(--border);
  box-shadow: var(--box-shadow);
  border-radius: var(--border-radius);
}

.toc-title {
  font-weight: bold;
  font-size: 1.1rem;
  margin-bottom: 0.6rem;
  color: var(--text-color);
  border-bottom: 2px dashed;
  padding-bottom: 0.3rem;
}

.toc-list {
  overflow-y: auto;
  max-height: 40vh;
  padding-right: 4px;
  transition: max-height 0.3s ease;
}



.toc-item {
  cursor: pointer;
  padding: 0.25rem 0.4rem;
  border-left: 2px solid transparent;
  color: var(--text-color);
  line-height: 1.5;
  transition: all 0.2s;
  word-break: break-word;
}

.toc-item:hover {
  color: #f78fb3;
  background-color: rgba(252, 186, 211, 0.1);
}

.level-1 {
  margin-left: 0rem;
  font-weight: 600;
}

.level-2 {
  margin-left: 1rem;
  font-size: 0.95em;
}

.level-3 {
  margin-left: 2rem;
  font-size: 0.9em;
  opacity: 0.9;
}

.no-headings {
  color: #aaa;
  text-align: center;
  margin-top: 1rem;
}




</style>
