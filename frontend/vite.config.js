import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'


// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  },

  build: {
    sourcemap: false,
    minify: 'esbuild',
  
    // 自动拆包：首页加载更快（核心优化）
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'axios']
        }
      }
    },

    // 关闭 sourcemap（线上不需要，减小包体积）
    sourcemap: false,

    // 打包文件大小警告阈值
    chunkSizeWarningLimit: 1000
  },

  // 基础路径（配合 Nginx 访问正常）
  base: './'
})
