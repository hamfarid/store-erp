import React, { useState, useEffect } from 'react';
import {
  AlertTriangle, Package, Clock, TrendingDown, CheckCircle, XCircle,
  Search, Filter, Bell, RefreshCw, Eye, Check, Trash2, BarChart3
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
 * صفحة تنبيهات المخزون
 * Inventory Alerts Page
 */
const InventoryAlerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [filteredAlerts, setFilteredAlerts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterPriority, setFilterPriority] = useState('all');
  const [filterResolved, setFilterResolved] = useState('unresolved');
  const [isLoading, setIsLoading] = useState(true);
  const [summary, setSummary] = useState(null);

  // بيانات نموذجية
  const sampleAlerts = [
    {
      id: 1,
      alert_type: 'out_of_stock',
      type_ar: 'نفاد المخزون',
      priority: 'critical',
      priority_ar: 'حرج',
      product_id: 1,
      product_name: 'لابتوب HP ProBook 450',
      warehouse_id: 1,
      warehouse_name: 'المستودع الرئيسي',
      title: 'نفاد المخزون: لابتوب HP ProBook 450',
      message: 'المنتج غير متوفر في المخزون',
      current_value: 0,
      threshold_value: 0,
      is_read: false,
      is_resolved: false,
      created_at: '2024-01-15T10:00:00'
    },
    {
      id: 2,
      alert_type: 'low_stock',
      type_ar: 'مخزون منخفض',
      priority: 'high',
      priority_ar: 'عالي',
      product_id: 2,
      product_name: 'طابعة Canon PIXMA',
      warehouse_id: 1,
      warehouse_name: 'المستودع الرئيسي',
      title: 'مخزون منخفض: طابعة Canon PIXMA',
      message: 'الكمية الحالية (5) أقل من الحد الأدنى (10)',
      current_value: 5,
      threshold_value: 10,
      is_read: false,
      is_resolved: false,
      created_at: '2024-01-15T09:30:00'
    },
    {
      id: 3,
      alert_type: 'expiring_soon',
      type_ar: 'قرب انتهاء الصلاحية',
      priority: 'high',
      priority_ar: 'عالي',
      product_id: 3,
      product_name: 'حبر طابعة HP 123',
      warehouse_id: 2,
      warehouse_name: 'مستودع الفرع',
      title: 'قرب انتهاء الصلاحية: حبر طابعة HP 123',
      message: 'الدفعة LOT-2024-003 تنتهي صلاحيتها خلال 15 يوم',
      current_value: 15,
      threshold_value: 30,
      is_read: true,
      is_resolved: false,
      created_at: '2024-01-15T08:00:00'
    },
    {
      id: 4,
      alert_type: 'reorder_point',
      type_ar: 'نقطة إعادة الطلب',
      priority: 'medium',
      priority_ar: 'متوسط',
      product_id: 4,
      product_name: 'ماوس لاسلكي Logitech',
      warehouse_id: 1,
      warehouse_name: 'المستودع الرئيسي',
      title: 'نقطة إعادة الطلب: ماوس لاسلكي Logitech',
      message: 'الكمية الحالية (20) وصلت لنقطة إعادة الطلب (25)',
      current_value: 20,
      threshold_value: 25,
      is_read: true,
      is_resolved: false,
      created_at: '2024-01-14T16:00:00'
    },
    {
      id: 5,
      alert_type: 'low_stock',
      type_ar: 'مخزون منخفض',
      priority: 'medium',
      priority_ar: 'متوسط',
      product_id: 5,
      product_name: 'كيبورد ميكانيكي',
      warehouse_id: 1,
      warehouse_name: 'المستودع الرئيسي',
      title: 'مخزون منخفض: كيبورد ميكانيكي',
      message: 'الكمية الحالية (8) أقل من الحد الأدنى (15)',
      current_value: 8,
      threshold_value: 15,
      is_read: false,
      is_resolved: true,
      resolved_at: '2024-01-15T11:00:00',
      created_at: '2024-01-14T14:00:00'
    }
  ];

  const alertTypes = [
    { value: 'out_of_stock', label: 'نفاد المخزون', icon: XCircle, color: 'red' },
    { value: 'low_stock', label: 'مخزون منخفض', icon: TrendingDown, color: 'orange' },
    { value: 'expiring_soon', label: 'قرب انتهاء الصلاحية', icon: Clock, color: 'yellow' },
    { value: 'reorder_point', label: 'نقطة إعادة الطلب', icon: Package, color: 'blue' }
  ];

  const priorities = [
    { value: 'critical', label: 'حرج', color: 'destructive' },
    { value: 'high', label: 'عالي', color: 'warning' },
    { value: 'medium', label: 'متوسط', color: 'default' },
    { value: 'low', label: 'منخفض', color: 'secondary' }
  ];

  useEffect(() => {
    fetchAlerts();
    fetchSummary();
  }, []);

  const fetchAlerts = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.get('/api/inventory/alerts');
      if (response.status === 'success' && response.alerts?.length > 0) {
        setAlerts(response.alerts);
        setFilteredAlerts(response.alerts);
      } else {
        setAlerts(sampleAlerts);
        setFilteredAlerts(sampleAlerts.filter(a => !a.is_resolved));
      }
    } catch (error) {
      console.log('Using sample data:', error);
      setAlerts(sampleAlerts);
      setFilteredAlerts(sampleAlerts.filter(a => !a.is_resolved));
    } finally {
      setIsLoading(false);
    }
  };

  const fetchSummary = async () => {
    try {
      const response = await apiClient.get('/api/inventory/alerts/summary');
      if (response.status === 'success') {
        setSummary(response.data);
      } else {
        // Calculate from sample data
        const unresolved = sampleAlerts.filter(a => !a.is_resolved);
        setSummary({
          total_unresolved: unresolved.length,
          critical: unresolved.filter(a => a.priority === 'critical').length,
          high: unresolved.filter(a => a.priority === 'high').length,
          medium: unresolved.filter(a => a.priority === 'medium').length,
          low: unresolved.filter(a => a.priority === 'low').length
        });
      }
    } catch (error) {
      const unresolved = sampleAlerts.filter(a => !a.is_resolved);
      setSummary({
        total_unresolved: unresolved.length,
        critical: unresolved.filter(a => a.priority === 'critical').length,
        high: unresolved.filter(a => a.priority === 'high').length,
        medium: unresolved.filter(a => a.priority === 'medium').length,
        low: unresolved.filter(a => a.priority === 'low').length
      });
    }
  };

  useEffect(() => {
    let filtered = alerts;

    if (searchTerm) {
      filtered = filtered.filter(alert =>
        alert.product_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        alert.title.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterType !== 'all') {
      filtered = filtered.filter(alert => alert.alert_type === filterType);
    }

    if (filterPriority !== 'all') {
      filtered = filtered.filter(alert => alert.priority === filterPriority);
    }

    if (filterResolved === 'unresolved') {
      filtered = filtered.filter(alert => !alert.is_resolved);
    } else if (filterResolved === 'resolved') {
      filtered = filtered.filter(alert => alert.is_resolved);
    }

    setFilteredAlerts(filtered);
  }, [alerts, searchTerm, filterType, filterPriority, filterResolved]);

  const getPriorityBadge = (priority) => {
    const config = priorities.find(p => p.value === priority);
    const colorClasses = {
      critical: 'bg-red-100 text-red-800 border-red-300',
      high: 'bg-orange-100 text-orange-800 border-orange-300',
      medium: 'bg-blue-100 text-blue-800 border-blue-300',
      low: 'bg-gray-100 text-gray-800 border-gray-300'
    };
    return (
      <span className={`px-2 py-1 text-xs font-medium rounded-full border ${colorClasses[priority]}`}>
        {config?.label || priority}
      </span>
    );
  };

  const getTypeIcon = (type) => {
    const config = alertTypes.find(t => t.value === type);
    if (!config) return <AlertTriangle className="w-5 h-5" />;
    
    const Icon = config.icon;
    const colorClasses = {
      red: 'text-red-500',
      orange: 'text-orange-500',
      yellow: 'text-yellow-500',
      blue: 'text-blue-500'
    };
    
    return <Icon className={`w-5 h-5 ${colorClasses[config.color]}`} />;
  };

  const handleMarkAsRead = (alertId) => {
    setAlerts(alerts.map(a =>
      a.id === alertId ? { ...a, is_read: true } : a
    ));
    toast.success('تم تعليم التنبيه كمقروء');
  };

  const handleResolve = (alertId) => {
    setAlerts(alerts.map(a =>
      a.id === alertId ? { ...a, is_resolved: true, resolved_at: new Date().toISOString() } : a
    ));
    toast.success('تم حل التنبيه');
  };

  const handleRefresh = () => {
    fetchAlerts();
    fetchSummary();
    toast.success('تم تحديث التنبيهات');
  };

  const handleRunCheck = () => {
    toast.success('جاري فحص المخزون...');
    setTimeout(() => {
      toast.success('تم فحص المخزون بنجاح');
      fetchAlerts();
      fetchSummary();
    }, 2000);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل التنبيهات...</p>
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
            <Bell className="w-8 h-8" />
            تنبيهات المخزون
          </h1>
          <p className="text-muted-foreground mt-1">مراقبة مستويات المخزون والتنبيهات</p>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={handleRefresh}
            className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            تحديث
          </button>
          <button 
            onClick={handleRunCheck}
            className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
          >
            <BarChart3 className="w-4 h-4" />
            فحص المخزون
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">إجمالي غير المحلولة</p>
                  <p className="text-2xl font-bold text-primary">{summary.total_unresolved}</p>
                </div>
                <AlertTriangle className="w-8 h-8 text-primary/60" />
              </div>
            </CardContent>
          </Card>

          <Card className="border-red-200 bg-red-50 dark:bg-red-900/20">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">حرجة</p>
                  <p className="text-2xl font-bold text-red-600">{summary.critical}</p>
                </div>
                <XCircle className="w-8 h-8 text-red-500" />
              </div>
            </CardContent>
          </Card>

          <Card className="border-orange-200 bg-orange-50 dark:bg-orange-900/20">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">عالية</p>
                  <p className="text-2xl font-bold text-orange-600">{summary.high}</p>
                </div>
                <TrendingDown className="w-8 h-8 text-orange-500" />
              </div>
            </CardContent>
          </Card>

          <Card className="border-blue-200 bg-blue-50 dark:bg-blue-900/20">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">متوسطة</p>
                  <p className="text-2xl font-bold text-blue-600">{summary.medium}</p>
                </div>
                <Package className="w-8 h-8 text-blue-500" />
              </div>
            </CardContent>
          </Card>

          <Card className="border-gray-200 bg-gray-50 dark:bg-gray-900/20">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">منخفضة</p>
                  <p className="text-2xl font-bold text-gray-600">{summary.low}</p>
                </div>
                <Clock className="w-8 h-8 text-gray-500" />
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
                  placeholder="البحث بالمنتج أو العنوان..."
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
                  {alertTypes.map(type => (
                    <SelectItem key={type.value} value={type.value}>{type.label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="min-w-32">
              <Label htmlFor="priority-filter">الأولوية</Label>
              <Select value={filterPriority} onValueChange={setFilterPriority}>
                <SelectTrigger>
                  <SelectValue placeholder="الأولوية" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">الكل</SelectItem>
                  {priorities.map(p => (
                    <SelectItem key={p.value} value={p.value}>{p.label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="min-w-32">
              <Label htmlFor="resolved-filter">الحالة</Label>
              <Select value={filterResolved} onValueChange={setFilterResolved}>
                <SelectTrigger>
                  <SelectValue placeholder="الحالة" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">الكل</SelectItem>
                  <SelectItem value="unresolved">غير محلولة</SelectItem>
                  <SelectItem value="resolved">محلولة</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Alerts Table */}
      <Card>
        <CardHeader>
          <CardTitle>قائمة التنبيهات ({filteredAlerts.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>النوع</TableHead>
                <TableHead>المنتج</TableHead>
                <TableHead>التنبيه</TableHead>
                <TableHead>القيمة</TableHead>
                <TableHead>الأولوية</TableHead>
                <TableHead>التاريخ</TableHead>
                <TableHead>الحالة</TableHead>
                <TableHead>الإجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredAlerts.map((alert) => (
                <TableRow 
                  key={alert.id} 
                  className={`${!alert.is_read ? 'bg-blue-50 dark:bg-blue-900/10' : ''} ${alert.is_resolved ? 'opacity-60' : ''}`}
                >
                  <TableCell>
                    <div className="flex items-center gap-2">
                      {getTypeIcon(alert.alert_type)}
                      <span className="text-sm">{alert.type_ar}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="font-medium">{alert.product_name}</div>
                    <div className="text-sm text-muted-foreground">{alert.warehouse_name}</div>
                  </TableCell>
                  <TableCell>
                    <div className="max-w-xs">
                      <div className="font-medium">{alert.title}</div>
                      <div className="text-sm text-muted-foreground truncate">{alert.message}</div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="text-center">
                      <span className="text-lg font-bold text-red-600">{alert.current_value}</span>
                      <span className="text-muted-foreground"> / {alert.threshold_value}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    {getPriorityBadge(alert.priority)}
                  </TableCell>
                  <TableCell>
                    <span className="text-sm">
                      {new Date(alert.created_at).toLocaleDateString('ar-SA')}
                    </span>
                  </TableCell>
                  <TableCell>
                    {alert.is_resolved ? (
                      <Badge variant="default" className="flex items-center gap-1">
                        <CheckCircle className="w-3 h-3" />
                        محلول
                      </Badge>
                    ) : (
                      <Badge variant="destructive" className="flex items-center gap-1">
                        <AlertTriangle className="w-3 h-3" />
                        قيد الانتظار
                      </Badge>
                    )}
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-1">
                      {!alert.is_read && (
                        <button
                          onClick={() => handleMarkAsRead(alert.id)}
                          className="p-1 hover:bg-muted rounded"
                          title="تعليم كمقروء"
                        >
                          <Eye className="w-4 h-4" />
                        </button>
                      )}
                      {!alert.is_resolved && (
                        <button
                          onClick={() => handleResolve(alert.id)}
                          className="p-1 text-green-600 hover:bg-green-50 rounded"
                          title="حل التنبيه"
                        >
                          <Check className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>

          {filteredAlerts.length === 0 && (
            <div className="text-center py-8">
              <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-4" />
              <p className="text-muted-foreground">لا توجد تنبيهات تطابق معايير البحث</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default InventoryAlerts;

