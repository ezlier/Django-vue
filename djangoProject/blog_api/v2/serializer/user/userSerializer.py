"""
v2 User Serializers — Comment, Message, WebSetting
"""
from rest_framework import serializers

from blog_api.models import Comment, Message, WebSetting
from blog_api.v2.validators import validate_name, validate_text


# ── Comment ───────────────────────────────────────────────────────

class UserCommentListSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "name", "text", "time"]
        read_only_fields = ["id", "time"]

    validate_name = validate_name
    validate_text = validate_text


class UserCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["name", "text", "QQ", "email"]

    validate_name = validate_name
    validate_text = validate_text


# ── Message ───────────────────────────────────────────────────────

class UserMessageListSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "name", "text", "time"]
        read_only_fields = ["id", "time"]

    validate_name = validate_name
    validate_text = validate_text


class UserMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["name", "text", "QQ", "email"]

    validate_name = validate_name
    validate_text = validate_text


# ── WebSetting ────────────────────────────────────────────────────

class UserWebSettingSerializer(serializers.ModelSerializer):
    updated_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    name_avatar = serializers.SerializerMethodField()

    class Meta:
        model = WebSetting
        fields = "__all__"

    def get_name_avatar(self, obj):
        request = self.context.get("request")
        if obj.name_avatar and request:
            return request.build_absolute_uri(obj.name_avatar.url)
        return None
