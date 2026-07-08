<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useUiStore } from '@/stores/ui'
import bgImage from '@/assets/img/background.png'

const ui = useUiStore()

const lightBgStyle = computed(() => ({
    backgroundImage: `url(${bgImage})`,
}))

const timestamp = ref('')

let timer: ReturnType<typeof setInterval>
onMounted(() => {
    const update = () => {
        const d = new Date()
        const pad = (n: number) => String(n).padStart(2, '0')
        timestamp.value = `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
    }
    update()
    timer = setInterval(update, 1000)
})

onUnmounted(() => {
    clearInterval(timer)
})
</script>

<template>
    <div class="background-wrapper">
        <div v-if="!ui.isDark" class="light-bg" :style="lightBgStyle"></div>
        <div v-else class="uiverse-midnight-sky">
            <div class="sky-canvas">
                <div class="stars stars-1"></div>
                <div class="stars stars-2"></div>
                <div class="stars stars-3"></div>

                <div class="meteor m1"></div>
                <div class="meteor m2"></div>
                <div class="meteor m3"></div>

                <div class="moon"></div>
            </div>
        </div>

        <div class="TimeLine">connecting [OK] ——{{ timestamp }}</div>

    </div>
</template>

<style scoped>
.background-wrapper {
    position: fixed;
    inset: 0;
    z-index: -1;
}

.light-bg {
    width: 100%;
    height: 100%;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

.uiverse-midnight-sky {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background-color: #050505;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Base Sky Layer */
.uiverse-midnight-sky .sky-canvas {
    width: 100%;
    height: 100%;
    position: absolute;
    inset: 0;
    background: #050505;
}

/* Generic star layer style */
.uiverse-midnight-sky .stars {
    position: absolute;
    inset: 0;
    background-repeat: repeat;
    pointer-events: none;
}

/* Layer 1: Small fast twinkling stars - High density */
.uiverse-midnight-sky .stars-1 {
    background-image: radial-gradient(1px 1px at 10% 10%, #fff, transparent),
        radial-gradient(1px 1px at 30% 20%, #fff, transparent),
        radial-gradient(1px 1px at 50% 50%, #fff, transparent),
        radial-gradient(1px 1px at 70% 30%, #fff, transparent),
        radial-gradient(1px 1px at 90% 10%, #fff, transparent);
    background-size: 200px 200px;
    animation: twinkle 3s ease-in-out infinite;
}

/* Layer 2: Medium slower twinkling stars */
.uiverse-midnight-sky .stars-2 {
    background-image: radial-gradient(1.5px 1.5px at 20% 40%, #fff, transparent),
        radial-gradient(1.5px 1.5px at 60% 85%, #fff, transparent),
        radial-gradient(1.5px 1.5px at 85% 65%, #fff, transparent);
    background-size: 300px 300px;
    animation: twinkle 5s ease-in-out infinite 1s;
}

/* Layer 3: Larger, very slow twinkling stars */
.uiverse-midnight-sky .stars-3 {
    background-image: radial-gradient(2px 2px at 40% 70%, #fff, transparent),
        radial-gradient(2px 2px at 10% 80%, #fff, transparent),
        radial-gradient(2px 2px at 80% 40%, #fff, transparent);
    background-size: 400px 400px;
    animation: twinkle 7s ease-in-out infinite 2s;
}

/* Meteor / Shooting Star Layer */
.uiverse-midnight-sky .meteor {
    position: absolute;
    width: 2px;
    height: 2px;
    background: #fff;
    border-radius: 50%;
    box-shadow: 0 0 10px 2px rgba(255, 255, 255, 0.5);
    opacity: 0;
    pointer-events: none;
}

/* Meteor Tail */
.uiverse-midnight-sky .meteor::after {
    content: "";
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 80px;
    height: 1px;
    background: linear-gradient(90deg, #fff, transparent);
}

/* Meteor Instances with staggered starts */
.uiverse-midnight-sky .m1 {
    top: 10%;
    left: 110%;
    animation: shoot 8s linear infinite;
}

.uiverse-midnight-sky .m2 {
    top: 30%;
    left: 110%;
    animation: shoot 12s linear infinite 4s;
}

.uiverse-midnight-sky .m3 {
    top: 50%;
    left: 110%;
    animation: shoot 10s linear infinite 2s;
}

/* The Moon */
.uiverse-midnight-sky .moon {
    position: absolute;
    top: 15%;
    right: 15%;
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: transparent;
    box-shadow: 15px 15px 0 0 #fdfbd3;
    filter: drop-shadow(0 0 15px rgba(253, 251, 211, 0.4));
    z-index: 10;
}

/* Twinkle Animation */
@keyframes twinkle {

    0%,
    100% {
        opacity: 1;
    }

    50% {
        opacity: 0.2;
    }
}

/* Shooting Star Animation - Using % instead of vw/vh */
@keyframes shoot {
    0% {
        transform: translateX(0) translateY(0) rotate(-35deg);
        opacity: 0;
    }

    5% {
        opacity: 1;
    }

    15% {
        transform: translateX(-1500px) translateY(1000px) rotate(-35deg);
        opacity: 0;
    }

    100% {
        transform: translateX(-1500px) translateY(1000px) rotate(-35deg);
        opacity: 0;
    }
}


.TimeLine {
    position: absolute;
    top: 20%;
    right: 5%;
    width: 1px;
    display: flex;
    flex-direction: column;
    writing-mode: vertical-rl;
    text-orientation: sideways;
    color: whitesmoke;
}
</style>
