<template>
  <div class="page admin-article-upload">
    <h1>上传文章</h1>

    <el-form label-position="top" class="article-form">
      <!-- 文章标题 -->
      <el-form-item label="文章标题">
        <el-input v-model="form.title" placeholder="请输入文章标题" />
      </el-form-item>

      <!-- 标签 -->
      <el-form-item label="标签">
        <div class="tag-input-area">
          <span v-for="(tag, idx) in form.tagNames" :key="idx" class="tag-chip">
            {{ tag }}
            <button class="tag-chip__remove" @click="removeTag(idx)">&times;</button>
          </span>
          <template v-if="addingTag">
            <el-input ref="tagInputRef" v-model="newTagName" size="small" style="width: 140px" placeholder="输入标签名"
              @keyup.enter="confirmAddTag" @keyup.escape="cancelAddTag" @blur="confirmAddTag" />
          </template>
          <button v-else class="tag-add-btn" @click="startAddTag">+</button>
        </div>
      </el-form-item>

      <!-- 文章封面 -->
      <el-form-item label="文章封面">
        <div class="cover-area">
          <div class="cover-placeholder" @click="triggerCoverUpload">
            <img v-if="coverPreview" :src="coverPreview" class="cover-img" />
            <div v-else class="cover-empty">
              <span class="cover-empty__icon">🖼</span>
              <span class="cover-empty__text">无封面图</span>
            </div>
          </div>
          <el-upload ref="coverUploadRef" class="cover-upload-hidden" :auto-upload="false" :show-file-list="false"
            :on-change="onCoverChange" accept="image/*">
          </el-upload>
        </div>
      </el-form-item>

      <!-- Markdown 文件上传 -->
      <el-form-item label="Markdown 文件">
        <el-upload class="md-upload" :auto-upload="false" :limit="1" :on-change="onMdFileChange" :file-list="mdFileList"
          accept=".md,.markdown,.txt">
          <el-button type="primary">选择 .md 文件</el-button>
        </el-upload>
      </el-form-item>

      <!-- 操作按钮 -->
      <el-form-item>
        <div class="form-actions">
          <el-button @click="handleSaveDraft" :loading="saving">保存草稿</el-button>
          <el-button type="success" @click="handlePublish" :loading="publishing">直接发布</el-button>
        </div>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { uploadArticle } from '@/api/admin'
import { ElMessage } from 'element-plus'
import type { UploadFile, UploadInstance, ElInput } from 'element-plus'

const router = useRouter()

const saving = ref(false)
const publishing = ref(false)

const form = ref({
  title: '',
  tagNames: [] as string[],
  cover: null as File | null,
  mdFile: null as File | null,
})

// ── 封面 ──
const coverPreview = ref('')
const coverUploadRef = ref<UploadInstance | null>(null)

function triggerCoverUpload() {
  const el = coverUploadRef.value?.$el as HTMLElement | undefined
  const input = el?.querySelector('input[type="file"]') as HTMLInputElement | null
  input?.click()
}

function onCoverChange(uploadFile: UploadFile) {
  form.value.cover = uploadFile.raw || null
  if (uploadFile.raw) {
    coverPreview.value = URL.createObjectURL(uploadFile.raw)
  }
}

// ── 标签 ──
const addingTag = ref(false)
const newTagName = ref('')
const tagInputRef = ref<InstanceType<typeof ElInput> | null>(null) as any

function startAddTag() {
  addingTag.value = true
  nextTick(() => {
    const el = tagInputRef.value?.$el as HTMLElement | undefined
    const input = el?.querySelector('input') as HTMLInputElement | null
    input?.focus()
  })
}

function confirmAddTag() {
  const name = newTagName.value.trim()
  if (name && !form.value.tagNames.includes(name)) {
    form.value.tagNames.push(name)
  }
  newTagName.value = ''
  addingTag.value = false
}

function cancelAddTag() {
  newTagName.value = ''
  addingTag.value = false
}

function removeTag(idx: number) {
  form.value.tagNames.splice(idx, 1)
}

// ── MD 文件 ──
const mdFileList = ref<UploadFile[]>([])

function onMdFileChange(uploadFile: UploadFile) {
  form.value.mdFile = uploadFile.raw || null
  mdFileList.value = [uploadFile]
}

// ── 提交 ──
async function buildFormData(isDraft: boolean): Promise<FormData> {
  const fd = new FormData()
  fd.append('title', form.value.title)

  if (form.value.mdFile) {
    fd.append('mdfile', form.value.mdFile)
  }

  fd.append('is_draft', String(isDraft))
  fd.append('tags', JSON.stringify(form.value.tagNames))

  if (form.value.cover) {
    fd.append('cover', form.value.cover)
  }

  return fd
}

async function handleSaveDraft() {
  if (!form.value.mdFile) {
    ElMessage.warning('请先选择 Markdown 文件')
    return
  }
  saving.value = true
  try {
    const fd = await buildFormData(true)
    await uploadArticle(fd)
    ElMessage.success('草稿已保存')
    router.push('/admin/articles')
  } catch {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

async function handlePublish() {
  if (!form.value.mdFile) {
    ElMessage.warning('请先选择 Markdown 文件')
    return
  }
  publishing.value = true
  try {
    const fd = await buildFormData(false)
    await uploadArticle(fd)
    ElMessage.success('文章已发布')
    router.push('/admin/articles')
  } catch {
    ElMessage.error('发布失败')
  } finally {
    publishing.value = false
  }
}
</script>

<style scoped>
.article-form {
  max-width: 960px;
  margin-top: 20px;
}

.form-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

/* ── 标签 ── */
.tag-input-area {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: var(--color-background-mute, #f0f2f5);
  border-radius: 4px;
  font-size: 13px;
  color: var(--color-text, #333);
}

.tag-chip__remove {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  border: none;
  border-radius: 50%;
  background: transparent;
  color: #999;
  font-size: 14px;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.tag-chip__remove:hover {
  background: #ddd;
  color: #333;
}

.tag-add-btn {
  width: 30px;
  height: 28px;
  border: 1px dashed var(--color-border, #dcdfe6);
  border-radius: 4px;
  background: transparent;
  color: var(--color-text, #666);
  font-size: 18px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  transition: border-color 0.2s, color 0.2s;
}

.tag-add-btn:hover {
  border-color: var(--color-heading, #42b883);
  color: var(--color-heading, #42b883);
}

/* ── 封面 ── */
.cover-area {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.cover-placeholder {
  width: 200px;
  height: 124px;
  border: 2px dashed var(--color-border, #dcdfe6);
  border-radius: 8px;
  cursor: pointer;
  overflow: hidden;
  transition: border-color 0.2s;
}

.cover-placeholder:hover {
  border-color: var(--color-heading, #42b883);
}

.cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-empty {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background: var(--color-background-mute, #fafbfc);
}

.cover-empty__icon {
  font-size: 32px;
  opacity: 0.6;
}

.cover-empty__text {
  font-size: 13px;
  color: #999;
}

.cover-upload-hidden {
  display: none;
}
</style>
