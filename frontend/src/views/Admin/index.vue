<template>
  <div class="content">
    <div class="header">
      <div class="nav">
        <span style="padding-right: 20px;"><RouterLink to="/">回到首页</RouterLink></span>
        <span style="padding-right: 20px;color: black;">{{ username }}</span>
        <button @click="logout">退出</button>
      </div>
    </div>
    <div class="row">
      <div class="menu">
        <p class="menu-item"><RouterLink to="/admin">首页</RouterLink></p>
        <p class="menu-item"><RouterLink to="/admin/WebSetting">网站设置</RouterLink></p>
        <p class="menu-item"><RouterLink to="/admin/PostSetting">文章管理</RouterLink></p>
        <p class="menu-item"><RouterLink to="/admin/MessageSetting">留言管理</RouterLink></p>
        <p class="menu-item"><RouterLink to="/admin/Bannedwords">违禁词管理</RouterLink></p>
      </div>
      <div class="main-content">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "@/utils/request"; // ✅ 使用封装好的 axios 实例

const router = useRouter();
const username = ref(localStorage.getItem("username"));
const message = ref("");

onMounted(async () => {
  const token = localStorage.getItem("token");
  if (!token) {
    router.push("/login");
    return;
  }

  try {
    // ✅ 用封装好的 api 自动带上 token
    const res = await api.get("admin_data/");
    message.value = res.data.message;
  } catch (error) {
    console.error(error);
    alert("登录状态已失效，请重新登录");
    logout();
  }
});

const logout = () => {
  localStorage.clear();
  router.push("/login");
};
</script>


<style scoped>
.content{
  color: #000;
  background-color: whitesmoke;
  margin: 0 auto;
  max-width: 1280px;
  width: 100%;
}

.header {
  padding: 15px;
  background-color: #dbe2ef;
  width: 100%;
}

.nav {
  text-align: right;
}

.row {
  display: flex;
  gap: 20px;
  max-width: 1280px;
  justify-content: center;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}

.menu {
  flex: 0 0 20%;
  min-height: 100vh;
  max-width: 200px;
}

.menu-item{
  padding: 10px 20px;
  width: 100%;
  background-color: #dbe2ef;
}

.main-content {
  padding: 20px;
  flex: 1;
  min-width: 0;
  width: 100%;
  border-radius: 8px;
}

button {
  padding: 10px 20px;
  background: #ff6b6b;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
</style>
