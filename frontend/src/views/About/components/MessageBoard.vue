<template>
    <div class="main-content">
        <div class="row">
            <el-divider content-position="left" class="divider">分割线喵</el-divider>
            <h1>留言板</h1>
            <div class="message-box fade-in" v-fade-in>
                <el-input v-model="form.text" style="width: 100%" type="textarea"
                    :autosize="{ minRows: 6, maxRows: 6 }" placeholder="Please input" maxlength="400" show-word-limit/>
                <div class="sure">
                    <el-input v-model="form.name" style="width: 240px" maxlength="10" show-word-limit placeholder="name" />
                    <el-input v-model="form.QQ" style="width: 240px" maxlength="10" show-word-limit placeholder="QQ" />
                    <el-input v-model="form.email" style="width: 240px" maxlength="10" show-word-limit placeholder="E-mail" />
                    <div>
                        <span>{{ num1 }} + {{ num2 }} = 
                            <el-input v-model="input" style="width: 50px" placeholder="?" maxlength="3"/>
                        </span>
                        <button class="custom-btn btn-8" @click="pushMessage"><span>这是提交喵</span></button>
                    </div>
                    
                </div>
            </div>
            <div class="message-list">
                <div class="message-card fade-in" v-for="(value, index) in messageList" :key="index" v-fade-in>
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
</template>

<script setup>
import { ElMessage } from "element-plus"
import { upMessage, getMessage } from '@/utils/message'
import { onMounted, ref } from 'vue'

const form = ref({
    text: "",
    name: "",
    QQ:"",
    email:"",
})

const get_message = async () =>{
    const res = await getMessage()
    messageList.value = res.data.data
}

const messageList = ref([])

const pushMessage = async () => {
    const userInput = input.value.trim()
    const userValue = parseInt(userInput)
    if(num3!==userValue){
        ElMessage.error("请完成左边的计算")
        return false
    }
    try {
        await upMessage(form.value)

        ElMessage.success("发送成功！")
        get_message()

    } catch (err) {
        const msg =
            err.response?.data?.msg ||
            err.response?.data?.error ||
            "发送失败！"

        ElMessage.error(msg)
    }
}

onMounted(get_message)

const num1 = Math.floor(Math.random()*10);
const num2 = Math.floor(Math.random()*10);
const num3 = num1 + num2;
const input = ref('')

</script>

<style scoped>
.row {
    justify-content: center;
    margin: 0 auto;
    width: 100%;
    box-sizing: border-box;
}

.message-box {
    /* padding: 50px; */
    width: 100%;
    border-radius: 10px;
}

.sure {
    padding: 20px;
}

.message-list {
    margin-top: 40px;
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
    background-image: linear-gradient(315deg, #f0ecfc 0%, #ffc7c7 74%);
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
    background: #ffc7c7;
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
    color: #ffc7c7;
}

.btn-8 span:before,
.btn-8 span:after {
    position: absolute;
    content: "";
    left: 0;
    top: 0;
    background: #ffc7c7;
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
  padding: 20px 24px;
  line-height: 1.6;
  word-wrap: break-word;
  border-bottom: 1px solid #E3E5E7;
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
  color: #61666D;
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
  color: var(--text-color);
}

:deep(.el-textarea__inner) {
    resize: none !important;
}

@media (max-width: 768px) {
    .message-list {
        grid-template-columns: 1fr;
    }
}
</style>