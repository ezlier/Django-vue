<template>
  <form class="comment-form" @submit.prevent="handleSubmit">
    <div class="comment-form__row">
      <input
        v-model="form.name"
        class="comment-form__input"
        type="text"
        placeholder="你的名字 *"
        required
        maxlength="10"
      />
      <input
        v-model="form.QQ"
        class="comment-form__input"
        type="text"
        placeholder="QQ（可选）"
        maxlength="15"
      />
      <input
        v-model="form.email"
        class="comment-form__input"
        type="email"
        placeholder="Email（可选）"
        maxlength="50"
      />
    </div>
    <textarea
      v-model="form.text"
      class="comment-form__textarea"
      rows="4"
      placeholder="说点什么吧..."
      required
      maxlength="400"
    ></textarea>
    <div class="comment-form__footer">
      <span class="comment-form__count">{{ form.text.length }}/400</span>
      <button type="submit" class="comment-form__btn" :disabled="submitting">
        {{ submitting ? '发送中...' : '发表留言' }}
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'

const emit = defineEmits<{
  submit: [data: { name: string; text: string; QQ?: string; email?: string }]
}>()

const form = reactive({
  name: '',
  text: '',
  QQ: '',
  email: '',
})
const submitting = ref(false)

function reset() {
  form.text = ''
}

async function handleSubmit() {
  if (!form.name.trim() || !form.text.trim()) {
    ElMessage.warning('请填写名字和内容')
    return
  }
  submitting.value = true
  try {
    emit('submit', {
      name: form.name.trim(),
      text: form.text.trim(),
      QQ: form.QQ.trim() || undefined,
      email: form.email.trim() || undefined,
    })
    reset()
  } finally {
    submitting.value = false
  }
}

defineExpose({ reset })
</script>

<style scoped>
.comment-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comment-form__row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.comment-form__input {
  flex: 1;
  min-width: 120px;
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  background: var(--color-background);
  color: var(--color-text);
  font-size: 14px;
  font-family: inherit;
  outline: none;
  transition: border-color 0.2s;
}

.comment-form__input:focus {
  border-color: var(--color-heading);
}

.comment-form__textarea {
  padding: 12px 14px;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  background: var(--color-background);
  color: var(--color-text);
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  outline: none;
  transition: border-color 0.2s;
}

.comment-form__textarea:focus {
  border-color: var(--color-heading);
}

.comment-form__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment-form__count {
  font-size: 12px;
  color: var(--color-text-mute);
}

.comment-form__btn {
  padding: 8px 24px;
  border-radius: 8px;
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
</style>
