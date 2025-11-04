from django.db import models


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


class Bannedwords(models.Model):
    word = models.TextField()