import api from "@/utils/request"

export const getAuditLogs = (params = {}) =>
  api.get('/admin/audit/logs/', {
    params: {
      limit: params.limit || 20,
      offset: params.offset || 0,
      user_id: params.user_id || undefined,
      action_type: params.action_type || undefined,
      action_result: params.action_result || undefined,
      start_date: params.start_date || undefined,
      end_date: params.end_date || undefined,
      target_model: params.target_model || undefined,
      search_text: params.search_text || undefined,
    },
  })

// 审计日志导出已移除（v2 不再提供 CSV 导出）

export const getAuditStatistics = (params = {}) =>
  api.get('/admin/audit/statistics/', { params })
