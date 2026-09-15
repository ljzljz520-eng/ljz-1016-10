import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// 开发服务器将 /api 代理到 Django，前端同源请求，会话 Cookie 无跨域问题
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: false,
      },
    },
  },
});
