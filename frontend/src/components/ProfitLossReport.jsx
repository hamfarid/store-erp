import React, { useState, useEffect } from 'react';
import {
  Search, Calendar, TrendingUp, TrendingDown, DollarSign, Download, FileText, Filter, BarChart3
} from 'lucide-react';

const ProfitLossReport = () => {
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [reportType, setReportType] = useState('monthly');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [year, setYear] = useState(new Date().getFullYear());
  const [month, setMonth] = useState(new Date().getMonth() + 1);

  useEffect(() => {
    // Set default dates
    const today = new Date();
    const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
    const lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0);
    
    setStartDate(firstDay.toISOString().split('T')[0]);
    setEndDate(lastDay.toISOString().split('T')[0]);
  }, []);

  const loadReport = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      
      let url = 'http://localhost:5002/api/accounting/profit-loss';
      const params = new URLSearchParams();
      
      if (reportType === 'monthly') {
        params.append('year', year);
        params.append('month', month);
      } else if (reportType === 'yearly') {
        params.append('year', year);
      } else if (reportType === 'custom') {
        params.append('start_date', startDate);
        params.append('end_date', endDate);
      }
      
      url += `?${params.toString()}`;
      
      const response = await fetch(url, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        setReportData(data.data || data);
      } else {
        alert('حدث خطأ أثناء تحميل التقرير');
      }
      
      setLoading(false);
    } catch (error) {
      console.error('Error loading report:', error);
      setLoading(false);
      alert('حدث خطأ أثناء تحميل التقرير');
    }
  };

  const handleGenerateReport = () => {
    loadReport();
  };

  const handleExport = () => {
    if (!reportData) return;
    
    // Export as JSON for now - can be enhanced to Excel/PDF
    const dataStr = JSON.stringify(reportData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `profit-loss-report-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
  };

  const calculateNetProfit = () => {
    if (!reportData) return 0;
    const revenue = reportData.total_revenue || 0;
    const expenses = reportData.total_expenses || 0;
    return revenue - expenses;
  };

  const calculateProfitMargin = () => {
    if (!reportData || !reportData.total_revenue) return 0;
    const netProfit = calculateNetProfit();
    return (netProfit / reportData.total_revenue) * 100;
  };

  return (
    <div className="p-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">تقرير الأرباح والخسائر</h1>
          <p className="text-gray-600 mt-1">تحليل الإيرادات والمصروفات</p>
        </div>
        {reportData && (
          <button
            onClick={handleExport}
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg flex items-center gap-2 transition-colors"
          >
            <Download className="w-5 h-5" />
            تصدير التقرير
          </button>
        )}
      </div>

      {/* Report Controls */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">نوع التقرير</label>
            <select
              value={reportType}
              onChange={(e) => setReportType(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="monthly">شهري</option>
              <option value="yearly">سنوي</option>
              <option value="custom">مخصص</option>
            </select>
          </div>

          {reportType === 'monthly' && (
            <>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">السنة</label>
                <input
                  type="number"
                  value={year}
                  onChange={(e) => setYear(parseInt(e.target.value))}
                  min="2020"
                  max="2099"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">الشهر</label>
                <select
                  value={month}
                  onChange={(e) => setMonth(parseInt(e.target.value))}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  {Array.from({ length: 12 }, (_, i) => (
                    <option key={i + 1} value={i + 1}>
                      {new Date(2000, i).toLocaleDateString('ar-EG', { month: 'long' })}
                    </option>
                  ))}
                </select>
              </div>
            </>
          )}

          {reportType === 'yearly' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">السنة</label>
              <input
                type="number"
                value={year}
                onChange={(e) => setYear(parseInt(e.target.value))}
                min="2020"
                max="2099"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
          )}

          {reportType === 'custom' && (
            <>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">من تاريخ</label>
                <input
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">إلى تاريخ</label>
                <input
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </>
          )}

          <div className="flex items-end">
            <button
              onClick={handleGenerateReport}
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-2 rounded-lg flex items-center justify-center gap-2 transition-colors"
            >
              <BarChart3 className="w-5 h-5" />
              {loading ? 'جاري التحميل...' : 'إنشاء التقرير'}
            </button>
          </div>
        </div>
      </div>

      {loading && (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500"></div>
        </div>
      )}

      {!loading && !reportData && (
        <div className="bg-white rounded-lg shadow-md p-12 text-center">
          <BarChart3 className="w-20 h-20 mx-auto text-gray-400 mb-4" />
          <p className="text-gray-600 text-lg mb-4">اختر الفترة الزمنية وانقر على "إنشاء التقرير"</p>
          <p className="text-gray-500 text-sm">سيتم عرض تحليل الأرباح والخسائر هنا</p>
        </div>
      )}

      {!loading && reportData && (
        <>
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm mb-1">إجمالي الإيرادات</p>
                  <p className="text-2xl font-bold text-green-600">
                    {(reportData.total_revenue || 0).toFixed(2)}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">ج.م</p>
                </div>
                <TrendingUp className="w-12 h-12 text-green-500" />
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm mb-1">إجمالي المصروفات</p>
                  <p className="text-2xl font-bold text-red-600">
                    {(reportData.total_expenses || 0).toFixed(2)}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">ج.م</p>
                </div>
                <TrendingDown className="w-12 h-12 text-red-500" />
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm mb-1">صافي الربح / الخسارة</p>
                  <p className={`text-2xl font-bold ${
                    calculateNetProfit() >= 0 ? 'text-blue-600' : 'text-red-600'
                  }`}>
                    {calculateNetProfit().toFixed(2)}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">ج.م</p>
                </div>
                <DollarSign className="w-12 h-12 text-blue-500" />
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm mb-1">هامش الربح</p>
                  <p className={`text-2xl font-bold ${
                    calculateProfitMargin() >= 0 ? 'text-blue-600' : 'text-red-600'
                  }`}>
                    {calculateProfitMargin().toFixed(2)}%
                  </p>
                  <p className="text-xs text-gray-500 mt-1">نسبة مئوية</p>
                </div>
                <BarChart3 className="w-12 h-12 text-blue-500" />
              </div>
            </div>
          </div>

          {/* Revenue Breakdown */}
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <TrendingUp className="w-6 h-6 text-green-600" />
              تفاصيل الإيرادات
            </h2>
            <div className="space-y-3">
              {reportData.revenue_breakdown && reportData.revenue_breakdown.length > 0 ? (
                reportData.revenue_breakdown.map((item, index) => (
                  <div key={index} className="flex justify-between items-center p-4 bg-green-50 rounded-lg">
                    <div>
                      <p className="font-medium text-gray-800">{item.category}</p>
                      <p className="text-sm text-gray-600">{item.description}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-lg font-bold text-green-600">{item.amount.toFixed(2)} ج.م</p>
                      <p className="text-xs text-gray-600">
                        {((item.amount / reportData.total_revenue) * 100).toFixed(1)}%
                      </p>
                    </div>
                  </div>
                ))
              ) : (
                <>
                  <div className="flex justify-between items-center p-4 bg-green-50 rounded-lg">
                    <span className="font-medium">إيرادات المبيعات</span>
                    <span className="text-lg font-bold text-green-600">
                      {(reportData.sales_revenue || 0).toFixed(2)} ج.م
                    </span>
                  </div>
                  <div className="flex justify-between items-center p-4 bg-green-50 rounded-lg">
                    <span className="font-medium">إيرادات أخرى</span>
                    <span className="text-lg font-bold text-green-600">
                      {(reportData.other_revenue || 0).toFixed(2)} ج.م
                    </span>
                  </div>
                </>
              )}
            </div>
          </div>

          {/* Expenses Breakdown */}
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <TrendingDown className="w-6 h-6 text-red-600" />
              تفاصيل المصروفات
            </h2>
            <div className="space-y-3">
              {reportData.expense_breakdown && reportData.expense_breakdown.length > 0 ? (
                reportData.expense_breakdown.map((item, index) => (
                  <div key={index} className="flex justify-between items-center p-4 bg-red-50 rounded-lg">
                    <div>
                      <p className="font-medium text-gray-800">{item.category}</p>
                      <p className="text-sm text-gray-600">{item.description}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-lg font-bold text-red-600">{item.amount.toFixed(2)} ج.م</p>
                      <p className="text-xs text-gray-600">
                        {((item.amount / reportData.total_expenses) * 100).toFixed(1)}%
                      </p>
                    </div>
                  </div>
                ))
              ) : (
                <>
                  <div className="flex justify-between items-center p-4 bg-red-50 rounded-lg">
                    <span className="font-medium">تكلفة البضاعة المباعة</span>
                    <span className="text-lg font-bold text-red-600">
                      {(reportData.cost_of_goods_sold || 0).toFixed(2)} ج.م
                    </span>
                  </div>
                  <div className="flex justify-between items-center p-4 bg-red-50 rounded-lg">
                    <span className="font-medium">مصاريف تشغيلية</span>
                    <span className="text-lg font-bold text-red-600">
                      {(reportData.operating_expenses || 0).toFixed(2)} ج.م
                    </span>
                  </div>
                  <div className="flex justify-between items-center p-4 bg-red-50 rounded-lg">
                    <span className="font-medium">مصاريف أخرى</span>
                    <span className="text-lg font-bold text-red-600">
                      {(reportData.other_expenses || 0).toFixed(2)} ج.م
                    </span>
                  </div>
                </>
              )}
            </div>
          </div>

          {/* Net Profit/Loss Summary */}
          <div className={`rounded-lg shadow-md p-8 text-center ${
            calculateNetProfit() >= 0 
              ? 'bg-gradient-to-r from-blue-50 to-green-50' 
              : 'bg-gradient-to-r from-red-50 to-orange-50'
          }`}>
            <h2 className="text-2xl font-bold text-gray-800 mb-4">النتيجة النهائية</h2>
            <div className="flex items-center justify-center gap-4">
              {calculateNetProfit() >= 0 ? (
                <TrendingUp className="w-16 h-16 text-green-600" />
              ) : (
                <TrendingDown className="w-16 h-16 text-red-600" />
              )}
              <div>
                <p className="text-sm text-gray-600 mb-1">
                  {calculateNetProfit() >= 0 ? 'صافي الربح' : 'صافي الخسارة'}
                </p>
                <p className={`text-5xl font-bold ${
                  calculateNetProfit() >= 0 ? 'text-blue-600' : 'text-red-600'
                }`}>
                  {Math.abs(calculateNetProfit()).toFixed(2)} ج.م
                </p>
                <p className="text-sm text-gray-600 mt-2">
                  هامش الربح: {calculateProfitMargin().toFixed(2)}%
                </p>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default ProfitLossReport;
