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
import Navbar from './component/navbar.vue';
import Footer from './component/footer.vue';
import Header from './component/header.vue';
import Sidebar from './component/Sidebar.vue';
</script>

<style scoped>
.front-layout {
  min-height: 100dvh;
  background: var(--color-background);
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
  flex: 0 0 260px;
  border-radius: 12px;
}

.rightcolumn {
  flex: 1;
  min-width: 0;
  border-radius: 12px;
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