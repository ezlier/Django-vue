"""
v2 Admin Serializers — Tag, Comment, Message, WebSetting, BannedWord

设计原则:
  - 统一使用 ModelSerializer
  - Serializer 只做校验和序列化，不调用 Service
"""
from rest_framework import serializers

from blog_api.models import Tag, Comment, Message, WebSetting, Bannedwords
from blog_api.v2.validators import validate_word, validate_unique_word


# ── Tag ───────────────────────────────────────────────────────────

class AdminTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


# ── Comment ───────────────────────────────────────────────────────

class AdminCommentListSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class AdminCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


# ── Message ───────────────────────────────────────────────────────

class AdminMessageListSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Message
        fields = "__all__"


class AdminMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


# ── WebSetting ────────────────────────────────────────────────────

class AdminWebSettingSerializer(serializers.ModelSerializer):
    updated_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False)

    class Meta:
        model = WebSetting
        fields = "__all__"


# ── BannedWord ────────────────────────────────────────────────────

class AdminBannedWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bannedwords
        fields = ["id", "word"]
        read_only_fields = ["id"]

    validate_word = validate_word


class AdminBannedWordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bannedwords
        fields = ["word"]

    validate_word = validate_unique_word
