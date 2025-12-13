/**
 * Purchase Service
 * خدمة المشتريات
 */

import api from './api';

const purchaseService = {
  /**
   * الحصول على قائمة أوامر الشراء
   */
  async getPurchaseOrders(params = {}) {
    try {
      const response = await api.get('/purchases', { params });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * الحصول على تفاصيل أمر شراء
   */
  async getPurchaseOrder(poId) {
    try {
      const response = await api.get(`/purchases/${poId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * إنشاء أمر شراء جديد
   */
  async createPurchaseOrder(data) {
    try {
      const response = await api.post('/purchases', data);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * تحديث أمر شراء
   */
  async updatePurchaseOrder(poId, data) {
    try {
      const response = await api.put(`/purchases/${poId}`, data);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * حذف أمر شراء
   */
  async deletePurchaseOrder(poId) {
    try {
      const response = await api.delete(`/purchases/${poId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * اعتماد أمر شراء
   */
  async approvePurchaseOrder(poId) {
    try {
      const response = await api.post(`/purchases/${poId}/approve`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * استلام أمر شراء
   */
  async receivePurchaseOrder(poId, data) {
    try {
      const response = await api.post(`/purchases/${poId}/receive`, data);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * ربط اللوطات بعناصر أمر الشراء
   */
  async linkBatches(poId, itemsBatches) {
    try {
      const response = await api.post(`/purchases/${poId}/link-batches`, {
        items_batches: itemsBatches
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * الحصول على إحصائيات المشتريات
   */
  async getStatistics() {
    try {
      const response = await api.get('/purchases/statistics');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * البحث عن أوامر الشراء
   */
  async searchPurchaseOrders(query) {
    try {
      const response = await api.get('/purchases', {
        params: { search: query }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * تصدير أوامر الشراء
   */
  async exportPurchaseOrders(format = 'excel', filters = {}) {
    try {
      const response = await api.get('/purchases/export', {
        params: { format, ...filters },
        responseType: 'blob'
      });
      
      // إنشاء رابط للتحميل
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `purchase_orders_${Date.now()}.${format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      return { success: true };
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * الحصول على أوامر الشراء المعلقة
   */
  async getPendingOrders() {
    try {
      const response = await api.get('/purchases', {
        params: { status: 'pending' }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * الحصول على أوامر الشراء المتأخرة
   */
  async getOverdueOrders() {
    try {
      const response = await api.get('/purchases/overdue');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * حساب إجمالي أمر الشراء
   */
  calculateTotal(items) {
    let total = 0;
    
    items.forEach(item => {
      const quantity = parseFloat(item.quantity) || 0;
      const unitPrice = parseFloat(item.unit_price) || 0;
      const discountPercentage = parseFloat(item.discount_percentage) || 0;
      const taxPercentage = parseFloat(item.tax_percentage) || 0;
      
      // السعر الأساسي
      const baseTotal = quantity * unitPrice;
      
      // الخصم
      const discountAmount = baseTotal * (discountPercentage / 100);
      const afterDiscount = baseTotal - discountAmount;
      
      // الضريبة
      const taxAmount = afterDiscount * (taxPercentage / 100);
      const finalPrice = afterDiscount + taxAmount;
      
      total += finalPrice;
    });
    
    return total;
  },

  /**
   * التحقق من صحة عناصر أمر الشراء
   */
  validateItems(items) {
    const errors = [];
    
    if (!items || items.length === 0) {
      errors.push('يجب إضافة عنصر واحد على الأقل');
      return { valid: false, errors };
    }
    
    items.forEach((item, index) => {
      if (!item.product_id) {
        errors.push(`العنصر ${index + 1}: المنتج مطلوب`);
      }
      
      if (!item.quantity || item.quantity <= 0) {
        errors.push(`العنصر ${index + 1}: الكمية يجب أن تكون أكبر من صفر`);
      }
      
      if (!item.unit_price || item.unit_price <= 0) {
        errors.push(`العنصر ${index + 1}: سعر الوحدة يجب أن يكون أكبر من صفر`);
      }
    });
    
    return {
      valid: errors.length === 0,
      errors
    };
  },

  /**
   * تنسيق بيانات أمر الشراء للعرض
   */
  formatPurchaseOrder(po) {
    return {
      ...po,
      order_date: po.order_date ? new Date(po.order_date).toLocaleDateString('ar-EG') : '-',
      expected_date: po.expected_date ? new Date(po.expected_date).toLocaleDateString('ar-EG') : '-',
      received_date: po.received_date ? new Date(po.received_date).toLocaleDateString('ar-EG') : '-',
      total_amount: parseFloat(po.total_amount || 0).toFixed(2),
      status_label: this.getStatusLabel(po.status)
    };
  },

  /**
   * الحصول على تسمية الحالة
   */
  getStatusLabel(status) {
    const labels = {
      'draft': 'مسودة',
      'pending': 'معلق',
      'approved': 'معتمد',
      'ordered': 'تم الطلب',
      'partial': 'استلام جزئي',
      'received': 'مستلم',
      'cancelled': 'ملغي'
    };
    
    return labels[status] || status;
  },

  /**
   * الحصول على لون الحالة
   */
  getStatusColor(status) {
    const colors = {
      'draft': 'gray',
      'pending': 'yellow',
      'approved': 'blue',
      'ordered': 'cyan',
      'partial': 'orange',
      'received': 'green',
      'cancelled': 'red'
    };
    
    return colors[status] || 'gray';
  }
};

export default purchaseService;
