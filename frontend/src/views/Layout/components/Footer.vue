<template>
  <footer class="kratos-footer ">
    <div class="footer-content">
      <div class="copyright">
        <p> {{ currentYear }} by Ezria. blog. | 这个网页运行了 {{ daysRunning }}天</p>
        <div style="display: flex;justify-content:center"><p class="theme-credit">咕咕咕</p></div>
      </div>
      
    </div>
  </footer>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const currentYear = computed(() => new Date().getFullYear());
const daysRunning = ref(0);


onMounted(() => {
  const startDate = new Date('2025-07-18');
  const today = new Date();
  const diffTime = Math.abs(today - startDate);
  daysRunning.value = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  
});
</script>

<style scoped>

.kratos-footer {
  background: linear-gradient(
    to right,
    #d3959b,
    #bfe6ba
  );
  color: whitesmoke;
  font-size: 14px;
  padding: 20px 0;
  text-align: center;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  width: 100%;
  box-sizing: border-box;
  flex-shrink: 0; 
  bottom: 0;
}
.footer-content {
  max-width: 12000px;
  margin: 0 auto;
  padding: 0 20px;
}

.copyright {
  margin-bottom: 1px;
  line-height: 1.6;
}

.theme-credit {
  font-size: 13px;
  color: white;
  margin-top: 5px;
}
</style>
