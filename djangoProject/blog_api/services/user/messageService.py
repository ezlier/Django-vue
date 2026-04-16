import os
import markdown

from django.core.cache import cache
from blog_api.models import Message, Bannedwords, Comment, WebSetting
from djangoProject import settings


class MessageService:

    @staticmethod
    def getMessages():
        return Message.objects.all().order_by("time")

    @staticmethod
    def createMessage(validated_data, ip):

        banned_words = cache.get("banned_words")

        if banned_words is None:
            banned_words = list(
                Bannedwords.objects.values_list("word", flat=True)
            )
            cache.set("banned_words", banned_words, 60 * 10)  # 缓存10分钟

        content = (validated_data["text"] + validated_data["name"]).lower()

        if any(word.lower() in content for word in banned_words):
            return {"code": 403, "msg": "不要乱说话喵"}

        validated_data["ip"] = ip
        Message.objects.create(**validated_data)

        return {"code": 200, "msg": "success"}

    @staticmethod
    def getCommit(slug):
        from blog_api.models import Article
        try:
            article = Article.objects.get(slug=slug)
            comments = Comment.objects.filter(article=article)
        except Article.DoesNotExist:
            comments = Comment.objects.none()
        return list(comments)

    @staticmethod
    def createComment(slug, comment, ip):
        from blog_api.models import Article
        
        # 违禁词检测（属于业务逻辑）
        banned_words = cache.get("banned_words")

        if banned_words is None:
            banned_words = list(
                Bannedwords.objects.values_list("word", flat=True)
            )
            cache.set("banned_words", banned_words, 60 * 10)  # 缓存10分钟

        content = (comment["text"] + comment["name"]).lower()

        if any(word.lower() in content for word in banned_words):
            return {"code": 403, "msg": "不要乱说话喵"}
        
        # 查找文章对象
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            return {"code": 404, "msg": "文章不存在"}
            
        comment["ip"] = ip
        comment["article"] = article
        Comment.objects.create(**comment)
        return {"code": 200, "msg": "success"}

    @staticmethod
    def getWebSetting():
        data = WebSetting.objects.first()
        return data

    @staticmethod
    def getAbout():
        about_path = os.path.join(settings.BASE_DIR, 'static', 'text', 'about.md')
        try:
            with open(about_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            html = markdown.markdown(md_content)
            return html
        except FileNotFoundError:
            return {'error': 'about.md not found'}