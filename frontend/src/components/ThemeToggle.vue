<script setup>
import { computed } from 'vue'
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()

/**
 * 逻辑适配：
 * 因为你的 CSS 中 input:checked 代表的是“白天”（蓝色背景+太阳）
 * 而 store 中 isDark = true 通常代表“深夜”。
 * 所以这里 checkbox 的选中状态应该是 !themeStore.isDark
 */
const isLight = computed({
  get: () => !themeStore.isDark,
  set: () => themeStore.toggleTheme()
})
</script>

<template>
  <label class="switch">
    <input v-model="isLight" type="checkbox" />
    <span class="slider">
      <div class="star star_1"></div>
      <div class="star star_2"></div>
      <div class="star star_3"></div>
      <svg viewBox="0 0 16 16" class="cloud_1 cloud">
        <path
          transform="matrix(.77976 0 0 .78395-299.99-418.63)"
          fill="#fff"
          d="m391.84 540.91c-.421-.329-.949-.524-1.523-.524-1.351 0-2.451 1.084-2.485 2.435-1.395.526-2.388 1.88-2.388 3.466 0 1.874 1.385 3.423 3.182 3.667v.034h12.73v-.006c1.775-.104 3.182-1.584 3.182-3.395 0-1.747-1.309-3.186-2.994-3.379.007-.106.011-.214.011-.322 0-2.707-2.271-4.901-5.072-4.901-2.073 0-3.856 1.202-4.643 2.925"
        ></path>
      </svg>
    </span>
  </label>
</template>

<style scoped>
.switch {
  font-size: 17px;
  position: relative;
  display: inline-block;
  width: 4em;
  height: 1.8em;
  border-radius: 30px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  vertical-align: middle;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #2a2a2a; /* 深色背景 */
  transition: 0.4s;
  border-radius: 30px;
  overflow: hidden;
}

.slider:before {
  position: absolute;
  content: "";
  height: 1.2em;
  width: 1.2em;
  border-radius: 20px;
  left: 0.7em;
  bottom: 0.3em;
  transition: 0.4s;
  transition-timing-function: cubic-bezier(0.81, -0.04, 0.38, 1.5);
  box-shadow: inset 8px -4px 0px 0px #fff; /* 月牙效果 */
}

/* 选中状态（白天） */
.switch input:checked + .slider {
  background-color: #00a6ff;
}

.switch input:checked + .slider:before {
  transform: translateX(1.8em);
  box-shadow: inset 15px -4px 0px 15px #ffcf48; /* 变太阳 */
}

.star {
  background-color: #fff;
  border-radius: 50%;
  position: absolute;
  width: 5px;
  height: 5px;
  transition: all 0.4s;
}

.star_1 { left: 2.5em; top: 0.5em; }
.star_2 { left: 2.2em; top: 1.2em; }
.star_3 { left: 3em; top: 0.9em; }

.switch input:checked + .slider .star {
  opacity: 0;
  transform: translateY(10px);
}

.cloud {
  width: 3.5em;
  position: absolute;
  bottom: -1.4em;
  left: -1.1em;
  opacity: 0;
  transition: all 0.4s;
}

.switch input:checked + .slider .cloud {
  opacity: 1;
  bottom: -0.5em; /* 轻微上浮动画 */
}
</style>