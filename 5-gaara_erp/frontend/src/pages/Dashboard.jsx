/**
 * Modern Dashboard - Store Management System
 * 
 * A beautiful, professional dashboard with modern UI/UX.
 */

import React, { useState, useEffect } from 'react';
import {
  TrendingUp,
  TrendingDown,
  Package,
  ShoppingCart,
  Users,
  DollarSign,
  AlertTriangle,
  ArrowUpRight,
  ArrowDownRight,
  Calendar,
  BarChart3,
  PieChart,
  Activity,
  Bell,
  Search,
  Filter,
  MoreVertical,
  RefreshCw,
  Download,
  ChevronLeft,
  ChevronRight,
  Box,
  Truck,
  CreditCard,
  Target
} from 'lucide-react';
import '../styles/theme.css';

// ============================================================================
// Stat Card Component
// ============================================================================

const StatCard = ({ title, value, change, changeType, icon: Icon, color, delay }) => {
  const isPositive = changeType === 'up';
  
  const colorClasses = {
    teal: 'from-teal-500 to-teal-600',
    amber: 'from-amber-500 to-amber-600',
    blue: 'from-blue-500 to-blue-600',
    purple: 'from-purple-500 to-purple-600',
    rose: 'from-rose-500 to-rose-600',
    emerald: 'from-emerald-500 to-emerald-600',
  };

  return (
    <div 
      className={`animate-fade-in-up stagger-${delay}`}
      style={{ opacity: 0, animationFillMode: 'forwards' }}
      data-testid="metric-card"
    >
      <div className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 border border-gray-100 relative overflow-hidden group">
        {/* Background decoration */}
        <div className={`absolute -top-4 -left-4 w-24 h-24 bg-gradient-to-br ${colorClasses[color]} opacity-10 rounded-full blur-2xl group-hover:opacity-20 transition-opacity`} />
        
        <div className="flex items-start justify-between relative z-10">
          <div>
            <p className="text-gray-500 text-sm font-medium mb-1">{title}</p>
            <h3 className="text-3xl font-bold text-gray-900 mb-2">{value}</h3>
            <div className={`inline-flex items-center gap-1 text-sm font-semibold px-2 py-1 rounded-full ${
              isPositive ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-600'
            }`}>
              {isPositive ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
              <span>{change}%</span>
              <span className="text-gray-400 font-normal mr-1">من الشهر الماضي</span>
            </div>
          </div>
          <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${colorClasses[color]} flex items-center justify-center shadow-lg`}>
            <Icon className="text-white" size={24} />
          </div>
        </div>
      </div>
    </div>
  );
};

// ============================================================================
// Quick Action Button
// ============================================================================

const QuickAction = ({ icon: Icon, label, onClick, color }) => (
  <button 
    onClick={onClick}
    className="flex flex-col items-center gap-2 p-4 rounded-xl bg-white border border-gray-100 hover:border-teal-200 hover:shadow-md transition-all duration-300 group"
  >
    <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${color} flex items-center justify-center shadow-md group-hover:scale-110 transition-transform`}>
      <Icon className="text-white" size={20} />
    </div>
    <span className="text-sm font-medium text-gray-700">{label}</span>
  </button>
);

// ============================================================================
// Activity Item
// ============================================================================

const ActivityItem = ({ type, title, description, time, amount }) => {
  const typeConfig = {
    sale: { icon: ShoppingCart, color: 'bg-emerald-500', label: 'بيع' },
    purchase: { icon: Package, color: 'bg-blue-500', label: 'شراء' },
    return: { icon: RefreshCw, color: 'bg-amber-500', label: 'إرجاع' },
    payment: { icon: CreditCard, color: 'bg-purple-500', label: 'دفعة' },
  };

  const config = typeConfig[type] || typeConfig.sale;
  const Icon = config.icon;

  return (
    <div className="flex items-center gap-4 p-4 hover:bg-gray-50 rounded-xl transition-colors">
      <div className={`w-10 h-10 rounded-xl ${config.color} flex items-center justify-center`}>
        <Icon className="text-white" size={18} />
      </div>
      <div className="flex-1 min-w-0">
        <p className="font-medium text-gray-900 truncate">{title}</p>
        <p className="text-sm text-gray-500 truncate">{description}</p>
      </div>
      <div className="text-left">
        <p className={`font-semibold ${type === 'sale' || type === 'payment' ? 'text-emerald-600' : 'text-gray-900'}`}>
          {amount}
        </p>
        <p className="text-xs text-gray-400">{time}</p>
      </div>
    </div>
  );
};

// ============================================================================
// Alert Item
// ============================================================================

const AlertItem = ({ severity, title, description }) => {
  const severityConfig = {
    critical: { color: 'bg-rose-50 border-rose-200', text: 'text-rose-700', icon: 'bg-rose-500' },
    warning: { color: 'bg-amber-50 border-amber-200', text: 'text-amber-700', icon: 'bg-amber-500' },
    info: { color: 'bg-blue-50 border-blue-200', text: 'text-blue-700', icon: 'bg-blue-500' },
  };

  const config = severityConfig[severity] || severityConfig.info;

  return (
    <div className={`flex items-center gap-3 p-4 rounded-xl border ${config.color}`}>
      <div className={`w-2 h-10 rounded-full ${config.icon}`} />
      <div className="flex-1">
        <p className={`font-medium ${config.text}`}>{title}</p>
        <p className="text-sm text-gray-600">{description}</p>
      </div>
    </div>
  );
};

// ============================================================================
// Top Product Item
// ============================================================================

const TopProductItem = ({ rank, name, sales, revenue, trend }) => (
  <div className="flex items-center gap-4 p-4 hover:bg-gray-50 rounded-xl transition-colors">
    <div className={`w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm ${
      rank === 1 ? 'bg-amber-100 text-amber-700' :
      rank === 2 ? 'bg-gray-100 text-gray-600' :
      rank === 3 ? 'bg-orange-100 text-orange-700' :
      'bg-gray-50 text-gray-500'
    }`}>
      {rank}
    </div>
    <div className="flex-1 min-w-0">
      <p className="font-medium text-gray-900 truncate">{name}</p>
      <p className="text-sm text-gray-500">{sales} مبيعات</p>
    </div>
    <div className="text-left">
      <p className="font-semibold text-gray-900">{revenue}</p>
      <div className={`text-xs flex items-center gap-1 ${trend > 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
        {trend > 0 ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
        {Math.abs(trend)}%
      </div>
    </div>
  </div>
);

// ============================================================================
// Main Dashboard Component
// ============================================================================

const Dashboard = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [currentDate] = useState(new Date()); // setCurrentDate unused

  useEffect(() => {
    const timer = setTimeout(() => setIsLoading(false), 500);
    return () => clearTimeout(timer);
  }, []);

  // Sample data
  const stats = [
    { title: 'إجمالي المبيعات', value: '125,430 ر.س', change: 12.5, changeType: 'up', icon: DollarSign, color: 'teal' },
    { title: 'الطلبات', value: '1,284', change: 8.2, changeType: 'up', icon: ShoppingCart, color: 'blue' },
    { title: 'المنتجات', value: '3,456', change: 3.1, changeType: 'down', icon: Package, color: 'purple' },
    { title: 'العملاء', value: '892', change: 15.3, changeType: 'up', icon: Users, color: 'amber' },
  ];

  const quickActions = [
    { icon: ShoppingCart, label: 'فاتورة جديدة', color: 'from-teal-500 to-teal-600' },
    { icon: Package, label: 'إضافة منتج', color: 'from-blue-500 to-blue-600' },
    { icon: Users, label: 'عميل جديد', color: 'from-purple-500 to-purple-600' },
    { icon: Truck, label: 'طلب شراء', color: 'from-amber-500 to-amber-600' },
    { icon: BarChart3, label: 'التقارير', color: 'from-rose-500 to-rose-600' },
    { icon: Download, label: 'تصدير البيانات', color: 'from-emerald-500 to-emerald-600' },
  ];

  const recentActivities = [
    { type: 'sale', title: 'فاتورة مبيعات #1234', description: 'أحمد محمد - 5 منتجات', time: 'منذ 5 دقائق', amount: '+2,450 ر.س' },
    { type: 'purchase', title: 'طلب شراء #567', description: 'مورد الإلكترونيات', time: 'منذ 15 دقيقة', amount: '-12,000 ر.س' },
    { type: 'payment', title: 'دفعة من عميل', description: 'شركة الفيصل التجارية', time: 'منذ 30 دقيقة', amount: '+5,000 ر.س' },
    { type: 'return', title: 'إرجاع منتج', description: 'هاتف سامسونج - عيب مصنعي', time: 'منذ ساعة', amount: '-1,200 ر.س' },
    { type: 'sale', title: 'فاتورة مبيعات #1233', description: 'محمد علي - 3 منتجات', time: 'منذ ساعتين', amount: '+890 ر.س' },
  ];

  const alerts = [
    { severity: 'critical', title: '5 منتجات نفدت من المخزون', description: 'يرجى إعادة الطلب فوراً' },
    { severity: 'warning', title: '12 منتج قارب على النفاد', description: 'المخزون أقل من الحد الأدنى' },
    { severity: 'info', title: '3 طلبات شراء بانتظار الموافقة', description: 'منذ يومين' },
  ];

  const topProducts = [
    { rank: 1, name: 'آيفون 15 برو ماكس', sales: 234, revenue: '468,000 ر.س', trend: 23 },
    { rank: 2, name: 'سماعات إيربودز برو', sales: 189, revenue: '94,500 ر.س', trend: 15 },
    { rank: 3, name: 'شاحن لاسلكي MagSafe', sales: 156, revenue: '31,200 ر.س', trend: -5 },
    { rank: 4, name: 'حافظة آيفون جلد', sales: 142, revenue: '28,400 ر.س', trend: 8 },
    { rank: 5, name: 'كابل USB-C', sales: 128, revenue: '6,400 ر.س', trend: 12 },
  ];

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-teal-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-600 font-medium">جاري التحميل...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100" dir="rtl">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-lg border-b border-gray-200 sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">لوحة التحكم</h1>
              <p className="text-gray-500 text-sm">
                {currentDate.toLocaleDateString('ar-SA', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
              </p>
            </div>
            
            <div className="flex items-center gap-4">
              {/* Search */}
              <div className="relative">
                <Search className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
                <input
                  type="text"
                  placeholder="بحث..."
                  className="w-64 pr-10 pl-4 py-2.5 bg-gray-100 border-0 rounded-xl focus:ring-2 focus:ring-teal-500 focus:bg-white transition-all"
                />
              </div>
              
              {/* Notifications */}
              <button className="relative p-2.5 bg-gray-100 rounded-xl hover:bg-gray-200 transition-colors">
                <Bell size={20} className="text-gray-600" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-rose-500 rounded-full" />
              </button>
              
              {/* Profile */}
              <div className="flex items-center gap-3 pr-3 border-r border-gray-200">
                <div className="text-left">
                  <p className="font-medium text-gray-900">أحمد محمد</p>
                  <p className="text-xs text-gray-500">مدير النظام</p>
                </div>
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-teal-500 to-teal-600 flex items-center justify-center text-white font-bold">
                  أ
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <StatCard key={index} {...stat} delay={index + 1} />
          ))}
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 mb-8 animate-fade-in-up" style={{ animationDelay: '0.5s', opacity: 0, animationFillMode: 'forwards' }}>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-gray-900">إجراءات سريعة</h2>
            <button className="text-teal-600 text-sm font-medium hover:text-teal-700">
              عرض الكل
            </button>
          </div>
          <div className="grid grid-cols-3 md:grid-cols-6 gap-4">
            {quickActions.map((action, index) => (
              <QuickAction key={index} {...action} />
            ))}
          </div>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Recent Activity */}
          <div className="lg:col-span-2 bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden animate-fade-in-up" style={{ animationDelay: '0.6s', opacity: 0, animationFillMode: 'forwards' }}>
            <div className="p-6 border-b border-gray-100">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-bold text-gray-900">النشاط الأخير</h2>
                <div className="flex items-center gap-2">
                  <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                    <Filter size={18} className="text-gray-500" />
                  </button>
                  <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                    <MoreVertical size={18} className="text-gray-500" />
                  </button>
                </div>
              </div>
            </div>
            <div className="divide-y divide-gray-50">
              {recentActivities.map((activity, index) => (
                <ActivityItem key={index} {...activity} />
              ))}
            </div>
            <div className="p-4 bg-gray-50 text-center">
              <button className="text-teal-600 font-medium hover:text-teal-700 transition-colors">
                عرض جميع الأنشطة
              </button>
            </div>
          </div>

          {/* Alerts */}
          <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden animate-fade-in-up" style={{ animationDelay: '0.7s', opacity: 0, animationFillMode: 'forwards' }}>
            <div className="p-6 border-b border-gray-100">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-bold text-gray-900">التنبيهات</h2>
                <span className="bg-rose-100 text-rose-600 text-xs font-semibold px-2.5 py-1 rounded-full">
                  {alerts.length} جديد
                </span>
              </div>
            </div>
            <div className="p-4 space-y-3">
              {alerts.map((alert, index) => (
                <AlertItem key={index} {...alert} />
              ))}
            </div>
            <div className="p-4 bg-gray-50 text-center">
              <button className="text-teal-600 font-medium hover:text-teal-700 transition-colors">
                عرض جميع التنبيهات
              </button>
            </div>
          </div>
        </div>

        {/* Top Products */}
        <div className="mt-8 bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden animate-fade-in-up" style={{ animationDelay: '0.8s', opacity: 0, animationFillMode: 'forwards' }}>
          <div className="p-6 border-b border-gray-100">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-bold text-gray-900">المنتجات الأكثر مبيعاً</h2>
              <div className="flex items-center gap-2">
                <select className="bg-gray-100 border-0 rounded-lg px-3 py-2 text-sm font-medium text-gray-700">
                  <option>هذا الأسبوع</option>
                  <option>هذا الشهر</option>
                  <option>هذا العام</option>
                </select>
              </div>
            </div>
          </div>
          <div className="divide-y divide-gray-50">
            {topProducts.map((product, index) => (
              <TopProductItem key={index} {...product} />
            ))}
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
          {/* Sales Chart */}
          <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 animate-fade-in-up" style={{ animationDelay: '0.9s', opacity: 0, animationFillMode: 'forwards' }}>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-bold text-gray-900">المبيعات</h2>
              <div className="flex items-center gap-2">
                <button className="px-3 py-1.5 bg-teal-100 text-teal-700 rounded-lg text-sm font-medium">
                  يومي
                </button>
                <button className="px-3 py-1.5 text-gray-500 hover:bg-gray-100 rounded-lg text-sm font-medium">
                  أسبوعي
                </button>
                <button className="px-3 py-1.5 text-gray-500 hover:bg-gray-100 rounded-lg text-sm font-medium">
                  شهري
                </button>
              </div>
            </div>
            {/* Chart placeholder */}
            <div className="h-64 bg-gradient-to-br from-teal-50 to-teal-100 rounded-xl flex items-center justify-center">
              <div className="text-center">
                <BarChart3 size={48} className="text-teal-300 mx-auto mb-2" />
                <p className="text-teal-600 font-medium">رسم بياني للمبيعات</p>
              </div>
            </div>
          </div>

          {/* Categories Chart */}
          <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 animate-fade-in-up" style={{ animationDelay: '1s', opacity: 0, animationFillMode: 'forwards' }}>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-bold text-gray-900">المبيعات حسب الفئة</h2>
              <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                <MoreVertical size={18} className="text-gray-500" />
              </button>
            </div>
            {/* Chart placeholder */}
            <div className="h-64 bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl flex items-center justify-center">
              <div className="text-center">
                <PieChart size={48} className="text-purple-300 mx-auto mb-2" />
                <p className="text-purple-600 font-medium">رسم دائري للفئات</p>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <p className="text-gray-500 text-sm">
              © 2025 نظام إدارة المخزون. جميع الحقوق محفوظة.
            </p>
            <div className="flex items-center gap-4">
              <a href="#" className="text-gray-500 hover:text-teal-600 text-sm">الدعم الفني</a>
              <a href="#" className="text-gray-500 hover:text-teal-600 text-sm">الوثائق</a>
              <a href="#" className="text-gray-500 hover:text-teal-600 text-sm">سياسة الخصوصية</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard;

