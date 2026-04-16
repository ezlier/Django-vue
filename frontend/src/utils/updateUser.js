import api from "@/utils/request"

export const updateUsername = (username) => {
    return api.put('/updateUser/', { username })
}

export const updatePassword = (oldPassword, newPassword) => {
    return api.put('/updateUser/', {
        old_password: oldPassword,
        new_password: newPassword
    })
}
