import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 4501,
    host: '0.0.0.0',
    strictPort: true,
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./"),
      "@/components": path.resolve(__dirname, "./components"),
      "@/lib": path.resolve(__dirname, "./lib"),
      "@/hooks": path.resolve(__dirname, "./hooks"),
      "@/services": path.resolve(__dirname, "./services"),
      "@/pages": path.resolve(__dirname, "./pages"),
      "@/context": path.resolve(__dirname, "./context"),
      "@/utils": path.resolve(__dirname, "./utils"),
    },
  },
  css: {
    postcss: './postcss.config.js',
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          charts: ['recharts'],
          ui: ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu', '@radix-ui/react-select'],
        },
      },
    },
  },
})
