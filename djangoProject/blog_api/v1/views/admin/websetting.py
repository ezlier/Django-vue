from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

from blog_api.models import WebSetting
from blog_api.v1.serializer.admin.messageSerializer import WebSettingSerializer
from blog_api.v1.views.response import ApiResponse
from blog_api.decorators import audit_websetting_update


@api_view(['PUT'])
@permission_classes([IsAdminUser])
@audit_websetting_update
def adminWebsetting(request):
    instance = WebSetting.objects.first()

    if not instance:
        return ApiResponse.not_found("WebSetting not found")

    serializer = WebSettingSerializer(instance, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return ApiResponse.success(serializer.data, msg="更新成功")

    return ApiResponse.bad_request("更新失败", errors=serializer.errors)
