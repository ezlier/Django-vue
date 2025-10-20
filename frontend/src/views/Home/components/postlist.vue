<script setup>
import { ref, onMounted, computed } from "vue"
import { getArticles } from "@/utils/article"

const articles = ref([])

onMounted(async () => {
  const res = await getArticles()
  articles.value = res.data
})

const sortedArticles = computed(() => {
  return [...articles.value].sort((a, b) => new Date(b.date) - new Date(a.date))
})
</script>

<template>
  
    <div class="card-container">
      <RouterLink v-for="a in sortedArticles" :key="a.slug" :to="`/post/${a.slug}`" class="card">
        <h2>{{ a.title }}</h2>
        <h5>{{ a.date }}</h5>
        <div class="fakeimg" style="height: 200px;">
          <img v-if="a.image" :src="a.image" alt="封面图">
        </div>
      </RouterLink>
    </div>
  
</template>

<style scoped>
.card-container {
  display: grid;
  grid-template-columns: repeat(2, minmax(300px, 1fr));
  gap: 20px;
  position: relative;
}

.card {
  text-decoration: none; /* 去掉下划线 */
  color: black; /* 设为黑色 */
  background-color: var(--bg-color);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.fakeimg {
  width: 100%;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background-color: #f5f5f5;
  border-radius:8px;
}

.fakeimg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

@media (max-width: 768px) {
  .card-container {
    grid-template-columns: 1fr;
  }
}
</style>