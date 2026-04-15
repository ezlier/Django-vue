from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.core.files.storage import default_storage

from blog_api.models import Article
from blog_api.serializer.admin.articleSerializer import ArticleUploadSerializer, ArticleCreateSerializer, ArticleUpdateSerializer, AdminArticleListSerializer
from blog_api.services.admin.articleService import ArticleService
from blog_api.views.response import ApiResponse
from blog_api.decorators import audit_article_create, audit_article_update, audit_article_delete


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@audit_article_create
def uploadArticle(request):

    serializer = ArticleUploadSerializer(data=request.data)

    if not serializer.is_valid():
        return ApiResponse.bad_request("上传失败", errors=serializer.errors)

    article = ArticleService.uploadArticle(serializer.validated_data)

    return ApiResponse.success({"id": article.id}, msg="上传成功")


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@audit_article_delete
def deleteArticle(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.md_file:
        if default_storage.exists(article.md_file.name):
            default_storage.delete(article.md_file.name)

    if article.cover:
        if default_storage.exists(article.cover.name):
            default_storage.delete(article.cover.name)
    article.delete()
    return ApiResponse.success(msg="删除成功")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
@audit_article_create
def createArticle(request):
    serializer = ArticleCreateSerializer(data=request.data)

    if serializer.is_valid():
        article = serializer.save()
        return ApiResponse.success({"slug": article.slug}, msg="发布成功")

    return ApiResponse.bad_request("发布失败", errors=serializer.errors)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
@audit_article_update
def updateArticle(request, slug):
    article = get_object_or_404(Article, slug=slug)

    serializer = ArticleUpdateSerializer(
        article,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return ApiResponse.success(msg="修改成功")

    return ApiResponse.bad_request("修改失败", errors=serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def adminGetArticles(request):
    page = request.query_params.get('page', 1)
    page_size = request.query_params.get('page_size', 10)
    is_draft = request.query_params.get('is_draft')
    search = request.query_params.get('search', '')

    queryset = Article.objects.all().order_by("-created_time")

    if is_draft is not None:
        queryset = queryset.filter(is_draft=is_draft.lower() == 'true')

    if search:
        queryset = queryset.filter(title__icontains=search)

    paginator = PageNumberPagination()
    paginator.page_size = int(page_size)
    paginated_queryset = paginator.paginate_queryset(queryset, request)

    serializer = AdminArticleListSerializer(paginated_queryset, many=True, context={"request": request})

    return ApiResponse.success({
        "count": paginator.page.paginator.count,
        "page": int(page),
        "page_size": int(page_size),
        "results": serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def adminGetArticle(request, slug):
    article = get_object_or_404(Article, slug=slug)

    try:
        with article.md_file.open("rb") as f:
            content = f.read().decode("utf-8")
    except FileNotFoundError:
        return ApiResponse.not_found("MD文件不存在")
    except Exception:
        return ApiResponse.error("读取文件失败")

    data = {
        "id": article.id,
        "title": article.title,
        "slug": article.slug,
        "content": content,
        "tags": [tag.name for tag in article.tags.all()],
        "is_draft": article.is_draft,
        "like_count": article.like_count,
        "cover": request.build_absolute_uri(article.cover.url) if article.cover else None,
        "created_time": article.created_time.strftime("%Y-%m-%d %H:%M"),
        "updated_time": article.updated_time.strftime("%Y-%m-%d %H:%M"),
    }

    return ApiResponse.success(data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@audit_article_update
def updateArticleStatus(request, pk):
    article = get_object_or_404(Article, pk=pk)

    is_draft = request.data.get('is_draft')

    if is_draft is None:
        return ApiResponse.bad_request("缺少is_draft参数")

    article.is_draft = is_draft
    article.save()

    status_text = "草稿" if is_draft else "已发布"
    return ApiResponse.success({"is_draft": article.is_draft}, msg=f"文章已设置为{status_text}")