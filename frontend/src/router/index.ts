import { createRouter, createWebHistory } from "vue-router";
import routes from "./routes";
import { useAuthStore } from "@/stores/auth";

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});

// 全局前置守卫：后台路由鉴权
router.beforeEach((to, _from, next) => {
  if (to.meta.requiresAuth) {
    const auth = useAuthStore();
    if (!auth.isLoggedIn) {
      next("/login");
      return;
    }
  }

  let originTitle = document.title;

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      // 页面隐藏（切走标签）
      document.title = "在暗处，有双眼睛盯着你";
    } else {
      // 页面激活（切回来）
      document.title = originTitle;
    }
  });

  next();
});

export default router;
