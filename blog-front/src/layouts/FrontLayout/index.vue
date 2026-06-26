<template>
  <div class="front-layout">
    <Navbar />

    <Header />

    <main class="front-main">
      <div class="leftcolumn">
        <Sidebar v-if="!isArticlePage" />
        <ArticleSidebar
          v-else
          :article="currentArticle"
          :content="articleContent"
        />
      </div>

      <div class="rightcolumn">
        <RouterView v-slot="{ Component }">
          <KeepAlive :exclude="['ArticleDetail']">
            <component :is="Component" :ref="setArticleRef" />
          </KeepAlive>
        </RouterView>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUiStore } from '@/stores/ui'
import { useArticleStore } from '@/stores/article'
import type { Article } from '@/stores/article'
import Navbar from './component/navbar.vue'
import Footer from './component/footer.vue'
import Header from './component/header.vue'
import Sidebar from './component/Sidebar.vue'
import ArticleSidebar from '@/views/article-detail/component/ArticleSidebar.vue'

const route = useRoute()
const ui = useUiStore()
const articleStore = useArticleStore()

const isArticlePage = computed(() => route.name === 'ArticleDetail')
const currentArticle = ref<Article | null>(null)
const articleContent = ref('')

function setArticleRef(el: any) {
  if (el?.article) {
    currentArticle.value = el.article
    articleContent.value = el.html || ''
  }
}

onMounted(() => {
  ui.fetchWebSetting()
})
</script>

<style scoped>
.front-layout {
  background: var(--color-background-soft);
}

.front-main {
  display: flex;
  gap: 24px;
  max-width: 1280px;
  padding: 24px;
  justify-content: center;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}

.leftcolumn {
  flex: 0 0 280px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.rightcolumn {
  flex: 1;
  min-width: 0;
  border-radius: 12px;
  border: var(--border);
  box-shadow: var(--box-shadow);
  border-color: var(--color-border);
  background-color: var(--color-background-soft);
  padding: 1.125rem;
}

@media (max-width: 768px) {
  .front-main {
    flex-direction: column;
    padding: 16px;
  }
  .leftcolumn {
    flex: none;
    width: 100%;
  }
}
</style>
