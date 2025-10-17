<script setup>
import { ref, onMounted } from "vue"
import { useRoute } from "vue-router"
import { getArticle } from "@/utils/article"

const route = useRoute()
const article = ref(null)

onMounted(async () => {
  const slug = route.params.slug
  const res = await getArticle(slug)
  article.value = res.data
})
</script>

<template>
  <div v-if="article" class="article-page">
    <h1>{{ article.title }}</h1>
    <p class="date">{{ article.date }}</p>
    <img v-if="article.image" :src="article.image" alt="封面图" class="cover" />
    <!-- content 是 HTML 格式 -->
    <div class="content" v-html="article.content"></div>
  </div>

  <div v-else class="loading">正在加载文章...</div>
</template>

<style scoped>
.article-page {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
  color: #fff;
  line-height: 1.8;
}
.cover {
  width: 100%;
  border-radius: 10px;
  margin: 1rem 0;
}
.date {
  color: #aaa;
  font-size: 0.9rem;
}
.content {
  margin-top: 1.5rem;
}
.loading {
  color: #aaa;
  text-align: center;
  margin-top: 2rem;
}
</style>
