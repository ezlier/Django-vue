import type { RouteRecordRaw } from "vue-router";
import { useAuthStore } from "@/stores/auth";

// 路由懒加载
const FrontLayout = () => import("@/layouts/FrontLayout/index.vue");
const AdminLayout = () => import("@/layouts/AdminLayout/index.vue");

// 前台
const HomeView = () => import("@/views/home/index.vue");
const ArticleDetail = () => import("@/views/article-detail/index.vue");
const ArchiveView = () => import("@/views/archive/index.vue");
const AboutView = () => import("@/views/about/index.vue");
const LoginView = () => import("@/views/login/index.vue");

// 侧边栏
const CommonSidebar = () =>
  import("@/layouts/FrontLayout/component/Sidebar.vue");
const ArticleSidebar = () =>
  import("@/views/article-detail/component/ArticleSidebar.vue");

// 后台
const AdminDashboard = () => import("@/views/admin/dashboard/index.vue");
const AdminArticles = () => import("@/views/admin/articles/index.vue");
const AdminArticleEdit = () => import("@/views/admin/article-edit/index.vue");
const AdminComments = () => import("@/views/admin/comments/index.vue");
const AdminMessages = () => import("@/views/admin/message/index.vue");
const AdminTags = () => import("@/views/admin/tags/index.vue");
const AdminUsers = () => import("@/views/admin/users/index.vue");
const AdminSettings = () => import("@/views/admin/settings/index.vue");

const routes: RouteRecordRaw[] = [
  // ── 前台 ──────────────────────────────────────────────────────
  {
    path: "/",
    component: FrontLayout,
    children: [
      { path: "", redirect: "/home" },
      {
        path: "home",
        name: "Home",
        components: {
          default: HomeView,
          sidebar: CommonSidebar,
        },
      },
      {
        path: "article/:slug",
        name: "ArticleDetail",
        components: {
          default: ArticleDetail,
          sidebar: ArticleSidebar,
        },
      },
      {
        path: "archive",
        name: "Archive",
        components: {
          default: ArchiveView,
          sidebar: CommonSidebar,
        },
      },
      {
        path: "about",
        name: "About",
        components: {
          default: AboutView,
          sidebar: CommonSidebar,
        },
      },
    ],
  },

  // ── 登录 ──────────────────────────────────────────────────────
  { path: "/login", name: "Login", component: LoginView },

  // ── 后台 ──────────────────────────────────────────────────────
  {
    path: "/admin",
    component: AdminLayout,
    meta: { requiresAuth: true },
    children: [
      { path: "", redirect: "/admin/dashboard" },
      { path: "dashboard", name: "AdminDashboard", component: AdminDashboard },
      { path: "articles", name: "AdminArticles", component: AdminArticles },
      {
        path: "article/edit/:slug?",
        name: "AdminArticleEdit",
        component: AdminArticleEdit,
      },
      { path: "comments", name: "AdminComments", component: AdminComments },
      { path: "message", name: "AdminMessages", component: AdminMessages },
      { path: "tags", name: "AdminTags", component: AdminTags },
      { path: "users", name: "AdminUsers", component: AdminUsers },
      { path: "settings", name: "AdminSettings", component: AdminSettings },
    ],
  },

  // ── 404 ───────────────────────────────────────────────────────
  { path: "/:pathMatch(.*)*", redirect: "/home" },
];

export default routes;
