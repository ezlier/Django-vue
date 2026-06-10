<script setup>
import { ref, onMounted, computed } from "vue";
import { useArticleStore } from "@/stores/article"

const articleStore = useArticleStore()

const currentPage = ref(1);
const articles = computed(() => articleStore.articleList)
const loading = ref(true)

onMounted(async () => {
  await articleStore.fetchArticles(currentPage.value, 10);
  loading.value = false;
});

const sortedArticles = computed(() => {
  return [...articles.value].sort((a, b) => new Date(b.date) - new Date(a.date));
});

const visibleArticles = computed(() => sortedArticles.value.slice(0, 10));

const changePage = async (page) => {
  currentPage.value = page;
  loading.value = true;
  await articleStore.fetchArticles(page, 10);
  loading.value = false;
};

</script>

<template>

  <el-skeleton v-if="loading" :rows="20"/>
  <div class="postlist-container">
    
    <div class="card-container">
      <RouterLink v-for="a in visibleArticles" :key="a.slug" :to="`/post/${a.slug}`" class="card fade-in"  v-fade-in>
        <div class="fakeimg">
          <img v-if="a.cover" :src="a.cover" alt="封面图" />
          <img v-else src="https://ezlier.github.io/blog-vue/cover/cover-14.jpg"/>
        </div>
        
        <div class="card-content">
          <h2>
            {{ a.title }}
          </h2>
          <p>{{ a.created_time }}</p>
          <div>
            <el-tag v-for="value in a.tags" effect="plain" type="info">#{{ value.name }} </el-tag>
             
          </div>
          <div class="initialize-access-btn">
            READING
            <span class="arrow-icon">→</span>
          </div>
        </div>
      </RouterLink>
    </div>

    <!-- 分页组件 -->
    <div class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="10"
        layout="prev, pager, next"
        :total="articleStore.articlesLength"
        @current-change="changePage"
      />
    </div>
  </div>
</template>

<style scoped>
.postlist-container {
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.5);
  position: relative;
  border: 1px solid rgba(255,255,255,.8);
  box-shadow: 0 10px 40px #ea810214;
  border-radius: var(--border-radius);
}

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
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  border: var(--border);
  cursor: pointer;
  transition: 0.3s ease;
}

.card:hover {
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  border-color: #ffb6b9;
}

.card-content {
  padding: 10px;
}

.icon {
  width: 15px;
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
}

.fakeimg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.pagination-container {
  
  margin-top: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.initialize-access-btn {
  /* 布局与尺寸 */
  display: inline-flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 1rem;
  /* 文字样式 */
  font-family: 'Arial', sans-serif;
  letter-spacing: 0.1em; /* 宽松字间距，还原原图风格 */
  text-transform: uppercase;
  color: #ffffff;
  /* 背景与质感 */
  background-color: #121212; /* 纯黑哑光基底 */
  border: none;
  border-radius: 4px; /* 轻微圆角，还原原图 */
  /* 阴影：模拟轻微凸起的物理质感 */
  box-shadow: 
    0 2px 4px rgba(0, 0, 0, 0.4), /* 外阴影，营造立体感 */
    inset 0 1px 0 rgba(255, 255, 255, 0.05); /* 内高光，增强质感 */
  /* 文字模糊：还原原图的柔化效果 */
  filter: blur(0.5px);
  -webkit-filter: blur(0.5px);
  /* 过渡动画：交互丝滑 */
  transition: all 0.2s ease;
  cursor: pointer;
}

/* 箭头图标样式 */
.arrow-icon {
  margin-left: 1.5rem;
  line-height: 1;
}

/* Hover状态：轻微提亮+上浮 */
.initialize-access-btn:hover {
  background-color: #1a1a1a;
  box-shadow: 
    0 4px 8px rgba(0, 0, 0, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.08);
  filter: blur(0.3px);
  transform: translateY(-1px);
}

/* Active状态：按压下陷效果 */
.initialize-access-btn:active {
  background-color: #0a0a0a;
  box-shadow: 
    0 1px 2px rgba(0, 0, 0, 0.6),
    inset 0 2px 4px rgba(0, 0, 0, 0.8);
  filter: blur(0.6px);
  transform: translateY(1px);
}


@media (max-width: 768px) {
  .card-container {
    grid-template-columns: 1fr;
  }
}
</style>
