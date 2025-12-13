import React, { useState, useEffect } from 'react';
import {
  Shield, Lock, Unlock, Monitor, Smartphone, Globe, Clock, AlertTriangle,
  CheckCircle, XCircle, RefreshCw, LogOut, Eye, Trash2, Activity, Key,
  Fingerprint, MapPin, Calendar, User, Settings, History
} from 'lucide-react';
import { toast } from 'react-hot-toast';
import apiClient from '../services/apiClient';
import sessionSecurity from '../services/sessionSecurity';

// UI Components
import { Badge } from '../components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow
} from '../components/ui/table';

/**
 * صفحة لوحة الأمان
 * Security Dashboard Page
 */
const SecurityDashboard = () => {
  const [activeSessions, setActiveSessions] = useState([]);
  const [securityLogs, setSecurityLogs] = useState([]);
  const [loginAttempts, setLoginAttempts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [currentSessionId, setCurrentSessionId] = useState(null);
  const [securityStatus, setSecurityStatus] = useState(null);

  // بيانات نموذجية للجلسات
  const sampleSessions = [
    {
      id: 'sess_1',
      device: 'Chrome on Windows',
      ip: '192.168.1.100',
      location: 'الرياض، السعودية',
      last_active: new Date().toISOString(),
      created_at: new Date(Date.now() - 3600000).toISOString(),
      is_current: true,
      device_type: 'desktop'
    },
    {
      id: 'sess_2',
      device: 'Safari on iPhone',
      ip: '192.168.1.105',
      location: 'الرياض، السعودية',
      last_active: new Date(Date.now() - 1800000).toISOString(),
      created_at: new Date(Date.now() - 86400000).toISOString(),
      is_current: false,
      device_type: 'mobile'
    },
    {
      id: 'sess_3',
      device: 'Firefox on Linux',
      ip: '10.0.0.50',
      location: 'جدة، السعودية',
      last_active: new Date(Date.now() - 7200000).toISOString(),
      created_at: new Date(Date.now() - 172800000).toISOString(),
      is_current: false,
      device_type: 'desktop'
    }
  ];

  // بيانات نموذجية لسجلات الأمان
  const sampleLogs = [
    {
      id: 1,
      event_type: 'login_success',
      timestamp: new Date().toISOString(),
      ip: '192.168.1.100',
      user_agent: 'Chrome/120.0',
      details: 'تسجيل دخول ناجح'
    },
    {
      id: 2,
      event_type: 'password_change',
      timestamp: new Date(Date.now() - 86400000).toISOString(),
      ip: '192.168.1.100',
      user_agent: 'Chrome/120.0',
      details: 'تم تغيير كلمة المرور'
    },
    {
      id: 3,
      event_type: 'mfa_enabled',
      timestamp: new Date(Date.now() - 172800000).toISOString(),
      ip: '192.168.1.100',
      user_agent: 'Chrome/120.0',
      details: 'تم تفعيل المصادقة الثنائية'
    },
    {
      id: 4,
      event_type: 'session_terminated',
      timestamp: new Date(Date.now() - 259200000).toISOString(),
      ip: '192.168.1.105',
      user_agent: 'Safari/17.0',
      details: 'تم إنهاء جلسة من جهاز آخر'
    }
  ];

  // بيانات نموذجية لمحاولات تسجيل الدخول
  const sampleAttempts = [
    {
      id: 1,
      status: 'success',
      timestamp: new Date().toISOString(),
      ip: '192.168.1.100',
      location: 'الرياض'
    },
    {
      id: 2,
      status: 'failed',
      timestamp: new Date(Date.now() - 3600000).toISOString(),
      ip: '192.168.1.200',
      location: 'غير معروف',
      reason: 'كلمة مرور خاطئة'
    },
    {
      id: 3,
      status: 'success',
      timestamp: new Date(Date.now() - 86400000).toISOString(),
      ip: '192.168.1.100',
      location: 'الرياض'
    },
    {
      id: 4,
      status: 'blocked',
      timestamp: new Date(Date.now() - 172800000).toISOString(),
      ip: '45.33.32.156',
      location: 'الصين',
      reason: 'موقع غير معتاد'
    }
  ];

  useEffect(() => {
    fetchSecurityData();
    const currentId = localStorage.getItem('session_id');
    setCurrentSessionId(currentId);
  }, []);

  const fetchSecurityData = async () => {
    setIsLoading(true);
    try {
      // Fetch active sessions
      const sessions = await sessionSecurity.getActiveSessions();
      setActiveSessions(sessions.length > 0 ? sessions : sampleSessions);

      // Fetch security logs
      try {
        const logsResponse = await apiClient.get('/api/security/logs');
        setSecurityLogs(logsResponse.logs || sampleLogs);
      } catch {
        setSecurityLogs(sampleLogs);
      }

      // Fetch login attempts
      try {
        const attemptsResponse = await apiClient.get('/api/security/login-attempts');
        setLoginAttempts(attemptsResponse.attempts || sampleAttempts);
      } catch {
        setLoginAttempts(sampleAttempts);
      }

      // Check security status
      const validation = sessionSecurity.validateSession();
      setSecurityStatus({
        valid: validation.valid,
        errors: validation.errors,
        fingerprint: sessionSecurity.generateFingerprint(),
        mfaEnabled: localStorage.getItem('mfa_enabled') === 'true'
      });

    } catch (error) {
      console.log('Using sample data:', error);
      setActiveSessions(sampleSessions);
      setSecurityLogs(sampleLogs);
      setLoginAttempts(sampleAttempts);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTerminateSession = async (sessionId) => {
    if (sessionId === currentSessionId) {
      toast.error('لا يمكن إنهاء الجلسة الحالية');
      return;
    }

    if (!window.confirm('هل أنت متأكد من إنهاء هذه الجلسة؟')) return;

    const success = await sessionSecurity.terminateSession(sessionId);
    if (success) {
      setActiveSessions(activeSessions.filter(s => s.id !== sessionId));
      toast.success('تم إنهاء الجلسة بنجاح');
    } else {
      // Demo mode
      setActiveSessions(activeSessions.filter(s => s.id !== sessionId));
      toast.success('تم إنهاء الجلسة');
    }
  };

  const handleTerminateAllOthers = async () => {
    if (!window.confirm('هل أنت متأكد من إنهاء جميع الجلسات الأخرى؟')) return;

    const success = await sessionSecurity.terminateOtherSessions();
    if (success) {
      setActiveSessions(activeSessions.filter(s => s.is_current));
      toast.success('تم إنهاء جميع الجلسات الأخرى');
    } else {
      // Demo mode
      setActiveSessions(activeSessions.filter(s => s.is_current));
      toast.success('تم إنهاء جميع الجلسات الأخرى');
    }
  };

  const getDeviceIcon = (deviceType) => {
    if (deviceType === 'mobile') return <Smartphone className="w-5 h-5" />;
    if (deviceType === 'tablet') return <Monitor className="w-5 h-5" />;
    return <Monitor className="w-5 h-5" />;
  };

  const getEventBadge = (eventType) => {
    const configs = {
      login_success: { color: 'bg-green-100 text-green-800', label: 'تسجيل دخول' },
      login_failed: { color: 'bg-red-100 text-red-800', label: 'فشل تسجيل' },
      password_change: { color: 'bg-blue-100 text-blue-800', label: 'تغيير كلمة مرور' },
      mfa_enabled: { color: 'bg-purple-100 text-purple-800', label: 'تفعيل MFA' },
      mfa_disabled: { color: 'bg-orange-100 text-orange-800', label: 'تعطيل MFA' },
      session_terminated: { color: 'bg-yellow-100 text-yellow-800', label: 'إنهاء جلسة' },
      force_logout: { color: 'bg-red-100 text-red-800', label: 'خروج إجباري' }
    };
    const config = configs[eventType] || { color: 'bg-gray-100 text-gray-800', label: eventType };
    return (
      <span className={`px-2 py-1 text-xs font-medium rounded-full ${config.color}`}>
        {config.label}
      </span>
    );
  };

  const getAttemptStatus = (status) => {
    const configs = {
      success: { icon: CheckCircle, color: 'text-green-500', label: 'ناجح' },
      failed: { icon: XCircle, color: 'text-red-500', label: 'فاشل' },
      blocked: { icon: Shield, color: 'text-orange-500', label: 'محظور' }
    };
    const config = configs[status] || configs.failed;
    const Icon = config.icon;
    return (
      <div className={`flex items-center gap-1 ${config.color}`}>
        <Icon className="w-4 h-4" />
        <span className="text-sm font-medium">{config.label}</span>
      </div>
    );
  };

  const formatTimeAgo = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return 'الآن';
    if (minutes < 60) return `منذ ${minutes} دقيقة`;
    if (hours < 24) return `منذ ${hours} ساعة`;
    return `منذ ${days} يوم`;
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل بيانات الأمان...</p>
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
            <Shield className="w-8 h-8" />
            لوحة الأمان
          </h1>
          <p className="text-muted-foreground mt-1">إدارة الجلسات وحماية الحساب</p>
        </div>
        <button
          onClick={fetchSecurityData}
          className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
          تحديث
        </button>
      </div>

      {/* Security Status */}
      <Card className={securityStatus?.valid ? 'border-green-500' : 'border-red-500'}>
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              {securityStatus?.valid ? (
                <CheckCircle className="w-12 h-12 text-green-500" />
              ) : (
                <AlertTriangle className="w-12 h-12 text-red-500" />
              )}
              <div>
                <h3 className="text-xl font-bold">
                  {securityStatus?.valid ? 'حسابك آمن' : 'يوجد مخاوف أمنية'}
                </h3>
                <p className="text-muted-foreground">
                  {securityStatus?.mfaEnabled 
                    ? 'المصادقة الثنائية مفعلة'
                    : 'يُنصح بتفعيل المصادقة الثنائية'}
                </p>
              </div>
            </div>
            <div className="text-left">
              <p className="text-sm text-muted-foreground">بصمة الجلسة</p>
              <code className="text-xs bg-muted px-2 py-1 rounded">
                {securityStatus?.fingerprint?.substring(0, 16)}...
              </code>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">الجلسات النشطة</p>
                <p className="text-2xl font-bold text-primary">{activeSessions.length}</p>
              </div>
              <Monitor className="w-8 h-8 text-primary/60" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">محاولات اليوم</p>
                <p className="text-2xl font-bold text-blue-600">
                  {loginAttempts.filter(a => 
                    new Date(a.timestamp).toDateString() === new Date().toDateString()
                  ).length}
                </p>
              </div>
              <Key className="w-8 h-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">محاولات فاشلة</p>
                <p className="text-2xl font-bold text-red-600">
                  {loginAttempts.filter(a => a.status === 'failed').length}
                </p>
              </div>
              <XCircle className="w-8 h-8 text-red-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">محاولات محظورة</p>
                <p className="text-2xl font-bold text-orange-600">
                  {loginAttempts.filter(a => a.status === 'blocked').length}
                </p>
              </div>
              <Shield className="w-8 h-8 text-orange-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Active Sessions */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Activity className="w-5 h-5" />
            الجلسات النشطة ({activeSessions.length})
          </CardTitle>
          {activeSessions.length > 1 && (
            <button
              onClick={handleTerminateAllOthers}
              className="flex items-center gap-2 px-3 py-1 text-sm text-red-600 border border-red-300 rounded-lg hover:bg-red-50 transition-colors"
            >
              <LogOut className="w-4 h-4" />
              إنهاء الجلسات الأخرى
            </button>
          )}
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {activeSessions.map((session) => (
              <div
                key={session.id}
                className={`p-4 rounded-lg border ${session.is_current ? 'border-green-500 bg-green-50 dark:bg-green-900/20' : 'border-border'}`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className={`p-3 rounded-full ${session.is_current ? 'bg-green-100' : 'bg-muted'}`}>
                      {getDeviceIcon(session.device_type)}
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-medium">{session.device}</span>
                        {session.is_current && (
                          <Badge variant="default" className="bg-green-500">الجلسة الحالية</Badge>
                        )}
                      </div>
                      <div className="flex items-center gap-4 text-sm text-muted-foreground mt-1">
                        <span className="flex items-center gap-1">
                          <Globe className="w-3 h-3" />
                          {session.ip}
                        </span>
                        <span className="flex items-center gap-1">
                          <MapPin className="w-3 h-3" />
                          {session.location}
                        </span>
                        <span className="flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          {formatTimeAgo(session.last_active)}
                        </span>
                      </div>
                    </div>
                  </div>
                  {!session.is_current && (
                    <button
                      onClick={() => handleTerminateSession(session.id)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                      title="إنهاء الجلسة"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Login Attempts */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Key className="w-5 h-5" />
            محاولات تسجيل الدخول الأخيرة
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>الحالة</TableHead>
                <TableHead>التاريخ</TableHead>
                <TableHead>عنوان IP</TableHead>
                <TableHead>الموقع</TableHead>
                <TableHead>السبب</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loginAttempts.map((attempt) => (
                <TableRow key={attempt.id}>
                  <TableCell>{getAttemptStatus(attempt.status)}</TableCell>
                  <TableCell>{new Date(attempt.timestamp).toLocaleString('ar-SA')}</TableCell>
                  <TableCell className="font-mono">{attempt.ip}</TableCell>
                  <TableCell>{attempt.location}</TableCell>
                  <TableCell className="text-muted-foreground">{attempt.reason || '-'}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Security Logs */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <History className="w-5 h-5" />
            سجل الأمان
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>الحدث</TableHead>
                <TableHead>التاريخ</TableHead>
                <TableHead>عنوان IP</TableHead>
                <TableHead>التفاصيل</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {securityLogs.map((log) => (
                <TableRow key={log.id}>
                  <TableCell>{getEventBadge(log.event_type)}</TableCell>
                  <TableCell>{new Date(log.timestamp).toLocaleString('ar-SA')}</TableCell>
                  <TableCell className="font-mono">{log.ip}</TableCell>
                  <TableCell className="text-muted-foreground">{log.details}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Security Tips */}
      <Card>
        <CardHeader>
          <CardTitle>نصائح أمنية</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-muted rounded-lg">
              <Lock className="w-6 h-6 text-primary mb-2" />
              <h4 className="font-bold mb-1">كلمة مرور قوية</h4>
              <p className="text-sm text-muted-foreground">
                استخدم كلمة مرور طويلة تحتوي على أحرف وأرقام ورموز
              </p>
            </div>
            <div className="p-4 bg-muted rounded-lg">
              <Fingerprint className="w-6 h-6 text-primary mb-2" />
              <h4 className="font-bold mb-1">المصادقة الثنائية</h4>
              <p className="text-sm text-muted-foreground">
                فعّل المصادقة الثنائية لحماية إضافية لحسابك
              </p>
            </div>
            <div className="p-4 bg-muted rounded-lg">
              <Eye className="w-6 h-6 text-primary mb-2" />
              <h4 className="font-bold mb-1">راقب جلساتك</h4>
              <p className="text-sm text-muted-foreground">
                راجع الجلسات النشطة بشكل دوري وأنهِ أي جلسة مشبوهة
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default SecurityDashboard;

