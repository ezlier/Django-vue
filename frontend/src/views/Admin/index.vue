<template>
  <div class="admin-layout">
    <!-- 顶栏 -->
    <header class="topbar">
      <div class="top-left">
        <RouterLink to="/" class="home-link">← 回到首页</RouterLink>
      </div>

      <div class="top-right">
        <ThemeToggle class="theme-toggle" />
        <span class="username">{{ username }}</span>
        <button class="logout-btn" @click="logout">退出登录</button>
      </div>
    </header>

    <!-- 主结构 -->
    <div class="container">
      <!-- 侧边菜单 -->
      <div class="sidebar">
        <RouterLink to="/admin" class="menu-item" active-class="active">工作台</RouterLink>
        <RouterLink to="/admin/WebSetting" class="menu-item" active-class="active">网站设置</RouterLink>
        <RouterLink to="/admin/PostSetting" class="menu-item" active-class="active">文章管理</RouterLink>
        <RouterLink to="/admin/tags" class="menu-item" active-class="active">标签管理</RouterLink>
        <RouterLink to="/admin/MessageSetting" class="menu-item" active-class="active">留言管理</RouterLink>
        <RouterLink to="/admin/Comments" class="menu-item" active-class="active">评论管理</RouterLink>
        <RouterLink to="/admin/Bannedwords" class="menu-item" active-class="active">违禁词管理</RouterLink>
      </div>

      <!-- 主内容区 -->
      <main class="main-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import ThemeToggle from '@/components/ThemeToggle.vue'

const router = useRouter();
const username = ref(localStorage.getItem("username"));

onMounted(() => {
  const token = localStorage.getItem("access_token");
  
  if (!token) {
    router.push("/login");
  }
});

const logout = () => {
  localStorage.clear();
  router.push("/login");
};
</script>


<style scoped>
.theme-toggle{
  background-color: var(--bg-color);
}

.admin-layout {
  background: #f7f9fc;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 顶栏 */
.topbar {
  height: 60px;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

.top-left .home-link {
  font-size: 15px;
  color: #4a69bd;
  text-decoration: none;
  font-weight: 600;
}

.top-right {
  display: flex;
  align-items: center;
  gap: 18px;
}

.username {
  font-weight: 600;
  color: #34495e;
}

.logout-btn {
  padding: 8px 16px;
  background: #ff7675;
  border: none;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: 0.2s;
}

.logout-btn:hover {
  background: #e84141;
}

/* 主体区域 */
.container {
  display: flex;
  width: 100%;
  flex: 1;
}

/* 侧边栏 */
.sidebar {
  width: 220px;
  height: auto;
  background: #f1f4f9;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.menu-item {
  display: block;
  padding: 12px 16px;
  border-radius: 6px;
  text-decoration: none;
  color: #34495e;
  font-weight: 500;
  transition: 0.2s;
}

.menu-item:hover {
  background: #e6ebf3;
}

/* 主视图区 */
.main-content {
  flex: 1;
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  min-height: 400px;
}

</style>
