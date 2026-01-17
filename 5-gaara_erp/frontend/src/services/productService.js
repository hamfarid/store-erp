/**
 * خدمة إدارة المنتجات
 * /home/ubuntu/upload/store_v1.1/complete_inventory_system/frontend/src/services/productService.js
 */

import apiClient from './apiClient';

export const productService = {
  // ==================== العمليات الأساسية ====================

  /**
   * الحصول على جميع المنتجات
   */
  async getAll(params = {}) {
    try {
      const queryParams = {
        page: params.page || 1,
        limit: params.limit || 50,
        search: params.search || '',
        category_id: params.categoryId || '',
        warehouse_id: params.warehouseId || '',
        is_active: params.isActive !== undefined ? params.isActive : '',
        sort_by: params.sortBy || 'name',
        sort_order: params.sortOrder || 'asc',
        ...params
      };

      const response = await apiClient.get('/api/products', queryParams);
      return {
        products: response.products || response.data || [],
        total: response.total || 0,
        page: response.page || 1,
        totalPages: response.total_pages || Math.ceil((response.total || 0) / (params.limit || 50)),
      };
    } catch (error) {
      throw new Error(`فشل في تحميل المنتجات: ${error.message}`);
    }
  },

  /**
   * الحصول على منتج بالمعرف
   */
  async getById(id) {
    try {
      const response = await apiClient.get(`/api/products/${id}`);
      return response.product || response;
    } catch (error) {
      throw new Error(`فشل في تحميل المنتج: ${error.message}`);
    }
  },

  /**
   * إنشاء منتج جديد
   */
  async create(productData) {
    try {
      const response = await apiClient.post('/api/products', productData);
      return response.product || response;
    } catch (error) {
      throw new Error(`فشل في إنشاء المنتج: ${error.message}`);
    }
  },

  /**
   * تحديث منتج
   */
  async update(id, productData) {
    try {
      const response = await apiClient.put(`/api/products/${id}`, productData);
      return response.product || response;
    } catch (error) {
      throw new Error(`فشل في تحديث المنتج: ${error.message}`);
    }
  },

  /**
   * حذف منتج
   */
  async delete(id) {
    try {
      const response = await apiClient.delete(`/api/products/${id}`);
      return response;
    } catch (error) {
      throw new Error(`فشل في حذف المنتج: ${error.message}`);
    }
  },

  // ==================== العمليات المتقدمة ====================

  /**
   * البحث في المنتجات
   */
  async search(query, filters = {}) {
    try {
      const params = {
        q: query,
        category_id: filters.categoryId,
        warehouse_id: filters.warehouseId,
        min_price: filters.minPrice,
        max_price: filters.maxPrice,
        in_stock: filters.inStock,
        ...filters
      };

      const response = await apiClient.get('/api/products/search', params);
      return response.products || response.data || [];
    } catch (error) {
      throw new Error(`فشل في البحث: ${error.message}`);
    }
  },

  /**
   * الحصول على منتجات حسب الفئة
   */
  async getByCategory(categoryId, params = {}) {
    try {
      const response = await apiClient.get(`/api/products/category/${categoryId}`, params);
      return response.products || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل منتجات الفئة: ${error.message}`);
    }
  },

  /**
   * الحصول على منتجات حسب المخزن
   */
  async getByWarehouse(warehouseId, params = {}) {
    try {
      const response = await apiClient.get(`/api/products/warehouse/${warehouseId}`, params);
      return response.products || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل منتجات المخزن: ${error.message}`);
    }
  },

  // ==================== إدارة المخزون ====================

  /**
   * تحديث كمية المخزون
   */
  async updateStock(id, stockData) {
    try {
      const response = await apiClient.post(`/api/products/${id}/stock`, stockData);
      return response;
    } catch (error) {
      throw new Error(`فشل في تحديث المخزون: ${error.message}`);
    }
  },

  /**
   * الحصول على تاريخ حركات المخزون
   */
  async getStockHistory(id, params = {}) {
    try {
      const response = await apiClient.get(`/api/products/${id}/stock-history`, params);
      return response.movements || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل تاريخ المخزون: ${error.message}`);
    }
  },

  /**
   * الحصول على المنتجات منخفضة المخزون
   */
  async getLowStock(params = {}) {
    try {
      const response = await apiClient.get('/api/products/low-stock', params);
      return response.products || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل المنتجات منخفضة المخزون: ${error.message}`);
    }
  },

  /**
   * الحصول على المنتجات منتهية الصلاحية
   */
  async getExpired(params = {}) {
    try {
      const response = await apiClient.get('/api/products/expired', params);
      return response.products || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل المنتجات منتهية الصلاحية: ${error.message}`);
    }
  },

  // ==================== إدارة الأسعار ====================

  /**
   * تحديث سعر المنتج
   */
  async updatePrice(id, priceData) {
    try {
      const response = await apiClient.post(`/api/products/${id}/price`, priceData);
      return response;
    } catch (error) {
      throw new Error(`فشل في تحديث السعر: ${error.message}`);
    }
  },

  /**
   * الحصول على تاريخ الأسعار
   */
  async getPriceHistory(id, params = {}) {
    try {
      const response = await apiClient.get(`/api/products/${id}/price-history`, params);
      return response.prices || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل تاريخ الأسعار: ${error.message}`);
    }
  },

  // ==================== إدارة الصور ====================

  /**
   * رفع صورة المنتج
   */
  async uploadImage(id, imageFile) {
    try {
      const response = await apiClient.uploadFile(
        `/api/products/${id}/image`, 
        imageFile
      );
      return response;
    } catch (error) {
      throw new Error(`فشل في رفع الصورة: ${error.message}`);
    }
  },

  /**
   * حذف صورة المنتج
   */
  async deleteImage(id, imageId) {
    try {
      const response = await apiClient.delete(`/api/products/${id}/images/${imageId}`);
      return response;
    } catch (error) {
      throw new Error(`فشل في حذف الصورة: ${error.message}`);
    }
  },

  // ==================== التقارير ====================

  /**
   * تقرير المنتجات الأكثر مبيعاً
   */
  async getTopSelling(params = {}) {
    try {
      const response = await apiClient.get('/api/products/reports/top-selling', params);
      return response.products || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل المنتجات الأكثر مبيعاً: ${error.message}`);
    }
  },

  /**
   * تقرير ربحية المنتجات
   */
  async getProfitability(params = {}) {
    try {
      const response = await apiClient.get('/api/products/reports/profitability', params);
      return response.products || response.data || [];
    } catch (error) {
      throw new Error(`فشل في تحميل تقرير الربحية: ${error.message}`);
    }
  },

  // ==================== الاستيراد والتصدير ====================

  /**
   * تصدير المنتجات إلى Excel
   */
  async exportToExcel(_params = {}) {
    try {
      await apiClient.downloadFile('/api/products/export/excel', 'products.xlsx');
    } catch (error) {
      throw new Error(`فشل في تصدير المنتجات: ${error.message}`);
    }
  },

  /**
   * استيراد المنتجات من Excel
   */
  async importFromExcel(file) {
    try {
      const response = await apiClient.uploadFile('/api/products/import/excel', file);
      return response;
    } catch (error) {
      throw new Error(`فشل في استيراد المنتجات: ${error.message}`);
    }
  },

  /**
   * تحميل قالب Excel للاستيراد
   */
  async downloadImportTemplate() {
    try {
      await apiClient.downloadFile('/api/products/import/template', 'products_template.xlsx');
    } catch (error) {
      throw new Error(`فشل في تحميل القالب: ${error.message}`);
    }
  },

  // ==================== العمليات المجمعة ====================

  /**
   * تحديث عدة منتجات
   */
  async bulkUpdate(updates) {
    try {
      const response = await apiClient.post('/api/products/bulk-update', { updates });
      return response;
    } catch (error) {
      throw new Error(`فشل في التحديث المجمع: ${error.message}`);
    }
  },

  /**
   * حذف عدة منتجات
   */
  async bulkDelete(ids) {
    try {
      const response = await apiClient.post('/api/products/bulk-delete', { ids });
      return response;
    } catch (error) {
      throw new Error(`فشل في الحذف المجمع: ${error.message}`);
    }
  },

  // ==================== التحقق من صحة البيانات ====================

  /**
   * التحقق من وجود باركود
   */
  async checkBarcodeExists(barcode, excludeId = null) {
    try {
      const params = { barcode };
      if (excludeId) params.exclude_id = excludeId;
      
      const response = await apiClient.get('/api/products/check-barcode', params);
      return response.exists || false;
    } catch (error) {
      return false;
    }
  },

  /**
   * التحقق من صحة بيانات المنتج
   */
  async validateProduct(productData) {
    try {
      const response = await apiClient.post('/api/products/validate', productData);
      return response;
    } catch (error) {
      throw new Error(`فشل في التحقق من البيانات: ${error.message}`);
    }
  }
};

export default productService;

