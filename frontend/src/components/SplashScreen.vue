<script setup lang="ts">
import { ref } from 'vue'

const show = ref(true)
const closing = ref(false)

function close() {
  closing.value = true
  setTimeout(() => {
    show.value = false
  }, 1000)
}

defineExpose({ close })
</script>

<template>
  <div v-if="show" class="splash" :class="{ 'splash--closing': closing }">
    <div class="splash__bg"></div>
    <div class="splash__center">
      <div class="loader">
        <div class="loader__inner"></div>
        <div class="loader__orbit">
          <div class="loader__dot"></div>
          <div class="loader__dot"></div>
          <div class="loader__dot"></div>
          <div class="loader__dot"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.splash {
  position: fixed;
  inset: 0;
  z-index: 10000;
  pointer-events: none;
}

/* ========== 背景层 ========== */
.splash__bg {
  position: fixed;
  inset: 0;
  background: #2c2c2c;
  z-index: 10001;
  transition: transform 0.8s cubic-bezier(0.77, 0, 0.175, 1);
}

/* 左侧透明渐变遮罩 */
.splash__bg::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 80px;
  height: 100%;
  background: linear-gradient(to right, transparent, #2c2c2c);
}

.splash--closing .splash__bg {
  transform: translateX(100%);
}

/* ========== 居中内容 ========== */
.splash__center {
  position: fixed;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10002;
}

/* ========== Loader ========== */
.loader {
  position: relative;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: radial-gradient(circle,
      rgba(255, 255, 255, 0.05) 30%,
      transparent 70%);
}

/* 外圈 */
.loader::before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 4px solid transparent;
  border-top-color: rgba(255, 255, 255, 0.6);
  animation: loader-spin 2s linear infinite;
}

/* 旋转光晕 */
.loader::after {
  content: "";
  position: absolute;
  inset: 10%;
  border-radius: 50%;
  background: conic-gradient(from 90deg, rgba(255, 255, 255, 0.2), transparent);
  filter: blur(2px);
  animation: loader-spin-reverse 1.5s linear infinite;
}

/* 中心小球 */
.loader__inner {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 30px;
  height: 30px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.6);
  animation: loader-pulse 1s ease-in-out infinite;
  transition: transform 0.6s cubic-bezier(0.55, 0, 1, 0.45), opacity 0.3s ease;
}

.splash--closing .loader__inner {
  transform: translate(calc(-50vw - 100px), -50%);
  left: -8%;
  animation: none;
}

/* 轨道 */
.loader__orbit {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  animation: orbit-rotate 3s linear infinite;
  transition: opacity 0.5s ease;
}

.splash--closing .loader__orbit {
  opacity: 0;
}

/* 轨道上的点 */
.loader__dot {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 8px;
  height: 8px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
}

.loader__dot:nth-child(1) {
  transform: rotate(0deg) translate(60px);
}

.loader__dot:nth-child(2) {
  transform: rotate(90deg) translate(60px);
}

.loader__dot:nth-child(3) {
  transform: rotate(180deg) translate(60px);
}

.loader__dot:nth-child(4) {
  transform: rotate(270deg) translate(60px);
}

/* ========== 关闭时 loader 伪元素淡出 ========== */
.splash--closing .loader::before,
.splash--closing .loader::after {
  opacity: 0;
  transition: opacity 0.4s ease;
}

/* ========== 动画 ========== */
@keyframes loader-spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

@keyframes loader-spin-reverse {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(-360deg);
  }
}

@keyframes loader-pulse {

  0%,
  100% {
    transform: translate(-50%, -50%) scale(1);
  }

  50% {
    transform: translate(-50%, -50%) scale(1.2);
  }
}

@keyframes orbit-rotate {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>
