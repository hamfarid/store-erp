import React, { useState, useEffect } from 'react';
import {
  CreditCard, DollarSign, AlertTriangle, CheckCircle, XCircle,
  Search, Filter, Eye, Edit, Lock, Unlock, Plus, BarChart3,
  Clock, TrendingUp, TrendingDown, History, User
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
 * صفحة إدارة ائتمان العملاء
 * Customer Credit Management Page
 */
const CustomerCredit = () => {
  const [creditAccounts, setCreditAccounts] = useState([]);
  const [filteredAccounts, setFilteredAccounts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRisk, setFilterRisk] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [selectedAccount, setSelectedAccount] = useState(null);
  const [showStatement, setShowStatement] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [summary, setSummary] = useState(null);

  // بيانات نموذجية
  const sampleAccounts = [
    {
      id: 1,
      customer_id: 1,
      customer_name: 'شركة الأمل التجارية',
      credit_limit: 50000,
      available_credit: 30000,
      used_credit: 20000,
      utilization_percent: 40,
      total_outstanding: 20000,
      payment_terms_days: 30,
      is_active: true,
      is_blocked: false,
      risk_level: 'low',
      is_overdue: false,
      oldest_overdue_days: 0,
      last_payment_date: '2024-01-10T00:00:00'
    },
    {
      id: 2,
      customer_id: 2,
      customer_name: 'مؤسسة النور للتجارة',
      credit_limit: 30000,
      available_credit: 5000,
      used_credit: 25000,
      utilization_percent: 83.3,
      total_outstanding: 25000,
      payment_terms_days: 15,
      is_active: true,
      is_blocked: false,
      risk_level: 'high',
      is_overdue: true,
      oldest_overdue_days: 15,
      last_payment_date: '2024-01-01T00:00:00'
    },
    {
      id: 3,
      customer_id: 3,
      customer_name: 'شركة السلام للمقاولات',
      credit_limit: 100000,
      available_credit: 70000,
      used_credit: 30000,
      utilization_percent: 30,
      total_outstanding: 30000,
      payment_terms_days: 45,
      is_active: true,
      is_blocked: false,
      risk_level: 'medium',
      is_overdue: false,
      oldest_overdue_days: 0,
      last_payment_date: '2024-01-12T00:00:00'
    },
    {
      id: 4,
      customer_id: 4,
      customer_name: 'مؤسسة الفجر',
      credit_limit: 20000,
      available_credit: 0,
      used_credit: 20000,
      utilization_percent: 100,
      total_outstanding: 22000,
      payment_terms_days: 30,
      is_active: true,
      is_blocked: true,
      blocked_reason: 'تجاوز حد الائتمان',
      risk_level: 'high',
      is_overdue: true,
      oldest_overdue_days: 45,
      last_payment_date: '2023-12-01T00:00:00'
    }
  ];

  useEffect(() => {
    fetchCreditAccounts();
  }, []);

  const fetchCreditAccounts = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.get('/api/credit/accounts');
      if (response.status === 'success' && response.accounts?.length > 0) {
        setCreditAccounts(response.accounts);
        setFilteredAccounts(response.accounts);
        calculateSummary(response.accounts);
      } else {
        setCreditAccounts(sampleAccounts);
        setFilteredAccounts(sampleAccounts);
        calculateSummary(sampleAccounts);
      }
    } catch (error) {
      console.log('Using sample data:', error);
      setCreditAccounts(sampleAccounts);
      setFilteredAccounts(sampleAccounts);
      calculateSummary(sampleAccounts);
    } finally {
      setIsLoading(false);
    }
  };

  const calculateSummary = (accounts) => {
    setSummary({
      totalAccounts: accounts.length,
      totalCreditLimit: accounts.reduce((sum, a) => sum + a.credit_limit, 0),
      totalUsed: accounts.reduce((sum, a) => sum + a.used_credit, 0),
      totalAvailable: accounts.reduce((sum, a) => sum + a.available_credit, 0),
      totalOutstanding: accounts.reduce((sum, a) => sum + a.total_outstanding, 0),
      overdueCount: accounts.filter(a => a.is_overdue).length,
      blockedCount: accounts.filter(a => a.is_blocked).length,
      highRiskCount: accounts.filter(a => a.risk_level === 'high').length
    });
  };

  useEffect(() => {
    let filtered = creditAccounts;

    if (searchTerm) {
      filtered = filtered.filter(account =>
        account.customer_name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterRisk !== 'all') {
      filtered = filtered.filter(account => account.risk_level === filterRisk);
    }

    if (filterStatus !== 'all') {
      if (filterStatus === 'blocked') {
        filtered = filtered.filter(account => account.is_blocked);
      } else if (filterStatus === 'overdue') {
        filtered = filtered.filter(account => account.is_overdue);
      } else if (filterStatus === 'active') {
        filtered = filtered.filter(account => account.is_active && !account.is_blocked);
      }
    }

    setFilteredAccounts(filtered);
  }, [creditAccounts, searchTerm, filterRisk, filterStatus]);

  const getRiskBadge = (risk) => {
    const configs = {
      low: { color: 'bg-green-100 text-green-800', label: 'منخفض' },
      medium: { color: 'bg-yellow-100 text-yellow-800', label: 'متوسط' },
      high: { color: 'bg-red-100 text-red-800', label: 'مرتفع' }
    };
    const config = configs[risk] || configs.low;
    return (
      <span className={`px-2 py-1 text-xs font-medium rounded-full ${config.color}`}>
        {config.label}
      </span>
    );
  };

  const getUtilizationColor = (percent) => {
    if (percent < 50) return 'bg-green-500';
    if (percent < 75) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('ar-SA', {
      style: 'currency',
      currency: 'SAR',
      minimumFractionDigits: 0
    }).format(amount);
  };

  const handleBlockAccount = (account) => {
    if (window.confirm(`هل تريد ${account.is_blocked ? 'إلغاء حظر' : 'حظر'} حساب ${account.customer_name}؟`)) {
      setCreditAccounts(creditAccounts.map(a =>
        a.id === account.id ? { ...a, is_blocked: !a.is_blocked } : a
      ));
      toast.success(`تم ${account.is_blocked ? 'إلغاء حظر' : 'حظر'} الحساب`);
    }
  };

  const handleViewStatement = (account) => {
    setSelectedAccount(account);
    setShowStatement(true);
    toast.success('جاري تحميل كشف الحساب...');
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
            <CreditCard className="w-8 h-8" />
            إدارة ائتمان العملاء
          </h1>
          <p className="text-muted-foreground mt-1">إدارة حدود الائتمان والمديونيات</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors">
          <Plus className="w-4 h-4" />
          حساب ائتمان جديد
        </button>
      </div>

      {/* Summary Cards */}
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-4 lg:grid-cols-8 gap-4">
          <Card className="col-span-2">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">إجمالي حد الائتمان</p>
                  <p className="text-xl font-bold text-primary">{formatCurrency(summary.totalCreditLimit)}</p>
                </div>
                <CreditCard className="w-8 h-8 text-primary/60" />
              </div>
            </CardContent>
          </Card>

          <Card className="col-span-2">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">الائتمان المستخدم</p>
                  <p className="text-xl font-bold text-orange-600">{formatCurrency(summary.totalUsed)}</p>
                </div>
                <TrendingUp className="w-8 h-8 text-orange-500" />
              </div>
            </CardContent>
          </Card>

          <Card className="col-span-2">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">الائتمان المتاح</p>
                  <p className="text-xl font-bold text-green-600">{formatCurrency(summary.totalAvailable)}</p>
                </div>
                <TrendingDown className="w-8 h-8 text-green-500" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="text-center">
                <p className="text-sm text-muted-foreground">متأخر</p>
                <p className="text-2xl font-bold text-red-600">{summary.overdueCount}</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="text-center">
                <p className="text-sm text-muted-foreground">خطر عالي</p>
                <p className="text-2xl font-bold text-yellow-600">{summary.highRiskCount}</p>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

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
                  placeholder="البحث بالعميل..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>

            <div className="min-w-32">
              <Label htmlFor="risk-filter">مستوى الخطر</Label>
              <Select value={filterRisk} onValueChange={setFilterRisk}>
                <SelectTrigger>
                  <SelectValue placeholder="الكل" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">الكل</SelectItem>
                  <SelectItem value="low">منخفض</SelectItem>
                  <SelectItem value="medium">متوسط</SelectItem>
                  <SelectItem value="high">مرتفع</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="min-w-32">
              <Label htmlFor="status-filter">الحالة</Label>
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger>
                  <SelectValue placeholder="الكل" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">الكل</SelectItem>
                  <SelectItem value="active">نشط</SelectItem>
                  <SelectItem value="blocked">محظور</SelectItem>
                  <SelectItem value="overdue">متأخر</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Credit Accounts Table */}
      <Card>
        <CardHeader>
          <CardTitle>حسابات الائتمان ({filteredAccounts.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>العميل</TableHead>
                <TableHead>حد الائتمان</TableHead>
                <TableHead>المستخدم</TableHead>
                <TableHead>نسبة الاستخدام</TableHead>
                <TableHead>المستحق</TableHead>
                <TableHead>مستوى الخطر</TableHead>
                <TableHead>الحالة</TableHead>
                <TableHead>آخر دفعة</TableHead>
                <TableHead>الإجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredAccounts.map((account) => (
                <TableRow key={account.id} className={account.is_blocked ? 'opacity-60' : ''}>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <User className="w-4 h-4 text-muted-foreground" />
                      <span className="font-medium">{account.customer_name}</span>
                    </div>
                  </TableCell>
                  <TableCell className="font-mono">
                    {formatCurrency(account.credit_limit)}
                  </TableCell>
                  <TableCell className="font-mono text-orange-600">
                    {formatCurrency(account.used_credit)}
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-muted h-2 rounded-full">
                        <div 
                          className={`h-2 rounded-full ${getUtilizationColor(account.utilization_percent)}`}
                          style={{ width: `${Math.min(account.utilization_percent, 100)}%` }}
                        />
                      </div>
                      <span className="text-sm">{account.utilization_percent.toFixed(1)}%</span>
                    </div>
                  </TableCell>
                  <TableCell className="font-mono font-bold text-red-600">
                    {formatCurrency(account.total_outstanding)}
                  </TableCell>
                  <TableCell>
                    {getRiskBadge(account.risk_level)}
                  </TableCell>
                  <TableCell>
                    <div className="flex flex-col gap-1">
                      {account.is_blocked && (
                        <Badge variant="destructive" className="flex items-center gap-1 w-fit">
                          <Lock className="w-3 h-3" />
                          محظور
                        </Badge>
                      )}
                      {account.is_overdue && (
                        <Badge variant="outline" className="text-red-600 border-red-300 w-fit">
                          <Clock className="w-3 h-3 ml-1" />
                          متأخر {account.oldest_overdue_days} يوم
                        </Badge>
                      )}
                      {!account.is_blocked && !account.is_overdue && (
                        <Badge variant="default" className="bg-green-100 text-green-800 w-fit">
                          <CheckCircle className="w-3 h-3 ml-1" />
                          نشط
                        </Badge>
                      )}
                    </div>
                  </TableCell>
                  <TableCell className="text-sm">
                    {account.last_payment_date 
                      ? new Date(account.last_payment_date).toLocaleDateString('ar-SA')
                      : '-'}
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-1">
                      <button
                        onClick={() => handleViewStatement(account)}
                        className="p-2 hover:bg-muted rounded"
                        title="كشف الحساب"
                      >
                        <History className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => {
                          setSelectedAccount(account);
                          setShowEditModal(true);
                        }}
                        className="p-2 hover:bg-muted rounded"
                        title="تعديل"
                      >
                        <Edit className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleBlockAccount(account)}
                        className={`p-2 rounded ${account.is_blocked ? 'text-green-600 hover:bg-green-50' : 'text-red-600 hover:bg-red-50'}`}
                        title={account.is_blocked ? 'إلغاء الحظر' : 'حظر'}
                      >
                        {account.is_blocked ? <Unlock className="w-4 h-4" /> : <Lock className="w-4 h-4" />}
                      </button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>

          {filteredAccounts.length === 0 && (
            <div className="text-center py-8">
              <CreditCard className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">لا توجد حسابات تطابق معايير البحث</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Credit Risk Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="border-green-200 bg-green-50 dark:bg-green-900/20">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <CheckCircle className="w-10 h-10 text-green-600" />
              <div>
                <p className="text-sm text-muted-foreground">خطر منخفض</p>
                <p className="text-2xl font-bold text-green-600">
                  {creditAccounts.filter(a => a.risk_level === 'low').length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-yellow-200 bg-yellow-50 dark:bg-yellow-900/20">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <AlertTriangle className="w-10 h-10 text-yellow-600" />
              <div>
                <p className="text-sm text-muted-foreground">خطر متوسط</p>
                <p className="text-2xl font-bold text-yellow-600">
                  {creditAccounts.filter(a => a.risk_level === 'medium').length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-red-200 bg-red-50 dark:bg-red-900/20">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <XCircle className="w-10 h-10 text-red-600" />
              <div>
                <p className="text-sm text-muted-foreground">خطر مرتفع</p>
                <p className="text-2xl font-bold text-red-600">
                  {creditAccounts.filter(a => a.risk_level === 'high').length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default CustomerCredit;

