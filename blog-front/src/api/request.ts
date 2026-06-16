import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api/v2/',
  timeout: 30000,
  withCredentials: false,
  headers: {
    'Content-Type': 'application/json',
  },
})

// ── 请求拦截器：自动附加 token ───────────────────────────────────
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error),
)

// 开发模式下打印请求日志
if (import.meta.env.DEV) {
  api.interceptors.request.use((config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`, config.params || config.data)
    return config
  })
  api.interceptors.response.use(
    (res) => {
      console.log(`[API] ${res.config.method?.toUpperCase()} ${res.config.url} →`, res.data)
      return res
    },
    (err) => {
      console.error(`[API] ${err.config?.method?.toUpperCase()} ${err.config?.url} →`, err.response?.status, err.response?.data)
      return Promise.reject(err)
    }
  )
}

// ── 响应拦截器：统一错误处理 + token 自动刷新 ────────────────────
let isRefreshing = false
let refreshSubscribers: Array<(token: string) => void> = []

function onRefreshed(token: string) {
  refreshSubscribers.forEach((cb) => cb(token))
  refreshSubscribers = []
}

api.interceptors.response.use(
  (response) => {
    const data = response.data
    // 统一响应格式 { code, msg, data }
    if (data.code && data.code >= 400) {
      ElMessage.error(data.msg || '请求失败')
      return Promise.reject(new Error(data.msg || '请求失败'))
    }
    return response
  },
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      if (isRefreshing) {
        return new Promise((resolve) => {
          refreshSubscribers.push((token: string) => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            resolve(api(originalRequest))
          })
        })
      }

      isRefreshing = true
      const refreshToken = localStorage.getItem('refresh_token')

      if (refreshToken) {
        try {
          const res = await axios.post('/api/v2/token/refresh/', { refresh: refreshToken })
          const tokenData = res.data
          let newAccess: string | null = null

          if (tokenData.data?.token) {
            newAccess = tokenData.data.token
            if (tokenData.data.refresh) {
              localStorage.setItem('refresh_token', tokenData.data.refresh)
            }
          } else if (tokenData.access) {
            newAccess = tokenData.access
          }

          if (newAccess) {
            localStorage.setItem('access_token', newAccess)
            api.defaults.headers.common['Authorization'] = `Bearer ${newAccess}`
            originalRequest.headers['Authorization'] = `Bearer ${newAccess}`
            onRefreshed(newAccess)
            isRefreshing = false
            return api(originalRequest)
          }
        } catch {
          // refresh 也过期了
        }
      }

      isRefreshing = false
      localStorage.clear()
      window.location.href = '/login'
      return Promise.reject(error)
    }

    // 网络错误或其他错误
    if (!error.response) {
      ElMessage.error('网络连接失败')
    } else if (error.response.status >= 500) {
      ElMessage.error('服务器内部错误')
    }

    return Promise.reject(error)
  },
)

export default api
