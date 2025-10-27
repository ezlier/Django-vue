<script setup>
import { ref, onMounted, computed, onUnmounted } from "vue";
import { getArticles } from "@/utils/article";

const articles = ref([]);
const visibleCount = ref(6); // 每次显示的数量

onMounted(async () => {
  const res = await getArticles();
  articles.value = res.data;
  window.addEventListener("scroll", handleScroll);
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
});

const sortedArticles = computed(() => {
  return [...articles.value].sort((a, b) => new Date(b.date) - new Date(a.date));
});

// 仅显示部分文章
const visibleArticles = computed(() => sortedArticles.value.slice(0, visibleCount.value));

// 滚动触底加载更多
function handleScroll() {
  const scrollTop = window.scrollY || document.documentElement.scrollTop;
  const windowHeight = window.innerHeight;
  const docHeight = document.documentElement.scrollHeight;

  // 距底 100px 时加载更多
  if (scrollTop + windowHeight >= docHeight - 100) {
    loadMore();
  }
}

function loadMore() {
  if (visibleCount.value < sortedArticles.value.length) {
    visibleCount.value += 6;
  }
}
</script>

<template>
  <div class="card-container">
    <RouterLink v-for="a in visibleArticles" :key="a.slug" :to="`/post/${a.slug}`" class="card">
      <h2>
        <svg style="height: 20px;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
          <path fill="currentColor"
            d="m249.6 417.088 319.744 43.072 39.168 310.272L845.12 178.88zm-129.024 47.168a32 32 0 0 1-7.68-61.44l777.792-311.04a32 32 0 0 1 41.6 41.6l-310.336 775.68a32 32 0 0 1-61.44-7.808L512 516.992z" />
        </svg>
        {{ a.title }}
      </h2>

      <h5>
        <el-tag effect="plain">
          <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
            <path fill="currentColor"
              d="M128 384v512h768V192H768v32a32 32 0 1 1-64 0v-32H320v32a32 32 0 0 1-64 0v-32H128v128h768v64zm192-256h384V96a32 32 0 1 1 64 0v32h160a32 32 0 0 1 32 32v768a32 32 0 0 1-32 32H96a32 32 0 0 1-32-32V160a32 32 0 0 1 32-32h160V96a32 32 0 1 1 64 0zm-32 384h64a32 32 0 0 1 0 64h-64a32 32 0 0 1 0-64m0 192h64a32 32 0 1 1 0 64h-64a32 32 0 1 1 0-64m192-192h64a32 32 0 0 1 0 64h-64a32 32 0 0 1 0-64m0 192h64a32 32 0 1 1 0 64h-64a32 32 0 1 1 0-64m192-192h64a32 32 0 1 1 0 64h-64a32 32 0 1 1 0-64m0 192h64a32 32 0 1 1 0 64h-64a32 32 0 1 1 0-64" />
          </svg>
          {{ a.date }} |
          <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
            <path fill="currentColor"
              d="M224 704h576V318.336L552.512 115.84a64 64 0 0 0-81.024 0L224 318.336zm0 64v128h576V768zM593.024 66.304l259.2 212.096A32 32 0 0 1 864 303.168V928a32 32 0 0 1-32 32H192a32 32 0 0 1-32-32V303.168a32 32 0 0 1 11.712-24.768l259.2-212.096a128 128 0 0 1 162.112 0" />
            <path fill="currentColor"
              d="M512 448a64 64 0 1 0 0-128 64 64 0 0 0 0 128m0 64a128 128 0 1 1 0-256 128 128 0 0 1 0 256" />
          </svg>
          {{ a.tags }}
        </el-tag>
      </h5>

      <div class="fakeimg">
        <img v-if="a.image" :src="a.image" alt="封面图" />
      </div>
    </RouterLink>

    <!-- 加载提示 -->
    <div v-if="visibleCount < sortedArticles.length" class="loading-text">
      加载中...
    </div>
    <div v-else class="loading-text">没有更多文章啦~</div>
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
  text-decoration: none;
  color: var(--text-color);
  background-color: var(--bg-color);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  color: #ffb6b9;
}

.icon {
  width: 12px;
  vertical-align: middle;
}

.fakeimg {
  width: 100%;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.fakeimg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.loading-text {
  text-align: center;
  color: var(--text-color);
  font-size: 14px;
  margin: 20px 0;
  grid-column: span 2;
}

@media (max-width: 768px) {
  .card-container {
    grid-template-columns: 1fr;
  }

  .loading-text {
  text-align: center;
  color: var(--text-color);
  font-size: 14px;
  margin: 20px 0;
  grid-column: span 1;
}
}
</style>
