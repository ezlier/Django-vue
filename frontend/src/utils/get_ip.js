import axios from "axios"

const baseURL = "http://127.0.0.1:8000/api"

export const get_ip = () => axios.get(`${baseURL}/visitor_stats/`)