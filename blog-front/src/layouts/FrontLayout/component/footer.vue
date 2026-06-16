<template>
  <footer class="footer">
    <div class="footer__inner">
      <div class="footer__brand">
        <RouterLink to="/home" class="footer__logo">
          {{ ui.webSetting?.web_name || 'Blog' }}
        </RouterLink>
        <p class="footer__tagline">
          {{ ui.webSetting?.footer_text1 || '记录思考，分享生活' }}
        </p>
      </div>

      <div class="footer__links">
        <RouterLink to="/home">首页</RouterLink>
        <RouterLink to="/archive">归档</RouterLink>
        <RouterLink to="/about">关于</RouterLink>
        <a href="https://github.com/ezlier" target="_blank" rel="noopener">GitHub</a>
      </div>
    </div>

    <div class="footer__bottom">
      <p>&copy; {{ year }} {{ ui.webSetting?.web_name || 'Blog' }}. All rights reserved.</p>
      <p class="footer__text">{{ ui.webSetting?.footer_text2 || 'Powered by Vue & Django' }}</p>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()
const year = computed(() => new Date().getFullYear())


</script>

<style scoped>
.footer {
  padding: 24px 24px 24px;
  border-top: 1px solid var(--color-border);
  background: var(--color-background);
}

.footer__inner {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  max-width: 1280px;
  margin: 0 auto;
  gap: 32px;
  flex-wrap: wrap;
}

.footer__brand {
  flex: 1;
  min-width: 200px;
}

.footer__logo {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-heading);
  text-decoration: none;
  letter-spacing: -0.5px;
}

.footer__logo:hover {
  opacity: 0.7;
}

.footer__tagline {
  margin-top: 8px;
  font-size: 14px;
  color: var(--color-text-mute);
  line-height: 1.5;
}

.footer__links {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}

.footer__links a {
  font-size: 14px;
  color: var(--color-text);
  text-decoration: none;
  transition: color 0.2s;
}

.footer__links a:hover {
  color: var(--color-heading);
}

.footer__bottom {
  max-width: 1280px;
  margin: 10px auto 0;
  padding-top: 20px;
  border-top: 1px solid var(--color-border);
  text-align: center;
}

.footer__bottom p {
  font-size: 13px;
  color: var(--color-text-mute);
  margin: 0;
  line-height: 1.6;
}

.footer__text {
  margin-top: 4px !important;
}
</style>
