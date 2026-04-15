from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404

from blog_api.models import Article, Tag


class ArticleService:

    @staticmethod
    def getArticles():
        return Article.objects.filter(is_draft=False).prefetch_related("tags").order_by("-created_time")

    @staticmethod
    def getArticle(slug):
        article = get_object_or_404(Article, slug=slug, is_draft=False)
        try:
            # 尝试读取 md 文件内容
            with article.md_file.open("rb") as f:
                content = f.read().decode("utf-8")
        except FileNotFoundError:
            # 如果文件不存在，抛出 404 错误
            raise Http404("MD 文件不存在")
        except Exception as e:
            # 捕获其他异常并记录或返回通用错误
            raise Http404(f"读取文件时发生错误: {str(e)}")
        return article, content

    @staticmethod
    def getTags():
        return Tag.objects.annotate(article_count=Count("article")).order_by("-article_count")