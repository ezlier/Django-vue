from datetime import timedelta

from django.utils.html import escape
from django.utils import timezone

from blog_api.models import Visitor


def record_visitor(request):
    ip = get_client_ip(request)
    path = request.path
    user_agent = escape(request.META.get("HTTP_USER_AGENT", "")[:256])
    now = timezone.now()

    # 查找该IP在最近30分钟是否访问过
    recent_visit = Visitor.objects.filter(ip=ip, path=path, visit_time__gte=now - timedelta(minutes=30)).exists()
    if not recent_visit:
        Visitor.objects.create(ip=ip, path=path, user_agent=user_agent)



def get_client_ip(request):
    """获取真实客户端IP"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
