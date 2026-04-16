import json
from django.db import transaction, models
from django.contrib.auth import get_user_model
from blog_api.models import AdminAuditLog
from django.http import HttpRequest

User = get_user_model()


class AuditService:
    """管理员操作记录服务"""
    
    @staticmethod
    def create_audit_log(
        user,
        action_type,
        action_result,
        request=None,
        target_model=None,
        target_id=None,
        target_name=None,
        details=None,
        error_message=None
    ):
        """
        创建操作记录
        
        参数:
            user: User对象或用户ID
            action_type: 操作类型 (AdminAuditLog.ACTION_*)
            action_result: 操作结果 (AdminAuditLog.RESULT_*)
            request: HttpRequest对象（用于获取IP和User-Agent）
            target_model: 目标模型名称
            target_id: 目标ID
            target_name: 目标名称
            details: 操作详情（字典，会自动转换为JSON）
            error_message: 错误信息
        """
        try:
            # 确保在事务中执行，避免影响主操作
            with transaction.atomic():
                # 获取User对象
                if isinstance(user, int):
                    user_obj = User.objects.filter(id=user).first()
                elif isinstance(user, User):
                    user_obj = user
                else:
                    user_obj = None
                
                # 准备日志数据
                log_data = {
                    'user': user_obj,
                    'action_type': action_type,
                    'action_result': action_result,
                    'target_model': target_model,
                    'target_id': str(target_id) if target_id is not None else None,
                    'target_name': str(target_name) if target_name is not None else None,
                    'error_message': error_message,
                }
                
                # 处理详情数据
                if details is not None:
                    if isinstance(details, dict):
                        log_data['details'] = details
                    else:
                        # 尝试序列化
                        try:
                            log_data['details'] = json.loads(json.dumps(details, default=str))
                        except:
                            log_data['details'] = {'raw_data': str(details)}
                
                # 从request获取IP和User-Agent
                if request is not None and isinstance(request, HttpRequest):
                    # 获取IP地址
                    ip_address = None
                    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                    if x_forwarded_for:
                        ip_address = x_forwarded_for.split(',')[0]
                    else:
                        ip_address = request.META.get('REMOTE_ADDR')
                    
                    log_data['ip_address'] = ip_address
                    log_data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
                
                # 创建记录
                audit_log = AdminAuditLog.objects.create(**log_data)
                return audit_log
                
        except Exception as e:
            # 记录失败时不抛出异常，避免影响主流程
            # 可以记录到系统日志中
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"创建操作记录失败: {e}", exc_info=True)
            return None
    
    @staticmethod
    def log_login_success(user, request):
        """记录登录成功"""
        return AuditService.create_audit_log(
            user=user,
            action_type=AdminAuditLog.ACTION_LOGIN,
            action_result=AdminAuditLog.RESULT_SUCCESS,
            request=request,
            details={'login_method': 'password'}
        )
    
    @staticmethod
    def log_login_failure(username, request, error_message="认证失败"):
        """记录登录失败"""
        # 查找用户（如果存在）
        user = User.objects.filter(username=username).first()
        return AuditService.create_audit_log(
            user=user.id if user else None,
            action_type=AdminAuditLog.ACTION_LOGIN,
            action_result=AdminAuditLog.RESULT_FAILURE,
            request=request,
            details={'attempted_username': username},
            error_message=error_message
        )
    
    @staticmethod
    def log_logout(user, request):
        """记录登出"""
        return AuditService.create_audit_log(
            user=user,
            action_type=AdminAuditLog.ACTION_LOGOUT,
            action_result=AdminAuditLog.RESULT_SUCCESS,
            request=request
        )
    
    @staticmethod
    def log_article_operation(user, action_type, article, request=None, result=AdminAuditLog.RESULT_SUCCESS, error_message=None):
        """记录文章操作"""
        return AuditService.create_audit_log(
            user=user,
            action_type=action_type,
            action_result=result,
            request=request,
            target_model='Article',
            target_id=article.id if article else None,
            target_name=article.title if article else None,
            details={'slug': article.slug if article else None},
            error_message=error_message
        )
    
    @staticmethod
    def log_tag_operation(user, action_type, tag, request=None, result=AdminAuditLog.RESULT_SUCCESS, error_message=None):
        """记录标签操作"""
        return AuditService.create_audit_log(
            user=user,
            action_type=action_type,
            action_result=result,
            request=request,
            target_model='Tag',
            target_id=tag.id if tag else None,
            target_name=tag.name if tag else None,
            error_message=error_message
        )
    
    @staticmethod
    def log_comment_operation(user, action_type, comment, request=None, result=AdminAuditLog.RESULT_SUCCESS, error_message=None):
        """记录评论操作"""
        return AuditService.create_audit_log(
            user=user,
            action_type=action_type,
            action_result=result,
            request=request,
            target_model='Comment',
            target_id=comment.id if comment else None,
            target_name=f"{comment.name} - {comment.text[:50]}" if comment else None,
            details={'article': comment.article.slug if comment and comment.article else None},
            error_message=error_message
        )
    
    @staticmethod
    def log_message_operation(user, action_type, message, request=None, result=AdminAuditLog.RESULT_SUCCESS, error_message=None):
        """记录留言操作"""
        return AuditService.create_audit_log(
            user=user,
            action_type=action_type,
            action_result=result,
            request=request,
            target_model='Message',
            target_id=message.id if message else None,
            target_name=f"{message.name} - {message.text[:50]}" if message else None,
            error_message=error_message
        )
    
    @staticmethod
    def log_bannedword_operation(user, action_type, bannedword, request=None, result=AdminAuditLog.RESULT_SUCCESS, error_message=None):
        """记录违禁词操作"""
        return AuditService.create_audit_log(
            user=user,
            action_type=action_type,
            action_result=result,
            request=request,
            target_model='Bannedwords',
            target_id=bannedword.id if bannedword else None,
            target_name=bannedword.word[:100] if bannedword else None,
            error_message=error_message
        )
    
    @staticmethod
    def log_websetting_operation(user, action_type, websetting, request=None, result=AdminAuditLog.RESULT_SUCCESS, error_message=None):
        """记录网站设置操作"""
        return AuditService.create_audit_log(
            user=user,
            action_type=action_type,
            action_result=result,
            request=request,
            target_model='WebSetting',
            target_id=websetting.id if websetting else None,
            target_name=websetting.web_name if websetting else None,
            error_message=error_message
        )
    
    @staticmethod
    def log_visitor_view(user, request, result=AdminAuditLog.RESULT_SUCCESS):
        """记录查看访客统计"""
        return AuditService.create_audit_log(
            user=user,
            action_type=AdminAuditLog.ACTION_VISITOR_VIEW,
            action_result=result,
            request=request
        )
    
    @staticmethod
    def get_audit_logs(
        user_id=None,
        action_type=None,
        action_result=None,
        start_date=None,
        end_date=None,
        target_model=None,
        search_text=None,
        limit=100,
        offset=0
    ):
        """
        查询操作记录
        
        参数:
            user_id: 用户ID
            action_type: 操作类型
            action_result: 操作结果
            start_date: 开始时间
            end_date: 结束时间
            target_model: 目标模型
            search_text: 搜索文本（在目标名称、错误信息中搜索）
            limit: 返回数量
            offset: 偏移量
        """
        queryset = AdminAuditLog.objects.all()
        
        # 过滤条件
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        
        if action_type is not None:
            queryset = queryset.filter(action_type=action_type)
        
        if action_result is not None:
            queryset = queryset.filter(action_result=action_result)
        
        if target_model is not None:
            queryset = queryset.filter(target_model=target_model)
        
        if start_date is not None:
            queryset = queryset.filter(action_time__gte=start_date)
        
        if end_date is not None:
            queryset = queryset.filter(action_time__lte=end_date)
        
        if search_text is not None:
            queryset = queryset.filter(
                models.Q(target_name__icontains=search_text) |
                models.Q(error_message__icontains=search_text) |
                models.Q(details__icontains=search_text) |
                models.Q(user__username__icontains=search_text)
            )
        
        # 总数
        total = queryset.count()
        
        # 分页
        queryset = queryset.order_by('-action_time')[offset:offset+limit]
        
        return {
            'total': total,
            'logs': list(queryset),
            'limit': limit,
            'offset': offset
        }
    
    @staticmethod
    def export_audit_logs(format='json', **filters):
        """
        导出操作记录
        
        参数:
            format: 导出格式 ('json', 'csv')
            **filters: 过滤参数，同get_audit_logs
        """
        logs_data = AuditService.get_audit_logs(**filters)
        logs = logs_data['logs']
        
        if format == 'json':
            import json
            from django.core.serializers import serialize
            return json.loads(serialize('json', logs))
        
        elif format == 'csv':
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # 写入表头
            writer.writerow([
                'ID', '操作时间', '管理员', '操作类型', '操作结果',
                'IP地址', '目标模型', '目标ID', '目标名称', '错误信息'
            ])
            
            # 写入数据
            for log in logs:
                writer.writerow([
                    log.id,
                    log.action_time.strftime('%Y-%m-%d %H:%M:%S'),
                    log.user.username if log.user else '未知',
                    log.get_action_type_display(),
                    log.get_action_result_display(),
                    log.ip_address or '',
                    log.target_model or '',
                    log.target_id or '',
                    log.target_name or '',
                    log.error_message or ''
                ])
            
            return output.getvalue()
        
        else:
            raise ValueError(f"不支持的导出格式: {format}")