<template>
  <nav class="navbar" :class="{ 'navbar--scrolled': scrolled }">
    <div class="navbar__inner">
      <RouterLink to="/home" class="navbar__logo">
        {{ ui.webSetting?.web_name || 'Blog' }}
      </RouterLink>

      <div class="navbar__links">
        <RouterLink v-for="item in navItems" :key="item.to" :to="item.to" class="navbar__link"
          active-class="navbar__link--active">
          {{ item.label }}
        </RouterLink>
      </div>

      <el-dropdown trigger="hover" class="navbar__dropdown" popper-class="navbar__dropdown-popper">
        <button class="navbar__menu-button" type="button" aria-label="打开导航菜单">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item v-for="item in navItems" :key="item.to">
              <RouterLink :to="item.to" class="navbar__dropdown-link">
                {{ item.label }}
              </RouterLink>
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()
const scrolled = ref(false)

const navItems = [
  { to: '/home', label: '首页' },
  { to: '/archive', label: '归档' },
  { to: '/about', label: '关于' },
]

function onScroll() {
  scrolled.value = window.scrollY > 50
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  onScroll()
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

.navbar__menu-button {
  display: none;
  border: 0;
  padding: 0;
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

.navbar__backdrop,
.navbar__drawer {
  display: none;
}

.navbar__dropdown-link {
  text-decoration: none;
  color: inherit;
  display: block;
  width: 100%;
}

:global(body.navbar-menu-open) {
  overflow: hidden;
}

.navbar__dropdown {
  display: none;
}

@media (max-width: 768px) {
  .navbar {
    height: 60px;
    padding: 0 16px;
  }

  .navbar__logo {
    max-width: calc(100vw - 88px);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .navbar__links {
    display: none;
  }

  .navbar__menu-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 42px;
    height: 42px;
    flex: 0 0 42px;
    border-radius: 10px;
    color: var(--color-heading);
    background: rgba(255, 255, 255, 0.55);
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.06);
    cursor: pointer;
    transition: background 0.2s ease, transform 0.2s ease;
  }

  .dark .navbar__menu-button {
    background: rgba(255, 255, 255, 0.08);
  }

  .navbar__menu-button:active {
    transform: scale(0.94);
  }

  .navbar__menu-button svg {
    width: 24px;
    height: 24px;
    fill: none;
    stroke: currentColor;
    stroke-width: 2;
    stroke-linecap: round;
  }

  .navbar__dropdown {
    display: block;
  }
}
</style>
