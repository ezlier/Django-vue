import api from "@/utils/request"

export const get_ip = (page = 1) =>
     api.get(`/visitor_stats/`,{
        params: { page }
     })