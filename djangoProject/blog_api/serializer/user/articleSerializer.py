from rest_framework import serializers

from blog_api.models import Article, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class ArticleSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    updated_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    tags = TagSerializer(many=True, read_only=True)
    cover = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "cover",
            "created_time",
            "updated_time",
            "like_count",
            "tags"
        ]

    def get_cover(self, obj):
        request = self.context.get("request")
        if obj.cover:
            return request.build_absolute_uri(obj.cover.url)
        return None


class TagsSerializer(serializers.ModelSerializer):
    article_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = ["id", "name", "article_count"]