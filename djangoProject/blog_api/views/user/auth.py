from django_ratelimit.decorators import ratelimit
from rest_framework.decorators import api_view

from blog_api.serializer.user.aurhSerializer import LoginSerializer
from blog_api.services.user.authService import AuthService
from blog_api.services.admin.auditService import AuditService
from blog_api.views.response import ApiResponse


@api_view(['POST'])
@ratelimit(key='ip', rate='10/m', block=True)
def loginView(request):
    serializer = LoginSerializer(data=request.data)

    if not serializer.is_valid():
        # 记录登录失败（验证失败）
        username = request.data.get('username', '未知用户')
        AuditService.log_login_failure(username, request, "验证失败")
        return ApiResponse.bad_request("登录失败", errors=serializer.errors)

    user = serializer.validated_data['user']
    token_data = AuthService.generate_tokens_for_user(user)

    if not token_data:
        # 记录登录失败（Token生成失败）
        AuditService.log_login_failure(user.username, request, "Token生成失败")
        return ApiResponse.error("登录失败：Token生成失败")

    # 记录登录成功
    AuditService.log_login_success(user, request)
    
    return ApiResponse.success(token_data, msg="登录成功")
