/**
 * Vite Performance Configuration
 * ===============================
 * 
 * Enhanced Vite configuration for optimal performance.
 * Part of T26: Frontend Performance Enhancement
 * 
 * Features:
 * - Bundle analysis
 * - Advanced code splitting
 * - Compression
 * - Tree shaking
 * - Asset optimization
 */

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { visualizer } from 'rollup-plugin-visualizer';
import viteCompression from 'vite-plugin-compression';
import { resolve } from 'path';

export default defineConfig(({ mode }) => {
  const isProduction = mode === 'production';
  const isAnalyze = mode === 'analyze';

  return {
    plugins: [
      react({
        // Enable Fast Refresh
        fastRefresh: true,
        
        // Babel configuration for optimization
        babel: {
          plugins: [
            // Remove PropTypes in production
            isProduction && ['babel-plugin-transform-react-remove-prop-types', { removeImport: true }]
          ].filter(Boolean)
        }
      }),

      // Bundle analyzer (only in analyze mode)
      isAnalyze && visualizer({
        filename: './dist/stats.html',
        open: true,
        gzipSize: true,
        brotliSize: true,
        template: 'treemap' // or 'sunburst', 'network'
      }),

      // Gzip compression
      isProduction && viteCompression({
        algorithm: 'gzip',
        ext: '.gz',
        threshold: 10240, // Only compress files > 10KB
        deleteOriginFile: false
      }),

      // Brotli compression
      isProduction && viteCompression({
        algorithm: 'brotliCompress',
        ext: '.br',
        threshold: 10240,
        deleteOriginFile: false
      })
    ].filter(Boolean),

    // Build configuration
    build: {
      // Target modern browsers
      target: 'es2015',

      // Output directory
      outDir: 'dist',

      // Asset directory
      assetsDir: 'assets',

      // Inline assets smaller than 4KB
      assetsInlineLimit: 4096,

      // CSS code splitting
      cssCodeSplit: true,

      // Source maps (only in development)
      sourcemap: !isProduction,

      // Minification
      minify: isProduction ? 'terser' : false,

      // Terser options
      terserOptions: isProduction ? {
        compress: {
          drop_console: true,
          drop_debugger: true,
          pure_funcs: ['console.log', 'console.info', 'console.debug'],
          passes: 2
        },
        mangle: {
          safari10: true
        },
        format: {
          comments: false
        }
      } : {},

      // Rollup options
      rollupOptions: {
        output: {
          // Manual chunks for better caching
          manualChunks: {
            // React core
            'react-core': ['react', 'react-dom'],
            
            // React Router
            'react-router': ['react-router-dom'],
            
            // UI libraries
            'ui-libs': ['lucide-react', 'react-hot-toast'],
            
            // Utility libraries
            'utils': ['date-fns', 'lodash'],
            
            // Chart libraries
            'charts': ['recharts'],
            
            // Form libraries (if used)
            // 'forms': ['formik', 'yup'],
          },

          // Asset file names
          assetFileNames: (assetInfo) => {
            const info = assetInfo.name.split('.');
            let extType = info[info.length - 1];
            
            if (/\.(png|jpe?g|svg|gif|tiff|bmp|ico)$/i.test(assetInfo.name)) {
              extType = 'images';
            } else if (/\.(woff2?|eot|ttf|otf)$/i.test(assetInfo.name)) {
              extType = 'fonts';
            }
            
            return `assets/${extType}/[name]-[hash][extname]`;
          },

          // Chunk file names
          chunkFileNames: 'assets/js/[name]-[hash].js',

          // Entry file names
          entryFileNames: 'assets/js/[name]-[hash].js'
        },

        // External dependencies (if needed)
        // external: [],

        // Tree shaking
        treeshake: {
          moduleSideEffects: false,
          propertyReadSideEffects: false,
          tryCatchDeoptimization: false
        }
      },

      // Chunk size warning limit (500KB)
      chunkSizeWarningLimit: 500,

      // Report compressed size
      reportCompressedSize: isProduction,

      // Write bundle to disk
      write: true,

      // Empty outDir before build
      emptyOutDir: true
    },

    // Server configuration
    server: {
      port: 3000,
      host: true,
      cors: true,
      
      // HMR configuration
      hmr: {
        overlay: true
      },

      // Proxy configuration (if needed)
      proxy: {
        '/api': {
          target: 'http://localhost:5001',
          changeOrigin: true,
          secure: false
        }
      }
    },

    // Preview configuration
    preview: {
      port: 3000,
      host: true,
      cors: true
    },

    // Resolve configuration
    resolve: {
      alias: {
        '@': resolve(__dirname, 'src'),
        '@components': resolve(__dirname, 'src/components'),
        '@pages': resolve(__dirname, 'src/pages'),
        '@utils': resolve(__dirname, 'src/utils'),
        '@hooks': resolve(__dirname, 'src/hooks'),
        '@assets': resolve(__dirname, 'src/assets'),
        '@services': resolve(__dirname, 'src/services'),
        '@contexts': resolve(__dirname, 'src/contexts')
      },

      // Extensions to resolve
      extensions: ['.mjs', '.js', '.jsx', '.json']
    },

    // CSS configuration
    css: {
      // CSS modules
      modules: {
        localsConvention: 'camelCase'
      },

      // PostCSS configuration
      postcss: {
        plugins: [
          // Add PostCSS plugins here if needed
        ]
      },

      // Dev source map
      devSourcemap: !isProduction
    },

    // Dependency optimization
    optimizeDeps: {
      include: [
        'react',
        'react-dom',
        'react-router-dom',
        'lucide-react',
        'react-hot-toast'
      ],

      // Exclude from optimization
      exclude: []
    },

    // Esbuild configuration
    esbuild: {
      // Drop console in production
      drop: isProduction ? ['console', 'debugger'] : [],

      // JSX configuration
      jsxInject: `import React from 'react'`,

      // Minify identifiers
      minifyIdentifiers: isProduction,

      // Minify syntax
      minifySyntax: isProduction,

      // Minify whitespace
      minifyWhitespace: isProduction
    },

    // Performance hints
    performance: {
      // Max entry point size (500KB)
      maxEntrypointSize: 500000,

      // Max asset size (500KB)
      maxAssetSize: 500000
    }
  };
});

