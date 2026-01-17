/**
 * إعدادات التطوير للنظام الموحد
 * Development Configuration for Unified System
 */

const developmentConfig = {
  // إعدادات الخادم الخلفي
  backend: {
    host: 'localhost',
    port: 5000,
    protocol: 'http',
    baseUrl: 'http://localhost:5000',
    apiPrefix: '/api',
    
    // إعدادات قاعدة البيانات
    database: {
      type: 'sqlite',
      path: './backend/src/database/unified_inventory.db',
      logging: true,
      synchronize: false
    },
    
    // إعدادات الأمان
    security: {
      sessionSecret: 'unified-inventory-system-2024',
      sessionTimeout: 24 * 60 * 60 * 1000, // 24 ساعة
      corsOrigins: ['http://localhost:3000', 'http://localhost:5502'],
      rateLimiting: {
        windowMs: 15 * 60 * 1000, // 15 دقيقة
        max: 100 // حد أقصى 100 طلب لكل IP
      }
    },
    
    // إعدادات التسجيل
    logging: {
      level: 'info',
      format: 'combined',
      file: './backend/logs/app.log'
    }
  },
  
  // إعدادات الواجهة الأمامية
  frontend: {
    host: 'localhost',
    port: 5502,
    protocol: 'http',
    baseUrl: 'http://localhost:5502',
    
    // إعدادات API
    api: {
      baseUrl: 'http://127.0.0.1:8000',
      timeout: 10000,
      retries: 3
    },
    
    // إعدادات التطبيق
    app: {
      title: 'نظام إدارة المخزون الزراعي',
      description: 'نظام شامل لإدارة المخزون الزراعي - Gaara Seeds',
      version: '2.0.0',
      language: 'ar',
      direction: 'rtl',
      theme: 'light'
    },
    
    // إعدادات التطوير
    development: {
      hotReload: true,
      sourceMap: true,
      devtools: true,
      strictMode: true
    }
  },
  
  // أدوات التطوير
  tools: {
    // أوامر مفيدة
    scripts: {
      // Backend
      'start:backend': 'cd backend/src && python unified_server.py',
      'test:backend': 'cd backend/src && python test_unified_server.py',
      'migrate:db': 'cd backend/src && python database_migration_unified.py',
      'seed:db': 'cd backend/src && python add_sample_data.py',
      'optimize:db': 'cd backend/src && python optimize_database.py',
      
      // Frontend
      'start:frontend': 'cd frontend && npm run dev',
      'build:frontend': 'cd frontend && npm run build',
      'test:frontend': 'cd frontend && npm test',
      'lint:frontend': 'cd frontend && npm run lint',
      
      // Full System
      'start:all': 'concurrently "npm run start:backend" "npm run start:frontend"',
      'test:all': 'npm run test:backend && npm run test:frontend',
      'setup:dev': 'npm run migrate:db && npm run seed:db && npm run optimize:db'
    },
    
    // متغيرات البيئة
    environment: {
      NODE_ENV: 'development',
      REACT_APP_API_URL: 'http://localhost:5000',
      REACT_APP_VERSION: '2.0.0',
      REACT_APP_TITLE: 'نظام إدارة المخزون الزراعي',
      FLASK_ENV: 'development',
      FLASK_DEBUG: 'true'
    },
    
    // إعدادات Git
    git: {
      hooks: {
        'pre-commit': 'npm run lint:frontend',
        'pre-push': 'npm run test:all'
      },
      ignore: [
        'node_modules/',
        '*.log',
        '.env',
        'dist/',
        'build/',
        '__pycache__/',
        '*.pyc',
        '.DS_Store',
        'Thumbs.db'
      ]
    }
  },
  
  // إعدادات الاختبار
  testing: {
    backend: {
      framework: 'unittest',
      coverage: true,
      reports: './backend/test-reports/'
    },
    frontend: {
      framework: 'jest',
      coverage: true,
      reports: './frontend/test-reports/'
    }
  },
  
  // إعدادات النشر
  deployment: {
    staging: {
      backend: {
        host: 'staging.gaara-seeds.com',
        port: 5000
      },
      frontend: {
        host: 'staging.gaara-seeds.com',
        port: 3000
      }
    },
    production: {
      backend: {
        host: 'app.gaara-seeds.com',
        port: 5000
      },
      frontend: {
        host: 'app.gaara-seeds.com',
        port: 80
      }
    }
  },
  
  // إرشادات التطوير
  guidelines: {
    coding: {
      style: 'PEP 8 for Python, ESLint for JavaScript',
      naming: 'snake_case for Python, camelCase for JavaScript',
      comments: 'Arabic for business logic, English for technical',
      documentation: 'JSDoc for JavaScript, Docstrings for Python'
    },
    
    git: {
      commits: 'Conventional Commits format',
      branches: 'feature/*, bugfix/*, hotfix/*',
      merging: 'Squash and merge for features'
    },
    
    testing: {
      coverage: 'Minimum 80% code coverage',
      types: 'Unit, Integration, E2E tests',
      naming: 'test_* for Python, *.test.js for JavaScript'
    }
  },
  
  // معلومات المشروع
  project: {
    name: 'Unified Agricultural Inventory Management System',
    nameAr: 'نظام إدارة المخزون الزراعي الموحد',
    version: '2.0.0',
    description: 'نظام شامل لإدارة المخزون الزراعي مصمم خصيصاً لشركة Gaara Seeds',
    author: 'Development Team',
    license: 'Proprietary',
    repository: 'https://github.com/gaara-seeds/inventory-system',
    
    // معلومات الشركة
    company: {
      name: 'Gaara Seeds',
      website: 'https://gaara-seeds.com',
      email: 'info@gaara-seeds.com',
      phone: '+20 xxx xxx xxxx'
    },
    
    // الفريق
    team: {
      lead: 'Senior Developer',
      backend: 'Backend Developer',
      frontend: 'Frontend Developer',
      qa: 'QA Engineer'
    }
  },
  
  // الميزات المتاحة
  features: {
    authentication: true,
    authorization: true,
    products: true,
    customers: true,
    suppliers: true,
    warehouses: true,
    inventory: true,
    invoices: true,
    reports: true,
    audit: true,
    notifications: true,
    multiLanguage: false, // قريباً
    mobileApp: false, // قريباً
    api: true,
    realtime: false // قريباً
  },
  
  // حالة المشروع
  status: {
    overall: 'completed',
    backend: 'completed',
    frontend: 'completed',
    database: 'completed',
    testing: 'completed',
    documentation: 'completed',
    deployment: 'ready'
  }
};

// تصدير الإعدادات
if (typeof module !== 'undefined' && module.exports) {
  module.exports = developmentConfig;
}

// للاستخدام في المتصفح
if (typeof window !== 'undefined') {
  window.developmentConfig = developmentConfig;
}

console.log('🔧 تم تحميل إعدادات التطوير بنجاح');
console.log('📊 حالة المشروع:', developmentConfig.status.overall);
console.log('🚀 النظام جاهز للتطوير والاستخدام!');
