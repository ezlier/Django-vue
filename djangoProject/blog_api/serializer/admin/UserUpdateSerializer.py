from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class UserUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(max_length=150, required=False)

    def validate_username(self, value):
        if value:
            if User.objects.exclude(pk=self.context["request"].user.pk).filter(username=value).exists():
                raise serializers.ValidationError("用户名已存在")
        return value

    def validate_old_password(self, value):
        user = self.context["request"].user
        if value and not user.check_password(value):
            raise serializers.ValidationError("原密码不正确")
        return value

    def validate(self, attrs):
        if not attrs.get('old_password') and not attrs.get('username'):
            raise serializers.ValidationError("必须提供用户名或密码")
        if attrs.get('new_password') and not attrs.get('old_password'):
            raise serializers.ValidationError("修改密码必须提供原密码")
        return attrs

    def save(self):
        user = self.context["request"].user
        username = self.validated_data.get('username')
        new_password = self.validated_data.get('new_password')

        if username:
            user.username = username

        if new_password:
            user.set_password(new_password)

        user.save()
        return user
