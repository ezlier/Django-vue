<template>
  <section class="comment-section">
    <h3 class="comment-section__title">{{ title }}</h3>

    <!-- 输入表单 -->
    <CommentForm ref="formRef" @submit="onSubmit" />

    <!-- 评论列表 -->
    <div class="comment-section__list" v-if="comments.length">
      <div
        v-for="item in comments"
        :key="item.id"
        class="comment-item"
      >
        <div class="comment-item__avatar">
          <img
            v-if="item.QQ"
            :src="`https://q1.qlogo.cn/g?b=qq&nk=${item.QQ}&s=100`"
            :alt="item.name"
            class="comment-item__avatar-img"
            @error="onAvatarError(item)"
          />
          <div v-else class="comment-item__avatar-placeholder">
            {{ item.name[0] }}
          </div>
        </div>

        <div class="comment-item__body">
          <div class="comment-item__head">
            <span class="comment-item__name">{{ item.name }}</span>
            <span class="comment-item__time">{{ item.time }}</span>
          </div>
          <p class="comment-item__text">{{ item.text }}</p>
        </div>
      </div>
    </div>

    <p v-else class="comment-section__empty">暂无评论，来说两句吧</p>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import CommentForm from './CommentForm.vue'

interface CommentItem {
  id: number | string
  name: string
  text: string
  time: string
  QQ?: string
  email?: string
  _avatarFailed?: boolean
}

const props = defineProps<{
  title?: string
  comments: CommentItem[]
}>()

const emit = defineEmits<{
  submit: [data: { name: string; text: string; QQ?: string; email?: string }]
}>()

function onAvatarError(item: CommentItem) {
  item._avatarFailed = true
}

async function onSubmit(data: { name: string; text: string; QQ?: string; email?: string }) {
  try {
    await emit('submit', data)
    ElMessage.success('留言成功')
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.msg || '留言失败')
  }
}
</script>

<style scoped>
.comment-section {
  padding: 0;
}

.comment-section__title {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-heading);
  margin: 0 0 16px;
}

.comment-section__list {
  margin-top: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-radius: 10px;
  background: var(--color-background);
  border: 1px solid var(--color-border);
}

.comment-item__avatar {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
}

.comment-item__avatar-img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.comment-item__avatar-placeholder {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--color-heading);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 700;
}

.comment-item__body {
  flex: 1;
  min-width: 0;
}

.comment-item__head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
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
  margin-top: 24px;
  text-align: center;
  font-size: 13px;
  color: var(--color-text-mute);
}
</style>
