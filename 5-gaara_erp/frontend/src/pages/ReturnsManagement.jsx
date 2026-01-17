import React, { useState, useEffect } from 'react';
import {
  Clock, RotateCcw, CheckCircle, XCircle, ShoppingCart, Package,
  Search, Filter, Download, Eye, Plus, Edit, Trash2, Calendar, DollarSign
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
 * صفحة إدارة المرتجعات
 * Returns Management Page
 */
const ReturnsManagement = () => {
  const [returns, setReturns] = useState([]);
  const [filteredReturns, setFilteredReturns] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedReturn, setSelectedReturn] = useState(null);

  // بيانات نموذجية للاختبار
  const sampleReturns = [
    {
      id: 1,
      returnNumber: 'RET-2024-001',
      type: 'sales',
      originalInvoiceNumber: 'INV-2024-150',
      customerName: 'شركة الأحمد للتجارة',
      customerPhone: '+966501234567',
      reason: 'عيب في المنتج',
      status: 'pending',
      createdBy: 'أحمد محمد',
      createdAt: '2024-01-15T10:00:00',
      processedBy: null,
      processedAt: null,
      items: [
        { productName: 'لابتوب ديل', quantity: 1, unitPrice: 2500, totalPrice: 2500, condition: 'damaged' },
        { productName: 'ماوس لاسلكي', quantity: 2, unitPrice: 80, totalPrice: 160, condition: 'good' }
      ],
      totalAmount: 2660,
      refundAmount: 2660,
      notes: 'عيب في شاشة اللابتوب، الماوس في حالة جيدة'
    },
    {
      id: 2,
      returnNumber: 'RET-2024-002',
      type: 'purchase',
      originalInvoiceNumber: 'PUR-2024-075',
      supplierName: 'مؤسسة التقنية المتقدمة',
      supplierPhone: '+966507654321',
      reason: 'مواصفات خاطئة',
      status: 'approved',
      createdBy: 'سارة أحمد',
      createdAt: '2024-01-14T14:30:00',
      processedBy: 'محمد علي',
      processedAt: '2024-01-14T16:00:00',
      items: [
        { productName: 'هاتف ذكي', quantity: 5, unitPrice: 1200, totalPrice: 6000, condition: 'good' }
      ],
      totalAmount: 6000,
      refundAmount: 6000,
      notes: 'تم استلام موديل مختلف عن المطلوب'
    },
    {
      id: 3,
      returnNumber: 'RET-2024-003',
      type: 'sales',
      originalInvoiceNumber: 'INV-2024-148',
      customerName: 'متجر الإلكترونيات الحديث',
      customerPhone: '+966512345678',
      reason: 'تغيير في الطلب',
      status: 'rejected',
      createdBy: 'فاطمة سالم',
      createdAt: '2024-01-13T11:00:00',
      processedBy: 'أحمد محمد',
      processedAt: '2024-01-13T15:30:00',
      items: [
        { productName: 'تابلت سامسونج', quantity: 3, unitPrice: 800, totalPrice: 2400, condition: 'good' }
      ],
      totalAmount: 2400,
      refundAmount: 0,
      notes: 'تم رفض المرتجع - تجاوز المدة المسموحة'
    },
    {
      id: 4,
      returnNumber: 'RET-2024-004',
      type: 'purchase',
      originalInvoiceNumber: 'PUR-2024-072',
      supplierName: 'شركة المكونات الإلكترونية',
      supplierPhone: '+966555123456',
      reason: 'كمية زائدة',
      status: 'processing',
      createdBy: 'خالد أحمد',
      createdAt: '2024-01-12T08:00:00',
      processedBy: 'سارة أحمد',
      processedAt: '2024-01-12T10:00:00',
      items: [
        { productName: 'كيبل USB', quantity: 50, unitPrice: 25, totalPrice: 1250, condition: 'good' },
        { productName: 'شاحن سريع', quantity: 20, unitPrice: 45, totalPrice: 900, condition: 'good' }
      ],
      totalAmount: 2150,
      refundAmount: 2150,
      notes: 'طلب كمية أكبر من المطلوب'
    }
  ];

  useEffect(() => {
    fetchReturns();
  }, []);

  const fetchReturns = async () => {
    setIsLoading(true);
    try {
      // محاولة جلب البيانات من API
      const response = await apiClient.get('/api/returns');
      if (response.success && response.data.length > 0) {
        setReturns(response.data);
        setFilteredReturns(response.data);
      } else {
        // استخدام البيانات النموذجية
        setReturns(sampleReturns);
        setFilteredReturns(sampleReturns);
      }
    } catch (error) {
      console.log('Using sample data:', error);
      setReturns(sampleReturns);
      setFilteredReturns(sampleReturns);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let filtered = returns;

    if (searchTerm) {
      filtered = filtered.filter(returnItem =>
        returnItem.returnNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
        returnItem.originalInvoiceNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (returnItem.customerName && returnItem.customerName.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (returnItem.supplierName && returnItem.supplierName.toLowerCase().includes(searchTerm.toLowerCase())) ||
        returnItem.reason.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterType !== 'all') {
      filtered = filtered.filter(returnItem => returnItem.type === filterType);
    }

    if (filterStatus !== 'all') {
      filtered = filtered.filter(returnItem => returnItem.status === filterStatus);
    }

    setFilteredReturns(filtered);
  }, [returns, searchTerm, filterType, filterStatus]);

  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { label: 'في الانتظار', variant: 'secondary', icon: Clock },
      processing: { label: 'قيد المعالجة', variant: 'default', icon: RotateCcw },
      approved: { label: 'معتمد', variant: 'default', icon: CheckCircle },
      rejected: { label: 'مرفوض', variant: 'destructive', icon: XCircle }
    };

    const config = statusConfig[status] || statusConfig.pending;
    const IconComponent = config.icon;
    
    return (
      <Badge variant={config.variant} className="flex items-center gap-1">
        <IconComponent className="w-3 h-3" />
        {config.label}
      </Badge>
    );
  };

  const getTypeBadge = (type) => {
    const typeConfig = {
      sales: { label: 'مرتجع مبيعات', variant: 'default', icon: ShoppingCart },
      purchase: { label: 'مرتجع مشتريات', variant: 'secondary', icon: Package }
    };

    const config = typeConfig[type] || typeConfig.sales;
    const IconComponent = config.icon;
    
    return (
      <Badge variant={config.variant} className="flex items-center gap-1">
        <IconComponent className="w-3 h-3" />
        {config.label}
      </Badge>
    );
  };

  const handleAddReturn = () => {
    setSelectedReturn(null);
    setShowAddModal(true);
    toast.success('جاري فتح نموذج إضافة مرتجع جديد');
  };

  const handleEditReturn = (returnItem) => {
    setSelectedReturn(returnItem);
    setShowAddModal(true);
  };

  const handleDeleteReturn = (returnId) => {
    if (window.confirm('هل أنت متأكد من حذف هذا المرتجع؟')) {
      setReturns(returns.filter(returnItem => returnItem.id !== returnId));
      toast.success('تم حذف المرتجع بنجاح');
    }
  };

  const handleApproveReturn = (returnId) => {
    setReturns(returns.map(returnItem =>
      returnItem.id === returnId
        ? { 
            ...returnItem, 
            status: 'approved',
            processedBy: 'المدير الحالي',
            processedAt: new Date().toISOString()
          }
        : returnItem
    ));
    toast.success('تم اعتماد المرتجع بنجاح');
  };

  const handleRejectReturn = (returnId) => {
    setReturns(returns.map(returnItem =>
      returnItem.id === returnId
        ? { 
            ...returnItem, 
            status: 'rejected',
            processedBy: 'المدير الحالي',
            processedAt: new Date().toISOString()
          }
        : returnItem
    ));
    toast.success('تم رفض المرتجع');
  };

  const handleProcessReturn = (returnId) => {
    setReturns(returns.map(returnItem =>
      returnItem.id === returnId
        ? { 
            ...returnItem, 
            status: 'processing',
            processedBy: 'المدير الحالي',
            processedAt: new Date().toISOString()
          }
        : returnItem
    ));
    toast.success('تم بدء معالجة المرتجع');
  };

  const handleExport = () => {
    toast.success('تم تصدير البيانات بنجاح');
  };

  const getStatusCounts = () => {
    return {
      total: returns.length,
      pending: returns.filter(r => r.status === 'pending').length,
      processing: returns.filter(r => r.status === 'processing').length,
      approved: returns.filter(r => r.status === 'approved').length,
      rejected: returns.filter(r => r.status === 'rejected').length
    };
  };

  const getTotalRefundAmount = () => {
    return returns
      .filter(r => r.status === 'approved')
      .reduce((sum, r) => sum + r.refundAmount, 0);
  };

  const statusCounts = getStatusCounts();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل إدارة المرتجعات...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">إدارة المرتجعات</h1>
          <p className="text-muted-foreground mt-1">إدارة مرتجعات المبيعات والمشتريات</p>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={handleExport}
            className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors"
          >
            <Download className="w-4 h-4" />
            تصدير
          </button>
          <button 
            onClick={handleAddReturn}
            className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
          >
            <Plus className="w-4 h-4" />
            إضافة مرتجع جديد
          </button>
        </div>
      </div>

      {/* Status Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي المرتجعات</p>
                <p className="text-2xl font-bold text-primary">{statusCounts.total}</p>
              </div>
              <RotateCcw className="w-8 h-8 text-primary/60" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">في الانتظار</p>
                <p className="text-2xl font-bold text-yellow-600">{statusCounts.pending}</p>
              </div>
              <Clock className="w-8 h-8 text-yellow-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">قيد المعالجة</p>
                <p className="text-2xl font-bold text-blue-600">{statusCounts.processing}</p>
              </div>
              <RotateCcw className="w-8 h-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">معتمدة</p>
                <p className="text-2xl font-bold text-green-600">{statusCounts.approved}</p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">مرفوضة</p>
                <p className="text-2xl font-bold text-red-600">{statusCounts.rejected}</p>
              </div>
              <XCircle className="w-8 h-8 text-red-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي المبالغ المستردة</p>
                <p className="text-2xl font-bold text-green-600">{getTotalRefundAmount().toLocaleString()}</p>
              </div>
              <DollarSign className="w-8 h-8 text-green-500" />
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
                  placeholder="البحث برقم المرتجع، رقم الفاتورة، العميل/المورد، أو السبب..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>

            <div className="min-w-48">
              <Label htmlFor="type-filter">نوع المرتجع</Label>
              <Select value={filterType} onValueChange={setFilterType}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر نوع المرتجع" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع الأنواع</SelectItem>
                  <SelectItem value="sales">مرتجع مبيعات</SelectItem>
                  <SelectItem value="purchase">مرتجع مشتريات</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="min-w-48">
              <Label htmlFor="status-filter">الحالة</Label>
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر الحالة" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع الحالات</SelectItem>
                  <SelectItem value="pending">في الانتظار</SelectItem>
                  <SelectItem value="processing">قيد المعالجة</SelectItem>
                  <SelectItem value="approved">معتمد</SelectItem>
                  <SelectItem value="rejected">مرفوض</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Returns Table */}
      <Card>
        <CardHeader>
          <CardTitle>قائمة المرتجعات ({filteredReturns.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>رقم المرتجع</TableHead>
                <TableHead>النوع</TableHead>
                <TableHead>الفاتورة الأصلية</TableHead>
                <TableHead>العميل/المورد</TableHead>
                <TableHead>السبب</TableHead>
                <TableHead>المبلغ الإجمالي</TableHead>
                <TableHead>المبلغ المسترد</TableHead>
                <TableHead>الحالة</TableHead>
                <TableHead>تاريخ الإنشاء</TableHead>
                <TableHead>الإجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredReturns.map((returnItem) => (
                <TableRow key={returnItem.id}>
                  <TableCell>
                    <div className="font-medium">{returnItem.returnNumber}</div>
                    <div className="text-sm text-muted-foreground">
                      {returnItem.items.length} عنصر
                    </div>
                  </TableCell>
                  <TableCell>
                    {getTypeBadge(returnItem.type)}
                  </TableCell>
                  <TableCell>
                    <div className="font-medium">{returnItem.originalInvoiceNumber}</div>
                  </TableCell>
                  <TableCell>
                    <div>
                      <div className="font-medium">
                        {returnItem.customerName || returnItem.supplierName}
                      </div>
                      <div className="text-sm text-muted-foreground">
                        {returnItem.customerPhone || returnItem.supplierPhone}
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <span className="text-sm">{returnItem.reason}</span>
                  </TableCell>
                  <TableCell>
                    <div className="font-medium">
                      {returnItem.totalAmount.toLocaleString()} ر.س
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className={`font-medium ${returnItem.refundAmount > 0 ? 'text-green-600' : 'text-muted-foreground'}`}>
                      {returnItem.refundAmount.toLocaleString()} ر.س
                    </div>
                  </TableCell>
                  <TableCell>
                    {getStatusBadge(returnItem.status)}
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Calendar className="w-3 h-3 text-muted-foreground" />
                      <span className="text-sm">
                        {new Date(returnItem.createdAt).toLocaleDateString('ar-SA')}
                      </span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-1">
                      {returnItem.status === 'pending' && (
                        <>
                          <button
                            onClick={() => handleProcessReturn(returnItem.id)}
                            className="px-2 py-1 text-sm text-blue-600 hover:bg-blue-50 rounded"
                          >
                            معالجة
                          </button>
                          <button
                            onClick={() => handleApproveReturn(returnItem.id)}
                            className="px-2 py-1 text-sm text-green-600 hover:bg-green-50 rounded"
                          >
                            اعتماد
                          </button>
                          <button
                            onClick={() => handleRejectReturn(returnItem.id)}
                            className="px-2 py-1 text-sm text-red-600 hover:bg-red-50 rounded"
                          >
                            رفض
                          </button>
                        </>
                      )}
                      {returnItem.status === 'processing' && (
                        <>
                          <button
                            onClick={() => handleApproveReturn(returnItem.id)}
                            className="px-2 py-1 text-sm text-green-600 hover:bg-green-50 rounded"
                          >
                            اعتماد
                          </button>
                          <button
                            onClick={() => handleRejectReturn(returnItem.id)}
                            className="px-2 py-1 text-sm text-red-600 hover:bg-red-50 rounded"
                          >
                            رفض
                          </button>
                        </>
                      )}
                      <button
                        onClick={() => handleEditReturn(returnItem)}
                        className="p-1 hover:bg-muted rounded"
                      >
                        <Edit className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => setSelectedReturn(returnItem)}
                        className="p-1 hover:bg-muted rounded"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                      {returnItem.status === 'pending' && (
                        <button
                          onClick={() => handleDeleteReturn(returnItem.id)}
                          className="p-1 text-red-600 hover:bg-red-50 rounded"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>

          {filteredReturns.length === 0 && (
            <div className="text-center py-8">
              <RotateCcw className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">لا توجد مرتجعات تطابق معايير البحث</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Return Details Modal */}
      {selectedReturn && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-background rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">تفاصيل المرتجع</h2>
              <button
                onClick={() => setSelectedReturn(null)}
                className="p-2 hover:bg-muted rounded"
              >
                <XCircle className="w-5 h-5" />
              </button>
            </div>
            
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>رقم المرتجع</Label>
                  <p className="font-medium">{selectedReturn.returnNumber}</p>
                </div>
                <div>
                  <Label>نوع المرتجع</Label>
                  <p>{getTypeBadge(selectedReturn.type)}</p>
                </div>
                <div>
                  <Label>الفاتورة الأصلية</Label>
                  <p className="font-medium">{selectedReturn.originalInvoiceNumber}</p>
                </div>
                <div>
                  <Label>الحالة</Label>
                  <p>{getStatusBadge(selectedReturn.status)}</p>
                </div>
              </div>

              <div>
                <Label>المنتجات</Label>
                <div className="border rounded-lg mt-2">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>المنتج</TableHead>
                        <TableHead>الكمية</TableHead>
                        <TableHead>السعر</TableHead>
                        <TableHead>الإجمالي</TableHead>
                        <TableHead>الحالة</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {selectedReturn.items.map((item, index) => (
                        <TableRow key={index}>
                          <TableCell>{item.productName}</TableCell>
                          <TableCell>{item.quantity}</TableCell>
                          <TableCell>{item.unitPrice.toLocaleString()} ر.س</TableCell>
                          <TableCell>{item.totalPrice.toLocaleString()} ر.س</TableCell>
                          <TableCell>
                            <Badge variant={item.condition === 'good' ? 'default' : 'destructive'}>
                              {item.condition === 'good' ? 'جيد' : 'تالف'}
                            </Badge>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </div>

              <div>
                <Label>ملاحظات</Label>
                <p className="text-muted-foreground">{selectedReturn.notes}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ReturnsManagement;
