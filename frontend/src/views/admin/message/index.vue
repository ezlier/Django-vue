<template>
  <div class="page admin-messages">
    <div class="page-header">
      <h1>留言管理</h1>
      <el-button type="danger" :disabled="selectedIds.length === 0" @click="handleBatchDelete">
        批量删除 ({{ selectedIds.length }})
      </el-button>
    </div>

    <el-table
      :data="messages"
      stripe
      v-loading="loading"
      empty-text="暂无留言"
      @selection-change="onSelectionChange"
    >
      <el-table-column type="selection" width="44" />
      <el-table-column prop="text" label="留言内容" min-width="240" show-overflow-tooltip />
      <el-table-column prop="name" label="昵称" width="120" />
      <el-table-column prop="ip" label="IP" width="140" />
      <el-table-column prop="time" label="时间" width="170" />
      <el-table-column prop="QQ" label="QQ" width="120" />
      <el-table-column prop="email" label="Email" width="180" show-overflow-tooltip />
      <el-table-column label="操作" width="100" fixed="right">
        <template #default="{ row }">
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getAdminMessages, deleteMessage, batchDeleteMessages } from '@/api/admin'
import { ElMessage, ElMessageBox } from 'element-plus'

interface MessageItem {
  id: number
  text: string
  name: string
  ip: string
  time: string
  QQ?: string
  email?: string
}

const messages = ref<MessageItem[]>([])
const loading = ref(false)
const selectedIds = ref<number[]>([])

function onSelectionChange(rows: MessageItem[]) {
  selectedIds.value = rows.map((r) => r.id)
}

async function fetchMessages() {
  loading.value = true
  try {
    const res = await getAdminMessages()
    const payload = res.data.data || res.data
    messages.value = payload.results || payload || []
  } catch {
    ElMessage.error('获取留言列表失败')
  } finally {
    loading.value = false
  }
}

async function handleDelete(id: number) {
  try {
    await ElMessageBox.confirm('确定删除该留言？', '提示', { type: 'warning' })
  } catch {
    return
  }
  try {
    await deleteMessage(id)
    ElMessage.success('删除成功')
    fetchMessages()
  } catch {
    ElMessage.error('删除失败')
  }
}

async function handleBatchDelete() {
  try {
    await ElMessageBox.confirm(`确定删除选中的 ${selectedIds.value.length} 条留言？`, '批量删除', { type: 'warning' })
  } catch {
    return
  }
  try {
    await batchDeleteMessages(selectedIds.value)
    ElMessage.success('批量删除成功')
    selectedIds.value = []
    fetchMessages()
  } catch {
    ElMessage.error('批量删除失败')
  }
}

onMounted(() => {
  fetchMessages()
})
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}

.page-header h1 {
  margin: 0;
}
</style>
