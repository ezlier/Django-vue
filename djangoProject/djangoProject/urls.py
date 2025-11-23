from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from blog_api import views

urlpatterns = [
    path('api/login/', views.login_view),
    path('api/articles/', views.list_articles),
    path('api/articles/<path:slug>/', views.get_article),
    path('api/articles_comment/<str:slug>/', views.get_commit),
    path('api/about/', views.get_about_text),
    path('api/get_websetting', views.getwebsetting),
    path("api/visitor_stats/", views.visitor_stats),
    path('api/message/', views.get_message),
    path('api/bannedwords/', views.bannedwords_setting),
    path('api/get_csrf/', views.get_csrf),
    path('api/admin_articles/', views.admin_articles),
    path('api/admin_message/', views.admin_message),
    path('api/admin_websetting', views.admin_websetting),
    path('api/admin_data/', views.admin_data),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])