from datetime import timedelta
from django.utils import timezone
from .models import Visitor

class VisitorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # 只记录 GET 请求（避免 POST / admin 等污染）
        if request.method == "GET":
            self.record_visitor(request)

        return response

    def record_visitor(self, request):
        ip = self.get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")

        # 排除管理后台和静态文件的请求
        if request.path.startswith("/admin") or request.path.startswith("/static"):
            return

        now = timezone.now()
        ten_minutes_ago = now - timedelta(minutes=10)

        # 查找过去 10 分钟内是否已经有该 IP 的记录
        exists = Visitor.objects.filter(
            ip=ip,
            visit_time__gte=ten_minutes_ago
        ).exists()

        if not exists:
            # 如果没有记录，则创建一条新记录
            Visitor.objects.create(
                ip=ip,
                path=request.path,  # 记录访问的路径
                user_agent=user_agent,
                visit_time=now
            )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")