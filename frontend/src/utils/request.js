import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v2/',
  withCredentials: false
})

api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refreshToken = localStorage.getItem('refresh_token')

      if (refreshToken) {
        try {
          const res = await axios.post('/api/v2/token/refresh/', { refresh: refreshToken })
          const tokenData = res.data
          let newAccess = null

          // v1 返回 { access: "..." }，v2 返回 { code, data: { token: "..." } }
          if (tokenData.data && tokenData.data.token) {
            newAccess = tokenData.data.token
            if (tokenData.data.refresh) {
              localStorage.setItem('refresh_token', tokenData.data.refresh)
            }
          } else if (tokenData.access) {
            newAccess = tokenData.access
          }
          localStorage.setItem('access_token', newAccess)
          api.defaults.headers.common['Authorization'] = `Bearer ${newAccess}`
          originalRequest.headers['Authorization'] = `Bearer ${newAccess}`
          return api(originalRequest)
        } catch (err) {
          localStorage.clear()
          window.location.href = '/login'
        }
      } else {
        localStorage.clear()
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

export default api
