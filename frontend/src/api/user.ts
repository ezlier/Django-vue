import api from './request'

// ═══════════ User 公开接口 ═══════════

// ── Article ───────────────────────────────────
export const getArticles = (params?: Record<string, any>) =>
  api.get('user/article/', { params })

export const getArticle = (slug: string) =>
  api.get(`user/article/${slug}/`)

// ── Tag ───────────────────────────────────────
export const getTags = () =>
  api.get('user/article/tag/')

// ── Comment ───────────────────────────────────
export const getComments = (slug: string) =>
  api.get(`user/article/${slug}/comment/`)

export const createComment = (slug: string, data: { name: string; text: string; QQ?: string; email?: string }) =>
  api.post(`user/article/${slug}/comment/`, data)

// ── Message ───────────────────────────────────
export const getMessages = () =>
  api.get('user/message/')

export const createMessage = (data: { name: string; text: string; QQ?: string; email?: string }) =>
  api.post('user/message/', data)

// ── WebSetting ────────────────────────────────
export const getWebSetting = () =>
  api.get('user/websetting/')

// ── About ─────────────────────────────────────
export const getAbout = () =>
  api.get('user/about/')
