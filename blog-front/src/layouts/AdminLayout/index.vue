<template>
  <div class="admin-layout" :class="{ collapsed: ui.sidebarCollapsed }">
    <aside class="admin-sidebar">
      <div class="sidebar-header">
        <RouterLink to="/admin/dashboard" class="admin-logo">Blog Admin</RouterLink>
      </div>
      <nav class="sidebar-nav">
        <RouterLink to="/admin/dashboard" active-class="active">📊 仪表盘</RouterLink>
        <RouterLink to="/admin/articles" active-class="active">📝 文章管理</RouterLink>
        <RouterLink to="/admin/comments" active-class="active">💬 评论管理</RouterLink>
        <RouterLink to="/admin/message" active-class="active">📩 留言管理</RouterLink>
        <RouterLink to="/admin/tags" active-class="active">🏷️ 标签管理</RouterLink>
        <RouterLink to="/admin/users" active-class="active">👤 用户管理</RouterLink>
        <RouterLink to="/admin/settings" active-class="active">⚙️ 网站设置</RouterLink>
      </nav>
    </aside>

    <div class="admin-right">
      <header class="admin-topbar">
        <button class="collapse-btn" @click="ui.toggleSidebar">☰</button>
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
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'

const auth = useAuthStore()
const ui = useUiStore()
</script>
