import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    // в dev-режиме запросы к API уходят на uvicorn, поэтому CORS не нужен
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
