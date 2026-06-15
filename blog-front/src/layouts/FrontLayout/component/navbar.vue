<template>
  <nav class="navbar" :class="{ 'navbar--scrolled': scrolled }">
    <div class="navbar__inner">
      <RouterLink to="/home" class="navbar__logo">
        {{ ui.webSetting?.web_name || 'Blog' }}
      </RouterLink>

      <div class="navbar__links">
        <RouterLink to="/home" class="navbar__link" active-class="navbar__link--active">首页</RouterLink>
        <RouterLink to="/archive" class="navbar__link" active-class="navbar__link--active">归档</RouterLink>
        <RouterLink to="/about" class="navbar__link" active-class="navbar__link--active">关于</RouterLink>
        <button class="navbar__theme-btn" @click="ui.toggleTheme" :aria-label="ui.isDark ? '切换亮色模式' : '切换暗色模式'">
          <span v-if="ui.isDark" class="theme-icon">☀️</span>
          <span v-else class="theme-icon">🌙</span>
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()
const scrolled = ref(false)

function onScroll() {
  scrolled.value = window.scrollY > 50
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  onScroll() // 初始化滚动状态
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
})
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  transition: background 0.3s ease, box-shadow 0.3s ease, backdrop-filter 0.3s ease;
}

.navbar--scrolled {
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(12px) saturate(180%);
  -webkit-backdrop-filter: blur(12px) saturate(180%);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

.dark .navbar--scrolled {
  background: rgba(15, 15, 15, 0.78);
  backdrop-filter: blur(12px) saturate(180%);
  -webkit-backdrop-filter: blur(12px) saturate(180%);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.navbar__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
}

.navbar__logo {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-heading);
  text-decoration: none;
  letter-spacing: -0.5px;
  transition: opacity 0.2s;
}

.navbar__logo:hover {
  opacity: 0.7;
}

.navbar__links {
  display: flex;
  align-items: center;
  gap: 8px;
}

.navbar__link {
  padding: 6px 16px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  color: var(--color-text);
  text-decoration: none;
  transition: background 0.2s, color 0.2s;
}

.navbar__link:hover {
  background: rgba(0, 0, 0, 0.05);
}

.dark .navbar__link:hover {
  background: rgba(255, 255, 255, 0.08);
}

.navbar__link--active {
  color: var(--color-primary);
  background: rgba(99, 102, 241, 0.08);
}

.dark .navbar__link--active {
  background: rgba(129, 140, 248, 0.12);
}

.navbar__theme-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: none;
  background: rgba(0, 0, 0, 0.04);
  cursor: pointer;
  font-size: 16px;
  transition: background 0.2s, transform 0.15s;
  margin-left: 4px;
}

.navbar__theme-btn:hover {
  background: rgba(0, 0, 0, 0.08);
  transform: scale(1.08);
}

.dark .navbar__theme-btn {
  background: rgba(255, 255, 255, 0.06);
}

.dark .navbar__theme-btn:hover {
  background: rgba(255, 255, 255, 0.12);
}

.theme-icon {
  line-height: