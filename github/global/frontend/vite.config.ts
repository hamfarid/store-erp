import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Global System Ultimate - Vite Config
// Verified Feb 2026: React 19.2.4

export default defineConfig({
  plugins: [react()],
  server: {
    port: parseInt(process.env.FRONTEND_PORT || '3000'),
    proxy: {
      '/api': {
        target: process.env.BACKEND_URL || 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
