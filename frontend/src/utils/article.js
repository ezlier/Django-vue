import api from "@/utils/request"

// ── 获取文章 ───────────────────────────────────
export const getArticle = (slug) =>
  api.get(`user/article/${slug}/`)

export const getArticles2 = (params = {}) =>
  api.get(`user/article/`, { params })


// ── Admin 文章 ─────────────────────────────────
export const getAdminArticles = (params = {}) =>
  api.get(`admin/article/`, { params })

export const getAdminArticle = (slug) =>
  api.get(`admin/article/${slug}/`)

export const createArticle = (data) =>
  api.post(`admin/article/`, data, {
    headers: { "Content-Type": "multipart/form-data" },
  })

export const uploadArticle = (data, config = {}) =>
  api.post(`admin/article/upload/`, data, {
    headers: { "Content-Type": "multipart/form-data" },
    ...config,
  })

export const updateArticle = (slug, data) =>
  api.put(`admin/article/${slug}/`, data, {
    headers: { "Content-Type": "multipart/form-data" },
  })

export const updateArticleStatus = (slug, isDraft) =>
  api.patch(`admin/article/${slug}/status/`, { is_draft: isDraft })

export const deleteArticle = (id) =>
  api.delete(`admin/article/${id}/`)

export const batchDeleteArticles = (ids) =>
  api.delete(`admin/article/batch-delete/`, { data: { ids } })


// ── 标签 ───────────────────────────────────────
export const getTags = () =>
  api.get(`user/article/tag/`)

export const getAdminTags = () =>
  api.get(`admin/tag/`)

export const updateTag = (id, name) =>
  api.put(`admin/tag/${id}/`, { name })

export const deleteTag = (id) =>
  api.delete(`admin/tag/${id}/`)


// ── 兼容旧 API 名称（组件中仍在使用） ──────────
export const CreateArticle = createArticle
export const uploadArticles = uploadArticle
export const deleteArticle2 = deleteArticle
