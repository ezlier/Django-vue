import axios from 'axios'

// 创建 axios 实例
const api = axios.create({
  baseURL: '/api/',
  withCredentials: true // 允许跨域请求时携带 Cookie
})

// 获取 csrftoken 的函数
function getCookie(name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
}

// --- 初始化 CSRF Cookie ---
// 访问后端专门的 GET 接口，让浏览器下发 csrftoken
axios.get(`${api.defaults.baseURL}get_csrf/`, { withCredentials: true })
  .then(() => console.log('CSRF cookie 已初始化'))
  .catch(err => console.warn('CSRF 初始化失败', err))

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 携带登录 Token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }

    // 携带 Django CSRF Token
    const csrftoken = getCookie('csrftoken')
    if (csrftoken) {
      config.headers['X-CSRFToken'] = csrftoken
    }

    return config
  },
  error => Promise.reject(error)
)

// 响应拦截器（可选）
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 403) {
      console.warn('CSRF 验证失败或未授权')
    }
    return Promise.reject(error)
  }
)

export default api
