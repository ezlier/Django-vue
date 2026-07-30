<template>
  <div class="page admin-dashboard">
    <h1>仪表盘</h1>

    <div class="dashboard-grid">
      <!-- 访客统计 -->
      <section class="dashboard-section">
        <h2>访客统计</h2>
        <el-table :data="visitors" stripe v-loading="visitorLoading" empty-text="暂无访客数据">
          <el-table-column prop="ip" label="IP 地址" />
          <el-table-column prop="user_agent" label="User Agent" show-overflow-tooltip />
          <el-table-column prop="visit_time" label="访问时间" />
        </el-table>
        <Pagination v-if="visitorTotal > 10" :current="visitorPage" :total="visitorTotal" :page-size="10"
          @change="onVisitorPageChange" />
      </section>

      <!-- 审计日志 -->
      <section class="dashboard-section">
        <h2>审计日志</h2>
        <el-table :data="logs" stripe v-loading="logLoading" empty-text="暂无日志数据">
          <el-table-column prop="user_username" label="操作用户" />
          <el-table-column prop="action_type_display" label="操作" />
          <el-table-column prop="action_result_display" label="结果" show-overflow-tooltip />
          <el-table-column prop="action_time_formatted" label="时间" />
        </el-table>
        <Pagination v-if="logTotal > 10" :current="logPage" :total="logTotal" :page-size="10"
          @change="onLogPageChange" />
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getVisitorStats, getAuditLogs } from '@/api/admin'
import { ElMessage } from 'element-plus'
import Pagination from '@/components/Pagination.vue'

interface Visitor {
  ip: string
  path: string
  referer: string
  user_agent: string
  created_time: string
}

interface LogEntry {
  user: string
  action: string
  resource: string
  ip: string
  created_time: string
}

const visitors = ref<Visitor[]>([])
const visitorLoading = ref(false)
const visitorPage = ref(1)
const visitorTotal = ref(0)

const logs = ref<LogEntry[]>([])
const logLoading = ref(false)
const logPage = ref(1)
const logTotal = ref(0)

async function fetchVisitors(page = 1) {
  visitorLoading.value = true
  try {
    const res = await getVisitorStats(page)
    const payload = res.data.data || res.data
    visitors.value = payload.results || []
    visitorTotal.value = payload.count || 0
  } catch {
    ElMessage.error('获取访客数据失败')
  } finally {
    visitorLoading.value = false
  }
}

async function fetchLogs(page = 1) {
  const pageSize = 10
  logLoading.value = true
  try {
    const res = await getAuditLogs({ limit: pageSize, offset: (page - 1) * pageSize })
    const payload = res.data.data || res.data
    logs.value = payload.logs || []
    logTotal.value = payload.total || 0
  } catch {
    ElMessage.error('获取审计日志失败')
  } finally {
    logLoading.value = false
  }
}

function onVisitorPageChange(page: number) {
  visitorPage.value = page
  fetchVisitors(page)
}

function onLogPageChange(page: number) {
  logPage.value = page
  fetchLogs(page)
}

onMounted(() => {
  fetchVisitors()
  fetchLogs()
})
</script>

<style scoped>
.dashboard-grid {
  display: flex;
  flex-direction: column;
  gap: 32px;
  margin-top: 20px;
}

.dashboard-section h2 {
  font-size: 17px;
  margin-bottom: 14px;
  color: var(--color-heading, #1a1a1a);
}
</style>
