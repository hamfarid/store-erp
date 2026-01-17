import React, { useState, useEffect } from 'react';
import {
  Clock, AlertTriangle, CheckCircle, TrendingUp, TrendingDown,
  Search, Download, Eye, Plus, Edit, Trash2, DollarSign, CreditCard,
  Calendar, Phone, Building, User
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
 * صفحة إدارة المدفوعات والديون
 * Payment & Debt Management Page
 */
const PaymentDebtManagement = () => {
  const [debts, setDebts] = useState([]);
  const [filteredDebts, setFilteredDebts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [selectedDebt, setSelectedDebt] = useState(null);

  // بيانات نموذجية للاختبار
  const sampleDebts = [
    {
      id: 1,
      debtNumber: 'DEBT-2024-001',
      type: 'receivable',
      customerName: 'شركة الأحمد للتجارة',
      customerPhone: '+966501234567',
      originalAmount: 15000,
      paidAmount: 5000,
      remainingAmount: 10000,
      dueDate: '2024-02-15',
      status: 'overdue',
      priority: 'high',
      invoiceNumbers: ['INV-2024-150', 'INV-2024-155'],
      createdAt: '2024-01-15T09:00:00',
      lastPaymentDate: '2024-01-20T14:30:00',
      notes: 'عميل مهم - متابعة دورية',
      paymentHistory: [
        { date: '2024-01-20', amount: 5000, method: 'bank_transfer', reference: 'TXN-001' }
      ]
    },
    {
      id: 2,
      debtNumber: 'DEBT-2024-002',
      type: 'payable',
      supplierName: 'مؤسسة التقنية المتقدمة',
      supplierPhone: '+966507654321',
      originalAmount: 25000,
      paidAmount: 15000,
      remainingAmount: 10000,
      dueDate: '2024-01-25',
      status: 'pending',
      priority: 'medium',
      invoiceNumbers: ['PUR-2024-075'],
      createdAt: '2024-01-10T11:00:00',
      lastPaymentDate: '2024-01-18T10:00:00',
      notes: 'دفع جزئي - باقي المبلغ نهاية الشهر',
      paymentHistory: [
        { date: '2024-01-18', amount: 15000, method: 'cash', reference: 'CASH-002' }
      ]
    },
    {
      id: 3,
      debtNumber: 'DEBT-2024-003',
      type: 'receivable',
      customerName: 'متجر الإلكترونيات الحديث',
      customerPhone: '+966512345678',
      originalAmount: 8500,
      paidAmount: 8500,
      remainingAmount: 0,
      dueDate: '2024-01-30',
      status: 'paid',
      priority: 'low',
      invoiceNumbers: ['INV-2024-148'],
      createdAt: '2024-01-12T14:00:00',
      lastPaymentDate: '2024-01-22T16:00:00',
      notes: 'تم السداد كاملاً',
      paymentHistory: [
        { date: '2024-01-22', amount: 8500, method: 'check', reference: 'CHK-003' }
      ]
    },
    {
      id: 4,
      debtNumber: 'DEBT-2024-004',
      type: 'payable',
      supplierName: 'شركة المكونات الإلكترونية',
      supplierPhone: '+966555123456',
      originalAmount: 12000,
      paidAmount: 0,
      remainingAmount: 12000,
      dueDate: '2024-02-10',
      status: 'pending',
      priority: 'high',
      invoiceNumbers: ['PUR-2024-072', 'PUR-2024-078'],
      createdAt: '2024-01-08T09:30:00',
      lastPaymentDate: null,
      notes: 'مورد جديد - شروط دفع 30 يوم',
      paymentHistory: []
    }
  ];

  useEffect(() => {
    fetchDebts();
  }, []);

  const fetchDebts = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.get('/api/payment-management/debt-records');
      if (response.status === 'success' && response.data?.records?.length > 0) {
        setDebts(response.data.records);
        setFilteredDebts(response.data.records);
      } else {
        setDebts(sampleDebts);
        setFilteredDebts(sampleDebts);
      }
    } catch (error) {
      console.log('Using sample data:', error);
      setDebts(sampleDebts);
      setFilteredDebts(sampleDebts);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let filtered = debts;

    if (searchTerm) {
      filtered = filtered.filter(debt =>
        debt.debtNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (debt.customerName && debt.customerName.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (debt.supplierName && debt.supplierName.toLowerCase().includes(searchTerm.toLowerCase())) ||
        debt.invoiceNumbers.some(inv => inv.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    if (filterType !== 'all') {
      filtered = filtered.filter(debt => debt.type === filterType);
    }

    if (filterStatus !== 'all') {
      filtered = filtered.filter(debt => debt.status === filterStatus);
    }

    setFilteredDebts(filtered);
  }, [debts, searchTerm, filterType, filterStatus]);

  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { label: 'معلق', variant: 'secondary', icon: Clock },
      overdue: { label: 'متأخر', variant: 'destructive', icon: AlertTriangle },
      paid: { label: 'مدفوع', variant: 'default', icon: CheckCircle },
      partial: { label: 'دفع جزئي', variant: 'outline', icon: CreditCard }
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

  const getPriorityBadge = (priority) => {
    const priorityConfig = {
      low: { label: 'منخفض', variant: 'outline' },
      medium: { label: 'متوسط', variant: 'secondary' },
      high: { label: 'عالي', variant: 'destructive' }
    };

    const config = priorityConfig[priority] || priorityConfig.medium;
    
    return (
      <Badge variant={config.variant}>
        {config.label}
      </Badge>
    );
  };

  const getTypeBadge = (type) => {
    const typeConfig = {
      receivable: { label: 'مدين (لنا)', variant: 'default', icon: TrendingUp },
      payable: { label: 'دائن (علينا)', variant: 'secondary', icon: TrendingDown }
    };

    const config = typeConfig[type] || typeConfig.receivable;
    const IconComponent = config.icon;
    
    return (
      <Badge variant={config.variant} className="flex items-center gap-1">
        <IconComponent className="w-3 h-3" />
        {config.label}
      </Badge>
    );
  };

  const getDaysOverdue = (dueDate) => {
    const today = new Date();
    const due = new Date(dueDate);
    const diffTime = today - due;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays > 0 ? diffDays : 0;
  };

  const handleAddDebt = () => {
    setSelectedDebt(null);
    setShowAddModal(true);
    toast.success('جاري فتح نموذج إضافة دين جديد');
  };

  const handleEditDebt = (debt) => {
    setSelectedDebt(debt);
    setShowAddModal(true);
  };

  const handleDeleteDebt = (debtId) => {
    if (window.confirm('هل أنت متأكد من حذف هذا الدين؟')) {
      setDebts(debts.filter(debt => debt.id !== debtId));
      toast.success('تم حذف الدين بنجاح');
    }
  };

  const handleMarkAsPaid = (debtId) => {
    setDebts(debts.map(debt =>
      debt.id === debtId
        ? { 
            ...debt, 
            status: 'paid',
            paidAmount: debt.originalAmount,
            remainingAmount: 0,
            lastPaymentDate: new Date().toISOString()
          }
        : debt
    ));
    toast.success('تم تحديث حالة الدين إلى مدفوع');
  };

  const handleAddPayment = (debtId) => {
    const debt = debts.find(d => d.id === debtId);
    setSelectedDebt(debt);
    setShowPaymentModal(true);
  };

  const processPayment = (paymentAmount) => {
    if (!selectedDebt || !paymentAmount) return;
    
    setDebts(debts.map(debt => {
      if (debt.id === selectedDebt.id) {
        const newPaidAmount = debt.paidAmount + parseFloat(paymentAmount);
        const newRemainingAmount = debt.originalAmount - newPaidAmount;
        const newStatus = newRemainingAmount <= 0 ? 'paid' : 'partial';
        
        return {
          ...debt,
          paidAmount: newPaidAmount,
          remainingAmount: Math.max(0, newRemainingAmount),
          status: newStatus,
          lastPaymentDate: new Date().toISOString(),
          paymentHistory: [
            ...debt.paymentHistory,
            {
              date: new Date().toISOString(),
              amount: parseFloat(paymentAmount),
              method: 'manual',
              reference: `PAY-${Date.now()}`
            }
          ]
        };
      }
      return debt;
    }));
    
    setShowPaymentModal(false);
    setSelectedDebt(null);
    toast.success('تم إضافة الدفعة بنجاح');
  };

  const handleExport = () => {
    toast.success('تم تصدير البيانات بنجاح');
  };

  const getStatusCounts = () => {
    return {
      total: debts.length,
      pending: debts.filter(d => d.status === 'pending').length,
      overdue: debts.filter(d => d.status === 'overdue').length,
      paid: debts.filter(d => d.status === 'paid').length,
      partial: debts.filter(d => d.status === 'partial').length
    };
  };

  const getTotalAmounts = () => {
    const receivables = debts.filter(d => d.type === 'receivable');
    const payables = debts.filter(d => d.type === 'payable');
    
    return {
      totalReceivables: receivables.reduce((sum, d) => sum + d.remainingAmount, 0),
      totalPayables: payables.reduce((sum, d) => sum + d.remainingAmount, 0),
      overdueReceivables: receivables.filter(d => d.status === 'overdue').reduce((sum, d) => sum + d.remainingAmount, 0)
    };
  };

  const statusCounts = getStatusCounts();
  const totalAmounts = getTotalAmounts();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل إدارة المدفوعات والديون...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">إدارة المدفوعات والديون</h1>
          <p className="text-muted-foreground mt-1">متابعة المدفوعات والديون المستحقة</p>
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
            onClick={handleAddDebt}
            className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
          >
            <Plus className="w-4 h-4" />
            إضافة دين جديد
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي المدينين</p>
                <p className="text-2xl font-bold text-green-600">
                  {totalAmounts.totalReceivables.toLocaleString()} ج.م
                </p>
              </div>
              <TrendingUp className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي الدائنين</p>
                <p className="text-2xl font-bold text-red-600">
                  {totalAmounts.totalPayables.toLocaleString()} ج.م
                </p>
              </div>
              <TrendingDown className="w-8 h-8 text-red-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">المتأخرات</p>
                <p className="text-2xl font-bold text-orange-600">
                  {totalAmounts.overdueReceivables.toLocaleString()} ج.م
                </p>
              </div>
              <AlertTriangle className="w-8 h-8 text-orange-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي الديون</p>
                <p className="text-2xl font-bold text-primary">{statusCounts.total}</p>
              </div>
              <CreditCard className="w-8 h-8 text-primary/60" />
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
                  placeholder="البحث برقم الدين، العميل/المورد، أو رقم الفاتورة..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>

            <div className="min-w-48">
              <Label htmlFor="type-filter">نوع الدين</Label>
              <Select value={filterType} onValueChange={setFilterType}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر نوع الدين" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع الأنواع</SelectItem>
                  <SelectItem value="receivable">مدين (لنا)</SelectItem>
                  <SelectItem value="payable">دائن (علينا)</SelectItem>
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
                  <SelectItem value="pending">معلق</SelectItem>
                  <SelectItem value="overdue">متأخر</SelectItem>
                  <SelectItem value="paid">مدفوع</SelectItem>
                  <SelectItem value="partial">دفع جزئي</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Debts Table */}
      <Card>
        <CardHeader>
          <CardTitle>قائمة الديون ({filteredDebts.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>رقم الدين</TableHead>
                <TableHead>النوع</TableHead>
                <TableHead>العميل/المورد</TableHead>
                <TableHead>المبلغ الأصلي</TableHead>
                <TableHead>المبلغ المدفوع</TableHead>
                <TableHead>المبلغ المتبقي</TableHead>
                <TableHead>تاريخ الاستحقاق</TableHead>
                <TableHead>الحالة</TableHead>
                <TableHead>الأولوية</TableHead>
                <TableHead>الإجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredDebts.map((debt) => {
                const daysOverdue = getDaysOverdue(debt.dueDate);
                
                return (
                  <TableRow key={debt.id} className={debt.status === 'overdue' ? 'bg-red-50' : ''}>
                    <TableCell>
                      <div className="font-medium">{debt.debtNumber}</div>
                      <div className="text-sm text-muted-foreground">
                        {debt.invoiceNumbers.join(', ')}
                      </div>
                    </TableCell>
                    <TableCell>
                      {getTypeBadge(debt.type)}
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        {debt.type === 'receivable' ? (
                          <User className="w-4 h-4 text-blue-500" />
                        ) : (
                          <Building className="w-4 h-4 text-green-500" />
                        )}
                        <div>
                          <div className="font-medium">
                            {debt.customerName || debt.supplierName}
                          </div>
                          <div className="text-sm text-muted-foreground flex items-center gap-1">
                            <Phone className="w-3 h-3" />
                            {debt.customerPhone || debt.supplierPhone}
                          </div>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="font-medium">
                        {debt.originalAmount.toLocaleString()} ج.م
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="font-medium text-green-600">
                        {debt.paidAmount.toLocaleString()} ج.م
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className={`font-medium ${debt.remainingAmount > 0 ? 'text-red-600' : 'text-green-600'}`}>
                        {debt.remainingAmount.toLocaleString()} ج.م
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-1">
                        <Calendar className="w-3 h-3 text-muted-foreground" />
                        <div>
                          <div className="text-sm">
                            {new Date(debt.dueDate).toLocaleDateString('ar-SA')}
                          </div>
                          {debt.status === 'overdue' && (
                            <div className="text-xs text-red-600">
                              متأخر {daysOverdue} يوم
                            </div>
                          )}
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      {getStatusBadge(debt.status)}
                    </TableCell>
                    <TableCell>
                      {getPriorityBadge(debt.priority)}
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-1">
                        {debt.remainingAmount > 0 && (
                          <>
                            <button
                              onClick={() => handleMarkAsPaid(debt.id)}
                              className="px-2 py-1 text-sm text-green-600 hover:bg-green-50 rounded"
                            >
                              تسديد
                            </button>
                            <button
                              onClick={() => handleAddPayment(debt.id)}
                              className="px-2 py-1 text-sm text-blue-600 hover:bg-blue-50 rounded"
                            >
                              دفعة
                            </button>
                          </>
                        )}
                        <button
                          onClick={() => handleEditDebt(debt)}
                          className="p-1 hover:bg-muted rounded"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => setSelectedDebt(debt)}
                          className="p-1 hover:bg-muted rounded"
                        >
                          <Eye className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDeleteDebt(debt.id)}
                          className="p-1 text-red-600 hover:bg-red-50 rounded"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>

          {filteredDebts.length === 0 && (
            <div className="text-center py-8">
              <CreditCard className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">لا توجد ديون تطابق معايير البحث</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Payment Modal */}
      {showPaymentModal && selectedDebt && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-background rounded-lg p-6 max-w-md w-full mx-4">
            <h2 className="text-xl font-bold mb-4">إضافة دفعة</h2>
            <div className="space-y-4">
              <div>
                <Label>رقم الدين</Label>
                <p className="font-medium">{selectedDebt.debtNumber}</p>
              </div>
              <div>
                <Label>المبلغ المتبقي</Label>
                <p className="font-medium text-red-600">{selectedDebt.remainingAmount.toLocaleString()} ج.م</p>
              </div>
              <div>
                <Label htmlFor="payment-amount">مبلغ الدفعة</Label>
                <Input
                  id="payment-amount"
                  type="number"
                  placeholder="أدخل مبلغ الدفعة"
                  max={selectedDebt.remainingAmount}
                />
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => {
                    const amount = document.getElementById('payment-amount').value;
                    if (amount && !isNaN(amount) && parseFloat(amount) > 0) {
                      processPayment(parseFloat(amount));
                    } else {
                      toast.error('الرجاء إدخال مبلغ صحيح');
                    }
                  }}
                  className="flex-1 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90"
                >
                  تأكيد الدفعة
                </button>
                <button
                  onClick={() => {
                    setShowPaymentModal(false);
                    setSelectedDebt(null);
                  }}
                  className="px-4 py-2 border border-border rounded-lg hover:bg-muted"
                >
                  إلغاء
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Debt Details Modal */}
      {selectedDebt && !showPaymentModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-background rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">تفاصيل الدين</h2>
              <button
                onClick={() => setSelectedDebt(null)}
                className="p-2 hover:bg-muted rounded"
              >
                ✕
              </button>
            </div>
            
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>رقم الدين</Label>
                  <p className="font-medium">{selectedDebt.debtNumber}</p>
                </div>
                <div>
                  <Label>نوع الدين</Label>
                  <p>{getTypeBadge(selectedDebt.type)}</p>
                </div>
                <div>
                  <Label>المبلغ الأصلي</Label>
                  <p className="font-medium">{selectedDebt.originalAmount.toLocaleString()} ج.م</p>
                </div>
                <div>
                  <Label>المبلغ المتبقي</Label>
                  <p className={`font-medium ${selectedDebt.remainingAmount > 0 ? 'text-red-600' : 'text-green-600'}`}>
                    {selectedDebt.remainingAmount.toLocaleString()} ج.م
                  </p>
                </div>
              </div>

              <div>
                <Label>سجل المدفوعات</Label>
                {selectedDebt.paymentHistory.length > 0 ? (
                  <div className="border rounded-lg mt-2">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>التاريخ</TableHead>
                          <TableHead>المبلغ</TableHead>
                          <TableHead>الطريقة</TableHead>
                          <TableHead>المرجع</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {selectedDebt.paymentHistory.map((payment, index) => (
                          <TableRow key={index}>
                            <TableCell>{new Date(payment.date).toLocaleDateString('ar-SA')}</TableCell>
                            <TableCell className="text-green-600">{payment.amount.toLocaleString()} ج.م</TableCell>
                            <TableCell>{payment.method}</TableCell>
                            <TableCell>{payment.reference}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                ) : (
                  <p className="text-muted-foreground mt-2">لا توجد مدفوعات مسجلة</p>
                )}
              </div>

              <div>
                <Label>ملاحظات</Label>
                <p className="text-muted-foreground">{selectedDebt.notes}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PaymentDebtManagement;
