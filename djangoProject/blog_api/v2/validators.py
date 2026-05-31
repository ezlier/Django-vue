"""
公共 validator 函数 —— 供 v2 Serializer 复用

设计原则 (Phase 3):
  - 每个 validator 都是独立函数，接收 value 返回 value
  - 校验失败抛出 serializers.ValidationError
  - 统一管理避免各 Serializer 重复实现
"""
from rest_framework import serializers


def validate_name(value, field_label="姓名", max_length=10):
    """校验姓名/昵称：非空、长度限制"""
    if not value.strip():
        raise serializers.ValidationError(f"{field_label}不能为空")
    if len(value) > max_length:
        raise serializers.ValidationError(f"{field_label}长度不能超过{max_length}个字符")
    return value


def validate_text(value, field_label="内容", max_length=400):
    """校验文本内容：非空、长度限制"""
    if not value.strip():
        raise serializers.ValidationError(f"{field_label}不能为空")
    if len(value) > max_length:
        raise serializers.ValidationError(f"{field_label}长度不能超过{max_length}个字符")
    return value


def validate_title(value, field_label="标题"):
    """校验标题：非空"""
    if not value.strip():
        raise serializers.ValidationError(f"{field_label}不能为空")
    return value


def validate_word(value):
    """校验违禁词：非空"""
    if not value.strip():
        raise serializers.ValidationError("违禁词不能为空")
    return value


def validate_unique_word(value):
    """校验违禁词唯一性"""
    from blog_api.models import Bannedwords
    if not value.strip():
        raise serializers.ValidationError("违禁词不能为空")
    if Bannedwords.objects.filter(word=value).exists():
        raise serializers.ValidationError("该违禁词已存在")
    return value
