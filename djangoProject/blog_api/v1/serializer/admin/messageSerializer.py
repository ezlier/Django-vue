from rest_framework import serializers
from blog_api.models import Message, Comment, WebSetting
from ..base import BaseContentSerializer


class adminCommentSerializer(BaseContentSerializer):
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Comment
        fields = "__all__"


class adminMessageSerializer(BaseContentSerializer):
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Message
        fields = "__all__"


class WebSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebSetting
        fields = "__all__"
