import api from "@/utils/request"

// 获取单篇文章
export const getArticle = (slug) => {
  return api.get(`/articles/${slug}/`)
}

// 获取文章总数
export const getPostSum = async () => {
  const res = await api.get(`/articles/`)
  const articles = res.data
  const count = articles.length
  return count
}

// 获取关于页内容
export const getAbout = () => {
  return api.get(`/about/`)
}

// 删除文章
export const deleteArticle = (slug) => {
  return api.delete(`/admin_articles/`, {
    data: { slug },
    headers: {
      "Content-Type": "application/json",
    },
  })
}

// 获取全部文章
export const getArticles = () => {
  return api.get(`/articles/`)
}
