<template>
  <div class="article-sidebar">
    <div class="article-sidebar__sticky">
      <ArticleInfoCard :article="article" :content="content" class="article-sidebar__info-card" />
      <ArticleNavCard class="article-sidebar__nav-card" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import type { Article } from '@/stores/article'
import { useArticleStore } from '@/stores/article'
import ArticleInfoCard from './ArticleInfoCard.vue'
import ArticleNavCard from './ArticleNavCard.vue'

const route = useRoute()
const articleStore = useArticleStore()
const article = ref<Article | null>(null)
const content = ref('')

async function load() {
  const slug = route.params.slug as string
  if (!slug) return
  const data = await articleStore.fetchArticle(slug)
  article.value = data
  content.value = data.content || ''
}

// 首次挂载加载
load()

// 监听路由切换（同一组件在不同 slug 之间跳转时 onMounted 不会重新触发）
watch(() => route.params.slug, () => {
  if (route.name === 'ArticleDetail') {
    load()
  }
})
</script>

<style scoped>
.article-sidebar {
  height: 100%;
}

.article-sidebar__sticky {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
}

.article-sidebar__nav-card {
  position: sticky;
  top: 80px;
}
</style>
