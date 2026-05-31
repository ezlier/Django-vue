from rest_framework import serializers
from blog_api.models import Message, Comment, WebSetting


class BaseContentSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True  # 告诉 Django 这是抽象基类

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("姓名不能为空")
        if len(value) > 10:
            raise serializers.ValidationError("姓名长度超限")
        return value

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("内容不能为空")
        if len(value) > 400:
            raise serializers.ValidationError("内容长度超限")
        return value
