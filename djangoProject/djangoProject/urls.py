from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from blog_api import views

urlpatterns = [
    path('api/login/', views.login_view),
    path('api/admin_data/', views.admin_data),
    path('api/articles/', views.list_articles),
    path('api/articles/<path:slug>/', views.get_article),
    path('api/about/', views.get_about_text),
    path('api/websetting', views.get_websetting),
    path("api/visitor_stats/", views.visitor_stats),
    path('api/message/', views.get_message)
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])