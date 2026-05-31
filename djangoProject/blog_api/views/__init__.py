# 向后兼容：所有 v1 views 已迁移到 blog_api.v1.views
# 此处仅做 re-export，v1 路由和旧代码仍可通过 blog_api.views 访问
from blog_api.v1.views.user.auth import *
from blog_api.v1.views.user.articles import *
from blog_api.v1.views.user.message import *
from blog_api.v1.views.admin.admin_init import *
from blog_api.v1.views.admin.article import *
from blog_api.v1.views.admin.bannedwords import *
from blog_api.v1.views.admin.comment import *
from blog_api.v1.views.admin.message import *
from blog_api.v1.views.admin.tag import *
from blog_api.v1.views.admin.visitor import *
from blog_api.v1.views.admin.websetting import *
from blog_api.v1.views.admin.audit import *
from blog_api.v1.views.admin.UserUpdate import *
