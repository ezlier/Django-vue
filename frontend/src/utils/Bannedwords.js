import api from "@/utils/request"

export const bannedwords = () => {
    return api.get('/bannedwords/')
}

export const addBannedWord = (data) => {
    return api.post(`/create_bannedword/`,data,{
    })
}

export const deleteBannedWord = (id) => {
    return api.delete(`/delete_bannedword/${id}/`,{
        data: { id }
    })
}
