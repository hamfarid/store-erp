/**
 * مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/router/index.js
 * ملف التوجيه الرئيسي للواجهة الأمامية
 */

import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '../store';
import { handleRouteError } from './error-handler';
import securityMiddleware from './security-middleware';

Vue.use(VueRouter);

// مكونات الصفحات
const Home = () => import('../views/Home.vue');
const Login = () => import('../views/auth/Login.vue');
const Register = () => import('../views/auth/Register.vue');
const ForgotPassword = () => import('../views/auth/ForgotPassword.vue');
const ResetPassword = () => import('../views/auth/ResetPassword.vue');
const Dashboard = () => import('../views/Dashboard.vue');
const Settings = () => import('../views/Settings.vue');
const UserProfile = () => import('../views/UserProfile.vue');
const AdminDashboard = () => import('../views/admin/AdminDashboard.vue');
const UserManagement = () => import('../components/settings/UserManagement.vue');
const AIAgentManagement = () => import('../components/settings/AIAgentManagement.vue');
const DatabaseSelector = () => import('../components/settings/DatabaseSelector.vue');
const BackupRestore = () => import('../components/settings/BackupRestore.vue');
const ModuleManager = () => import('../components/settings/ModuleManager.vue');
const PermissionsManager = () => import('../components/settings/PermissionsManager.vue');
const CompanyManagement = () => import('../components/settings/CompanyManagement.vue');
const SystemSettings = () => import('../components/settings/SystemSettings.vue');
const SetupWizard = () => import('../components/setup/SetupWizard.vue');
const SetupWizardContainer = () => import('../components/setup/SetupWizardContainer.vue');
const AIChat = () => import('../components/ai_agent/AIChat.vue');
const DiagnosisForm = () => import('../components/diagnosis/DiagnosisForm.vue');
const DiagnosisResults = () => import('../components/diagnosis/DiagnosisResults.vue');
const ActivityLog = () => import('../components/activity_log/ActivityLog.vue');
const ImportExportDashboard = () => import('../components/import_export/ImportExportDashboard.vue');
const ErrorPage = () => import('../components/errors/ErrorPage.vue');
const NotFound = () => import('../views/errors/NotFound.vue');
const Forbidden = () => import('../views/errors/Forbidden.vue');
const ServerError = () => import('../views/errors/ServerError.vue');
const Blocked = () => import('../views/errors/Blocked.vue');

// تعريف المسارات
const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: {
      title: 'الصفحة الرئيسية',
      requiresAuth: false
    }
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: {
      title: 'تسجيل الدخول',
      requiresGuest: true
    }
  },
  {
    path: '/register',
    name: 'register',
    component: Register,
    meta: {
      title: 'إنشاء حساب',
      requiresGuest: true
    }
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: ForgotPassword,
    meta: {
      title: 'نسيت كلمة المرور',
      requiresGuest: true
    }
  },
  {
    path: '/reset-password/:token',
    name: 'reset-password',
    component: ResetPassword,
    meta: {
      title: 'إعادة تعيين كلمة المرور',
      requiresGuest: true
    }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
    meta: {
      title: 'لوحة التحكم',
      requiresAuth: true
    }
  },
  {
    path: '/profile',
    name: 'profile',
    component: UserProfile,
    meta: {
      title: 'الملف الشخصي',
      requiresAuth: true
    }
  },
  {
    path: '/ai-chat',
    name: 'ai-chat',
    component: AIChat,
    meta: {
      title: 'محادثة الذكاء الاصطناعي',
      requiresAuth: true,
      permissions: 'ai_chat_access'
    }
  },
  {
    path: '/diagnosis',
    name: 'diagnosis',
    component: DiagnosisForm,
    meta: {
      title: 'نموذج التشخيص',
      requiresAuth: true,
      permissions: 'diagnosis_access'
    }
  },
  {
    path: '/diagnosis/results/:id',
    name: 'diagnosis-results',
    component: DiagnosisResults,
    meta: {
      title: 'نتائج التشخيص',
      requiresAuth: true,
      permissions: 'diagnosis_access'
    }
  },
  {
    path: '/activity-log',
    name: 'activity-log',
    component: ActivityLog,
    meta: {
      title: 'سجل النشاط',
      requiresAuth: true,
      permissions: 'logs_access'
    }
  },
  {
    path: '/import-export',
    name: 'import-export',
    component: ImportExportDashboard,
    meta: {
      title: 'استيراد وتصدير البيانات',
      requiresAuth: true,
      permissions: 'import_export_access'
    }
  },
  {
    path: '/settings',
    name: 'settings',
    component: Settings,
    meta: {
      title: 'الإعدادات',
      requiresAuth: true,
      permissions: 'settings_access'
    },
    children: [
      {
        path: 'users',
        name: 'user-management',
        component: UserManagement,
        meta: {
          title: 'إدارة المستخدمين',
          requiresAuth: true,
          permissions: 'user_management'
        }
      },
      {
        path: 'ai-agents',
        name: 'ai-agent-management',
        component: AIAgentManagement,
        meta: {
          title: 'إدارة وكلاء الذكاء الاصطناعي',
          requiresAuth: true,
          permissions: 'ai_agent_management'
        }
      },
      {
        path: 'databases',
        name: 'database-selector',
        component: DatabaseSelector,
        meta: {
          title: 'اختيار قاعدة البيانات',
          requiresAuth: true,
          permissions: 'database_management'
        }
      },
      {
        path: 'backup-restore',
        name: 'backup-restore',
        component: BackupRestore,
        meta: {
          title: 'النسخ الاحتياطي والاستعادة',
          requiresAuth: true,
          permissions: 'backup_management'
        }
      },
      {
        path: 'modules',
        name: 'module-manager',
        component: ModuleManager,
        meta: {
          title: 'إدارة المديولات',
          requiresAuth: true,
          permissions: 'module_management'
        }
      },
      {
        path: 'permissions',
        name: 'permissions-manager',
        component: PermissionsManager,
        meta: {
          title: 'إدارة الصلاحيات',
          requiresAuth: true,
          permissions: 'permissions_management'
        }
      },
      {
        path: 'companies',
        name: 'company-management',
        component: CompanyManagement,
        meta: {
          title: 'إدارة الشركات',
          requiresAuth: true,
          permissions: 'company_management'
        }
      },
      {
        path: 'system',
        name: 'system-settings',
        component: SystemSettings,
        meta: {
          title: 'إعدادات النظام',
          requiresAuth: true,
          permissions: 'system_settings'
        }
      }
    ]
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminDashboard,
    meta: {
      title: 'لوحة تحكم المسؤول',
      requiresAuth: true,
      permissions: 'admin'
    }
  },
  {
    path: '/setup',
    name: 'setup-wizard',
    component: SetupWizardContainer,
    meta: {
      title: 'معالج الإعداد',
      requiresAuth: true,
      permissions: 'setup_access'
    }
  },
  {
    path: '/blocked',
    name: 'blocked',
    component: Blocked,
    meta: {
      title: 'الحساب محظور',
      requiresAuth: false
    }
  },
  {
    path: '/error/:code',
    name: 'error',
    component: ErrorPage,
    props: true,
    meta: {
      title: 'خطأ',
      requiresAuth: false
    }
  },
  {
    path: '/403',
    name: 'forbidden',
    component: Forbidden,
    meta: {
      title: 'غير مصرح',
      requiresAuth: false
    }
  },
  {
    path: '/500',
    name: 'server-error',
    component: ServerError,
    meta: {
      title: 'خطأ في الخادم',
      requiresAuth: false
    }
  },
  {
    path: '*',
    name: 'not-found',
    component: NotFound,
    meta: {
      title: 'الصفحة غير موجودة',
      requiresAuth: false
    }
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { x: 0, y: 0 };
    }
  }
});

// وسيط الأمان
router.beforeEach(async (to, from, next) => {
  try {
    // التحقق من بروتوكول HTTPS
    if (window.location.protocol !== 'https:' && process.env.NODE_ENV === 'production') {
      window.location.href = window.location.href.replace('http:', 'https:');
      return;
    }

    // تطبيق وسيط الأمان
    await securityMiddleware(to, from, next);
  } catch (error) {
    // معالجة الأخطاء
    handleRouteError(error, to, next);
  }
});

// تحديث عنوان الصفحة
router.afterEach((to) => {
  // تحديث عنوان الصفحة
  document.title = to.meta.title ? `${to.meta.title} | Scan AI` : 'Scan AI';

  // تسجيل زيارة الصفحة في سجل النشاط
  if (store.getters['auth/isAuthenticated']) {
    const userId = store.getters['auth/userId'];
    const username = store.getters['auth/username'];
    const pageName = to.name;
    const pageTitle = to.meta.title;

    // استدعاء خدمة سجل النشاط
    store.dispatch('activity/logPageVisit', {
      userId,
      username,
      pageName,
      pageTitle,
      timestamp: new Date().toISOString()
    });
  }
});

export default router;
