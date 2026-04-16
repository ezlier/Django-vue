from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import os

from .models import WebSetting

User = get_user_model()


@receiver(post_migrate)
def create_default_websetting(sender, **kwargs):
    if not WebSetting.objects.exists():
        WebSetting.objects.create(
            name="默认名字",
            web_name="我的博客",
            name_avatar="about/avatar.jpg",
            about_md='默认默认',
            updated_time=now(),
            footer_text1="Powered by Django",
            footer_text2="© 2026"
        )


@receiver(post_migrate)
def create_default_admin_user(sender, **kwargs):
    """创建默认管理员用户（仅当系统中没有任何用户时）"""
    
    # 检查是否已经有用户存在
    if User.objects.exists():
        return
    
    # 从环境变量获取初始密码，或使用默认强密码
    # 注意：在生产环境中，应该通过环境变量设置安全的初始密码
    default_password = os.environ.get('DEFAULT_ADMIN_PASSWORD', '123456')
    
    try:
        # 创建超级管理员用户
        admin_user = User.objects.create(
            username='admin',
            email='admin@example.com',
            password=make_password(default_password),
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        
        print(f"默认管理员用户创建成功")
        print(f"用户名: admin")
        print(f"初始密码: {default_password}")
        print("警告：请立即登录并修改密码！")
        
            
    except Exception as e:
        print(f"创建默认管理员用户失败: {e}")