from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from blog_api.views.response import ApiResponse
from .visitor import visitor_stats
from .bannedwords import bannedwordsSetting, createBannedword, deleteBannedword
from .message import adminMessage, deleteMessage
from .websetting import adminWebsetting
from .comment import adminComment, deleteComment
from .article import uploadArticle, deleteArticle, createArticle, updateArticle, adminGetArticles, adminGetArticle, updateArticleStatus
from .tag import updateTag, deleteTag


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def adminData(request):
    return ApiResponse.success(msg=f"Welcome, {request.user.username}!")


# 导出所有函数，保持与原admin.py相同的接口
__all__ = [
    'visitor_stats',
    'bannedwordsSetting',
    'createBannedword',
    'deleteBannedword',
    'adminMessage',
    'deleteMessage',
    'adminWebsetting',
    'adminData',
    'adminComment',
    'deleteComment',
    'uploadArticle',
    'deleteArticle',
    'createArticle',
    'updateArticle',
    'adminGetArticles',
    'adminGetArticle',
    'updateArticleStatus',
    'updateTag',
    'deleteTag'
]