import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useThemeStore } from './stores/theme'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.directive('fade-in', {
  mounted(el) {
    const observer = new IntersectionObserver((entries) => {
      const entry = entries[0]
      // 元素进入视口
      if (entry.isIntersecting) {
        el.classList.add('visible')
        observer.unobserve(el) // 只执行一次，用完取消监听
      }
    })

    // 开始监听元素
    observer.observe(el)
  }
})



app.use(createPinia())

const themeStore = useThemeStore();
themeStore.initTheme();

app.use(router)
app.use(ElementPlus)
app.mount('#app')


