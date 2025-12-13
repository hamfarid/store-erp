import React, { useState, useEffect } from 'react';
import {
  Clock, RotateCcw, CheckCircle, XCircle, ShoppingCart, Package,
  Search, Filter, Download, Eye, Plus, Edit, Trash2
} from 'lucide-react';
import { toast } from 'react-hot-toast';

const ReturnsManagement = () => {
  const [returns, setReturns] = useState([]);
  const [filteredReturns, setFilteredReturns] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedReturn, setSelectedReturn] = useState(null);

  // Sample data
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
    // Simulate API call
    setTimeout(() => {
      setReturns(sampleReturns);
      setFilteredReturns(sampleReturns);
      setIsLoading(false);
    }, 1000);
  }, []);

  useEffect(() => {
    let filtered = returns;

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(returnItem =>
        returnItem.returnNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
        returnItem.originalInvoiceNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (returnItem.customerName && returnItem.customerName.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (returnItem.supplierName && returnItem.supplierName.toLowerCase().includes(searchTerm.toLowerCase())) ||
        returnItem.reason.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Filter by type
    if (filterType !== 'all') {
      filtered = filtered.filter(returnItem => returnItem.type === filterType);
    }

    // Filter by status
    if (filterStatus !== 'all') {
      filtered = filtered.filter(returnItem => returnItem.status === filterStatus);
    }

    setFilteredReturns(filtered);
  }, [returns, searchTerm, filterType, filterStatus]);

  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { label: 'في الانتظار', variant: 'secondary', icon: Clock, color: 'text-accent' },
      processing: { label: 'قيد المعالجة', variant: 'default', icon: RotateCcw, color: 'text-primary' },
      approved: { label: 'معتمد', variant: 'default', icon: CheckCircle, color: 'text-primary' },
      rejected: { label: 'مرفوض', variant: 'destructive', icon: XCircle, color: 'text-destructive' }
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

  const getTypeLabel = (type) => {
    const types = {
      sales: 'مرتجع مبيعات',
      purchase: 'مرتجع مشتريات'
    };
    return types[type] || type;
  };

  const getTypeBadge = (type) => {
    const typeConfig = {
      sales: { label: 'مرتجع مبيعات', variant: 'default', icon: ShoppingCart, color: 'text-primary' },
      purchase: { label: 'مرتجع مشتريات', variant: 'secondary', icon: Package, color: 'text-primary' }
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
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل إدارة المرتجعات...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">إدارة المرتجعات</h1>
          <p className="text-muted-foreground mt-1">إدارة مرتجعات المبيعات والمشتريات</p>
        </div>
        <div className="flex gap-2">
          <Button onClick={handleExport} variant="outline">
            <Download className="w-4 h-4 mr-2" />
            تصدير
          </Button>
          <Button onClick={handleAddReturn}>
            <Plus className="w-4 h-4 mr-2" />
            إضافة مرتجع جديد
          </Button>
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
              <RotateCcw className="w-8 h-8 text-primary/100" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">في الانتظار</p>
                <p className="text-2xl font-bold text-accent">{statusCounts.pending}</p>
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
                <p className="text-2xl font-bold text-primary">{statusCounts.processing}</p>
              </div>
              <RotateCcw className="w-8 h-8 text-primary/100" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">معتمدة</p>
                <p className="text-2xl font-bold text-primary">{statusCounts.approved}</p>
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
                <p className="text-2xl font-bold text-destructive">{statusCounts.rejected}</p>
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
                <p className="text-2xl font-bold text-primary">{getTotalRefundAmount().toLocaleString()}</p>
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
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  id="search"
                  placeholder="البحث برقم المرتجع، رقم الفاتورة، العميل/المورد، أو السبب..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
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
          <div className="overflow-x-auto">
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
                      <div className="text-sm text-gray-500">
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
                        <div className="text-sm text-gray-500">
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
                      <div className={`font-medium ${returnItem.refundAmount > 0 ? 'text-primary' : 'text-gray-500'}`}>
                        {returnItem.refundAmount.toLocaleString()} ر.س
                      </div>
                    </TableCell>
                    <TableCell>
                      {getStatusBadge(returnItem.status)}
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-1">
                        <Calendar className="w-3 h-3 text-gray-500" />
                        <span className="text-sm">
                          {new Date(returnItem.createdAt).toLocaleDateString('ar-SA')}
                        </span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-1">
                        {returnItem.status === 'pending' && (
                          <>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleProcessReturn(returnItem.id)}
                              className="text-primary hover:text-primary/90"
                            >
                              معالجة
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleApproveReturn(returnItem.id)}
                              className="text-primary hover:text-primary"
                            >
                              اعتماد
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleRejectReturn(returnItem.id)}
                              className="text-destructive hover:text-destructive"
                            >
                              رفض
                            </Button>
                          </>
                        )}
                        {returnItem.status === 'processing' && (
                          <>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleApproveReturn(returnItem.id)}
                              className="text-primary hover:text-primary"
                            >
                              اعتماد
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleRejectReturn(returnItem.id)}
                              className="text-destructive hover:text-destructive"
                            >
                              رفض
                            </Button>
                          </>
                        )}
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleEditReturn(returnItem)}
                        >
                          <Edit className="w-4 h-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setSelectedReturn(returnItem)}
                        >
                          <Eye className="w-4 h-4" />
                        </Button>
                        {returnItem.status === 'pending' && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleDeleteReturn(returnItem.id)}
                            className="text-destructive hover:text-destructive"
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        )}
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>

          {filteredReturns.length === 0 && (
            <div className="text-center py-8">
              <RotateCcw className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">لا توجد مرتجعات تطابق معايير البحث</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default ReturnsManagement;

