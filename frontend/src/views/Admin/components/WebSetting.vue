<template>
  <div class="setting-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span class="header-title">📰 网站基础设置</span>
        </div>
      </template>

      <el-form :model="form" label-width="120px" label-position="left">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="名称">
              <el-input v-model="form.name" placeholder="请输入网站名称" />
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="网站名字">
              <el-input v-model="form.web_name" placeholder="副标题或短名称" />
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="运行日期">
              <el-date-picker
                v-model="form.updated_time"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="备案号">
              <el-input v-model="form.footer_text2" placeholder="如：京ICP备xxxxxx号" />
            </el-form-item>
          </el-col>

          <el-col :span="24">
            <el-form-item label="网站头像">
              <el-upload
                class="avatar-uploader"
                action="#"
                :auto-upload="false"
                :show-file-list="false"
                :on-change="handleAvatarChange"
              >
                <img v-if="imageUrl" :src="imageUrl" class="avatar" />
                <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
              </el-upload>
            </el-form-item>
          </el-col>

          <el-col :span="24">
            <el-form-item label="页脚文案">
              <el-input
                v-model="form.footer_text1"
                type="textarea"
                placeholder="请输入页脚详细文案"
              />
            </el-form-item>
          </el-col>

          <el-col :span="24">
            <el-form-item label="关于文档">
              <div class="editor-wrapper">
                <MdEditor v-model="form.about_md" height="400px" />
              </div>
            </el-form-item>
          </el-col>
        </el-row>

        <div class="form-footer">
          <el-button type="primary" size="large" @click="saveWebSetting" :loading="loading">
            保存修改
          </el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { ElMessage } from "element-plus"
import { Plus } from "@element-plus/icons-vue"
import { getWebSetting, updateWebSetting } from "@/utils/websetting"
import { MdEditor } from "md-editor-v3"
import "md-editor-v3/lib/style.css"

const loading = ref(false)
const imageUrl = ref("") // 用于存储本地预览地址
const rawFile = ref(null) // 用于存储原始文件对象

const form = ref({
  name: "",
  web_name: "",
  updated_time: "",
  footer_text1: "",
  footer_text2: "",
  about_md: "",
  // 注意：name_avatar 在后端如果是文件，这里初始可以不放，也可以存 URL
})

onMounted(async () => {
  const res = await getWebSetting()
  const data = res.data.data

  form.value.name = data.name
  form.value.web_name = data.web_name
  form.value.updated_time = data.updated_time
  form.value.footer_text1 = data.footer_text1
  form.value.footer_text2 = data.footer_text2
  form.value.about_md = data.about_md

  if (data.name_avatar) {
    imageUrl.value = data.name_avatar
  }
})

// 当用户选择图片时触发
const handleAvatarChange = (file) => {
  const isJPGorPNG = file.raw.type === 'image/jpeg' || file.raw.type === 'image/png';

  if (!isJPGorPNG) {
    ElMessage.error('图片只能是 JPG 或 PNG 格式!');
    return false;
  }

  // 1. 保存原始文件对象用于上传
  rawFile.value = file.raw;
  // 2. 创建本地 URL 用于回显预览
  imageUrl.value = URL.createObjectURL(file.raw);
}

const saveWebSetting = async () => {
  loading.value = true

  const formData = new FormData()

  Object.entries(form.value).forEach(([key, value]) => {
    if (value !== null && value !== undefined && value !== "") {
      formData.append(key, value)
    }
  })

  if (rawFile.value) {
    formData.append("name_avatar", rawFile.value)
  }

  try {
    await updateWebSetting(formData)
    ElMessage.success("保存成功！")
    rawFile.value = null
  } catch (err) {
    ElMessage.error("保存失败")
  } finally {
    loading.value = false
  }
}
</script>


<style scoped>
.setting-container {
  background-color: #f5f7fa;
  min-height: 100vh;
}



.header-title {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}

.editor-wrapper {
  width: 100%;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

.form-footer {
  margin-top: 30px;
  text-align: center;
  border-top: 1px solid #ebeef5;
  padding-top: 20px;
}

/* 头像上传样式 */
.avatar-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 100px;
  height: 100px;
  transition: border-color 0.3s;
}

.avatar-uploader:hover {
  border-color: #409eff;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  text-align: center;
  line-height: 100px;
}

.avatar {
  width: 100px;
  height: 100px;
  display: block;
  object-fit: cover;
}

.upload-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
}
</style>
