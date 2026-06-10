import api from "@/utils/request"

export const getWebSetting = () =>
  api.get(`/user/websetting/`)

export const updateWebSetting = (data) =>
  api.put(`/admin/websetting/update/`, data, {
    headers: { "Content-Type": "multipart/form-data" },
  })
