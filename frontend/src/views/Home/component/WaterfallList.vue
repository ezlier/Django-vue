<template>
  <div class="waterfall">
    <div
      v-for="(article, index) in visibleArticles"
      :key="article.slug"
      class="waterfall__item"
    >
      <ArticleCard
        :article="article"
        :style="{ animationDelay: `${index * 0.06}s` }"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import ArticleCard from '@/views/home/component/ArticleCard.vue'
import type { Article } from '@/stores/article'

const props = defineProps<{
  articles: Article[]
}>()

const visibleArticles = computed(() => props.articles.slice(0, 10))
</script>

<style scoped>
.waterfall {
  width: 100%;
  column-count: 2;
  column-gap: 20px;
}

.waterfall__item {
  width: 100%;
  margin-bottom: 20px;
  break-inside: avoid;
  page-break-inside: avoid;
  -webkit-column-break-inside: avoid;
}

@media (max-width: 768px) {
  .waterfall {
    column-count: 1;
    column-gap: 0;
  }

  .waterfall__item {
    margin-bottom: 16px;
  }
}
</style>
