<script setup>
import { computed, ref, onMounted, onUnmounted } from "vue";
import { useRoute } from "vue-router";
import { useThemeStore } from "@/stores/theme";

import MeteorBackground from "@/components/MeteorBackground.vue";
import PointerTextTrail from '@/components/PointerTextTrail.vue';
import navbar from "@/views/Layout/components/nav.vue"
import footera from "@/views/Layout/components/Footer.vue"
import Welcome from '@/components/welcome.vue'
import About from '@/components/about.vue';
import RandomArticle from '@/components/RandomArticle.vue'
import Clock from '@/components/clock2.vue';
import Loading from "@/components/loading.vue"
import TrailToggle from "@/components/TrailToggle.vue"

import { useArticleStore } from "@/stores/article"
import { useWebSettingStore } from "@/stores/WebSetting";
import { useTagsStore } from "@/stores/tags";

const articleStore = useArticleStore()
const WebSettingStore = useWebSettingStore()
const tagsStore = useTagsStore()

const route = useRoute();
const themeStore = useThemeStore();

const loadingRef = ref(null);

const windowWidth = ref(window.innerWidth);

// 监听窗口大小变化
const handleResize = () => {
  windowWidth.value = window.innerWidth;
};

onMounted(() => {
  themeStore.initTrail()
  document.addEventListener('visibilitychange', handleVisibilityChange);
  window.addEventListener('resize', handleResize);
  articleStore.fetchArticles()
  WebSettingStore.fetchWebSetting()
  tagsStore.fetchTags()

  window.addEventListener('load', () => {
    if (loadingRef.value) {
      loadingRef.value.setResourceLoaded();
    }
  });

});

onUnmounted(() => {
  document.removeEventListener('visibilitychange', handleVisibilityChange);
  window.removeEventListener('resize', handleResize);
});

// 动态计算 header 高度
const headerHeight = computed(() => {
  if (route.name === "Home") return "100vh";
  if (route.name === "ArticleDetail") return "300px"; // 可按需改
  return "300px";
});

// 记录初始标题
const originalTitle = document.title;
let timeoutId = null;

const handleVisibilityChange = () => {
  // 清除之前的定时器，防止冲突
  if (timeoutId) clearTimeout(timeoutId);

  if (document.hidden) {
    // 用户离开标签页
    document.title = '在暗处，有双眼睛盯着你';
  } else {
    // 用户回到标签页
    document.title = '喵~（目移）';
    
    // 1.5秒后恢复原网页标题
    timeoutId = setTimeout(() => {
      document.title = originalTitle;
    }, 1500);
  }
};
</script>

<template>
  <Loading ref="loadingRef" />

  <transition name="fade">
    <MeteorBackground v-if="themeStore.isDark" key="night" />
    <div v-else class="bg" key="day" />
  </transition>
  <PointerTextTrail class="texiao" v-if="themeStore.showTrail" />

  <el-backtop :right="40" :bottom="100"  style="color: #fcbad3;">
    <div
      style="
        height: 100%;
        width: 100%;
        border-radius: var(--border-radius);
        background-color: var(--el-bg-color-overlay);
        box-shadow: var(--el-box-shadow-lighter);
        text-align: center;
        line-height: 40px;
      "
    >
    UP
    </div>
  </el-backtop>

  <TrailToggle />

  <navbar />

  <main class="main-content">
    <div class="header" :style="{ height: headerHeight }">
      <Welcome v-if="route.name === 'Home'" />
    </div>
    <div class="content">
      <div class="row">
        <div class="leftcolumn">
            <About class="fade-in" v-fade-in />
            <div class="sticky-container fade-in" v-fade-in>
              <Clock class="clock-wrapper" />
              <RandomArticle class="RandomArticle" />
            </div>
        </div>

        <div class="rightcolumn">
          <router-view v-slot="{ Component }">
            <transition name="route-fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </div>
    </div>
  </main>

  <footera />
</template>

<style scoped>
.main-content{
  min-height: 100vh;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.8s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.route-fade-enter-active,
.route-fade-leave-active {
  transition: all 0.4s ease;
}

.route-fade-enter-from {
  opacity: 0;
  transform: translateY(10px); /* 增加一点向上滑入的效果，更灵动 */
}

.route-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px); /* 向上滑出 */
}



.icon {
  width: 15px;
  height: 15px;
  color: #fcbad3;
  fill: #fcbad3;
  stroke: #fcbad3;
}

.header {
  transition: height 0.5s ease;
  /* 动画过渡更自然 */
}

.row {
  display: flex;
  gap: 20px;
  max-width: 1100px;
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
  top: 80px;
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