from django.core.files.base import ContentFile
from django.db import transaction
from django.utils.text import slugify
from django.shortcuts import get_object_or_404

from blog_api.models import Article, Tag


class ArticleService:

    @staticmethod
    def uploadArticle(validated_data):
        tags = validated_data.pop("tags", [])
        is_draft = validated_data.pop("is_draft", False)

        article = Article.objects.create(is_draft=is_draft, **validated_data)

        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
            article.tags.add(tag)

        return article

    @staticmethod
    @transaction.atomic
    def createArticle(data):
        title = data.get("title")
        md_content = data.get("mdfile")
        tag_names = data.get("tags", [])
        cover_file = data.get("cover")
        is_draft = data.get("is_draft", False)

        article = Article(title=title, is_draft=is_draft)

        # 保存 markdown 文件
        md_file = ContentFile(md_content.encode("utf-8"))
        md_filename = f"{slugify(title, allow_unicode=True)}.md"
        article.md_file.save(md_filename, md_file, save=False)

        # 保存封面
        if cover_file:
            article.cover = cover_file

        # 先保存 article（生成 slug）
        article.save()

        # 处理 tags
        tag_objects = []
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name.strip())
            tag_objects.append(tag)

        article.tags.set(tag_objects)

        return article

    @staticmethod
    @transaction.atomic
    def updateArticle(article, data):
        # 1️⃣ 更新标题
        if "title" in data:
            article.title = data["title"]

        # 2️⃣ 更新 markdown 文件
        if "mdfile" in data:
            md_content = data["mdfile"]

            # 删除旧 md 文件（防止垃圾文件）
            if article.md_file:
                article.md_file.delete(save=False)

            md_file = ContentFile(md_content.encode("utf-8"))
            filename = f"{slugify(article.title, allow_unicode=True)}.md"

            article.md_file.save(filename, md_file, save=False)

        # 3️⃣ 更新封面（只在传了 cover 时）
        if "cover" in data:
            if article.cover:
                article.cover.delete(save=False)
            article.cover = data["cover"]

        article.save()

        # 4️⃣ 更新标签
        if "tags" in data:
            tag_names = data["tags"]
            tag_objects = []

            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name.strip())
                tag_objects.append(tag)

            article.tags.set(tag_objects)

        # 5️⃣ 更新草稿状态
        if "is_draft" in data:
            article.is_draft = data["is_draft"]
            article.save()

        return article


class TagService:

    @staticmethod
    def renameTag(tag_id, new_name):
        if Tag.objects.filter(name=new_name).exists():
            raise Exception("标签名已存在")

        tag = Tag.objects.get(id=tag_id)
        tag.name = new_name
        tag.slug = slugify(new_name)
        tag.save()

        return tag