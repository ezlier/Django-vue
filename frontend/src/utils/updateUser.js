import api from "@/utils/request"

export const updateUsername = (username) =>
  api.put('/admin/user/', { username })

export const updatePassword = (oldPassword, newPassword) =>
  api.put('/admin/user/', {
    old_password: oldPassword,
    new_password: newPassword,
  })
