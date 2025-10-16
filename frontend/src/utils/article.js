import axios from "axios"

const baseURL = "http://127.0.0.1:8000/api"

export const getArticles = () => axios.get(`${baseURL}/articles/`)
export const getArticle = (slug) => axios.get(`${baseURL}/articles/${slug}/`)
