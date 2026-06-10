<template>
  <section>
    <div class="color"></div>
    <div class="color"></div>
    <div class="color"></div>

    <div class="box">
      <div class="square" v-for="i in 5" :key="i" :style="`--i:${i - 1}`"></div>

      <div class="container">
        <div class="form">
          <h2>管理员登录</h2>

          <form @submit.prevent="handleLogin">
            <div class="inputBox">
              <input
                v-model="username"
                type="text"
                placeholder="Username"
                required
                :disabled="loading"
              />
            </div>

            <div class="inputBox">
              <input
                v-model="password"
                type="password"
                placeholder="Password"
                required
                :disabled="loading"
              />
            </div>

            <div class="inputBox">
              <input type="submit" value="Login" :disabled="loading" />
            </div>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "@/utils/request";
import { ElMessage } from "element-plus"

const router = useRouter();
const username = ref("");
const password = ref("");
const loading = ref(false);

const handleLogin = async () => {
  if (loading.value) return;

  if (!username.value || !password.value) {
    ElMessage.warning("请输入用户名和密码");
    return;
  }

  loading.value = true;

  try {
    const res = await api.post("admin/login/", {
      username: username.value,
      password: password.value,
    });

    const tokenData = res.data.data;
    if (!tokenData) {
      ElMessage.error("登录失败：服务器返回数据格式错误");
      return;
    }

    localStorage.setItem("access_token", tokenData.token);
    localStorage.setItem("refresh_token", tokenData.refresh);
    localStorage.setItem("username", tokenData.username);
    localStorage.setItem("isLoggedIn", "true");

    ElMessage.success("登录成功！");
    router.push("/admin");
  } catch (err) {
    const errorMsg = err.response?.data?.msg || err.response?.data?.message || "用户名或密码错误！";
    ElMessage.error(errorMsg);
  } finally {
    loading.value = false;
  }
};
</script>


<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Poppins", sans-serif;
}

section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(to bottom, #f1f4f9, #dff1ff);
  overflow: hidden;
}

section .color {
  position: absolute;
  filter: blur(150px);
}

section .color:nth-child(1) {
  top: -350px;
  width: 600px;
  height: 600px;
  background: #ff359b;
}

section .color:nth-child(2) {
  bottom: 0px;
  left: 100px;
  width: 500px;
  height: 500px;
  background: #fffd87;
}

section .color:nth-child(3) {
  bottom: 50px;
  right: 100px;
  width: 500px;
  height: 500px;
  background: #00d2ff;
}

.box {
  position: relative;
}

.box .square {
  position: absolute;
  backdrop-filter: blur(5px);
  box-shadow: 0 25px 45px rgb(0, 0, 0, 0.1);
  border: 1px solid rgb(255, 255, 255, 0.5);
  border-right: 1px solid rgb(255, 255, 255, 0.2);
  border-bottom: 1px solid rgb(255, 255, 255, 0.2);
  background: rgb(255, 255, 255, 0.1);
  border-radius: 10px;
  animation: animate 10s linear infinite;
  animation-delay: calc(-1s * var(--i));
}

@keyframes animate {
  0%, 100% {
    transform: translateY(-40px);
  }
  50% {
    transform: translateY(40px);
  }
}

.container {
  position: relative;
  width: 400px;
  min-height: 400px;
  background: rgb(255, 255, 255, 0.1);
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(5px);
  box-shadow: 0 25px 45px rgb(0, 0, 0, 0.1);
  border: 1px solid rgb(255, 255, 255, 0.5);
  border-right: 1px solid rgb(255, 255, 255, 0.2);
  border-bottom: 1px solid rgb(255, 255, 255, 0.2);
}

.form {
  position: relative;
  height: 100%;
  width: 100%;
  padding: 40px;
}

.form h2 {
  position: relative;
  color: #fff;
  font-size: 24px;
  font-weight: 600;
  letter-spacing: 1px;
  margin-bottom: 40px;
}

.form h2::before {
  content: "";
  position: absolute;
  left: 0;
  bottom: -10px;
  width: 80px;
  height: 4px;
  background: #fff;
}

.form .inputBox {
  width: 100%;
  margin-top: 20px;
}

.form .inputBox input {
  width: 100%;
  background: rgb(255, 255, 255, 0.2);
  border: none;
  outline: none;
  padding: 10px 20px;
  border-radius: 35px;
  border: 1px solid rgb(255, 255, 255, 0.5);
  border-right: 1px solid rgb(255, 255, 255, 0.2);
  border-bottom: 1px solid rgb(255, 255, 255, 0.2);
  font-size: 16px;
  letter-spacing: 1px;
  color: black;
  box-shadow: 0 5px 15px rgb(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.form .inputBox input::placeholder {
  color: #fff;
}

.form .inputBox input[type="submit"] {
  background: #fff;
  color: #666;
  max-width: 100px;
  cursor: pointer;
  margin-bottom: 20px;
  font-weight: 600;
}

.form .inputBox input[type="submit"]:hover:not(:disabled) {
  background: #f0f0f0;
}

.form .inputBox input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
