/**
 * 主题存储
 * 管理应用主题（深色/浅色模式）的全局状态
 */
import { defineStore } from "pinia";

export const useThemeStore = defineStore("theme", {
  state: () => ({
    isDark: false,
    showTrail: true,
  }),
  actions: {
    initTheme() {
      let saved = null;
      try {
        saved = localStorage.getItem("theme");
      } catch (err) {
        // localStorage 访问失败，使用系统偏好
      }
      if (saved) {
        this.isDark = saved === "dark";
      } else {
        this.isDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      }
      this.applyTheme();
    },
    toggleTheme() {
      this.isDark = !this.isDark;
      try {
        localStorage.setItem("theme", this.isDark ? "dark" : "light");
      } catch (err) {
        // localStorage 存储失败，继续应用主题
      }
      this.applyTheme();
    },
    applyTheme() {
      document.documentElement.classList.toggle("dark", this.isDark);
    },
    initTrail() {
      let saved = null;
      try {
        saved = localStorage.getItem("showTrail");
      } catch (err) {
        // localStorage 访问失败，使用默认值
      }
      if (saved !== null) {
        this.showTrail = saved === 'true';
      }
    },
    toggleTrail() {
      this.showTrail = !this.showTrail;
      try {
        localStorage.setItem("showTrail", this.showTrail.toString());
      } catch (err) {
        // localStorage 存储失败，继续应用状态
      }
    },
  },
});
