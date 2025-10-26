import axios from "axios"

const baseURL = "http://127.0.0.1:8000/api"

export const getArticles = () => axios.get(`${baseURL}/articles/`)
export const getArticle = (slug) => axios.get(`${baseURL}/articles/${slug}/`)

export const getPostSum = async () => {
  const res = await axios.get(`${baseURL}/articles/`)
  const articles = res.data
  const count = articles.length
  return count
}

export const getAbout = () => axios.get(`${baseURL}/about/`)