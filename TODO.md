# 接口重构计划：RESTful 风格改造

## 通用约定

### HTTP 方法映射
| 方法 | 操作 | 响应状态码 |
|------|------|-----------|
| GET | 获取资源（无ID=列表，有ID=详情） | 200 |
| POST | 创建资源 | 201 |
| PUT | 全量更新资源 | 200 |
| PATCH | 部分更新资源 | 200 |
| DELETE | 删除资源 | 204 |

### 查询参数
- `page` / `page_size` - 分页
- `search` - 搜索关键词
- `ordering` - 排序字段（加 `-` 表示降序）
- 各资源特有筛选参数

### 请求/响应格式
- 请求：`application/json`
- 响应：统一使用 `ApiResponse` 封装
  ```json
  {
    "code": 200,
    "message": "success",
    "data": {}
  }
  ```

### 认证与权限
- 使用 JWT Token（`access` + `refresh`）
- 请求头：`Authorization: Bearer <access_token>`
- Admin 接口需 `IsAdminUser` 权限
- User 接口对外公开

### API 版本管理
- **v1**：保留旧的非 RESTful 接口，路径保持现状（如 `/api/admin/login/`），仅做维护不再新增功能
- **v2**：所有新 RESTful 接口统一使用 `/api/v2/` 前缀（如 `/api/v2/admin/article/`），本计划中所有接口均指 v2
- 过渡期 v1 和 v2 并行运行，前端逐步切换到 v2，确认稳定后下线 v1

---

## Admin 接口

| 方法 | 路由 | 说明 |
|------|------|------|
| POST | /api/v2/admin/login/ | 管理员登录 |
| GET/POST | /api/v2/admin/article/ | 文章列表/创建 |
| GET/PUT/DELETE | /api/v2/admin/article/{slug}/ | 文章详情/更新/删除 |
| POST | /api/v2/admin/article/upload/ | 上传 MD 文件创建文章 |
| PATCH | /api/v2/admin/article/{slug}/status/ | 更新文章状态（发布/下架） |
| DELETE | /api/v2/admin/article/ | 批量删除文章（body 传入 ids） |
| GET/POST | /api/v2/admin/tag/ | 标签列表/创建 |
| PUT/DELETE | /api/v2/admin/tag/{id}/ | 标签更新/删除 |
| GET | /api/v2/admin/comment/ | 评论管理列表 |
| DELETE | /api/v2/admin/comment/{pk}/ | 删除特定评论 |
| DELETE | /api/v2/admin/comment/ | 批量删除评论（body 传入 ids） |
| GET | /api/v2/admin/message/ | 留言管理列表 |
| DELETE | /api/v2/admin/message/{id}/ | 删除特定留言 |
| DELETE | /api/v2/admin/message/ | 批量删除留言（body 传入 ids） |
| GET | /api/v2/admin/websetting/settings/ | 网站设置查看 |
| PUT | /api/v2/admin/websetting/update/ | 网站设置更新 |
| GET/POST | /api/v2/admin/bannedword/ | 敏感词列表/添加 |
| DELETE | /api/v2/admin/bannedword/{id}/ | 删除敏感词 |
| DELETE | /api/v2/admin/bannedword/ | 批量删除敏感词（body 传入 ids） |
| GET | /api/v2/admin/audit/logs/ | 审计日志列表 |
| GET | /api/v2/admin/audit/statistics/ | 审计统计 |
| GET | /api/v2/admin/visitor-stats/ | 访客统计 |
| GET | /api/v2/admin/dashboard/ | 控制台数据 |
| PUT | /api/v2/admin/user/ | 更新当前用户信息 |

## User 接口

| 方法 | 路由 | 说明 |
|------|------|------|
| GET | /api/v2/user/article/ | 文章列表（公开，支持分页/搜索/排序） |
| GET | /api/v2/user/article/{slug}/ | 文章详情 |
| GET | /api/v2/user/tag/ | 标签列表 |
| GET | /api/v2/user/article/{slug}/comment/ | 文章评论列表 |
| POST | /api/v2/user/article/{slug}/comment/ | 发表评论 |
| GET | /api/v2/user/message/ | 留言列表 |
| POST | /api/v2/user/message/ | 发布留言 |
| GET | /api/v2/user/websetting/ | 获取网站配置 |
| GET | /api/v2/user/about/ | 关于页信息 |

---

## 批量操作规范

```
# 批量删除：使用 DELETE 请求，body 传入 id 列表
DELETE /api/v2/admin/article/    body: {"ids": [1, 2, 3]}
DELETE /api/v2/admin/comment/    body: {"ids": [1, 2, 3]}
DELETE /api/v2/admin/message/    body: {"ids": [1, 2, 3]}
DELETE /api/v2/admin/bannedword/ body: {"ids": [1, 2, 3]}

# 单个删除
DELETE /api/v2/admin/article/{slug}/
DELETE /api/v2/admin/comment/{id}/
DELETE /api/v2/admin/message/{id}/
DELETE /api/v2/admin/bannedword/{id}/
```

---

## 代码架构重构

### 现状
- **Views**：全部使用函数视图 `@api_view`，分页/校验逻辑在每个视图重复
- **Services**：类 + `@staticmethod`，实质是命名空间包装的过程式代码，无状态、不可测试
- **Serializers**：部分使用 `serializers.Serializer` 而非 `ModelSerializer`，且存在直接调用 Service 的耦合

### Views：函数视图 → 类视图
| 重构项 | 当前写法 | 目标写法 |
|--------|---------|---------|
| 列表/详情 | `@api_view(['GET'])` 两个独立函数 | `ListAPIView` + `RetrieveAPIView` 或 `ModelViewSet` |
| 创建 | `@api_view(['POST'])` + 手动校验 | `CreateAPIView` + `serializer_class` |
| 更新 | `@api_view(['PUT'])` + 手动查对象 | `UpdateAPIView` / `GenericAPIView` + `get_object()` |
| 删除 | `@api_view(['DELETE'])` + 手动查对象 | `DestroyAPIView` |
| 分页 | 每个视图手动 `PageNumberPagination` | 在 `settings.py` 配置全局分页类 |

**优势**：
- DRF 内置 `get_queryset()`、`get_object()`、`get_serializer()` 消除重复代码
- ViewSet + Router 自动生成路由，减少 `urls.py` 配置
- `permission_classes` / `authentication_classes` 在类属性中统一声明
- Mixin 组合复用逻辑（如日志记录、缓存）

### Services：@staticmethod → 实例方法 + 依赖注入
| 重构项 | 当前写法 | 目标写法 |
|--------|---------|---------|
| 方法定义 | `@staticmethod` 所有方法 | 实例方法 `def xxx(self, ...)` |
| 依赖 | 硬编码 `Model.objects` | 构造函数注入 `__init__(self, queryset=None)` |
| 测试 | 无法 Mock，必须连数据库 | 可注入 Mock 对象，纯单元测试 |

**示例对比**：
```python
# 当前：伪类
class ArticleService:
    @staticmethod
    def uploadArticle(data):
        article = Article.objects.create(...)
        return article

# 目标：真正的类
class ArticleService:
    def __init__(self, article_repo=None):
        self.repo = article_repo or Article.objects

    def upload(self, data):
        article = self.repo.create(**data)
        return article
```

### Serializers：统一规范与解耦
| 重构项 | 当前问题 | 目标 |
|--------|---------|------|
| 基类 | `ArticleCreateSerializer` 用 `Serializer` 手写 create | 统一用 `ModelSerializer`，自动生成 create/update |
| 耦合 | Serializer 直接 `import ArticleService` 并调用 | Serializer 只做校验，业务逻辑放 Service/View |
| 校验 | 部分 validator 散落在各 Serializer 中 | 提取公共 validator 到 `validators.py` |
| 字段定义 | 显式列出 fields | 用 `exclude` 或 `fields = '__all__'` 精简 |

---

## 阶段性任务

### 第一阶段：URL 重构
- [x] 统一 URL 命名风格（下划线 → 中划线）
- [x] 拆分 `urls.py` 为 `api_admin.py` 和 `api_user.py`，分模块管理
- [x] 新增 `/api/v2/` 前缀，v2 所有路由挂载在 v2 子路径下；v1 路由保持不变
- [x] 使用 DRF `DefaultRouter` 或 `SimpleRouter` 简化 v2 路由注册

### 第二阶段：视图与服务重构（函数 → 类）
- [x] Views 函数视图 → DRF 类视图（`ListAPIView` / `CreateAPIView` / `ModelViewSet`）
- [x] Services `@staticmethod` → 实例方法 + 构造函数注入依赖
- [x] 统一使用 DRF Serializer 做参数校验
- [x] 统一响应格式（全部走 `ApiResponse`）
- [x] 明确区分 admin 和 user 的权限控制
- [x] 全局分页配置移至 `settings.py`，消除每个视图的重复分页代码

### 第三阶段：Serializer 优化与解耦
- [x] `serializers.Serializer` → `ModelSerializer`，利用 DRF 自动生成 create/update
- [x] Serializer 只做校验和序列化，移除业务逻辑调用 Service 的耦合
- [x] 提取公共 validator 到 `validators.py`
- [x] 精简 fields 定义（`fields = '__all__'` 或 `exclude`）

### 第四阶段：功能完善
- [x] 完善排序、搜索功能
- [x] 补充嵌套路由（评论作为文章的子资源）
- [x] 补充批量操作接口（article/comment/message/bannedword 的 batch-delete）
- [x] ViewSet + Router 自动生成路由，减少手动配置
- [x] 补充错误处理中间件，捕获全局异常

### 第五阶段：v1 → v2 迁移与验证
- [ ] 前端接口调用逐步从 v1 切换到 v2，v1 和 v2 并行运行
- [ ] v2 接口全量测试（单元测试 + 集成测试）
- [ ] 确认前端所有调用已迁移完毕、线上无 v1 流量后，下线 v1 旧接口
- [ ] 清理 v1 相关代码
