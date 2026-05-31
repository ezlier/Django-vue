"""
v2 User ViewSets — Comment, Message
"""
from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from blog_api.models import Article
from blog_api.v2.serializer.user.userSerializer import (
    UserCommentListSerializer,
    UserCommentCreateSerializer,
    UserMessageListSerializer,
    UserMessageCreateSerializer,
    UserWebSettingSerializer,
)
from blog_api.v2.services.user.userService import (
    CommentService,
    MessageService,
    WebSettingService,
)
from blog_api.v1.views.response import ApiResponse
from blog_api.v1.views.user.instrument import get_client_ip


# ── Comment ───────────────────────────────────────────────────────

class UserCommentViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.comment_service = CommentService()

    @action(detail=False, methods=["get"], url_path="(?P<slug>[^/.]+)/comment")
    def list_by_article(self, request, slug=None):
        queryset = self.comment_service.list_by_article(slug)
        serializer = UserCommentListSerializer(queryset, many=True)
        return ApiResponse.success(serializer.data)

    @action(detail=False, methods=["post"], url_path="(?P<slug>[^/.]+)/comment")
    def create_comment(self, request, slug=None):
        serializer = UserCommentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.bad_request("评论失败", errors=serializer.errors)
        result = self.comment_service.create(
            slug, serializer.validated_data, get_client_ip(request)
        )
        if result["code"] == 200:
            return ApiResponse.success(msg="评论成功")
        return ApiResponse.error(result.get("msg", "评论失败"), result.get("code"))


# ── Message ───────────────────────────────────────────────────────

class UserMessageViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message_service = MessageService()

    @action(detail=False, methods=["get"])
    def messages(self, request):
        queryset = self.message_service.list_messages()
        serializer = UserMessageListSerializer(queryset, many=True)
        return ApiResponse.success(serializer.data)

    @action(detail=False, methods=["post"])
    def create_message(self, request):
        serializer = UserMessageCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.bad_request("发送失败", errors=serializer.errors)
        result = self.message_service.create(
            serializer.validated_data, get_client_ip(request)
        )
        if result["code"] == 200:
            return ApiResponse.success(msg="留言成功")
        return ApiResponse.error(result.get("msg", "发送失败"), result.get("code"))


# ── WebSetting ────────────────────────────────────────────────────

class UserWebSettingViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.websetting_service = WebSettingService()

    @action(detail=False, methods=["get"], url_path="websetting")
    def get_websetting(self, request):
        obj = self.websetting_service.get_settings()
        serializer = UserWebSettingSerializer(obj, context={"request": request})
        return ApiResponse.success(serializer.data)

    @action(detail=False, methods=["get"], url_path="about")
    def about(self, request):
        html = self.websetting_service.get_about_html()
        return ApiResponse.success({"html": html})
