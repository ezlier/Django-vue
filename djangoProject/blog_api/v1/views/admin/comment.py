from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

from blog_api.models import Comment
from blog_api.v1.serializer.admin.messageSerializer import adminCommentSerializer
from blog_api.v1.services.admin.messageService import MessageService
from blog_api.v1.views.response import ApiResponse
from blog_api.decorators import audit_comment_delete


@api_view(['GET'])
@permission_classes([IsAdminUser])
def adminComment(request):
    queryset = MessageService.adminGetComment()
    serializer = adminCommentSerializer(queryset, many=True)
    return ApiResponse.success(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
@audit_comment_delete
def deleteComment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return ApiResponse.success(msg="删除成功")
