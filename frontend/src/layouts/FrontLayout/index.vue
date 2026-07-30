<template>
  <div class="front-layout">
    <SplashScreen ref="splashRef" />
    <PageTransition />
    <Background />
    <Dock />

    <Navbar />

    <div class="head" :style="{ height: headerHeight }">
      <Header v-if="route.name === 'Home'" />
      <h1 v-else style="color: var(--color-text);">{{ route.name }}</h1>
    </div>

    <main class="front-main">
      <div class="leftcolumn">
        <RouterView name="sidebar" />
      </div>

      <div class="rightcolumn">
        <RouterView v-slot="{ Component }">
          <template v-if="Component">
            <KeepAlive :exclude="['ArticleDetail']">
              <component :is="Component" />
            </KeepAlive>
          </template>
        </RouterView>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useUiStore } from '@/stores/ui'
import { useRoute } from 'vue-router'
import Navbar from './component/navbar.vue'
import Footer from './component/footer.vue'
import Header from './component/header.vue'
import Background from './component/background.vue'
import Dock from './component/dock.vue'
import SplashScreen from '@/components/SplashScreen.vue'
import PageTransition from '@/components/PageTransition.vue'

const ui = useUiStore()

const route = useRoute();

const splashRef = ref<InstanceType<typeof SplashScreen>>()

onMounted(async () => {
  await ui.fetchWebSetting()
  splashRef.value?.close()
})

const headerHeight = computed(() => {
  if (route.name === "Home") return "100vh";
  return "300px";
});

</script>

<style scoped>
.head {
  transition: height 0.5s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.front-main {
  display: flex;
  gap: 24px;
  max-width: 1280px;
  padding: 24px;
  justify-content: center;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}

.leftcolumn {
  flex: 0 0 23%;
}

.rightcolumn {
  flex: 1;
  min-width: 0;
  border-radius: var(--border-radius-xs);
  box-shadow: var(--box-shadow);
  border-color: var(--color-border);
  background-color: var(--color-background-soft);
  padding: 1.125rem;
}

@media (max-width: 768px) {
  .front-main {
    flex-direction: column;
    padding: 16px;
  }

  .leftcolumn {
    display: none;
    width: 100%;
  }
}
</style>
