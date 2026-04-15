<template>
  <div class="upload-container">
    <div class="header">
      <el-button type="primary" @click="$router.back()">← 返回列表</el-button>
      <h2>发布新文章</h2>
    </div>

    <el-form :model="form" label-width="100px">
      <div class="top-info-row">
        <div class="left-inputs">
          <el-form-item label="文章标题" required>
            <el-input v-model="form.title" placeholder="请输入文章标题" />
          </el-form-item>

          <el-form-item label="文章标签">
            <el-select
              v-model="form.tags"
              multiple
              filterable
              allow-create
              placeholder="请选择或输入标签"
              style="width: 100%"
            >
            </el-select>
          </el-form-item>
        </div>

        <div class="right-upload">
          <el-form-item label="文章封面">
            <el-upload
              list-type="picture-card"
              :auto-upload="false"
              :limit="1"
              v-model:file-list="coverFile"
              :on-change="handleFileChange"
              :on-remove="handleRemove"
              :class="{ hide: coverFile.length >= 1 }"
              accept=".jpg,.jpeg,.png,.webp"
            >
              <el-icon><Plus /></el-icon>
              <template #file="{ file }">
                <div class="upload-preview" @click="handleReUpload">
                  <img class="el-upload-list__item-thumbnail" :src="file.url" alt="" />
                  <div class="upload-hover-mask">
                    <span>更换图片</span>
                  </div>
                </div>
              </template>
            </el-upload>
          </el-form-item>
        </div>
      </div>

      <div class="editor-wrapper">
        <MdEditor v-model="form.mdFile" height="500px" />
      </div>

      <div class="footer-action">
        <el-radio-group v-model="form.isDraft">
          <el-radio :value="false">直接发布</el-radio>
          <el-radio :value="true">保存为草稿</el-radio>
        </el-radio-group>
        <el-button type="primary" size="large" @click="submitForm">
          {{ form.isDraft ? '保存草稿' : '发布文章' }}
        </el-button>
      </div>
    </el-form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { MdEditor } from "md-editor-v3"
import "md-editor-v3/lib/style.css"
import { ElMessage } from 'element-plus'
import { CreateArticle } from '@/utils/article'

const form = reactive({
  title: '',
  tags: [],
  mdFile: '',
  isDraft: false
})

const coverFile = ref([])

// 模拟重新上传：点击图片时清空列表，触发文件选择
const handleReUpload = () => {
  coverFile.value = []
}

const submitForm = async () => {
    
    if (!form.title || form.mdFile.length === 0) {
        return ElMessage.warning('请填写标题和文章内容')
    }

    const formData = new FormData()

    formData.append("title", form.title)
    formData.append("mdfile", form.mdFile)
    form.tags.forEach(tag => {
        formData.append("tags", tag)
    });

    if (coverFile.value.length > 0) {
        formData.append("cover", coverFile.value[0].raw)
    }

    formData.append("is_draft", form.isDraft)

    try {
    await CreateArticle(formData)
    ElMessage.success(form.isDraft ? "草稿保存成功！" : "发布成功！")
  } catch (err) {
    const msg =
      err.response?.data?.msg ||
      err.response?.data?.error ||
      (form.isDraft ? "保存失败！" : "发布失败！")

    ElMessage.error(msg)
  }
}
</script>

<style scoped>
.upload-container {
  background: #fff;
  border-radius: 12px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 40px;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 20px;
}

.top-info-row {
  display: flex;
  gap: 40px;
}

.left-inputs {
  flex: 1;
  max-width: 600px;
}

:deep(.hide .el-upload--picture-card) {
  display: none;
}

.upload-preview {
  position: relative;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.upload-hover-mask {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
  border-radius: 6px;
}

.upload-preview:hover .upload-hover-mask {
  opacity: 1;
}

.editor-wrapper {
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  overflow: hidden;
}

.footer-action {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}
</style>