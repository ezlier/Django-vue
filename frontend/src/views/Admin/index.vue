<template>
  <div class="admin">
    <h1 v-if="username">欢迎回来，{{ username }}</h1>
    <p v-if="message">{{ message }}</p>
    <button @click="logout">退出登录</button>
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
.admin {
  text-align: center;
  margin-top: 200px;
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
