from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from blog_api.models import Tag
from blog_api.services.admin.articleService import TagService
from blog_api.views.response import ApiResponse
from blog_api.decorators import audit_tag_update, audit_tag_delete


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@audit_tag_update
def updateTag(request, id):
    TagService.renameTag(id, request.data['name'])
    return ApiResponse.success(msg="更新成功")


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@audit_tag_delete
def deleteTag(request, id):
    tag = get_object_or_404(Tag, pk=id)
    tag.delete()
    return ApiResponse.success(msg="删除成功")