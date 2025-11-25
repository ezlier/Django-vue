import axios from 'axios'

const api = axios.create({
  baseURL: '/api/',
  withCredentials: false
})

// 请求拦截器：携带 JWT
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}` // ✅ 注意是 Bearer
    }
    return config
  },
  error => Promise.reject(error)
)

// 响应拦截器：自动刷新 token
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    // 如果返回 401 并且还没重试过
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refreshToken = localStorage.getItem('refresh_token')

      if (refreshToken) {
        try {
          const res = await axios.post('/api/token/refresh/', { refresh: refreshToken })
          const newAccess = res.data.access
          localStorage.setItem('access_token', newAccess)
          api.defaults.headers.common['Authorization'] = `Bearer ${newAccess}`
          originalRequest.headers['Authorization'] = `Bearer ${newAccess}`
          return api(originalRequest)
        } catch (err) {
          console.warn('刷新 Token 失败', err)
          localStorage.clear()
          // window.location.href = '/login'
        }
      }
    }

    return Promise.reject(error)
  }
)

export default api
