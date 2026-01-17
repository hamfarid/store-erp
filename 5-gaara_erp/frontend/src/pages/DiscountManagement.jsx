import React, { useState, useEffect } from 'react';
import {
  Tag, Plus, Search, Edit, Trash2, Eye, Calendar, Percent, DollarSign,
  Package, Users, CheckCircle, XCircle, Clock, AlertTriangle, Copy
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
 * صفحة إدارة الخصومات
 * Discount Management Page
 */
const DiscountManagement = () => {
  const [discounts, setDiscounts] = useState([]);
  const [filteredDiscounts, setFilteredDiscounts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [isLoading, setIsLoading] = useState(true);

  // بيانات نموذجية
  const sampleDiscounts = [
    {
      id: 1,
      name: 'خصم الصيف 2024',
      code: 'SUMMER2024',
      type: 'percentage',
      value: 20,
      min_order: 500,
      max_discount: 200,
      applies_to: 'all',
      usage_limit: 100,
      used_count: 45,
      start_date: '2024-06-01',
      end_date: '2024-08-31',
      status: 'active',
      created_by: 'admin'
    },
    {
      id: 2,
      name: 'خصم العملاء الجدد',
      code: 'NEWCUSTOMER',
      type: 'percentage',
      value: 15,
      min_order: 200,
      max_discount: 100,
      applies_to: 'new_customers',
      usage_limit: null,
      used_count: 78,
      start_date: '2024-01-01',
      end_date: '2024-12-31',
      status: 'active',
      created_by: 'admin'
    },
    {
      id: 3,
      name: 'خصم مبلغ ثابت',
      code: 'FLAT50',
      type: 'fixed',
      value: 50,
      min_order: 300,
      max_discount: null,
      applies_to: 'all',
      usage_limit: 200,
      used_count: 200,
      start_date: '2024-01-01',
      end_date: '2024-06-30',
      status: 'expired',
      created_by: 'admin'
    },
    {
      id: 4,
      name: 'خصم فئة الإلكترونيات',
      code: 'ELEC10',
      type: 'percentage',
      value: 10,
      min_order: 1000,
      max_discount: 500,
      applies_to: 'category',
      category_id: 1,
      category_name: 'الإلكترونيات',
      usage_limit: 50,
      used_count: 23,
      start_date: '2024-01-15',
      end_date: '2024-03-15',
      status: 'active',
      created_by: 'admin'
    },
    {
      id: 5,
      name: 'خصم الجملة',
      code: 'BULK25',
      type: 'percentage',
      value: 25,
      min_order: 5000,
      max_discount: 2000,
      applies_to: 'all',
      usage_limit: 20,
      used_count: 8,
      start_date: '2024-01-01',
      end_date: '2024-12-31',
      status: 'active',
      created_by: 'manager'
    },
    {
      id: 6,
      name: 'خصم مجدول (قريباً)',
      code: 'UPCOMING20',
      type: 'percentage',
      value: 20,
      min_order: 400,
      max_discount: 150,
      applies_to: 'all',
      usage_limit: 100,
      used_count: 0,
      start_date: '2024-02-01',
      end_date: '2024-02-29',
      status: 'scheduled',
      created_by: 'admin'
    },
    {
      id: 7,
      name: 'خصم معطل',
      code: 'DISABLED10',
      type: 'percentage',
      value: 10,
      min_order: 100,
      max_discount: 50,
      applies_to: 'all',
      usage_limit: 500,
      used_count: 125,
      start_date: '2023-01-01',
      end_date: '2023-12-31',
      status: 'disabled',
      created_by: 'admin'
    }
  ];

  const typeConfig = {
    percentage: { label: 'نسبة مئوية', icon: Percent, color: 'bg-blue-100 text-blue-800' },
    fixed: { label: 'مبلغ ثابت', icon: DollarSign, color: 'bg-green-100 text-green-800' }
  };

  const statusConfig = {
    active: { label: 'نشط', color: 'bg-green-100 text-green-800', icon: CheckCircle },
    expired: { label: 'منتهي', color: 'bg-red-100 text-red-800', icon: XCircle },
    scheduled: { label: 'مجدول', color: 'bg-blue-100 text-blue-800', icon: Clock },
    disabled: { label: 'معطل', color: 'bg-gray-100 text-gray-800', icon: AlertTriangle }
  };

  const appliesToConfig = {
    all: 'جميع المنتجات',
    category: 'فئة محددة',
    product: 'منتج محدد',
    new_customers: 'العملاء الجدد',
    vip_customers: 'عملاء VIP'
  };

  useEffect(() => {
    fetchDiscounts();
  }, []);

  const fetchDiscounts = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.get('/api/discounts');
      if (response.success && response.data?.length > 0) {
        setDiscounts(response.data);
        setFilteredDiscounts(response.data);
      } else {
        setDiscounts(sampleDiscounts);
        setFilteredDiscounts(sampleDiscounts);
      }
    } catch (error) {
      console.log('Using sample data:', error);
      setDiscounts(sampleDiscounts);
      setFilteredDiscounts(sampleDiscounts);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let filtered = discounts;

    if (searchTerm) {
      filtered = filtered.filter(d =>
        d.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        d.code.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterType !== 'all') {
      filtered = filtered.filter(d => d.type === filterType);
    }

    if (filterStatus !== 'all') {
      filtered = filtered.filter(d => d.status === filterStatus);
    }

    setFilteredDiscounts(filtered);
  }, [discounts, searchTerm, filterType, filterStatus]);

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('ar-SA', {
      style: 'currency',
      currency: 'SAR',
      minimumFractionDigits: 0
    }).format(amount);
  };

  const getTypeBadge = (type) => {
    const config = typeConfig[type] || typeConfig.percentage;
    const Icon = config.icon;
    return (
      <span className={`inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full ${config.color}`}>
        <Icon className="w-3 h-3" />
        {config.label}
      </span>
    );
  };

  const getStatusBadge = (status) => {
    const config = statusConfig[status] || statusConfig.disabled;
    const Icon = config.icon;
    return (
      <span className={`inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full ${config.color}`}>
        <Icon className="w-3 h-3" />
        {config.label}
      </span>
    );
  };

  const getUsagePercent = (used, limit) => {
    if (!limit) return 0;
    return Math.round((used / limit) * 100);
  };

  const handleCopyCode = (code) => {
    navigator.clipboard.writeText(code);
    toast.success(`تم نسخ الكود: ${code}`);
  };

  const handleStatusChange = (discountId, newStatus) => {
    setDiscounts(discounts.map(d =>
      d.id === discountId ? { ...d, status: newStatus } : d
    ));
    toast.success(`تم تحديث حالة الخصم`);
  };

  const handleDelete = (discountId) => {
    if (window.confirm('هل أنت متأكد من حذف هذا الخصم؟')) {
      setDiscounts(discounts.filter(d => d.id !== discountId));
      toast.success('تم حذف الخصم بنجاح');
    }
  };

  // Calculate summary
  const summary = {
    total: discounts.length,
    active: discounts.filter(d => d.status === 'active').length,
    expired: discounts.filter(d => d.status === 'expired').length,
    scheduled: discounts.filter(d => d.status === 'scheduled').length,
    totalUsed: discounts.reduce((sum, d) => sum + d.used_count, 0)
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
            <Tag className="w-8 h-8" />
            إدارة الخصومات
          </h1>
          <p className="text-muted-foreground mt-1">إنشاء وإدارة أكواد الخصم والعروض</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors">
          <Plus className="w-4 h-4" />
          إضافة خصم جديد
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي الخصومات</p>
                <p className="text-2xl font-bold text-primary">{summary.total}</p>
              </div>
              <Tag className="w-8 h-8 text-primary/60" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">نشطة</p>
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
                <p className="text-sm text-muted-foreground">مجدولة</p>
                <p className="text-2xl font-bold text-blue-600">{summary.scheduled}</p>
              </div>
              <Clock className="w-8 h-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">منتهية</p>
                <p className="text-2xl font-bold text-red-600">{summary.expired}</p>
              </div>
              <XCircle className="w-8 h-8 text-red-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">مرات الاستخدام</p>
                <p className="text-2xl font-bold text-purple-600">{summary.totalUsed}</p>
              </div>
              <Users className="w-8 h-8 text-purple-500" />
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
              <Label htmlFor="type-filter">النوع</Label>
              <Select value={filterType} onValueChange={setFilterType}>
                <SelectTrigger>
                  <SelectValue placeholder="الكل" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">الكل</SelectItem>
                  <SelectItem value="percentage">نسبة مئوية</SelectItem>
                  <SelectItem value="fixed">مبلغ ثابت</SelectItem>
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
                  {Object.entries(statusConfig).map(([key, config]) => (
                    <SelectItem key={key} value={key}>{config.label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Discounts Table */}
      <Card>
        <CardHeader>
          <CardTitle>قائمة الخصومات ({filteredDiscounts.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>الخصم</TableHead>
                <TableHead>الكود</TableHead>
                <TableHead>النوع</TableHead>
                <TableHead>القيمة</TableHead>
                <TableHead>الحد الأدنى للطلب</TableHead>
                <TableHead>ينطبق على</TableHead>
                <TableHead>الاستخدام</TableHead>
                <TableHead>الفترة</TableHead>
                <TableHead>الحالة</TableHead>
                <TableHead>الإجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredDiscounts.map((discount) => {
                const usagePercent = getUsagePercent(discount.used_count, discount.usage_limit);
                return (
                  <TableRow key={discount.id} className={discount.status === 'disabled' ? 'opacity-60' : ''}>
                    <TableCell>
                      <div className="font-medium">{discount.name}</div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <code className="px-2 py-1 bg-muted rounded font-mono text-sm">
                          {discount.code}
                        </code>
                        <button
                          onClick={() => handleCopyCode(discount.code)}
                          className="p-1 hover:bg-muted rounded"
                          title="نسخ الكود"
                        >
                          <Copy className="w-3 h-3" />
                        </button>
                      </div>
                    </TableCell>
                    <TableCell>{getTypeBadge(discount.type)}</TableCell>
                    <TableCell className="font-bold">
                      {discount.type === 'percentage' ? `${discount.value}%` : formatCurrency(discount.value)}
                    </TableCell>
                    <TableCell>{formatCurrency(discount.min_order)}</TableCell>
                    <TableCell>
                      <Badge variant="outline">
                        {appliesToConfig[discount.applies_to]}
                      </Badge>
                      {discount.category_name && (
                        <div className="text-xs text-muted-foreground mt-1">
                          {discount.category_name}
                        </div>
                      )}
                    </TableCell>
                    <TableCell>
                      <div className="space-y-1">
                        <div className="text-sm">
                          {discount.used_count} / {discount.usage_limit || '∞'}
                        </div>
                        {discount.usage_limit && (
                          <div className="w-full bg-muted h-2 rounded-full">
                            <div
                              className={`h-2 rounded-full ${usagePercent >= 90 ? 'bg-red-500' : usagePercent >= 70 ? 'bg-yellow-500' : 'bg-green-500'}`}
                              style={{ width: `${Math.min(usagePercent, 100)}%` }}
                            />
                          </div>
                        )}
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="text-sm space-y-1">
                        <div className="flex items-center gap-1">
                          <Calendar className="w-3 h-3 text-muted-foreground" />
                          {new Date(discount.start_date).toLocaleDateString('ar-SA')}
                        </div>
                        <div className="flex items-center gap-1 text-muted-foreground">
                          <span>إلى</span>
                          {new Date(discount.end_date).toLocaleDateString('ar-SA')}
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>{getStatusBadge(discount.status)}</TableCell>
                    <TableCell>
                      <div className="flex gap-1">
                        <button className="p-2 hover:bg-muted rounded" title="عرض">
                          <Eye className="w-4 h-4" />
                        </button>
                        <button className="p-2 hover:bg-muted rounded" title="تعديل">
                          <Edit className="w-4 h-4" />
                        </button>
                        {discount.status === 'active' && (
                          <button
                            onClick={() => handleStatusChange(discount.id, 'disabled')}
                            className="p-2 text-orange-600 hover:bg-orange-50 rounded"
                            title="تعطيل"
                          >
                            <AlertTriangle className="w-4 h-4" />
                          </button>
                        )}
                        {discount.status === 'disabled' && (
                          <button
                            onClick={() => handleStatusChange(discount.id, 'active')}
                            className="p-2 text-green-600 hover:bg-green-50 rounded"
                            title="تفعيل"
                          >
                            <CheckCircle className="w-4 h-4" />
                          </button>
                        )}
                        <button
                          onClick={() => handleDelete(discount.id)}
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

          {filteredDiscounts.length === 0 && (
            <div className="text-center py-8">
              <Tag className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">لا توجد خصومات</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default DiscountManagement;

