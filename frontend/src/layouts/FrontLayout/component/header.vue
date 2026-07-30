<template>
  <section class="hero">
    <div class="hero__overlay"></div>
    <div class="hero__content">
      <p class="hero__info">{<span class="bounce"> CODE/GAME </span>}</p>
      <h1 class="hero__title">{{ ui.webSetting?.web_name || 'My Blog' }}</h1>
      <p class="hero__subtitle">{{ ui.webSetting?.footer_text1 || '记录思考，分享生活' }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()

</script>

<style scoped>
.hero {
  position: relative;
  height: 100dvh;
  display: flex;
  overflow: hidden;
  pointer-events: none;
  width: 100%;
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
  left: 25%;
  top: 30%;
  position: relative;
  z-index: 1;
  padding: 32px;
  animation: fadeInUp 0.8s ease-out;
  color: var(--color-text);
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



.bounce {
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  border: 1px solid whitesmoke;
  padding: 4px 6px;
}

.hero__title {
  font-size: 8rem;
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

@keyframes bounce {

  0%,
  20%,
  50%,
  80%,
  100% {
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
