import { defineStore } from "pinia";
import { ref } from "vue";
import { getArticles, getArticle, getTags } from "@/api/user";

export const useArticleStore = defineStore("article", () => {
  const articles = ref<Article[]>([]);
  const currentArticle = ref<Article | null>(null);
  const tags = ref<Tag[]>([]);
  const total = ref(0);
  const loading = ref(false);

  async function fetchArticles(page = 1, pageSize = 10) {
    loading.value = true;
    try {
      const res = await getArticles({ page, page_size: pageSize });
      const data = res.data.data || res.data;
      articles.value = data.results || data;
      total.value = data.count || 0;
    } finally {
      loading.value = false;
    }
  }

  async function fetchArticle(slug: string) {
    const res = await getArticle(slug);
    currentArticle.value = res.data.data;
    return currentArticle.value;
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
    fetchArticles,
    fetchArticle,
    fetchTags,
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
  article_c