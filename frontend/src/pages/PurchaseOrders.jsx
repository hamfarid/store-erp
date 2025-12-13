import React, { useState, useEffect } from 'react';
import {
  ShoppingCart, Plus, Search, Filter, Eye, Edit, Trash2, Check, X,
  FileText, Truck, Calendar, DollarSign, Package, Clock, CheckCircle, AlertTriangle
} from 'lucide-react';
import { toast } from 'react-hot-toast';
import apiClient from '../services/apiClient';

// UI Components
import { Badge } from '../components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow
} from '../components/ui/table';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue
} from '../components/ui/select';

/**
 * صفحة أوامر الشراء
 * Purchase Orders Page
 */
const PurchaseOrders = () => {
  const [orders, setOrders] = useState([]);
  const [filteredOrders, setFilteredOrders] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [isLoading, setIsLoading] = useState(true);

  // بيانات نموذجية
  const sampleOrders = [
    {
      id: 1,
      order_number: 'PO-2024-001',
      supplier_id: 1,
      supplier_name: 'شركة المستلزمات التقنية',
      order_date: '2024-01-15',
      expected_date: '2024-01-25',
      received_date: null,
      status: 'pending',
      items_count: 5,
      total_amount: 25000,
      paid_amount: 0,
      notes: 'طلب عاجل',
      created_by: 'admin'
    },
    {
      id: 2,
      order_number: 'PO-2024-002',
      supplier_id: 2,
      supplier_name: 'مؤسسة الإمداد',
      order_date: '2024-01-14',
      expected_date: '2024-01-20',
      received_date: '2024-01-19',
      status: 'received',
      items_count: 8,
      total_amount: 45000,
      paid_amount: 45000,
      notes: '',
      created_by: 'admin'
    },
    {
      id: 3,
      order_number: 'PO-2024-003',
      supplier_id: 3,
      supplier_name: 'شركة التوريدات العامة',
      order_date: '2024-01-13',
      expected_date: '2024-01-23',
      received_date: null,
      status: 'approved',
      items_count: 3,
      total_amount: 15000,
      paid_amount: 7500,
      notes: 'تم الموافقة',
      created_by: 'manager'
    },
    {
      id: 4,
      order_number: 'PO-2024-004',
      supplier_id: 1,
      supplier_name: 'شركة المستلزمات التقنية',
      order_date: '2024-01-12',
      expected_date: '2024-01-22',
      received_date: null,
      status: 'cancelled',
      items_count: 2,
      total_amount: 8000,
      paid_amount: 0,
      notes: 'ملغي بسبب تغيير الأسعار',
      created_by: 'admin'
    },
    {
      id: 5,
      order_number: 'PO-2024-005',
      supplier_id: 4,
      supplier_name: 'مصنع الأدوات',
      order_date: '2024-01-10',
      expected_date: '2024-01-15',
      received_date: '2024-01-14',
      status: 'partial',
      items_count: 10,
      total_amount: 75000,
      paid_amount: 50000,
      notes: 'تم استلام جزئي',
      created_by: 'admin'
    }
  ];

  const statusConfig = {
    draft: { label: 'مسودة', color: 'bg-gray-100 text-gray-800', icon: FileText },
    pending: { label: 'قيد الانتظار', color: 'bg-yellow-100 text-yellow-800', icon: Clock },
    approved: { label: 'موافق عليه', color: 'bg-blue-100 text-blue-800', icon: Check },
    ordered: { label: 'تم الطلب', color: 'bg-purple-100 text-purple-800', icon: ShoppingCart },
    partial: { label: 'استلام جزئي', color: 'bg-orange-100 text-orange-800', icon: Package },
    received: { label: 'تم الاستلام', color: 'bg-green-100 text-green-800', icon: CheckCircle },
    cancelled: { label: 'ملغي', color: 'bg-red-100 text-red-800', icon: X }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.get('/api/purchase-orders');
      if (response.success && response.data?.length > 0) {
        setOrders(response.data);
        setFilteredOrders(response.data);
      } else {
        setOrders(sampleOrders);
        setFilteredOrders(sampleOrders);
      }
    } catch (error) {
      console.log('Using sample data:', error);
      setOrders(sampleOrders);
      setFilteredOrders(sampleOrders);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let filtered = orders;

    if (searchTerm) {
      filtered = filtered.filter(order =>
        order.order_number.toLowerCase().includes(searchTerm.toLowerCase()) ||
        order.supplier_name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterStatus !== 'all') {
      filtered = filtered.filter(order => order.status === filterStatus);
    }

    setFilteredOrders(filtered);
  }, [orders, searchTerm, filterStatus]);

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('ar-SA', {
      style: 'currency',
      currency: 'SAR',
      minimumFractionDigits: 0
    }).format(amount);
  };

  const getStatusBadge = (status) => {
    const config = statusConfig[status] || statusConfig.draft;
    const Icon = config.icon;
    return (
      <span className={`inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full ${config.color}`}>
        <Icon className="w-3 h-3" />
        {config.label}
      </span>
    );
  };

  const handleStatusChange = (orderId, newStatus) => {
    setOrders(orders.map(o =>
      o.id === orderId ? { ...o, status: newStatus } : o
    ));
    toast.success(`تم تحديث حالة الطلب إلى: ${statusConfig[newStatus]?.label}`);
  };

  const handleDelete = (orderId) => {
    if (window.confirm('هل أنت متأكد من حذف أمر الشراء؟')) {
      setOrders(orders.filter(o => o.id !== orderId));
      toast.success('تم حذف أمر الشراء');
    }
  };

  // Calculate summary
  const summary = {
    total: orders.length,
    pending: orders.filter(o => o.status === 'pending').length,
    approved: orders.filter(o => o.status === 'approved').length,
    received: orders.filter(o => o.status === 'received').length,
    totalValue: orders.filter(o => o.status !== 'cancelled').reduce((sum, o) => sum + o.total_amount, 0),
    unpaid: orders.filter(o => o.status !== 'cancelled').reduce((sum, o) => sum + (o.total_amount - o.paid_amount), 0)
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">جاري التحميل...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground flex items-center gap-2">
            <ShoppingCart className="w-8 h-8" />
            أوامر الشراء
          </h1>
          <p className="text-muted-foreground mt-1">إدارة طلبات الشراء من الموردين</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors">
          <Plus className="w-4 h-4" />
          أمر شراء جديد
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي الأوامر</p>
                <p className="text-2xl font-bold text-primary">{summary.total}</p>
              </div>
              <ShoppingCart className="w-8 h-8 text-primary/60" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">قيد الانتظار</p>
                <p className="text-2xl font-bold text-yellow-600">{summary.pending}</p>
              </div>
              <Clock className="w-8 h-8 text-yellow-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">موافق عليها</p>
                <p className="text-2xl font-bold text-blue-600">{summary.approved}</p>
              </div>
              <Check className="w-8 h-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">تم الاستلام</p>
                <p className="text-2xl font-bold text-green-600">{summary.received}</p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي القيمة</p>
                <p className="text-lg font-bold text-purple-600">{formatCurrency(summary.totalValue)}</p>
              </div>
              <DollarSign className="w-8 h-8 text-purple-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">غير مدفوع</p>
                <p className="text-lg font-bold text-red-600">{formatCurrency(summary.unpaid)}</p>
              </div>
              <AlertTriangle className="w-8 h-8 text-red-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-wrap gap-4">
            <div className="flex-1 min-w-64">
              <Label htmlFor="search">البحث</Label>
              <div className="relative">
                <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
                <Input
                  id="search"
                  placeholder="البحث برقم الأمر أو المورد..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>

            <div className="min-w-40">
              <Label htmlFor="status-filter">الحالة</Label>
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger>
                  <SelectValue placeholder="الكل" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">الكل</SelectItem>
                  {Object.entries(statusConfig).map(([key, config]) => (
                    <SelectItem key={key} value={key}>{config.label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Orders Table */}
      <Card>
        <CardHeader>
          <CardTitle>قائمة أوامر الشراء ({filteredOrders.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>رقم الأمر</TableHead>
                <TableHead>المورد</TableHead>
                <TableHead>تاريخ الطلب</TableHead>
                <TableHead>تاريخ التوصيل المتوقع</TableHead>
                <TableHead>المنتجات</TableHead>
                <TableHead>المبلغ</TableHead>
                <TableHead>المدفوع</TableHead>
                <TableHead>الحالة</TableHead>
                <TableHead>الإجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredOrders.map((order) => (
                <TableRow key={order.id} className={order.status === 'cancelled' ? 'opacity-60' : ''}>
                  <TableCell>
                    <div className="font-mono font-bold">{order.order_number}</div>
                  </TableCell>
                  <TableCell>
                    <div className="font-medium">{order.supplier_name}</div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Calendar className="w-3 h-3 text-muted-foreground" />
                      {new Date(order.order_date).toLocaleDateString('ar-SA')}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Truck className="w-3 h-3 text-muted-foreground" />
                      {new Date(order.expected_date).toLocaleDateString('ar-SA')}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline">{order.items_count} منتج</Badge>
                  </TableCell>
                  <TableCell className="font-mono font-bold">
                    {formatCurrency(order.total_amount)}
                  </TableCell>
                  <TableCell>
                    <div className="space-y-1">
                      <span className={order.paid_amount >= order.total_amount ? 'text-green-600' : 'text-orange-600'}>
                        {formatCurrency(order.paid_amount)}
                      </span>
                      {order.paid_amount < order.total_amount && (
                        <div className="text-xs text-red-600">
                          متبقي: {formatCurrency(order.total_amount - order.paid_amount)}
                        </div>
                      )}
                    </div>
                  </TableCell>
                  <TableCell>
                    {getStatusBadge(order.status)}
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-1">
                      <button className="p-2 hover:bg-muted rounded" title="عرض التفاصيل">
                        <Eye className="w-4 h-4" />
                      </button>
                      {order.status !== 'cancelled' && order.status !== 'received' && (
                        <>
                          <button className="p-2 hover:bg-muted rounded" title="تعديل">
                            <Edit className="w-4 h-4" />
                          </button>
                          {order.status === 'pending' && (
                            <button
                              onClick={() => handleStatusChange(order.id, 'approved')}
                              className="p-2 text-green-600 hover:bg-green-50 rounded"
                              title="موافقة"
                            >
                              <Check className="w-4 h-4" />
                            </button>
                          )}
                          {(order.status === 'approved' || order.status === 'partial') && (
                            <button
                              onClick={() => handleStatusChange(order.id, 'received')}
                              className="p-2 text-blue-600 hover:bg-blue-50 rounded"
                              title="تأكيد الاستلام"
                            >
                              <Package className="w-4 h-4" />
                            </button>
                          )}
                        </>
                      )}
                      {order.status === 'pending' && (
                        <button
                          onClick={() => handleStatusChange(order.id, 'cancelled')}
                          className="p-2 text-red-600 hover:bg-red-50 rounded"
                          title="إلغاء"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>

          {filteredOrders.length === 0 && (
            <div className="text-center py-8">
              <ShoppingCart className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">لا توجد أوامر شراء</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default PurchaseOrders;

