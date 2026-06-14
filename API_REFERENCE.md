# 当前 v2 API 接口清单

项目已完成 Phase 1-4 重构：v1 代码迁移至 `v1/`，v2 采用 ModelViewSet + Router + 实例化 Service + ModelSerializer。

## Admin 接口 (前缀 `/api/v2/admin/`)
| 方法 | 路由 | 说明 |
|------|------|------|
| POST | /login/ | 管理员登录 (公开) |
| GET | /article/ | 文章列表 (分页、搜索、草稿筛选) |
| POST | /article/ | 表单创建文章 |
| POST | /article/upload/ | MD 文件上传创建 |
| GET | /article/{slug}/ | 文章详情 (含正文) |
| PUT/PATCH | /article/{slug}/ | 文章更新 |
| DELETE | /article/{slug}/ | 删除文章 |
| PATCH | /article/{slug}/status/ | 发布/下架 |
| DELETE | /article/batch-delete/ | 批量删除文章 (body: ids) |
| GET | /tag/ | 标签列表 |
| POST | /tag/ | 创建标签 |
| PUT/PATCH | /tag/{id}/ | 更新标签 |
| DELETE | /tag/{id}/ | 删除标签 |
| GET | /comment/ | 评论管理列表 |
| DELETE | /comment/{pk}/ | 删除评论 |
| DELETE | /comment/batch-delete/ | 批量删除评论 (body: ids) |
| GET | /message/ | 留言管理列表 |
| DELETE | /message/{pk}/ | 删除留言 |
| DELETE | /message/batch-delete/ | 批量删除留言 (body: ids) |
| GET | /bannedword/ | 敏感词列表 |
| POST | /bannedword/ | 添加敏感词 |
| DELETE | /bannedword/{pk}/ | 删除敏感词 |
| DELETE | /bannedword/batch-delete/ | 批量删除敏感词 (body: ids) |
| GET | /websetting/settings/ | 网站设置查看 |
| PUT | /websetting/update/ | 网站设置更新 |
| GET | /visitor-stats/ | 访客统计 (分页) |
| GET | /audit/logs/ | 审计日志 (筛选/分页) |
| GET | /audit/statistics/ | 审计统计 |
| GET | /dashboard/ | 控制台欢迎页 |
| PUT | /user/ | 更新当前用户 (用户名/密码) |

## User 接口 (前缀 `/api/v2/user/`)
| 方法 | 路由 | 说明 |
|------|------|------|
| GET | /article/ | 公开文章列表 (分页) |
| GET | /article/{slug}/ | 文章详情 (Markdown 内容) |
| GET | /article/{slug}/comment/ | 文章评论列表 |
| POST | /article/{slug}/comment/ | 发表评论 (含违禁词检测) |
| GET | /message/ | 留言列表 |
| POST | /message/ | 发布留言 (含违禁词检测) |
| GET | /article/tag/ | 标签列表 |
| GET | /websetting/ | 网站配置 |
| GET | /about/ | 关于页 (Markdown 渲染为 HTML) |
