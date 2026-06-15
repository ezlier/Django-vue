<template>
  <div class="front-layout">
    <Navbar />

    <Header />

    <main class="front-main">
      <div class="leftcolumn">
        <Sidebar />
      </div>

      <div class="rightcolumn">
        <RouterView v-slot="{ Component }">
          <KeepAlive>
            <component :is="Component" />
          </KeepAlive>
        </RouterView>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useUiStore } from '@/stores/ui'
import Navbar from './component/navbar.vue';
import Footer from './component/footer.vue';
import Header from './component/header.vue';
import Sidebar from './component/Sidebar.vue';

const ui = useUiStore()

onMounted(() => {
  ui.fetchWebSetting()
})
</script>

<style scoped>
.front-layout {
  min-height: 100dvh;
  background: var(--color-background-soft);

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
  min-height: 100dvh;
}

.leftcolumn,
.rightcolumn {
  border-radius: 12px;
  border: var(--border);
  box-shadow: var(--box-shadow);
  bor