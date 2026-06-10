<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch, computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import ArticleToc from '@/components/ArticleToc.vue'
import ThemeToggle from '@/components/ThemeToggle.vue'
import About from '@/components/about.vue';
import { useWebSettingStore } from '@/stores/WebSetting'

const route = useRoute()
const showSidebar = ref(false)
const toggleSidebar = () => (showSidebar.value = !showSidebar.value)
const closeSidebar = () => (showSidebar.value = false)
const WebSetting = useWebSettingStore()

// 滚动控制逻辑
const isNavbarVisible = ref(true)
const lastScrollPosition = ref(0)
const navbarTransparent = ref(true)

const handleScroll = () => {
  const currentScroll = window.pageYOffset || document.documentElement.scrollTop
  navbarTransparent.value = currentScroll < 1

  if (currentScroll <= 10) {
    isNavbarVisible.value = true
  } else if (currentScroll > lastScrollPosition.value && currentScroll > 100) {
    isNavbarVisible.value = false
  } else if (currentScroll < lastScrollPosition.value) {
    isNavbarVisible.value = true
  }
  lastScrollPosition.value = currentScroll
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
})
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

const isPostPage = computed(() => route.name === "ArticleDetail");

// ======== 滑块逻辑 ========
const navRef = ref(null)
const activeBarStyle = ref({ left: '0px', width: '0px' })

const updateActiveBar = () => {
  nextTick(() => {
    const activeLink = navRef.value?.querySelector('.router-link-active')
    if (activeLink) {
      const rect = activeLink.getBoundingClientRect()
      const parentRect = navRef.value.getBoundingClientRect()
      activeBarStyle.value = {
        left: `${rect.left - parentRect.left}px`,
        width: `${rect.width}px`
      }
    }
  })
}

onMounted(updateActiveBar)
watch(() => route.path, updateActiveBar)


</script>


<template>
  <nav class="navbar" :class="{ 'navbar-hidden': !isNavbarVisible, 'navbar-transparent': navbarTransparent }">
    <div class="navbar-inner">
      <div class="logo">
        <RouterLink to="/" exact-active-class="router-link-active">
          <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
            <path fill="currentColor" d="M288 128h608L736 384l160 256H288v320h-96V64h96z"></path>
          </svg>
          {{ WebSetting.WebSettingList.name }}
        </RouterLink>
      </div>

      <!-- 桌面导航 -->
      <div class="nav-wrapper" ref="navRef">
        <ul class="nav-links desktop-nav">
          <li>
            <RouterLink to="/" exact-active-class="router-link-active">
              <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
                <path fill="currentColor" d="M512 128 128 447.936V896h255.936V640H640v256h255.936V447.936z"></path>
              </svg>
              首页
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/file" exact-active-class="router-link-active">
              <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
                <path fill="currentColor"
                  d="M192 736h640V128H256a64 64 0 0 0-64 64zm64-672h608a32 32 0 0 1 32 32v672a32 32 0 0 1-32 32H160l-32 57.536V192A128 128 0 0 1 256 64">
                </path>
                <path fill="currentColor"
                  d="M240 800a48 48 0 1 0 0 96h592v-96zm0-64h656v160a64 64 0 0 1-64 64H240a112 112 0 0 1 0-224m144-608v250.88l96-76.8 96 76.8V128zm-64-64h320v381.44a32 32 0 0 1-51.968 24.96L480 384l-108.032 86.4A32 32 0 0 1 320 445.44z">
                </path>
              </svg>
              归档
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/about" exact-active-class="router-link-active">
              <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
                <path fill="currentColor"
                  d="M288 320a224 224 0 1 0 448 0 224 224 0 1 0-448 0m544 608H160a32 32 0 0 1-32-32v-96a160 160 0 0 1 160-160h448a160 160 0 0 1 160 160v96a32 32 0 0 1-32 32z">
                </path>
              </svg>
              关于
            </RouterLink>
          </li>
        </ul>
      </div>

      <ThemeToggle class="theme-toggle" />
      <!-- 移动端菜单 -->
      <div class="menu-actions">
        <el-dropdown placement="bottom-end" class="mobile-dropdown" v-if="isPostPage">
          <el-button class="nav-button">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
              <path fill="currentColor"
                d="M128 192h768v128H128zm0 256h512v128H128zm0 256h768v128H128zm576-352 192 160-192 128z">
              </path>
            </svg>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <ArticleToc />
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <button class="menu-button" @click="toggleSidebar">☰</button>
      </div>
    </div>

    <!-- 侧边栏 -->
    <teleport to="body">
      <transition name="fade">
        <div v-show="showSidebar" class="overlay" @click="closeSidebar"></div>
      </transition>

      <transition name="slide">
        <div class="sidebar" v-show="showSidebar">
          <About />
          <ul class="nav-links mobile-nav">
            <li @click="closeSidebar">
              <RouterLink to="/" exact-active-class="router-link-active">
                <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
                  <path fill="currentColor" d="M512 128 128 447.936V896h255.936V640H640v256h255.936V447.936z"></path>
                </svg>
                首页
              </RouterLink>
            </li>
            <li @click="closeSidebar">
              <RouterLink to="/file" exact-active-class="router-link-active">
                <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
                  <path fill="currentColor"
                    d="M192 736h640V128H256a64 64 0 0 0-64 64zm64-672h608a32 32 0 0 1 32 32v672a32 32 0 0 1-32 32H160l-32 57.536V192A128 128 0 0 1 256 64">
                  </path>
                  <path fill="currentColor"
                    d="M240 800a48 48 0 1 0 0 96h592v-96zm0-64h656v160a64 64 0 0 1-64 64H240a112 112 0 0 1 0-224m144-608v250.88l96-76.8 96 76.8V128zm-64-64h320v381.44a32 32 0 0 1-51.968 24.96L480 384l-108.032 86.4A32 32 0 0 1 320 445.44z">
                  </path>
                </svg>
                归档
              </RouterLink>
            </li>
            <li @click="closeSidebar">
              <RouterLink to="/about" exact-active-class="router-link-active">
                <svg class="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
                  <path fill="currentColor"
                    d="M288 320a224 224 0 1 0 448 0 224 224 0 1 0-448 0m544 608H160a32 32 0 0 1-32-32v-96a160 160 0 0 1 160-160h448a160 160 0 0 1 160 160v96a32 32 0 0 1-32 32z">
                  </path>
                </svg>
                关于
              </RouterLink>
            </li>
          </ul>
        </div>
      </transition>
    </teleport>
  </nav>
</template>

<style scoped>
/* ===== 顶部导航基础样式 ===== */
.navbar {
  height: 72px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  margin: 10px auto;
  transition: all 0.5s ease;
  z-index: 150;
}

.navbar-transparent {
  background: transparent;
  box-shadow: none;
}

.navbar-hidden {
  transform: translateY(-200%);
}

.navbar-inner {
  height: 100%;
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  background: var(--nav-color);
  backdrop-filter: blur(10px);
  border-radius: var(--border-radius);
  /* border-style:solid; */
  border: var(--border);
  box-shadow: var(--box-shadow);
}

.logo {
  margin-right: auto;
}

.logo a {
  border-radius: 5px;
  text-decoration: none;
  color: #ffb6b9;
  font-weight: 800;
  position: relative;
  padding: 0.4rem 1.25rem;
  transition: 0.5s ease;
}

.logo a:hover {
  background-color: #fae3d9;
}

.icon {
  width: 20px;
  vertical-align: middle;
}

.nav-button {
  background: none !important;
  border: none !important;
  box-shadow: none !important;
  color: var(--text-color);
  font-weight: 500;
  border-radius: 5px;
  padding: 0.4rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: 0.5s ease;
}

.nav-button:hover {
  color: #ffb6b9;
  background-color: #fae3d9;
}

.nav-button svg {
  width: 20px;
  vertical-align: middle;
}

/* ===== 桌面导航 ===== */
.nav-wrapper {
  position: relative;
}

.nav-links {
  display: flex;
  gap: 20px;
  list-style: none;
  margin: 0;
  padding: 0;
  transition: color 0.5s ease;
}

.nav-links a {
  border-radius: 5px;
  text-decoration: none;
  color: var(--text-color);
  font-weight: 500;
  position: relative;
  padding: 0.4rem 1.25rem;
  transition: 0.5s ease;
}

.nav-links a:hover {
  background-color: #fae3d9;

}


/* ===== 移动端菜单 ===== */
.menu-actions {
  display: none;
  transition: 0.5s ease;
}

.menu-button {
  font-size: 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
}

/* ===== 侧边栏 ===== */
.sidebar {
  position: fixed;
  top: 0;
  right: 0;
  width: 200px;
  height: 100vh;
  background-color: var(--bg-color);
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  z-index: 1101;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.mobile-nav {
  display: flex;
  flex-direction: column;
}

.mobile-nav a {
  text-decoration: none;
  color: var(--text-color);
  border: 1px solid #aaa;
  padding: 6px 12px;
  border-radius: 8px;
  transition: background 0.3s;
}



.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.4);
  z-index: 1100;
}

/* ===== 动画 ===== */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ===== 响应式 ===== */
@media (max-width: 768px) {
  .navbar-inner {
    justify-content: flex-start;
  }

  .navbar {
    margin: 0 auto;
    width: 100%;
  }

  .desktop-nav {
    display: none;
  }

  /* 右侧区域：夜间按钮 + 菜单 */
  .theme-toggle,
  .menu-actions {
    display: flex;
    align-items: center;
  }

  .theme-toggle {
    margin-right: 6px;
    /* 调整间距 */
  }

  .menu-actions {
    gap: 8px;
  }
}
</style>
