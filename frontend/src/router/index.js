import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/views/Layout/index.vue'
import Home from '@/views/Home/index.vue'
import File from '@/views/File/index.vue'
import About from '@/views/About/index.vue'
import Login from '@/views/Login/index.vue'
import Admin from '@/views/Admin/index.vue'
import ArticleDetail from '@/views/Post/index.vue'
import WebSetting from '@/views/Admin/components/WebSetting.vue'
import PostSetting from '@/views/Admin/components/PostSetting.vue'
import visitor_IP from '@/views/Admin/components/visitor_IP.vue'
import MessageBoard from '@/views/MessageBoard/index.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Layout,
      children: [
        {path: '',name: "Home",component: Home},
        {path: 'file',name: "File",component: File},
        {path: 'about',name: "About",component: About},
        {path: 'post/:slug',name: 'ArticleDetail',component:ArticleDetail}
      ]
    },
    {
      path: '/MessageBoard',name: 'MessageBoard',component:MessageBoard
    },
    {
      path: '/login',
      component: Login
    },
    {
      path: '/admin',
      component: Admin,
      meta: { requiresAuth: true }, // ✅ 后台页需要登录
      children: [
        {path: 'WebSetting',name: 'WebSetting',component:WebSetting},
        {path: '',name: 'IP',component:visitor_IP},
        {path: 'PostSetting',name: 'PostSetting',component:PostSetting},
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  },
})

// ✅ 登录守卫逻辑
router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
  const token = localStorage.getItem('token')

  // 1️⃣ 未登录访问后台页 → 跳转登录页
  if (to.meta.requiresAuth && (!isLoggedIn || !token)) {
    next('/login')
    return
  }

  // 2️⃣ 已登录访问登录页 → 跳转后台页
  if (to.path === '/login' && isLoggedIn && token) {
    next('/admin')
    return
  }

  // 3️⃣ 其他页面正常放行
  next()
})


export default router
