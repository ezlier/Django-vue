<template>
  <div class="random-card">
    <h3 class="random-card__title">推荐阅读</h3>
    <ul class="random-card__list" v-if="list.length">
      <li v-for="article in list" :key="article.slug">
        <RouterLink :to="`/article/${article.slug}`" class="random-card__link">
          {{ article.title }}
        </RouterLink>
        <span class="random-card__date">{{ formatDate(article.created_time) }}</span>
      </li>
    </ul>
    <p v-else class="random-card__empty">暂无文章</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useArticleStore } from '@/stores/article'

const articleStore = useArticleStore()

const list = computed(() => {
  const all = [...articleStore.articleList]
  // Fisher-Yates shuffle
  for (let i = all.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [all[i], all[j]] = [all[j], all[i]]
  }
  return all.slice(0, 3)
})

function formatDate(date: string) {
  const d = new Date(date)
  const m = (d.getMonth() + 1).toString().padStart(2, '0')
  const day = d.getDate().toString().padStart(2, '0')
  return `${m}-${day}`
}
</script>

<style scoped>
.random-card {
  padding: 20px;
  border-radius: 12px;
  border: 1px solid var(--color-border);
  background: var(--color-background);
}

.random-card__title {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-heading);
  margin: 0 0 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--color-border);
}

.random-card__list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.random-card__list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.random-card__link {
  font-size: 14px;
  color: var(--color-text);
  text-decoration: none;
  flex: 1;
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: color 0.2s;
}

.random-card__link:hover {
  color: var(--color-heading);
}

.random-card__date {
  font-size: 12px;
  color: var(--color-text-mute);
  flex-shrink: 0;
}

.random-card__empty {
  font-size: 13px;
  color: var(--color-text-mute);
  margin: 0;
}
</style>
