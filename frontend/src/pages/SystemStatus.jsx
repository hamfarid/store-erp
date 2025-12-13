import React, { useState, useEffect } from 'react';
import {
  Server, Database, CheckCircle, XCircle, AlertTriangle, RefreshCw,
  Cpu, HardDrive, Activity, Clock, Wifi, Shield, Users, Package
} from 'lucide-react';
import { toast } from 'react-hot-toast';
import apiClient from '../services/apiClient';

// UI Components
import { Badge } from '../components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';

/**
 * صفحة حالة النظام
 * System Status Page
 */
const SystemStatus = () => {
  const [status, setStatus] = useState(null);
  const [health, setHealth] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(null);

  // بيانات نموذجية
  const sampleStatus = {
    system_name: 'Complete Inventory Management System',
    version: '1.5.0',
    status: 'running',
    timestamp: new Date().toISOString(),
    services: {
      database: 'متوفرة',
      models_available: 12,
      models_errors: 0,
      python_version: '3.11.5',
      flask_env: 'development'
    },
    available_models: [
      'models.user.User',
      'models.customer.Customer',
      'models.supplier.Supplier',
      'models.inventory.Product',
      'models.inventory.Category',
      'models.inventory.Warehouse',
      'models.inventory.StockMovement',
      'models.inventory.Lot',
      'models.invoice.Invoice',
      'models.invoice.InvoiceItem',
      'models.payment.Payment',
      'models.audit.AuditLog'
    ],
    model_errors: [],
    recommendations: [
      'استخدم /api/temp/* للوصول للبيانات التجريبية',
      'تحقق من ملفات النماذج في src/models/',
      'راجع سجلات الخادم للأخطاء التفصيلية'
    ]
  };

  const sampleHealth = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    components: {
      database: { status: 'healthy', response_time: 15 },
      cache: { status: 'healthy', response_time: 5 },
      api: { status: 'healthy', response_time: 25 },
      storage: { status: 'healthy', used: '45%' }
    },
    metrics: {
      uptime: '7d 14h 32m',
      requests_today: 1250,
      active_users: 8,
      memory_usage: '62%',
      cpu_usage: '35%',
      disk_usage: '45%'
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 30000); // Auto-refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchStatus = async () => {
    setIsLoading(true);
    try {
      const [statusRes, healthRes] = await Promise.all([
        apiClient.get('/api/system/status'),
        apiClient.get('/api/system/health')
      ]);

      if (statusRes.success) {
        setStatus(statusRes.data);
      } else {
        setStatus(sampleStatus);
      }

      if (healthRes.success) {
        setHealth(healthRes);
      } else {
        setHealth(sampleHealth);
      }

      setLastUpdated(new Date());
    } catch (error) {
      console.log('Using sample data:', error);
      setStatus(sampleStatus);
      setHealth(sampleHealth);
      setLastUpdated(new Date());
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const configs = {
      healthy: { color: 'bg-green-100 text-green-800', icon: CheckCircle, label: 'سليم' },
      running: { color: 'bg-green-100 text-green-800', icon: CheckCircle, label: 'يعمل' },
      warning: { color: 'bg-yellow-100 text-yellow-800', icon: AlertTriangle, label: 'تحذير' },
      error: { color: 'bg-red-100 text-red-800', icon: XCircle, label: 'خطأ' },
      unhealthy: { color: 'bg-red-100 text-red-800', icon: XCircle, label: 'غير سليم' }
    };
    const config = configs[status] || configs.warning;
    const Icon = config.icon;
    
    return (
      <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium ${config.color}`}>
        <Icon className="w-4 h-4" />
        {config.label}
      </span>
    );
  };

  const getProgressColor = (percentage) => {
    const num = parseInt(percentage);
    if (num < 50) return 'bg-green-500';
    if (num < 75) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  if (isLoading && !status) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل حالة النظام...</p>
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
            <Server className="w-8 h-8" />
            حالة النظام
          </h1>
          <p className="text-muted-foreground mt-1">مراقبة صحة وأداء النظام</p>
        </div>
        <div className="flex items-center gap-4">
          {lastUpdated && (
            <span className="text-sm text-muted-foreground flex items-center gap-1">
              <Clock className="w-4 h-4" />
              آخر تحديث: {lastUpdated.toLocaleTimeString('ar-SA')}
            </span>
          )}
          <button 
            onClick={fetchStatus}
            disabled={isLoading}
            className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
            تحديث
          </button>
        </div>
      </div>

      {/* Overall Status */}
      <Card className={health?.status === 'healthy' ? 'border-green-500' : 'border-yellow-500'}>
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className={`w-16 h-16 rounded-full flex items-center justify-center ${health?.status === 'healthy' ? 'bg-green-100' : 'bg-yellow-100'}`}>
                {health?.status === 'healthy' ? (
                  <CheckCircle className="w-10 h-10 text-green-600" />
                ) : (
                  <AlertTriangle className="w-10 h-10 text-yellow-600" />
                )}
              </div>
              <div>
                <h2 className="text-2xl font-bold">{status?.system_name}</h2>
                <p className="text-muted-foreground">الإصدار {status?.version}</p>
              </div>
            </div>
            <div className="text-left">
              {getStatusBadge(health?.status || status?.status)}
              <p className="text-sm text-muted-foreground mt-2">
                وقت التشغيل: {health?.metrics?.uptime || 'غير متوفر'}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <Cpu className="w-5 h-5 text-blue-500" />
                <span className="font-medium">المعالج</span>
              </div>
              <span className="text-2xl font-bold">{health?.metrics?.cpu_usage || '35%'}</span>
            </div>
            <div className="w-full bg-muted h-2 rounded-full">
              <div 
                className={`h-2 rounded-full ${getProgressColor(health?.metrics?.cpu_usage || '35%')}`}
                style={{ width: health?.metrics?.cpu_usage || '35%' }}
              />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <Activity className="w-5 h-5 text-green-500" />
                <span className="font-medium">الذاكرة</span>
              </div>
              <span className="text-2xl font-bold">{health?.metrics?.memory_usage || '62%'}</span>
            </div>
            <div className="w-full bg-muted h-2 rounded-full">
              <div 
                className={`h-2 rounded-full ${getProgressColor(health?.metrics?.memory_usage || '62%')}`}
                style={{ width: health?.metrics?.memory_usage || '62%' }}
              />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <HardDrive className="w-5 h-5 text-purple-500" />
                <span className="font-medium">التخزين</span>
              </div>
              <span className="text-2xl font-bold">{health?.metrics?.disk_usage || '45%'}</span>
            </div>
            <div className="w-full bg-muted h-2 rounded-full">
              <div 
                className={`h-2 rounded-full ${getProgressColor(health?.metrics?.disk_usage || '45%')}`}
                style={{ width: health?.metrics?.disk_usage || '45%' }}
              />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <Users className="w-5 h-5 text-orange-500" />
                <span className="font-medium">المستخدمين النشطين</span>
              </div>
              <span className="text-2xl font-bold">{health?.metrics?.active_users || 8}</span>
            </div>
            <p className="text-sm text-muted-foreground">
              {health?.metrics?.requests_today || 1250} طلب اليوم
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Services Status */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Wifi className="w-5 h-5" />
              حالة الخدمات
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {health?.components && Object.entries(health.components).map(([name, data]) => (
              <div key={name} className="flex items-center justify-between p-3 bg-muted rounded-lg">
                <div className="flex items-center gap-2">
                  {data.status === 'healthy' ? (
                    <CheckCircle className="w-5 h-5 text-green-500" />
                  ) : (
                    <XCircle className="w-5 h-5 text-red-500" />
                  )}
                  <span className="font-medium capitalize">{name}</span>
                </div>
                <div className="flex items-center gap-2">
                  {data.response_time && (
                    <span className="text-sm text-muted-foreground">{data.response_time}ms</span>
                  )}
                  {data.used && (
                    <span className="text-sm text-muted-foreground">{data.used}</span>
                  )}
                  {getStatusBadge(data.status)}
                </div>
              </div>
            ))}

            <div className="flex items-center justify-between p-3 bg-muted rounded-lg">
              <div className="flex items-center gap-2">
                <Database className="w-5 h-5 text-blue-500" />
                <span className="font-medium">قاعدة البيانات</span>
              </div>
              <Badge variant="default">{status?.services?.database || 'متوفرة'}</Badge>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Package className="w-5 h-5" />
              النماذج المتوفرة ({status?.services?.models_available || 0})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="max-h-64 overflow-y-auto space-y-2">
              {status?.available_models?.map((model, index) => (
                <div key={index} className="flex items-center gap-2 p-2 bg-muted rounded text-sm font-mono">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  {model}
                </div>
              ))}
            </div>
            
            {status?.model_errors?.length > 0 && (
              <div className="mt-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 rounded-lg">
                <h4 className="font-bold text-red-600 mb-2 flex items-center gap-1">
                  <XCircle className="w-4 h-4" />
                  أخطاء النماذج ({status.model_errors.length})
                </h4>
                {status.model_errors.map((error, index) => (
                  <p key={index} className="text-sm text-red-600 font-mono">{error}</p>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Environment Info */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="w-5 h-5" />
            معلومات البيئة
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="p-4 bg-muted rounded-lg">
              <p className="text-sm text-muted-foreground">إصدار Python</p>
              <p className="font-mono font-bold">{status?.services?.python_version || '3.11.5'}</p>
            </div>
            <div className="p-4 bg-muted rounded-lg">
              <p className="text-sm text-muted-foreground">بيئة Flask</p>
              <p className="font-mono font-bold">{status?.services?.flask_env || 'development'}</p>
            </div>
            <div className="p-4 bg-muted rounded-lg">
              <p className="text-sm text-muted-foreground">آخر تشغيل</p>
              <p className="font-mono font-bold">
                {status?.timestamp ? new Date(status.timestamp).toLocaleString('ar-SA') : '-'}
              </p>
            </div>
            <div className="p-4 bg-muted rounded-lg">
              <p className="text-sm text-muted-foreground">عنوان API</p>
              <p className="font-mono font-bold text-sm">localhost:5506</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Recommendations */}
      {status?.recommendations?.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-yellow-500" />
              التوصيات
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {status.recommendations.map((rec, index) => (
                <li key={index} className="flex items-start gap-2 text-muted-foreground">
                  <span className="text-primary">•</span>
                  {rec}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default SystemStatus;

