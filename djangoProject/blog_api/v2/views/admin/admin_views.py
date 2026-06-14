"""
v2 Admin ViewSets — Tag, Comment, Message, WebSetting, BannedWord
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action

from blog_api.models import Tag, Comment, Message, WebSetting, Bannedwords
from blog_api.v2.serializer.admin.adminSerializer import (
    AdminTagSerializer,
    AdminCommentListSerializer,
    AdminMessageListSerializer,
    AdminWebSettingSerializer,
    AdminBannedWordSerializer,
    AdminBannedWordCreateSerializer,
)
from blog_api.v2.services.admin.adminService import (
    TagService,
    CommentService,
    MessageService,
    WebSettingService,
    BannedWordService,
)
from blog_api.v1.views.response import ApiResponse


# ── Tag ───────────────────────────────────────────────────────────

class AdminTagViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag_service = TagService()

    def get_queryset(self):
        return self.tag_service.list_tags()

    def get_serializer_class(self):
        return AdminTagSerializer

    def get_object(self):
        return self.tag_service.get_tag(self.kwargs["id"])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag = self.tag_service.create_tag(serializer.validated_data["name"])
        return ApiResponse.success({"id": tag.id, "name": tag.name}, msg="创建成功")

    def update(self, request, *args, **kwargs):
        self.tag_service.rename(
            self.kwargs["id"],
            request.data.get("name", "")
        )
        return ApiResponse.success(msg="更新成功")

    def destroy(self, request, *args, **kwargs):
        self.tag_service.delete(self.kwargs["id"])
        return ApiResponse.success(msg="删除成功")


# ── Comment ───────────────────────────────────────────────────────

class AdminCommentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ["get", "delete"]
    lookup_field = "pk"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.comment_service = CommentService()

    def get_queryset(self):
        return self.comment_service.list_comments()

    def get_serializer_class(self):
        return AdminCommentListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(serializer.data)

    def destroy(self, request, *args, **kwargs):
        self.comment_service.delete(kwargs["pk"])
        return ApiResponse.success(msg="删除成功")

    @action(detail=False, methods=["delete"], url_path="batch-delete")
    def batch_delete(self, request):
        ids = request.data.get("ids", [])
        if not ids:
            return ApiResponse.bad_request("ids 不能为空")
        for pk in ids:
            try:
                self.comment_service.delete(pk)
            except Comment.DoesNotExist:
                pass
        return ApiResponse.success(msg=f"已删除 {len(ids)} 条评论")


# ── Message ───────────────────────────────────────────────────────

class AdminMessageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ["get", "delete"]
    lookup_field = "pk"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message_service = MessageService()

    def get_queryset(self):
        return self.message_service.list_messages()

    def get_serializer_class(self):
        return AdminMessageListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(serializer.data)

    def destroy(self, request, *args, **kwargs):
        self.message_service.delete(kwargs["pk"])
        return ApiResponse.success(msg="删除成功")

    @action(detail=False, methods=["delete"], url_path="batch-delete")
    def batch_delete(self, request):
        ids = request.data.get("ids", [])
        if not ids:
            return ApiResponse.bad_request("ids 不能为空")
        for pk in ids:
            try:
                self.message_service.delete(pk)
            except Message.DoesNotExist:
                pass
        return ApiResponse.success(msg=f"已删除 {len(ids)} 条留言")


# ── BannedWord ────────────────────────────────────────────────────

class AdminBannedWordViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "pk"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bannedword_service = BannedWordService()

    def get_queryset(self):
        return self.bannedword_service.list_bannedwords()

    def get_serializer_class(self):
        if self.action == "create":
            return AdminBannedWordCreateSerializer
        return AdminBannedWordSerializer

    def list(self, request, *args, **kwargs):
        words = self.bannedword_service.list_bannedwords()
        return ApiResponse.success(words)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.bannedword_service.create(serializer.validated_data)
        return ApiResponse.success(msg="创建成功")

    def destroy(self, request, *args, **kwargs):
        self.bannedword_service.delete(kwargs["pk"])
        return ApiResponse.success(msg="删除成功")

    @action(detail=False, methods=["delete"], url_path="batch-delete")
    def batch_delete(self, request):
        ids = request.data.get("ids", [])
        if not ids:
            return ApiResponse.bad_request("ids 不能为空")
        for pk in ids:
            try:
                self.bannedword_service.delete(pk)
            except Bannedwords.DoesNotExist:
                pass
        return ApiResponse.success(msg=f"已删除 {len(ids)} 个敏感词")


# ── WebSetting ────────────────────────────────────────────────────

class AdminWebSettingViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AdminWebSettingSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.websetting_service = WebSettingService()

    @action(detail=False, methods=["get"])
    def settings(self, request):
        instance = self.websetting_service.get_settings()
        if not instance:
            return ApiResponse.not_found("WebSetting not found")
        serializer = self.get_serializer(instance)
        return ApiResponse.success(serializer.data)

    @action(detail=False, methods=["put"])
    def update_settings(self, request):
        instance = self.websetting_service.get_settings()
        if not instance:
            return ApiResponse.not_found("WebSetting not found")
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.websetting_service.update(serializer.validated_data)
        return ApiResponse.success(serializer.data, msg="更新成功")
