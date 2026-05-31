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
            with article.md_file.open("rb") as f:
                content = f.read().decode("utf-8")
        except FileNotFoundError:
            raise Http404("MD 文件不存在")
        except Exception as e:
            raise Http404(f"读取文件时发生错误: {str(e)}")
        return article, content

    @staticmethod
    def getTags():
        return Tag.objects.annotate(article_count=Count("article")).order_by("-article_count")
