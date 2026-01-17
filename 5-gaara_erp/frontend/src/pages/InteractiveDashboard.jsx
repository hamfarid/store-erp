import React, { useState, useEffect } from 'react';

const InteractiveDashboard = () => {
  const [stats, setStats] = useState({
    totalProducts: 0,
    totalSales: 0,
    totalPurchases: 0,
    lowStock: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setStats({
        totalProducts: 1250,
        totalSales: 85000,
        totalPurchases: 65000,
        lowStock: 15
      });
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل لوحة المعلومات...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-foreground">لوحة المعلومات التفاعلية</h1>
        <p className="text-muted-foreground">نظرة شاملة على أداء النظام</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg shadow-lg p-6 text-white" data-testid="metric-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-100 font-semibold">إجمالي المنتجات</p>
              <p className="text-3xl font-bold text-white mt-2">{stats.totalProducts.toLocaleString()}</p>
            </div>
            <div className="text-primary/30">
              <svg className="w-12 h-12" fill="currentColor" viewBox="0 0 20 20">
                <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"></path>
              </svg>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-r from-green-500 to-green-600 rounded-lg shadow-lg p-6 text-white" data-testid="metric-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100">إجمالي المبيعات</p>
              <p className="text-3xl font-bold">{stats.totalSales.toLocaleString()} ج.م</p>
            </div>
            <div className="text-green-200">
              <svg className="w-12 h-12" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"></path>
              </svg>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg shadow-lg p-6 text-white" data-testid="metric-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-100">إجمالي المشتريات</p>
              <p className="text-3xl font-bold">{stats.totalPurchases.toLocaleString()} ج.م</p>
            </div>
            <div className="text-purple-200">
              <svg className="w-12 h-12" fill="currentColor" viewBox="0 0 20 20">
                <path d="M3 1a1 1 0 000 2h1.22l.305 1.222a.997.997 0 00.01.042l1.358 5.43-.893.892C3.74 11.846 4.632 14 6.414 14H15a1 1 0 000-2H6.414l1-1H14a1 1 0 00.894-.553l3-6A1 1 0 0017 3H6.28l-.31-1.243A1 1 0 005 1H3zM16 16.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zM6.5 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"></path>
              </svg>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-r from-red-500 to-red-600 rounded-lg shadow-lg p-6 text-white" data-testid="metric-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-red-100">مخزون منخفض</p>
              <p className="text-3xl font-bold">{stats.lowStock}</p>
            </div>
            <div className="text-red-200">
              <svg className="w-12 h-12" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd"></path>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-foreground mb-4">أحدث المعاملات</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
              <div>
                <p className="font-semibold">فاتورة مبيعات #001</p>
                <p className="text-sm text-muted-foreground">عميل: شركة الأحمد</p>
              </div>
              <span className="text-primary font-bold">+5,000 ج.م</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
              <div>
                <p className="font-semibold">فاتورة شراء #002</p>
                <p className="text-sm text-muted-foreground">مورد: شركة التقنية</p>
              </div>
              <span className="text-destructive font-bold">-3,500 ج.م</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
              <div>
                <p className="font-semibold">تعديل مخزون</p>
                <p className="text-sm text-muted-foreground">المخزن الرئيسي</p>
              </div>
              <span className="text-primary font-bold">جرد دوري</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-foreground mb-4">تنبيهات النظام</h3>
          <div className="space-y-4">
            <div className="flex items-center p-3 bg-accent/10 border-l-4 border-yellow-400 rounded">
              <div className="flex-shrink-0">
                <svg className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd"></path>
                </svg>
              </div>
              <div className="mr-3">
                <p className="text-sm font-medium text-yellow-800">مخزون منخفض</p>
                <p className="text-sm text-yellow-700">15 منتج يحتاج إعادة تموين</p>
              </div>
            </div>
            <div className="flex items-center p-3 bg-primary/10 border-l-4 border-primary/50 rounded">
              <div className="flex-shrink-0">
                <svg className="w-5 h-5 text-primary/50" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd"></path>
                </svg>
              </div>
              <div className="mr-3">
                <p className="text-sm font-medium text-primary/95">تحديث النظام</p>
                <p className="text-sm text-primary/90">إصدار جديد متاح للتحميل</p>
              </div>
            </div>
            <div className="flex items-center p-3 bg-primary/10 border-l-4 border-green-400 rounded">
              <div className="flex-shrink-0">
                <svg className="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path>
                </svg>
              </div>
              <div className="mr-3">
                <p className="text-sm font-medium text-green-800">نسخ احتياطي</p>
                <p className="text-sm text-primary">تم إنشاء النسخة الاحتياطية بنجاح</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InteractiveDashboard;

