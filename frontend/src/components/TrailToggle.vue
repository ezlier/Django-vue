<template>
  <div class="trail-toggle">
    <button class="trail-btn" @click="toggleTrail">
      <svg v-if="themeStore.showTrail" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" class="icon">
        <path fill="currentColor"
          d="M4.89.188a.505.505 0 0 0-.555-.16a.5.5 0 0 0-.334.472v13a.5.5 0 0 0 .625.484a.5.5 0 0 0 .254-.16l2.44-2.85l1.71 4.7a.497.497 0 0 0 .641.3a.497.497 0 0 0 .299-.641l-1.73-4.75l4.21.42a.502.502 0 0 0 .548-.542a.5.5 0 0 0-.108-.268l-8-10zm.11 12v-10.2l6.37 7.96l-3.82-.383a.5.5 0 0 0-.43.173L5 12.208z" />
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon">
        <g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
          <path
            d="M2.034 2.681a.498.498 0 0 1 .647-.647l9 3.5a.5.5 0 0 1-.033.944L8.204 7.545a1 1 0 0 0-.66.66l-1.066 3.443a.5.5 0 0 1-.944.033z" />
          <circle cx="16" cy="16" r="6" />
          <path d="m11.8 11.8l8.4 8.4" />
        </g>
      </svg>
    </button>
  </div>
</template>

<script setup>
import { useThemeStore } from "@/stores/theme"

const themeStore = useThemeStore()

const toggleTrail = () => {
  themeStore.toggleTrail()
}
</script>

<style scoped>
.trail-toggle {
  position: fixed;
  right: 40px;
  bottom: 40px;
  z-index: 150;
}

.trail-btn {
  width: 40px;
  height: 40px;
  border-radius: var(--border-radius);
  background: var(--el-bg-color);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  border: 2px solid var(--el-bg-color);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s ease;
}

.icon {
  width: 15px;
  height: 15px;
  color: #fcbad3;
  fill: #fcbad3;
  stroke: #fcbad3;
}
</style>
