"""
v2 Admin Services — Visitor, Audit, Dashboard, Login, UserUpdate
"""
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from blog_api.models import Visitor, AdminAuditLog
from blog_api.v1.services.admin.auditService import AuditService as v1AuditService

User = get_user_model()


class VisitorService:
    def __init__(self, visitor_repo=None):
        self.visitors = visitor_repo if visitor_repo is not None else Visitor.objects

    def list_visitors(self):
        return self.visitors.all().order_by("-visit_time")


class AuditService:
    def get_logs(self, **filters):
        """复用 v1 AuditService 的查询逻辑"""
        return v1AuditService.get_audit_logs(**filters)

    def get_statistics(self, start_date=None, end_date=None):
        queryset = AdminAuditLog.objects.all()
        if start_date:
            queryset = queryset.filter(action_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(action_time__lte=end_date)

        action_type_stats = list(
            queryset.values("action_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        action_result_stats = list(
            queryset.values("action_result")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        user_stats = list(
            queryset.filter(user__isnull=False)
            .values("user__username")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )
        thirty_days_ago = timezone.now() - timedelta(days=30)
        daily_stats = list(
            queryset.filter(action_time__gte=thirty_days_ago)
            .extra(select={"day": "DATE(action_time)"})
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )
        failure_stats = list(
            queryset.filter(action_result=AdminAuditLog.RESULT_FAILURE)
            .values("action_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        return {
            "action_type_stats": action_type_stats,
            "action_result_stats": action_result_stats,
            "user_stats": user_stats,
            "daily_stats": daily_stats,
            "failure_stats": failure_stats,
            "total_count": queryset.count(),
            "success_count": queryset.filter(action_result=AdminAuditLog.RESULT_SUCCESS).count(),
            "failure_count": queryset.filter(action_result=AdminAuditLog.RESULT_FAILURE).count(),
        }


class AuthService:
    @staticmethod
    def login(username, password):
        user = authenticate(username=username, password=password)
        if not user:
            return None
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        return {
            "token": str(refresh.access_token),
            "refresh": str(refresh),
            "username": user.username,
            "expires_in": refresh.access_token.lifetime.total_seconds(),
        }

    @staticmethod
    def get_dashboard_welcome(user):
        return {"username": user.username}
