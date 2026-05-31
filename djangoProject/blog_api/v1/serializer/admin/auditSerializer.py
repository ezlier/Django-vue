from rest_framework import serializers
from blog_api.models import AdminAuditLog


class AdminAuditLogSerializer(serializers.ModelSerializer):
    """管理员操作记录序列化器"""

    user_username = serializers.CharField(source='user.username', read_only=True)
    action_type_display = serializers.CharField(source='get_action_type_display', read_only=True)
    action_result_display = serializers.CharField(source='get_action_result_display', read_only=True)
    action_time_formatted = serializers.SerializerMethodField()

    class Meta:
        model = AdminAuditLog
        fields = [
            'id',
            'user',
            'user_username',
            'action_time',
            'action_time_formatted',
            'action_type',
            'action_type_display',
            'action_result',
            'action_result_display',
            'ip_address',
            'user_agent',
            'target_model',
            'target_id',
            'target_name',
            'details',
            'error_message',
        ]
        read_only_fields = fields  # 所有字段都是只读的

    def get_action_time_formatted(self, obj):
        """格式化操作时间"""
        return obj.action_time.strftime('%Y-%m-%d %H:%M:%S')

    def to_representation(self, instance):
        """自定义序列化输出"""
        data = super().to_representation(instance)
        if data.get('error_message') and len(data['error_message']) > 200:
            data['error_message'] = data['error_message'][:200] + '...'
        if data.get('user_agent') and len(data['user_agent']) > 100:
            data['user_agent'] = data['user_agent'][:100] + '...'
        return data


class AdminAuditLogFilterSerializer(serializers.Serializer):
    """操作记录过滤序列化器"""

    user_id = serializers.IntegerField(required=False, allow_null=True)
    action_type = serializers.CharField(required=False, allow_null=True)
    action_result = serializers.CharField(required=False, allow_null=True)
    start_date = serializers.DateTimeField(required=False, allow_null=True)
    end_date = serializers.DateTimeField(required=False, allow_null=True)
    target_model = serializers.CharField(required=False, allow_null=True)
    search_text = serializers.CharField(required=False, allow_null=True)
    limit = serializers.IntegerField(default=100, min_value=1, max_value=1000)
    offset = serializers.IntegerField(default=0, min_value=0)

    def validate_action_type(self, value):
        """验证操作类型"""
        if value and value not in dict(AdminAuditLog.ACTION_CHOICES):
            valid_choices = ', '.join([choice[0] for choice in AdminAuditLog.ACTION_CHOICES])
            raise serializers.ValidationError(f"无效的操作类型，有效值为: {valid_choices}")
        return value

    def validate_action_result(self, value):
        """验证操作结果"""
        if value and value not in dict(AdminAuditLog.RESULT_CHOICES):
            valid_choices = ', '.join([choice[0] for choice in AdminAuditLog.RESULT_CHOICES])
            raise serializers.ValidationError(f"无效的操作结果，有效值为: {valid_choices}")
        return value

    def validate(self, data):
        """验证日期范围"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("开始时间不能晚于结束时间")
        return data
