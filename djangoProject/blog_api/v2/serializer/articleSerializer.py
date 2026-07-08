"""
v2 Article Serializers — ModelSerializer，只做校验和序列化

设计原则 (Phase 2):
  - 统一使用 ModelSerializer，利用 DRF 自动生成 create/update
  - Serializer 不调用 Service —— 业务逻辑由 View 层调用 Service
  - 公共 validator 提取到 validators.py
"""
from rest_framework import serializers

from blog_api.models import Article, Tag
from blog_api.v2.validators import validate_title, validate_title_optional


def _parse_tags_from_formdata(value):
    """FormData 传 tags 时，DRF 的 ListField 会将 JSON 字符串当作单个标签名存储，
    此方法检测并解析回真正的列表。"""
    if isinstance(value, list) and len(value) == 1 and isinstance(value[0], str):
        import json
        try:
            parsed = json.loads(value[0])
            if isinstance(parsed, list):
                return parsed
        except (json.JSONDecodeError, TypeError):
            pass
    return value


# ── User 侧 Serializer ────────────────────────────────────────────

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class UserArticleListSerializer(serializers.ModelSerializer):
    """User 文章列表 —— 精简字段，不含正文"""
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    cover = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id", "title", "slug", "cover",
            "created_time", "updated_time", "like_count", "tags",
        ]
        read_only_fields = fields

    def get_cover(self, obj):
        request = self.context.get("request")
        if obj.cover and request:
            return request.build_absolute_uri(obj.cover.url)
        return None


class UserArticleDetailSerializer(serializers.ModelSerializer):
    """User 文章详情 —— 含正文内容"""
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    cover = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id", "title", "slug", "cover",
            "content", "tags", "like_count",
            "created_time", "updated_time",
        ]
        read_only_fields = fields

    def get_cover(self, obj):
        request = self.context.get("request")
        if obj.cover and request:
            return request.build_absolute_uri(obj.cover.url)
        return None

    def get_content(self, obj):
        """读取 md_file 内容为纯文本"""
        try:
            with obj.md_file.open("rb") as f:
                return f.read().decode("utf-8")
        except Exception:
            return ""


class TagsSerializer(serializers.ModelSerializer):
    """User 标签列表 —— 带文章计数"""
    article_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = ["id", "name", "article_count"]


# ── Admin 侧 Serializer ───────────────────────────────────────────

class AdminArticleListSerializer(serializers.ModelSerializer):
    """Admin 文章列表"""
    tags = serializers.SerializerMethodField()
    is_draft = serializers.BooleanField(read_only=True)

    class Meta:
        model = Article
        fields = [
            "id", "title", "slug", "cover", "tags", "is_draft",
            "like_count", "created_time", "updated_time",
        ]
        read_only_fields = fields

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]


class AdminArticleDetailSerializer(serializers.ModelSerializer):
    """Admin 文章详情 —— 含正文内容（用于编辑）"""
    tags = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id", "title", "slug", "cover", "content", "tags",
            "is_draft", "like_count", "created_time", "updated_time",
        ]
        read_only_fields = ["id", "slug", "like_count", "created_time", "updated_time"]

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def get_content(self, obj):
        try:
            with obj.md_file.open("rb") as f:
                return f.read().decode("utf-8")
        except Exception:
            return ""


class AdminArticleCreateSerializer(serializers.ModelSerializer):
    """Admin 创建文章 —— 表单方式（title + mdfile + cover + tags）"""
    mdfile = serializers.CharField(write_only=True)
    tags = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )

    class Meta:
        model = Article
        fields = ["title", "mdfile", "cover", "tags", "is_draft"]

    def validate_title(self, value):
        return validate_title(value)

    def validate_tags(self, value):
        return _parse_tags_from_formdata(value)


class AdminArticleUpdateSerializer(serializers.ModelSerializer):
    """Admin 更新文章 —— 部分更新，所有字段 optional"""
    mdfile = serializers.CharField(write_only=True, required=False)
    tags = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )

    class Meta:
        model = Article
        fields = ["title", "mdfile", "cover", "tags", "is_draft"]

    def validate_title(self, value):
        return validate_title_optional(value)

    def validate_tags(self, value):
        return _parse_tags_from_formdata(value)


class AdminArticleStatusSerializer(serializers.ModelSerializer):
    """Admin 文章状态更新 —— 仅 is_draft"""
    is_draft = serializers.BooleanField(required=True)

    class Meta:
        model = Article
        fields = ["is_draft"]


class AdminArticleUploadSerializer(serializers.ModelSerializer):
    """Admin 上传文章 —— MD 文件直传"""
    mdfile = serializers.FileField(write_only=True, source='md_file')
    tags = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )

    class Meta:
        model = Article
        fields = ["title", "mdfile", "cover", "tags", "is_draft"]

    def validate_title(self, value):
        return validate_title(value)

    def validate_tags(self, value):
        return _parse_tags_from_formdata(value)
