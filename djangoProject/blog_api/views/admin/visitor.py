from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser

from blog_api.models import Visitor
from blog_api.views.response import ApiResponse
from blog_api.decorators import audit_visitor_view


@api_view(['GET'])
@permission_classes([IsAdminUser])
@audit_visitor_view
def visitor_stats(request):
    queryset = Visitor.objects.all().order_by("-visit_time").values("ip", "visit_time", "user_agent", "path")

    paginator = PageNumberPagination()
    paginator.page_size = 10

    page = paginator.paginate_queryset(queryset, request)

    return ApiResponse.success(paginator.get_paginated_response(page).data)