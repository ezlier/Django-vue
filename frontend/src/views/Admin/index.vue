<template>
  <div class="content">
    <div class="header">
      <div class="neirong">
        <span style="padding-right: 20px;">{{ username }}</span>
        <button @click="logout">退出</button>
      </div>
    </div>
    <div class="row">
      <div class="menu">
        <p class="menu-item">1</p>
        <p class="menu-item">1</p>
        <p class="menu-item">1</p>
        <p class="menu-item">1</p>
      </div>
      <div>

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
.header {
  padding: 15px;
  background-color: #000;
  width: 100%;
}

.neirong {
  text-align: right;
}

.menu {
  max-width: 200px;
}

.menu-item{
  padding: 10px;
  width: 100%;
  background-color: black;
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
