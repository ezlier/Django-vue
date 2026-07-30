"""
v2 路由聚合模块

Admin — Article, Tag, Comment, Message, BannedWord, WebSetting 使用 Router 自动注册。
        Visitor, Audit, Dashboard, Auth 保留手动路由。
User  — Article, Comment, Message, WebSetting, About 使用 Router 自动注册。

重要：自定义路由（comment nested、message、websetting、about）必须放在
Router 之前，否则 Router 生成的 article/{slug}/ 会先匹配，
导致 POST /article/{slug}/comment/ 被当成 article 详情返回 405。
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from blog_api.v2.views.admin.admin_views import (
    AdminTagViewSet,
    AdminCommentViewSet,
    AdminMessageViewSet,
    AdminBannedWordViewSet,
    AdminWebSettingViewSet,
)
from blog_api.v2.views.admin.articles import AdminArticleViewSet
from blog_api.v2.views.user.articles import UserArticleViewSet

# ── Admin Router ──────────────────────────────────────────────────
admin_router = DefaultRouter()
admin_router.register(r'article', AdminArticleViewSet, basename='admin-article')
admin_router.register(r'tag', AdminTagViewSet, basename='admin-tag')
admin_router.register(r'comment', AdminCommentViewSet, basename='admin-comment')
admin_router.register(r'message', AdminMessageViewSet, basename='admin-message')
admin_router.register(r'bannedword', AdminBannedWordViewSet, basename='admin-bannedword')
admin_router.register(r'websetting', AdminWebSettingViewSet, basename='admin-websetting')

# ── User Router ───────────────────────────────────────────────────
user_router = DefaultRouter()
user_router.register(r'article', UserArticleViewSet, basename='user-article')

app_name = 'v2'

urlpatterns = [
    # 自定义路由必须放在 Router 之前（Django 按顺序匹配）
    path('user/', include('blog_api.urls.user_urls')),
    path('admin/', include('blog_api.urls.admin_urls')),

    # Router 生成的路由
    path('admin/', include(admin_router.urls)),
    path('user/', include(user_router.urls)),
]