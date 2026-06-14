import api from './request'

// ── 登录 ─────────────────────────────────────────────────────────
export const login = (username: string, password: string) =>
  api.post('admin/login/', { username, password })

// ── Token 刷新 ───────────────────────────────────────────────────
export const refreshToken = (refresh: string) =>
  api.post('token/refresh/', { refresh })

// ── 当前用户 ─────────────────────────────────────────────────────
export const updateUser = (data: { username?: string; old_password?: string; new_password?: string }) =>
  api.put('admin/user/', data)
