<template>
  <div>
    <h1>📰网站基础设置</h1>
    <div>
      名称：
      <el-input v-model="form.name" placeholder="请输入网站名称" style="width: 100%" />
    </div>

    <div>
      网站名字：
      <el-input v-model="form.blog_name" placeholder="请输入网站名称" style="width: 100%" />
    </div>

    <div>
      网站运行日期：
      <el-input v-model="form.date" placeholder="请输入开始运行日期" style="width: 100%" />
    </div>

    <div>
      页脚文案：
      <el-input v-model="form.footer_text1" placeholder="请输入页脚文字" style="width: 100%" />
    </div>

    <div>
      备案号：
      <el-input v-model="form.footer_text2" placeholder="请输入页脚文字" style="width: 100%" />
    </div>

    <div style="margin-top: 15px;">
      <button @click="saveWebSetting">保存修改</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { ElMessage } from "element-plus"
import { getWebSetting, updateWebSetting } from "@/utils/websetting"

const form = ref({
  name: "",
  blog_name: "",
  date: "",
  footer_text1: "",
  footer_text2: "",
})

onMounted(async () => {
  const res = await getWebSetting()
  form.value = res.data
})

const saveWebSetting = async () => {
  try {
    const res = await updateWebSetting(form.value)
    ElMessage.success("保存成功！")
  } catch (err) {
    console.error(err)
    ElMessage.error("保存失败！")
  }
}
</script>
