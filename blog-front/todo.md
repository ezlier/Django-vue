# 接口

**Admin 接口**（需认证或管理员权限，前缀 `/api/v2/admin/`）

| 方法   | 路由                      | 说明                                               | 权限            |
| ------ | ------------------------- | -------------------------------------------------- | --------------- |
| POST   | /login/                   | 管理员登录（返回 token + refresh）                 | 公开            |
| GET    | /article/                 | 文章列表（支持 search, is_draft, page, page_size） | IsAdminUser     |
| POST   | /article/                 | 表单创建文章（title + mdfile + tags + cover）      | IsAdminUser     |
| POST   | /article/upload/          | MD 文件上传创建                                    | IsAuthenticated |
| GET    | /article/{slug}/          | 文章详情（含正文内容）                             | IsAuthenticated |
| PUT    | /article/{slug}/          | 全量更新文章                                       | IsAuthenticated |
| PATCH  | /article/{slug}/          | 部分更新文章                                       | IsAuthenticated |
| DELETE | /article/{slug}/          | 删除单篇文章                                       | IsAuthenticated |
| PATCH  | /article/{slug}/status/   | 更新发布状态（草稿/已发布）                        | IsAuthenticated |
| DELETE | /article/batch-delete/    | 批量删除文章                                       | IsAuthenticated |
| GET    | /tag/                     | 标签列表                                           | IsAuthenticated |
| POST   | /tag/                     | 创建标签                                           | IsAuthenticated |
| GET    | /tag/{id}/                | 标签详情                                           | IsAuthenticated |
| PUT    | /tag/{id}/                | 更新标签                                           | IsAuthenticated |
| DELETE | /tag/{id}/                | 删除标签                                           | IsAuthenticated |
| GET    | /comment/                 | 评论管理列表                                       | IsAdminUser     |
| DELETE | /comment/{pk}/            | 删除单条评论                                       | IsAdminUser     |
| DELETE | /comment/batch-delete/    | 批量删除评论                                       | IsAdminUser     |
| GET    | /message/                 | 留言管理列表                                       | IsAdminUser     |
| DELETE | /message/{pk}/            | 删除单条留言                                       | IsAdminUser     |
| DELETE | /message/batch-delete/    | 批量删除留言                                       | IsAdminUser     |
| GET    | /bannedword/              | 敏感词列表                                         | IsAdminUser     |
| POST   | /bannedword/              | 添加敏感词                                         | IsAdminUser     |
| DELETE | /bannedword/{pk}/         | 删除单个敏感词                                     | IsAdminUser     |
| DELETE | /bannedword/batch-delete/ | 批量删除敏感词                                     | IsAdminUser     |
| GET    | /websetting/settings/     | 网站设置查看                                       | IsAdminUser     |
| PUT    | /websetting/update/       | 网站设置更新                                       | IsAdminUser     |
| GET    | /visitor-stats/           | 访客统计（分页）                                   | IsAdminUser     |
| GET    | /audit/logs/              | 审计日志列表（支持多种筛选）                       | IsAdminUser     |
| GET    | /audit/statistics/        | 审计统计                                           | IsAdminUser     |
| GET    | /dashboard/               | 控制台欢迎信息                                     | IsAdminUser     |
| PUT    | /user/                    | 更新当前用户（用户名/密码）                        | IsAdminUser     |

------

**User 公开接口**（无需认证，前缀 `/api/v2/user/`）

| 方法 | 路由                     | 说明                     |
| ---- | ------------------------ | ------------------------ |
| GET  | /article/                | 已发布文章列表（分页）   |
| GET  | /article/{slug}/         | 文章详情（含正文）       |
| GET  | /article/tag/            | 标签列表（含文章计数）   |
| GET  | /article/{slug}/comment/ | 文章评论列表             |
| POST | /article/{slug}/comment/ | 发表评论（含违禁词检测） |
| GET  | /message/                | 留言列表                 |
| POST | /message/                | 发布留言（含违禁词检测） |
| GET  | /websetting/             | 网站公开配置             |
| GET  | /about/                  | 关于页 HTML              |

------

**Token 刷新**

| 方法 | 路由                   | 说明              |
| ---- | ---------------------- | ----------------- |
| POST | /api/v2/token/refresh/ | 刷新 access token |

-------------------

# 博客结构

## 项目目录

```
src/

api/
assets/
components/
composables/
layouts/
router/
stores/
utils/
views/

App.vue
main.js
```

目录职责：

```
api
负责接口请求

components
复用组件

views
页面

layouts
布局

stores
状态管理

composables
逻辑复用

utils
工具函数

router
路由
```

# 页面结构

## 前台/

```
首页
文章详情
归档
关于
```

实际路由：

```
/home
/article/:id
/archive
/about
```

## 后台admin

包含：

```
仪表盘
文章管理
文章编辑
评论管理
留言管理
分类管理
标签管理
用户管理
网站设置
```

实际路由：

```
/admin/dashboard
/admin/articles
/admin/article/edit/:id?
/admin/comments
/admin/message
/admin/tags
/admin/users
/admin/settings
```

## 登录页面

路由：

```
/login
```

# 布局设计

## FrontLayout

结构：

```
Navbar

Header(100vh)

sidebar|RouterView

Footer
```

负责：

- 导航
- 页面切换
- 全局主题

## AdminLayout

结构：

```
Sidebar

Navbar|RouterView
```

负责：

- 后台导航
- 权限校验

# 性能设计

优化：

```
路由懒加载

图片懒加载

keep-alive

分页加载

组件按需加载
```

缓存：

```
文章缓存

配置缓存
```