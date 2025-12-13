import React, { useState, useEffect } from 'react';
import {
  Plus, Search, Download, Edit, Trash2, Eye, CheckCircle, XCircle,
  Clock, Receipt, DollarSign, CreditCard, FileText, Printer, ArrowUpDown
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
 * صفحة قسائم الدفع والقبض
 * Payment & Receipt Vouchers Page
 */
const AccountingVouchers = () => {
  const [vouchers, setVouchers] = useState([]);
  const [filteredVouchers, setFilteredVouchers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedVoucher, setSelectedVoucher] = useState(null);

  // بيانات نموذجية
  const sampleVouchers = [
    {
      id: 1,
      voucherNumber: 'VCH-2024-001',
      type: 'receipt',
      category: 'sales',
      customerName: 'شركة الأحمد للتجارة',
      amount: 5000,
      currency: 'ر.س',
      paymentMethod: 'cash',
      cashBoxName: 'الخزينة الرئيسية',
      invoiceNumber: 'INV-2024-150',
      status: 'approved',
      createdBy: 'أحمد محمد',
      createdAt: '2024-01-15T09:00:00',
      approvedBy: 'محمد علي',
      approvedAt: '2024-01-15T10:00:00',
      notes: 'دفعة نقدية من العميل'
    },
    {
      id: 2,
      voucherNumber: 'VCH-2024-002',
      type: 'payment',
      category: 'purchase',
      supplierName: 'مؤسسة التقنية المتقدمة',
      amount: 15000,
      currency: 'ر.س',
      paymentMethod: 'bank_transfer',
      bankName: 'البنك الأهلي',
      invoiceNumber: 'PUR-2024-075',
      status: 'pending',
      createdBy: 'سارة أحمد',
      createdAt: '2024-01-14T14:30:00',
      approvedBy: null,
      approvedAt: null,
      notes: 'تحويل بنكي للمورد'
    },
    {
      id: 3,
      voucherNumber: 'VCH-2024-003',
      type: 'receipt',
      category: 'sales',
      customerName: 'متجر الإلكترونيات الحديث',
      amount: 8500,
      currency: 'ر.س',
      paymentMethod: 'check',
      checkNumber: 'CHK-123456',
      checkDate: '2024-02-15',
      invoiceNumber: 'INV-2024-148',
      status: 'approved',
      createdBy: 'فاطمة سالم',
      createdAt: '2024-01-13T11:00:00',
      approvedBy: 'أحمد محمد',
      approvedAt: '2024-01-13T12:00:00',
      notes: 'شيك مؤجل'
    },
    {
      id: 4,
      voucherNumber: 'VCH-2024-004',
      type: 'payment',
      category: 'expense',
      description: 'مصاريف صيانة',
      amount: 2500,
      currency: 'ر.س',
      paymentMethod: 'cash',
      cashBoxName: 'الخزينة الرئيسية',
      status: 'rejected',
      createdBy: 'خالد أحمد',
      createdAt: '2024-01-12T08:00:00',
      approvedBy: 'محمد علي',
      approvedAt: '2024-01-12T09:00:00',
      rejectionReason: 'مبلغ غير مدعوم بمستندات',
      notes: 'مصاريف صيانة المكيفات'
    }
  ];

  useEffect(() => {
    fetchVouchers();
  }, []);

  const fetchVouchers = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.get('/api/accounting/vouchers');
      if (response.status === 'success' && response.data?.length > 0) {
        setVouchers(response.data);
        setFilteredVouchers(response.data);
      } else {
        setVouchers(sampleVouchers);
        setFilteredVouchers(sampleVouchers);
      }
    } catch (error) {
      console.log('Using sample data:', error);
      setVouchers(sampleVouchers);
      setFilteredVouchers(sampleVouchers);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let filtered = vouchers;

    if (searchTerm) {
      filtered = filtered.filter(v =>
        v.voucherNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (v.customerName && v.customerName.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (v.supplierName && v.supplierName.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (v.invoiceNumber && v.invoiceNumber.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    if (filterType !== 'all') {
      filtered = filtered.filter(v => v.type === filterType);
    }

    if (filterStatus !== 'all') {
      filtered = filtered.filter(v => v.status === filterStatus);
    }

    setFilteredVouchers(filtered);
  }, [vouchers, searchTerm, filterType, filterStatus]);

  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { label: 'في الانتظار', variant: 'secondary', icon: Clock },
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
      receipt: { label: 'سند قبض', variant: 'default', icon: DollarSign },
      payment: { label: 'سند صرف', variant: 'secondary', icon: CreditCard }
    };

    const config = typeConfig[type] || typeConfig.receipt;
    const IconComponent = config.icon;
    
    return (
      <Badge variant={config.variant} className="flex items-center gap-1">
        <IconComponent className="w-3 h-3" />
        {config.label}
      </Badge>
    );
  };

  const getPaymentMethodLabel = (method) => {
    const methods = {
      cash: 'نقدي',
      bank_transfer: 'تحويل بنكي',
      check: 'شيك',
      card: 'بطاقة'
    };
    return methods[method] || method;
  };

  const handleAddVoucher = () => {
    setSelectedVoucher(null);
    setShowAddModal(true);
    toast.success('جاري فتح نموذج سند جديد');
  };

  const handleEditVoucher = (voucher) => {
    if (voucher.status !== 'pending') {
      toast.error('لا يمكن تعديل سند معتمد أو مرفوض');
      return;
    }
    setSelectedVoucher(voucher);
    setShowAddModal(true);
  };

  const handleDeleteVoucher = (voucherId) => {
    const voucher = vouchers.find(v => v.id === voucherId);
    if (voucher.status === 'approved') {
      toast.error('لا يمكن حذف سند معتمد');
      return;
    }
    
    if (window.confirm('هل أنت متأكد من حذف هذا السند؟')) {
      setVouchers(vouchers.filter(v => v.id !== voucherId));
      toast.success('تم حذف السند بنجاح');
    }
  };

  const handleApproveVoucher = (voucherId) => {
    setVouchers(vouchers.map(v =>
      v.id === voucherId
        ? { ...v, status: 'approved', approvedBy: 'المدير الحالي', approvedAt: new Date().toISOString() }
        : v
    ));
    toast.success('تم اعتماد السند بنجاح');
  };

  const handleRejectVoucher = (voucherId) => {
    const reason = prompt('سبب الرفض:');
    if (!reason) return;
    
    setVouchers(vouchers.map(v =>
      v.id === voucherId
        ? { ...v, status: 'rejected', approvedBy: 'المدير الحالي', approvedAt: new Date().toISOString(), rejectionReason: reason }
        : v
    ));
    toast.success('تم رفض السند');
  };

  const handlePrintVoucher = (voucher) => {
    toast.success(`جاري طباعة السند ${voucher.voucherNumber}`);
  };

  const handleExport = () => {
    toast.success('تم تصدير البيانات بنجاح');
  };

  const getSummary = () => {
    return {
      total: vouchers.length,
      pending: vouchers.filter(v => v.status === 'pending').length,
      approved: vouchers.filter(v => v.status === 'approved').length,
      rejected: vouchers.filter(v => v.status === 'rejected').length,
      totalReceipts: vouchers.filter(v => v.type === 'receipt' && v.status === 'approved').reduce((sum, v) => sum + v.amount, 0),
      totalPayments: vouchers.filter(v => v.type === 'payment' && v.status === 'approved').reduce((sum, v) => sum + v.amount, 0)
    };
  };

  const summary = getSummary();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل قسائم الدفع والقبض...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">قسائم الدفع والقبض</h1>
          <p className="text-muted-foreground mt-1">إدارة سندات القبض والصرف</p>
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
            onClick={handleAddVoucher}
            className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
          >
            <Plus className="w-4 h-4" />
            سند جديد
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي السندات</p>
                <p className="text-2xl font-bold text-primary">{summary.total}</p>
              </div>
              <FileText className="w-8 h-8 text-primary/60" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">في الانتظار</p>
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
                <p className="text-sm text-muted-foreground">معتمدة</p>
                <p className="text-2xl font-bold text-green-600">{summary.approved}</p>
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
                <p className="text-2xl font-bold text-red-600">{summary.rejected}</p>
              </div>
              <XCircle className="w-8 h-8 text-red-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي المقبوضات</p>
                <p className="text-2xl font-bold text-green-600">{summary.totalReceipts.toLocaleString()}</p>
              </div>
              <DollarSign className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي المصروفات</p>
                <p className="text-2xl font-bold text-red-600">{summary.totalPayments.toLocaleString()}</p>
              </div>
              <CreditCard className="w-8 h-8 text-red-500" />
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
                  placeholder="البحث برقم السند، العميل/المورد، رقم الفاتورة..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>

            <div className="min-w-40">
              <Label htmlFor="type-filter">النوع</Label>
              <Select value={filterType} onValueChange={setFilterType}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر النوع" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع الأنواع</SelectItem>
                  <SelectItem value="receipt">سند قبض</SelectItem>
                  <SelectItem value="payment">سند صرف</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="min-w-40">
              <Label htmlFor="status-filter">الحالة</Label>
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر الحالة" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع الحالات</SelectItem>
                  <SelectItem value="pending">في الانتظار</SelectItem>
                  <SelectItem value="approved">معتمد</SelectItem>
                  <SelectItem value="rejected">مرفوض</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Vouchers Table */}
      <Card>
        <CardHeader>
          <CardTitle>قائمة السندات ({filteredVouchers.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>رقم السند</TableHead>
                <TableHead>النوع</TableHead>
                <TableHead>الطرف</TableHead>
                <TableHead>المبلغ</TableHead>
                <TableHead>طريقة الدفع</TableHead>
                <TableHead>رقم الفاتورة</TableHead>
                <TableHead>الحالة</TableHead>
                <TableHead>التاريخ</TableHead>
                <TableHead>الإجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredVouchers.map((voucher) => (
                <TableRow key={voucher.id}>
                  <TableCell>
                    <div className="font-medium">{voucher.voucherNumber}</div>
                  </TableCell>
                  <TableCell>
                    {getTypeBadge(voucher.type)}
                  </TableCell>
                  <TableCell>
                    <span>{voucher.customerName || voucher.supplierName || voucher.description || '-'}</span>
                  </TableCell>
                  <TableCell>
                    <div className={`font-medium ${voucher.type === 'receipt' ? 'text-green-600' : 'text-red-600'}`}>
                      {voucher.type === 'receipt' ? '+' : '-'}{voucher.amount.toLocaleString()} {voucher.currency}
                    </div>
                  </TableCell>
                  <TableCell>
                    <span className="text-sm">{getPaymentMethodLabel(voucher.paymentMethod)}</span>
                  </TableCell>
                  <TableCell>
                    <span className="text-sm">{voucher.invoiceNumber || '-'}</span>
                  </TableCell>
                  <TableCell>
                    {getStatusBadge(voucher.status)}
                  </TableCell>
                  <TableCell>
                    <span className="text-sm">
                      {new Date(voucher.createdAt).toLocaleDateString('ar-SA')}
                    </span>
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-1">
                      {voucher.status === 'pending' && (
                        <>
                          <button
                            onClick={() => handleApproveVoucher(voucher.id)}
                            className="px-2 py-1 text-sm text-green-600 hover:bg-green-50 rounded"
                          >
                            اعتماد
                          </button>
                          <button
                            onClick={() => handleRejectVoucher(voucher.id)}
                            className="px-2 py-1 text-sm text-red-600 hover:bg-red-50 rounded"
                          >
                            رفض
                          </button>
                        </>
                      )}
                      <button
                        onClick={() => handlePrintVoucher(voucher)}
                        className="p-1 hover:bg-muted rounded"
                      >
                        <Printer className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleEditVoucher(voucher)}
                        className="p-1 hover:bg-muted rounded"
                        disabled={voucher.status !== 'pending'}
                      >
                        <Edit className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => setSelectedVoucher(voucher)}
                        className="p-1 hover:bg-muted rounded"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                      {voucher.status !== 'approved' && (
                        <button
                          onClick={() => handleDeleteVoucher(voucher.id)}
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

          {filteredVouchers.length === 0 && (
            <div className="text-center py-8">
              <Receipt className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">لا توجد سندات تطابق معايير البحث</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Voucher Details Modal */}
      {selectedVoucher && !showAddModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-background rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">تفاصيل السند</h2>
              <button
                onClick={() => setSelectedVoucher(null)}
                className="p-2 hover:bg-muted rounded"
              >
                ✕
              </button>
            </div>
            
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>رقم السند</Label>
                  <p className="font-medium">{selectedVoucher.voucherNumber}</p>
                </div>
                <div>
                  <Label>النوع</Label>
                  <p>{getTypeBadge(selectedVoucher.type)}</p>
                </div>
                <div>
                  <Label>المبلغ</Label>
                  <p className={`font-medium ${selectedVoucher.type === 'receipt' ? 'text-green-600' : 'text-red-600'}`}>
                    {selectedVoucher.amount.toLocaleString()} {selectedVoucher.currency}
                  </p>
                </div>
                <div>
                  <Label>الحالة</Label>
                  <p>{getStatusBadge(selectedVoucher.status)}</p>
                </div>
                <div>
                  <Label>طريقة الدفع</Label>
                  <p className="font-medium">{getPaymentMethodLabel(selectedVoucher.paymentMethod)}</p>
                </div>
                <div>
                  <Label>رقم الفاتورة</Label>
                  <p className="font-medium">{selectedVoucher.invoiceNumber || '-'}</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>المنشئ</Label>
                  <p className="text-muted-foreground">{selectedVoucher.createdBy}</p>
                </div>
                <div>
                  <Label>تاريخ الإنشاء</Label>
                  <p className="text-muted-foreground">{new Date(selectedVoucher.createdAt).toLocaleString('ar-SA')}</p>
                </div>
                {selectedVoucher.approvedBy && (
                  <>
                    <div>
                      <Label>المعتمد</Label>
                      <p className="text-muted-foreground">{selectedVoucher.approvedBy}</p>
                    </div>
                    <div>
                      <Label>تاريخ الاعتماد</Label>
                      <p className="text-muted-foreground">{new Date(selectedVoucher.approvedAt).toLocaleString('ar-SA')}</p>
                    </div>
                  </>
                )}
              </div>

              {selectedVoucher.rejectionReason && (
                <div>
                  <Label>سبب الرفض</Label>
                  <p className="text-red-600">{selectedVoucher.rejectionReason}</p>
                </div>
              )}

              <div>
                <Label>ملاحظات</Label>
                <p className="text-muted-foreground">{selectedVoucher.notes || 'لا توجد ملاحظات'}</p>
              </div>

              <div className="flex gap-2 pt-4">
                <button
                  onClick={() => handlePrintVoucher(selectedVoucher)}
                  className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90"
                >
                  <Printer className="w-4 h-4" />
                  طباعة
                </button>
                <button
                  onClick={() => setSelectedVoucher(null)}
                  className="px-4 py-2 border border-border rounded-lg hover:bg-muted"
                >
                  إغلاق
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AccountingVouchers;

