from rest_framework import serializers
from django.urls import reverse

from blog_api.models import Article, Tag
from blog_api.v1.services.admin.articleService import ArticleService


class ArticleUploadSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )

    class Meta:
        model = Article
        fields = ["title", "md_file", "cover", "tags", "is_draft"]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("标题不能为空")
        return value


class ArticleCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    mdfile = serializers.CharField()
    tags = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    cover = serializers.ImageField(required=False)
    is_draft = serializers.BooleanField(required=False, default=False)

    def create(self, validated_data):
        return ArticleService.createArticle(validated_data)


class ArticleUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=False)
    mdfile = serializers.CharField(required=False)
    tags = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )
    cover = serializers.ImageField(required=False)
    is_draft = serializers.BooleanField(required=False)

    def update(self, instance, validated_data):
        return ArticleService.updateArticle(instance, validated_data)


class AdminArticleListSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    is_draft = serializers.BooleanField(read_only=True)

    class Meta:
        model = Article
        fields = ["id", "title", "slug", "cover", "tags", "is_draft", "like_count", "created_time", "updated_time"]

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]
