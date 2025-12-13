// خدمة API للتعامل مع الخادم الخلفي
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

// قائمة بالخوادم البديلة للاتصال
const FALLBACK_URLS = [
  'http://172.16.16.27:8000/api',
  'http://172.31.0.1:8000/api',
  'http://localhost:8000/api',
  'http://127.0.0.1:8000/api'
]

class ApiService {
  static currentBaseUrl = API_BASE_URL
  static connectionTested = false

  // اختبار الاتصال بالخادم
  static async testConnection(baseUrl = API_BASE_URL) {
    try {
      const response = await fetch(`${baseUrl}/health`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        signal: AbortSignal.timeout(5000) // 5 second timeout
      })
      return response.ok
    } catch (error) {
      return false
    }
  }

  // العثور على خادم متاح
  static async findAvailableServer() {
    if (this.connectionTested) {
      return this.currentBaseUrl
    }

    // اختبار الخادم الحالي أولاً
    if (await this.testConnection(this.currentBaseUrl)) {
      this.connectionTested = true
      return this.currentBaseUrl
    }

    // اختبار الخوادم البديلة
    for (const url of FALLBACK_URLS) {
      if (url !== this.currentBaseUrl && await this.testConnection(url)) {
        this.currentBaseUrl = url
        this.connectionTested = true
        return url
      }
    }

    // إذا فشل جميع الخوادم، استخدم الافتراضي
    this.connectionTested = true
    return this.currentBaseUrl
  }

  // الحصول على رؤوس المصادقة
  static getHeaders() {
    const token = localStorage.getItem('token')
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    }
  }

  // الحصول على خيارات الطلب مع الكوكيز
  static getRequestOptions(method = 'GET', data = null) {
    const options = {
      method,
      headers: this.getHeaders(),
      credentials: 'same-origin', // تغيير من include إلى same-origin
    }

    if (data) {
      options.body = JSON.stringify(data)
    }

    return options
  }

  // معالج الأخطاء العام
  static async handleResponse(response) {
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`)
    }
    return response.json()
  }

  // طلب GET عام
  static async get(endpoint) {
    try {
      const baseUrl = await this.findAvailableServer()
      const response = await fetch(`${baseUrl}${endpoint}`, this.getRequestOptions('GET'))
      return await this.handleResponse(response)
    } catch (error) {
      // إعادة تعيين حالة الاتصال للمحاولة مرة أخرى
      this.connectionTested = false
      throw error
    }
  }

  // طلب POST عام
  static async post(endpoint, data) {
    try {
      const baseUrl = await this.findAvailableServer()
      const response = await fetch(`${baseUrl}${endpoint}`, this.getRequestOptions('POST', data))
      return await this.handleResponse(response)
    } catch (error) {
      // إعادة تعيين حالة الاتصال للمحاولة مرة أخرى
      this.connectionTested = false
      throw error
    }
  }

  // طلب PUT عام
  static async put(endpoint, data) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, this.getRequestOptions('PUT', data))
    return await this.handleResponse(response)
  }

  // طلب DELETE عام
  static async delete(endpoint) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, this.getRequestOptions('DELETE'))
    return await this.handleResponse(response)
  }

  // فحص حالة الخادم
  static async healthCheck() {
    return this.get('/health')
  }

  // تسجيل الدخول
  static async login(credentials) {
    return this.post('/user/login', credentials)
  }

  // تسجيل الخروج
  static async logout() {
    return this.post('/user/logout', {})
  }

  // الحصول على ملف المستخدم
  static async getProfile() {
    return this.get('/user/profile')
  }

  // APIs المنتجات
  static async getProducts() {
    return this.get('/products')
  }

  static async createProduct(productData) {
    return this.post('/products', productData)
  }

  static async updateProduct(id, productData) {
    return this.put(`/products/${id}`, productData)
  }

  static async deleteProduct(id) {
    return this.delete(`/products/${id}`)
  }

  static async getLowStockProducts() {
    return this.get('/products/low-stock')
  }

  // APIs التصنيفات والمجموعات والمراتب
  static async getCategories() {
    return this.get('/categories')
  }

  static async createCategory(categoryData) {
    return this.post('/categories', categoryData)
  }

  static async updateCategory(id, categoryData) {
    return this.put(`/categories/${id}`, categoryData)
  }

  static async deleteCategory(id) {
    return this.delete(`/categories/${id}`)
  }

  static async getProductGroups() {
    return this.get('/product-groups')
  }

  static async createProductGroup(groupData) {
    return this.post('/product-groups', groupData)
  }

  static async updateProductGroup(id, groupData) {
    return this.put(`/product-groups/${id}`, groupData)
  }

  static async deleteProductGroup(id) {
    return this.delete(`/product-groups/${id}`)
  }

  static async getRanks() {
    return this.get('/ranks')
  }

  static async createRank(rankData) {
    return this.post('/ranks', rankData)
  }

  static async updateRank(id, rankData) {
    return this.put(`/ranks/${id}`, rankData)
  }

  static async deleteRank(id) {
    return this.delete(`/ranks/${id}`)
  }

  // APIs الإحصائيات
  static async getOverviewStats() {
    return this.get('/stats/overview')
  }

  static async getRecentMovements() {
    return this.get('/stats/movements/recent')
  }

  static async getProductsByCategory() {
    return this.get('/stats/products/categories')
  }

  // APIs العملاء (محاكاة - يمكن تطويرها لاحقاً)
  static async getCustomers() {
    // محاكاة بيانات العملاء
    return new Promise(resolve => {
      setTimeout(() => {
        resolve({
          success: true,
          data: [
            {
              id: 1,
              name: 'مزرعة النيل',
              contact_person: 'خالد حسن',
              phone: '01234567890',
              email: 'khaled@nilfarm.com',
              address: 'المنيا، مصر'
            },
            {
              id: 2,
              name: 'شركة الزراعة الحديثة',
              contact_person: 'فاطمة محمود',
              phone: '01234567891',
              email: 'fatma@modern-agri.com',
              address: 'بني سويف، مصر'
            }
          ]
        })
      }, 500)
    })
  }

  // APIs الموردين (محاكاة - يمكن تطويرها لاحقاً)
  static async getSuppliers() {
    // محاكاة بيانات الموردين
    return new Promise(resolve => {
      setTimeout(() => {
        resolve({
          success: true,
          data: [
            {
              id: 1,
              name: 'شركة البذور المصرية',
              contact_person: 'أحمد محمد',
              phone: '01234567893',
              email: 'ahmed@seeds.com',
              address: 'القاهرة، مصر',
              category: 'بذور'
            },
            {
              id: 2,
              name: 'مؤسسة الأسمدة الحديثة',
              contact_person: 'محمد علي',
              phone: '01234567894',
              email: 'mohamed@fertilizers.com',
              address: 'الجيزة، مصر',
              category: 'أسمدة'
            }
          ]
        })
      }, 500)
    })
  }

  // استيراد البيانات
  static async importData(file, type = 'products') {
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('type', type)

      const response = await fetch(`${API_BASE_URL}/import/data`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          // لا نضع Content-Type للـ FormData
          'Authorization': localStorage.getItem('token') ? `Bearer ${localStorage.getItem('token')}` : ''
        },
        body: formData
      })

      return await this.handleResponse(response)
    } catch (error) {
      console.error('Import error:', error);
      throw error;
    }
  }

  // تصدير البيانات
  static async exportData(type = 'products', format = 'excel') {
    try {
      const response = await fetch(`${API_BASE_URL}/export/data?type=${type}&format=${format}`, {
        method: 'GET',
        credentials: 'include',
        headers: this.getHeaders()
      })

      if (!response.ok) {
        throw new Error(`Export failed: ${response.status}`)
      }

      // إنشاء blob من الاستجابة
      const blob = await response.blob()

      // إنشاء رابط تحميل
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url

      // تحديد اسم الملف بناءً على النوع والتنسيق
      const timestamp = new Date().toISOString().split('T')[0]
      const extension = format === 'pdf' ? 'pdf' : 'xlsx'
      link.download = `${type}_export_${timestamp}.${extension}`

      // تحميل الملف
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)

      return { success: true, message: 'تم تصدير البيانات بنجاح' }
    } catch (error) {
      console.error('Export error:', error);
      throw error;
    }
  }

  // تصدير تقرير PDF
  static async exportPDF(reportType = 'inventory') {
    return this.exportData(reportType, 'pdf')
  }

  // تصدير Excel
  static async exportExcel(dataType = 'products') {
    return this.exportData(dataType, 'excel')
  }

  // استيراد ملف Excel
  static async importExcel(file, dataType = 'products') {
    return this.importData(file, dataType)
  }

  // APIs أنواع العملاء
  static async getCustomerTypes() {
    return this.get('/customer-types')
  }

  static async createCustomerType(data) {
    return this.post('/customer-types', data)
  }

  static async updateCustomerType(id, data) {
    return this.put(`/customer-types/${id}`, data)
  }

  static async deleteCustomerType(id) {
    return this.delete(`/customer-types/${id}`)
  }

  // APIs أنواع الموردين
  static async getSupplierTypes() {
    return this.get('/supplier-types')
  }

  static async createSupplierType(data) {
    return this.post('/supplier-types', data)
  }

  static async updateSupplierType(id, data) {
    return this.put(`/supplier-types/${id}`, data)
  }

  static async deleteSupplierType(id) {
    return this.delete(`/supplier-types/${id}`)
  }
}

export default ApiService

