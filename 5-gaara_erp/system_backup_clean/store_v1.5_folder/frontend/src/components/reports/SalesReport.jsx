import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, PieChart, Pie, Cell, LineChart, Line } from 'recharts';

const SalesReport = () => {
  const [salesData, setSalesData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSalesData();
  }, []);

  const fetchSalesData = async () => {
    try {
      const response = await fetch('http://localhost:5002/api/reports/sales-summary');
      const result = await response.json();
      if (result.success) {
        setSalesData(result.data);
      }
    } catch (error) {
      console.error('خطأ في جلب بيانات المبيعات:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center p-8">جاري تحميل تقرير المبيعات...</div>;
  }

  if (!salesData) {
    return <div className="text-center p-8">لا توجد بيانات متاحة</div>;
  }

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">تقرير المبيعات المتقدم</h2>
      
      {/* إحصائيات سريعة */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-blue-800">إجمالي المبيعات</h3>
          <p className="text-3xl font-bold text-blue-600">{salesData.total_sales.toLocaleString()} ر.س</p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-green-800">عدد الطلبات</h3>
          <p className="text-3xl font-bold text-green-600">{salesData.total_orders}</p>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-purple-800">متوسط قيمة الطلب</h3>
          <p className="text-3xl font-bold text-purple-600">{salesData.average_order_value} ر.س</p>
        </div>
      </div>

      {/* أفضل المنتجات */}
      <div className="mb-8">
        <h3 className="text-xl font-semibold mb-4">أفضل المنتجات مبيعاً</h3>
        <BarChart width={600} height={300} data={salesData.top_products}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="sales" fill="#8884d8" />
        </BarChart>
      </div>

      {/* الاتجاه الشهري */}
      <div>
        <h3 className="text-xl font-semibold mb-4">اتجاه المبيعات الشهرية</h3>
        <LineChart width={600} height={300} data={salesData.monthly_trend}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="sales" stroke="#8884d8" strokeWidth={2} />
        </LineChart>
      </div>
    </div>
  );
};

export default SalesReport;