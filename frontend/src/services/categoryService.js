/**
 * خدمة إدارة الفئات (Category Management Service)
 * @file frontend/src/services/categoryService.js
 */

import apiClient from './apiClient';

const categoryService = {
  // ==================== CRUD Operations ====================

  /**
   * الحصول على جميع الفئات
   * @param {Object} params - معلمات الترشيح
   */
  async getCategories(params = {}) {
    return apiClient.get('/api/categories', params);
  },

  /**
   * الحصول على فئة بواسطة ID
   * @param {number} id - معرف الفئة
   */
  async getCategoryById(id) {
    return apiClient.get(`/api/categories/${id}`);
  },

  /**
   * إنشاء فئة جديدة
   * @param {Object} data - بيانات الفئة
   */
  async createCategory(data) {
    return apiClient.post('/api/categories', data);
  },

  /**
   * تحديث فئة
   * @param {number} id - معرف الفئة
   * @param {Object} data - البيانات المحدثة
   */
  async updateCategory(id, data) {
    return apiClient.put(`/api/categories/${id}`, data);
  },

  /**
   * حذف فئة
   * @param {number} id - معرف الفئة
   */
  async deleteCategory(id) {
    return apiClient.delete(`/api/categories/${id}`);
  },

  // ==================== Hierarchical Operations ====================

  /**
   * الحصول على شجرة الفئات
   */
  async getCategoriesTree() {
    return apiClient.get('/api/categories/tree');
  },

  /**
   * الحصول على الفئات الفرعية
   * @param {number} parentId - معرف الفئة الأم
   */
  async getSubcategories(parentId) {
    return apiClient.get('/api/categories', { parent_id: parentId });
  },

  /**
   * الحصول على الفئات الرئيسية فقط
   */
  async getRootCategories() {
    return apiClient.get('/api/categories', { root_only: true });
  },

  /**
   * نقل فئة إلى فئة أم أخرى
   * @param {number} categoryId - معرف الفئة
   * @param {number|null} newParentId - معرف الفئة الأم الجديدة
   */
  async moveCategory(categoryId, newParentId) {
    return apiClient.patch(`/api/categories/${categoryId}/move`, {
      parent_id: newParentId
    });
  },

  // ==================== Status Operations ====================

  /**
   * تفعيل/إلغاء تفعيل فئة
   * @param {number} id - معرف الفئة
   * @param {boolean} isActive - حالة التفعيل
   */
  async toggleCategoryActive(id, isActive) {
    return apiClient.patch(`/api/categories/${id}/active`, { is_active: isActive });
  },

  // ==================== Products Operations ====================

  /**
   * الحصول على منتجات الفئة
   * @param {number} categoryId - معرف الفئة
   * @param {Object} params - معلمات الترشيح
   */
  async getCategoryProducts(categoryId, params = {}) {
    return apiClient.get(`/api/categories/${categoryId}/products`, params);
  },

  /**
   * عدد منتجات الفئة
   * @param {number} categoryId - معرف الفئة
   */
  async getCategoryProductCount(categoryId) {
    return apiClient.get(`/api/categories/${categoryId}/product-count`);
  },

  // ==================== Image Operations ====================

  /**
   * رفع صورة الفئة
   * @param {number} categoryId - معرف الفئة
   * @param {File} file - ملف الصورة
   */
  async uploadCategoryImage(categoryId, file) {
    return apiClient.uploadFile(`/api/categories/${categoryId}/image`, file);
  },

  /**
   * حذف صورة الفئة
   * @param {number} categoryId - معرف الفئة
   */
  async deleteCategoryImage(categoryId) {
    return apiClient.delete(`/api/categories/${categoryId}/image`);
  },

  // ==================== Statistics ====================

  /**
   * إحصائيات الفئات
   */
  async getCategoryStats() {
    return apiClient.get('/api/categories/stats');
  },

  // ==================== Export ====================

  /**
   * تصدير الفئات إلى Excel
   */
  async exportToExcel() {
    return apiClient.downloadFile('/api/categories/export/excel', 'categories_export.xlsx');
  }
};

export default categoryService;
