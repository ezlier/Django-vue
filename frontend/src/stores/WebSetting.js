/**
 * 网站设置存储
 * 管理网站配置信息的全局状态
 */
import { defineStore } from "pinia"
import { getWebSetting } from "@/utils/websetting"

export const useWebSettingStore = defineStore("WebSetting", {
    state: () => ({
        WebSettingList: [],
        loaded: false
    }),

    actions: {
        async fetchWebSetting() {
            if (this.loaded) return

            const res = await getWebSetting()
            this.WebSettingList = res.data.data
            this.loaded = true
        }
    }
})