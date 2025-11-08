import api from "@/utils/request"

export const upMessage = (data) => {
  return api.post("/message/", data)
}

export const getMessage = () => {
  return api.get("/message/")
}

export const getadminMessage = () => {
  return api.get("/admin_message/")
}

export const deleteMessage = (id) => {
  return api.delete("/admin_message/", {
    data: { id }
  })
}