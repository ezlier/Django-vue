"""
v2 User 路由 — 剩余非 ViewSet 路由

Router 已自动接管: article
自定义路由: comment (nested), message, websetting, about

所有路由以 /api/v2/user/ 为前缀。
"""
from django.urls import path, re_path

from blog_api.v2.views.user.user_views import (
    UserCommentViewSet,
    UserMessageViewSet,
    UserWebSettingViewSet,
)

urlpatterns = [
    # ── Comment (nested under article) ────────────────────────────
    # GET  /user/article/{slug}/comment/
    # POST /user/article/{slug}/comment/
    re_path(r'article/(?P<slug>[^/]+)/comment/',
         UserCommentViewSet.as_view({"get": "list_by_article", "post": "create_comment"}),
         name='user-article-comment'),

    # ── Message ───────────────────────────────────────────────────
    # GET  /user/message/
    # POST /user/message/
    path('message/',
         UserMessageViewSet.as_view({"get": "messages", "post": "create_message"}),
         name='user-message'),

    # ── WebSetting ────────────────────────────────────────────────
    path('websetting/',
         UserWebSettingViewSet.as_view({"get": "get_websetting"}),
         name='user-websetting'),

    # ── About ─────────────────────────────────────────────────────
    path('about/',
         UserWebSettingViewSet.as_view({"get": "about"}),
         name='user-about'),
]
