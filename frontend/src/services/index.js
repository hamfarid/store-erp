/**
 * مركز تصدير جميع الخدمات (Services Index)
 * @file frontend/src/services/index.js
 * 
 * هذا الملف يصدر جميع الخدمات المتاحة للتطبيق
 */

// API Client الأساسي
export { default as apiClient } from './apiClient';

// خدمات المصادقة والمستخدمين
export { default as authService } from './authService';
export { default as userService } from './userService';
export { default as permissionService } from './permissionService';
export { default as sessionSecurity } from './sessionSecurity';

// خدمات المنتجات والمخزون
export { default as productService } from './productService';
export { default as categoryService } from './categoryService';
export { default as lotService } from './lotService';
export { default as warehouseService } from './warehouseService';

// خدمات المبيعات والمشتريات
export { default as invoiceService } from './invoiceService';
export { default as posService } from './posService';
export { default as purchaseService } from './purchaseService';
export { default as cartService } from './cartService';

// خدمات العملاء والموردين
export { default as customerService } from './customerService';

// خدمات التقارير والإعدادات
export { default as reportsService } from './reportsService';
export { default as settingsService } from './settingsService';

// خدمات إدارية
export { default as adminService } from './adminService';

// خدمات الصحة والمراقبة
export { default as healthService } from './healthService';

// API Service الموحد (للتوافق)
export { default as ApiService } from './ApiService';
export { default as enhancedAPI } from './enhancedAPI';
export { default as api } from './api';

/**
 * تهيئة جميع الخدمات
 * يمكن استخدامها لإعداد الخدمات عند بدء التطبيق
 */
export const initializeServices = (config = {}) => {
  // يمكن إضافة تهيئة مخصصة هنا
  console.log('📦 Services initialized');
  return true;
};

/**
 * فحص صحة جميع الاتصالات
 */
export const healthCheckServices = async () => {
  const { default: apiClient } = await import('./apiClient');
  return apiClient.healthCheck();
};
