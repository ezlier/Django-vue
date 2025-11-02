<template>
  <footer class="kratos-footer ">
    <div class="footer-content">
      <div class="copyright">
        <p>© {{ currentYear }} by Ezria blog. | 我们度过了{{ daysRunning }}个风雨</p>
        <div style="display: flex;justify-content:center">
          <p class="theme-credit">{{ form.footer_text1 }}</p>
          <p>
            <RouterLink to="/login" class="aaa"><svg style="width: 25px;" xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 1024 1024">
                <path fill="currentColor"
                  d="M512 386.88V448h405.568a32 32 0 0 1 30.72 40.768l-76.48 267.968A192 192 0 0 1 687.168 896H336.832a192 192 0 0 1-184.64-139.264L75.648 488.768A32 32 0 0 1 106.368 448H448V117.888a32 32 0 0 1 47.36-28.096l13.888 7.616L512 96v2.88l231.68 126.4a32 32 0 0 1-2.048 57.216zm0-70.272 144.768-65.792L512 171.84zM512 512H148.864l18.24 64H856.96l18.24-64zM185.408 640l28.352 99.2A128 128 0 0 0 336.832 832h350.336a128 128 0 0 0 123.072-92.8l28.352-99.2z">
                </path>
              </svg></RouterLink>
          </p>
        </div>
        <p>{{ form.footer_text2 }}</p>
      </div>

    </div>
  </footer>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { getWebSetting } from "@/utils/websetting"

const form = ref([])
onMounted(async () => {
  const res = await getWebSetting();
  form.value = res.data;
  const startDate = new Date(form.value.date);
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
  background: linear-gradient(to right,
      #d3959b,
      #bfe6ba);
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
