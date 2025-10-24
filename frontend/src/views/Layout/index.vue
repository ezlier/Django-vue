<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import PointerTextTrail from '@/components/PointerTextTrail.vue';
import navbar from "@/views/Layout/components/nav.vue"
import footera from "@/views/Layout/components/Footer.vue"
import Welcome from '@/components/welcome.vue'
import About from '@/components/about.vue';
import RandomArticle from '@/components/RandomArticle.vue'
import Clock from '@/components/clock.vue';
import ArticleToc from '@/components/ArticleToc.vue'

const route = useRoute();

// 动态计算 header 高度
const headerHeight = computed(() => {
  if (route.name === "Home") return "100vh";
  if (route.name === "ArticleDetail") return "300px"; // 可按需改
  return "300px";
});

// 动态判断是否为文章详情页
const isPostPage = computed(() => route.name === "ArticleDetail");
</script>

<template>
  <div class="bg" />
  <PointerTextTrail class="texiao " />

  <navbar />

  <main class="main-content">
    <div class="header" :style="{ height: headerHeight }">
      <Welcome v-if="route.name === 'Home'" />
    </div>
    <div class="content">
      <div class="row">
        <div class="leftcolumn">

          <!-- 其他页面部分 -->
          <template v-if="!isPostPage">
            <About />
            <div class="sticky-container">
              <RandomArticle class="RandomArticle" />
              <Clock class="clock-wrapper" />
            </div>
          </template>

          <!-- 文章目录部分 -->
          <template v-else>
            <ArticleToc />
          </template>
        </div>

        <div class="rightcolumn">
          <RouterView />
        </div>
      </div>
    </div>
  </main>

  <footera />
</template>

<style scoped>
.content {
  background-color: rgba(204, 204, 204, 0.9);
}

.header {
  transition: height 0.5s ease;
  /* 动画过渡更自然 */
}

.row {
  display: flex;
  /* align-items: flex-start; */
  gap: 20px;
  max-width: 1280px;
  padding: 20px;
  justify-content: center;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}

.leftcolumn {
  flex: 0 0 20%;
  /* 固定25%宽度 */
  /* background-color: #f1f1f1; */
  /* padding: 20px; */
  border-radius: 8px;
}

.sticky-container {
  position: sticky;
  top: 50px;
}

.RandomArticle {
  margin-top: 20px;
}

.clock-wrapper {
  width: 100%;
  margin-top: 20px;
}


.rightcolumn {
  flex: 1;
  min-width: 0;
  width: 100%;
  border-radius: 8px;
  /* box-shadow: 2px 2px 5px #000; */
}

.bg {
  position: fixed;
  /* 固定在视口 */
  top: 0;
  left: 0;
  width: 100vw;
  /* 拉伸占满全屏 */
  height: 100vh;
  background-image: url('@/assets/img/bg1.jpg');
  background-size: cover;
  /* 拉伸裁剪为最大，保持比例 */
  background-repeat: no-repeat;
  background-position: center;
  z-index: -1;
  /* 放到内容后面 */
}

@media (max-width: 1000px) {
  .bg {
    position: fixed;
    /* 固定在视口 */
    top: 0;
    left: 0;
    width: 100vw;
    /* 拉伸占满全屏 */
    height: 100vh;
    background-image: url('@/assets/img/bg2.png');
    background-size: cover;
    /* 拉伸裁剪为最大，保持比例 */
    background-repeat: no-repeat;
    background-position: center;
    z-index: -1;
    /* 放到内容后面 */
  }

  .texiao {
    display: none;
  }

  .leftcolumn {
    display: none;
  }
}
</style>