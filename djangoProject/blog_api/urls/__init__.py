"""
v2 路由聚合模块

Admin — Article, Tag, Comment, Message, BannedWord 使用 Router 自动注册。
        WebSetting, Visitor, Audit, Dashboard, Auth 保留手动路由。
User  — Article, Comment, Message, WebSetting, About 使用 Router 自动注册。

非 ViewSet 的剩余资源（visitor, audit, dashboard, login）保留在 admin_urls.py。
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from blog_api.v2.views.admin.articles import AdminArticleViewSet
from blog_api.v2.views.admin.admin_views import (
    AdminTagViewSet,
    AdminCommentViewSet,
    AdminMessageViewSet,
    AdminBannedWordViewSet,
    AdminWebSettingViewSet,
)
from blog_api.v2.views.user.articles import UserArticleViewSet
from blog_api.v2.views.user.user_views import (
    UserCommentViewSet,
    UserMessageViewSet,
    UserWebSettingViewSet,
)

# ── Admin Router ──────────────────────────────────────────────────
admin_router = DefaultRouter()
admin_router.register(r'article', AdminArticleViewSet, basename='admin-article')
admin_router.register(r'tag', AdminTagViewSet, basename='admin-tag')
admin_router.register(r'comment', AdminCommentViewSet, basename='admin-comment')
admin_router.register(r'message', AdminMessageViewSet, basename='admin-message')
admin_router.register(r'bannedword', AdminBannedWordViewSet, basename='admin-bannedword')

# ── User Router ───────────────────────────────────────────────────
user_router = DefaultRouter()
user_router.register(r'article', UserArticleViewSet, basename='user-article')

app_name = 'v2'

urlpatterns = [
    # Router 生成的资源路由
    path('admin/', include(admin_router.urls)),
    path('user/', include(user_router.urls)),

    # WebSetting, Comment/Message nested, WebSetting/About 走自定义路由
    path('admin/', include('blog_api.urls.admin_urls')),
    path('user/', include('blog_api.urls.user_urls')),
]
