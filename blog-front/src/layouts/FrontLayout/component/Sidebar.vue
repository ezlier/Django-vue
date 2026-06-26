<template>
  <aside class="sidebar">
    <ProfileCard />
    <TagCloudCard />
    <RandomPostsCard />
  </aside>
</template>

<script setup lang="ts">
import ProfileCard from '@/components/ProfileCard.vue'
import TagCloudCard from '@/components/TagCloudCard.vue'
import RandomPostsCard from '@/components/RandomPostsCard.vue'
</script>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
