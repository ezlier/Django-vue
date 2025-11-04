import axios from "axios"

const baseURL = "http://127.0.0.1:8000/api"

export const upMessage = (data) => {
  return axios.post(`${baseURL}/message/`, data, {
    headers: {
      "Content-Type": "application/json",
    },
  })
}

export const getMessage = () => axios.get(`${baseURL}/message/`)

export const deleteMessage = (id) =>
  axios.delete(`${baseURL}/message/`,{
    data: {id},
    headers: {
      "Content-Type": "application/json",
    }
  })
  