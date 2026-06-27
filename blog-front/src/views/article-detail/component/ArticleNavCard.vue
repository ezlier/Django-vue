<template>
  <nav class="article-nav-card" v-if="headings.length">
    <h3 class="article-nav-card__title">目录</h3>
    <ul class="article-nav-card__list">
      <li v-for="(h, i) in headings" :key="i" :class="[
        'article-nav-card__item',
        `article-nav-card__item--${h.level}`,
        { 'article-nav-card__item--active': activeId === h.id }
      ]">
        <a :href="`#${h.id}`" @click.prevent="scrollTo(h.id)" :title="h.text">
          {{ h.text }}
        </a>
      </li>
    </ul>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

interface Heading {
  id: string
  text: string
  level: number
}

const headings = ref<Heading[]>([])
const activeId = ref('')

function collectHeadings() {
  setTimeout(() => {
    const container = document.querySelector('.article-body')
    if (!container) return
    const els = container.querySelectorAll('h1, h2, h3')
    headings.value = Array.from(els).map((el) => {
      const h = el as HTMLElement
      if (!h.id) {
        h.id = 'heading-' + Math.random().toString(36).slice(2, 8)
      }
      const rawText = h.innerText || h.textContent || ''
      return {
        id: h.id,
        text: rawText.slice(0, 30) + (rawText.length > 30 ? '...' : ''),
        level: Number(h.tagName[1]),
      }
    })
  }, 600)
}

function scrollTo(id: string) {
  const el = document.getElementById(id)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    activeId.value = id
  }
}

function onScroll() {
  if (!headings.value.length) return
  const els = headings.value.map((h) => document.getElementById(h.id)).filter(Boolean) as HTMLElement[]
  if (!els.length) return
  for (let i = els.length - 1; i >= 0; i--) {
    if (els[i].getBoundingClientRect().top <= 120) {
      activeId.value = headings.value[i].id
      return
    }
  }
  activeId.value = headings.value[0].id
}

onMounted(() => {
  collectHeadings()
  window.addEventListener('scroll', onScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
})
</script>

<style scoped>
.article-nav-card {
  padding: 20px;
  border-radius: 12px;
  border: 1px solid var(--color-border);
  background: var(--color-background);
}

.article-nav-card__title {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-heading);
  margin: 0 0 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--color-border);
}

.article-nav-card__list {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 40vh;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--color-border) transparent;
}

.article-nav-card__list::-webkit-scrollbar {
  width: 4px;
}

.article-nav-card__list::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: 2px;
}

.article-nav-card__list::-webkit-scrollbar-track {
  background: transparent;
}

.article-nav-card__item {
  border-left: 2px solid transparent;
  transition: border-color 0.2s;
  color: var(--color-text);
}

.article-nav-card__item--active {
  border-left-color: var(--color-heading);
}

.article-nav-card__item a {
  display: block;
  padding: 6px 12px;
  font-size: 13px;
  color: var(--color-text-mute);
  text-decoration: none;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: color 0.2s;
}

.article-nav-card__item--active a {
  color: var(--color-heading);
  font-weight: 600;
}

.article-nav-card__item a:hover {
  color: var(--color-heading);
}

.article-nav-card__item--level2 a {
  padding-left: 24px;
}

.article-nav-card__item--level3 a {
  padding-left: 36px;
}
</style>
