<template>
  <div class="upload-container">
    <div class="header">
      <el-button type="primary" @click="$router.back()">← 返回列表</el-button>
      <h2>发布新文章</h2>
    </div>

    <el-form :model="form" label-width="100px" style="max-width: 800px">
      <el-form-item label="文章标题" required>
        <el-input v-model="form.title" placeholder="请输入文章标题" />
      </el-form-item>

      <el-form-item label="文章标签">
        <el-select
          v-model="form.tags"
          multiple
          filterable
          allow-create
          default-first-option
          placeholder="请选择或输入标签"
        >
          <el-option label="Vue" value="Vue" />
          <el-option label="JavaScript" value="JavaScript" />
        </el-select>
      </el-form-item>

      <el-form-item label="文章封面">
        <el-upload
          action="#"
          list-type="picture-card"
          :auto-upload="false"
          :limit="1"
          v-model:file-list="coverFile"
          accept=".jpg,.jpeg,.png,.webp"
        >
          <el-icon><Plus /></el-icon>
        </el-upload>
      </el-form-item>

      <el-form-item label="MD文件" required>
        <el-upload
          drag
          action="#"
          :auto-upload="false"
          :limit="1"
          accept=".md"
          v-model:file-list="mdFile"
          :on-progress="handleProgress"
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text" style="width: 300px;">
            将 Markdown 文件拖到此处
          </div>
        </el-upload>
      </el-form-item>

      <el-form-item>
        <el-radio-group v-model="form.isDraft">
          <el-radio :value="false">直接发布</el-radio>
          <el-radio :value="true">保存为草稿</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" size="large" @click="submitForm">
          {{ form.isDraft ? '保存草稿' : '立即发布' }}
        </el-button>
      </el-form-item>

      <!-- 上传进度条 -->
      <el-form-item v-if="uploading">
        <el-progress :percentage="progress" />
        <p>上传速度: {{ uploadSpeed }} KB/s</p>
        <div style="margin-top: 10px;">
          <el-button @click="toggleUpload" :type="isPaused ? 'primary' : 'warning'">
            {{ isPaused ? '继续上传' : '暂停上传' }}
          </el-button>
        </div>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';
import { Plus, UploadFilled } from '@element-plus/icons-vue';
import { uploadArticles } from '@/utils/article';
import axios from 'axios';

const form = reactive({
  title: '',
  tags: [],
  isDraft: false
});

const coverFile = ref([]);
const mdFile = ref([]);
const progress = ref(0);  // 上传进度
const uploading = ref(false);  // 是否正在上传
const uploadSpeed = ref(0);  // 上传速度 (KB/s)
const lastTimestamp = ref(0);  // 上次上传时间戳
const lastLoadedBytes = ref(0);  // 上次已上传字节数
const isPaused = ref(false);  // 是否暂停上传
const cancelTokenSource = ref(null);  // 用于取消上传的token

const handleProgress = (event) => {
  if (event.lengthComputable && event.total > 0) {
    const percent = Math.round((event.loaded / event.total) * 100);
    progress.value = percent;
    
    // 计算上传速度（KB/s）
    const timeElapsed = (event.timeStamp - lastTimestamp.value) / 1000;  // 秒
    if (timeElapsed > 0 && lastTimestamp.value > 0) {
      const speed = (event.loaded - lastLoadedBytes.value) / timeElapsed / 1024;  // KB/s
      uploadSpeed.value = Math.round(speed);
    }

    lastTimestamp.value = event.timeStamp;
    lastLoadedBytes.value = event.loaded;
  }
};

const toggleUpload = () => {
  if (isPaused.value) {
    // 继续上传（重新开始）
    submitForm();
  } else {
    // 暂停上传（取消当前请求）
    if (cancelTokenSource.value) {
      cancelTokenSource.value.cancel('Upload paused by user');
      isPaused.value = true;
      ElMessage.info('上传已暂停');
    }
  }
};

const submitForm = async () => {
  if (!form.title || mdFile.value.length === 0) {
    return ElMessage.warning('请填写标题并上传 Markdown 文件');
  }

  const formData = new FormData()

  formData.append("title", form.title)

  form.tags.forEach(tag => {
    formData.append("tags", tag)
  })

  // 上传 md 文件
  formData.append("md_file", mdFile.value[0].raw)

  // 上传封面（可选）
  if (coverFile.value.length > 0) {
    formData.append("cover", coverFile.value[0].raw)
  }

  formData.append("is_draft", form.isDraft)

  try {
    // 重置上传状态
    progress.value = 0;
    uploadSpeed.value = 0;
    lastTimestamp.value = 0;
    lastLoadedBytes.value = 0;
    isPaused.value = false;

    // 创建新的cancelToken
    cancelTokenSource.value = axios.CancelToken.source();

    uploading.value = true;
    await uploadArticles(formData, {
      onUploadProgress: handleProgress,
      cancelToken: cancelTokenSource.value.token
    })
    ElMessage.success(form.isDraft ? "草稿保存成功喵！" : "上传成功喵！")
  } catch (err) {
    if (axios.isCancel(err)) {
      // 上传被用户取消，不显示错误信息
      return;
    }
    const msg =
      err.response?.data?.msg ||
      err.response?.data?.error ||
      "上传失败喵！"

    ElMessage.error(msg)
  } finally {
    uploading.value = false;
    isPaused.value = false;
    // 重置上传状态
    progress.value = 0;
    uploadSpeed.value = 0;
    lastTimestamp.value = 0;
    lastLoadedBytes.value = 0;
  }
};
</script>

<style scoped>
.upload-container {
  padding: 20px;
  background: #fff;
  border-radius: 8px;
}
.header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}
</style>