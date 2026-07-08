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
</style>
