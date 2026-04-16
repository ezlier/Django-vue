# 前端项目文档

## 项目概述

这是一个基于 Vue 3 + Vite 开发的前端项目，主要用于文章管理系统，包含文章发布、编辑、评论、标签管理等功能。项目采用现代化的前端技术栈，具有良好的用户体验和响应式设计。

## 核心功能

- **文章管理**：发布、编辑、删除文章，支持 Markdown 格式
- **评论系统**：支持文章评论，管理员可管理评论
- **标签管理**：文章标签的增删改查
- **用户认证**：登录功能
- **后台管理**：管理员后台，可管理文章、评论、标签等
- **主题切换**：支持浅色/深色模式
- **响应式设计**：适配不同屏幕尺寸
- **上传功能**：支持文章封面和 Markdown 文件上传

## 技术栈

### 前端框架
- Vue 3 (Composition API)
- Vue Router
- Pinia (状态管理)

### UI 组件库
- Element Plus
- md-editor-v3 (Markdown 编辑器)

### 工具库
- Axios (网络请求)
- Markdown-it (Markdown 解析)
- Highlight.js (代码高亮)

### 构建工具
- Vite
- ES6+

## 环境配置要求

- Node.js: ^20.19.0 || >=22.12.0
- npm: >=9.0.0
- 浏览器: Chrome, Firefox, Edge 等现代浏览器

## 安装步骤

### 1. 克隆项目

```bash
git clone <项目仓库地址>
cd frontend
```

### 2. 安装依赖

```bash
npm install
```

### 3. 配置环境变量

在 `.env.development` 文件中配置开发环境变量：

```env
# 开发环境配置
VITE_API_BASE_URL=/api
```

### 4. 启动开发服务器

```bash
npm run dev
```

### 5. 构建生产版本

```bash
npm run build
```

### 6. 预览生产构建

```bash
npm run preview
```

## 使用指南

### 访问项目

开发环境：`http://localhost:5173`

生产环境：根据部署服务器地址访问

### 功能使用

#### 前台功能
- **首页**：浏览文章列表
- **文章详情**：查看文章内容和评论
- **关于页**：查看网站信息和留言板
- **主题切换**：点击顶部导航栏的主题切换按钮

#### 后台功能
- **登录**：访问 `/login` 页面登录
- **文章管理**：创建、编辑、删除文章
- **评论管理**：查看和管理评论
- **标签管理**：添加、编辑、删除标签
- **网站设置**：配置网站基本信息

### 上传文章

1. 登录后台管理系统
2. 点击「发布新文章」
3. 填写文章标题和标签
4. 上传文章封面（可选）
5. 上传 Markdown 文件
6. 点击「立即发布」按钮

## API 接口文档

### 文章相关接口

#### 获取文章列表
- **URL**: `/api/get_articles/`
- **方法**: GET
- **参数**: `page` (页码), `limit` (每页数量)
- **返回**: 文章列表数据

#### 获取单篇文章
- **URL**: `/api/articles/{slug}/`
- **方法**: GET
- **返回**: 文章详情数据

#### 上传文章
- **URL**: `/api/uploadArticles/`
- **方法**: POST
- **参数**: `title` (标题), `tags` (标签), `md_file` (Markdown 文件), `cover` (封面图片)
- **返回**: 上传结果

#### 更新文章
- **URL**: `/api/updateArticle/{slug}/`
- **方法**: PUT
- **参数**: `title` (标题), `tags` (标签), `md_file` (Markdown 文件), `cover` (封面图片)
- **返回**: 更新结果

#### 删除文章
- **URL**: `/api/deleteArticles/{id}/`
- **方法**: DELETE
- **返回**: 删除结果

### 标签相关接口

#### 获取标签列表
- **URL**: `/api/getTags/`
- **方法**: GET
- **返回**: 标签列表

#### 更新标签
- **URL**: `/api/updateTag/{id}/`
- **方法**: PUT
- **参数**: `name` (标签名称)
- **返回**: 更新结果

#### 删除标签
- **URL**: `/api/deleteTag/{id}/`
- **方法**: DELETE
- **返回**: 删除结果

### 认证相关接口

#### 登录
- **URL**: `/api/token/`
- **方法**: POST
- **参数**: `username` (用户名), `password` (密码)
- **返回**: token 数据

#### 刷新 token
- **URL**: `/api/token/refresh/`
- **方法**: POST
- **参数**: `refresh` (refresh token)
- **返回**: 新的 access token

## 项目结构

```
frontend/
├── public/              # 静态资源
├── src/
│   ├── assets/          # 资源文件
│   │   ├── fonts/       # 字体文件
│   │   ├── img/         # 图片文件
│   │   ├── base.css     # 基础样式
│   │   └── main.css     # 主样式
│   ├── components/      # 通用组件
│   ├── router/          # 路由配置
│   ├── stores/          # 状态管理
│   ├── utils/           # 工具函数
│   ├── views/           # 页面组件
│   │   ├── Admin/       # 后台管理
│   │   ├── Home/        # 首页
│   │   ├── Post/        # 文章详情
│   │   └── Layout/      # 布局组件
│   ├── App.vue          # 根组件
│   └── main.js          # 入口文件
├── .env.development     # 开发环境配置
├── .gitignore           # Git 忽略文件
├── Dockerfile           # Docker 配置
├── index.html           # HTML 模板
├── package.json         # 项目配置
└── vite.config.js       # Vite 配置
```

