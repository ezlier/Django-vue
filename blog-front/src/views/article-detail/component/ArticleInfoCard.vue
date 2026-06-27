<template>
  <div class="article-info-card" v-if="article">
    <div class="article-info-card__title">文章统计</div>
    <!-- 封面 -->
    <div class="article-info-card__cover">
      <img v-if="article.cover" :src="article.cover" :alt="article.title" />
      <div v-else class="article-info-card__cover-placeholder">📝</div>
    </div>

    <!-- 标签 -->
    <div class="article-info-card__tags" v-if="article.tags?.length">
      <span v-for="tag in article.tags" :key="typeof tag === 'string' ? tag : tag.id" class="article-info-card__tag">
        {{ typeof tag === 'string' ? tag : tag.name }}
      </span>
    </div>

    <!-- 统计 -->
    <div class="article-info-card__stats">
      <div class="article-info-card__stat">
        <span class="stat-icon">字数</span>
        <span>{{ wordCount }} 字</span>
      </div>
      <div class="article-info-card__stat">
        <span class="stat-icon">最后更新</span>
        <span>{{ daysAgo }}</span>
      </div>
      <div class="article-info-card__stat">
        <span class="stat-icon">点赞</span>
        <span>{{ article.like_count }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Article } from '@/stores/article'

const props = defineProps<{
  article: Article | null
  content?: string
}>()

const wordCount = computed(() => {
  if (!props.content) return 0
  // 去掉 markdown 标记粗略统计中文字数
  const clean = props.content.replace(/[#*>`\[\]()\-\n\r]/g, '')
  return clean.length
})

const daysAgo = computed(() => {
  if (!props.article?.updated_time) return ''
  const updated = new Date(props.article.updated_time)
  const now = new Date()
  const diff = Math.floor((now.getTime() - updated.getTime()) / (1000 * 60 * 60 * 24))
  if (diff === 0) return '今天更新'
  if (diff === 1) return '昨天更新'
  return `${diff} 天前更新`
})
</script>

<style scoped>
.article-info-card {
  border-radius: 12px;
  border: 1px solid var(--color-border);
  background: var(--color-background);
  overflow: hidden;
}

.article-info-card__title {
  padding: 16px 20px;
  margin-bottom: 12px;
  font-weight: 700;
  font-size: 1.1rem;
  margin-bottom: .6rem;
  border-bottom: 2px dashed;
  padding-bottom: .3rem;
}

.article-info-card__cover {
  padding: 16px 20px;
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;

}

.article-info-card__cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 0.5rem;
  border: 1px solid var(--color-border);
}

.article-info-card__cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  opacity: 0.5;
}

.article-info-card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  padding: 16px 20px 0;
}

.article-info-card__tag {
  padding: 3px 12px;
  font-size: 12px;
  border-radius: 100px;
  background: var(--color-background-mute);
  color: var(--color-text-mute);
}

.article-info-card__stats {
  padding: 16px 20px 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.article-info-card__stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--color-text);
}

.stat-icon {
  font-size: 14px;
}
</style>
