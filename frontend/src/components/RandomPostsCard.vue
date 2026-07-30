<template>
  <div class="random-card">
    <h3 class="random-card__title">随便看看</h3>
    <ul class="random-card__list" v-if="list.length">
      <li v-for="article in list" :key="article.slug">
        <RouterLink :to="`/article/${article.slug}`" class="random-card__link">
          <img class="random-card__cover" :src="article.cover">
          <p class="card-title">{{ article.title.length > 20 ? article.title.slice(0, 20) + '...' : article.title }}</p>

        </RouterLink>
      </li>
    </ul>
    <p v-else class="random-card__empty">暂无文章</p>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useArticleStore } from '@/stores/article'

const articleStore = useArticleStore()

const list = computed(() => {
  const all = [...articleStore.articleList]
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

onMounted(async () => {
  if (!articleStore.articleList.length) {
    await articleStore.fetchAllArticles()
  }
})
</script>

<style scoped>
.random-card {
  padding: 15px;
  border-radius: 12px;
  border: 1px solid var(--color-border);
  background: var(--color-background);
  position: sticky;
  top: 100px;
  min-width: 0;
}

.random-card__title {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-heading);
  margin: 0 0 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--color-border);
  position: relative;
  top: 10px;
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
  min-height: 150px;
  transition: color 0.2s;
  position: relative;
  overflow: hidden;
  display: block;
  min-width: 0;
  transition: transform 0.4s ease;
}

.random-card__link:hover {
  color: var(--color-heading);
  transform: scale(1.04);
}

.card-title {
  position: absolute;
  bottom: 0px;
  left: 10px;
  right: 10px;
  color: black;
  font-size: 14px;
  font-weight: 700;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.random-card__date {
  font-size: 12px;
  color: var(--color-text-mute);
  flex-shrink: 0;
}

.random-card__cover {
  width: 100%;
  height: 150px;
  border-radius: 8px;
  object-fit: cover;
}



.random-card__empty {
  font-size: 13px;
  color: var(--color-text-mute);
  margin: 0;
}
</style>
