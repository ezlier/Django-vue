<script setup>
import head from '@/assets/img/head.jpg' 
import { getPostSum } from "@/utils/article"
import { ref, onMounted } from "vue"

import { getWebSetting } from "@/utils/websetting"

const form = ref([])
onMounted(async () => {
  
})


const articlesCount = ref()

onMounted(async () => {
  const text = await getPostSum();
  articlesCount.value = text;
  const res = await getWebSetting();
  form.value = res.data;
})
</script>

<template>
      <div class="card">
        <div class="avatar-container">
          <img :src='head' width="100" class="avatar" />
        </div>
        <h1 style="color: #f77;">{{ form.name }}</h1>
        <div class="stats">
          <div class="stat-item">
            <span class="stat-label">文章</span>
            <span class="stat-number">{{ articlesCount }}</span>
          </div>
        </div>
      </div>

</template>

<style scoped>

.card {
  /* flex: 1; */
  background-color: var(--bg-color);
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center; 
  border-radius: 8px;
  border-style:solid;
  border-color: var(--border);
  box-shadow: 2px 2px #000;
}

.avatar-container {
  width: 100px;
  height: 100px;
  overflow: hidden; 
  border-radius: 1rem;
  box-shadow: 0 0 15px 5px rgba(255, 0, 0, 0.2);
}

.stats {
  display: flex;
  margin-top: 10px;
  gap: 20px;
  color: #f77;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-number {
  font-size: 1.2rem;
  font-weight: bold;
}

.stat-label {
  font-size: 0.8rem;
  
}
</style>