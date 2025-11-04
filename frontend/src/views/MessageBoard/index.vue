<template>
    <navbar />
    <div class="bg"></div>
    <div class="main-content">
        <div class="row">
            <div class="message-box">
                <el-input v-model="form.message" style="width: 100%" type="textarea"
                    :autosize="{ minRows: 6, maxRows: 6 }" placeholder="Please input" maxlength="400" show-word-limit />
                <div class="sure">
                    <el-input v-model="form.name" style="width: 240px" maxlength="10" show-word-limit
                        placeholder="name" />
                    <button class="custom-btn btn-8" @click="pushMessage"><span>这是提交喵</span></button>
                </div>
            </div>
            <div class="message-list">
                <div class="message-card" v-for="(value, index) in messageList" :key="index">
                    <div class="message-header">
                        <span class="name">{{ value.name }}</span>
                        <span class="time">{{ value.time ? value.time.slice(0, 19).replace('T', ' ') : '' }}</span>
                    </div>
                    <div class="message-body">
                        {{ value.text }}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footera />
</template>

<script setup>
import navbar from "@/views/Layout/components/nav.vue"
import footera from "@/views/Layout/components/Footer.vue"
import { ElMessage } from "element-plus"
import { upMessage, getMessage } from '@/utils/message'
import { onMounted, ref } from 'vue'

const form = ref({
    message: "",
    name: "",
})

const a = async () =>{
    const res = await getMessage()
    messageList.value = res.data
}

const messageList = ref([])

const pushMessage = async () => {
    try {
        const res = await upMessage(form.value)
        ElMessage.success("发送成功！")
        a()
    } catch (err) {
        console.error(err)
        ElMessage.error("发送失败！")
    }
}

onMounted(a)


</script>

<style scoped>
.main-content {
    min-height: 100vh;
}

.bg {
    position: fixed;
    /* 固定在视口 */
    top: 0;
    left: 0;
    width: 100vw;
    /* 拉伸占满全屏 */
    height: 100vh;
    background-image: url('@/assets/img/bg3.jpg');
    background-size: cover;
    /* 拉伸裁剪为最大，保持比例 */
    background-repeat: no-repeat;
    background-position: center;
    z-index: -1;
    /* 放到内容后面 */
}

.row {
    max-width: 900px;
    padding: 20px;
    justify-content: center;
    margin: 0 auto;
    width: 100%;
    box-sizing: border-box;
}

.message-box {
    padding: 50px;
    margin-top: 80px;
    width: 100%;
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 10px;
}

.sure {
    padding: 20px;
}

.message-list {
    margin-top: 40px;
    display: grid;
    gap: 20px;
    grid-template-columns: repeat(3, minmax(100px, 1fr));
}

.custom-btn {
    float: right;
    width: 100px;
    height: 40px;
    color: #fff;
    border-radius: 5px;
    padding: 10px 25px;
    font-family: 'Lato', sans-serif;
    font-weight: 500;
    background: transparent;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    display: inline-block;
    box-shadow: inset 2px 2px 2px 0px rgba(255, 255, 255, .5),
        7px 7px 20px 0px rgba(0, 0, 0, .1),
        4px 4px 5px 0px rgba(0, 0, 0, .1);
    outline: none;
}

.btn-8 {
    background-color: #f0ecfc;
    background-image: linear-gradient(315deg, #f0ecfc 0%, #c797eb 74%);
    line-height: 42px;
    padding: 0;
    border: none;
}

.btn-8 span {
    position: relative;
    display: block;
    width: 100%;
    height: 100%;
}

.btn-8:before,
.btn-8:after {
    position: absolute;
    content: "";
    right: 0;
    bottom: 0;
    background: #c797eb;
    /*box-shadow:  4px 4px 6px 0 rgba(255,255,255,.5),
              -4px -4px 6px 0 rgba(116, 125, 136, .2), 
    inset -4px -4px 6px 0 rgba(255,255,255,.5),
    inset 4px 4px 6px 0 rgba(116, 125, 136, .3);*/
    transition: all 0.3s ease;
}

.btn-8:before {
    height: 0%;
    width: 2px;
}

.btn-8:after {
    width: 0%;
    height: 2px;
}

.btn-8:hover:before {
    height: 100%;
}

.btn-8:hover:after {
    width: 100%;
}

.btn-8:hover {
    background: transparent;
}

.btn-8 span:hover {
    color: #c797eb;
}

.btn-8 span:before,
.btn-8 span:after {
    position: absolute;
    content: "";
    left: 0;
    top: 0;
    background: #c797eb;
    /*box-shadow:  4px 4px 6px 0 rgba(255,255,255,.5),
              -4px -4px 6px 0 rgba(116, 125, 136, .2), 
    inset -4px -4px 6px 0 rgba(255,255,255,.5),
    inset 4px 4px 6px 0 rgba(116, 125, 136, .3);*/
    transition: all 0.3s ease;
}

.btn-8 span:before {
    width: 2px;
    height: 0%;
}

.btn-8 span:after {
    height: 2px;
    width: 0%;
}

.btn-8 span:hover:before {
    height: 100%;
}

.btn-8 span:hover:after {
    width: 100%;
}

.message-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 20px 24px;
  line-height: 1.6;
  word-wrap: break-word;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

/* 悬停动画 */
.message-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

/* 名字与时间 */
.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.name {
  font-weight: 600;
  color: #7b4bb7;
  font-size: 1.1em;
}

.time {
  font-size: 0.85em;
  color: #888;
}

/* 正文部分自适应高度 */
.message-body {
  white-space: pre-wrap; /* 保留换行 */
  font-size: 1em;
  color: #333;
}

@media (max-width: 768px) {
    .message-list {
        grid-template-columns: 1fr;
    }
}
</style>