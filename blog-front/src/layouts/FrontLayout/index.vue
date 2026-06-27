<template>
  <div class="front-layout">
    <Navbar />

    <Header />

    <main class="front-main">
      <div class="leftcolumn">
        <RouterView name="sidebar" />
      </div>

      <div class="rightcolumn">
        <RouterView v-slot="{ Component }">
          <KeepAlive :exclude="['ArticleDetail']">
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
import Navbar from './component/navbar.vue'
import Footer from './component/footer.vue'
import Header from './component/header.vue'

const ui = useUiStore()

onMounted(() => {
  ui.fetchWebSetting()
})
</script>

<style scoped>
.front-layout {
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
}

.leftcolumn {
  flex: 0 0 23%;
}

.rightcolumn {
  flex: 1;
  min-width: 0;
  border-radius: 12px;
  border: var(--border);
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
    flex: none;
    width: 100%;
  }
}
</style>
