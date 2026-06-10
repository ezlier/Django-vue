<template>
    <h1>📃留言管理</h1>
    <el-table :data="messageList" stripe border style="width: 100%">
        <el-table-column prop="id" label="ID"/>
        <el-table-column prop="name" label="Name"/>
        <el-table-column prop="ip" label="IP"/>
        <el-table-column prop="text" label="Text"/>
        <el-table-column prop="time" label="Time" />
        <el-table-column prop="QQ" label="QQ" />
        <el-table-column prop="email" label="E-mail" />
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
import { getadminMessage, deleteMessage } from '@/utils/message'
import { onMounted, ref } from 'vue'
import { ElMessage } from "element-plus";

const messageList = ref([])

const fetchMessage = async () => {
    const res = await getadminMessage()
    messageList.value = res.data.data
}

onMounted(fetchMessage)

const deleteRow = async (row) => {
  try {
    await deleteMessage(row.id)
    ElMessage.success(`已删除：${row.name}`)
    messageList.value = messageList.value.filter(item => item.id !== row.id)
  } catch (err) {
    ElMessage.error("删除失败：" + err)
  }
}
</script>

