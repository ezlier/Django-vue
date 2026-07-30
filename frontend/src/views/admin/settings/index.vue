<template>
  <div class="page admin-settings">
    <h1>网站设置</h1>

    <el-form
      v-loading="loading"
      label-position="top"
      class="settings-form"
    >
      <el-row :gutter="24">
        <el-col :span="12">
          <el-form-item label="网站名称">
            <el-input v-model="form.web_name" placeholder="请输入网站名称" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="站长名称">
            <el-input v-model="form.name" placeholder="请输入站长名称" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="站长头像">
        <div class="avatar-row">
          <img v-if="form.name_avatar" :src="form.name_avatar" class="avatar-preview" />
          <el-upload
            :auto-upload="false"
            :limit="1"
            :on-change="onAvatarChange"
            :file-list="avatarFileList"
            accept="image/*"
            list-type="picture"
          >
            <el-button>更换头像</el-button>
          </el-upload>
        </div>
      </el-form-item>

      <el-form-item label="页脚文字1">
        <el-input v-model="form.footer_text1" placeholder="请输入页脚第一行文字" />
      </el-form-item>

      <el-form-item label="页脚文字2">
        <el-input v-model="form.footer_text2" placeholder="请输入页脚第二行文字" />
      </el-form-item>

      <el-form-item label="关于页 Markdown">
        <MdEditor v-if="showAboutEditor" v-model="form.about_md" />
        <div v-else class="editor-placeholder">
          <el-button type="primary" @click="showAboutEditor = true">编写关于页内容</el-button>
        </div>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleSave" :loading="saving">保存设置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getAdminWebSetting, updateWebSetting } from '@/api/admin'
import { ElMessage } from 'element-plus'
import MdEditor from '@/components/MdEditor.vue'
import type { UploadFile } from 'element-plus'

const loading = ref(false)
const saving = ref(false)
const showAboutEditor = ref(false)

const form = ref({
  web_name: '',
  name: '',
  name_avatar: null as File | null,
  name_avatar_url: '',
  footer_text1: '',
  footer_text2: '',
  about_md: '',
})

const avatarFileList = ref<UploadFile[]>([])

function onAvatarChange(uploadFile: UploadFile) {
  form.value.name_avatar = uploadFile.raw || null
  avatarFileList.value = [uploadFile]
}

async function fetchSettings() {
  loading.value = true
  try {
    const res = await getAdminWebSetting()
    const data = res.data.data || res.data
    form.value.web_name = data.web_name || ''
    form.value.name = data.name || ''
    form.value.name_avatar_url = data.name_avatar || ''
    form.value.footer_text1 = data.footer_text1 || ''
    form.value.footer_text2 = data.footer_text2 || ''
    form.value.about_md = data.about_md || ''
    showAboutEditor.value = !!data.about_md
  } catch {
    ElMessage.error('获取网站设置失败')
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  saving.value = true
  try {
    const fd = new FormData()
    fd.append('web_name', form.value.web_name)
    fd.append('name', form.value.name)
    fd.append('footer_text1', form.value.footer_text1)
    fd.append('footer_text2', form.value.footer_text2)
    fd.append('about_md', form.value.about_md)
    if (form.value.name_avatar) {
      fd.append('name_avatar', form.value.name_avatar)
    }
    await updateWebSetting(fd)
    ElMessage.success('设置已保存')
    fetchSettings()
  } catch {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchSettings()
})
</script>

<style scoped>
.settings-form {
  max-width: 860px;
  margin-top: 20px;
}

.avatar-row {
  display: flex;
  align-items: center;
  gap: 16px;
}

.avatar-preview {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--color-border, #dcdfe6);
}

.editor-placeholder {
  border: 2px dashed var(--color-border, #dcdfe6);
  border-radius: 8px;
  padding: 32px;
  text-align: center;
}
</style>
