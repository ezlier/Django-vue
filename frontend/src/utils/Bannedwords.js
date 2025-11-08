import api from "@/utils/request"

export const bannedwords = () => {
    return api.get('/bannedwords/')
}

export const addBannedWord = (data) => {
    return api.post(`/bannedwords/`,data,{
    })
}

export const deleteBannedWord = (id) => {
    return api.delete(`/bannedwords/`,{
        data: { id }
    })
}
