<template>
  <div class="tag-filter">
    <div class="tag-filter__scroll">
      <button
        class="tag-filter__btn"
        :class="{ 'tag-filter__btn--active': activeTag === null }"
        @click="$emit('change', null)"
      >
        All
      </button>
      <button
        v-for="tag in tags"
        :key="tag.id"
        class="tag-filter__btn"
        :class="{ 'tag-filter__btn--active': activeTag === tag.id }"
        @click="$emit('change', tag.id)"
      >
        {{ tag.name }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Tag } from '@/stores/article'

defineProps<{
  tags: Tag[]
  activeTag: number | null
}>()

defineEmits<{
  change: [tagId: number | null]
}>()
</script>

<style scoped>
.tag-filter {
  margin-bottom: 24px;
}

.tag-filter__scroll {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  white-space: nowrap;
  padding: 8px 0;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}

.tag-filter__scroll::-webkit-scrollbar {
  display: none;
}

.tag-filter__btn {
  padding: 6px 16px;
  border-radius: 10px;
  border: 1px solid var(--color-border);
  background: var(--color-background);
  color: var(--color-text);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
  font-family: inherit;
}

.tag-filter__btn:hover {
  background: var(--color-background-mute);
  border-color: var(--color-border-hover);
}

.tag-filter__btn--active {
  background: var(--color-heading);
  border-color: var(--color-heading);
  color: #fff;
  font-weight: 600;
}
</style>
