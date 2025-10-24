<script setup>
import { ref, onMounted, computed } from "vue"
import { getArticles } from "@/utils/article"
import About from '@/components/about.vue';
import RandomArticle from '@/components/RandomArticle.vue'
import Clock from '@/components/clock.vue';

const articles = ref([])

const loading = ref(true)

onMounted(async () => {
  const res = await getArticles()
  articles.value = res.data

  loading.value = false
})



// 按年份分组排序
const groupedArticles = computed(() => {
  const grouped = {}
  for (const article of articles.value) {
    const year = new Date(article.date).getFullYear()
    if (!grouped[year]) grouped[year] = []
    grouped[year].push(article)
  }
  return Object.keys(grouped)
    .sort((a, b) => b - a)
    .map((year) => ({
      year,
      posts: grouped[year].sort((a, b) => new Date(b.date) - new Date(a.date)),
    }))
})

function formatDate(date) {
  const d = new Date(date)
  const m = (d.getMonth() + 1).toString().padStart(2, "0")
  const day = d.getDate().toString().padStart(2, "0")
  return `${m}-${day}`
}
</script>

<template>
  <div class="rightcolumn">
    <el-skeleton v-if="loading" :rows="20" animated />
    <div class="timeline-container">
      <div v-for="group in groupedArticles" :key="group.year" class="timeline-year-block">
        <!-- 年份标题行 -->
        <div class="timeline-year-header">
          <div class="timeline-year">{{ group.year }}</div>
          <div class="timeline-dot-outline"></div>
          <div class="timeline-year-count">
            {{ group.posts.length }} 篇文章
          </div>
        </div>

        <!-- 每篇文章 -->
        <RouterLink v-for="post in group.posts" :key="post.slug" :to="`/post/${post.slug}`" class="timeline-item">
          <div class="timeline-date">{{ formatDate(post.date) }}</div>

          <div class="timeline-dot-line">
            <div class="timeline-dot"></div>
          </div>

          <div class="timeline-title">{{ post.title }}</div>

        </RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.rightcolumn {
  flex: 1;
  padding: 20px;
  min-width: 0;
  border-radius: 8px;
  background-color: whitesmoke;
}

/* === 时间线整体容器 === */
.timeline-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* === 年份行 === */
.timeline-year-header {
  display: flex;
  align-items: center;
  height: 3.5rem;
}

.timeline-year {
  width: 15%;
  text-align: right;
  font-size: 1.5rem;
  font-weight: bold;
  color: #555;
}

.timeline-dot-outline {
  width: 15%;
  position: relative;
}

.timeline-dot-outline::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 9999px;
  border: 2px solid #fcbad3;
  transform: translate(-50%, -50%);
}

.timeline-year-count {
  width: 70%;
  text-align: left;
  color: #777;
}

/* === 时间线文章项 === */
.timeline-item {
  display: flex;
  align-items: center;
  height: 2.5rem;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
}

.timeline-item:hover {
  background-color: #ffe2e2;
  border-radius: 10px;
}

.timeline-item:hover .timeline-title {
  transform: translateX(4px);
  color: #aa96da;
}

/* 日期在左边 */
.timeline-date {
  width: 15%;
  text-align: right;
  color: #888;
  font-size: 0.875rem;
}

/* 竖线+中点 */
.timeline-dot-line {
  width: 15%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 2.5rem;
}

.timeline-dot-line::after {
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  left: 50%;
  width: 1px;
  background-color: rgba(180, 180, 180, 0.4);
  transform: translateX(-50%);
  z-index: 0;
}

.timeline-dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background-color: #bbb;
  transition: all 0.2s ease;
  position: relative;
  z-index: 1;
}

.timeline-item:hover .timeline-dot {
  width: 8px;
  height: 8px;
  background-color: #fcbad3;
}

/* 标题 */
.timeline-title {
  width: 70%;
  text-align: left;
  font-weight: 600;
  color: #444;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: all 0.3s ease;
  padding-right: 1rem;
}

</style>