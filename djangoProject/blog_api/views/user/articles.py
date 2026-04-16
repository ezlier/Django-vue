from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from blog_api.serializer.user.articleSerializer import ArticleSerializer, TagsSerializer
from blog_api.services.user.articleService import ArticleService
from blog_api.views.response import ApiResponse


@api_view(['GET'])
def getArticles(request):
    page = request.query_params.get('page', 1)
    page_size = request.query_params.get('page_size', 100)

    queryset = ArticleService.getArticles()

    paginator = PageNumberPagination()
    paginator.page_size = int(page_size)
    paginated_queryset = paginator.paginate_queryset(queryset, request)

    serializer = ArticleSerializer(paginated_queryset, many=True, context={"request": request})

    return ApiResponse.success({
        "count": paginator.page.paginator.count,
        "page": int(page),
        "page_size": int(page_size),
        "results": serializer.data
    })


@api_view(['GET'])
def getArticle(request, slug):
    article, content = ArticleService.getArticle(slug)

    data = {
        "title": article.title,
        "slug": article.slug,
        "content": content,
        "tags": [tag.name for tag in article.tags.all()],
        "created_time": article.created_time.strftime("%Y-%m-%d %H:%M"),
        "updated_time": article.updated_time.strftime("%Y-%m-%d %H:%M"),
        "like_count": article.like_count,
        "cover": request.build_absolute_uri(article.cover.url) if article.cover else None
    }

    return ApiResponse.success(data)


@api_view(['GET'])
def getTags(request):
    queryset = ArticleService.getTags()
    serializer = TagsSerializer(queryset, many=True, context={"request": request})
    return ApiResponse.success(serializer.data)


