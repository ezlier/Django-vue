from datetime import datetime

from django.db import models
from django.utils.text import slugify


def article_md_upload_path(instance, filename):
    ext = filename.split('.')[-1]

    # 如果还没生成 slug，生成一个
    if not instance.slug:
        instance.slug = slugify(instance.title)

    now = datetime.now()

    return f"articles/{now.year}/{now.month}/{instance.slug}.{ext}"


def article_cover_upload_path(instance, filename):
    ext = filename.split('.')[-1]

    if not instance.slug:
        instance.slug = slugify(instance.title)

    now = datetime.now()

    return f"imgs/{now.year}/{now.month}/{instance.slug}.{ext}"


def avatar_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"about/avatar.{ext}"


# Create your models here.
class Visitor(models.Model):
    ip = models.CharField(max_length=50, verbose_name="访客IP")
    path = models.CharField(max_length=200, verbose_name="访问路径")
    user_agent = models.TextField(blank=True, null=True, verbose_name="浏览器信息")
    visit_time = models.DateTimeField(auto_now_add=True, verbose_name="访问时间")

    def __str__(self):
        return f"{self.ip} - {self.path} ({self.visit_time})"


class Message(models.Model):
    ip = models.CharField(max_length=50, verbose_name="IP")
    text = models.TextField()
    name = models.CharField(max_length=30, verbose_name="姓名")
    time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    QQ = models.CharField(max_length=30, verbose_name="QQ", default='', blank=True)
    email = models.CharField(max_length=30, verbose_name="email", default='', blank=True)


class Bannedwords(models.Model):
    word = models.TextField()


class Comment(models.Model):
    ip = models.CharField(max_length=50, verbose_name="IP")
    text = models.TextField()
    name = models.CharField(max_length=30, verbose_name="姓名")
    time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    article = models.ForeignKey('Article', on_delete=models.CASCADE, verbose_name="所属文章", related_name='comments', null=True, blank=True)
    QQ = models.CharField(max_length=30, verbose_name="QQ", default='', blank=True)
    email = models.CharField(max_length=30, verbose_name="email", default='', blank=True)

    def __str__(self):
        return f"{self.name} - {self.text[:50]}"


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, db_index=True)
    cover = models.ImageField(upload_to=article_cover_upload_path, null=True, blank=True)
    md_file = models.FileField(upload_to=article_md_upload_path)
    tags = models.ManyToManyField("Tag", blank=True)
    like_count = models.PositiveIntegerField(default=0)
    is_draft = models.BooleanField(default=False, verbose_name="是否为草稿")
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)

            if not base_slug:
                base_slug = "article"

            slug = base_slug
            counter = 1

            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class WebSetting(models.Model):
    name = models.CharField(max_length=50)
    web_name = models.CharField(max_length=50)
    name_avatar = models.ImageField(upload_to=avatar_upload_path, null=True, blank=True)
    about_md = models.TextField(blank=True)
    footer_text1 = models.CharField(max_length=100, blank=True)
    footer_text2 = models.CharField(max_length=100, blank=True)

    updated_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.pk:
            old = WebSetting.objects.get(pk=self.pk)
            if old.name_avatar and old.name_avatar != self.name_avatar:
                old.name_avatar.delete(save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.web_name


class AdminAuditLog(models.Model):
    """管理员操作记录"""
    
    # 操作类型枚举
    ACTION_LOGIN = 'login'
    ACTION_LOGOUT = 'logout'
    ACTION_ARTICLE_CREATE = 'article_create'
    ACTION_ARTICLE_UPDATE = 'article_update'
    ACTION_ARTICLE_DELETE = 'article_delete'
    ACTION_TAG_CREATE = 'tag_create'
    ACTION_TAG_UPDATE = 'tag_update'
    ACTION_TAG_DELETE = 'tag_delete'
    ACTION_COMMENT_DELETE = 'comment_delete'
    ACTION_MESSAGE_DELETE = 'message_delete'
    ACTION_BANNEDWORD_CREATE = 'bannedword_create'
    ACTION_BANNEDWORD_DELETE = 'bannedword_delete'
    ACTION_WEBSETTING_UPDATE = 'websetting_update'
    ACTION_VISITOR_VIEW = 'visitor_view'
    ACTION_OTHER = 'other'
    
    ACTION_CHOICES = [
        (ACTION_LOGIN, '登录'),
        (ACTION_LOGOUT, '登出'),
        (ACTION_ARTICLE_CREATE, '创建文章'),
        (ACTION_ARTICLE_UPDATE, '更新文章'),
        (ACTION_ARTICLE_DELETE, '删除文章'),
        (ACTION_TAG_CREATE, '创建标签'),
        (ACTION_TAG_UPDATE, '更新标签'),
        (ACTION_TAG_DELETE, '删除标签'),
        (ACTION_COMMENT_DELETE, '删除评论'),
        (ACTION_MESSAGE_DELETE, '删除留言'),
        (ACTION_BANNEDWORD_CREATE, '添加违禁词'),
        (ACTION_BANNEDWORD_DELETE, '删除违禁词'),
        (ACTION_WEBSETTING_UPDATE, '更新网站设置'),
        (ACTION_VISITOR_VIEW, '查看访客统计'),
        (ACTION_OTHER, '其他操作'),
    ]
    
    # 操作结果
    RESULT_SUCCESS = 'success'
    RESULT_FAILURE = 'failure'
    RESULT_CHOICES = [
        (RESULT_SUCCESS, '成功'),
        (RESULT_FAILURE, '失败'),
    ]
    
    # 基本信息
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, verbose_name="操作管理员")
    action_time = models.DateTimeField(auto_now_add=True, verbose_name="操作时间")
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES, verbose_name="操作类型")
    action_result = models.CharField(max_length=20, choices=RESULT_CHOICES, verbose_name="操作结果")
    
    # 操作详情
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP地址")
    user_agent = models.TextField(null=True, blank=True, verbose_name="用户代理")
    
    # 操作对象信息
    target_model = models.CharField(max_length=100, null=True, blank=True, verbose_name="目标模型")
    target_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="目标ID")
    target_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="目标名称")
    
    # 操作详情（JSON格式，存储额外信息）
    details = models.JSONField(null=True, blank=True, verbose_name="操作详情")
    
    # 错误信息（如果操作失败）
    error_message = models.TextField(null=True, blank=True, verbose_name="错误信息")
    
    class Meta:
        verbose_name = "管理员操作记录"
        verbose_name_plural = "管理员操作记录"
        ordering = ['-action_time']
        indexes = [
            models.Index(fields=['action_time']),
            models.Index(fields=['user', 'action_time']),
            models.Index(fields=['action_type', 'action_time']),
            models.Index(fields=['action_result', 'action_time']),
        ]
    
    def __str__(self):
        return f"{self.user.username if self.user else '未知用户'} - {self.get_action_type_display()} - {self.get_action_result_display()} - {self.action_time.strftime('%Y-%m-%d %H:%M:%S')}"
