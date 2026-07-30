<template>
  <div class="page admin-tags">
    <div class="page-header">
      <h1>标签管理</h1>
      <div class="page-header__actions">
        <el-input v-model="newTagName" placeholder="输入新标签名" size="default" style="width: 200px"
          @keyup.enter="handleAddTag" />
        <el-button type="primary" @click="handleAddTag">新建标签</el-button>
        <el-button type="danger" :disabled="selectedIds.length === 0" @click="handleBatchDelete">
          批量删除 ({{ selectedIds.length }})
        </el-button>
      </div>
    </div>

    <el-table :data="tags" stripe v-loading="loading" empty-text="暂无标签" @selection-change="onSelectionChange">
      <el-table-column type="selection" width="44" />
      <el-table-column prop="name" label="标签名称" min-width="200">
        <template #default="{ row }">
          <template v-if="editingId === row.id">
            <el-input v-model="editingName" size="small" style="width: 160px" @keyup.enter="handleRenameConfirm(row.id)"
              @keyup.escape="cancelEditing" />
            <el-button size="small" type="primary" style="margin-left: 8px"
              @click="handleRenameConfirm(row.id)">确认</el-button>
            <el-button size="small" @click="cancelEditing">取消</el-button>
          </template>
          <template v-else>
            <el-tag size="default">{{ row.name }}</el-tag>
          </template>
        </template>
      </el-table-column>
      <el-table-column prop="article_count" label="文章数量" width="120" align="center" />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button v-if="editingId !== row.id" size="small" @click="startEditing(row)">修改</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getAdminTags, createTag, updateTag, deleteTag } from '@/api/admin'
import { ElMessage, ElMessageBox } from 'element-plus'

interface TagItem {
  id: number
  name: string
  article_count?: number
}

const tags = ref<TagItem[]>([])
const loading = ref(false)
const newTagName = ref('')
const selectedIds = ref<number[]>([])
const editingId = ref<number | null>(null)
const editingName = ref('')

function onSelectionChange(rows: TagItem[]) {
  selectedIds.value = rows.map((r) => r.id)
}

async function fetchTags() {
  loading.value = true
  try {
    const res = await getAdminTags()
    tags.value = res.data.results || []
  } catch {
    ElMessage.error('获取标签列表失败')
  } finally {
    loading.value = false
  }
}

async function handleAddTag() {
  if (!newTagName.value.trim()) {
    ElMessage.warning('请输入标签名称')
    return
  }
  try {
    await createTag(newTagName.value.trim())
    ElMessage.success('标签创建成功')
    newTagName.value = ''
    fetchTags()
  } catch {
    ElMessage.error('创建标签失败')
  }
}

function startEditing(row: TagItem) {
  editingId.value = row.id
  editingName.value = row.name
}

function cancelEditing() {
  editingId.value = null
  editingName.value = ''
}

async function handleRenameConfirm(id: number) {
  if (!editingName.value.trim()) {
    ElMessage.warning('标签名不能为空')
    return
  }
  try {
    await updateTag(id, editingName.value.trim())
    ElMessage.success('标签已更新')
    cancelEditing()
    fetchTags()
  } catch {
    ElMessage.error('更新失败')
  }
}

async function handleDelete(id: number) {
  try {
    await ElMessageBox.confirm('确定删除该标签？', '提示', { type: 'warning' })
  } catch {
    return
  }
  try {
    await deleteTag(id)
    ElMessage.success('已删除')
    fetchTags()
  } catch {
    ElMessage.error('删除失败')
  }
}

async function handleBatchDelete() {
  try {
    await ElMessageBox.confirm(`确定删除选中的 ${selectedIds.value.length} 个标签？`, '批量删除', { type: 'warning' })
  } catch {
    return
  }
  try {
    await Promise.all(selectedIds.value.map((id) => deleteTag(id)))
    ElMessage.success('批量删除成功')
    selectedIds.value = []
    fetchTags()
  } catch {
    ElMessage.error('批量删除失败')
  }
}

onMounted(() => {
  fetchTags()
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
