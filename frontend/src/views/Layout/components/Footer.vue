<template>
  <footer class="kratos-footer ">
    <div class="footer-content">
      <div class="copyright">
        <p>© {{ currentYear }} by Ezria blog. | 已运行{{ daysRunning }}天</p>
        <div style="display: flex;justify-content:center">
          <p class="theme-credit">{{ WebSetting.WebSettingList.footer_text1 }}</p>

        </div>
        <p>{{ WebSetting.WebSettingList.footer_text2 }}</p>
      </div>

    </div>
  </footer>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

import { useWebSettingStore } from '@/stores/WebSetting'

const WebSetting = useWebSettingStore()

onMounted(async () => {
  await WebSetting.fetchWebSetting();
  const startDate = new Date(WebSetting.WebSettingList.updated_time);
  const today = new Date();
  const diffTime = Math.abs(today - startDate);
  daysRunning.value = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
})

const currentYear = computed(() => new Date().getFullYear());
const daysRunning = ref(0);

</script>

<style scoped>
.aaa {
  color: whitesmoke;
}

.aaa:hover {
  background-color: rgba(255, 255, 255, 0);
}

.kratos-footer {

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
