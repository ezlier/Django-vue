<template>
  <div ref="container" class="text-container"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

// === 配置常量 ===
const TEXT = '◊◊◊◊◊◊◊'
const BASE_FONT_SIZE = 36
const ROTATE_SPEED = 0.01
const SMOOTHING = 0.15
const RT_SMOOTHING = 0.3
const RAINBOW_SPEED = 0.01

// === 响应式引用和变量 ===
const container = ref(null)
let chars = []
let circleGuide = null
let circleRotateAngle = 0
let hue = 0
let isRotate = false
let idTimer = null
let animationId = null
let mouseX = window.innerWidth / 2
let mouseY = window.innerHeight / 2

// === 工具函数 ===
function lerp(start, end, t) {
  return start * (1 - t) + end * t
}

// === 初始化字符和引导线 ===
function initChars() {
  if (!container.value) return

  // 清空旧内容
  container.value.innerHTML = ''
  chars = []

  for (let i = 0; i < TEXT.length; i++) {
    const char = document.createElement('div')
    char.className = 'char'
    char.textContent = TEXT[i]
    char.style.fontSize = `${BASE_FONT_SIZE}px`
    char.dataset.x = mouseX
    char.dataset.y = mouseY
    char.style.left = `${mouseX}px`
    char.style.top = `${mouseY}px`
    char.style.color = `hsl(${(i / TEXT.length) * 360}, 100%, 75%)`

    container.value.appendChild(char)
    chars.push(char)
  }

  // 引导圈
  circleGuide = document.createElement('div')
  circleGuide.className = 'circle-guide'
  circleGuide.style.display = 'none'
  container.value.appendChild(circleGuide)
}

// === 更新引导圈 ===
function updateCircleGuide() {
  if (!circleGuide) return

  if (isRotate) {
    const radius = Math.min(220, Math.max(100, TEXT.length * BASE_FONT_SIZE / 2.5))
    Object.assign(circleGuide.style, {
      width: `${radius * 2}px`,
      height: `${radius * 2}px`,
      left: `${mouseX}px`,
      top: `${mouseY}px`,
      display: 'block'
    })
  } else {
    circleGuide.style.display = 'none'
  }
}

// === 动画更新逻辑 ===
function updateChars() {
  updateCircleGuide()

  if (isRotate) {
    circleRotateAngle += ROTATE_SPEED
    if (circleRotateAngle >= Math.PI * 2) circleRotateAngle = 0

    const radius = Math.min(220, Math.max(100, TEXT.length * BASE_FONT_SIZE / 2.5))
    chars.forEach((char, index) => {
      const currentX = parseFloat(char.dataset.x)
      const currentY = parseFloat(char.dataset.y)
      const angle = (index / chars.length) * Math.PI * 2 + circleRotateAngle
      const targetX = mouseX + Math.cos(angle) * radius
      const targetY = mouseY + Math.sin(angle) * radius
      const newX = lerp(currentX, targetX, RT_SMOOTHING)
      const newY = lerp(currentY, targetY, RT_SMOOTHING)

      char.dataset.x = newX
      char.dataset.y = newY
      char.style.left = `${newX}px`
      char.style.top = `${newY}px`
      char.style.transform = `translate(-50%, -50%) rotate(${angle * 180 / Math.PI + 90}deg)`

      hue = (hue + RAINBOW_SPEED) % 360
      const charHue = (hue + (index / TEXT.length) * 360) % 360
      char.style.color = `hsl(${charHue}, 100%, 75%)`
    })
  } else {
    let targetX = mouseX
    let targetY = mouseY
    chars.forEach((char, index) => {
      const currentX = parseFloat(char.dataset.x)
      const currentY = parseFloat(char.dataset.y)
      const newX = lerp(currentX, targetX, SMOOTHING)
      const newY = lerp(currentY, targetY, SMOOTHING)

      char.dataset.x = newX
      char.dataset.y = newY
      char.style.left = `${newX}px`
      char.style.top = `${newY}px`

      let angle
      if (index === 0) {
        angle = Math.atan2(targetY - currentY, targetX - currentX) * 180 / Math.PI + 90
      } else {
        const prev = chars[index - 1]
        const prevX = parseFloat(prev.dataset.x)
        const prevY = parseFloat(prev.dataset.y)
        angle = Math.atan2(newY - prevY, newX - prevX) * 180 / Math.PI + 90
      }

      char.style.transform = `translate(-50%, -50%) rotate(${angle}deg)`

      hue = (hue + RAINBOW_SPEED) % 360
      const charHue = (hue + (index / TEXT.length) * 360) % 360
      char.style.color = `hsl(${charHue}, 100%, 75%)`

      targetX = newX
      targetY = newY
    })
  }

  animationId = requestAnimationFrame(updateChars)
}

// === 生命周期 ===
onMounted(() => {
  initChars()
  updateChars()

  const moveHandler = (e) => {
    mouseX = e.clientX
    mouseY = e.clientY
    clearTimeout(idTimer)
    isRotate = false
    idTimer = setTimeout(() => {
      isRotate = true
    }, 500)
  }

  const leaveHandler = () => {
    clearTimeout(idTimer)
    mouseX = window.innerWidth + 20
    mouseY = window.innerHeight + 20
  }

  window.addEventListener('mousemove', moveHandler, true)
  window.addEventListener('mouseleave', leaveHandler)
  window.addEventListener('resize', leaveHandler)

  onBeforeUnmount(() => {
    cancelAnimationFrame(animationId)
    window.removeEventListener('mousemove', moveHandler, true)
    window.removeEventListener('mouseleave', leaveHandler)
    window.removeEventListener('resize', leaveHandler)
  })
})
</script>

<style>
.text-container {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  pointer-events: none;
  z-index: 9999;
  overflow: hidden;
}

.char {
  position: absolute;
  font-size: 2.8rem;
  font-weight: bold;
  transform: translate(-50%, -50%);
  text-shadow: 0 0 15px #ffffff99;
  will-change: transform;
  user-select: none;
  pointer-events: none;
}

.circle-guide {
  position: absolute;
  border: 2px dashed #ffffff4d;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 0;
  transition: opacity 0.5s ease;
}
</style>
