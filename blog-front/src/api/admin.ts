import api from './request'
import type { AxiosProgressEvent } from 'axios'

// ═══════════ Admin 接口 ═══════════

// ── Article ───────────────────────────────────
export const getAdminArticles = (params?: Record<string, any>) =>
  api.get('admin/article/', { params })

export const getAdminArticle = (slug: string) =>
  api.get(`admin/article/${slug}/`)

export const createArticle = (formData: FormData) =>
  api.post('admin/article/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

export const uploadArticle = (formData: FormData, onProgress?: (e: AxiosProgressEvent) => void) =>
  api.post('admin/article/upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: onProgress,
  })

export const updateArticle = (slug: string, formData: FormData) =>
  api.put(`admin/article/${slug}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

export const updateArticleStatus = (slug: string, isDraft: boolean) =>
  api.patch(`admin/article/${slug}/status/`, { is_draft: isDraft })

export const deleteArticle = (slug: string) =>
  api.delete(`admin/article/${slug}/`)

export const batchDeleteArticles = (ids: number[]) =>
  api.delete('admin/article/batch-delete/', { data: { ids } })

// ── Tag ───────────────────────────────────────
export const getAdminTags = () =>
  api.get('admin/tag/')

export const createTag = (name: string) =>
  api.post('admin/tag/', { name })

export const updateTag = (id: number, name: string) =>
  api.put(`admin/tag/${id}/`, { name })

export const deleteTag = (id: number) =>
  api.delete(`admin/tag/${id}/`)

// ── Comment ───────────────────────────────────
export const getAdminComments = () =>
  api.get('admin/comment/')

export const deleteComment = (id: number) =>
  api.delete(`admin/comment/${id}/`)

export const batchDeleteComments = (ids: number[]) =>
  api.delete('admin/comment/batch-delete/', { data: { ids } })

// ── Message ───────────────────────────────────
export const getAdminMessages = () =>
  api.get('admin/message/')

export const deleteMessage = (id: number) =>
  api.delete(`admin/message/${id}/`)

export const batchDeleteMessages = (ids: number[]) =>
  api.delete('admin/message/batch-delete/', { data: { ids } })

// ── BannedWord ────────────────────────────────
export const getBannedWords = () =>
  api.get('admin/bannedword/')

export const createBannedWord = (word: string) =>
  api.post('admin/bannedword/', { word })

export const deleteBannedWord = (id: number) =>
  api.delete(`admin/bannedword/${id}/`)

export const batchDeleteBannedWords = (ids: number[]) =>
  api.delete('admin/bannedword/batch-delete/', { data: { ids } })

// ── WebSetting ────────────────────────────────
export const getAdminWebSetting = () =>
  api.get('admin/websetting/settings/')

export const updateWebSetting = (formData: FormData) =>
  api.put('admin/websetting/update/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

// ── Visitor ───────────────────────────────────
export const getVisitorStats = (page = 1) =>
  api.get('admin/visitor-stats/', { params: { page } })

// ── Audit ─────────────────────────────────────
export const getAuditLogs = (params?: Record<string, any>) =>
  api.get('admin/audit/logs/', { params })

export const getAuditStatistics = (params?: Record<string, any>) =>
  api.get('admin/audit/statistics/', { params })

// ── Dashboard ─────────────────────────────────
export const getDashboard = () =>
  api.get('admin/dashboard/')
