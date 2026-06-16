<template>
  <article class="card" @click="goDetail">
    <div class="card__cover">
      <img
        v-if="article.cover"
        :src="article.cover"
        :alt="article.title"
        loading="lazy"
      />
      <div v-else class="card__cover-placeholder">
        <span class="placeholder-icon">📝</span>
      </div>
    </div>

    <div class="card__body">
      <h3 class="card__title">{{ article.title }}</h3>

      <div class="card__meta">
        <div class="card__tags" v-if="article.tags?.length">
          <span
            v-for="tag in article.tags"
            :key="tag.id || tag.name"
            class="card__tag"
          >
            {{ typeof tag === 'string' ? tag : tag.name }}
          </span>
        </div>
        <span class="card__date">{{ article.created_time }}</span>
      </div>

      <div class="card__action">
        <span class="card__read-btn">
          阅读全文
          <span class="arrow">→</span>
        </span>
      </div>
    </div>
  </article>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Article } from '@/stores/article'

const props = defineProps<{
  article: Article
}>()

const router = useRouter()

function goDetail() {
  router.push(`/article/${props.article.slug}`)
}
</script>

<style scoped>
.card {
  border-radius: 12px;
  background: var(--color-background);
  border: 1px solid var(--color-border);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  animation: cardIn 0.5s ease-out both;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: var(--box-shadow-hover);
}

@keyframes cardIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card__cover {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  background: var(--color-background-mute);
}

.card__cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.card:hover .card__cover img {
  transform: scale(1.04);
}

.card__cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-background-mute), var(--color-background-soft));
}

.placeholder-icon {
  font-size: 40px;
  opacity: 0.5;
}

.card__body {
  padding: 16px 20px 20px;
}

.card__title {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-heading);
  margin: 0 0 12px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card__meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.card__tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.card__tag {
  padding: 2px 10px;
  font-size: 12px;
  border-radius: 100px;
  background: var(--color-background-mute);
  color: var(--color-text-mute);
  white-space: nowrap;
}

.card__date {
  font-size: 13px;
  color: var(--color-text-mute);
  white-space: nowrap;
}

.card__action {
  display: flex;
  justify-content: flex-end;
}

.card__read-btn {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-heading);
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: gap 0.25s ease;
}

.card:hover .card__read-btn {
  gap: 8px;
}

.arrow {
  display: inline-block;
  transition: transform 0.25s ease;
}

.card:hover .arrow {
  transform: translateX(2px);
}
</style>
