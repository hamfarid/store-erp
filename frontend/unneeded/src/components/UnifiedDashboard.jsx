import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Package,
  Users,
  Building2,
  TrendingUp,
  AlertTriangle,
  DollarSign,
  ShoppingCart,
  Truck,
  BarChart3,
  Activity
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import { logClick, logRoute } from '../utils/logger';

const UnifiedDashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // دالة التنقل مع التسجيل
  const navigateWithLogging = (path, actionName) => {
    logClick(`dashboard-${actionName}`, actionName, {
      destination: path,
      source: 'dashboard'
    });
    logRoute(path, 'GET', { source: 'dashboard_navigation' });
    navigate(path);
  };

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/api/dashboard/stats', {
        credentials: 'include'
      });
      
      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          setStats(data.stats);
        } else {
          throw new Error(data.message || 'فشل في تحميل الإحصائيات');
        }
      } else {
        throw new Error('خطأ في الاتصال بالخادم');
      }
    } catch (error) {
      setError(error.message);
      
      // بيانات احتياطية للعرض
      setStats({
        products: { total: 0, low_stock: 0, categories: 0 },
        inventory: { total_value: 0, warehouses: 0, movements_today: 0 },
        sales: { invoices_today: 0, total_customers: 0, pending_invoices: 0 },
        purchases: { invoices_today: 0, total_suppliers: 0, pending_invoices: 0 }
      });
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ title, value, icon: Icon, color, subtitle, trend }) => (
    <div className="bg-white rounded-lg shadow-sm border p-6 hover:shadow-md transition-shadow duration-200">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-muted-foreground" dir="rtl">{title}</p>
          <p className="text-2xl font-bold text-foreground mt-1">{value}</p>
          {subtitle && (
            <p className="text-sm text-gray-500 mt-1" dir="rtl">{subtitle}</p>
          )}
          {trend && (
            <div className="flex items-center mt-2">
              <span className={`text-xs px-2 py-1 rounded-full ${
                trend.type === 'up' ? 'bg-primary/20 text-green-800' :
                trend.type === 'down' ? 'bg-destructive/20 text-red-800' :
                'bg-muted text-foreground'
              }`}>
                {trend.type === 'up' ? '↗️' : trend.type === 'down' ? '↘️' : '➡️'} {trend.value}
              </span>
            </div>
          )}
        </div>
        <div className={`p-3 rounded-full ${color} shadow-lg`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
    </div>
  );

  const QuickActionCard = ({ title, description, icon: Icon, color, onClick, badge }) => (
    <div
      className="bg-white rounded-lg shadow-sm border p-6 cursor-pointer hover:shadow-lg hover:scale-105 transition-all duration-200 group"
      onClick={onClick}
    >
      <div className="flex items-center space-x-4 rtl:space-x-reverse">
        <div className={`p-3 rounded-full ${color} group-hover:scale-110 transition-transform duration-200 shadow-md`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        <div className="flex-1">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-foreground group-hover:text-primary-600 transition-colors" dir="rtl">{title}</h3>
            {badge && (
              <span className="bg-primary-100 text-primary-800 text-xs px-2 py-1 rounded-full">
                {badge}
              </span>
            )}
          </div>
          <p className="text-sm text-muted-foreground mt-1" dir="rtl">{description}</p>
        </div>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-muted/50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-muted-foreground" dir="rtl">جاري تحميل لوحة التحكم...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-muted/50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-foreground" dir="rtl">
                لوحة التحكم الموحدة
              </h1>
            </div>
            <div className="flex items-center space-x-4 rtl:space-x-reverse">
              <span className="text-sm text-foreground" dir="rtl">
                مرحباً، {user?.full_name || user?.name}
              </span>
              <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
                <span className="text-white text-sm font-medium">
                  {(user?.full_name || user?.name || 'U').charAt(0)}
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          
          {/* Error Message */}
          {error && (
            <div className="mb-6 bg-accent/10 border border-yellow-200 rounded-lg p-4">
              <div className="flex">
                <AlertTriangle className="w-5 h-5 text-yellow-400" />
                <div className="ml-3 rtl:mr-3 rtl:ml-0">
                  <p className="text-sm text-yellow-700" dir="rtl">
                    تحذير: {error}
                  </p>
                  <p className="text-xs text-accent mt-1" dir="rtl">
                    يتم عرض البيانات الاحتياطية. تحقق من اتصال الخادم.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Statistics Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 mb-6 sm:mb-8">
            <StatCard
              title="إجمالي المنتجات"
              value={stats?.products?.total || 0}
              icon={Package}
              color="bg-gradient-to-r from-blue-500 to-blue-600"
              subtitle={`${stats?.products?.categories || 0} فئة`}
              trend={{ type: 'up', value: '+5%' }}
            />
            <StatCard
              title="العملاء"
              value={stats?.sales?.total_customers || 0}
              icon={Users}
              color="bg-gradient-to-r from-green-500 to-green-600"
              subtitle="عميل نشط"
              trend={{ type: 'up', value: '+12%' }}
            />
            <StatCard
              title="الموردين"
              value={stats?.purchases?.total_suppliers || 0}
              icon={Truck}
              color="bg-gradient-to-r from-purple-500 to-purple-600"
              subtitle="مورد معتمد"
              trend={{ type: 'stable', value: '0%' }}
            />
            <StatCard
              title="المخازن"
              value={stats?.inventory?.warehouses || 0}
              icon={Building2}
              color="bg-gradient-to-r from-orange-500 to-orange-600"
              subtitle="مخزن فعال"
              trend={{ type: 'stable', value: '0%' }}
            />
          </div>

          {/* Additional Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <StatCard
              title="قيمة المخزون"
              value={`${(stats?.inventory?.total_value || 0).toLocaleString()} ج.م`}
              icon={DollarSign}
              color="bg-emerald-500"
              subtitle="إجمالي قيمة المخزون"
            />
            <StatCard
              title="فواتير اليوم"
              value={`${(stats?.sales?.invoices_today || 0) + (stats?.purchases?.invoices_today || 0)}`}
              icon={ShoppingCart}
              color="bg-secondary/100"
              subtitle="مبيعات ومشتريات"
            />
            <StatCard
              title="حركات المخزون"
              value={stats?.inventory?.movements_today || 0}
              icon={Activity}
              color="bg-destructive/100"
              subtitle="حركات اليوم"
            />
          </div>

          {/* Alerts */}
          {stats?.products?.low_stock > 0 && (
            <div className="mb-8 bg-destructive/10 border border-destructive/30 rounded-lg p-4">
              <div className="flex">
                <AlertTriangle className="w-5 h-5 text-red-400" />
                <div className="ml-3 rtl:mr-3 rtl:ml-0">
                  <h3 className="text-sm font-medium text-red-800" dir="rtl">
                    تنبيه: منتجات قليلة المخزون
                  </h3>
                  <p className="text-sm text-destructive mt-1" dir="rtl">
                    يوجد {stats.products.low_stock} منتج بحاجة لإعادة تموين
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Quick Actions */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            <QuickActionCard
              title="إدارة المنتجات"
              description="إضافة وتعديل المنتجات"
              icon={Package}
              color="bg-gradient-to-r from-blue-500 to-blue-600"
              badge={stats?.products?.total || 0}
              onClick={() => navigateWithLogging('/products', 'إدارة المنتجات')}
            />
            <QuickActionCard
              title="إدارة العملاء"
              description="إضافة وإدارة العملاء"
              icon={Users}
              color="bg-gradient-to-r from-green-500 to-green-600"
              badge={stats?.sales?.total_customers || 0}
              onClick={() => navigateWithLogging('/customers', 'إدارة العملاء')}
            />
            <QuickActionCard
              title="إدارة المخزون"
              description="متابعة حركات المخزون"
              icon={TrendingUp}
              color="bg-gradient-to-r from-purple-500 to-purple-600"
              badge="جديد"
              onClick={() => navigateWithLogging('/inventory', 'إدارة المخزون')}
            />
            <QuickActionCard
              title="الفواتير"
              description="إنشاء ومتابعة الفواتير"
              icon={ShoppingCart}
              color="bg-gradient-to-r from-orange-500 to-orange-600"
              badge={((stats?.sales?.invoices_today || 0) + (stats?.purchases?.invoices_today || 0))}
              onClick={() => navigateWithLogging('/invoices', 'الفواتير')}
            />
            <QuickActionCard
              title="التقارير"
              description="تقارير شاملة ومفصلة"
              icon={BarChart3}
              color="bg-gradient-to-r from-secondary/100 to-indigo-600"
              badge="متقدم"
              onClick={() => navigateWithLogging('/reports', 'التقارير')}
            />
            <QuickActionCard
              title="الإعدادات"
              description="إعدادات النظام والشركة"
              icon={Building2}
              color="bg-gradient-to-r from-gray-500 to-gray-600"
              onClick={() => navigateWithLogging('/settings', 'الإعدادات')}
            />
          </div>
        </div>
      </main>
    </div>
  );
};

export default UnifiedDashboard;

