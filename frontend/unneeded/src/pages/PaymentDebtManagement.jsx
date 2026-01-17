import React, { useState, useEffect } from 'react';
import {
  Clock, AlertTriangle, CheckCircle, TrendingUp, TrendingDown,
  Search, Filter, Download, Eye, Plus, Edit, Trash2, DollarSign, CreditCard
} from 'lucide-react';
import { toast } from 'react-hot-toast';

const PaymentDebtManagement = () => {
  const [debts, setDebts] = useState([]);
  const [filteredDebts, setFilteredDebts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedDebt, setSelectedDebt] = useState(null);

  // Sample data
  const sampleDebts = [
    {
      id: 1,
      debtNumber: 'DEBT-2024-001',
      type: 'receivable', // مدين (لنا)
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
      type: 'payable', // دائن (علينا)
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
    // Simulate API call
    setTimeout(() => {
      setDebts(sampleDebts);
      setFilteredDebts(sampleDebts);
      setIsLoading(false);
    }, 1000);
  }, []);

  useEffect(() => {
    let filtered = debts;

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(debt =>
        debt.debtNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (debt.customerName && debt.customerName.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (debt.supplierName && debt.supplierName.toLowerCase().includes(searchTerm.toLowerCase())) ||
        debt.invoiceNumbers.some(inv => inv.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    // Filter by type
    if (filterType !== 'all') {
      filtered = filtered.filter(debt => debt.type === filterType);
    }

    // Filter by status
    if (filterStatus !== 'all') {
      filtered = filtered.filter(debt => debt.status === filterStatus);
    }

    setFilteredDebts(filtered);
  }, [debts, searchTerm, filterType, filterStatus]);

  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { label: 'معلق', variant: 'secondary', icon: Clock, color: 'text-accent' },
      overdue: { label: 'متأخر', variant: 'destructive', icon: AlertTriangle, color: 'text-destructive' },
      paid: { label: 'مدفوع', variant: 'default', icon: CheckCircle, color: 'text-primary' },
      partial: { label: 'دفع جزئي', variant: 'outline', icon: CreditCard, color: 'text-primary' }
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
      low: { label: 'منخفض', variant: 'outline', color: 'text-muted-foreground' },
      medium: { label: 'متوسط', variant: 'secondary', color: 'text-accent' },
      high: { label: 'عالي', variant: 'destructive', color: 'text-destructive' }
    };

    const config = priorityConfig[priority] || priorityConfig.medium;
    
    return (
      <Badge variant={config.variant} className="flex items-center gap-1">
        {config.label}
      </Badge>
    );
  };

  const getTypeLabel = (type) => {
    const types = {
      receivable: 'مدين (لنا)',
      payable: 'دائن (علينا)'
    };
    return types[type] || type;
  };

  const getTypeBadge = (type) => {
    const typeConfig = {
      receivable: { label: 'مدين (لنا)', variant: 'default', icon: TrendingUp, color: 'text-primary' },
      payable: { label: 'دائن (علينا)', variant: 'secondary', icon: TrendingDown, color: 'text-destructive' }
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

  const isOverdue = (dueDate) => {
    return new Date(dueDate) < new Date();
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

  const handleAddPayment = (debtId, paymentAmount) => {
    setDebts(debts.map(debt => {
      if (debt.id === debtId) {
        const newPaidAmount = debt.paidAmount + paymentAmount;
        const newRemainingAmount = debt.originalAmount - newPaidAmount;
        const newStatus = newRemainingAmount === 0 ? 'paid' : 'partial';
        
        return {
          ...debt,
          paidAmount: newPaidAmount,
          remainingAmount: newRemainingAmount,
          status: newStatus,
          lastPaymentDate: new Date().toISOString(),
          paymentHistory: [
            ...debt.paymentHistory,
            {
              date: new Date().toISOString(),
              amount: paymentAmount,
              method: 'manual',
              reference: `PAY-${Date.now()}`
            }
          ]
        };
      }
      return debt;
    }));
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
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل إدارة المدفوعات والديون...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">إدارة المدفوعات والديون</h1>
          <p className="text-muted-foreground mt-1">متابعة المدفوعات والديون المستحقة</p>
        </div>
        <div className="flex gap-2">
          <Button onClick={handleExport} variant="outline">
            <Download className="w-4 h-4 mr-2" />
            تصدير
          </Button>
          <Button onClick={handleAddDebt}>
            <Plus className="w-4 h-4 mr-2" />
            إضافة دين جديد
          </Button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي المدينين</p>
                <p className="text-2xl font-bold text-primary">
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
                <p className="text-2xl font-bold text-destructive">
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
                <p className="text-2xl font-bold text-destructive">
                  {totalAmounts.overdueReceivables.toLocaleString()} ج.م
                </p>
              </div>
              <AlertTriangle className="w-8 h-8 text-red-500" />
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
              <CreditCard className="w-8 h-8 text-primary/100" />
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
                  placeholder="البحث برقم الدين، العميل/المورد، أو رقم الفاتورة..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
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
          <div className="overflow-x-auto">
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
                    <TableRow key={debt.id} className={debt.status === 'overdue' ? 'bg-destructive/10' : ''}>
                      <TableCell>
                        <div className="font-medium">{debt.debtNumber}</div>
                        <div className="text-sm text-gray-500">
                          {debt.invoiceNumbers.join(', ')}
                        </div>
                      </TableCell>
                      <TableCell>
                        {getTypeBadge(debt.type)}
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          {debt.type === 'receivable' ? (
                            <User className="w-4 h-4 text-primary/100" />
                          ) : (
                            <Building className="w-4 h-4 text-green-500" />
                          )}
                          <div>
                            <div className="font-medium">
                              {debt.customerName || debt.supplierName}
                            </div>
                            <div className="text-sm text-gray-500 flex items-center gap-1">
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
                        <div className="font-medium text-primary">
                          {debt.paidAmount.toLocaleString()} ج.م
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className={`font-medium ${debt.remainingAmount > 0 ? 'text-destructive' : 'text-primary'}`}>
                          {debt.remainingAmount.toLocaleString()} ج.م
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-1">
                          <Calendar className="w-3 h-3 text-gray-500" />
                          <div>
                            <div className="text-sm">
                              {new Date(debt.dueDate).toLocaleDateString('ar-SA')}
                            </div>
                            {debt.status === 'overdue' && (
                              <div className="text-xs text-destructive">
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
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleMarkAsPaid(debt.id)}
                                className="text-primary hover:text-primary"
                              >
                                تسديد
                              </Button>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => {
                                  const amount = prompt('أدخل مبلغ الدفعة:');
                                  if (amount && !isNaN(amount)) {
                                    handleAddPayment(debt.id, parseFloat(amount));
                                  }
                                }}
                                className="text-primary hover:text-primary/90"
                              >
                                دفعة
                              </Button>
                            </>
                          )}
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleEditDebt(debt)}
                          >
                            <Edit className="w-4 h-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => setSelectedDebt(debt)}
                          >
                            <Eye className="w-4 h-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleDeleteDebt(debt.id)}
                            className="text-destructive hover:text-destructive"
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </div>

          {filteredDebts.length === 0 && (
            <div className="text-center py-8">
              <CreditCard className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">لا توجد ديون تطابق معايير البحث</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default PaymentDebtManagement;

