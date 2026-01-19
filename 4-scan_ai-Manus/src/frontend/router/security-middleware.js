/**
 * مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/router/security-middleware.js
 * وسيط أمان للتوجيه في الواجهة الأمامية
 * يتحقق من صلاحيات المستخدم ويمنع الوصول غير المصرح به
 */

import { checkPermission } from '../services/securityService';
import store from '../store';

/**
 * وسيط للتحقق من صلاحيات المستخدم قبل الانتقال إلى الصفحة
 * @param {Object} to - الوجهة المطلوبة
 * @param {Object} from - الوجهة الحالية
 * @param {Function} next - دالة للاستمرار في التوجيه
 */
export default async function securityMiddleware(to, from, next) {
  // التحقق من أن الاتصال يتم عبر HTTPS
  if (window.location.protocol !== 'https:' && process.env.NODE_ENV === 'production') {
    window.location.href = window.location.href.replace('http:', 'https:');
    return;
  }

  // التحقق من وجود مسار محمي
  if (to.meta.requiresAuth) {
    // التحقق من تسجيل الدخول
    const isLoggedIn = store.getters['auth/isAuthenticated'];
    if (!isLoggedIn) {
      // إعادة التوجيه إلى صفحة تسجيل الدخول مع حفظ الوجهة المطلوبة
      return next({
        name: 'login',
        query: { redirect: to.fullPath }
      });
    }

    // التحقق من الصلاحيات المطلوبة
    if (to.meta.permissions) {
      const hasPermission = await checkPermission(to.meta.permissions);
      if (!hasPermission) {
        // إعادة التوجيه إلى صفحة الخطأ 403 (غير مصرح)
        return next({ name: 'forbidden' });
      }
    }

    // التحقق من حالة حظر المستخدم
    const isBlocked = store.getters['auth/isUserBlocked'];
    if (isBlocked) {
      // إعادة التوجيه إلى صفحة الحظر
      return next({ name: 'blocked' });
    }
  }

  // التحقق من وجود مسار يتطلب عدم تسجيل الدخول (مثل صفحة تسجيل الدخول)
  if (to.meta.requiresGuest) {
    const isLoggedIn = store.getters['auth/isAuthenticated'];
    if (isLoggedIn) {
      // إعادة التوجيه إلى الصفحة الرئيسية
      return next({ name: 'home' });
    }
  }

  // التحقق من وجود مسار يتطلب إعداد النظام
  if (to.meta.requiresSetup) {
    const isSetupComplete = store.getters['setup/isComplete'];
    if (!isSetupComplete) {
      // إعادة التوجيه إلى معالج الإعداد
      return next({ name: 'setup-wizard' });
    }
  }

  // السماح بالانتقال إلى الصفحة المطلوبة
  next();
}
