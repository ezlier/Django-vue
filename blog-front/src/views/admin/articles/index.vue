<template>
  <div class="page admin-article-list">
    <div class="page-header">
      <h1>文章管理</h1>
      <div class="page-header__actions">
        <el-button type="danger" :disabled="selectedIds.length === 0" @click="handleBatchDelete">
          批量删除 ({{ selectedIds.length }})
        </el-button>
      </div>
    </div>

    <el-table :data="articles" stripe v-loading="loading" empty-text="暂无文章" @selection-change="onSelectionChange">
      <el-table-column type="selection" width="44" />
      <el-table-column label="封面" width="80">
        <template #default="{ row }">
          <img v-if="row.cover" :src="row.cover" class="article-cover-thumb" alt="cover" />
          <span v-else class="no-cover">—</span>
        </template>
      </el-table-column>
      <el-table-column prop="title" label="标题" show-overflow-tooltip />
      <el-table-column label="标签" width="160">
        <template #default="{ row }">
          <el-tag v-for="(tag, idx) in row.tags" :key="idx" size="small" class="article-tag">{{ tag }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_draft ? 'info' : 'success'" size="small">
            {{ row.is_draft ? '草稿' : '已发布' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_time" label="创建时间" />
      <el-table-column label="操作" width="260" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="handleEdit(row.slug)">编辑</el-button>
          <el-button size="small" :type="row.is_draft ? 'success' : 'warning'" @click="handleToggleStatus(row)">
            {{ row.is_draft ? '发布' : '转草稿' }}
          </el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.slug)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <Pagination v-if="total > pageSize" :current="page" :total="total" :page-size="pageSize" @change="onPageChange" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  getAdminArticles,
  updateArticleStatus,
  deleteArticle,
  batchDeleteArticles,
} from '@/api/admin'
import { ElMessage, ElMessageBox } from 'element-plus'
import Pagination from '@/components/Pagination.vue'

interface ArticleItem {
  id: number
  title: string
  slug: string
  cover: string | null
  tags: { id: number; name: string }[]
  is_draft: boolean
  created_time: string
}

const router = useRouter()
const articles = ref<ArticleItem[]>([])
const loading = ref(false)
const page = ref(1)
const pageSize = 10
const total = ref(0)
const selectedIds = ref<number[]>([])

function onSelectionChange(rows: ArticleItem[]) {
  selectedIds.value = rows.map((r) => r.id)
}

async function fetchArticles() {
  loading.value = true
  try {
    const res = await getAdminArticles({ page: page.value, page_size: pageSize })
    const payload = res.data.data || res.data
    articles.value = payload.results || []
    total.value = payload.count || 0
  } catch {
    ElMessage.error('获取文章列表失败')
  } finally {
    loading.value = false
  }
}

function handleEdit(slug: string) {
  router.push(`/admin/article/edit/${slug}`)
}

async function handleToggleStatus(row: ArticleItem) {
  try {
    await updateArticleStatus(row.slug, !row.is_draft)
    ElMessage.success(row.is_draft ? '已发布' : '已转为草稿')
    row.is_draft = !row.is_draft
  } catch {
    ElMessage.error('状态更新失败')
  }
}

async function handleDelete(slug: string) {
  try {
    await ElMessageBox.confirm('确定删除该文章？', '提示', { type: 'warning' })
  } catch {
    return
  }
  try {
    await deleteArticle(slug)
    ElMessage.success('删除成功')
    fetchArticles()
  } catch {
    ElMessage.error('删除失败')
  }
}

async function handleBatchDelete() {
  try {
    await ElMessageBox.confirm(`确定删除选中的 ${selectedIds.value.length} 篇文章？`, '批量删除', { type: 'warning' })
  } catch {
    return
  }
  try {
    await batchDeleteArticles(selectedIds.value)
    ElMessage.success('批量删除成功')
    selectedIds.value = []
    fetchArticles()
  } catch {
    ElMessage.error('批量删除失败')
  }
}

function onPageChange(p: number) {
  page.value = p
  fetchArticles()
}

onMounted(() => {
  fetchArticles()
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

.article-cover-thumb {
  width: 48px;
  height: 36px;
  object-fit: cover;
  border-radius: 4px;
}

.no-cover {
  color: #999;
  font-size: 13px;
}

.article-tag {
  margin-right: 4px;
  margin-bottom: 2px;
}
</style>
