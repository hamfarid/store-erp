/**
 * Vue Router - نظام التنقل الرئيسي
 * Main Navigation System
 */

import { createRouter, createWebHistory } from 'vue-router'

// استيراد الصفحات الرئيسية
import Dashboard from '@/pages/Dashboard.vue'
import Login from '@/pages/Login.vue'

// استيراد صفحات الذكاء الاصطناعي
import AIManagement from '@/pages/ai/AIManagement.vue'
import AIAgent from '@/pages/ai/AIAgent.vue'
import AIReports from '@/pages/ai/AIReports.vue'

// استيراد صفحات التشخيص
import DiagnosisDashboard from '@/pages/diagnosis/DiagnosisDashboard.vue'
import ImageEnhancement from '@/pages/diagnosis/ImageEnhancement.vue'
import PlantHybridization from '@/pages/diagnosis/PlantHybridization.vue'
import YoloDetection from '@/pages/diagnosis/YoloDetection.vue'

// استيراد صفحات الإدارة
import Settings from '@/pages/admin/Settings.vue'
import UserManagement from '@/pages/admin/UserManagement.vue'
import SystemMonitoring from '@/pages/admin/SystemMonitoring.vue'
import BackupRestore from '@/pages/admin/BackupRestore.vue'
import SecurityManagement from '@/pages/admin/SecurityManagement.vue'

// استيراد صفحات البيانات
import ActivityLog from '@/pages/data/ActivityLog.vue'
import ImportExport from '@/pages/data/ImportExport.vue'
import DataValidation from '@/pages/data/DataValidation.vue'

// استيراد صفحات Docker
import DockerManagement from '@/pages/docker/DockerManagement.vue'
import ContainerMonitoring from '@/pages/docker/ContainerMonitoring.vue'

// تعريف المسارات
const routes = [
  // الصفحة الرئيسية
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: {
      title: 'لوحة التحكم الرئيسية',
      requiresAuth: true,
      icon: 'fas fa-tachometer-alt'
    }
  },

  // تسجيل الدخول
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      title: 'تسجيل الدخول',
      requiresAuth: false,
      hideInMenu: true
    }
  },

  // مجموعة الذكاء الاصطناعي
  {
    path: '/ai',
    name: 'AI',
    meta: {
      title: 'الذكاء الاصطناعي',
      icon: 'fas fa-brain',
      requiresAuth: true
    },
    children: [
      {
        path: 'management',
        name: 'AIManagement',
        component: AIManagement,
        meta: {
          title: 'إدارة الذكاء الاصطناعي',
          icon: 'fas fa-cogs'
        }
      },
      {
        path: 'agent',
        name: 'AIAgent',
        component: AIAgent,
        meta: {
          title: 'المساعد الذكي',
          icon: 'fas fa-robot'
        }
      },
      {
        path: 'reports',
        name: 'AIReports',
        component: AIReports,
        meta: {
          title: 'تقارير الاستخدام',
          icon: 'fas fa-chart-line'
        }
      }
    ]
  },

  // مجموعة التشخيص
  {
    path: '/diagnosis',
    name: 'Diagnosis',
    meta: {
      title: 'التشخيص والتحليل',
      icon: 'fas fa-microscope',
      requiresAuth: true
    },
    children: [
      {
        path: 'dashboard',
        name: 'DiagnosisDashboard',
        component: DiagnosisDashboard,
        meta: {
          title: 'لوحة التشخيص',
          icon: 'fas fa-stethoscope'
        }
      },
      {
        path: 'image-enhancement',
        name: 'ImageEnhancement',
        component: ImageEnhancement,
        meta: {
          title: 'تحسين الصور',
          icon: 'fas fa-image'
        }
      },
      {
        path: 'plant-hybridization',
        name: 'PlantHybridization',
        component: PlantHybridization,
        meta: {
          title: 'تهجين النباتات',
          icon: 'fas fa-seedling'
        }
      },
      {
        path: 'yolo-detection',
        name: 'YoloDetection',
        component: YoloDetection,
        meta: {
          title: 'كشف الكائنات',
          icon: 'fas fa-search'
        }
      }
    ]
  },

  // مجموعة الإدارة
  {
    path: '/admin',
    name: 'Admin',
    meta: {
      title: 'الإدارة',
      icon: 'fas fa-user-shield',
      requiresAuth: true,
      requiresAdmin: true
    },
    children: [
      {
        path: 'settings',
        name: 'Settings',
        component: Settings,
        meta: {
          title: 'إعدادات النظام',
          icon: 'fas fa-cog'
        }
      },
      {
        path: 'users',
        name: 'UserManagement',
        component: UserManagement,
        meta: {
          title: 'إدارة المستخدمين',
          icon: 'fas fa-users'
        }
      },
      {
        path: 'monitoring',
        name: 'SystemMonitoring',
        component: SystemMonitoring,
        meta: {
          title: 'مراقبة النظام',
          icon: 'fas fa-chart-area'
        }
      },
      {
        path: 'backup',
        name: 'BackupRestore',
        component: BackupRestore,
        meta: {
          title: 'النسخ الاحتياطي',
          icon: 'fas fa-database'
        }
      },
      {
        path: 'security',
        name: 'SecurityManagement',
        component: SecurityManagement,
        meta: {
          title: 'إدارة الأمان',
          icon: 'fas fa-shield-alt'
        }
      }
    ]
  },

  // مجموعة البيانات
  {
    path: '/data',
    name: 'Data',
    meta: {
      title: 'إدارة البيانات',
      icon: 'fas fa-database',
      requiresAuth: true
    },
    children: [
      {
        path: 'activity-log',
        name: 'ActivityLog',
        component: ActivityLog,
        meta: {
          title: 'سجل الأنشطة',
          icon: 'fas fa-history'
        }
      },
      {
        path: 'import-export',
        name: 'ImportExport',
        component: ImportExport,
        meta: {
          title: 'الاستيراد والتصدير',
          icon: 'fas fa-exchange-alt'
        }
      },
      {
        path: 'validation',
        name: 'DataValidation',
        component: DataValidation,
        meta: {
          title: 'التحقق من البيانات',
          icon: 'fas fa-check-circle'
        }
      }
    ]
  },

  // مجموعة Docker
  {
    path: '/docker',
    name: 'Docker',
    meta: {
      title: 'إدارة الحاويات',
      icon: 'fab fa-docker',
      requiresAuth: true
    },
    children: [
      {
        path: 'management',
        name: 'DockerManagement',
        component: DockerManagement,
        meta: {
          title: 'إدارة الحاويات',
          icon: 'fas fa-cubes'
        }
      },
      {
        path: 'monitoring',
        name: 'ContainerMonitoring',
        component: ContainerMonitoring,
        meta: {
          title: 'مراقبة الحاويات',
          icon: 'fas fa-eye'
        }
      }
    ]
  },

  // صفحة 404
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/pages/NotFound.vue'),
    meta: {
      title: 'الصفحة غير موجودة',
      hideInMenu: true
    }
  }
]

// إنشاء Router
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// حراس التنقل (Navigation Guards)
router.beforeEach((to, from, next) => {
  // تحديث عنوان الصفحة
  document.title = to.meta.title ? `${to.meta.title} - Gaara Scan AI` : 'Gaara Scan AI'
  
  // فحص المصادقة
  const isAuthenticated = localStorage.getItem('auth_token')
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
    return
  }
  
  // فحص صلاحيات الإدارة
  if (to.meta.requiresAdmin) {
    const userRole = localStorage.getItem('user_role')
    if (userRole !== 'admin') {
      next('/')
      return
    }
  }
  
  next()
})

// تصدير Router
export default router

// تصدير المسارات للاستخدام في القوائم
export const menuRoutes = routes.filter(route => 
  !route.meta?.hideInMenu && route.meta?.requiresAuth
)

