import api from "@/utils/request"

export const bannedwords = () =>
  api.get('/admin/bannedword/')

export const addBannedWord = (data) =>
  api.post('/admin/bannedword/', data)

export const deleteBannedWord = (id) =>
  api.delete(`/admin/bannedword/${id}/`)

export const batchDeleteBannedWords = (ids) =>
  api.delete('/admin/bannedword/batch-delete/', { data: { ids } })
