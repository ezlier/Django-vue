from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

from blog_api.models import Bannedwords
from blog_api.v1.serializer.admin.adminSerializer import bannedSerializer
from blog_api.v1.services.admin.adminService import adminService
from blog_api.v1.views.response import ApiResponse
from blog_api.decorators import audit_bannedword_create, audit_bannedword_delete


@api_view(['GET'])
@permission_classes([IsAdminUser])
def bannedwordsSetting(request):
    word = adminService.get_bannedword()
    return ApiResponse.success(word)


@api_view(['POST'])
@permission_classes([IsAdminUser])
@audit_bannedword_create
def createBannedword(request):
    serializer = bannedSerializer(data=request.data)
    if not serializer.is_valid():
        return ApiResponse.bad_request("创建失败", errors=serializer.errors)
    result = adminService.create_bannedword(serializer.validated_data)
    if result["code"] == 200:
        return ApiResponse.success(msg="创建成功")
    return ApiResponse.error(result.get("msg", "创建失败"))


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
@audit_bannedword_delete
def deleteBannedword(request, id):
    ID = get_object_or_404(Bannedwords, pk=id)
    ID.delete()
    return ApiResponse.success(msg="删除成功")
