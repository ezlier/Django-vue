<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const show = ref(false)
const revealing = ref(false)

router.beforeEach((_to, from) => {
    if (from.name) {
        show.value = true
        revealing.value = false
    }
    return true
})

router.afterEach(() => {
    if (show.value) {
        requestAnimationFrame(() => {
            revealing.value = true
            setTimeout(() => {
                show.value = false
                revealing.value = false
            }, 800)
        })
    }
})
</script>

<template>
    <div v-if="show" class="page-overlay" :class="{ 'page-overlay--reveal': revealing }">
        <div class="page-overlay__bg"></div>
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
.page-overlay {
    position: fixed;
    inset: 0;
    z-index: 9999;
    pointer-events: none;
}

.page-overlay__bg {
    position: fixed;
    inset: 0;
    background: #2c2c2c;
    transition: transform 0.6s cubic-bezier(0.77, 0, 0.175, 1);
}

/* 左侧透明渐变 */
.page-overlay__bg::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 80px;
    height: 100%;
    background: linear-gradient(to right, transparent, #2c2c2c);
}

.page-overlay--reveal .page-overlay__bg {
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
    transition: opacity 0.4s ease;
}

.page-overlay--reveal .splash__center {
    opacity: 0;
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
}

/* 轨道 */
.loader__orbit {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    animation: orbit-rotate 3s linear infinite;
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
