<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import ThemeButton from '@/components/ThemeButton.vue'
import BackButton from '@/components/BackButton.vue'
import ToTopButton from '@/components/ToTopButton.vue'
import ToAdminButton from '@/components/ToAdmin.vue'

const visible = ref(false)

function onMouseMove(e: MouseEvent) {
    const threshold = 100
    const thresholdHeight = 300
    const { clientX, clientY } = e
    const { innerWidth, innerHeight } = window
    visible.value = clientX > innerWidth - threshold && clientY > innerHeight - thresholdHeight
}

onMounted(() => {
    window.addEventListener('mousemove', onMouseMove, { passive: true })
})

onUnmounted(() => {
    window.removeEventListener('mousemove', onMouseMove)
})
</script>

<template>
    <div class="dock" :class="{ 'dock--visible': visible }">
        <ToTopButton class="dock-btn" />
        <BackButton class="dock-btn" />
        <ThemeButton class="dock-btn" />
        <ToAdminButton class="dock-btn" />
    </div>
</template>

<style scoped>
.dock {
    position: fixed;
    bottom: 50px;
    right: -60px;
    width: 50px;
    display: grid;
    place-items: center;
    gap: 10px;
    /* z-index: 1000; */
    transition: right 0.3s ease;
}

.dock--visible {
    right: 10px;
}

.dock-btn {
    width: 50px;
    height: 50px;
    border-radius: 4px;
}
</style>