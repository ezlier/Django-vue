"""
v2 全局异常处理中间件

截获所有未处理的异常，统一转为 ApiResponse 的 error 格式（code 500）。
DRF 层面 ValidationError / NotFound / PermissionDenied 等不经过此中间件，
由 DRF 自己的 exception_handler 处理。
"""
import logging
import traceback

from django.http import JsonResponse

logger = logging.getLogger(__name__)


class GlobalExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception as e:
            logger.error(
                f"Unhandled exception on {request.method} {request.path}: {e}\n"
                f"{traceback.format_exc()}"
            )
            return JsonResponse(
                {"code": 500, "msg": "服务器内部错误"},
                status=500,
            )
