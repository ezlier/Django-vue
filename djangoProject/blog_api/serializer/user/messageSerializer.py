from rest_framework import serializers
from blog_api.models import Message, Comment, WebSetting
from ..base import BaseContentSerializer


class MessageSerializer(BaseContentSerializer):
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "name", "text", "time"]
        read_only_fields = ["id", "time"]


class CommentSerializer(BaseContentSerializer):
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "name", "text", "time"]
        read_only_fields = ["id", "time"]


class aboutSerializer(serializers.ModelSerializer):
    updated_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    name_avatar = serializers.SerializerMethodField()

    class Meta:
        model = WebSetting
        fields = "__all__"

    def get_name_avatar(self, obj):
        request = self.context.get("request")
        if obj.name_avatar:
            return request.build_absolute_uri(obj.name_avatar.url)
        return None
