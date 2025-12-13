import React, { useState, useEffect } from 'react';
import {
  Search, Filter, Plus, Edit, Trash2, Eye, Download, Upload, Settings, CheckCircle, XCircle, AlertTriangle, Package, User, Calendar, Clock
} from 'lucide-react';

const LotManagementAdvanced = () => {
  const [lots, setLots] = useState([]);
  const [products, setProducts] = useState([]);
  const [warehouses, setWarehouses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedProduct, setSelectedProduct] = useState('');
  const [selectedWarehouse, setSelectedWarehouse] = useState('');
  const [statusFilter, setStatusFilter] = useState('active');
  const [showAddModal, setShowAddModal] = useState(false);
  const [showExpiringAlert, setShowExpiringAlert] = useState(false);
  const [expiringLots, setExpiringLots] = useState([]);

  // عرض تفاصيل اللوط
  const handleViewLot = (lot) => {
    alert(
      `عرض تفاصيل اللوط: ${lot.lot_number}\n\n` +
      `المنتج: ${lot.product_name} (${lot.product_sku})\n` +
      `المخزن: ${lot.warehouse_name}\n` +
      `الكمية: ${lot.quantity}\n` +
      `تاريخ الإنتاج: ${lot.production_date}\n` +
      `تاريخ الانتهاء: ${lot.expiry_date}\n` +
      `المورد: ${lot.supplier_name}\n` +
      `درجة الجودة: ${lot.quality_grade}\n` +
      `الحالة: ${lot.status === 'active' ? 'نشط' : lot.status === 'expired' ? 'منتهي' : 'مستهلك'}\n` +
      `الأيام المتبقية: ${lot.days_to_expiry} يوم`
    );
  };

  // بيانات تجريبية للوتات
  const demoLots = [
    {
      id: 1,
      lot_number: 'LOT-2024-001',
      product_name: 'بذور طماطم هجين',
      product_sku: 'TOM-HYB-001',
      warehouse_name: 'المخزن الرئيسي',
      quantity: 50,
      unit_cost: 25.50,
      production_date: '2024-01-15',
      expiry_date: '2024-12-15',
      supplier_name: 'شركة البذور المصرية',
      quality_grade: 'ممتاز',
      status: 'active',
      days_to_expiry: 160
    },
    {
      id: 2,
      lot_number: 'LOT-2024-002',
      product_name: 'سماد NPK متوازن',
      product_sku: 'NPK-BAL-001',
      warehouse_name: 'مخزن الإسكندرية',
      quantity: 25,
      unit_cost: 45.00,
      production_date: '2024-02-01',
      expiry_date: '2024-08-01',
      supplier_name: 'مصنع الأسمدة الحديث',
      quality_grade: 'جيد',
      status: 'active',
      days_to_expiry: 25
    },
    {
      id: 3,
      lot_number: 'LOT-2024-003',
      product_name: 'مبيد حشري طبيعي',
      product_sku: 'INS-NAT-001',
      warehouse_name: 'المخزن الرئيسي',
      quantity: 15,
      unit_cost: 85.00,
      production_date: '2024-03-01',
      expiry_date: '2024-07-15',
      supplier_name: 'شركة المبيدات المتقدمة',
      quality_grade: 'ممتاز',
      status: 'active',
      days_to_expiry: 7
    }
  ];

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      // محاكاة تحميل البيانات
      setTimeout(() => {
        setLots(demoLots);
        setProducts([
          { id: 1, name: 'بذور طماطم هجين', sku: 'TOM-HYB-001' },
          { id: 2, name: 'سماد NPK متوازن', sku: 'NPK-BAL-001' },
          { id: 3, name: 'مبيد حشري طبيعي', sku: 'INS-NAT-001' }
        ]);
        setWarehouses([
          { id: 1, name: 'المخزن الرئيسي' },
          { id: 2, name: 'مخزن الإسكندرية' }
        ]);
        
        // فحص اللوطات قريبة الانتهاء
        const expiring = demoLots.filter(lot => lot.days_to_expiry <= 30);
        setExpiringLots(expiring);
        if (expiring.length > 0) {
          setShowExpiringAlert(true);
        }
        
        setLoading(false);
      }, 1000);
    } catch (error) {
      setLoading(false);
    }
  };

  const filteredLots = lots.filter(lot => {
    const matchesSearch = lot.lot_number.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         lot.product_name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesProduct = !selectedProduct || lot.product_sku === selectedProduct;
    const matchesWarehouse = !selectedWarehouse || lot.warehouse_name === selectedWarehouse;
    const matchesStatus = lot.status === statusFilter;
    
    return matchesSearch && matchesProduct && matchesWarehouse && matchesStatus;
  });

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-primary/20 text-green-800';
      case 'expired': return 'bg-destructive/20 text-red-800';
      case 'consumed': return 'bg-muted text-foreground';
      default: return 'bg-primary-100 text-primary-800';
    }
  };

  const getExpiryColor = (daysToExpiry) => {
    if (daysToExpiry <= 7) return 'text-destructive font-bold';
    if (daysToExpiry <= 30) return 'text-accent font-semibold';
    return 'text-primary';
  };

  const AddLotModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">إضافة لوت جديد</h3>
          <button
            onClick={() => setShowAddModal(false)}
            className="text-gray-500 hover:text-foreground"
          >
            ✕
          </button>
        </div>
        
        <form className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">
                رقم اللوت *
              </label>
              <input
                type="text"
                className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="LOT-2024-004"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">
                المنتج *
              </label>
              <select className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500">
                <option value="">اختر المنتج</option>
                {products.map(product => (
                  <option key={product.id} value={product.id}>
                    {product.name} ({product.sku})
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">
                المخزن *
              </label>
              <select className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500">
                <option value="">اختر المخزن</option>
                {warehouses.map(warehouse => (
                  <option key={warehouse.id} value={warehouse.id}>
                    {warehouse.name}
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">
                الكمية *
              </label>
              <input
                type="number"
                className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="100"
                min="0"
                step="0.01"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">
                تكلفة الوحدة
              </label>
              <input
                type="number"
                className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="25.50"
                min="0"
                step="0.01"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">
                تاريخ الإنتاج
              </label>
              <input
                type="date"
                className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">
                تاريخ الانتهاء
              </label>
              <input
                type="date"
                className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">
                درجة الجودة
              </label>
              <select className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500">
                <option value="ممتاز">ممتاز</option>
                <option value="جيد جداً">جيد جداً</option>
                <option value="جيد">جيد</option>
                <option value="مقبول">مقبول</option>
              </select>
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-foreground mb-1">
              ملاحظات
            </label>
            <textarea
              className="w-full px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              rows="3"
              placeholder="ملاحظات إضافية..."
            ></textarea>
          </div>
          
          <div className="flex justify-end space-x-2 space-x-reverse">
            <button
              type="button"
              onClick={() => setShowAddModal(false)}
              className="px-4 py-2 text-muted-foreground bg-muted rounded-md hover:bg-muted"
            >
              إلغاء
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
            >
              حفظ اللوت
            </button>
          </div>
        </form>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="p-6">
      {/* تنبيه اللوطات قريبة الانتهاء */}
      {showExpiringAlert && expiringLots.length > 0 && (
        <div className="mb-6 bg-accent/10 border-l-4 border-orange-400 p-4 rounded-md">
          <div className="flex items-center">
            <AlertTriangle className="h-5 w-5 text-orange-400 ml-2" />
            <div>
              <h3 className="text-sm font-medium text-orange-800">
                تنبيه: يوجد {expiringLots.length} لوت قريب من الانتهاء
              </h3>
              <div className="mt-2 text-sm text-orange-700">
                {expiringLots.map(lot => (
                  <div key={lot.id} className="mb-1">
                    {lot.lot_number} - {lot.product_name} (ينتهي خلال {lot.days_to_expiry} يوم)
                  </div>
                ))}
              </div>
            </div>
            <button
              onClick={() => setShowExpiringAlert(false)}
              className="mr-auto text-orange-400 hover:text-accent"
            >
              ✕
            </button>
          </div>
        </div>
      )}

      {/* رأس الصفحة */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-foreground">إدارة اللوطات المتقدمة</h1>
          <p className="text-muted-foreground">تتبع وإدارة جميع لوتات المنتجات</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 flex items-center"
        >
          <Plus className="h-4 w-4 ml-2" />
          إضافة لوت جديد
        </button>
      </div>

      {/* أدوات البحث والفلترة */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="relative">
            <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <input
              type="text"
              placeholder="البحث برقم اللوت أو المنتج..."
              className="w-full pr-10 pl-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <select
            className="px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            value={selectedProduct}
            onChange={(e) => setSelectedProduct(e.target.value)}
          >
            <option value="">جميع المنتجات</option>
            {products.map(product => (
              <option key={product.sku} value={product.sku}>
                {product.name}
              </option>
            ))}
          </select>
          
          <select
            className="px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            value={selectedWarehouse}
            onChange={(e) => setSelectedWarehouse(e.target.value)}
          >
            <option value="">جميع المخازن</option>
            {warehouses.map(warehouse => (
              <option key={warehouse.name} value={warehouse.name}>
                {warehouse.name}
              </option>
            ))}
          </select>
          
          <select
            className="px-3 py-2 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="active">نشط</option>
            <option value="expired">منتهي الصلاحية</option>
            <option value="consumed">مستهلك</option>
          </select>
        </div>
      </div>

      {/* جدول اللوطات */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-muted/50">
              <tr>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  رقم اللوت
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  المنتج
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  المخزن
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  الكمية
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  تاريخ الانتهاء
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  الجودة
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  الحالة
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  الإجراءات
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredLots.map((lot) => (
                <tr key={lot.id} className="hover:bg-muted/50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-foreground">
                    {lot.lot_number}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-foreground">{lot.product_name}</div>
                    <div className="text-sm text-gray-500">{lot.product_sku}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                    {lot.warehouse_name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                    {lot.quantity.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className={`text-sm ${getExpiryColor(lot.days_to_expiry)}`}>
                      {lot.expiry_date}
                    </div>
                    <div className="text-xs text-gray-500">
                      ({lot.days_to_expiry} يوم متبقي)
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                    {lot.quality_grade}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(lot.status)}`}>
                      {lot.status === 'active' ? 'نشط' : lot.status === 'expired' ? 'منتهي' : 'مستهلك'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex space-x-2 space-x-reverse">
                      <button 
                        onClick={() => handleViewLot(lot)}
                        className="text-primary-600 hover:text-primary-900 p-2 rounded-lg hover:bg-blue-50 transition-colors"
                        title="عرض التفاصيل"
                      >
                        <Eye className="h-4 w-4" />
                      </button>
                      <button 
                        onClick={() => {
                          alert('سيتم فتح نموذج التعديل قريباً');
                        }}
                        className="text-green-600 hover:text-green-900 p-2 rounded-lg hover:bg-green-50 transition-colors"
                        title="تعديل اللوط"
                      >
                        <Edit className="h-4 w-4" />
                      </button>
                      <button 
                        onClick={() => {
                          if (window.confirm(`هل أنت متأكد من حذف اللوط ${lot.lot_number}؟`)) {
                            alert('سيتم تنفيذ الحذف عبر API');
                          }
                        }}
                        className="text-red-600 hover:text-red-900 p-2 rounded-lg hover:bg-red-50 transition-colors"
                        title="حذف اللوط"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* إحصائيات سريعة */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center">
            <Package className="h-8 w-8 text-primary-600" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">إجمالي اللوطات</p>
              <p className="text-2xl font-bold text-foreground">{lots.length}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center">
            <Calendar className="h-8 w-8 text-primary" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">اللوطات النشطة</p>
              <p className="text-2xl font-bold text-foreground">
                {lots.filter(lot => lot.status === 'active').length}
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center">
            <AlertTriangle className="h-8 w-8 text-accent" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">قريبة الانتهاء</p>
              <p className="text-2xl font-bold text-foreground">{expiringLots.length}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="flex items-center">
            <Download className="h-8 w-8 text-purple-600" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">إجمالي الكمية</p>
              <p className="text-2xl font-bold text-foreground">
                {lots.reduce((sum, lot) => sum + lot.quantity, 0).toLocaleString()}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* نافذة إضافة لوت */}
      {showAddModal && <AddLotModal />}
    </div>
  );
};

export default LotManagementAdvanced;

