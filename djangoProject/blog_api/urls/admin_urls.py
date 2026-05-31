"""
v2 Admin 路由 — Router 已接管 article/tag/comment/message/bannedword，
剩余路由全部走 v2 ViewSet 的 .as_view() 映射。

Admin 接口完整清单 (前缀 /api/v2/admin/):
  POST   /login/                       — 管理员登录
  GET    /visitor-stats/               — 访客统计
  GET    /audit/logs/                  — 审计日志列表
  GET    /audit/statistics/            — 审计统计
  GET    /dashboard/                   — 控制台
  PUT    /user/                        — 更新当前用户信息
  GET    /websetting/settings/         — 网站设置查看
  PUT    /websetting/update/           — 网站设置更新
"""
from django.urls import path

from blog_api.v2.views.admin.extra_views import (
    AdminLoginViewSet,
    AdminVisitorViewSet,
    AdminAuditViewSet,
    AdminDashboardViewSet,
)
from blog_api.v2.views.admin.admin_views import AdminWebSettingViewSet
from blog_api.v1.views.admin.UserUpdate import UserUpdate

urlpatterns = [
    # ── Login ──────────────────────────────────────────────────────
    path('login/',
         AdminLoginViewSet.as_view({"post": "login"}),
         name='admin-login'),

    # ── Visitor ───────────────────────────────────────────────────
    path('visitor-stats/',
         AdminVisitorViewSet.as_view({"get": "stats"}),
         name='admin-visitor-stats'),

    # ── Audit ─────────────────────────────────────────────────────
    path('audit/logs/',
         AdminAuditViewSet.as_view({"get": "logs"}),
         name='admin-audit-logs'),
    path('audit/statistics/',
         AdminAuditViewSet.as_view({"get": "statistics"}),
         name='admin-audit-statistics'),
    # 不再提供 /audit/export/ (已删除 csv 导出功能)

    # ── Dashboard ─────────────────────────────────────────────────
    path('dashboard/',
         AdminDashboardViewSet.as_view({"get": "dashboard"}),
         name='admin-dashboard'),

    # ── WebSetting ────────────────────────────────────────────────
    path('websetting/settings/',
         AdminWebSettingViewSet.as_view({"get": "settings"}),
         name='admin-websetting-get'),
    path('websetting/update/',
         AdminWebSettingViewSet.as_view({"put": "update_settings"}),
         name='admin-websetting-update'),

    # ── User (self update) ────────────────────────────────────────
    path('user/', UserUpdate, name='admin-user-update'),
]
