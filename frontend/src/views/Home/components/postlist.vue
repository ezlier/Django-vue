<script setup>
import { ref, onMounted } from "vue"
import { getArticles, getArticle } from "@/utils/article"

const articles = ref([])
const article = ref(null)

onMounted(async () => {
  const res = await getArticles()
  articles.value = res.data
})
</script>

<template>
  <div>
    <h2>文章列表</h2>
    <ul>
      <li v-for="a in articles" :key="a.title">
        {{ a.title }} - {{ a.date }}
      </li>
    </ul>
  </div>
</template>
