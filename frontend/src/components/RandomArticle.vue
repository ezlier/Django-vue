<script setup>
import { ref, onMounted, computed } from "vue"
import { getArticles } from "@/utils/article"

const articles = ref([])

const loading = ref(true)

onMounted(async () => {
  const res = await getArticles()
  const allArticles = res.data

  // 随机打乱数组
  const shuffled = allArticles.sort(() => 0.5 - Math.random())

  // 取前 N 条
  const N = 3 // 改成 2 就是取 2 条
  articles.value = shuffled.slice(0, N)
  loading.value = false
})
</script>

<template>
  <div class="random">
    <div class="card-header">
      <span class="icon-text">
        <svg style="width: 20px;" xmlns="http://www.w3.org/2000/svg" xml:space="preserve" viewBox="0 0 1024 1024">
          <path fill="currentColor"
            d="M480 320h192c21.33 0 32-10.67 32-32s-10.67-32-32-32H480c-21.33 0-32 10.67-32 32s10.67 32 32 32"></path>
          <path fill="currentColor"
            d="M887.01 72.99C881.01 67 873.34 64 864 64H160c-9.35 0-17.02 3-23.01 8.99C131 78.99 128 86.66 128 96v832c0 9.35 2.99 17.02 8.99 23.01S150.66 960 160 960h704c9.35 0 17.02-2.99 23.01-8.99S896 937.34 896 928V96c0-9.35-3-17.02-8.99-23.01M192 896V128h96v768zm640 0H352V128h480z">
          </path>
          <path fill="currentColor"
            d="M480 512h192c21.33 0 32-10.67 32-32s-10.67-32-32-32H480c-21.33 0-32 10.67-32 32s10.67 32 32 32m0 192h192c21.33 0 32-10.67 32-32s-10.67-32-32-32H480c-21.33 0-32 10.67-32 32s10.67 32 32 32">
          </path>
        </svg>
        随便看看
      </span>
    </div>
    <div v-if="loading">
      <el-skeleton-item variant="image" style="width: 100%; height: 120px" animated />
      <el-skeleton-item variant="image" style="width: 100%; height: 120px" animated />
      <el-skeleton-item variant="image" style="width: 100%; height: 120px" animated />
    </div>

    <RouterLink v-for="a in articles" :key="a.slug" :to="`/post/${a.slug}`" class="random-card">
      <div class="image-wrapper">
        <img :src="a.image || '/default-cover.jpg'" alt="封面图">
        <div class="info">
          <p class="title">{{ a.title }}</p>
        </div>
      </div>
    </RouterLink>
  </div>
</template>

<style scoped>
.random{
  background-color: var(--bg-color);
  padding: 20px;
  max-width: 480px;
  border-radius: 8px;
  border-style:solid;
  border-color: var(--border);
  box-shadow: 2px 2px #000;
}

.card-header{
  border-bottom: 2px dashed;
}

.icon-text {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 16px;
  color: var(--text-color);
}

.icon-text svg {
  width: 20px;
  height: 20px;
  vertical-align: middle;
}

/* 随机文章卡片样式 */
.random-card {
  margin-top: 5px;
  display: block;
  position: relative;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 12px;
  text-decoration: none;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.random-card:hover {
  transform: translateY(-3px);
}

/* 图片封面 */
.image-wrapper {
  position: relative;
  width: 100%;
  height: 120px;
  overflow: hidden;
}

.image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.random-card:hover img {
  transform: scale(1.05);
}

/* 信息层 */
.info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 10px 12px;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0));
  color: #fff;
}

.title {
  font-size: 15px;
  font-weight: 600;
  margin-top: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>