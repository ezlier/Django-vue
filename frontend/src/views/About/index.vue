<script setup>
import { getAbout } from '@/utils/article'
import { onMounted, ref } from 'vue';

const article = ref(null)

onMounted(async () => {
    const res = await getAbout()
    article.value = res.data
})
</script>

<template>
    <div class="content">
        <div v-if="article">
            <div class="markdown-body" v-html="article.html"></div>
        </div>
    </div>
</template>

<style scoped>
.content {
    min-height: 100vh;
    padding: 20px;
    min-width: 0;
    border-radius: 8px;
    background-color: var(--bg-color);
    border-style: solid;
    border-color: var(--border);
    box-shadow: 2px 2px #000;
}
</style>