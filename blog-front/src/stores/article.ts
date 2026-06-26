import { defineStore } from "pinia";
import { ref } from "vue";
import { getArticles, getArticle, getTags } from "@/api/user";

export const useArticleStore = defineStore("article", () => {
  const articles = ref<Article[]>([]);
  const articleList = ref<Article[]>([]);
  const currentArticle = ref<Article | null>(null);
  const tags = ref<Tag[]>([]);
  const total = ref(0);
  const loading = ref(false);

  async function fetchArticles(page = 1, pageSize = 10) {
    loading.value = true;
    try {
      const res = await getArticles({ page, page_size: pageSize });
      const responseData = res.data;
      // ApiResponse 格式: { code, msg, data: { results, count } }
      // 部分接口直接返回 data 本身
      const payload = responseData.data || responseData;
      articles.value = payload.results || payload;
      total.value = payload.count || payload.length || 0;
    } finally {
      loading.value = false;
    }
  }

  async function fetchArticle(slug: string) {
    const res = await getArticle(slug);
    currentArticle.value = res.data.data;
    return currentArticle.value;
  }

  async function fetchAllArticles() {
    loading.value = true;
    try {
      const res = await getArticles({ page: 1, page_size: 9999 });
      const responseData = res.data;
      const payload = responseData.data || responseData;
      articleList.value = payload.results || payload;
      total.value = payload.count || payload.length || 0;
    } finally {
      loading.value = false;
    }
  }

  async function fetchTags() {
    const res = await getTags();
    tags.value = res.data.data;
  }

  return {
    articles,
    currentArticle,
    tags,
    total,
    loading,
    articleList,
    fetchArticles,
    fetchArticle,
    fetchTags,
    fetchAllArticles,
  };
});

export interface Article {
  id: number;
  title: string;
  slug: string;
  cover: string | null;
  content?: string;
  tags: Tag[];
  like_count: number;
  created_time: string;
  updated_time: string;
}

export interface Tag {
  id: number;
  name: string;
  article_count?: number;
}
