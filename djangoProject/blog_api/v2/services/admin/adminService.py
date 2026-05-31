"""
v2 Admin Services — Tag, Comment, Message, BannedWord, WebSetting
"""
from django.shortcuts import get_object_or_404

from blog_api.models import Tag, Comment, Message, WebSetting, Bannedwords


class TagService:
    def __init__(self, tag_repo=None):
        self.tags = tag_repo if tag_repo is not None else Tag.objects

    def list_tags(self):
        return self.tags.all()

    def get_tag(self, tag_id):
        return get_object_or_404(self.tags, pk=tag_id)

    def create_tag(self, name):
        return self.tags.create(name=name.strip())

    def rename(self, tag_id, new_name):
        if self.tags.filter(name=new_name).exists():
            raise Exception("标签名已存在")
        tag = self.tags.get(id=tag_id)
        tag.name = new_name
        tag.save()
        return tag

    def delete(self, tag_id):
        self.tags.filter(id=tag_id).delete()


class CommentService:
    def __init__(self, comment_repo=None):
        self.comments = comment_repo if comment_repo is not None else Comment.objects

    def list_comments(self):
        return self.comments.all()

    def get_comment(self, comment_id):
        return get_object_or_404(self.comments, pk=comment_id)

    def delete(self, comment_id):
        self.comments.filter(id=comment_id).delete()


class MessageService:
    def __init__(self, message_repo=None):
        self.messages = message_repo if message_repo is not None else Message.objects

    def list_messages(self):
        return self.messages.all()

    def get_message(self, message_id):
        return get_object_or_404(self.messages, pk=message_id)

    def delete(self, message_id):
        self.messages.filter(id=message_id).delete()


class BannedWordService:
    def __init__(self, bannedword_repo=None):
        self.bannedwords = bannedword_repo if bannedword_repo is not None else Bannedwords.objects

    def list_bannedwords(self):
        return list(self.bannedwords.all().values("id", "word"))

    def create(self, validated_data):
        word = validated_data.get("word")
        return self.bannedwords.create(word=word)

    def delete(self, bannedword_id):
        self.bannedwords.filter(id=bannedword_id).delete()


class WebSettingService:
    def __init__(self, websetting_repo=None):
        self.websettings = websetting_repo if websetting_repo is not None else WebSetting.objects

    def get_settings(self):
        return self.websettings.first()

    def update(self, data):
        instance = self.websettings.first()
        if not instance:
            return None
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
