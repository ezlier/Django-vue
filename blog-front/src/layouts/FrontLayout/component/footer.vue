<template>
    <footer class="front-footer">
        <p>{{ ui.webSetting?.footer_text1 || '' }}</p>
        <p>{{ ui.webSetting?.footer_text2 || '' }}</p>
    </footer>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()

onMounted(() => {
    ui.fetchWebSetting()
})
</script>