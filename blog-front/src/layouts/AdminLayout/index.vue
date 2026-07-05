<template>
  <div class="admin-layout" :class="{ collapsed: ui.sidebarCollapsed }">
    <aside class="admin-sidebar">
      <div class="sidebar-header">
        <RouterLink to="/admin/dashboard" class="admin-logo">Blog Admin</RouterLink>
      </div>
      <nav class="sidebar-nav">
        <RouterLink to="/admin/dashboard" active-class="active">📊 仪表盘</RouterLink>

        <div class="nav-dropdown" @mouseenter="showArticleMenu = true" @mouseleave="showArticleMenu = false">
          <RouterLink to="/admin/articles" active-class="active" class="nav-dropdown-trigger">📝 文章管理 <span
              class="arrow">▾</span></RouterLink>
          <div v-show="showArticleMenu" class="nav-dropdown-menu">
            <RouterLink to="/admin/article/edit" active-class="active">✏️ 创建文章</RouterLink>
            <RouterLink to="/admin/article/upload" active-class="active">📤 上传文章</RouterLink>
          </div>
        </div>

        <RouterLink to="/admin/prohibited-words" active-class="active">🚫 违禁词管理</RouterLink>
        <RouterLink to="/admin/comments" active-class="active">💬 评论管理</RouterLink>
        <RouterLink to="/admin/message" active-class="active">📩 留言管理</RouterLink>
        <RouterLink to="/admin/tags" active-class="active">🏷️ 标签管理</RouterLink>
        <RouterLink to="/admin/users" active-class="active">👤 用户管理</RouterLink>
        <RouterLink to="/admin/settings" active-class="active">⚙️ 网站设置</RouterLink>
      </nav>
    </aside>

    <div class="admin-right">
      <header class="admin-topbar">
        <a href="/">返回首页</a>
        <span class="username">{{ auth.username }}</span>
        <button class="theme-toggle" @click="ui.toggleTheme">
          {{ ui.isDark ? '☀️' : '🌙' }}
        </button>
        <button class="logout-btn" @click="auth.logout">退出</button>
      </header>
      <main class="admin-main">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'

const auth = useAuthStore()
const ui = useUiStore()
const showArticleMenu = ref(false)
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100dvh;
}

.admin-sidebar {
  width: 240px;
  background: var(--color-background-mute);
  border-right: 1px solid var(--color-border);
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  transition: width 0.3s;
}

.admin-layout.collapsed .admin-sidebar {
  width: 64px;
}

.sidebar-header {
  padding: 0 20px 20px;
  border-bottom: 1px solid var(--color-border);
  margin-bottom: 12px;
}

.admin-logo {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-heading);
  text-decoration: none;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 0 12px;
}

.sidebar-nav a {
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 14px;
  color: var(--color-text);
  text-decoration: none;
  transition: background 0.2s;
}

.sidebar-nav a:hover {
  background: var(--color-border);
}

.sidebar-nav a.active {
  background: var(--color-heading);
  color: #fff;
  font-weight: 600;
}

.nav-dropdown {
  position: relative;
}

.nav-dropdown-trigger {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 14px;
  color: var(--color-text);
  cursor: pointer;
  transition: background 0.2s;
}

.nav-dropdown-trigger:hover {
  background: var(--color-border);
}

.nav-dropdown-trigger .arrow {
  font-size: 10px;
  margin-left: auto;
}

.nav-dropdown-menu {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 4px 0 4px 12px;
}

.nav-dropdown-menu a {
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 13px;
  color: var(--color-text);
  text-decoration: none;
  transition: background 0.2s;
}

.nav-dropdown-menu a:hover {
  background: var(--color-border);
}

.nav-dropdown-menu a.active {
  background: var(--color-heading);
  color: #fff;
  font-weight: 600;
}

.admin-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.admin-topbar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 24px;
  height: 56px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-background);
}

.collapse-btn {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: var(--color-text);
}

.admin-topbar .username {
  font-size: 14px;
  color: var(--color-text);
  margin-left: auto;
}

.admin-topbar .theme-toggle {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
}

.logout-btn {
  padding: 6px 14px;
  border-radius: 6px;
  border: 1px solid var(--color-border);
  background: var(--color-background);
  color: var(--color-text);
  font-size: 13px;
  cursor: pointer;
  transition: background 0.2s;
}

.logout-btn:hover {
  background: var(--color-background-mute);
}

.admin-main {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}
</style>
