<template>
  <section class="hero">
    <div class="hero__overlay"></div>
    <div class="hero__content">
      <p class="hero__greeting">{{ greeting }}</p>
      <h1 class="hero__title">{{ ui.webSetting?.web_name || 'My Blog' }}</h1>
      <p class="hero__subtitle">{{ ui.webSetting?.footer_text1 || '记录思考，分享生活' }}</p>
      <div class="hero__scroll-hint" @click="scrollDown">
        <span class="scroll-arrow">↓</span>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()

const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 6) return '✨ 夜深了'
  if (hour < 12) return '☀️ 早上好'
  if (hour < 18) return '🌤 下午好'
  return '🌙 晚上好'
})

function scrollDown() {
  window.scrollBy({ top: window.innerHeight, behavior: 'smooth' })
}

onMounted(() => {
  ui.fetchWebSetting()
})
</script>

<style scoped>
.hero {
  position: relative;
  height: 100dvh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e9f0 30%, #d4dce6 60%, #c8d6e5 100%);
}

.dark .hero {
  background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 40%, #16213e 70%, #0f3460 100%);
}

.hero__overlay {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 50% -20%, rgba(99, 102, 241, 0.12), transparent),
    radial-gradient(ellipse 60% 40% at 80% 80%, rgba(139, 92, 246, 0.08), transparent);
  pointer-events: none;
}

.dark .hero__overlay {
  background:
    radial-gradient(ellipse 80% 50% at 50% -20%, rgba(129, 140, 248, 0.1), transparent),
    radial-gradient(ellipse 60% 40% at 80% 80%, rgba(167, 139, 250, 0.06), transparent);
}

.hero__content {
  position: relative;
  text-align: center;
  z-index: 1;
  padding: 32px;
  animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero__greeting {
  font-size: 15px;
  font-weight: 500;
  color: var(--color-text-mute);
  margin-bottom: 16px;
  letter-spacing: 1px;
}

.hero__title {
  font-size: clamp(36px, 6vw, 64px);
  font-weight: 800;
  color: var(--color-heading);
  margin: 0 0 16px;
  letter-spacing: -2px;
  line-height: 1.1;
}

.hero__subtitle {
  font-size: 18px;
  color: var(--color-text-mute);
  margin: 0;
  font-weight: 400;
  line-height: 1.6;
}

.hero__scroll-hint {
  position: absolute;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  cursor: pointer;
  animation: bounce 2s infinite;
}

.scroll-arrow {
  font-size: 24px;
  color: var(--color-text-mute);
  opacity: 0.5;
  transition: opacity 0.2s;
}

.hero__scroll-hint:hover .scroll-arrow {
  opacity: 1;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateX(-50%) translateY(0);
  }
  40% {
    transform: translateX(-50%) translateY(-8px);
  }
  60% {
    transform: translateX(-50%) translateY(-4px);
  }
}
</style>
