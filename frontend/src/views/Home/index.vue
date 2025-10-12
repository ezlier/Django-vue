<script setup>
import Welcome from './components/welcome.vue';
</script>

<template>
    <div class="header">
        <Welcome/>
    </div>
    <div class="content">
        主页
    </div>
</template>

<style scoped>
    .content{
        height: 1800px;
        background-color: rgba(204, 204, 204, 0.9);
    }

    .header{
    height: 100vh;
    display: flex;
    justify-content: center; /* 水平居中 */
    align-items: center;
    }

</style>