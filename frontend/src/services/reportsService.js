/**
 * خدمة نظام التقارير
 */
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

const reportsService = {
  // ==================== Sales Reports ====================
  
  /**
   * تقرير ملخص المبيعات
   */
  async getSalesSummary(startDate, endDate) {
    const response = await axios.get(`${API_URL}/api/reports/sales/summary`, {
      params: { start_date: startDate, end_date: endDate }
    });
    return response.data;
  },

  /**
   * تقرير المبيعات حسب المنتج
   */
  async getSalesByProduct(startDate, endDate) {
    const response = await axios.get(`${API_URL}/api/reports/sales/by-product`, {
      params: { start_date: startDate, end_date: endDate }
    });
    return response.data;
  },

  /**
   * تقرير المبيعات حسب العميل
   */
  async getSalesByCustomer(startDate, endDate) {
    const response = await axios.get(`${API_URL}/api/reports/sales/by-customer`, {
      params: { start_date: startDate, end_date: endDate }
    });
    return response.data;
  },

  // ==================== Inventory Reports ====================
  
  /**
   * تقرير مستويات المخزون
   */
  async getStockLevels(lowStockOnly = false) {
    const response = await axios.get(`${API_URL}/api/reports/inventory/stock-levels`, {
      params: { low_stock_only: lowStockOnly }
    });
    return response.data;
  },

  /**
   * تقرير اللوطات قريبة الانتهاء
   */
  async getExpiringLots(days = 30) {
    const response = await axios.get(`${API_URL}/api/reports/inventory/expiring-lots`, {
      params: { days }
    });
    return response.data;
  },

  // ==================== Financial Reports ====================
  
  /**
   * تقرير الأرباح والخسائر
   */
  async getProfitLoss(startDate, endDate) {
    const response = await axios.get(`${API_URL}/api/reports/financial/profit-loss`, {
      params: { start_date: startDate, end_date: endDate }
    });
    return response.data;
  },

  // ==================== Shift Reports ====================
  
  /**
   * تقرير أداء الورديات
   */
  async getShiftsPerformance(startDate, endDate) {
    const response = await axios.get(`${API_URL}/api/reports/shifts/performance`, {
      params: { start_date: startDate, end_date: endDate }
    });
    return response.data;
  },

  // ==================== Dashboard ====================
  
  /**
   * إحصائيات لوحة التحكم
   */
  async getDashboardStats() {
    const response = await axios.get(`${API_URL}/api/reports/dashboard/stats`);
    return response.data;
  },

  // ==================== Export ====================
  
  /**
   * تصدير تقرير إلى Excel
   */
  async exportToExcel(reportType, params = {}) {
    const response = await axios.get(`${API_URL}/api/reports/export/${reportType}`, {
      params,
      responseType: 'blob'
    });
    
    // إنشاء رابط تحميل
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${reportType}_${new Date().toISOString()}.xlsx`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    
    return { success: true };
  },

  /**
   * طباعة تقرير
   */
  printReport(reportData, reportTitle) {
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
      <html>
        <head>
          <title>${reportTitle}</title>
          <style>
            body { font-family: Arial, sans-serif; direction: rtl; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: right; }
            th { background-color: #f2f2f2; }
            h1 { text-align: center; }
            @media print {
              button { display: none; }
            }
          </style>
        </head>
        <body>
          <h1>${reportTitle}</h1>
          <button onclick="window.print()">طباعة</button>
          ${reportData}
        </body>
      </html>
    `);
    printWindow.document.close();
  }
};

export default reportsService;
