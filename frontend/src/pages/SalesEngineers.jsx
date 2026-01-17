import React, { useState, useEffect } from 'react';
import {
  Users, Plus, Search, Filter, Edit, Trash2, Eye, Phone, Mail,
  DollarSign, Target, TrendingUp, Award, Calendar, CheckCircle, XCircle
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
 * صفحة إدارة مهندسي المبيعات
 * Sales Engineers Management Page
 */
const SalesEngineers = () => {
  const [engineers, setEngineers] = useState([]);
  const [filteredEngineers, setFilteredEngineers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedEngineer, setSelectedEngineer] = useState(null);

  // بيانات نموذجية
  const sampleEngineers = [
    {
      id: 1,
      employee_id: 'EMP001',
      name: 'محمد أحمد',
      code: 'SE001',
      email: 'mohamed@company.com',
      phone: '0501234567',
      commission_rate: 5.0,
      target_monthly: 100000,
      achieved_monthly: 85000,
      status: 'active',
      hire_date: '2023-01-15',
      customers_count: 25,
      invoices_count: 150,
      total_sales: 1250000
    },
    {
      id: 2,
      employee_id: 'EMP002',
      name: 'أحمد علي',
      code: 'SE002',
      email: 'ahmed@company.com',
      phone: '0507654321',
      commission_rate: 4.5,
      target_monthly: 80000,
      achieved_monthly: 92000,
      status: 'active',
      hire_date: '2023-03-20',
      customers_count: 30,
      invoices_count: 180,
      total_sales: 1450000
    },
    {
      id: 3,
      employee_id: 'EMP003',
      name: 'سارة محمد',
      code: 'SE003',
      email: 'sara@company.com',
      phone: '0509876543',
      commission_rate: 5.5,
      target_monthly: 120000,
      achieved_monthly: 110000,
      status: 'active',
      hire_date: '2022-06-10',
      customers_count: 40,
      invoices_count: 220,
      total_sales: 2100000
    },
    {
      id: 4,
      employee_id: 'EMP004',
      name: 'خالد عبدالله',
      code: 'SE004',
      email: 'khaled@company.com',
      phone: '0505551234',
      commission_rate: 4.0,
      target_monthly: 60000,
      achieved_monthly: 45000,
      status: 'inactive',
      hire_date: '2023-09-01',
      customers_count: 15,
      invoices_count: 50,
      total_sales: 350000
    }
  ];

  useEffect(() => {
    fetchEngineers();
  }, []);

  const fetchEngineers = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.get('/api/sales-engineers');
      if (response.success && response.data?.length > 0) {
        setEngineers(response.data);
        setFilteredEngineers(response.data);
      } else {
        setEngineers(sampleEngineers);
        setFilteredEngineers(sampleEngineers);
      }
    } catch (error) {
      console.log('Using sample data:', error);
      setEngineers(sampleEngineers);
      setFilteredEngineers(sampleEngineers);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let filtered = engineers;

    if (searchTerm) {
      filtered = filtered.filter(eng =>
        eng.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        eng.employee_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
        eng.email.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterStatus !== 'all') {
      filtered = filtered.filter(eng => eng.status === filterStatus);
    }

    setFilteredEngineers(filtered);
  }, [engineers, searchTerm, filterStatus]);

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('ar-SA', {
      style: 'currency',
      currency: 'EGP',
      minimumFractionDigits: 0
    }).format(amount);
  };

  const getAchievementPercent = (achieved, target) => {
    if (!target || target === 0) return 0;
    return Math.round((achieved / target) * 100);
  };

  const getAchievementColor = (percent) => {
    if (percent >= 100) return 'text-green-600 bg-green-100';
    if (percent >= 75) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const handleDelete = (id) => {
    if (window.confirm('هل أنت متأكد من حذف مهندس المبيعات؟')) {
      setEngineers(engineers.filter(e => e.id !== id));
      toast.success('تم حذف مهندس المبيعات');
    }
  };

  const handleStatusChange = (id, newStatus) => {
    setEngineers(engineers.map(e =>
      e.id === id ? { ...e, status: newStatus } : e
    ));
    toast.success(`تم ${newStatus === 'active' ? 'تفعيل' : 'تعطيل'} مهندس المبيعات`);
  };

  // Calculate summary
  const summary = {
    total: engineers.length,
    active: engineers.filter(e => e.status === 'active').length,
    totalSales: engineers.reduce((sum, e) => sum + e.total_sales, 0),
    totalTarget: engineers.filter(e => e.status === 'active').reduce((sum, e) => sum + e.target_monthly, 0),
    totalAchieved: engineers.filter(e => e.status === 'active').reduce((sum, e) => sum + e.achieved_monthly, 0)
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
            <Users className="w-8 h-8" />
            مهندسي المبيعات
          </h1>
          <p className="text-muted-foreground mt-1">إدارة فريق المبيعات والأداء</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
        >
          <Plus className="w-4 h-4" />
          إضافة مهندس مبيعات
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي المهندسين</p>
                <p className="text-2xl font-bold text-primary">{summary.total}</p>
              </div>
              <Users className="w-8 h-8 text-primary/60" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">النشطين</p>
                <p className="text-2xl font-bold text-green-600">{summary.active}</p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي المبيعات</p>
                <p className="text-xl font-bold text-blue-600">{formatCurrency(summary.totalSales)}</p>
              </div>
              <DollarSign className="w-8 h-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">الهدف الشهري</p>
                <p className="text-xl font-bold text-purple-600">{formatCurrency(summary.totalTarget)}</p>
              </div>
              <Target className="w-8 h-8 text-purple-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">نسبة الإنجاز</p>
                <p className="text-2xl font-bold text-orange-600">
                  {getAchievementPercent(summary.totalAchieved, summary.totalTarget)}%
                </p>
              </div>
              <TrendingUp className="w-8 h-8 text-orange-500" />
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
                  placeholder="البحث بالاسم أو الكود..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pr-10"
                />
              </div>
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
                  <SelectItem value="inactive">غير نشط</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Engineers Table */}
      <Card>
        <CardHeader>
          <CardTitle>قائمة مهندسي المبيعات ({filteredEngineers.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>المهندس</TableHead>
                <TableHead>التواصل</TableHead>
                <TableHead>العمولة</TableHead>
                <TableHead>الهدف/المحقق</TableHead>
                <TableHead>العملاء</TableHead>
                <TableHead>إجمالي المبيعات</TableHead>
                <TableHead>الحالة</TableHead>
                <TableHead>الإجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredEngineers.map((engineer) => {
                const achievementPercent = getAchievementPercent(engineer.achieved_monthly, engineer.target_monthly);
                return (
                  <TableRow key={engineer.id}>
                    <TableCell>
                      <div>
                        <div className="font-medium">{engineer.name}</div>
                        <div className="text-sm text-muted-foreground">{engineer.employee_id}</div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="space-y-1">
                        <div className="flex items-center gap-1 text-sm">
                          <Mail className="w-3 h-3" />
                          {engineer.email}
                        </div>
                        <div className="flex items-center gap-1 text-sm">
                          <Phone className="w-3 h-3" />
                          {engineer.phone}
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">{engineer.commission_rate}%</Badge>
                    </TableCell>
                    <TableCell>
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span>{formatCurrency(engineer.achieved_monthly)}</span>
                          <span className="text-muted-foreground">من {formatCurrency(engineer.target_monthly)}</span>
                        </div>
                        <div className="w-full bg-muted h-2 rounded-full">
                          <div
                            className={`h-2 rounded-full ${achievementPercent >= 100 ? 'bg-green-500' : achievementPercent >= 75 ? 'bg-yellow-500' : 'bg-red-500'}`}
                            style={{ width: `${Math.min(achievementPercent, 100)}%` }}
                          />
                        </div>
                        <span className={`text-xs px-2 py-0.5 rounded-full ${getAchievementColor(achievementPercent)}`}>
                          {achievementPercent}%
                        </span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="text-center">
                        <div className="font-bold">{engineer.customers_count}</div>
                        <div className="text-xs text-muted-foreground">{engineer.invoices_count} فاتورة</div>
                      </div>
                    </TableCell>
                    <TableCell className="font-mono font-bold text-green-600">
                      {formatCurrency(engineer.total_sales)}
                    </TableCell>
                    <TableCell>
                      {engineer.status === 'active' ? (
                        <Badge variant="default" className="bg-green-100 text-green-800">نشط</Badge>
                      ) : (
                        <Badge variant="secondary">غير نشط</Badge>
                      )}
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-1">
                        <button
                          onClick={() => setSelectedEngineer(engineer)}
                          className="p-2 hover:bg-muted rounded"
                          title="عرض التفاصيل"
                        >
                          <Eye className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => setSelectedEngineer(engineer)}
                          className="p-2 hover:bg-muted rounded"
                          title="تعديل"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleStatusChange(engineer.id, engineer.status === 'active' ? 'inactive' : 'active')}
                          className={`p-2 rounded ${engineer.status === 'active' ? 'text-red-600 hover:bg-red-50' : 'text-green-600 hover:bg-green-50'}`}
                          title={engineer.status === 'active' ? 'تعطيل' : 'تفعيل'}
                        >
                          {engineer.status === 'active' ? <XCircle className="w-4 h-4" /> : <CheckCircle className="w-4 h-4" />}
                        </button>
                        <button
                          onClick={() => handleDelete(engineer.id)}
                          className="p-2 text-red-600 hover:bg-red-50 rounded"
                          title="حذف"
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

          {filteredEngineers.length === 0 && (
            <div className="text-center py-8">
              <Users className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">لا يوجد مهندسي مبيعات</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default SalesEngineers;

