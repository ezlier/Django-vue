<template>
  <aside class="article-sidebar">
    <ArticleInfoCard :article="article" :content="content" />
    <ArticleNavCard />
  </aside>
</template>

<script setup lang="ts">
import type { Article } from '@/stores/article'
import ArticleInfoCard from './ArticleInfoCard.vue'
import ArticleNavCard from './ArticleNavCard.vue'

defineProps<{
  article: Article | null
  content?: string
}>()
</script>

<style scoped>
.article-sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
