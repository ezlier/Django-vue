<template>
  <div class="archive">
    <TagFilter :tags="validTags" :activeTag="activeTag" @change="activeTag = $event" />

    <div v-if="loading" class="archive__loading">
      <span class="loading-spinner"></span>
    </div>

    <TimelineList :articles="filteredArticles" />

    <div v-if="!loading && filteredArticles.length === 0" class="archive__empty">
      暂无文章
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useArticleStore } from '@/stores/article'
import TagFilter from './component/TagFilter.vue'
import TimelineList from './component/TimelineList.vue'

const articleStore = useArticleStore()
const loading = ref(true)
const activeTag = ref<number | null>(null)

const validTags = computed(() =>
  articleStore.tags.filter((t) => (t.article_count ?? 0) > 0)
)

const filteredArticles = computed(() => {
  if (activeTag.value === null) return articleStore.articleList
  return articleStore.articleList.filter((a) =>
    a.tags.some((t) =>
      typeof t === 'string' ? false : t.id === activeTag.value
    )
  )
})



onMounted(async () => {
  try {
    await articleStore.fetchAllArticles()
    await articleStore.fetchTags()
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.archive {
  width: 100%;
}

.archive__loading {
  display: flex;
  justify-content: center;
  padding: 32px 0;
}

.loading-spinner {
  width: 28px;
  height: 28px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-heading);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.archive__empty {
  text-align: center;
  padding: 64px 0;
  color: var(--color-text-mute);
  font-size: 15px;
}
</style>
