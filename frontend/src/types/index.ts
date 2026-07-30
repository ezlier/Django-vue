// 文章相关类型
export interface Article {
  id: number
  title: string
  slug: string
  cover: string | null
  content?: string
  tags: Tag[]
  like_count: number
  is_draft?: boolean
  created_time: string
  updated_time: string
}

export interface Tag {
  id: number
  name: string
  article_count?: number
}

// 评论
export interface Comment {
  id: number
  name: string
  text: string
  time: string
  QQ?: string
  email?: string
}

// 留言
export interface Message {
  id: number
  name: string
  text: string
  time: string
  QQ?: string
  email?: string
}

// 网站设置
export interface WebSetting {
  name: string
  web_name: string
  name_avatar: string | null
  about_md: string
  footer_text1: string
  footer_text2: string
  updated_time: string
}

// ApiResponse 通用响应
export interface ApiResponse<T = any> {
  code: number
  msg: string
  data: T
}
