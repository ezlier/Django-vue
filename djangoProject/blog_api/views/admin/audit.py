from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

from blog_api.services.admin.auditService import AuditService
from blog_api.serializer.admin.auditSerializer import AdminAuditLogSerializer, AdminAuditLogFilterSerializer
from blog_api.views.response import ApiResponse


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_admin_audit_logs(request):
    """
    获取管理员操作记录
    
    查询参数:
        user_id: 用户ID
        action_type: 操作类型
        action_result: 操作结果
        start_date: 开始时间 (YYYY-MM-DD或YYYY-MM-DD HH:MM:SS)
        end_date: 结束时间
        target_model: 目标模型
        search_text: 搜索文本
        limit: 返回数量 (默认100, 最大1000)
        offset: 偏移量 (默认0)
    """
    # 验证过滤参数
    filter_serializer = AdminAuditLogFilterSerializer(data=request.query_params)
    if not filter_serializer.is_valid():
        return ApiResponse.bad_request("参数错误", errors=filter_serializer.errors)
    
    filters = filter_serializer.validated_data
    
    # 获取操作记录
    result = AuditService.get_audit_logs(**filters)
    
    # 序列化数据
    logs_data = AdminAuditLogSerializer(result['logs'], many=True).data
    
    return ApiResponse.success({
        'total': result['total'],
        'logs': logs_data,
        'limit': result['limit'],
        'offset': result['offset'],
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def export_admin_audit_logs(request):
    """
    导出管理员操作记录
    
    查询参数: 同get_admin_audit_logs
    额外参数:
        format: 导出格式 (json或csv, 默认csv)
    """
    # 验证过滤参数
    filter_serializer = AdminAuditLogFilterSerializer(data=request.query_params)
    if not filter_serializer.is_valid():
        return ApiResponse.bad_request("参数错误", errors=filter_serializer.errors)
    
    filters = filter_serializer.validated_data
    
    # 获取导出格式
    export_format = request.query_params.get('format', 'csv').lower()
    if export_format not in ['json', 'csv']:
        return ApiResponse.bad_request("不支持的导出格式，请使用json或csv")
    
    # 导出数据
    try:
        export_data = AuditService.export_audit_logs(format=export_format, **filters)
        
        if export_format == 'csv':
            response = HttpResponse(export_data, content_type='text/csv; charset=utf-8')
            filename = f"admin_audit_logs_{filters.get('start_date', '')}_{filters.get('end_date', '')}.csv".replace(':', '-').replace(' ', '_')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        
        elif export_format == 'json':
            return ApiResponse.success(export_data)
            
    except Exception as e:
        return ApiResponse.error(f"导出失败: {str(e)}")


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_admin_audit_statistics(request):
    """
    获取操作记录统计信息
    
    查询参数:
        start_date: 开始时间
        end_date: 结束时间
    """
    from django.db.models import Count
    from blog_api.models import AdminAuditLog
    
    # 基本过滤
    queryset = AdminAuditLog.objects.all()
    
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    if start_date:
        queryset = queryset.filter(action_time__gte=start_date)
    if end_date:
        queryset = queryset.filter(action_time__lte=end_date)
    
    # 操作类型统计
    action_type_stats = (
        queryset.values('action_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    
    # 操作结果统计
    action_result_stats = (
        queryset.values('action_result')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    
    # 管理员操作统计
    user_stats = (
        queryset.filter(user__isnull=False)
        .values('user__username')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]  # 前10名管理员
    )
    
    # 每日操作统计（最近30天）
    from django.utils import timezone
    from datetime import timedelta
    
    thirty_days_ago = timezone.now() - timedelta(days=30)
    daily_stats = (
        queryset.filter(action_time__gte=thirty_days_ago)
        .extra(select={'day': "DATE(action_time)"})
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    
    # 失败操作统计
    failure_stats = (
        queryset.filter(action_result=AdminAuditLog.RESULT_FAILURE)
        .values('action_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    
    return ApiResponse.success({
        'action_type_stats': list(action_type_stats),
        'action_result_stats': list(action_result_stats),
        'user_stats': list(user_stats),
        'daily_stats': list(daily_stats),
        'failure_stats': list(failure_stats),
        'total_count': queryset.count(),
        'success_count': queryset.filter(action_result=AdminAuditLog.RESULT_SUCCESS).count(),
        'failure_count': queryset.filter(action_result=AdminAuditLog.RESULT_FAILURE).count(),
    })