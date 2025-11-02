import axios from "axios"

const baseURL = "http://127.0.0.1:8000/api"

export const getWebSetting = () => axios.get(`${baseURL}/websetting`)

export const updateWebSetting = (data) => {
  return axios.post(`${baseURL}/websetting`, data, {
    headers: {
      "Content-Type": "application/json",
    },
  })
}