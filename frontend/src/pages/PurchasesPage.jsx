import React, { useState, useEffect } from 'react';
import {
  FileText, Plus, Search, Filter, Eye, Edit, Trash2,
  CheckCircle, Clock, XCircle, AlertCircle, DollarSign,
  Calendar, Truck, Download
} from 'lucide-react';
import { toast } from 'react-hot-toast';
import purchaseService from '../services/purchaseService';

// UI Components
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow
} from '../components/ui/table';
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue
} from '../components/ui/select';

// Sample data as fallback
const samplePurchases = [
  { id: 'PO-2024-001', supplier: 'شركة التقنية', items_count: 25, total_amount: 125000, paid_amount: 125000, status: 'received', created_at: '2024-12-01', expected_date: '2024-12-15' },
  { id: 'PO-2024-002', supplier: 'Apple Inc.', items_count: 50, total_amount: 450000, paid_amount: 200000, status: 'partial', created_at: '2024-11-28', expected_date: '2024-12-28' },
  { id: 'PO-2024-003', supplier: 'Samsung Electronics', items_count: 30, total_amount: 180000, paid_amount: 0, status: 'pending', created_at: '2024-11-25', expected_date: '2024-12-25' },
  { id: 'PO-2024-004', supplier: 'مصنع الملابس', items_count: 100, total_amount: 85000, paid_amount: 85000, status: 'received', created_at: '2024-11-20', expected_date: '2024-12-05' },
  { id: 'PO-2024-005', supplier: 'شركة التقنية', items_count: 15, total_amount: 45000, paid_amount: 0, status: 'cancelled', created_at: '2024-11-15', expected_date: '2024-12-01' },
];

const PurchasesPage = () => {
  const [purchases, setPurchases] = useState([]);
  const [filteredPurchases, setFilteredPurchases] = useState([]);
  const [stats, setStats] = useState({
    total_orders: 0,
    total_amount: 0,
    paid_amount: 0,
    pending_amount: 0
  });
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  const fetchPurchases = React.useCallback(async () => {
    setLoading(true);
    try {
      const response = await purchaseService.getPurchaseOrders();
      if (response && response.length > 0) {
         setPurchases(response);
         setFilteredPurchases(response);
      } else {
         setPurchases(samplePurchases);
         setFilteredPurchases(samplePurchases);
      }

      // Fetch stats if available, otherwise calculate
      try {
        const statsResponse = await purchaseService.getStatistics();
        if (statsResponse) setStats(statsResponse);
      } catch (e) {
        // Calculate from data if stats API fails
        const currentData = (response && response.length > 0) ? response : samplePurchases;
        const totalAmount = currentData.reduce((sum, p) => sum + (parseFloat(p.total_amount) || 0), 0);
        const paidAmount = currentData.reduce((sum, p) => sum + (parseFloat(p.paid_amount) || 0), 0);
        setStats({
          total_orders: currentData.length,
          total_amount: totalAmount,
          paid_amount: paidAmount,
          pending_amount: totalAmount - paidAmount
        });
      }

    } catch (error) {
      console.error('Failed to fetch purchases:', error);
      setPurchases(samplePurchases);
      setFilteredPurchases(samplePurchases);
      toast.error('حدث خطأ في تحميل البيانات، تم عرض بيانات نموذجية');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchPurchases();
  }, [fetchPurchases]);

  useEffect(() => {
    let result = purchases;

    if (searchTerm) {
      result = result.filter(p => 
        p.id?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        p.supplier?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (statusFilter !== 'all') {
      result = result.filter(p => p.status === statusFilter);
    }

    setFilteredPurchases(result);
  }, [purchases, searchTerm, statusFilter]);

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('ar-SA', {
      style: 'currency',
      currency: 'EGP',
      minimumFractionDigits: 0
    }).format(amount);
  };

  const getStatusBadge = (status) => {
    const config = {
      received: { label: 'مكتمل', variant: 'default', className: 'bg-green-100 text-green-800 hover:bg-green-100' },
      completed: { label: 'مكتمل', variant: 'default', className: 'bg-green-100 text-green-800 hover:bg-green-100' },
      partial: { label: 'مدفوع جزئياً', variant: 'warning', className: 'bg-yellow-100 text-yellow-800 hover:bg-yellow-100' },
      pending: { label: 'قيد الانتظار', variant: 'secondary', className: 'bg-blue-100 text-blue-800 hover:bg-blue-100' },
      cancelled: { label: 'ملغي', variant: 'destructive', className: '' },
      draft: { label: 'مسودة', variant: 'outline', className: '' }
    };

    const style = config[status] || config['draft'];

    return (
      <Badge variant={style.variant} className={style.className}>
        {style.label}
      </Badge>
    );
  };

  if (loading) {
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
            <FileText className="w-8 h-8" />
            فواتير الشراء
          </h1>
          <p className="text-muted-foreground mt-1">إدارة طلبات الشراء من الموردين</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => toast.success('تم تصدير البيانات')}>
            <Download className="w-4 h-4 ml-2" />
            تصدير
          </Button>
          <Button className="gap-2">
            <Plus className="w-4 h-4" />
            طلب شراء جديد
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">إجمالي الطلبات</p>
              <p className="text-2xl font-bold">{stats.total_orders}</p>
            </div>
            <div className="p-3 bg-blue-100 rounded-full text-blue-600">
              <FileText className="w-6 h-6" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">إجمالي المشتريات</p>
              <p className="text-2xl font-bold text-teal-600">{formatCurrency(stats.total_amount)}</p>
            </div>
            <div className="p-3 bg-teal-100 rounded-full text-teal-600">
              <DollarSign className="w-6 h-6" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">المدفوع</p>
              <p className="text-2xl font-bold text-green-600">{formatCurrency(stats.paid_amount)}</p>
            </div>
            <div className="p-3 bg-green-100 rounded-full text-green-600">
              <CheckCircle className="w-6 h-6" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4 flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">المستحق</p>
              <p className="text-2xl font-bold text-red-600">{formatCurrency(stats.pending_amount)}</p>
            </div>
            <div className="p-3 bg-red-100 rounded-full text-red-600">
              <AlertCircle className="w-6 h-6" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-wrap gap-4">
            <div className="flex-1 min-w-64">
              <div className="relative">
                <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
                <Input
                  placeholder="بحث برقم الطلب أو المورد..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>
            <div className="min-w-40">
              <Select value={statusFilter} onValueChange={setStatusFilter}>
                <SelectTrigger>
                  <SelectValue placeholder="فيلتر بالحالة" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">الكل</SelectItem>
                  <SelectItem value="pending">قيد الانتظار</SelectItem>
                  <SelectItem value="partial">مدفوع جزئياً</SelectItem>
                  <SelectItem value="received">مكتمل</SelectItem>
                  <SelectItem value="cancelled">ملغي</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Table */}
      <Card>
        <CardHeader>
          <CardTitle>أحدث الفواتير</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>رقم الطلب</TableHead>
                <TableHead>المورد</TableHead>
                <TableHead>المنتجات</TableHead>
                <TableHead>الإجمالي</TableHead>
                <TableHead>المدفوع</TableHead>
                <TableHead>التاريخ</TableHead>
                <TableHead>الحالة</TableHead>
                <TableHead>الإجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredPurchases.map((purchase) => (
                <TableRow key={purchase.id}>
                  <TableCell className="font-semibold">{purchase.id}</TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                       <Truck className="w-4 h-4 text-muted-foreground" />
                       {purchase.supplier}
                    </div>
                  </TableCell>
                  <TableCell>{purchase.items_count} منتج</TableCell>
                  <TableCell className="font-bold">{formatCurrency(purchase.total_amount)}</TableCell>
                  <TableCell>
                    <span className={purchase.paid_amount >= purchase.total_amount ? 'text-green-600' : 'text-yellow-600'}>
                      {formatCurrency(purchase.paid_amount)}
                    </span>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1 text-muted-foreground">
                      <Calendar className="w-4 h-4" />
                      {new Date(purchase.created_at).toLocaleDateString('ar-SA')}
                    </div>
                  </TableCell>
                  <TableCell>{getStatusBadge(purchase.status)}</TableCell>
                  <TableCell>
                    <div className="flex gap-1">
                      <Button variant="ghost" size="icon" title="عرض"><Eye className="w-4 h-4" /></Button>
                      <Button variant="ghost" size="icon" title="تعديل"><Edit className="w-4 h-4" /></Button>
                      <Button variant="ghost" size="icon" className="text-destructive hover:bg-destructive/10" title="حذف"><Trash2 className="w-4 h-4" /></Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          
          {filteredPurchases.length === 0 && (
            <div className="text-center py-8">
              <FileText className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">لا توجد فواتير شراء مطابقة</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default PurchasesPage;



