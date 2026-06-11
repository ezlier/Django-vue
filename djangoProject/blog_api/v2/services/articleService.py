"""
v2 Article Service — 实例方法 + 构造函数注入依赖

设计原则 (Phase 2):
  - 实例方法替代 @staticmethod
  - 构造函数注入 queryset/repo，默认为 Model.objects，测试时可 Mock
  - Service 不处理序列化/校验 —— 那是 Serializer 和 View 的职责
"""
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils.text import slugify
from django.shortcuts import get_object_or_404

from blog_api.models import Article, Tag


class ArticleService:
    """文章业务逻辑"""

    def __init__(self, article_repo=None, tag_repo=None):
        self.articles = article_repo if article_repo is not None else Article.objects
        self._model = self.articles.model
        self.tags = tag_repo if tag_repo is not None else Tag.objects

    # ── 查询 ──────────────────────────────────────────────────────

    def list_articles(self, is_draft=None, search=""):
        """后台文章列表"""
        qs = self.articles.all().order_by("-created_time")
        if is_draft is not None:
            qs = qs.filter(is_draft=is_draft)
        if search:
            qs = qs.filter(title__icontains=search)
        return qs

    def list_published(self):
        """公开文章列表"""
        return (
            self.articles.filter(is_draft=False)
            .prefetch_related("tags")
            .order_by("-created_time")
        )

    def get_article(self, **lookup):
        """获取单篇文章"""
        return self.articles.get(**lookup)

    def get_article_or_404(self, **lookup):
        return get_object_or_404(self.articles, **lookup)

    # ── 创建 ──────────────────────────────────────────────────────

    @transaction.atomic
    def create_from_form(self, title, mdfile, cover=None, tags=None, is_draft=False):
        """从表单创建文章（title + md 文本 + 可选 cover）"""
        article = self._model(title=title, is_draft=is_draft)
        # 显式生成 slug 并检查唯一性，不依赖模型 save() 的自动生成
        base_slug = slugify(title, allow_unicode=True) or "article"
        slug = base_slug
        counter = 1
        while self.articles.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        article.slug = slug

        md_file = ContentFile(mdfile.encode("utf-8"))
        md_filename = f"{slugify(title, allow_unicode=True)}.md"
        article.md_file.save(md_filename, md_file, save=False)

        if cover:
            article.cover = cover

        article.save()

        if tags:
            self._set_tags(article, tags)

        return article

    @transaction.atomic
    def create_from_upload(self, title, md_file, cover=None, tags=None, is_draft=False):
        """从文件上传创建文章"""
        article = self._model(title=title, is_draft=is_draft)
        # 显式生成 slug 并检查唯一性
        base_slug = slugify(title, allow_unicode=True) or "article"
        slug = base_slug
        counter = 1
        while self.articles.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        article.slug = slug

        article.cover = cover if cover else None

        article.md_file = md_file
        article.save()

        if tags:
            self._set_tags(article, tags)

        return article

    # ── 更新 ──────────────────────────────────────────────────────

    @transaction.atomic
    def update_article(self, article, *, title=None, mdfile=None, cover=None,
                       tags=None, is_draft=None):
        """部分更新文章 —— 只更新传入的字段"""
        if title is not None:
            article.title = title

        if mdfile is not None:
            if article.md_file:
                article.md_file.delete(save=False)
            md_file = ContentFile(mdfile.encode("utf-8"))
            filename = f"{slugify(article.title, allow_unicode=True)}.md"
            article.md_file.save(filename, md_file, save=False)

        if cover is not None:
            if article.cover:
                article.cover.delete(save=False)
            article.cover = cover

        article.save()

        if tags is not None:
            self._set_tags(article, tags)

        if is_draft is not None:
            article.is_draft = is_draft
            article.save(update_fields=["is_draft"])

        return article

    def publish(self, article, is_draft):
        """更新文章发布状态"""
        article.is_draft = is_draft
        article.save(update_fields=["is_draft"])
        return article

    # ── 删除 ──────────────────────────────────────────────────────

    def delete_article(self, article):
        """删除文章及关联文件"""
        if article.md_file:
            article.md_file.delete(save=False)
        if article.cover:
            article.cover.delete(save=False)
        article.delete()

    # ── 标签辅助 ──────────────────────────────────────────────────

    def _set_tags(self, article, tag_names):
        tag_objects = []
        for name in tag_names:
            tag, _ = self.tags.get_or_create(name=name.strip())
            tag_objects.append(tag)
        article.tags.set(tag_objects)

    def list_tags(self):
        """获取标签列表（含文章计数）"""
        from django.db.models import Count
        return self.tags.annotate(article_count=Count("article")).order_by("-article_count")


class TagService:
    """标签业务逻辑"""

    def __init__(self, tag_repo=None):
        self.tags = tag_repo if tag_repo is not None else Tag.objects

    def rename(self, tag_id, new_name):
        if self.tags.filter(name=new_name).exists():
            raise Exception("标签名已存在")
        tag = self.tags.get(id=tag_id)
        tag.name = new_name
        tag.slug = slugify(new_name)
        tag.save()
        return tag

    def get_or_create(self, name):
        return self.tags.get_or_create(name=name.strip())

    def delete(self, tag_id):
        self.tags.filter(id=tag_id).delete()
