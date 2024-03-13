import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// // https://vitejs.dev/config/
// export default defineConfig({
//   plugins: [react()],
// })

export default {
  root: './frontend',  // 设置Vite的工作目录为'./frontend'
  build: {
    rollupOptions: {
      input: './fronted/src/main.jsx'  // 指定入口文件的路径
    }
  }
}