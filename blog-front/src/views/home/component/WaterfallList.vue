<template>
  <div class="waterfall">
    <div class="waterfall__col">
      <ArticleCard v-for="(article, i) in leftColumn" :key="article.slug" :article="article"
        :style="{ animationDelay: `${(i * 0.1).toFixed(1)}s` }" />
    </div>
    <div class="waterfall__col">
      <ArticleCard v-for="(article, i) in rightColumn" :key="article.slug" :article="article"
        :style="{ animationDelay: `${(i * 0.1 + 0.05).toFixed(1)}s` }" />
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

const leftColumn = computed(() =>
  props.articles.filter((_, i) => i % 2 === 0)
)

const rightColumn = computed(() =>
  props.articles.filter((_, i) => i % 2 === 1)
)
</script>

<style scoped>
.waterfall {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.waterfall__col {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-width: 0;
}

@media (max-width: 768px) {
  .waterfall {
    flex-direction: column;
  }

  .waterfall__col {
    gap: 16px;
  }
}
</style>
