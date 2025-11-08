import api from "@/utils/request"

export const get_ip = () => api.get(`/visitor_stats/`)