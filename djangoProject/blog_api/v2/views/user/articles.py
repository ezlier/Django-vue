"""
v2 User Article ViewSet — 公开接口

用法（Phase 2 启用 Router 后自动生成）:
  GET    /api/v2/user/article/              → list
  GET    /api/v2/user/article/{slug}/       → retrieve
  GET    /api/v2/user/tag/                  → list (custom action)
"""
from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from blog_api.models import Article, Tag
from blog_api.v2.serializer.articleSerializer import (
    UserArticleListSerializer,
    UserArticleDetailSerializer,
    TagsSerializer,
)
from blog_api.v2.services.articleService import ArticleService
from blog_api.v1.views.response import ApiResponse


class UserArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    User 文章接口 —— 只读，仅返回已发布文章

    GET /article/            → 文章列表 (分页)
    GET /article/{slug}/     → 文章详情
    GET /tag/                → 标签列表
    """
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"
    lookup_value_regex = r"[^/]+"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.article_service = ArticleService()

    @property
    def paginator(self):
        """返回自定义分页器，允许客户端通过 page_size 覆盖全局 PAGE_SIZE"""
        if not hasattr(self, '_paginator'):
            from rest_framework.pagination import PageNumberPagination
            self._paginator = PageNumberPagination()
            page_size = self.request.query_params.get('page_size')
            if page_size is not None:
                self._paginator.page_size = int(page_size)
        return self._paginator

    def get_queryset(self):
        return self.article_service.list_published().all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserArticleDetailSerializer
        return UserArticleListSerializer

    def retrieve(self, request, *args, **kwargs):
        article = self.get_object()
        serializer = self.get_serializer(article)
        return ApiResponse.success(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(serializer.data)

    @action(detail=False, methods=["get"], url_path="tag")
    def tag_list(self, request):
        tags = self.article_service.list_tags()
        serializer = TagsSerializer(tags, many=True, context={"request": request})
        return ApiResponse.success(serializer.data)
