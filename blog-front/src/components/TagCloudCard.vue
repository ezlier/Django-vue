<template>
  <div class="tag-cloud-card">
    <h3 class="tag-cloud-card__title">标签</h3>
    <div class="tag-cloud-card__list" v-if="tags.length">
      <RouterLink v-for="tag in tags" :key="tag.id" :to="`/archive`" class="tag-cloud-card__item"
        :style="{ color: randomColor(tag.id) }">
        {{ tag.name }}
      </RouterLink>
    </div>
    <p v-else class="tag-cloud-card__empty">暂无标签</p>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useArticleStore } from '@/stores/article'

const articleStore = useArticleStore()

const tags = computed(() =>
  articleStore.tags.filter((t) => (t.article_count ?? 0) > 0)
)

const colorPool = [
  '#6366f1', '#ec4899', '#f59e0b', '#10b981', '#3b82f6',
  '#8b5cf6', '#ef4444', '#14b8a6', '#f97316', '#06b6d4',
  '#84cc16', '#d946ef', '#e11d48', '#0ea5e9', '#a855f7',
]

function randomColor(seed: number) {
  return colorPool[seed % colorPool.length]
}

onMounted(async () => {
  if (!articleStore.tags.length) {
    await articleStore.fetchTags()
  }
})
</script>

<style scoped>
.tag-cloud-card {
  padding: 15px;
  border-radius: 12px;
  border: 1px solid var(--color-border);
  background: var(--color-background);
  top: 80px;
}

.tag-cloud-card__title {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-heading);
  margin: 0 0 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--color-border);
}

.tag-cloud-card__list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-cloud-card__item {
  display: inline-block;
  padding: 4px 14px;
  font-size: 13px;
  font-weight: 500;
  border-radius: 4px;
  background: var(--color-background-mute);
  text-decoration: none;
  transition: transform 0.15s, background 0.2s;
}

.tag-cloud-card__item:hover {
  transform: scale(1.05);
  background: var(--color-border-hover);
}

.tag-cloud-card__empty {
  font-size: 13px;
  color: var(--color-text-mute);
  margin: 0;
}
</style>
