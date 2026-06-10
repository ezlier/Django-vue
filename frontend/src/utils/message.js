import api from "@/utils/request"

export const getMessage = () =>
  api.get("/user/message/")

export const upMessage = (data) =>
  api.post("/user/message/", data)


// ── Admin ───────────────────────────────────────
export const getadminMessage = () =>
  api.get("/admin/message/")

export const deleteMessage = (id) =>
  api.delete(`/admin/message/${id}/`)

export const batchDeleteMessages = (ids) =>
  api.delete(`/admin/message/batch-delete/`, { data: { ids } })
