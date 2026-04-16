/**
 * 文章数据存储
 * 管理文章列表的全局状态
 */
import { defineStore } from "pinia"
import { getArticles2 } from "@/utils/article"

export const useArticleStore = defineStore("article", {
  state: () => ({
    articleList: [],
    articlesLength: 0,
    currentPage: 1,
    pageSize: 10
  }),

  actions: {
    async fetchArticles(page = 1, pageSize = 10) {
      this.currentPage = page
      this.pageSize = pageSize

      const res = await getArticles2({ page, page_size: pageSize })
      this.articleList = res.data.data.results
      this.articlesLength = res.data.data.count
    }
  }
})
