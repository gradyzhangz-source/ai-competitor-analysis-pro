import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// GitHub Pages 使用子路径 /<repo>/，通过 CI 注入 VITE_BASE_PATH
const base = process.env.VITE_BASE_PATH || '/'

// https://vitejs.dev/config/
export default defineConfig({
  base,
  plugins: [react()],
  server: {
    host: true, // 允许局域网外部设备访问
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      }
    }
  }
})
