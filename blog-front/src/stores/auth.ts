import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi, updateUser as updateUserApi } from '@/api/auth'
import { ElMessage } from 'element-plus'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('access_token') || '')
  const refreshToken = ref(localStorage.getItem('refresh_token') || '')
  const username = ref(localStorage.getItem('username') || '')
  const isLoggedIn = computed(() => !!token.value)

  async function login(usernameVal: string, password: string) {
    const res = await loginApi(usernameVal, password)
    const data = res.data.data
    token.value = data.token
    refreshToken.value = data.refresh
    username.value = data.username
    localStorage.setItem('access_token', data.token)
    localStorage.setItem('refresh_token', data.refresh)
    localStorage.setItem('username', data.username)
    ElMessage.success('登录成功')
    router.push('/admin/dashboard')
  }

  async function updateUser(data: { username?: string; old_password?: string; new_password?: string }) {
    await updateUserApi(data)
    if (data.username) {
      username.value = data.username
      localStorage.setItem('username', data.username)
    }
  }

  function logout() {
    token.value = ''
    refreshToken.value = ''
    username.value = ''
    localStorage.clear()
    router.push('/login')
  }

  return { token, refreshToken, username, isLoggedIn, login, updateUser, logout }
})
