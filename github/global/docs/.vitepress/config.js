import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Store - نظام إدارة المخزون العربي',
  description: 'Arabic Inventory Management System Documentation',
  
  // Base URL for GitHub Pages
  base: '/Store/',
  
  // Language configuration
  lang: 'ar',
  
  // Theme configuration
  themeConfig: {
    // Navigation
    nav: [
      { text: 'الرئيسية', link: '/' },
      { text: 'دليل المستخدم', link: '/user-guide/' },
      { text: 'التوثيق التقني', link: '/technical/' },
      { text: 'API', link: '/api/' },
      { text: 'GitHub', link: 'https://github.com/hamfarid/Store' }
    ],

    // Sidebar
    sidebar: {
      '/user-guide/': [
        {
          text: 'دليل المستخدم',
          items: [
            { text: 'البدء السريع', link: '/user-guide/quick-start' },
            { text: 'إدارة المنتجات', link: '/user-guide/products' },
            { text: 'إدارة العملاء', link: '/user-guide/customers' },
            { text: 'إدارة المبيعات', link: '/user-guide/sales' },
            { text: 'إدارة المخزون', link: '/user-guide/inventory' },
            { text: 'التقارير', link: '/user-guide/reports' }
          ]
        }
      ],
      '/technical/': [
        {
          text: 'التوثيق التقني',
          items: [
            { text: 'هيكل المشروع', link: '/technical/architecture' },
            { text: 'قاعدة البيانات', link: '/technical/database' },
            { text: 'الواجهة الخلفية', link: '/technical/backend' },
            { text: 'الواجهة الأمامية', link: '/technical/frontend' },
            { text: 'النشر', link: '/technical/deployment' },
            { text: 'الأمان', link: '/technical/security' }
          ]
        }
      ],
      '/api/': [
        {
          text: 'API Documentation',
          items: [
            { text: 'مقدمة', link: '/api/introduction' },
            { text: 'المصادقة', link: '/api/authentication' },
            { text: 'المنتجات', link: '/api/products' },
            { text: 'العملاء', link: '/api/customers' },
            { text: 'المبيعات', link: '/api/sales' },
            { text: 'المخزون', link: '/api/inventory' }
          ]
        }
      ]
    },

    // Social links
    socialLinks: [
      { icon: 'github', link: 'https://github.com/hamfarid/Store' }
    ],

    // Footer
    footer: {
      message: 'Built with ❤️ for Arabic-speaking businesses',
      copyright: 'Copyright © 2025 Store - Arabic Inventory Management System'
    },

    // Search
    search: {
      provider: 'local',
      options: {
        locales: {
          ar: {
            translations: {
              button: {
                buttonText: 'بحث',
                buttonAriaLabel: 'بحث'
              },
              modal: {
                displayDetails: 'عرض التفاصيل',
                resetButtonTitle: 'إعادة تعيين البحث',
                backButtonTitle: 'إغلاق البحث',
                noResultsText: 'لا توجد نتائج',
                footer: {
                  selectText: 'للاختيار',
                  selectKeyAriaLabel: 'enter',
                  navigateText: 'للتنقل',
                  navigateUpKeyAriaLabel: 'up arrow',
                  navigateDownKeyAriaLabel: 'down arrow',
                  closeText: 'للإغلاق',
                  closeKeyAriaLabel: 'escape'
                }
              }
            }
          }
        }
      }
    },

    // Edit link
    editLink: {
      pattern: 'https://github.com/hamfarid/Store/edit/main/docs/:path',
      text: 'تحرير هذه الصفحة على GitHub'
    },

    // Last updated
    lastUpdated: {
      text: 'آخر تحديث',
      formatOptions: {
        dateStyle: 'short',
        timeStyle: 'medium'
      }
    }
  },

  // Markdown configuration
  markdown: {
    lineNumbers: true,
    config: (md) => {
      // Add any markdown-it plugins here
    }
  },

  // Head configuration
  head: [
    ['link', { rel: 'icon', href: '/Store/favicon.ico' }],
    ['meta', { name: 'theme-color', content: '#3c8772' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:locale', content: 'ar' }],
    ['meta', { property: 'og:title', content: 'Store - نظام إدارة المخزون العربي' }],
    ['meta', { property: 'og:site_name', content: 'Store Documentation' }],
    ['meta', { property: 'og:image', content: 'https://hamfarid.github.io/Store/og-image.png' }],
    ['meta', { property: 'og:url', content: 'https://hamfarid.github.io/Store/' }]
  ],

  // Sitemap
  sitemap: {
    hostname: 'https://hamfarid.github.io/Store'
  }
})
