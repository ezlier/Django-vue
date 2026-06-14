# v2 接口
总览如下：

## Admin (前缀 /api/v2/admin/)
  POST   /login/             管理员登录
  GET    /article/           文章列表
  POST   /article/           表单创建文章
  POST   /article/upload/    MD 文件上传创建
  GET    /article/{slug}/    文章详情
  PUT    /article/{slug}/    更新文章
  DELETE /article/{slug}/    删除文章
  PATCH  /article/{slug}/status/  发布/下架
  DELETE /article/batch-delete/   批量删除
  GET    /tag/               标签列表
  POST   /tag/               创建标签
  PUT    /tag/{id}/          更新标签
  DELETE /tag/{id}/          删除标签
  GET    /comment/           评论列表
  DELETE /comment/{pk}/      删除评论
  DELETE /comment/batch-delete/   批量删除评论
  GET    /message/           留言列表
  DELETE /message/{pk}/      删除留言
  DELETE /message/batch-delete/   批量删除留言
  GET    /bannedword/        敏感词列表
  POST   /bannedword/        添加敏感词
  DELETE /bannedword/{pk}/   删除敏感词
  DELETE /bannedword/batch-delete/ 批量删除
  GET    /websetting/settings/  查看配置
  PUT    /websetting/update/    更新配置
  GET    /visitor-stats/     访客统计
  GET    /audit/logs/        审计日志
  GET    /audit/statistics/  审计统计
  GET    /dashboard/         控制台
  PUT    /user/              更新用户

## User (前缀 /api/v2/user/)
  GET    /article/           文章列表
  GET    /article/{slug}/    文章详情
  GET    /article/tag/       标签列表
  GET    /article/{slug}/comment/  评论列表
  POST   /article/{slug}/comment/  发表评论
  GET    /message/           留言列表
  POST   /message/           发布留言
  GET    /websetting/        网站配置
  GET    /about/             关于页
