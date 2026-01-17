import React, { useState, useEffect } from 'react';
import {
  Search, Shield, AlertTriangle, Eye, Calendar, User, Activity, Lock, Unlock, CheckCircle, XCircle, Filter
} from 'lucide-react';

const SecurityMonitoring = () => {
  const [auditLogs, setAuditLogs] = useState([]);
  const [loginAttempts, setLoginAttempts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('audit');
  const [searchTerm, setSearchTerm] = useState('');
  const [actionFilter, setActionFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [dateFilter, setDateFilter] = useState('');

  useEffect(() => {
    loadData();
  }, [activeTab]);

  const loadData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      
      if (activeTab === 'audit') {
        const response = await fetch('http://localhost:5002/api/admin/security/audit-logs', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
          const data = await response.json();
          setAuditLogs(data.data || data.logs || []);
        }
      } else if (activeTab === 'login') {
        const response = await fetch('http://localhost:5002/api/admin/security/login-attempts', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
          const data = await response.json();
          setLoginAttempts(data.data || data.attempts || []);
        }
      }
      
      setLoading(false);
    } catch (error) {
      console.error('Error loading security data:', error);
      setLoading(false);
    }
  };

  const filteredLogs = auditLogs.filter(log => {
    const matchesSearch = (log.action || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (log.user_email || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (log.resource || '').toLowerCase().includes(searchTerm.toLowerCase());
    const matchesAction = !actionFilter || log.action === actionFilter;
    const matchesDate = !dateFilter || log.timestamp?.startsWith(dateFilter);
    return matchesSearch && matchesAction && matchesDate;
  });

  const filteredAttempts = loginAttempts.filter(attempt => {
    const matchesSearch = (attempt.email || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (attempt.ip_address || '').toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = !statusFilter || attempt.success?.toString() === statusFilter;
    const matchesDate = !dateFilter || attempt.timestamp?.startsWith(dateFilter);
    return matchesSearch && matchesStatus && matchesDate;
  });

  const getActionIcon = (action) => {
    const icons = {
      'CREATE': <CheckCircle className="w-5 h-5 text-green-600" />,
      'UPDATE': <Activity className="w-5 h-5 text-blue-600" />,
      'DELETE': <XCircle className="w-5 h-5 text-red-600" />,
      'LOGIN': <Unlock className="w-5 h-5 text-green-600" />,
      'LOGOUT': <Lock className="w-5 h-5 text-gray-600" />,
      'VIEW': <Eye className="w-5 h-5 text-blue-600" />,
    };
    return icons[action] || <Activity className="w-5 h-5 text-gray-600" />;
  };

  const getActionColor = (action) => {
    const colors = {
      'CREATE': 'bg-green-100 text-green-800',
      'UPDATE': 'bg-blue-100 text-blue-800',
      'DELETE': 'bg-red-100 text-red-800',
      'LOGIN': 'bg-green-100 text-green-800',
      'LOGOUT': 'bg-gray-100 text-gray-800',
      'VIEW': 'bg-blue-100 text-blue-800',
    };
    return colors[action] || 'bg-gray-100 text-gray-800';
  };

  const calculateStats = () => {
    if (activeTab === 'audit') {
      return {
        total: auditLogs.length,
        creates: auditLogs.filter(l => l.action === 'CREATE').length,
        updates: auditLogs.filter(l => l.action === 'UPDATE').length,
        deletes: auditLogs.filter(l => l.action === 'DELETE').length,
      };
    } else {
      return {
        total: loginAttempts.length,
        successful: loginAttempts.filter(a => a.success).length,
        failed: loginAttempts.filter(a => !a.success).length,
        blocked: loginAttempts.filter(a => a.blocked).length,
      };
    }
  };

  const stats = calculateStats();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="p-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">مراقبة الأمان</h1>
          <p className="text-gray-600 mt-1">سجلات الأمان والتدقيق</p>
        </div>
        <div className="flex items-center gap-2">
          <Shield className="w-8 h-8 text-blue-600" />
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-md mb-6">
        <div className="flex border-b">
          <button
            onClick={() => setActiveTab('audit')}
            className={`flex-1 px-6 py-4 font-medium transition-colors ${
              activeTab === 'audit'
                ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <Activity className="w-5 h-5 inline ml-2" />
            سجلات التدقيق
          </button>
          <button
            onClick={() => setActiveTab('login')}
            className={`flex-1 px-6 py-4 font-medium transition-colors ${
              activeTab === 'login'
                ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <Lock className="w-5 h-5 inline ml-2" />
            محاولات تسجيل الدخول
          </button>
        </div>
      </div>

      {/* Statistics */}
      {activeTab === 'audit' ? (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white rounded-lg shadow-md p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">إجمالي السجلات</p>
                <p className="text-2xl font-bold text-gray-800">{stats.total}</p>
              </div>
              <Activity className="w-10 h-10 text-blue-500" />
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">عمليات الإضافة</p>
                <p className="text-2xl font-bold text-green-600">{stats.creates}</p>
              </div>
              <CheckCircle className="w-10 h-10 text-green-500" />
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">عمليات التعديل</p>
                <p className="text-2xl font-bold text-blue-600">{stats.updates}</p>
              </div>
              <Activity className="w-10 h-10 text-blue-500" />
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">عمليات الحذف</p>
                <p className="text-2xl font-bold text-red-600">{stats.deletes}</p>
              </div>
              <XCircle className="w-10 h-10 text-red-500" />
            </div>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white rounded-lg shadow-md p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">إجمالي المحاولات</p>
                <p className="text-2xl font-bold text-gray-800">{stats.total}</p>
              </div>
              <Lock className="w-10 h-10 text-gray-500" />
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">محاولات ناجحة</p>
                <p className="text-2xl font-bold text-green-600">{stats.successful}</p>
              </div>
              <Unlock className="w-10 h-10 text-green-500" />
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">محاولات فاشلة</p>
                <p className="text-2xl font-bold text-red-600">{stats.failed}</p>
              </div>
              <XCircle className="w-10 h-10 text-red-500" />
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">محاولات محظورة</p>
                <p className="text-2xl font-bold text-orange-600">{stats.blocked}</p>
              </div>
              <AlertTriangle className="w-10 h-10 text-orange-500" />
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Search className="w-4 h-4 inline ml-1" />
              بحث
            </label>
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder={activeTab === 'audit' ? 'بحث في السجلات...' : 'بحث في المحاولات...'}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {activeTab === 'audit' ? (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">نوع الإجراء</label>
              <select
                value={actionFilter}
                onChange={(e) => setActionFilter(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="">الكل</option>
                <option value="CREATE">إضافة</option>
                <option value="UPDATE">تعديل</option>
                <option value="DELETE">حذف</option>
                <option value="LOGIN">دخول</option>
                <option value="LOGOUT">خروج</option>
                <option value="VIEW">عرض</option>
              </select>
            </div>
          ) : (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">الحالة</label>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="">الكل</option>
                <option value="true">ناجح</option>
                <option value="false">فاشل</option>
              </select>
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">التاريخ</label>
            <input
              type="date"
              value={dateFilter}
              onChange={(e) => setDateFilter(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="flex items-end">
            <button
              onClick={() => {
                setSearchTerm('');
                setActionFilter('');
                setStatusFilter('');
                setDateFilter('');
              }}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center justify-center gap-2"
            >
              <XCircle className="w-4 h-4" />
              إعادة تعيين
            </button>
          </div>
        </div>
      </div>

      {/* Data Table */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="overflow-x-auto">
          {activeTab === 'audit' ? (
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الإجراء</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المورد</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المستخدم</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">التفاصيل</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">التاريخ والوقت</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredLogs.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="px-6 py-8 text-center text-gray-500">
                      <Activity className="w-12 h-12 mx-auto text-gray-400 mb-2" />
                      <p>لا توجد سجلات</p>
                    </td>
                  </tr>
                ) : (
                  filteredLogs.map((log) => (
                    <tr key={log.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center gap-2">
                          {getActionIcon(log.action)}
                          <span className={`px-3 py-1 rounded-full text-xs font-medium ${getActionColor(log.action)}`}>
                            {log.action}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {log.resource || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        <div className="flex items-center gap-2">
                          <User className="w-4 h-4" />
                          {log.user_email || 'غير معروف'}
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600 max-w-xs truncate">
                        {log.details || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <div className="flex items-center gap-2">
                          <Calendar className="w-4 h-4" />
                          {new Date(log.timestamp).toLocaleString('ar-EG')}
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          ) : (
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الحالة</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">البريد الإلكتروني</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">عنوان IP</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المتصفح</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">التاريخ والوقت</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredAttempts.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="px-6 py-8 text-center text-gray-500">
                      <Lock className="w-12 h-12 mx-auto text-gray-400 mb-2" />
                      <p>لا توجد محاولات</p>
                    </td>
                  </tr>
                ) : (
                  filteredAttempts.map((attempt) => (
                    <tr key={attempt.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        {attempt.success ? (
                          <span className="px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 inline-flex items-center">
                            <Unlock className="w-3 h-3 ml-1" />
                            ناجح
                          </span>
                        ) : (
                          <span className="px-3 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800 inline-flex items-center">
                            <XCircle className="w-3 h-3 ml-1" />
                            فاشل
                          </span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {attempt.email}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 font-mono">
                        {attempt.ip_address}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600 max-w-xs truncate">
                        {attempt.user_agent || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <div className="flex items-center gap-2">
                          <Calendar className="w-4 h-4" />
                          {new Date(attempt.timestamp).toLocaleString('ar-EG')}
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
};

export default SecurityMonitoring;
