"""
v2 Admin ViewSets — Visitor, Audit, Dashboard, Login

Router 不接管这些，在 admin_urls.py 中通过 .as_view() 映射。
"""
from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from blog_api.v2.serializer.admin.auditSerializer import (
    VisitorListSerializer,
    AuditLogFilterSerializer,
    AuditLogListSerializer,
)
from blog_api.v2.services.admin.extraService import (
    VisitorService,
    AuditService,
    AuthService,
)
from blog_api.v1.views.response import ApiResponse


# ── Login ─────────────────────────────────────────────────────────

class AdminLoginViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"])
    def login(self, request):
        from blog_api.v1.serializer.user.aurhSerializer import LoginSerializer
        from blog_api.v1.services.admin.auditService import AuditService as v1Audit
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            username = request.data.get("username", "未知用户")
            v1Audit.log_login_failure(username, request, "验证失败")
            return ApiResponse.bad_request("登录失败", errors=serializer.errors)
        user = serializer.validated_data["user"]
        token_data = AuthService.login(user.username, request.data.get("password"))
        # AuthService.login 内部 authenticate 不传 request —— 简化处理：
        # LoginSerializer 已经 authenticate 过，直接生成 token
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        token_data = {
            "token": str(refresh.access_token),
            "refresh": str(refresh),
            "username": user.username,
            "expires_in": refresh.access_token.lifetime.total_seconds(),
        }
        if not token_data:
            v1Audit.log_login_failure(user.username, request, "Token生成失败")
            return ApiResponse.error("登录失败：Token生成失败")
        v1Audit.log_login_success(user, request)
        return ApiResponse.success(token_data, msg="登录成功")


# ── Visitor ───────────────────────────────────────────────────────

class AdminVisitorViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAdminUser]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.visitor_service = VisitorService()

    @action(detail=False, methods=["get"], url_path="visitor-stats")
    def stats(self, request):
        queryset = self.visitor_service.list_visitors()
        page = self.paginate_queryset(queryset)
        if page is not None:
            return ApiResponse.success(
                self.paginator.get_paginated_response(page).data
            )
        return ApiResponse.success(list(queryset))


# ── Audit ─────────────────────────────────────────────────────────

class AdminAuditViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAdminUser]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.audit_service = AuditService()

    @action(detail=False, methods=["get"], url_path="audit/logs")
    def logs(self, request):
        filter_serializer = AuditLogFilterSerializer(data=request.query_params)
        if not filter_serializer.is_valid():
            return ApiResponse.bad_request("参数错误", errors=filter_serializer.errors)
        filters = filter_serializer.validated_data
        result = self.audit_service.get_logs(**filters)
        logs_data = AuditLogListSerializer(result["logs"], many=True).data
        return ApiResponse.success({
            "total": result["total"],
            "logs": logs_data,
            "limit": result["limit"],
            "offset": result["offset"],
        })

    @action(detail=False, methods=["get"], url_path="audit/statistics")
    def statistics(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        stats = self.audit_service.get_statistics(start_date, end_date)
        return ApiResponse.success(stats)


# ── Dashboard ─────────────────────────────────────────────────────

class AdminDashboardViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="dashboard")
    def dashboard(self, request):
        return ApiResponse.success(msg=f"Welcome, {request.user.username}!")
