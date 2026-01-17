import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'
import { fileURLToPath } from 'url'
import path from 'node:path'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: [
      resolve(__dirname, 'src/tests/setupTests.js'),
      resolve(__dirname, 'src/tests/setup.js')
    ],
    css: true,
    coverage: {
      reporter: ['text', 'lcov'],
      exclude: ['node_modules/', 'dist/']
    },
    exclude: ['**/e2e/**', '**/node_modules/**', '**/dist/**', '**/*.spec.js']
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@components': resolve(__dirname, 'src/components'),
      '@pages': resolve(__dirname, 'src/pages'),
      '@utils': resolve(__dirname, 'src/utils'),
      '@assets': resolve(__dirname, 'src/assets')
    }
  }
})
