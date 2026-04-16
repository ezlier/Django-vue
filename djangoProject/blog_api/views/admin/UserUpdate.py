from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from blog_api.serializer.admin.UserUpdateSerializer import UserUpdateSerializer
from blog_api.views import ApiResponse


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def UserUpdate(request):
    serializer = UserUpdateSerializer(
        data=request.data,
        context={'request': request}
    )

    if serializer.is_valid():
        user = serializer.save()
        return ApiResponse.success({"username": user.username})

    return ApiResponse.error(serializer.errors)