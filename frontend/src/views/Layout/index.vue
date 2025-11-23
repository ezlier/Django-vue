<script setup>
import { computed, ref } from "vue";
import { useRoute } from "vue-router";
import { useThemeStore } from "@/stores/theme";
import MeteorBackground from "@/components/MeteorBackground.vue";

import PointerTextTrail from '@/components/PointerTextTrail.vue';
import navbar from "@/views/Layout/components/nav.vue"
import footera from "@/views/Layout/components/Footer.vue"
import Welcome from '@/components/welcome.vue'
import About from '@/components/about.vue';
import RandomArticle from '@/components/RandomArticle.vue'
import Clock from '@/components/clock.vue';
import ArticleToc from '@/components/ArticleToc.vue'


const route = useRoute();
const themeStore = useThemeStore();

const showTrail = ref(true);

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
  <transition name="fade">
    <MeteorBackground v-if="themeStore.isDark" key="night" />
    <div v-else class="bg" key="day" />
  </transition>
  <PointerTextTrail class="texiao" v-if="showTrail" />
  <el-backtop :right="40" :bottom="100" style="color: #fcbad3;" />

  <div class="trail-toggle">
    <button class="trail-btn" @click="showTrail = !showTrail">
      <svg v-if="showTrail" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" class="icon">
        <path fill="currentColor"
          d="M4.89.188a.505.505 0 0 0-.555-.16a.5.5 0 0 0-.334.472v13a.5.5 0 0 0 .625.484a.5.5 0 0 0 .254-.16l2.44-2.85l1.71 4.7a.497.497 0 0 0 .641.3a.497.497 0 0 0 .299-.641l-1.73-4.75l4.21.42a.502.502 0 0 0 .548-.542a.5.5 0 0 0-.108-.268l-8-10zm.11 12v-10.2l6.37 7.96l-3.82-.383a.5.5 0 0 0-.43.173L5 12.208z" />
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon">
        <g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
          <path
            d="M2.034 2.681a.498.498 0 0 1 .647-.647l9 3.5a.5.5 0 0 1-.033.944L8.204 7.545a1 1 0 0 0-.66.66l-1.066 3.443a.5.5 0 0 1-.944.033z" />
          <circle cx="16" cy="16" r="6" />
          <path d="m11.8 11.8l8.4 8.4" />
        </g>
      </svg>
    </button>
  </div>

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
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.8s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.trail-toggle {
  position: fixed;
  right: 40px;
  bottom: 40px;
  z-index: 9999;
}

.trail-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--el-bg-color);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  border: 2px solid var(--el-bg-color);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s ease;
}


.trail-btn:hover {
  transform: scale(1.1);
}


.icon {
  width: 15px;
  height: 15px;
  color: #fcbad3;
  fill: #fcbad3;
  stroke: #fcbad3;
}

.content {
  border-top-left-radius: 1.125rem;
  border-top-right-radius: 1.125rem;
  background-color: var(--bg-content);
}

.header {
  transition: height 0.5s ease;
  /* 动画过渡更自然 */
}

.row {
  display: flex;
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

  .trail-toggle {
    display: none;
  }

  .leftcolumn {
    display: none;
  }
}
</style>