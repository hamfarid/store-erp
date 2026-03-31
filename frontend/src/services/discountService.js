/**
 * خدمة إدارة الخصومات (Discount Service)
 * @file frontend/src/services/discountService.js
 */

import apiClient from './apiClient';

export const discountService = {
  // ==================== العمليات الأساسية ====================

  /**
   * الحصول على جميع الخصومات
   */
  async getAll(params = {}) {
    try {
      const queryParams = {
        page: params.page || 1,
        limit: params.limit || 50,
        is_active: params.isActive !== undefined ? params.isActive : '',
        type: params.type || '',
        ...params
      };

      const response = await apiClient.get('/api/discounts', queryParams);
      return {
        discounts: response.discounts || response.data || [],
        total: response.total || 0,
        page: response.page || 1,
        totalPages: response.total_pages || Math.ceil((response.total || 0) / (params.limit || 50)),
      };
    } catch (error) {
      throw new Error(`فشل في تحميل الخصومات: ${error.message}`);
    }
  },

  /**
   * الحصول على خصم بالمعرف
   */
  async getById(id) {
    try {
      const response = await apiClient.get(`/api/discounts/${id}`);
      return response.discount || response;
    } catch (error) {
      throw new Error(`فشل في تحميل الخصم: ${error.message}`);
    }
  },

  /**
   * إنشاء خصم جديد
   */
  async create(discountData) {
    try {
      const response = await apiClient.post('/api/discounts', discountData);
      return response.discount || response;
    } catch (error) {
      throw new Error(`فشل في إنشاء الخصم: ${error.message}`);
    }
  },

  /**
   * تحديث خصم
   */
  async update(id, discountData) {
    try {
      const response = await apiClient.put(`/api/discounts/${id}`, discountData);
      return response.discount || response;
    } catch (error) {
      throw new Error(`فشل في تحديث الخصم: ${error.message}`);
    }
  },

  /**
   * حذف خصم
   */
  async delete(id) {
    try {
      const response = await apiClient.delete(`/api/discounts/${id}`);
      return response;
    } catch (error) {
      throw new Error(`فشل في حذف الخصم: ${error.message}`);
    }
  },

  // ==================== أنواع الخصومات ====================

  /**
   * الحصول على الخصومات حسب النوع
   */
  async getByType(type, params = {}) {
    try {
      const response = await apiClient.get(`/api/discounts/type/${type}`, params);
      return response.discounts || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل الخصومات: ${error.message}`);
    }
  },

  /**
   * الحصول على الخصومات النشطة
   */
  async getActive(params = {}) {
    try {
      const response = await apiClient.get('/api/discounts/active', params);
      return response.discounts || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل الخصومات النشطة: ${error.message}`);
    }
  },

  // ==================== تطبيق الخصومات ====================

  /**
   * تطبيق خصم على منتج
   */
  async applyToProduct(discountId, productId) {
    try {
      const response = await apiClient.post(`/api/discounts/${discountId}/apply/product`, { product_id: productId });
      return response;
    } catch (error) {
      throw new Error(`فشل في تطبيق الخصم: ${error.message}`);
    }
  },

  /**
   * تطبيق خصم على فئة
   */
  async applyToCategory(discountId, categoryId) {
    try {
      const response = await apiClient.post(`/api/discounts/${discountId}/apply/category`, { category_id: categoryId });
      return response;
    } catch (error) {
      throw new Error(`فشل في تطبيق الخصم: ${error.message}`);
    }
  },

  /**
   * تطبيق خصم على عميل
   */
  async applyToCustomer(discountId, customerId) {
    try {
      const response = await apiClient.post(`/api/discounts/${discountId}/apply/customer`, { customer_id: customerId });
      return response;
    } catch (error) {
      throw new Error(`فشل في تطبيق الخصم: ${error.message}`);
    }
  },

  /**
   * إزالة خصم
   */
  async removeDiscount(discountId, targetType, targetId) {
    try {
      const response = await apiClient.post(`/api/discounts/${discountId}/remove`, { 
        target_type: targetType, 
        target_id: targetId 
      });
      return response;
    } catch (error) {
      throw new Error(`فشل في إزالة الخصم: ${error.message}`);
    }
  },

  // ==================== حساب الخصم ====================

  /**
   * حساب الخصم لمنتج
   */
  async calculateForProduct(productId, quantity = 1) {
    try {
      const response = await apiClient.get('/api/discounts/calculate/product', { 
        product_id: productId, 
        quantity 
      });
      return response.discount || 0;
    } catch (error) {
      throw new Error(`فشل في حساب الخصم: ${error.message}`);
    }
  },

  /**
   * حساب الخصم لسلة المشتريات
   */
  async calculateForCart(cartItems) {
    try {
      const response = await apiClient.post('/api/discounts/calculate/cart', { items: cartItems });
      return response.totalDiscount || 0;
    } catch (error) {
      throw new Error(`فشل في حساب الخصم: ${error.message}`);
    }
  },

  /**
   * التحقق من كود الخصم
   */
  async validateCode(code) {
    try {
      const response = await apiClient.post('/api/discounts/validate-code', { code });
      return response;
    } catch (error) {
      throw new Error(`فشل في التحقق من الكود: ${error.message}`);
    }
  },

  // ==================== التقارير ====================

  /**
   * تقرير استخدام الخصومات
   */
  async getUsageReport(params = {}) {
    try {
      const response = await apiClient.get('/api/discounts/reports/usage', params);
      return response.report || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل التقرير: ${error.message}`);
    }
  },

  /**
   * إحصائيات الخصومات
   */
  async getStats(params = {}) {
    try {
      const response = await apiClient.get('/api/discounts/stats', params);
      return response.stats || {};
    } catch (error) {
      throw new Error(`فشل في تحميل الإحصائيات: ${error.message}`);
    }
  },

  // ==================== العمليات المجمعة ====================

  /**
   * تفعيل عدة خصومات
   */
  async bulkActivate(ids) {
    try {
      const response = await apiClient.post('/api/discounts/bulk-activate', { ids });
      return response;
    } catch (error) {
      throw new Error(`فشل في التفعيل المجمع: ${error.message}`);
    }
  },

  /**
   * إلغاء تفعيل عدة خصومات
   */
  async bulkDeactivate(ids) {
    try {
      const response = await apiClient.post('/api/discounts/bulk-deactivate', { ids });
      return response;
    } catch (error) {
      throw new Error(`فشل في إلغاء التفعيل المجمع: ${error.message}`);
    }
  },

  /**
   * حذف عدة خصومات
   */
  async bulkDelete(ids) {
    try {
      const response = await apiClient.post('/api/discounts/bulk-delete', { ids });
      return response;
    } catch (error) {
      throw new Error(`فشل في الحذف المجمع: ${error.message}`);
    }
  }
};

export default discountService;
