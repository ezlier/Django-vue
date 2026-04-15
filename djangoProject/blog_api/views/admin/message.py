from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

from blog_api.models import Message
from blog_api.serializer.admin.messageSerializer import adminMessageSerializer
from blog_api.services.admin.messageService import MessageService
from blog_api.views.response import ApiResponse
from blog_api.decorators import audit_message_delete


@api_view(['GET'])
@permission_classes([IsAdminUser])
def adminMessage(request):
    queryset = MessageService.adminGetMessage()
    serializer = adminMessageSerializer(queryset, many=True)
    return ApiResponse.success(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
@audit_message_delete
def deleteMessage(request, id):
    ID = get_object_or_404(Message, pk=id)
    ID.delete()
    return ApiResponse.success(msg="删除成功")