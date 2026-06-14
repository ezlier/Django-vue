"""
v2 Admin Article ViewSet — 管理后台

用法（Phase 2 启用 Router 后自动生成）:
  GET    /api/v2/admin/article/              → list
  POST   /api/v2/admin/article/              → create
  GET    /api/v2/admin/article/{slug}/       → retrieve
  PUT    /api/v2/admin/article/{slug}/       → update
  PATCH  /api/v2/admin/article/{slug}/       → partial_update
  DELETE /api/v2/admin/article/{slug}/       → destroy
  POST   /api/v2/admin/article/upload/       → upload (custom action)
  PATCH  /api/v2/admin/article/{slug}/status/→ status (custom action)
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser

from blog_api.models import Article
from blog_api.v2.serializer.articleSerializer import (
    AdminArticleListSerializer,
    AdminArticleDetailSerializer,
    AdminArticleCreateSerializer,
    AdminArticleUpdateSerializer,
    AdminArticleUploadSerializer,
    AdminArticleStatusSerializer,
)
from blog_api.v2.services.articleService import ArticleService
from blog_api.v1.views.response import ApiResponse


class AdminArticleViewSet(viewsets.ModelViewSet):
    """
    Admin 文章接口 —— 需认证

    GET    /article/              → 文章列表（分页、搜索、草稿筛选）
    POST   /article/              → 表单创建
    GET    /article/{slug}/       → 文章详情（含正文用于编辑）
    PUT    /article/{slug}/       → 更新
    DELETE /article/{slug}/       → 删除
    POST   /article/upload/       → MD 文件上传创建
    PATCH  /article/{slug}/status/ → 更新发布状态
    """
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "slug"
    lookup_value_regex = r"[^/]+"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.article_service = ArticleService()

    def get_queryset(self):
        return Article.objects.all().order_by("-created_time")

    def get_serializer_class(self):
        action_serializers = {
            "list": AdminArticleListSerializer,
            "retrieve": AdminArticleDetailSerializer,
            "create": AdminArticleCreateSerializer,
            "update": AdminArticleUpdateSerializer,
            "partial_update": AdminArticleUpdateSerializer,
            "upload": AdminArticleUploadSerializer,
            "status": AdminArticleStatusSerializer,
        }
        return action_serializers.get(self.action, AdminArticleListSerializer)

    # ── 列表 ──────────────────────────────────────────────────────

    def list(self, request, *args, **kwargs):
        is_draft = request.query_params.get("is_draft")
        search = request.query_params.get("search", "")

        if is_draft is not None:
            is_draft = is_draft.lower() == "true"

        queryset = self.article_service.list_articles(is_draft=is_draft, search=search)
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(serializer.data)

    # ── 创建（表单） ──────────────────────────────────────────────

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        article = self.article_service.create_from_form(
            title=data["title"],
            mdfile=data["mdfile"],
            cover=data.get("cover"),
            tags=data.get("tags", []),
            is_draft=data.get("is_draft", False),
        )
        return ApiResponse.success({"slug": article.slug}, msg="发布成功")

    # ── 文件上传创建 ──────────────────────────────────────────────

    @action(detail=False, methods=["post"], url_path="upload",
            parser_classes=[MultiPartParser, FormParser])
    def upload(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        article = self.article_service.create_from_upload(
            title=data["title"],
            md_file=data["md_file"],
            cover=data.get("cover"),
            tags=data.get("tags", []),
            is_draft=data.get("is_draft", False),
        )
        return ApiResponse.success({"id": article.id}, msg="上传成功")

    # ── 详情 ──────────────────────────────────────────────────────

    def retrieve(self, request, *args, **kwargs):
        article = self.get_object()
        serializer = self.get_serializer(article)
        return ApiResponse.success(serializer.data)

    # ── 更新 ──────────────────────────────────────────────────────

    def update(self, request, *args, **kwargs):
        article = self.get_object()
        serializer = self.get_serializer(article, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        self.article_service.update_article(
            article,
            title=data.get("title"),
            mdfile=data.get("mdfile"),
            cover=data.get("cover"),
            tags=data.get("tags"),
            is_draft=data.get("is_draft"),
        )
        return ApiResponse.success(msg="修改成功")

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # ── 删除 ──────────────────────────────────────────────────────

    def destroy(self, request, *args, **kwargs):
        article = self.get_object()
        self.article_service.delete_article(article)
        return ApiResponse.success(msg="删除成功")
        # 注意: ApiResponse.success 返回 200，RESTful 规范建议 204
        # 保持与现有前端一致，回复 200

    # ── 批量删除 ──────────────────────────────────────────────────

    @action(detail=False, methods=["delete"], url_path="batch-delete")
    def batch_delete(self, request):
        ids = request.data.get("ids", [])
        if not ids:
            return ApiResponse.bad_request("ids 不能为空")
        for pk in ids:
            try:
                article = Article.objects.get(pk=pk)
                self.article_service.delete_article(article)
            except Article.DoesNotExist:
                pass
        return ApiResponse.success(msg=f"已删除 {len(ids)} 篇文章")

    # ── 状态更新 ──────────────────────────────────────────────────

    @action(detail=True, methods=["patch"], url_path="status")
    def status(self, request, slug=None):
        article = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_draft = serializer.validated_data["is_draft"]

        self.article_service.publish(article, is_draft)
        status_text = "草稿" if is_draft else "已发布"
        return ApiResponse.success({"is_draft": article.is_draft},
                                   msg=f"文章已设置为{status_text}")
