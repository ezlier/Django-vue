<template>
  <div class="home">
    <WaterfallList :articles="articles" />

    <Pagination :current="currentPage" :total="total" :pageSize="10" @change="onPageChange" />

    <div v-if="loading" class="home__loading">
      <span class="loading-spinner"></span>
    </div>

    <div v-if="!loading && articles.length === 0" class="home__empty">
      暂无文章
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useArticleStore } from '@/stores/article'
import WaterfallList from '@/views/home/component/WaterfallList.vue'
import Pagination from '@/components/Pagination.vue'

const articleStore = useArticleStore()
const articles = ref(articleStore.articles)
const total = ref(articleStore.total)
const loading = ref(true)
const currentPage = ref(1)
const pageSize = 10

async function fetchPage(page: number) {
  loading.value = true
  try {
    await articleStore.fetchArticles(page, pageSize)
    articles.value = articleStore.articles
    total.value = articleStore.total
    currentPage.value = page
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } finally {
    loading.value = false
  }
}

function onPageChange(page: number) {
  fetchPage(page)
}

onMounted(() => {
  fetchPage(1)
})
</script>

<style scoped>
.home {
  width: 100%;
}

.home__loading {
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

.home__empty {
  text-align: center;
  padding: 64px 0;
  color: var(--color-text-mute);
  font-size: 15px;
}
</style>
