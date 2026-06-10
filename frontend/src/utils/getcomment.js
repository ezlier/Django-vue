import api from "@/utils/request"

export const getcomment = (slug) =>
  api.get(`/user/article/${slug}/comment/`)

export const upcomment = (slug, data) =>
  api.post(`/user/article/${slug}/comment/`, data)


// ── Admin ───────────────────────────────────────
export const getadminComment = () =>
  api.get("/admin/comment/")

export const deleteComment = (id) =>
  api.delete(`/admin/comment/${id}/`)

export const batchDeleteComments = (ids) =>
  api.delete(`/admin/comment/batch-delete/`, { data: { ids } })
