<template>
  <div class="page admin-prohibited-words">
    <div class="page-header">
      <h1>违禁词管理</h1>
      <div class="page-header__actions">
        <el-input
          v-model="newWord"
          placeholder="输入违禁词"
          size="default"
          style="width: 200px"
          @keyup.enter="handleAddWord"
        />
        <el-button type="primary" @click="handleAddWord">添加违禁词</el-button>
        <el-button type="danger" :disabled="selectedIds.length === 0" @click="handleBatchDelete">
          批量删除 ({{ selectedIds.length }})
        </el-button>
      </div>
    </div>

    <el-table
      :data="words"
      stripe
      v-loading="loading"
      empty-text="暂无违禁词"
      @selection-change="onSelectionChange"
    >
      <el-table-column type="selection" width="44" />
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="word" label="违禁词" min-width="300" />
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getBannedWords, createBannedWord, deleteBannedWord, batchDeleteBannedWords } from '@/api/admin'
import { ElMessage, ElMessageBox } from 'element-plus'

interface BannedWordItem {
  id: number
  word: string
}

const words = ref<BannedWordItem[]>([])
const loading = ref(false)
const newWord = ref('')
const selectedIds = ref<number[]>([])

function onSelectionChange(rows: BannedWordItem[]) {
  selectedIds.value = rows.map((r) => r.id)
}

async function fetchWords() {
  loading.value = true
  try {
    const res = await getBannedWords()
    const payload = res.data.data || res.data
    words.value = payload.results || payload || []
  } catch {
    ElMessage.error('获取违禁词列表失败')
  } finally {
    loading.value = false
  }
}

async function handleAddWord() {
  if (!newWord.value.trim()) {
    ElMessage.warning('请输入违禁词')
    return
  }
  try {
    await createBannedWord(newWord.value.trim())
    ElMessage.success('添加成功')
    newWord.value = ''
    fetchWords()
  } catch {
    ElMessage.error('添加失败')
  }
}

async function handleDelete(id: number) {
  try {
    await ElMessageBox.confirm('确定删除该违禁词？', '提示', { type: 'warning' })
  } catch {
    return
  }
  try {
    await deleteBannedWord(id)
    ElMessage.success('已删除')
    fetchWords()
  } catch {
    ElMessage.error('删除失败')
  }
}

async function handleBatchDelete() {
  try {
    await ElMessageBox.confirm(`确定删除选中的 ${selectedIds.value.length} 个违禁词？`, '批量删除', { type: 'warning' })
  } catch {
    return
  }
  try {
    await batchDeleteBannedWords(selectedIds.value)
    ElMessage.success('批量删除成功')
    selectedIds.value = []
    fetchWords()
  } catch {
    ElMessage.error('批量删除失败')
  }
}

onMounted(() => {
  fetchWords()
})
</script>

<style scoped>
.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0 0 14px;
}

.page-header__actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
</style>
