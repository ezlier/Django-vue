import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// 路由懒加载
const FrontLayout = () => import('@/layouts/FrontLayout.vue')
const AdminLayout = () => import('@/layouts/AdminLayout.vue')

const HomeView = () => import('@/views/HomeView.vue')
const ArticleDetail = () => import('@/views/ArticleDetail.vue')
const ArchiveView = () => import('@/views/ArchiveView.vue')
const AboutView = () => import('@/views/AboutView.vue')
const LoginView = () => import('@/views/LoginView.vue')

const AdminDashboard = () => import('@/views/admin/DashboardView.vue')
const AdminArticles = () => import('@/views/admin/ArticleList.vue')
const AdminArticleEdit = () => import('@/views/admin/ArticleEdit.vue')
const AdminComments = () => import('@/views/admin/CommentList.vue')
const AdminMessages = () => import('@/views/admin/MessageList.vue')
const AdminTags = () => import('@/views/admin/TagList.vue')
const AdminUsers = () => import('@/views/admin/UserManage.vue')
const AdminSettings = () => import('@/views/admin/SettingView.vue')

const routes: RouteRecordRaw[] = [
  // ── 前台 ──────────────────────────────────────────────────────
  {
    path: '/',
    component: FrontLayout,
    children: [
      { path: '', redirect: '/home' },
      { path: 'home', name: 'Home', component: HomeView },
      { path: 'article/:slug', name: 'ArticleDetail', component: ArticleDetail },
      { path: 'archive', name: 'Archive', component: ArchiveView },
      { path: 'about', name: 'About', component: AboutView },
    ],
  },

  // ── 登录 ──────────────────────────────────────────────────────
  { path: '/login', name: 'Login', component: LoginView },

  // ── 后台 ──────────────────────────────────────────────────────
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/admin/dashboard' },
      { path: 'dashboard', name: 'AdminDashboard', component: AdminDashboard },
      { path: 'articles', name: 'AdminArticles', component: AdminArticles },
      { path: 'article/edit/:slug?', name: 'AdminArticleEdit', component: AdminArticleEdit },
      { path: 'comments', name: 'AdminComments', component: AdminComments },
      { path: 'message', name: 'AdminMessages', component: AdminMessages },
      { path: 'tags', name: 'AdminTags', component: AdminTags },
      { path: 'users', name: 'AdminUsers', component: AdminUsers },
      { path: 'settings', name: 'AdminSettings', component: AdminSettings },
    ],
  },

  // ── 404 ───────────────────────────────────────────────────────
  { path: '/:pathMatch(.*)*', redirect: '/home' },
]

export default routes
