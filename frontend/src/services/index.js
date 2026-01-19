/**
 * مركز تصدير جميع الخدمات (Services Index)
 * @file frontend/src/services/index.js
 * 
 * هذا الملف يصدر جميع الخدمات المتاحة للتطبيق
 * Total Services: 30+
 */

// ==================== API Client الأساسي ====================
export { default as apiClient } from './apiClient';
export { default as ApiService } from './ApiService';
export { default as enhancedAPI } from './enhancedAPI';
export { default as api } from './api';

// ==================== خدمات المصادقة والمستخدمين ====================
export { default as authService } from './authService';
export { default as userService } from './userService';
export { default as permissionService } from './permissionService';
export { default as sessionSecurity } from './sessionSecurity';

// ==================== خدمات المنتجات والمخزون ====================
export { default as productService } from './productService';
export { default as categoryService } from './categoryService';
export { default as lotService } from './lotService';
export { default as warehouseService } from './warehouseService';
export { default as stockMovementService } from './stockMovementService';
export { default as priceHistoryService } from './priceHistoryService';

// ==================== خدمات المبيعات والمشتريات ====================
export { default as invoiceService } from './invoiceService';
export { default as posService } from './posService';
export { default as purchaseService } from './purchaseService';
export { default as cartService } from './cartService';
export { default as discountService } from './discountService';
export { default as returnsService } from './returnsService';

// ==================== خدمات العملاء والموردين ====================
export { default as customerService } from './customerService';
export { default as supplierService } from './supplierService';
export { default as salesEngineerService } from './salesEngineerService';

// ==================== خدمات المالية والخزينة ====================
export { default as treasuryService } from './treasuryService';

// ==================== خدمات التقارير والإعدادات ====================
export { default as reportsService } from './reportsService';
export { default as settingsService } from './settingsService';

// ==================== خدمات إدارية ====================
export { default as adminService } from './adminService';
export { default as auditService } from './auditService';
export { default as backupService } from './backupService';
export { default as automationService } from './automationService';
export { default as notificationService } from './notificationService';

// ==================== خدمات الصحة والمراقبة ====================
export { default as healthService } from './healthService';

/**
 * تهيئة جميع الخدمات
 * يمكن استخدامها لإعداد الخدمات عند بدء التطبيق
 */
export const initializeServices = (config = {}) => {
  // يمكن إضافة تهيئة مخصصة هنا
  console.log('📦 Services initialized - 30+ services loaded');
  return true;
};

/**
 * فحص صحة جميع الاتصالات
 */
export const healthCheckServices = async () => {
  const { default: apiClient } = await import('./apiClient');
  return apiClient.healthCheck();
};

/**
 * قائمة بجميع الخدمات المتاحة
 */
export const availableServices = [
  'apiClient',
  'authService',
  'userService',
  'permissionService',
  'sessionSecurity',
  'productService',
  'categoryService',
  'lotService',
  'warehouseService',
  'stockMovementService',
  'priceHistoryService',
  'invoiceService',
  'posService',
  'purchaseService',
  'cartService',
  'discountService',
  'returnsService',
  'customerService',
  'supplierService',
  'salesEngineerService',
  'treasuryService',
  'reportsService',
  'settingsService',
  'adminService',
  'auditService',
  'backupService',
  'automationService',
  'notificationService',
  'healthService'
];
