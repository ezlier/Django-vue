<template>
  <div class="front-layout">
    <header class="front-header">
      <nav class="front-nav">
        <RouterLink to="/home" class="logo">{{ ui.webSetting?.web_name || 'Blog' }}</RouterLink>
        <div class="nav-links">
          <RouterLink to="/home">首页</RouterLink>
          <RouterLink to="/archive">归档</RouterLink>
          <RouterLink to="/about">关于</RouterLink>
          <button class="theme-toggle" @click="ui.toggleTheme">
            {{ ui.isDark ? '☀️' : '🌙' }}
          </button>
        </div>
      </nav>
    </header>

    <main class="front-main">
      <RouterView v-slot="{ Component }">
        <KeepAlive>
          <component :is="Component" />
        </KeepAlive>
      </RouterView>
    </main>

    <footer class="front-footer">
      <p>{{ ui.webSetting?.footer_text1 || '' }}</p>
      <p>{{ ui.webSetting?.footer_text2 || '' }}</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()

onMounted(() => {
  ui.fetchWebSetting()
})
</script>
