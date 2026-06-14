import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getWebSetting } from '@/api/user'

export const useUiStore = defineStore('ui', () => {
  const isDark = ref(localStorage.getItem('theme') === 'dark')
  const sidebarCollapsed = ref(false)
  const webSetting = ref<WebSetting | null>(null)

  function toggleTheme() {
    isDark.value = !isDark.value
    localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
    document.documentElement.classList.toggle('dark', isDark.value)
  }

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  async function fetchWebSetting() {
    try {
      const res = await getWebSetting()
      webSetting.value = res.data.data
    } catch {
      // 配置加载失败不阻塞页面
    }
  }

  // 初始化主题
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  }

  return { isDark, sidebarCollapsed, webSetting, toggleTheme, toggleSidebar, fetchWebSetting }
})

export interface WebSetting {
  name: string
  web_name: string
  name_avatar: string | null
  about_md: string
  footer_text1: string
  footer_text2: string
  updated_time: string
}
