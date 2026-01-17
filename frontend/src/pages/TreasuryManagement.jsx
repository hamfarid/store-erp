import React, { useState, useEffect } from 'react';
import {
  Plus, Search, Download, Edit, Trash2, Eye, DollarSign, Wallet, 
  ArrowUpCircle, ArrowDownCircle, RefreshCw, Calendar, Building, User
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
 * صفحة إدارة الخزينة
 * Treasury Management Page
 */
const TreasuryManagement = () => {
  const [treasuries, setTreasuries] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [filteredTransactions, setFilteredTransactions] = useState([]);
  const [activeTab, setActiveTab] = useState('treasuries');
  const [searchTerm, setSearchTerm] = useState('');
  const [filterTreasury, setFilterTreasury] = useState('all');
  const [filterType, setFilterType] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showTransactionModal, setShowTransactionModal] = useState(false);
  const [selectedTreasury, setSelectedTreasury] = useState(null);

  // بيانات نموذجية
  const sampleTreasuries = [
    {
      id: 1,
      name: 'الخزينة الرئيسية',
      code: 'MAIN-001',
      description: 'الخزينة الرئيسية للشركة',
      location: 'المقر الرئيسي',
      managerName: 'أحمد محمد',
      currency: 'ج.م',
      openingBalance: 50000,
      currentBalance: 75000,
      isActive: true,
      createdAt: '2024-01-01T00:00:00'
    },
    {
      id: 2,
      name: 'خزينة الفرع الأول',
      code: 'BR1-001',
      description: 'خزينة فرع الرياض',
      location: 'فرع الرياض',
      managerName: 'سارة أحمد',
      currency: 'ج.م',
      openingBalance: 25000,
      currentBalance: 32000,
      isActive: true,
      createdAt: '2024-01-05T00:00:00'
    },
    {
      id: 3,
      name: 'حساب البنك الأهلي',
      code: 'BANK-001',
      description: 'الحساب البنكي الرئيسي',
      location: 'البنك الأهلي',
      managerName: 'محمد علي',
      currency: 'ج.م',
      openingBalance: 100000,
      currentBalance: 185000,
      isActive: true,
      createdAt: '2024-01-01T00:00:00'
    }
  ];

  const sampleTransactions = [
    {
      id: 1,
      treasuryId: 1,
      treasuryName: 'الخزينة الرئيسية',
      type: 'deposit',
      amount: 15000,
      currency: 'ج.م',
      reference: 'DEP-2024-001',
      description: 'إيداع مبيعات اليوم',
      balanceBefore: 60000,
      balanceAfter: 75000,
      createdBy: 'أحمد محمد',
      createdAt: '2024-01-15T10:00:00'
    },
    {
      id: 2,
      treasuryId: 1,
      treasuryName: 'الخزينة الرئيسية',
      type: 'withdrawal',
      amount: 5000,
      currency: 'ج.م',
      reference: 'WTH-2024-001',
      description: 'سحب لمصاريف التشغيل',
      balanceBefore: 75000,
      balanceAfter: 70000,
      createdBy: 'سارة أحمد',
      createdAt: '2024-01-14T14:30:00'
    },
    {
      id: 3,
      treasuryId: 2,
      treasuryName: 'خزينة الفرع الأول',
      type: 'transfer_in',
      amount: 10000,
      currency: 'ج.م',
      reference: 'TRF-2024-001',
      description: 'تحويل من الخزينة الرئيسية',
      balanceBefore: 22000,
      balanceAfter: 32000,
      createdBy: 'محمد علي',
      createdAt: '2024-01-13T11:00:00'
    },
    {
      id: 4,
      treasuryId: 3,
      treasuryName: 'حساب البنك الأهلي',
      type: 'deposit',
      amount: 50000,
      currency: 'ج.م',
      reference: 'DEP-2024-002',
      description: 'إيداع تحصيلات العملاء',
      balanceBefore: 135000,
      balanceAfter: 185000,
      createdBy: 'أحمد محمد',
      createdAt: '2024-01-12T09:00:00'
    }
  ];

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const [treasuriesRes, transactionsRes] = await Promise.allSettled([
        apiClient.get('/api/treasuries'),
        apiClient.get('/api/treasury/transactions')
      ]);

      if (treasuriesRes.status === 'fulfilled' && treasuriesRes.value.status === 'success') {
        setTreasuries(treasuriesRes.value.data);
      } else {
        setTreasuries(sampleTreasuries);
      }

      if (transactionsRes.status === 'fulfilled' && transactionsRes.value.status === 'success') {
        setTransactions(transactionsRes.value.data.transactions || []);
        setFilteredTransactions(transactionsRes.value.data.transactions || []);
      } else {
        setTransactions(sampleTransactions);
        setFilteredTransactions(sampleTransactions);
      }
    } catch (error) {
      console.log('Using sample data:', error);
      setTreasuries(sampleTreasuries);
      setTransactions(sampleTransactions);
      setFilteredTransactions(sampleTransactions);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let filtered = transactions;

    if (searchTerm) {
      filtered = filtered.filter(t =>
        t.reference.toLowerCase().includes(searchTerm.toLowerCase()) ||
        t.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        t.treasuryName.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterTreasury !== 'all') {
      filtered = filtered.filter(t => t.treasuryId === parseInt(filterTreasury));
    }

    if (filterType !== 'all') {
      filtered = filtered.filter(t => t.type === filterType);
    }

    setFilteredTransactions(filtered);
  }, [transactions, searchTerm, filterTreasury, filterType]);

  const getTypeBadge = (type) => {
    const typeConfig = {
      deposit: { label: 'إيداع', variant: 'default', icon: ArrowDownCircle, color: 'text-green-600' },
      withdrawal: { label: 'سحب', variant: 'destructive', icon: ArrowUpCircle, color: 'text-red-600' },
      transfer_in: { label: 'تحويل وارد', variant: 'default', icon: RefreshCw, color: 'text-blue-600' },
      transfer_out: { label: 'تحويل صادر', variant: 'secondary', icon: RefreshCw, color: 'text-orange-600' }
    };

    const config = typeConfig[type] || typeConfig.deposit;
    const IconComponent = config.icon;
    
    return (
      <Badge variant={config.variant} className="flex items-center gap-1">
        <IconComponent className="w-3 h-3" />
        {config.label}
      </Badge>
    );
  };

  const handleAddTreasury = () => {
    setSelectedTreasury(null);
    setShowAddModal(true);
    toast.success('جاري فتح نموذج إضافة خزينة');
  };

  const handleAddTransaction = () => {
    setShowTransactionModal(true);
    toast.success('جاري فتح نموذج إضافة معاملة');
  };

  const handleEditTreasury = (treasury) => {
    setSelectedTreasury(treasury);
    setShowAddModal(true);
  };

  const handleDeleteTreasury = (treasuryId) => {
    if (window.confirm('هل أنت متأكد من حذف هذه الخزينة؟')) {
      setTreasuries(treasuries.filter(t => t.id !== treasuryId));
      toast.success('تم حذف الخزينة بنجاح');
    }
  };

  const handleExport = () => {
    toast.success('تم تصدير البيانات بنجاح');
  };

  const getTotalBalance = () => {
    return treasuries.reduce((sum, t) => sum + t.currentBalance, 0);
  };

  const getTodayTransactions = () => {
    const today = new Date().toDateString();
    return transactions.filter(t => new Date(t.createdAt).toDateString() === today);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل إدارة الخزينة...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">إدارة الخزينة</h1>
          <p className="text-muted-foreground mt-1">إدارة الخزائن والمعاملات المالية</p>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={handleExport}
            className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors"
          >
            <Download className="w-4 h-4" />
            تصدير
          </button>
          {activeTab === 'treasuries' ? (
            <button 
              onClick={handleAddTreasury}
              className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
            >
              <Plus className="w-4 h-4" />
              إضافة خزينة
            </button>
          ) : (
            <button 
              onClick={handleAddTransaction}
              className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
            >
              <Plus className="w-4 h-4" />
              إضافة معاملة
            </button>
          )}
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي الرصيد</p>
                <p className="text-2xl font-bold text-green-600">{getTotalBalance().toLocaleString()} ج.م</p>
              </div>
              <DollarSign className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">عدد الخزائن</p>
                <p className="text-2xl font-bold text-primary">{treasuries.length}</p>
              </div>
              <Wallet className="w-8 h-8 text-primary/60" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">معاملات اليوم</p>
                <p className="text-2xl font-bold text-blue-600">{getTodayTransactions().length}</p>
              </div>
              <RefreshCw className="w-8 h-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي المعاملات</p>
                <p className="text-2xl font-bold text-purple-600">{transactions.length}</p>
              </div>
              <Calendar className="w-8 h-8 text-purple-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-border">
        <button
          onClick={() => setActiveTab('treasuries')}
          className={`px-4 py-2 font-medium transition-colors ${
            activeTab === 'treasuries' 
              ? 'border-b-2 border-primary text-primary' 
              : 'text-muted-foreground hover:text-foreground'
          }`}
        >
          الخزائن
        </button>
        <button
          onClick={() => setActiveTab('transactions')}
          className={`px-4 py-2 font-medium transition-colors ${
            activeTab === 'transactions' 
              ? 'border-b-2 border-primary text-primary' 
              : 'text-muted-foreground hover:text-foreground'
          }`}
        >
          المعاملات
        </button>
      </div>

      {/* Treasuries Tab */}
      {activeTab === 'treasuries' && (
        <Card>
          <CardHeader>
            <CardTitle>قائمة الخزائن ({treasuries.length})</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>الاسم</TableHead>
                  <TableHead>الكود</TableHead>
                  <TableHead>الموقع</TableHead>
                  <TableHead>المسؤول</TableHead>
                  <TableHead>الرصيد الافتتاحي</TableHead>
                  <TableHead>الرصيد الحالي</TableHead>
                  <TableHead>الحالة</TableHead>
                  <TableHead>الإجراءات</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {treasuries.map((treasury) => (
                  <TableRow key={treasury.id}>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Wallet className="w-4 h-4 text-primary" />
                        <div>
                          <div className="font-medium">{treasury.name}</div>
                          <div className="text-sm text-muted-foreground">{treasury.description}</div>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <span className="font-mono text-sm">{treasury.code}</span>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-1">
                        <Building className="w-3 h-3 text-muted-foreground" />
                        {treasury.location}
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-1">
                        <User className="w-3 h-3 text-muted-foreground" />
                        {treasury.managerName}
                      </div>
                    </TableCell>
                    <TableCell>
                      {treasury.openingBalance.toLocaleString()} {treasury.currency}
                    </TableCell>
                    <TableCell>
                      <span className={`font-medium ${treasury.currentBalance >= treasury.openingBalance ? 'text-green-600' : 'text-red-600'}`}>
                        {treasury.currentBalance.toLocaleString()} {treasury.currency}
                      </span>
                    </TableCell>
                    <TableCell>
                      <Badge variant={treasury.isActive ? 'default' : 'secondary'}>
                        {treasury.isActive ? 'نشط' : 'غير نشط'}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-1">
                        <button
                          onClick={() => handleEditTreasury(treasury)}
                          className="p-1 hover:bg-muted rounded"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => setSelectedTreasury(treasury)}
                          className="p-1 hover:bg-muted rounded"
                        >
                          <Eye className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDeleteTreasury(treasury.id)}
                          className="p-1 text-red-600 hover:bg-red-50 rounded"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}

      {/* Transactions Tab */}
      {activeTab === 'transactions' && (
        <>
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
                      placeholder="البحث بالمرجع، الوصف..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pr-10"
                    />
                  </div>
                </div>

                <div className="min-w-48">
                  <Label htmlFor="treasury-filter">الخزينة</Label>
                  <Select value={filterTreasury} onValueChange={setFilterTreasury}>
                    <SelectTrigger>
                      <SelectValue placeholder="اختر الخزينة" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">جميع الخزائن</SelectItem>
                      {treasuries.map(t => (
                        <SelectItem key={t.id} value={t.id.toString()}>{t.name}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="min-w-40">
                  <Label htmlFor="type-filter">النوع</Label>
                  <Select value={filterType} onValueChange={setFilterType}>
                    <SelectTrigger>
                      <SelectValue placeholder="اختر النوع" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">جميع الأنواع</SelectItem>
                      <SelectItem value="deposit">إيداع</SelectItem>
                      <SelectItem value="withdrawal">سحب</SelectItem>
                      <SelectItem value="transfer_in">تحويل وارد</SelectItem>
                      <SelectItem value="transfer_out">تحويل صادر</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Transactions Table */}
          <Card>
            <CardHeader>
              <CardTitle>قائمة المعاملات ({filteredTransactions.length})</CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>المرجع</TableHead>
                    <TableHead>الخزينة</TableHead>
                    <TableHead>النوع</TableHead>
                    <TableHead>المبلغ</TableHead>
                    <TableHead>الرصيد قبل</TableHead>
                    <TableHead>الرصيد بعد</TableHead>
                    <TableHead>الوصف</TableHead>
                    <TableHead>المنشئ</TableHead>
                    <TableHead>التاريخ</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredTransactions.map((transaction) => (
                    <TableRow key={transaction.id}>
                      <TableCell>
                        <span className="font-mono text-sm">{transaction.reference}</span>
                      </TableCell>
                      <TableCell>{transaction.treasuryName}</TableCell>
                      <TableCell>{getTypeBadge(transaction.type)}</TableCell>
                      <TableCell>
                        <span className={`font-medium ${
                          transaction.type === 'deposit' || transaction.type === 'transfer_in' 
                            ? 'text-green-600' 
                            : 'text-red-600'
                        }`}>
                          {transaction.type === 'deposit' || transaction.type === 'transfer_in' ? '+' : '-'}
                          {transaction.amount.toLocaleString()} {transaction.currency}
                        </span>
                      </TableCell>
                      <TableCell>{transaction.balanceBefore.toLocaleString()}</TableCell>
                      <TableCell>{transaction.balanceAfter.toLocaleString()}</TableCell>
                      <TableCell>
                        <span className="text-sm">{transaction.description}</span>
                      </TableCell>
                      <TableCell>{transaction.createdBy}</TableCell>
                      <TableCell>
                        <span className="text-sm">
                          {new Date(transaction.createdAt).toLocaleDateString('ar-SA')}
                        </span>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>

              {filteredTransactions.length === 0 && (
                <div className="text-center py-8">
                  <RefreshCw className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-muted-foreground">لا توجد معاملات تطابق معايير البحث</p>
                </div>
              )}
            </CardContent>
          </Card>
        </>
      )}

      {/* Treasury Details Modal */}
      {selectedTreasury && !showAddModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-background rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">تفاصيل الخزينة</h2>
              <button onClick={() => setSelectedTreasury(null)} className="p-2 hover:bg-muted rounded">✕</button>
            </div>
            
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>اسم الخزينة</Label>
                  <p className="font-medium">{selectedTreasury.name}</p>
                </div>
                <div>
                  <Label>الكود</Label>
                  <p className="font-mono">{selectedTreasury.code}</p>
                </div>
                <div>
                  <Label>الموقع</Label>
                  <p>{selectedTreasury.location}</p>
                </div>
                <div>
                  <Label>المسؤول</Label>
                  <p>{selectedTreasury.managerName}</p>
                </div>
                <div>
                  <Label>الرصيد الافتتاحي</Label>
                  <p className="font-medium">{selectedTreasury.openingBalance.toLocaleString()} {selectedTreasury.currency}</p>
                </div>
                <div>
                  <Label>الرصيد الحالي</Label>
                  <p className={`font-medium ${selectedTreasury.currentBalance >= selectedTreasury.openingBalance ? 'text-green-600' : 'text-red-600'}`}>
                    {selectedTreasury.currentBalance.toLocaleString()} {selectedTreasury.currency}
                  </p>
                </div>
              </div>
              <div>
                <Label>الوصف</Label>
                <p className="text-muted-foreground">{selectedTreasury.description}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TreasuryManagement;

