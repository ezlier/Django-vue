import api from "@/utils/request"

export const getAuditLogs = (params = {}) => {
  return api.get('/admin_audit/logs/', {
    params: {
      limit: params.limit || 20,
      offset: params.offset || 0,
      user_id: params.user_id || undefined,
      action_type: params.action_type || undefined,
      action_result: params.action_result || undefined,
      start_date: params.start_date || undefined,
      end_date: params.end_date || undefined,
      target_model: params.target_model || undefined,
      search_text: params.search_text || undefined
    }
  })
}

export const exportAuditLogs = (params = {}) => {
  const queryString = new URLSearchParams(params).toString()
  window.open(`/api/admin_audit/export/?${queryString}`, '_blank')
}

export const getAuditStatistics = (params = {}) => {
  return api.get('/admin_audit/statistics/', {
    params
  })
}