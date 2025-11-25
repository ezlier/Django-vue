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

app.use(createPinia())

const themeStore = useThemeStore();
themeStore.initTheme();

app.use(router)
app.use(ElementPlus)
app.mount('#app')


