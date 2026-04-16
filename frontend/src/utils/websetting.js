import api from "@/utils/request"

export const getWebSetting = () => api.get(`/get_websetting`)

export const updateWebSetting = (data) => {
  return api.put(`/admin_websetting`, data, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  })
}