<template>
    <h1>📃评论管理</h1>
    <el-table :data="messageList" stripe border style="width: 100%">
        <el-table-column prop="id" label="ID"/>
        <el-table-column prop="name" label="Name"/>
        <el-table-column prop="ip" label="IP"/>
        <el-table-column prop="text" label="Text"/>
        <el-table-column prop="time" label="Time" />
        <el-table-column prop="QQ" label="QQ" />
        <el-table-column prop="email" label="E-mail" />
        <el-table-column prop="article" label="article" />
        <el-table-column fixed="right" label="Operations" width="120">
            <template #default="scope">
                <el-button link type="danger" size="small" @click.prevent="deleteRow(scope.row)">
                    删除
                </el-button>
            </template>
        </el-table-column>
    </el-table>
</template>

<script setup>
import { getadminComment, deleteComment } from '@/utils/getcomment.js'
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from "element-plus";

const messageList = ref([])

const fetchMessage = async () => {
    const res = await getadminComment()
    messageList.value = res.data.data
}

onMounted(fetchMessage)


const deleteRow = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定删除评论：${row.text} 吗？`,
      "提示",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }
    )

    await deleteComment(row.id)
    ElMessage.success(`已删除：${row.name}`)
    messageList.value = messageList.value.filter(item => item.id !== row.id)

  } catch (err) {
    if (err !== "cancel") {
      ElMessage.error("删除失败")
    }
  }
}
</script>

