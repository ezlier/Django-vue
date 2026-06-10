<template>
    <h1>📕文章管理</h1>
    <div style="margin-bottom: 16px; display:flex; gap:10px;">
      <el-input
        v-model="keyword"
        placeholder="搜索标题"
        clearable
        style="width: 200px"
      />

      <el-select
        v-model="isDraftFilter"
        placeholder="文章状态"
        clearable
        style="width: 120px"
      >
        <el-option label="已发布" :value="false" />
        <el-option label="草稿" :value="true" />
      </el-select>

      <el-button type="primary" @click="fetchArticles">
        搜索
      </el-button>
    </div>
    <el-table :data="articles" style="width: 100%" max-height="600">
        <el-table-column type="index" width="50" />
        <el-table-column prop="created_time" sortable label="Date"/>
        <el-table-column prop="title" label="Name" />
        <el-table-column label="状态" width="80">
          <template #default="scope">
            <el-tag :type="scope.row.is_draft ? 'info' : 'success'" size="small">
              {{ scope.row.is_draft ? '草稿' : '已发布' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Tag">
          <template #default="scope">
            <el-tag
            v-for="tag in scope.row.tags"
            :key="tag"
            type="info"
            style="cursor:pointer;"
          >
            {{ tag }}
          </el-tag>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="Operations" min-width="180">
            <template #default="scope">
                <el-button link type="success" size="small" @click.prevent="togglePublish(scope.row)" v-if="scope.row.is_draft">
                    发布
                </el-button>
                <el-button link type="warning" size="small" @click.prevent="togglePublish(scope.row)" v-else>
                    下架
                </el-button>
                <el-button link type="warning" size="small" @click.prevent="$router.push(`/admin/Rewrite/${scope.row.slug}`)">
                    修改
                </el-button>
                <el-button link type="danger" size="small" @click.prevent="deleteRow(scope.row)">
                    删除
                </el-button>
            </template>
        </el-table-column>
    </el-table>
    <div class="pagination-wrapper">
      <el-pagination
        background
        layout="total, prev, pager, next"
        :total="total"
        :page-size="pageSize"
        :current-page="currentPage"
        @current-change="handlePageChange"
      />
    </div>
    <el-button type="primary" @click="$router.push('/admin/UploadArticle')">上传文章</el-button>
    <el-button type="primary" @click="$router.push('/admin/CreateArticle')">写文章</el-button>
</template>

<script setup>
import { getAdminArticles, deleteArticle2, updateArticleStatus } from "@/utils/article";
import { onMounted, ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";

const articles = ref([]);
const keyword = ref("")
const isDraftFilter = ref(null)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

const fetchArticles = async () => {
  const params = {
    page: currentPage.value,
    page_size: pageSize.value,
    search: keyword.value
  }
  if (isDraftFilter.value !== null) {
    params.is_draft = isDraftFilter.value
  }
  const res = await getAdminArticles(params);
  articles.value = res.data.data.results || res.data.data
  total.value = res.data.data.count || 0
};

const handlePageChange = (page) => {
  currentPage.value = page
  fetchArticles()
}

const togglePublish = async (row) => {
  const newStatus = !row.is_draft
  const action = newStatus ? '下架' : '发布'
  try {
    await ElMessageBox.confirm(`确定要${action}这篇文章吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await updateArticleStatus(row.slug, newStatus)
    ElMessage.success(`${action}成功`)
    fetchArticles()
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error(`${action}失败`)
    }
  }
}

onMounted(() => {
  fetchArticles()
})

const deleteRow = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除《${row.title}》吗？`, '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteArticle2(row.slug || row.id)
    ElMessage.success(`已删除：${row.title}`)
    fetchArticles()
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error("删除失败")
    }
  }
}
</script>

<style scoped>
.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}
</style>
