import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/views/Layout/index.vue'
import Home from '@/views/Home/index.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Layout,
      children: [
        {
          path: '',
          name: 'Home',
          component: Home,
          meta: { title: '首页' }
        },
        {
          path: 'file',
          name: 'File',
          component: () => import(/* webpackPrefetch: true */'@/views/File/index.vue'),
          meta: { title: '归档' }
        },
        {
          path: 'about',
          name: 'About',
          component: () => import(/* webpackPrefetch: true */'@/views/About/index.vue'),
          meta: { title: '关于' }
        },
        {
          path: 'post/:slug',
          name: 'ArticleDetail',
          component: () => import(/* webpackPrefetch: true */'@/views/Post/index.vue'),
          meta: { title: '文章' }
        }
      ]
    },
    {
      path: '/test',
      component: () => import('@/views/text/text.vue'),
      meta: { title: '测试' }
    },
    {
      path: '/login',
      component: () => import('@/views/Login/index.vue')
    },
    {
      path: '/admin',
      component: () => import('@/views/Admin/index.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: 'WebSetting',
          name: 'WebSetting',
          component: () => import('@/views/Admin/components/WebSetting.vue')
        },
        {
          path: '',
          name: 'IP',
          component: () => import('@/views/Admin/components/workbench.vue')
        },
        {
          path: 'PostSetting',
          name: 'PostSetting',
          component: () => import('@/views/Admin/components/PostSetting.vue')
        },
        {
          path: 'MessageSetting',
          name: 'MessageSetting',
          component: () => import('@/views/Admin/components/MessageSetting.vue')
        },
        {
          path: 'Bannedwords',
          name: 'Bannedwords',
          component: () => import('@/views/Admin/components/Bannedwords.vue')
        },
        {
          path: 'Comments',
          name: 'Comment',
          component: () => import('@/views/Admin/components/Comments.vue')
        },
        {
          path: 'UploadArticle',
          name: 'UploadArticle',
          component: () => import('@/views/Admin/components/UploadArticle.vue')
        },
        {
          path: 'CreateArticle',
          name: 'CreateArticle',
          component: () => import('@/views/Admin/components/CreateArticle.vue')
        },
        {
          path: 'Rewrite/:slug',
          name: 'RewriteArticle',
          component: () => import('@/views/Admin/components/RewriteArticle.vue')
        },
        {
          path: 'tags/',
          name: 'tags',
          component: () => import('@/views/Admin/components/tags.vue')
        },

      ]
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NofoundPage',
      component: () => import('@/views/404/index.vue')
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

const originalTitle = document.title;
router.beforeEach((to, from, next) => {
  
  if (to.meta.title) {
    document.title = to.meta.title + ' - ' + originalTitle;
  }
  let isLoggedIn = false
  let token = null
  try {
    isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
    token = localStorage.getItem('access_token')
  } catch (err) {
    // localStorage error
  }

  if (to.meta.requiresAuth && (!isLoggedIn || !token)) {
    next('/login')
    return
  }

  if (to.path === '/login' && isLoggedIn && token) {
    next('/admin')
    return
  }

  next()
})


export default router