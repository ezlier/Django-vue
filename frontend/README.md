# Blog 前端

按 TODO.md 规划完成：api 层、路由、状态管理、布局组件。

## 目录结构
```
src/
├── api/                # 接口封装
│   ├── request.ts      # axios 实例 + token 拦截器
│   ├── auth.ts         # 登录 / Token 刷新 / 用户更新
│   ├── admin.ts        # Admin 全套接口
│   └── user.ts         # User 公开接口
├── layouts/
│   ├── FrontLayout.vue # 前台布局 (Navbar + RouterView + Footer)
│   └── AdminLayout.vue # 后台布局 (Sidebar + Topbar + RouterView)
├── router/
│   ├── routes.ts       # 路由配置 (懒加载，前后台分离)
│   └── index.ts        # 路由实例 + 全局鉴权守卫
├── stores/
│   ├── auth.ts         # 认证 (login/logout/updateUser)
│   ├── article.ts      # 文章 + 标签
│   ├── tag.ts          # Admin 标签 CRUD
│   └── ui.ts           # 主题 / 侧栏 / 网站配置
├── types/
│   └── index.ts        # 通用类型定义
└── views/              # 页面 (占位，待填充)
```
