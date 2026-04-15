import api from "@/utils/request"

// 获取单篇文章
export const getArticle = (slug) => {
  return api.get(`/articles/${slug}/`)
}

export const CreateArticle = (data) => {
  return api.post(`/CreateArticle/`, data, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  })
}

export const uploadArticles = (data, config = {}) => {
  return api.post(`/uploadArticles/`, data, {
    headers: {
      "Content-Type": "multipart/form-data"
    },
    ...config
  })
}


export const getArticles2 = (params = {}) => {
  return api.get(`/get_articles/`, { params })
}


export const deleteArticle2 = (id) => {
  return api.delete(`/deleteArticles/${id}/`)
}

export const updateArticle = (slug, data) => {
  return api.put(`/updateArticle/${slug}/`, data, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  })
}

export const getTags = () => {
  return api.get(`/getTags/`)
}

export const updateTag = (id, data) => {
  return api.put(`/updateTag/${id}/`, data)
}

export const getAdminArticles = (params = {}) => {
  return api.get(`/admin/articles/`, { params })
}

export const getAdminArticle = (slug) => {
  return api.get(`/admin/articles/${slug}/`)
}

export const updateArticleStatus = (id, isDraft) => {
  return api.put(`/admin/articles/${id}/status/`, { is_draft: isDraft })
}

export const deleteTag = (id) => {
  return api.delete(`/deleteTag/${id}/`)
}