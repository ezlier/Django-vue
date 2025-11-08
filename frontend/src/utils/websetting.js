import api from "@/utils/request"

export const getWebSetting = () => api.get(`/get_websetting`)

export const updateWebSetting = (data) => {
  return api.post(`/admin_websetting`, data, {
    headers: {
      "Content-Type": "application/json",
    },
  })
}