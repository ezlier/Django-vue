<template>
  <div class="comment-section">
    <h3 class="comment-section__title">{{ title }}</h3>

    <!-- 发表表单 -->
    <form class="comment-form" @submit.prevent="submit">
      <div class="comment-form__row">
        <input
          v-model="form.name"
          type="text"
          placeholder="昵称 *"
          required
          maxlength="20"
          class="comment-form__input comment-form__input--name"
        />
        <input
          v-model="form.QQ"
          type="text"
          placeholder="QQ（可选）"
          maxlength="20"
          class="comment-form__input"
        />
        <input
          v-model="form.email"
          type="email"
          placeholder="Email（可选）"
          maxlength="50"
          class="comment-form__input"
        />
      </div>
      <textarea
        v-model="form.text"
        placeholder="说点什么..."
        required
        maxlength="400"
        rows="3"
        class="comment-form__textarea"
      ></textarea>
      <div class="comment-form__footer">
        <span class="comment-form__hint">{{ form.text.length }}/400</span>
        <button type="submit" class="comment-form__btn" :disabled="submitting">
          {{ submitting ? '发送中...' : '发表' }}
        </button>
      </div>
      <p v-if="error" class="comment-form__error">{{ error }}</p>
    </form>

    <!-- 评论列表 -->
    <ul class="comment-list" v-if="list.length">
      <li v-for="item in list" :key="item.id" class="comment-item">
        <div class="comment-item__avatar">
          <img
            v-if="qqAvatar(item)"
            :src="qqAvatar(item)!"
            :alt="item.name"
            class="comment-item__avatar-img"
            @error="onAvatarError"
          />
          <span v-else class="comment-item__avatar-text">
            {{ (item.name || '?')[0] }}
          </span>
        </div>
        <div class="comment-item__body">
          <div class="comment-item__header">
            <span class="comment-item__name">{{ item.name }}</span>
            <span class="comment-item__time">{{ item.time }}</span>
          </div>
          <p class="comment-item__text">{{ item.text }}</p>
        </div>
      </li>
    </ul>

    <p v-if="!loading && list.length === 0" class="comment-section__empty">
      暂无评论
    </p>

    <div v-if="loading" class="comment-section__loading">
      <span class="loading-spinner"></span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

interface CommentItem {
  id: number
  name: string
  text: string
  time: string
  QQ?: string
  email?: string
}

const props = defineProps<{
  title?: string
  // 获取列表的函数
  fetchFn: () => Promise<{ data: { data: CommentItem[] } }>
  // 提交评论的函数
  submitFn: (data: { name: string; text: string; QQ?: string; email?: string }) => Promise<any>
}>()

const list = ref<CommentItem[]>([])
const loading = ref(false)
const submitting = ref(false)
const error = ref('')

const form = ref({
  name: localStorage.getItem('comment_name') || '',
  QQ: localStorage.getItem('comment_qq') || '',
  email: localStorage.getItem('comment_email') || '',
  text: '',
})

function qqAvatar(item: CommentItem): string | null {
  if (item.QQ) {
    return `https://q1.qlogo.cn/g?b=qq&nk=${item.QQ}&s=100`
  }
  return null
}

function onAvatarError(e: Event) {
  const img = e.target as HTMLImageElement
  img.style.display = 'none'
  const span = img.nextElementSibling as HTMLElement
  if (span) span.style.display = 'flex'
}

async function load() {
  loading.value = true
  try {
    const res = await props.fetchFn()
    list.value = res.data.data || []
  } catch {
    // ignore
  } finally {
    loading.value = false
  }
}

async function submit() {
  if (!form.value.name.trim() || !form.value.text.trim()) {
    error.value = '请填写昵称和内容'
    return
  }
  error.value = ''
  submitting.value = true
  try {
    await props.submitFn({
      name: form.value.name.trim(),
      text: form.value.text.trim(),
      QQ: form.value.QQ.trim() || undefined,
      email: form.value.email.trim() || undefined,
    })
    // 记住昵称和 QQ
    localStorage.setItem('comment_name', form.value.name.trim())
    localStorage.setItem('comment_qq', form.value.QQ.trim())
    localStorage.setItem('comment_email', form.value.email.trim())
    form.value.text = ''
    ElMessage.success('发表成功')
    await load()
  } catch (err: any) {
    error.value = err.response?.data?.msg || '发表失败'
  } finally {
    submitting.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.comment-section {
  margin-top: 48px;
  padding-top: 24px;
  border-top: 1px solid var(--color-border);
}

.comment-section__title {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-heading);
  margin: 0 0 20px;
}

/* 发表表单 */
.comment-form {
  margin-bottom: 24px;
}

.comment-form__row {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.comment-form__input {
  flex: 1;
  padding: 10px 14px;
  border-radius: 10px;
  border: 1px solid var(--color-border);
  background: var(--color-background);
  color: var(--color-text);
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  font-family: inherit;
}

.comment-form__input:focus {
  border-color: var(--color-heading);
}

.comment-form__input--name {
  min-width: 100px;
}

.comment-form__textarea {
  width: 100%;
  padding: 10px 14px;
  border-radius: 10px;
  border: 1px solid var(--color-border);
  background: var(--color-background);
  color: var(--color-text);
  font-size: 14px;
  outline: none;
  resize: vertical;
  transition: border-color 0.2s;
  font-family: inherit;
  box-sizing: border-box;
}

.comment-form__textarea:focus {
  border-color: var(--color-heading);
}

.comment-form__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.comment-form__hint {
  font-size: 12px;
  color: var(--color-text-mute);
}

.comment-form__btn {
  padding: 8px 24px;
  border-radius: 10px;
  border: none;
  background: var(--color-heading);
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
  font-family: inherit;
}

.comment-form__btn:hover {
  opacity: 0.9;
}

.comment-form__btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.comment-form__error {
  color: #e74c3c;
  font-size: 13px;
  margin: 8px 0 0;
}

/* 评论列表 */
.comment-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-item {
  display: flex;
  gap: 12px;
}

.comment-item__avatar {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--color-background-mute);
}

.comment-item__avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.comment-item__avatar-text {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 700;
  color: var(--color-heading);
}

.comment-item__body {
  flex: 1;
  min-width: 0;
}

.comment-item__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.comment-item__name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-heading);
}

.comment-item__time {
  font-size: 12px;
  color: var(--color-text-mute);
}

.comment-item__text {
  font-size: 14px;
  color: var(--color-text);
  line-height: 1.6;
  margin: 0;
  word-break: break-word;
}

.comment-section__empty {
  text-align: center;
  padding: 32px 0;
  color: var(--color-text-mute);
  font-size: 14px;
}

.comment-section__loading {
  display: flex;
  justify-content: center;
  padding: 24px 0;
}

.loading-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-heading);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 640px) {
  .comment-form__row {
    flex-direction: column;
  }
}
</style>
