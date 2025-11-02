<template>
    <div>
        <h1>🔗访客IP</h1>
    </div>
    <el-table :data="IP" stripe border style="width: 100%">
        <el-table-column type="index" width="50" />
        <el-table-column prop="ip" label="IP" width="180" />
        <el-table-column prop="visit_time" label="Time"/>
    </el-table>
</template>

<script setup>
import { get_ip } from "@/utils/get_ip"
import { onMounted, ref } from "vue";

const IP = ref([])

onMounted(async () => {
    const res = await get_ip()
    IP.value = res.data
})
</script>