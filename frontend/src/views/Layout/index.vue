<script setup>
import PointerTextTrail from '@/components/PointerTextTrail.vue';
import navbar from "@/views/Layout/components/nav.vue"
import footera from "@/views/Layout/components/Footer.vue"
</script>

<template>
    <div class="bg"/>
    <PointerTextTrail class="texiao "/>
    <div class="nav">
        <navbar/>
    </div>

    <main class="main-content">
            <transition name="fade" mode="out-in">
              <router-view v-slot="{ Component }">
                <component :is="Component" />
              </router-view>
            </transition>
    </main>

    <div>
        <footera/>
    </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.bg {
  position: fixed;         /* 固定在视口 */
  top: 0;
  left: 0;
  width: 100vw;            /* 拉伸占满全屏 */
  height: 100vh;
  background-image: url('@/assets/img/bg1.jpg');
  background-size: cover;  /* 拉伸裁剪为最大，保持比例 */
  background-repeat: no-repeat;
  background-position: center;
  z-index: -1;             /* 放到内容后面 */
}

@media (max-width: 1000px) {
  .bg {
  position: fixed;         /* 固定在视口 */
  top: 0;
  left: 0;
  width: 100vw;            /* 拉伸占满全屏 */
  height: 100vh;
  background-image: url('@/assets/img/bg2.png');
  background-size: cover;  /* 拉伸裁剪为最大，保持比例 */
  background-repeat: no-repeat;
  background-position: center;
  z-index: -1;             /* 放到内容后面 */
}

  .texiao{
    display: none;
  }
}
</style>