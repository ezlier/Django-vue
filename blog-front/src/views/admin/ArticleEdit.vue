<template>
  <div class="page admin-article-edit">
    <h1>{{ isEdit ? '编辑文章' : '新建文章' }}</h1>
    <p><!-- TODO: 文章编辑器（Markdown、tags、cover 上传） --></p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isEdit = computed(() => !!route.params.slug)
</script>
