<template>
    <h1>违禁词标签</h1>
    <div>
        <el-tag v-for="tag in bannedword" :key="tag.word">
            {{ tag.word }}
        </el-tag>
    </div>
</template>
 
<script setup>
import {bannedwords} from '@/utils/Bannedwords'
import { onMounted, ref } from 'vue';

const bannedword = ref([])

const fetchbannedword = async () => {
    const res = await bannedwords()
    bannedword.value = res.data
}

onMounted(fetchbannedword)
</script>