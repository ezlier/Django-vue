/**
 * 标签数据存储
 * 管理文章标签的全局状态
 */
import { defineStore } from "pinia"
import { getTags } from "@/utils/article"

export const useTagsStore = defineStore("Tags", {
    state: () => ({
        tags: [],
        loaded: false,
        tagsLength: 0
    }),

    actions: {
        async fetchTags() {
            if (this.loaded) return

            const res = await getTags()
            this.tags = res.data.data
            this.loaded = true
            this.tagsLength = this.tags.length
        }
    }
})