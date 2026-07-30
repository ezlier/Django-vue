<template>
  <div class="profile-card">
    <div class="avatar-bg" :style="AvatarBgStyle"></div>
    <div class="avatar-card">
      <RouterLink to="/about" class="profile-card__avatar-link">
        <img v-if="ui.webSetting?.name_avatar" :src="ui.webSetting.name_avatar" :alt="ui.webSetting?.name || '博主'"
          class="profile-card__avatar" />
        <div v-else class="profile-card__avatar-placeholder">
          {{ (ui.webSetting?.name || 'B')[0] }}
        </div>
      </RouterLink>
      <RouterLink to="/about" class="profile-card__name">
        {{ ui.webSetting?.name || '博主' }}
      </RouterLink>
    </div>

    <div class="profile-card__stats">
      <div class="profile-card__stat">
        <span class="profile-card__stat-num">{{ articleStore.total || articleStore.articleList.length }}</span>
        <span class="profile-card__stat-label">文章</span>
      </div>
      <div class="profile-card__stat">
        <span class="profile-card__stat-num">{{ articleStore.tags.length }}</span>
        <span class="profile-card__stat-label">标签</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUiStore } from '@/stores/ui'
import { useArticleStore } from '@/stores/article'
import { computed } from 'vue'
import AvatarBgImage from '@/assets/img/avatarBg.png'


const ui = useUiStore()
const articleStore = useArticleStore()

const AvatarBgStyle = computed(() => ({
  backgroundImage: `url(${AvatarBgImage})`,
  backgroundSize: 'cover',
  height: '100px',
  borderRadius: '4px',
}))
</script>

<style scoped>
.profile-card {
  padding: 24px 20px;
  border-radius: 12px;
  border: 1px solid var(--color-border);
  background: var(--color-background);
  text-align: center;
}

.avatar-card {
  position: relative;
  margin-top: -50px;
  margin-left: -40%;
}

.profile-card__avatar-link {
  display: inline-block;
  border-radius: 50%;
  box-shadow: 0 0 15px 5px rgba(255, 0, 0, 0.2);
  overflow: hidden;
  transition: transform 0.6s ease;
}

.profile-card__avatar-link:hover {
  transform: rotate(360deg);
}

.profile-card__avatar {
  width: 100px;
  height: 100px;
  object-fit: cover;
  display: block;
}

.profile-card__avatar-placeholder {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: var(--color-background-mute);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 700;
  color: var(--color-heading);
}

.profile-card__name {
  display: block;
  margin-top: 12px;
  font-size: 16px;
  font-weight: 700;
  color: var(--color-heading);
  text-decoration: none;
  transition: opacity 0.2s;
  position: relative;
  top: -7dvh;
  left: 30%;
}

.profile-card__name:hover {
  opacity: 0.7;
}

.profile-card__stats {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-top: 16px;
}

.profile-card__stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.profile-card__stat-num {
  font-size: 18px;
  font-weight: 800;
  color: var(--color-heading);
}

.profile-card__stat-label {
  font-size: 12px;
  color: var(--color-text-mute);
}
</style>
