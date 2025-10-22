<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()
const showSidebar = ref(false)
const toggleSidebar = () => (showSidebar.value = !showSidebar.value)
const closeSidebar = () => (showSidebar.value = false)

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
      <div class="logo">LOGO</div>

      <!-- 桌面导航 -->
      <div class="nav-wrapper" ref="navRef">
        <ul class="nav-links desktop-nav">
          <li><RouterLink to="/" exact-active-class="router-link-active">首页</RouterLink></li>
          <li><RouterLink to="/file" exact-active-class="router-link-active">归档</RouterLink></li>
          <li><RouterLink to="/about" exact-active-class="router-link-active">关于</RouterLink></li>
        </ul>
      </div>

      <!-- 移动端菜单 -->
      <div class="menu-actions">
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
          <h2>导航菜单</h2>
          <ul class="nav-links mobile-nav">
            <li @click="closeSidebar"><RouterLink to="/" exact-active-class="router-link-active">首页</RouterLink></li>
            <li @click="closeSidebar"><RouterLink to="/file" exact-active-class="router-link-active">归档</RouterLink></li>
            <li @click="closeSidebar"><RouterLink to="/about" exact-active-class="router-link-active">关于</RouterLink></li>
          </ul>
        </div>
      </transition>
    </teleport>
  </nav>
</template>

<style scoped>
/* ===== 顶部导航基础样式 ===== */
.navbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  transition: all 0.5s ease;
  z-index: 1000;
}

.navbar-transparent {
  background: transparent;
  box-shadow: none;
}

.navbar-hidden {
  transform: translateY(-100%);
}

.navbar-inner {
  max-width: 1280px;
  margin: 0 auto;
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 20px;
}

.logo {
  font-size: 1.2rem;
  font-weight: bold;
}

/* ===== 桌面导航 ===== */
.nav-wrapper {
  position: relative;
}

.nav-links {
  display: flex;
  gap: 20px;
  list-style: none;
  margin: 0; padding: 0;
  transition: color 0.5s ease;
}

.nav-links a {
  border-radius: 5px;
  text-decoration: none;
  color: black;
  font-weight: 500;
  position: relative;
  padding: 5px 10px;
  transition: color 0.5s ease;
}

.nav-links a:hover {
  color: #1a1a1a;
  background-color: #fcbad3;

}


/* ===== 移动端菜单 ===== */
.menu-actions { display: none; }
.menu-button {
  font-size: 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
}

/* ===== 侧边栏 ===== */
.sidebar {
  position: fixed;
  top: 0; right: 0;
  width: 200px; height: 100vh;
  background-color: white;
  box-shadow: -2px 0 10px rgba(0,0,0,0.1);
  padding: 20px;
  z-index: 1101;
  display: flex; flex-direction: column;
  align-items: center;
  gap: 20px;
}

.mobile-nav {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.mobile-nav a {
  text-decoration: none;
  color: #333;
  border: 1px solid #aaa;
  padding: 6px 12px;
  border-radius: 8px;
  transition: background 0.3s;
}

.mobile-nav a.router-link-active {
  background-color: #6b8afd;
  color: #fff;
}

.overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  background-color: rgba(0,0,0,0.4);
  z-index: 1100;
}

/* ===== 动画 ===== */
.slide-enter-active, .slide-leave-active {
  transition: transform 0.3s ease;
}
.slide-enter-from, .slide-leave-to {
  transform: translateX(100%);
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* ===== 响应式 ===== */
@media (max-width: 768px) {
  .desktop-nav { display: none; }
  .menu-actions { display: block; }
}
</style>
