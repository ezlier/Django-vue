<template>
  <div class="bannedword-page">
    <h1 style="margin-bottom: 20px;">违禁词管理</h1>

    <!-- 添加违禁词输入框 -->
    <div class="add-section">
      <el-input
        v-model="newWord"
        placeholder="输入新的违禁词"
        style="width: 300px; margin-right: 10px;"
        clearable
      />
      <el-button type="primary" @click="addWord" :disabled="!newWord">添加</el-button>
    </div>

    <!-- 违禁词标签显示 -->
    <div class="word-list" style="margin-top: 20px;">
      <el-empty v-if="bannedword.length === 0" description="暂无违禁词" />
      <div v-else>
        <el-tag
          v-for="tag in bannedword"
          :key="tag.id || tag.word"
          type="danger"
          closable
          style="margin: 5px;"
          @close="removeWord(tag)"
        >
          {{ tag.word }}
        </el-tag>
      </div>
    </div>
  </div>
</template>

<script setup>
import { bannedwords, addBannedWord, deleteBannedWord } from '@/utils/Bannedwords'
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const bannedword = ref([])
const newWord = ref('')

// 获取违禁词列表
const fetchbannedword = async () => {
  try {
    const res = await bannedwords()
    bannedword.value = res.data.data
  } catch (error) {
    // 获取违禁词失败，静默处理
  }
}

// 添加违禁词
const addWord = async () => {
  try {
    const res = await addBannedWord({ word: newWord.value })
    if (res.status === 200) {
      ElMessage.success('添加成功')
      newWord.value = ''
      fetchbannedword()
    }
  } catch (err) {
    const msg =
            err.response?.data?.msg ||
            err.response?.data?.error ||
            "发送失败！"

    ElMessage.error(msg)
  }
}

// 删除违禁词
const removeWord = async (tag) => {
  try {
    await ElMessageBox.confirm(`确定要删除「${tag.word}」吗？`, '提示', {
      type: 'warning'
    })
    await deleteBannedWord(tag.id)
    ElMessage.success('删除成功')
    fetchbannedword()
  } catch (err){
    const msg =
            err.response?.data?.msg ||
            err.response?.data?.error ||
            "取消！"
    ElMessage.error(msg)
  }
}

onMounted(fetchbannedword)
</script>

<style scoped>
.bannedword-page {
  padding: 20px;
}
</style>
