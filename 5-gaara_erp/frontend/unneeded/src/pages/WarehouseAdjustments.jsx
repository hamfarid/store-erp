import React, { useState, useEffect } from 'react';

const WarehouseAdjustments = () => {
  const [adjustments, setAdjustments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // محاكاة تحميل البيانات
    setTimeout(() => {
      setAdjustments([
        {
          id: 1,
          adjustmentNumber: 'ADJ-001',
          warehouse: 'المخزن الرئيسي',
          type: 'زيادة',
          reason: 'جرد دوري',
          status: 'مكتمل',
          date: '2024-01-15',
          items: 5,
          totalValue: 2500
        },
        {
          id: 2,
          adjustmentNumber: 'ADJ-002',
          warehouse: 'مخزن الإلكترونيات',
          type: 'نقص',
          reason: 'تلف',
          status: 'معلق',
          date: '2024-01-14',
          items: 3,
          totalValue: -1200
        }
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل تعديلات المخازن...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow-lg">
        <div className="px-6 py-4 border-b border-border">
          <h1 className="text-2xl font-bold text-foreground">تعديلات المخازن</h1>
          <p className="text-muted-foreground">إدارة تعديلات المخزون والجرد</p>
        </div>
        
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div className="bg-primary/10 p-4 rounded-lg">
              <h3 className="text-lg font-semibold text-primary/95">إجمالي التعديلات</h3>
              <p className="text-2xl font-bold text-primary">{adjustments.length}</p>
            </div>
            <div className="bg-primary/10 p-4 rounded-lg">
              <h3 className="text-lg font-semibold text-green-800">التعديلات المكتملة</h3>
              <p className="text-2xl font-bold text-primary">
                {adjustments.filter(adj => adj.status === 'مكتمل').length}
              </p>
            </div>
            <div className="bg-accent/10 p-4 rounded-lg">
              <h3 className="text-lg font-semibold text-yellow-800">التعديلات المعلقة</h3>
              <p className="text-2xl font-bold text-accent">
                {adjustments.filter(adj => adj.status === 'معلق').length}
              </p>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border border-border">
              <thead className="bg-muted/50">
                <tr>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    رقم التعديل
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    المخزن
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    النوع
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    السبب
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    الحالة
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    التاريخ
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    عدد الأصناف
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    القيمة الإجمالية
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {adjustments.map((adjustment) => (
                  <tr key={adjustment.id} className="hover:bg-muted/50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-foreground">
                      {adjustment.adjustmentNumber}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {adjustment.warehouse}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        adjustment.type === 'زيادة' 
                          ? 'bg-primary/20 text-green-800' 
                          : 'bg-destructive/20 text-red-800'
                      }`}>
                        {adjustment.type}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {adjustment.reason}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        adjustment.status === 'مكتمل' 
                          ? 'bg-primary/20 text-green-800' 
                          : 'bg-accent/20 text-yellow-800'
                      }`}>
                        {adjustment.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {adjustment.date}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {adjustment.items}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <span className={adjustment.totalValue >= 0 ? 'text-primary' : 'text-destructive'}>
                        {adjustment.totalValue.toLocaleString()} ج.م
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WarehouseAdjustments;

