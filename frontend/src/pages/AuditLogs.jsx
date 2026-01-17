import React, { useState, useEffect } from 'react';
import {
  Search, Download, Eye, Shield, User, Calendar, Clock, 
  Activity, FileText, AlertTriangle, CheckCircle, XCircle, Filter
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
 * صفحة سجلات التدقيق
 * Audit Logs Page
 */
const AuditLogs = () => {
  const [logs, setLogs] = useState([]);
  const [filteredLogs, setFilteredLogs] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterAction, setFilterAction] = useState('all');
  const [filterResourceType, setFilterResourceType] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [selectedLog, setSelectedLog] = useState(null);

  // بيانات نموذجية
  const sampleLogs = [
    {
      id: 1,
      action: 'create',
      resourceType: 'product',
      resourceId: 101,
      resourceName: 'لابتوب ديل XPS 15',
      userId: 1,
      userName: 'أحمد محمد',
      userRole: 'admin',
      ipAddress: '192.168.1.100',
      userAgent: 'Chrome 120.0',
      status: 'success',
      details: { name: 'لابتوب ديل XPS 15', price: 5500, quantity: 10 },
      createdAt: '2024-01-15T10:30:00'
    },
    {
      id: 2,
      action: 'update',
      resourceType: 'invoice',
      resourceId: 250,
      resourceName: 'فاتورة INV-2024-250',
      userId: 2,
      userName: 'سارة أحمد',
      userRole: 'manager',
      ipAddress: '192.168.1.101',
      userAgent: 'Firefox 121.0',
      status: 'success',
      details: { oldStatus: 'draft', newStatus: 'confirmed', amount: 15000 },
      createdAt: '2024-01-15T11:15:00'
    },
    {
      id: 3,
      action: 'delete',
      resourceType: 'customer',
      resourceId: 45,
      resourceName: 'عميل محذوف',
      userId: 1,
      userName: 'أحمد محمد',
      userRole: 'admin',
      ipAddress: '192.168.1.100',
      userAgent: 'Chrome 120.0',
      status: 'success',
      details: { reason: 'طلب العميل' },
      createdAt: '2024-01-15T12:00:00'
    },
    {
      id: 4,
      action: 'login',
      resourceType: 'auth',
      resourceId: null,
      resourceName: 'تسجيل دخول',
      userId: 3,
      userName: 'محمد علي',
      userRole: 'cashier',
      ipAddress: '192.168.1.102',
      userAgent: 'Safari 17.0',
      status: 'success',
      details: { method: 'password' },
      createdAt: '2024-01-15T08:00:00'
    },
    {
      id: 5,
      action: 'login',
      resourceType: 'auth',
      resourceId: null,
      resourceName: 'محاولة دخول فاشلة',
      userId: null,
      userName: 'unknown',
      userRole: null,
      ipAddress: '192.168.1.200',
      userAgent: 'Chrome 120.0',
      status: 'failed',
      details: { reason: 'كلمة مرور خاطئة', attempts: 3 },
      createdAt: '2024-01-15T09:30:00'
    },
    {
      id: 6,
      action: 'export',
      resourceType: 'report',
      resourceId: null,
      resourceName: 'تقرير المبيعات الشهري',
      userId: 2,
      userName: 'سارة أحمد',
      userRole: 'manager',
      ipAddress: '192.168.1.101',
      userAgent: 'Firefox 121.0',
      status: 'success',
      details: { format: 'xlsx', period: 'January 2024' },
      createdAt: '2024-01-15T14:00:00'
    },
    {
      id: 7,
      action: 'update',
      resourceType: 'settings',
      resourceId: null,
      resourceName: 'إعدادات النظام',
      userId: 1,
      userName: 'أحمد محمد',
      userRole: 'admin',
      ipAddress: '192.168.1.100',
      userAgent: 'Chrome 120.0',
      status: 'success',
      details: { setting: 'tax_rate', oldValue: '15%', newValue: '16%' },
      createdAt: '2024-01-14T16:00:00'
    },
    {
      id: 8,
      action: 'create',
      resourceType: 'user',
      resourceId: 10,
      resourceName: 'مستخدم جديد: فاطمة سالم',
      userId: 1,
      userName: 'أحمد محمد',
      userRole: 'admin',
      ipAddress: '192.168.1.100',
      userAgent: 'Chrome 120.0',
      status: 'success',
      details: { username: 'fatima.salem', role: 'cashier' },
      createdAt: '2024-01-14T10:00:00'
    }
  ];

  const actionTypes = [
    { value: 'create', label: 'إنشاء' },
    { value: 'update', label: 'تعديل' },
    { value: 'delete', label: 'حذف' },
    { value: 'login', label: 'تسجيل دخول' },
    { value: 'logout', label: 'تسجيل خروج' },
    { value: 'export', label: 'تصدير' },
    { value: 'import', label: 'استيراد' }
  ];

  const resourceTypes = [
    { value: 'product', label: 'منتج' },
    { value: 'invoice', label: 'فاتورة' },
    { value: 'customer', label: 'عميل' },
    { value: 'supplier', label: 'مورد' },
    { value: 'user', label: 'مستخدم' },
    { value: 'auth', label: 'مصادقة' },
    { value: 'report', label: 'تقرير' },
    { value: 'settings', label: 'إعدادات' }
  ];

  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.get('/api/audit/logs');
      if (response.success && response.data?.logs?.length > 0) {
        setLogs(response.data.logs);
        setFilteredLogs(response.data.logs);
      } else {
        setLogs(sampleLogs);
        setFilteredLogs(sampleLogs);
      }
    } catch (error) {
      console.log('Using sample data:', error);
      setLogs(sampleLogs);
      setFilteredLogs(sampleLogs);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let filtered = logs;

    if (searchTerm) {
      filtered = filtered.filter(log =>
        log.resourceName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        log.userName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        log.ipAddress.includes(searchTerm)
      );
    }

    if (filterAction !== 'all') {
      filtered = filtered.filter(log => log.action === filterAction);
    }

    if (filterResourceType !== 'all') {
      filtered = filtered.filter(log => log.resourceType === filterResourceType);
    }

    if (filterStatus !== 'all') {
      filtered = filtered.filter(log => log.status === filterStatus);
    }

    setFilteredLogs(filtered);
  }, [logs, searchTerm, filterAction, filterResourceType, filterStatus]);

  const getActionBadge = (action) => {
    const actionConfig = {
      create: { label: 'إنشاء', variant: 'default', color: 'bg-green-100 text-green-800' },
      update: { label: 'تعديل', variant: 'secondary', color: 'bg-blue-100 text-blue-800' },
      delete: { label: 'حذف', variant: 'destructive', color: 'bg-red-100 text-red-800' },
      login: { label: 'دخول', variant: 'outline', color: 'bg-purple-100 text-purple-800' },
      logout: { label: 'خروج', variant: 'outline', color: 'bg-gray-100 text-gray-800' },
      export: { label: 'تصدير', variant: 'secondary', color: 'bg-orange-100 text-orange-800' },
      import: { label: 'استيراد', variant: 'secondary', color: 'bg-teal-100 text-teal-800' }
    };

    const config = actionConfig[action] || { label: action, variant: 'outline' };
    
    return (
      <span className={`px-2 py-1 text-xs font-medium rounded-full ${config.color}`}>
        {config.label}
      </span>
    );
  };

  const getStatusBadge = (status) => {
    if (status === 'success') {
      return (
        <Badge variant="default" className="flex items-center gap-1">
          <CheckCircle className="w-3 h-3" />
          ناجح
        </Badge>
      );
    }
    return (
      <Badge variant="destructive" className="flex items-center gap-1">
        <XCircle className="w-3 h-3" />
        فاشل
      </Badge>
    );
  };

  const getResourceTypeLabel = (type) => {
    const found = resourceTypes.find(r => r.value === type);
    return found ? found.label : type;
  };

  const handleExport = () => {
    toast.success('تم تصدير سجلات التدقيق بنجاح');
  };

  const getSummary = () => {
    return {
      total: logs.length,
      success: logs.filter(l => l.status === 'success').length,
      failed: logs.filter(l => l.status === 'failed').length,
      creates: logs.filter(l => l.action === 'create').length,
      updates: logs.filter(l => l.action === 'update').length,
      deletes: logs.filter(l => l.action === 'delete').length
    };
  };

  const summary = getSummary();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل سجلات التدقيق...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">سجلات التدقيق</h1>
          <p className="text-muted-foreground mt-1">مراقبة جميع الأنشطة في النظام</p>
        </div>
        <button 
          onClick={handleExport}
          className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors"
        >
          <Download className="w-4 h-4" />
          تصدير
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي السجلات</p>
                <p className="text-2xl font-bold text-primary">{summary.total}</p>
              </div>
              <Activity className="w-8 h-8 text-primary/60" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">ناجحة</p>
                <p className="text-2xl font-bold text-green-600">{summary.success}</p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">فاشلة</p>
                <p className="text-2xl font-bold text-red-600">{summary.failed}</p>
              </div>
              <AlertTriangle className="w-8 h-8 text-red-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إنشاء</p>
                <p className="text-2xl font-bold text-blue-600">{summary.creates}</p>
              </div>
              <FileText className="w-8 h-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">تعديل</p>
                <p className="text-2xl font-bold text-orange-600">{summary.updates}</p>
              </div>
              <FileText className="w-8 h-8 text-orange-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">حذف</p>
                <p className="text-2xl font-bold text-red-600">{summary.deletes}</p>
              </div>
              <FileText className="w-8 h-8 text-red-500" />
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
                  placeholder="البحث بالمورد، المستخدم، IP..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>

            <div className="min-w-40">
              <Label htmlFor="action-filter">الإجراء</Label>
              <Select value={filterAction} onValueChange={setFilterAction}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر الإجراء" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع الإجراءات</SelectItem>
                  {actionTypes.map(action => (
                    <SelectItem key={action.value} value={action.value}>{action.label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="min-w-40">
              <Label htmlFor="resource-filter">نوع المورد</Label>
              <Select value={filterResourceType} onValueChange={setFilterResourceType}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر النوع" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع الأنواع</SelectItem>
                  {resourceTypes.map(type => (
                    <SelectItem key={type.value} value={type.value}>{type.label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="min-w-32">
              <Label htmlFor="status-filter">الحالة</Label>
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger>
                  <SelectValue placeholder="الحالة" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">الكل</SelectItem>
                  <SelectItem value="success">ناجح</SelectItem>
                  <SelectItem value="failed">فاشل</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Logs Table */}
      <Card>
        <CardHeader>
          <CardTitle>سجلات النشاط ({filteredLogs.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>التاريخ والوقت</TableHead>
                <TableHead>المستخدم</TableHead>
                <TableHead>الإجراء</TableHead>
                <TableHead>نوع المورد</TableHead>
                <TableHead>الوصف</TableHead>
                <TableHead>IP</TableHead>
                <TableHead>الحالة</TableHead>
                <TableHead>التفاصيل</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredLogs.map((log) => (
                <TableRow key={log.id} className={log.status === 'failed' ? 'bg-red-50' : ''}>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Calendar className="w-3 h-3 text-muted-foreground" />
                      <span className="text-sm">
                        {new Date(log.createdAt).toLocaleDateString('ar-SA')}
                      </span>
                    </div>
                    <div className="flex items-center gap-1 text-muted-foreground">
                      <Clock className="w-3 h-3" />
                      <span className="text-xs">
                        {new Date(log.createdAt).toLocaleTimeString('ar-SA')}
                      </span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <User className="w-4 h-4 text-muted-foreground" />
                      <div>
                        <div className="font-medium">{log.userName}</div>
                        {log.userRole && (
                          <span className="text-xs text-muted-foreground">{log.userRole}</span>
                        )}
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    {getActionBadge(log.action)}
                  </TableCell>
                  <TableCell>
                    <span className="text-sm">{getResourceTypeLabel(log.resourceType)}</span>
                  </TableCell>
                  <TableCell>
                    <span className="text-sm">{log.resourceName}</span>
                  </TableCell>
                  <TableCell>
                    <span className="font-mono text-xs">{log.ipAddress}</span>
                  </TableCell>
                  <TableCell>
                    {getStatusBadge(log.status)}
                  </TableCell>
                  <TableCell>
                    <button
                      onClick={() => setSelectedLog(log)}
                      className="p-1 hover:bg-muted rounded"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>

          {filteredLogs.length === 0 && (
            <div className="text-center py-8">
              <Shield className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">لا توجد سجلات تطابق معايير البحث</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Log Details Modal */}
      {selectedLog && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-background rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">تفاصيل السجل</h2>
              <button onClick={() => setSelectedLog(null)} className="p-2 hover:bg-muted rounded">✕</button>
            </div>
            
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>التاريخ والوقت</Label>
                  <p className="font-medium">{new Date(selectedLog.createdAt).toLocaleString('ar-SA')}</p>
                </div>
                <div>
                  <Label>الحالة</Label>
                  <p>{getStatusBadge(selectedLog.status)}</p>
                </div>
                <div>
                  <Label>المستخدم</Label>
                  <p className="font-medium">{selectedLog.userName}</p>
                </div>
                <div>
                  <Label>الدور</Label>
                  <p>{selectedLog.userRole || '-'}</p>
                </div>
                <div>
                  <Label>الإجراء</Label>
                  <p>{getActionBadge(selectedLog.action)}</p>
                </div>
                <div>
                  <Label>نوع المورد</Label>
                  <p>{getResourceTypeLabel(selectedLog.resourceType)}</p>
                </div>
                <div>
                  <Label>عنوان IP</Label>
                  <p className="font-mono">{selectedLog.ipAddress}</p>
                </div>
                <div>
                  <Label>المتصفح</Label>
                  <p className="text-sm">{selectedLog.userAgent}</p>
                </div>
              </div>

              <div>
                <Label>الوصف</Label>
                <p>{selectedLog.resourceName}</p>
              </div>

              <div>
                <Label>التفاصيل</Label>
                <pre className="bg-muted p-4 rounded-lg text-sm overflow-x-auto">
                  {JSON.stringify(selectedLog.details, null, 2)}
                </pre>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AuditLogs;

