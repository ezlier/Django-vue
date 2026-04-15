from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from blog_api import views

urlpatterns = [
    path('api/login/', views.loginView),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/updateUser/', views.UserUpdate),

    path('api/get_articles/', views.getArticles),
    path('api/articles/<path:slug>/', views.getArticle),
    path('api/updateArticle/<path:slug>/', views.updateArticle),
    path('api/uploadArticles/', views.uploadArticle),
    path('api/CreateArticle/', views.createArticle),
    path('api/deleteArticles/<int:pk>/', views.deleteArticle),

    path('api/admin/articles/', views.adminGetArticles),
    path('api/admin/articles/<int:pk>/status/', views.updateArticleStatus),
    path('api/admin/articles/<path:slug>/', views.adminGetArticle),
    
    path('api/getTags/', views.getTags),
    path('api/updateTag/<int:id>/', views.updateTag),
    path('api/deleteTag/<int:id>/', views.deleteTag),

    path('api/articles_comment/<str:slug>/', views.getCommit),
    path('api/create_comment/<str:slug>/', views.createComment),
    path('api/admin_comment/', views.adminComment),
    path('api/comment/<int:pk>/', views.deleteComment),

    path('api/message/', views.getMessage),
    path('api/create_message/', views.pushMessage),
    path('api/admin_message/', views.adminMessage),
    path('api/delete_message/<int:id>/', views.deleteMessage),

    path('api/about/', views.getAboutText),
    path('api/get_websetting', views.getWebSetting),
    path("api/visitor_stats/", views.visitor_stats),


    path('api/bannedwords/', views.bannedwordsSetting),
    path('api/create_bannedword/', views.createBannedword),
    path('api/delete_bannedword/<int:id>/', views.deleteBannedword),


    path('api/admin_websetting', views.adminWebsetting),
    path('api/admin_audit/logs/', views.get_admin_audit_logs),
    path('api/admin_audit/export/', views.export_admin_audit_logs),
    path('api/admin_audit/statistics/', views.get_admin_audit_statistics),
    path('api/admin_data/', views.adminData),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)