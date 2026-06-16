<template>
  <nav class="pagination" v-if="totalPages > 1">
    <button
      class="pagination__btn"
      :disabled="current === 1"
      @click="go(current - 1)"
      aria-label="上一页"
    >
      ← 上一页
    </button>

    <div class="pagination__nums">
      <button
        v-for="page in visiblePages"
        :key="page"
        class="pagination__num"
        :class="{ 'pagination__num--active': page === current }"
        @click="go(page)"
      >
        {{ page }}
      </button>
    </div>

    <button
      class="pagination__btn"
      :disabled="current === totalPages"
      @click="go(current + 1)"
      aria-label="下一页"
    >
      下一页 →
    </button>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  current: number
  total: number
  pageSize?: number
}>()

const emit = defineEmits<{
  change: [page: number]
}>()

const totalPages = computed(() =>
  Math.max(1, Math.ceil(props.total / (props.pageSize || 10)))
)

const visiblePages = computed(() => {
  const pages: number[] = []
  const max = 5
  let start = Math.max(1, props.current - Math.floor(max / 2))
  let end = start + max - 1

  if (end > totalPages.value) {
    end = totalPages.value
    start = Math.max(1, end - max + 1)
  }

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

function go(page: number) {
  if (page >= 1 && page <= totalPages.value && page !== props.current) {
    emit('change', page)
  }
}
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 32px;
  flex-wrap: wrap;
}

.pagination__btn {
  padding: 8px 18px;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  background: var(--color-background);
  color: var(--color-text);
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
}

.pagination__btn:hover:not(:disabled) {
  background: var(--color-background-mute);
  border-color: var(--color-border-hover);
}

.pagination__btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.pagination__nums {
  display: flex;
  gap: 4px;
}

.pagination__num {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  background: var(--color-background);
  color: var(--color-text);
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s, border-color 0.2s, color 0.2s;
}

.pagination__num:hover {
  background: var(--color-background-mute);
  border-color: var(--color-border-hover);
}

.pagination__num--active {
  background: var(--color-heading);
  border-color: var(--color-heading);
  color: #fff;
  font-weight: 600;
}
</style>
