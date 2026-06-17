<template>
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

      <transition-group name="fade-slide" tag="div">
        <RouterLink
          v-for="post in group.posts"
          :key="post.slug"
          :to="`/article/${post.slug}`"
          class="timeline-item"
        >
          <div class="timeline-date">{{ formatDate(post.created_time) }}</div>

          <div class="timeline-dot-line">
            <div class="timeline-dot"></div>
          </div>

          <div class="timeline-title">{{ post.title }}</div>
          <div class="timeline-tags">
            <span
              v-for="tag in post.tags"
              :key="typeof tag === 'string' ? tag : tag.id"
              class="timeline-tag"
            >
              {{ typeof tag === 'string' ? tag : tag.name }}
            </span>
          </div>
        </RouterLink>
      </transition-group>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Article } from '@/stores/article'

const props = defineProps<{
  articles: Article[]
}>()

const groupedArticles = computed(() => {
  const grouped: Record<string, Article[]> = {}
  for (const article of props.articles) {
    const year = new Date(article.created_time).getFullYear()
    if (!grouped[year]) grouped[year] = []
    grouped[year].push(article)
  }
  return Object.keys(grouped)
    .sort((a, b) => Number(b) - Number(a))
    .map((year) => ({
      year: Number(year),
      posts: grouped[year].sort(
        (a, b) => new Date(b.created_time).getTime() - new Date(a.created_time).getTime()
      ),
    }))
})

function formatDate(date: string) {
  const d = new Date(date)
  const m = (d.getMonth() + 1).toString().padStart(2, '0')
  const day = d.getDate().toString().padStart(2, '0')
  return `${m}-${day}`
}
</script>

<style scoped>
.timeline-container {
  border-top: 2px dashed var(--color-border);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

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
  color: var(--color-heading);
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
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid var(--color-heading);
  transform: translate(-50%, -50%);
}

.timeline-year-count {
  width: 70%;
  text-align: left;
  color: var(--color-text-mute);
  font-size: 14px;
}

.timeline-item {
  display: flex;
  align-items: center;
  height: 2.5rem;
  text-decoration: none;
  color: inherit;
  transition: background 0.25s ease;
  border-radius: 10px;
}

.timeline-item:hover {
  background: var(--color-background-mute);
}

.timeline-item:hover .timeline-title {
  transform: translateX(4px);
}

.timeline-date {
  width: 15%;
  text-align: right;
  color: var(--color-text-mute);
  font-size: 14px;
}

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
  background: var(--color-border);
  transform: translateX(-50%);
  z-index: 0;
}

.timeline-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--color-text-mute);
  transition: all 0.2s ease;
  position: relative;
  z-index: 1;
}

.timeline-item:hover .timeline-dot {
  width: 10px;
  height: 10px;
  background: var(--color-heading);
}

.timeline-title {
  flex: 1;
  text-align: left;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: transform 0.25s ease;
}

.timeline-tags {
  margin-left: auto;
  padding-right: 16px;
  display: flex;
  gap: 6px;
}

.timeline-tag {
  padding: 2px 10px;
  font-size: 12px;
  border-radius: 100px;
  background: var(--color-background-mute);
  color: var(--color-text-mute);
  white-space: nowrap;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.35s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@media (max-width: 768px) {
  .timeline-tags {
    display: none;
  }
}
</style>
