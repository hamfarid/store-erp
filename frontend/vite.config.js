import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

export default defineConfig({
  plugins: [react()],

  // Test configuration
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/tests/setup.js',
    include: ['**/*.test.{js,jsx}'],
    exclude: ['**/node_modules/**', '**/dist/**', '**/tests/e2e/**'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/tests/',
        '**/*.test.{js,jsx}',
        '**/*.config.js'
      ]
    }
  },

  // تحسينات الأداء المتقدمة
  build: {
    // تحسين حجم الحزمة
    rollupOptions: {
      output: {
        manualChunks: {
          // فصل مكتبات React
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],

          // فصل مكتبات UI
          'ui-vendor': ['lucide-react'],

          // فصل مكتبات المساعدة
          'utils-vendor': ['date-fns', 'lodash'],

          // فصل مكتبات الرسوم البيانية
          'chart-vendor': ['recharts']
        }
      }
    },

    // تحسين الضغط
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    },

    // تحسين حجم الملفات
    chunkSizeWarningLimit: 1000,

    // تفعيل source maps للإنتاج
    sourcemap: false
  },

  // تحسين الخادم المحلي + بروكسي للـ API
  server: {
    port: 5505,
    host: true,
    cors: true,
    proxy: {
      '/api': {
        target: 'http://localhost:5506',
        changeOrigin: true,
        secure: false
      }
    }
  },

  // تحسين الحل
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@components': resolve(__dirname, 'src/components'),
      '@pages': resolve(__dirname, 'src/pages'),
      '@utils': resolve(__dirname, 'src/utils'),
      '@assets': resolve(__dirname, 'src/assets')
    }
  },

  // تحسين CSS
  css: {
    devSourcemap: false
  },

  // تحسين التبعيات
  optimizeDeps: {
    include: [
      'react',
      'react-dom',
      'react-router-dom',
      'lucide-react'
    ]
  }
})