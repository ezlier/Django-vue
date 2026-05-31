import functools
from django.contrib.auth import get_user_model
from blog_api.v1.services.admin.auditService import AuditService
from .models import AdminAuditLog

User = get_user_model()


def audit_admin_action(action_type, target_model=None, get_target_id=None, get_target_name=None):
    """
    管理员操作审计装饰器
    
    参数:
        action_type: 操作类型 (AdminAuditLog.ACTION_*)
        target_model: 目标模型名称（字符串）
        get_target_id: 从视图返回值或请求中获取目标ID的函数
        get_target_name: 从视图返回值或请求中获取目标名称的函数
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # 执行视图函数
            response = view_func(request, *args, **kwargs)
            
            # 检查用户是否已认证且是管理员
            if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
                return response
            
            try:
                # 确定操作结果
                action_result = AdminAuditLog.RESULT_SUCCESS
                error_message = None
                
                # 检查响应状态码（假设使用ApiResponse）
                if hasattr(response, 'data'):
                    response_data = response.data
                    if isinstance(response_data, dict):
                        code = response_data.get('code')
                        if code and code >= 400:  # 错误状态码
                            action_result = AdminAuditLog.RESULT_FAILURE
                            error_message = response_data.get('msg', '操作失败')
                
                # 获取目标信息
                target_id = None
                target_name = None
                
                if get_target_id:
                    target_id = get_target_id(response, request, *args, **kwargs)
                
                if get_target_name:
                    target_name = get_target_name(response, request, *args, **kwargs)
                
                # 创建操作记录
                AuditService.create_audit_log(
                    user=request.user,
                    action_type=action_type,
                    action_result=action_result,
                    request=request,
                    target_model=target_model,
                    target_id=target_id,
                    target_name=target_name,
                    error_message=error_message
                )
                
            except Exception as e:
                # 记录失败时不影响主流程
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"记录管理员操作失败: {e}", exc_info=True)
            
            return response
        
        return wrapped_view
    
    return decorator


# 预定义的装饰器函数
def audit_article_create(view_func):
    """审计文章创建"""
    def get_target_id(response, request, *args, **kwargs):
        if hasattr(response, 'data'):
            data = response.data
            if isinstance(data, dict):
                return data.get('data', {}).get('id')
        return None
    
    def get_target_name(response, request, *args, **kwargs):
        # 从请求数据中获取标题
        if request.method == 'POST' and hasattr(request, 'data'):
            return request.data.get('title')
        return None
    
    return audit_admin_action(
        action_type=AdminAuditLog.ACTION_ARTICLE_CREATE,
        target_model='Article',
        get_target_id=get_target_id,
        get_target_name=get_target_name
    )(view_func)


def audit_article_update(view_func):
    """审计文章更新"""
    def get_target_id(response, request, slug, *args, **kwargs):
        # slug作为文章标识
        return slug
    
    def get_target_name(response, request, slug, *args, **kwargs):
        return f"文章: {slug}"
    
    return audit_admin_action(
        action_type=AdminAuditLog.ACTION_ARTICLE_UPDATE,
        target_model='Article',
        get_target_id=get_target_id,
        get_target_name=get_target_name
    )(view_func)


def audit_article_delete(view_func):
    """审计文章删除"""
    def get_target_id(response, request, pk, *args, **kwargs):
        return pk
    
    def get_target_name(response, request, pk, *args, **kwargs):
        return f"文章ID: {pk}"
    
    return audit_admin_action(
        action_type=AdminAuditLog.ACTION_ARTICLE_DELETE,
        target_model='Article',
        get_target_id=get_target_id,
        get_target_name=get_target_name
    )(view_func)


def audit_tag_create(view_func):
    """审计标签创建"""
    def get_target_id(response, request, *args, **kwargs):
        if hasattr(response, 'data'):
            data = response.data
            if isinstance(data, dict):
                return data.get('data', {}).get('id')
        return None
    
    def get_target_name(response, request, *args, **kwargs):
        if request.method == 'POST' and hasattr(request, 'data'):
            return request.data.get('name')
        return None
    
    return audit_admin_action(
        action_type=AdminAuditLog.ACTION_TAG_CREATE,
        target_model='Tag',
        get_target_id=get_target_id,
        get_target_name=get_target_name
    )(view_func)


def audit_tag_update(view_func):
    """审计标签更新"""
    def get_target_id(response, request, id, *args, **kwargs):
        return id
    
    def get_target_name(response, request, id, *args, **kwargs):
        return f"标签ID: {id}"
    
    return audit_admin_action(
        action_type=AdminAuditLog.ACTION_TAG_UPDATE,
        target_model='Tag',
        get_target_id=get_target_id,
        get_target_name=get_target_name
    )(view_func)


def audit_tag_delete(view_func):
    """审计标签删除"""
    def get_target_id(response, request, id, *args, **kwargs):
        return id
    
    def get_target_name(response, request, id, *args, **kwargs):
        return f"标签ID: {id}"
    
    return audit_admin_action(
        action_type=AdminAuditLog.ACTION_TAG_DELETE,
        target_model='Tag',
        get_target_id=get_target_id,
        get_target_name=get_target_name
    )(view_func)


def audit_comment_delete(view_func):
    """审计评论删除"""
    def get_target_id(response, request, pk, *args, **kwargs):
        return pk
    
    def get_target_name(response, request, pk, *args, **kwargs):
        return f"评论ID: {pk}"
    
    return audit_admin_action(
        action_type=AdminAuditLog.ACTION_COMMENT_DELETE,
        target_model='Comment',
        get_target_id=get_target_id,
        get_target_name=get_target_name
    )(view_func)


def audit_message_delete(view_func):
    """审计留言删除"""
    def get_target_id(response, request, id, *args, **kwargs):
        return id
    
    def get_target_name(response, request, id, *args, **kwargs):
        return f"留言ID: {id}"
    
    return audit_admin_action(
        action_type=AdminAuditLog.ACTION_MESSAGE_DELETE,
        target_model='Message',
        get_target_id=get_target_id,
        get_target_name=get_target_name
    )(view_func)


def audit_bannedword_create(view_func):
    """审计违禁词添加"""
    def get_target_name(response, request, *args, **kwargs):
        if request.method == 'POST' and hasattr(request, 'data'):
            return request.data.get('word', '')[:100]
        return None
    
    return audit_admin_action(
        action_type=AdminAuditLog.ACTION_BANNEDWORD_CREATE,
        target_model='Bannedwords',
        get_target_name=get_target_name
    )(view_func)


def audit_bannedword_delete(view_func):
    """审计违禁词删除"""
    def get_target_id(response, request, id, *args, **kwargs):
        return id
    
    return audit_admin_action(
        action_type=AdminAuditLog.ACTION_BANNEDWORD_DELETE,
        target_model='Bannedwords',
        get_target_id=get_target_id
    )(view_func)


def audit_websetting_update(view_func):
    """审计网站设置更新"""
    return audit_admin_action(
        action_type=AdminAuditLog.ACTION_WEBSETTING_UPDATE,
        target_model='WebSetting'
    )(view_func)


def audit_visitor_view(view_func):
    """审计访客统计查看"""
    return audit_admin_action(
        action_type=AdminAuditLog.ACTION_VISITOR_VIEW,
    )(view_func)