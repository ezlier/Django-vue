from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit
from .instrument import get_client_ip

from blog_api.v1.services.user.messageService import MessageService
from blog_api.v1.serializer.user.messageSerializer import MessageSerializer, CommentSerializer, aboutSerializer
from blog_api.v1.views.response import ApiResponse


@api_view(['GET'])
@ratelimit(key='ip', rate='10/m', block=True)
def getMessage(request):
    queryset = MessageService.getMessages()
    serializer = MessageSerializer(queryset, many=True)

    return ApiResponse.success(serializer.data)


@api_view(['POST'])
@ratelimit(key='ip', rate='10/m', block=True)
def pushMessage(request):
    serializer = MessageSerializer(data=request.data)

    if not serializer.is_valid():
        return ApiResponse.bad_request("发送失败", errors=serializer.errors)

    result = MessageService.createMessage(
        serializer.validated_data,
        get_client_ip(request)
    )

    if result["code"] == 200:
        return ApiResponse.success(msg="留言成功")
    return ApiResponse.error(result.get("msg", "发送失败"), result.get("code"))


@api_view(['GET'])
def getCommit(request, slug):
    queryset = MessageService.getCommit(slug)
    serializer = CommentSerializer(queryset, many=True)

    return ApiResponse.success(serializer.data)


@api_view(['POST'])
@ratelimit(key='ip', rate='10/m', block=True)
def createComment(request, slug):
    serializer = CommentSerializer(data=request.data)
    if not serializer.is_valid():
        return ApiResponse.bad_request("评论失败", errors=serializer.errors)
    result = MessageService.createComment(
        slug,
        serializer.validated_data,
        get_client_ip(request)
    )
    if result["code"] == 200:
        return ApiResponse.success(msg="评论成功")
    return ApiResponse.error(result.get("msg", "评论失败"), result.get("code"))


@api_view(['GET'])
def getWebSetting(request):
    obj = MessageService.getWebSetting()
    serializer = aboutSerializer(obj, context={'request': request})
    return ApiResponse.success(serializer.data)


@api_view(['GET'])
def getAboutText(request):
    html = MessageService.getAbout()
    return ApiResponse.success({"html": html})
