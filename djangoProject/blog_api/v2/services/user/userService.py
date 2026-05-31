"""
v2 User Services — Comment, Message
"""
import markdown
from django.core.cache import cache

from blog_api.models import Comment, Message, Bannedwords, Article, WebSetting


class CommentService:
    def __init__(self, comment_repo=None):
        self.comments = comment_repo if comment_repo is not None else Comment.objects

    def list_by_article(self, slug):
        try:
            article = Article.objects.get(slug=slug)
            return self.comments.filter(article=article)
        except Article.DoesNotExist:
            return self.comments.none()

    def create(self, slug, validated_data, ip):
        # 违禁词检测
        self._check_banned_words(validated_data["text"], validated_data["name"])

        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            return {"code": 404, "msg": "文章不存在"}

        validated_data["ip"] = ip
        validated_data["article"] = article
        self.comments.create(**validated_data)
        return {"code": 200, "msg": "评论成功"}

    def _check_banned_words(self, text, name):
        banned_words = cache.get("banned_words")
        if banned_words is None:
            banned_words = list(Bannedwords.objects.values_list("word", flat=True))
            cache.set("banned_words", banned_words, 600)
        content = (text + name).lower()
        if any(word.lower() in content for word in banned_words):
            return {"code": 403, "msg": "不要乱说话喵"}


class MessageService:
    def __init__(self, message_repo=None):
        self.messages = message_repo if message_repo is not None else Message.objects

    def list_messages(self):
        return self.messages.all().order_by("-time")

    def create(self, validated_data, ip):
        banned_words = cache.get("banned_words")
        if banned_words is None:
            banned_words = list(Bannedwords.objects.values_list("word", flat=True))
            cache.set("banned_words", banned_words, 600)

        content = (validated_data["text"] + validated_data["name"]).lower()
        if any(word.lower() in content for word in banned_words):
            return {"code": 403, "msg": "不要乱说话喵"}

        validated_data["ip"] = ip
        self.messages.create(**validated_data)
        return {"code": 200, "msg": "success"}


class WebSettingService:
    def __init__(self, websetting_repo=None):
        self.websettings = websetting_repo if websetting_repo is not None else WebSetting.objects

    def get_settings(self):
        return self.websettings.first()

    def get_about_html(self):
        import os
        from djangoProject import settings
        about_path = os.path.join(settings.BASE_DIR, 'static', 'text', 'about.md')
        try:
            with open(about_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            return markdown.markdown(md_content)
        except FileNotFoundError:
            return None
