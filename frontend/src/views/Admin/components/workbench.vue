<template>
  <div class="container">
    <div>
        <div class="top">
      <div class="user-card">
        <div class="avatar"></div>

        <div class="info">
          <div class="name">{{ username }}</div>
          <div class="text">工作台</div>
        </div>

        <div class="actions">
          <el-button plain @click="changename">改名</el-button>
          <el-button plain @click="changePassword">改密码</el-button>
        </div>
      </div>

      
        </div>
        <div class="block">
        <el-table :data="IP" stripe style="width: 100%">
            <el-table-column type="index" />
            <el-table-column prop="ip" label="IP"/>
            <el-table-column show-overflow-tooltip prop="user_agent" label="设备"/>
            <el-table-column prop="path" label="路径"/>
            <el-table-column prop="visit_time" sortable label="访问时间"/>
        </el-table>

        <el-pagination
            style="margin-top: 10px"
            background
            layout="prev, pager, next"
            :total="total"
            :page-size="10"
            @current-change="(page) => {
            currentPage = page
            loadData()
            }"
        />
        </div>
        <div class="block">
        <el-form :inline="true" :model="auditFilters" class="audit-filter-form">
            <el-form-item label="操作类型">
            <el-select v-model="auditFilters.action_type" placeholder="全部" clearable style="width: 150px">
                <el-option label="登录" value="login" />
                <el-option label="登出" value="logout" />
                <el-option label="创建文章" value="article_create" />
                <el-option label="更新文章" value="article_update" />
                <el-option label="删除文章" value="article_delete" />
                <el-option label="创建标签" value="tag_create" />
                <el-option label="更新标签" value="tag_update" />
                <el-option label="删除标签" value="tag_delete" />
                <el-option label="删除评论" value="comment_delete" />
                <el-option label="删除留言" value="message_delete" />
                <el-option label="添加违禁词" value="bannedword_create" />
                <el-option label="删除违禁词" value="bannedword_delete" />
                <el-option label="更新网站设置" value="websetting_update" />
                <el-option label="查看访客统计" value="visitor_view" />
            </el-select>
            </el-form-item>

            <el-form-item label="操作结果">
            <el-select v-model="auditFilters.action_result" placeholder="全部" clearable style="width: 120px">
                <el-option label="成功" value="success" />
                <el-option label="失败" value="failure" />
            </el-select>
            </el-form-item>

            <el-form-item label="日期范围">
            <el-date-picker
                v-model="auditDateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                value-format="YYYY-MM-DD"
                style="width: 240px"
            />
            </el-form-item>

            <el-form-item>
            <el-button type="primary" @click="handleAuditSearch">查询</el-button>
            <el-button @click="handleAuditReset">重置</el-button>
            </el-form-item>
        </el-form>

        <!-- 表格 -->
        <el-table :data="auditLogs" stripe border style="width: 100%" v-loading="auditLoading">
            <el-table-column type="index" label="序号"/>
            <el-table-column prop="user_username" label="管理员"/>
            <el-table-column prop="action_type_display" label="操作类型"/>

            <el-table-column prop="action_result" label="结果" >
            <template #default="scope">
                <el-tag :type="scope.row.action_result === 'success' ? 'success' : 'danger'" size="small">
                {{ scope.row.action_result === 'success' ? '成功' : '失败' }}
                </el-tag>
            </template>
            </el-table-column>

            <el-table-column prop="target_model" label="目标模型"/>
            <el-table-column prop="action_time_formatted" label="操作时间"/>
        </el-table>

        <div class="audit-pagination">
            <el-pagination
            background
            layout="prev, pager, next"
            :total="auditTotal"
            :page-size="10"
            :current-page="auditCurrentPage"
            @current-change="(page) => {
                auditCurrentPage = page
                loadAuditLogs()
            }"
            />
        </div>
        </div>
    </div>
    <div class="right-empty">

    </div>

  </div>

</template>

<script setup>
import { get_ip } from "@/utils/get_ip"
import { getAuditLogs } from "@/utils/logs"
import { updateUsername, updatePassword } from "@/utils/updateUser"
import { h, onMounted, ref, reactive } from "vue";
import { ElMessage, ElMessageBox } from 'element-plus'

const IP = ref([])
const total = ref(0)
const currentPage = ref(1)

const username = ref(localStorage.getItem("username"));

const loadData = async () => {
    const res = await get_ip(currentPage.value)
    IP.value = res.data.data.results
    total.value = res.data.data.count
}

onMounted(loadData)

const auditLogs = ref([])
const auditLoading = ref(false)
const auditTotal = ref(0)
const auditCurrentPage = ref(1)
const auditPageSize = ref(10)
const auditDateRange = ref(null)

const auditFilters = reactive({
    action_type: '',
    action_result: '',
    start_date: '',
    end_date: ''
})

const loadAuditLogs = async () => {
    auditLoading.value = true
    try {
        const offset = (auditCurrentPage.value - 1) * auditPageSize.value
        const res = await getAuditLogs({
            limit: auditPageSize.value,
            offset: offset,
            action_type: auditFilters.action_type || undefined,
            action_result: auditFilters.action_result || undefined,
            start_date: auditFilters.start_date || undefined,
            end_date: auditFilters.end_date || undefined
        })
        
        auditLogs.value = res.data.data.logs
        auditTotal.value = res.data.data.total
    } catch (error) {
        console.error('加载操作记录失败:', error)
        ElMessage.error('加载操作记录失败')
    } finally {
        auditLoading.value = false
    }
}

const handleAuditSearch = () => {
    auditCurrentPage.value = 1
    loadAuditLogs()
}

const handleAuditReset = () => {
    auditFilters.action_type = ''
    auditFilters.action_result = ''
    auditFilters.start_date = ''
    auditFilters.end_date = ''
    auditDateRange.value = null
    auditCurrentPage.value = 1
    loadAuditLogs()
}

onMounted(() => {
    loadAuditLogs()
})

const changename = () => {
    ElMessageBox.prompt('输入新名字', '修改用户名', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPlaceholder: '请输入新用户名',
        inputValidator: (value) => {
            if (!value || value.trim() === '') {
                return '用户名不能为空'
            }
            return true
        }
    })
    .then(({ value }) => {
        updateUsername(value)
            .then(() => {
                username.value = value
                localStorage.setItem('username', value)
                ElMessage.success('用户名修改成功')
            })
            .catch((error) => {
                ElMessage.error(error.response?.data?.message || '用户名修改失败')
            })
    })
    .catch(() => {
        ElMessage.info('已取消修改')
    })
}

const changePassword = () => {
    ElMessageBox.confirm('请输入原密码和新密码', '修改密码', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        distinguishCancelAndClose: true,
        message: h('div', { class: 'password-dialog' }, [
            h('p', { style: 'margin-bottom: 10px;' }, '请输入密码:'),
            h('input', {
                ref: 'oldPasswordInput',
                type: 'password',
                placeholder: '原密码',
                class: 'el-input__inner',
                style: 'width: 100%; margin-bottom: 10px; padding: 8px; border: 1px solid #dcdfe6; border-radius: 4px;',
                onKeyup: (e) => { if (e.key === 'Enter') handlePasswordSubmit() }
            }),
            h('input', {
                ref: 'newPasswordInput',
                type: 'password',
                placeholder: '新密码',
                class: 'el-input__inner',
                style: 'width: 100%; padding: 8px; border: 1px solid #dcdfe6; border-radius: 4px;',
                onKeyup: (e) => { if (e.key === 'Enter') handlePasswordSubmit() }
            })
        ]),
        beforeClose: (action, instance, done) => {
            if (action === 'confirm') {
                const oldPassword = instance.message.el.querySelector('input[placeholder="原密码"]').value
                const newPassword = instance.message.el.querySelector('input[placeholder="新密码"]').value

                if (!oldPassword || !newPassword) {
                    ElMessage.warning('请输入原密码和新密码')
                    return false
                }

                if (oldPassword === newPassword) {
                    ElMessage.warning('新密码不能与原密码相同')
                    return false
                }

                updatePassword(oldPassword, newPassword)
                    .then(() => {
                        ElMessage.success('密码修改成功，请重新登录')
                        localStorage.clear()
                        window.location.href = '/login'
                    })
                    .catch((error) => {
                        ElMessage.error(error.response?.data?.message || '密码修改失败')
                        return false
                    })
                done()
            } else {
                done()
            }
        }
    })
}
</script>

<style scoped>
.container {
  display: flex;
}

/* 顶部布局 */
.top {
  display: flex;
  gap: 20px;
}

/* 左侧用户卡片 */
.user-card {
  flex: 2;
  display: flex;
  align-items: center;
  border: 1px solid #ccc;
  padding: 10px;
}

/* 右侧留白 */
.right-empty {
  flex: 1;
  border: 1px solid #ccc;
}

/* 头像 */
.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 1px solid #333;
  margin-right: 10px;
}

/* 信息 */
.info {
  flex: 1;
}

.name {
  font-weight: bold;
}

.text {
  font-size: 12px;
  color: #666;
}

/* 按钮 */
.actions {
  display: flex;
  gap: 5px;
}

/* 通用块 */
.block {
  border: 1px solid #ccc;
  padding: 10px;
}

.block-title {
  text-align: center;
  border-bottom: 1px solid #ccc;
  margin-bottom: 10px;
  padding-bottom: 5px;
}

/* 分页 */
.audit-pagination {
  margin-top: 10px;
  display: flex;
  justify-content: center;
}
</style>