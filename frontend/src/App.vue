<script setup>
import { ref, onMounted } from 'vue'
import api from '@/utils/request'

const message = ref('Loading...')

onMounted(async () => {
  const res = await api.get('/hello/')
  message.value = res.data.message
})
</script>

<template>
  <div class="home">
    <h1>{{ message }}</h1>
  </div>
</template>