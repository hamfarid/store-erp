import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const InventoryAnalysis = () => {
  const [inventoryData, setInventoryData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchInventoryData();
  }, []);

  const fetchInventoryData = async () => {
    try {
      const response = await fetch('http://localhost:5002/api/reports/inventory-analysis');
      const result = await response.json();
      if (result.success) {
        setInventoryData(result.data);
      }
    } catch (error) {
      console.error('خطأ في جلب بيانات المخزون:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center p-8">جاري تحميل تحليل المخزون...</div>;
  }

  if (!inventoryData) {
    return <div className="text-center p-8">لا توجد بيانات متاحة</div>;
  }

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];
  const stockLevelsData = Object.entries(inventoryData.stock_levels).map(([key, value]) => ({
    name: key === 'high_stock' ? 'مخزون عالي' : 
          key === 'medium_stock' ? 'مخزون متوسط' :
          key === 'low_stock' ? 'مخزون منخفض' : 'نفد المخزون',
    value
  }));

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">تحليل المخزون المتقدم</h2>
      
      {/* إحصائيات سريعة */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-blue-800">إجمالي المنتجات</h3>
          <p className="text-2xl font-bold text-blue-600">{inventoryData.total_products}</p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-green-800">قيمة المخزون</h3>
          <p className="text-2xl font-bold text-green-600">{inventoryData.total_value.toLocaleString()} ر.س</p>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-yellow-800">مخزون منخفض</h3>
          <p className="text-2xl font-bold text-yellow-600">{inventoryData.low_stock_items}</p>
        </div>
        <div className="bg-red-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-red-800">نفد المخزون</h3>
          <p className="text-2xl font-bold text-red-600">{inventoryData.out_of_stock_items}</p>
        </div>
      </div>

      {/* توزيع الفئات */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div>
          <h3 className="text-xl font-semibold mb-4">توزيع الفئات</h3>
          <BarChart width={400} height={300} data={inventoryData.categories_breakdown}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="category" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="count" fill="#8884d8" />
          </BarChart>
        </div>

        <div>
          <h3 className="text-xl font-semibold mb-4">مستويات المخزون</h3>
          <PieChart width={400} height={300}>
            <Pie
              data={stockLevelsData}
              cx={200}
              cy={150}
              labelLine={false}
              label={({name, percent}) => `${name} ${(percent * 100).toFixed(0)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {stockLevelsData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </div>
      </div>
    </div>
  );
};

export default InventoryAnalysis;