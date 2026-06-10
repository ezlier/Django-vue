<script setup>
import { getcomment, upcomment } from '@/utils/getcomment';
import { onMounted, ref, reactive } from 'vue';
import { useRoute } from "vue-router"
import { ElMessage } from "element-plus"

const comment = ref([])
const route = useRoute()
const loading = ref(false)   // 按钮 loading

const form = reactive({
    text: "",
    name: "",
    QQ: "",
    email: "",
    article: "",
})

onMounted(async () => {
    const slug = route.params.slug
    form.article = slug
    await loadComments()
})

// 加载评论
const loadComments = async () => {
    const res = await getcomment(form.article)
    comment.value = res.data.data
}

// 表单校验
function validateForm() {
    if (!form.text.trim()) {
        ElMessage.error("说点什么再提交喵~")
        return false
    }

    if (form.email && !/^\S+@\S+\.\S+$/.test(form.email)) {
        ElMessage.error("E-mail 格式不太对喵~")
        return false
    }

    if (form.QQ && !/^\d+$/.test(form.QQ)) {
        ElMessage.error("QQ 只能是数字喵~")
        return false
    }

    return true
}

// 提交评论
const pushcomment = async () => {
    const userInput = input.value.trim()
    const userValue = parseInt(userInput)
    if(num3!==userValue){
        ElMessage.error("请完成左边的计算")
        return false
    }

    if (!validateForm()) return

    if (loading.value) return
    loading.value = true

    try {
        await upcomment(form.article, form)
        ElMessage.success("发送成功喵！")

        // 清空表单
        form.text = ""
        form.name = ""
        form.QQ = ""
        form.email = ""

        // 刷新评论
        await loadComments()
    } catch (err) {
        const msg =
            err.response?.data?.msg ||
            err.response?.data?.error ||
            "发送失败喵！"

        ElMessage.error(msg)
    }

    loading.value = false
}

const num1 = Math.floor(Math.random()*10);
const num2 = Math.floor(Math.random()*10);
const num3 = num1 + num2;
const input = ref('')
</script>



<template>
    <div class="comment-section">
        <div class="comment-input fade-in" v-fade-in>
            <textarea 
                v-model="form.text" 
                class="form-control"
                placeholder="听说在这评论喵，讲话会不自觉带上某种口癖喵……是真的喵！">
            </textarea>

            <div class="send">
                <div class="inputs-row">
                    <el-input v-model="form.name" style="width: 100%" maxlength="10"
                        show-word-limit placeholder="name" />

                    <el-input v-model="form.QQ" style="width: 100%" maxlength="12"
                        show-word-limit placeholder="QQ" />

                    <el-input v-model="form.email" style="width: 100%" maxlength="50"
                        show-word-limit placeholder="E-mail" />
                </div>
                <div>
                    <span>{{ num1 }} + {{ num2 }} = 
                        <el-input v-model="input" style="width: 50px" placeholder="?" maxlength="3"/>
                    </span>
                    <button class="custom-btn btn-8" @click="pushcomment" :disabled="loading">
                        <span>
                            {{ loading ? "喵…发送中…" : "这是提交喵" }}
                        </span>
                    </button>
                </div>
                
            </div>
        </div>

        <div class="comment-list">
            <div class="comment-card fade-in" v-for="value in comment" :key="value.id" v-fade-in>
                <div class="comt-header">
                    <span class="name">{{ value.name }}</span>
                    <span class="time">{{ value.time ? value.time.slice(0, 19).replace('T', ' ') : '' }}</span>
                </div>
                <div class="comt-body">
                    <p>{{ value.text }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.comment-section {
    padding: 0px !important;
}

.comment-input {
    border: 2px solid #ccd4d9;
}

.inputs-row {
    display: flex;
    gap: 15px;
    /* 输入框之间的间距 */
    margin-bottom: 12px;
}

.send .custom-btn {
    display: block;
    margin-left: auto;
    /* 自动推到右边 */
}

.form-control {
    resize: none;
    width: 100%;
    height: 68px;
    border: none;
    outline: none;
    background-image: url('@/assets/img/bg4.png');
    background-repeat: no-repeat;
    background-position: right bottom;
    background-size: 60px 60px;
    line-height: 22px;
    font-size: 14px;
}

.comment-card {
    background: var(--bg-color);
    padding: 16px 20px;
    margin-bottom: 18px;
    border: var(--border);
    box-shadow: var(--box-shadow);
    border-radius: var(--border-radius);
    background-image: url('@/assets/img/bg5.png');
    background-repeat: no-repeat;
    background-position: right bottom;
    background-size: 60px 60px;
}


/* 名字与时间 */
.comt-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
}

.name {
    font-weight: 700;
    color: #5A3E99;
    font-size: 1.05rem;
}

.time {
    font-size: 0.85rem;
    color: #9ca3af;
}

/* 正文部分自适应高度 */
.comt-body {
    white-space: pre-wrap;
    word-wrap: break-word;
    overflow-wrap: break-word;
    line-height: 1.75;
    font-size: 0.96rem;
    margin-top: 6px;
}

.custom-btn {
    width: 100px;
    height: 100%;
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
    box-shadow:  4px 4px 6px 0 rgba(255,255,255,.5),
              -4px -4px 6px 0 rgba(116, 125, 136, .2), 
    inset -4px -4px 6px 0 rgba(255,255,255,.5),
    inset 4px 4px 6px 0 rgba(116, 125, 136, .3);
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
    box-shadow: 4px 4px 6px 0 rgba(255, 255, 255, .5),
        -4px -4px 6px 0 rgba(116, 125, 136, .2),
        inset -4px -4px 6px 0 rgba(255, 255, 255, .5),
        inset 4px 4px 6px 0 rgba(116, 125, 136, .3);
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

@media (max-width: 768px) {
    .inputs-row {
        display: block;
        width: 100%;
    }
}
</style>