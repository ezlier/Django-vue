import api from "@/utils/request"

export const getcomment = (slug) => {
  return api.get(`/articles_comment/${slug}/`)
}

export const upcomment = (slug, data) => {
  return api.post(`/articles_comment/${slug}/`, data)
}

export const getadminComment = () => {
  return api.get("/admin_comment/")
}

export const deleteComment = (id) => {
  return api.delete("/admin_comment/", {
    data: { id }
  })
}