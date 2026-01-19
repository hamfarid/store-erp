// ملف: /home/ubuntu/gaara_ai_FINAL_INTEGRATED_SYSTEM_20250708_040611/gaara_ai_integrated/frontend/src/pages/Dashboard/DashboardComplete.jsx
// لوحة التحكم الكاملة والمتكاملة لنظام Gaara AI
// الإصدار: 2.0.0
// تم الإنشاء: 2025-01-08
// المطور: Gaara Group & Manus AI

import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line, AreaChart, Area
} from 'recharts';
import {
  Users, Sprout, Activity, TrendingUp, AlertTriangle, CheckCircle,
  Plus, Eye, Edit, Trash2, Search, Filter, Download, RefreshCw,
  Calendar, MapPin, Thermometer, Droplets, Sun, Wind,
  Bell, Settings, HelpCircle, LogOut, Menu, X
} from 'lucide-react';

import { ApiService } from '../../services/ApiService';
import { useAuth } from '../../context/AuthContext';
import LoadingSpinner from '../../components/UI/LoadingSpinner';
import ErrorMessage from '../../components/UI/ErrorMessage';
import StatCard from '../../components/Dashboard/StatCard';
import QuickActions from '../../components/Dashboard/QuickActions';
import RecentActivity from '../../components/Dashboard/RecentActivity';
import WeatherWidget from '../../components/Dashboard/WeatherWidget';

const DashboardComplete = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [selectedPeriod, setSelectedPeriod] = useState('week');
  const [showNotifications, setShowNotifications] = useState(false);

  // استعلام الإحصائيات
  const { data: statistics, isLoading: statsLoading, error: statsError, refetch: refetchStats } = useQuery({
    queryKey: ['dashboard-statistics'],
    queryFn: () => ApiService.get('/statistics/dashboard'),
    refetchInterval: 30000, // تحديث كل 30 ثانية
  });

  // استعلام المزارع الحديثة
  const { data: recentFarms, isLoading: farmsLoading } = useQuery({
    queryKey: ['recent-farms'],
    queryFn: () => ApiService.get('/farms?page=1&per_page=5'),
  });

  // استعلام التشخيصات الحديثة
  const { data: recentDiagnoses, isLoading: diagnosesLoading } = useQuery({
    queryKey: ['recent-diagnoses'],
    queryFn: () => ApiService.get('/diagnosis?page=1&per_page=5'),
  });

  // استعلام تقرير المزارع
  const { data: farmsReport, isLoading: reportLoading } = useQuery({
    queryKey: ['farms-report'],
    queryFn: () => ApiService.get('/reports/farms'),
  });

  // بيانات الرسوم البيانية
  const chartData = farmsReport?.report?.map(farm => ({
    name: farm.farm_name,
    plants: farm.plants_count,
    healthy: farm.healthy_plants,
    sick: farm.sick_plants,
    diagnoses: farm.recent_diagnoses
  })) || [];

  const pieData = [
    { name: 'نباتات صحية', value: statistics?.statistics?.healthy_plants || 0, color: '#10B981' },
    { name: 'نباتات مريضة', value: statistics?.statistics?.sick_plants || 0, color: '#EF4444' },
  ];

  // الإجراءات السريعة
  const quickActions = [
    {
      title: 'إضافة مزرعة جديدة',
      description: 'إنشاء مزرعة جديدة وإدارة النباتات',
      icon: Plus,
      color: 'bg-blue-500',
      action: () => navigate('/farms/create'),
      permission: 'farms_create'
    },
    {
      title: 'تشخيص نبات',
      description: 'تشخيص أمراض النباتات بالذكاء الاصطناعي',
      icon: Activity,
      color: 'bg-green-500',
      action: () => navigate('/diagnosis/create'),
      permission: 'diagnosis_create'
    },
    {
      title: 'عرض التقارير',
      description: 'مراجعة التقارير والإحصائيات التفصيلية',
      icon: BarChart,
      color: 'bg-purple-500',
      action: () => navigate('/reports'),
      permission: 'reports_read'
    },
    {
      title: 'إدارة المستخدمين',
      description: 'إضافة وإدارة المستخدمين والصلاحيات',
      icon: Users,
      color: 'bg-orange-500',
      action: () => navigate('/admin/users'),
      permission: 'admin_users_read'
    }
  ];

  // الأنشطة الحديثة
  const recentActivities = [
    ...(recentDiagnoses?.diagnoses?.map(diagnosis => ({
      id: diagnosis.id,
      type: 'diagnosis',
      title: `تشخيص جديد للنبات ${diagnosis.plant_name}`,
      description: `تم تشخيص ${diagnosis.predicted_disease || 'مرض غير محدد'}`,
      time: diagnosis.created_at,
      icon: Activity,
      color: 'text-green-600',
      action: () => navigate(`/diagnosis/${diagnosis.id}`)
    })) || []),
    ...(recentFarms?.farms?.map(farm => ({
      id: farm.id,
      type: 'farm',
      title: `مزرعة جديدة: ${farm.name}`,
      description: `تم إنشاء مزرعة في ${farm.location}`,
      time: farm.created_at,
      icon: Sprout,
      color: 'text-blue-600',
      action: () => navigate(`/farms/${farm.id}`)
    })) || [])
  ].sort((a, b) => new Date(b.time) - new Date(a.time)).slice(0, 10);

  // معالجة تسجيل الخروج
  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // معالجة تحديث البيانات
  const handleRefresh = () => {
    refetchStats();
  };

  if (statsLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="large" />
      </div>
    );
  }

  if (statsError) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <ErrorMessage 
          message="حدث خطأ في تحميل البيانات" 
          onRetry={handleRefresh}
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 rtl">
      {/* شريط التنقل العلوي */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* الشعار والعنوان */}
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Sprout className="h-8 w-8 text-green-600" />
              </div>
              <div className="mr-4">
                <h1 className="text-xl font-semibold text-gray-900">
                  نظام Gaara AI
                </h1>
                <p className="text-sm text-gray-500">لوحة التحكم</p>
              </div>
            </div>

            {/* أدوات التنقل */}
            <div className="flex items-center space-x-4 space-x-reverse">
              {/* زر التحديث */}
              <button
                onClick={handleRefresh}
                className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                title="تحديث البيانات"
              >
                <RefreshCw className="h-5 w-5" />
              </button>

              {/* الإشعارات */}
              <div className="relative">
                <button
                  onClick={() => setShowNotifications(!showNotifications)}
                  className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors relative"
                  title="الإشعارات"
                >
                  <Bell className="h-5 w-5" />
                  <span className="absolute top-1 right-1 h-2 w-2 bg-red-500 rounded-full"></span>
                </button>
              </div>

              {/* الإعدادات */}
              <Link
                to="/settings"
                className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                title="الإعدادات"
              >
                <Settings className="h-5 w-5" />
              </Link>

              {/* الملف الشخصي */}
              <div className="flex items-center space-x-3 space-x-reverse">
                <div className="text-right">
                  <p className="text-sm font-medium text-gray-900">
                    {user?.first_name} {user?.last_name}
                  </p>
                  <p className="text-xs text-gray-500">{user?.role}</p>
                </div>
                <div className="h-8 w-8 bg-green-600 rounded-full flex items-center justify-center">
                  <span className="text-white text-sm font-medium">
                    {user?.first_name?.charAt(0)}
                  </span>
                </div>
              </div>

              {/* تسجيل الخروج */}
              <button
                onClick={handleLogout}
                className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                title="تسجيل الخروج"
              >
                <LogOut className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* المحتوى الرئيسي */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* الترحيب */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            مرحباً، {user?.first_name}! 👋
          </h2>
          <p className="text-gray-600">
            إليك نظرة عامة على مزارعك ونباتاتك اليوم
          </p>
        </div>

        {/* بطاقات الإحصائيات */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="إجمالي المزارع"
            value={statistics?.statistics?.my_farms || statistics?.statistics?.total_farms || 0}
            icon={Sprout}
            color="text-green-600"
            bgColor="bg-green-50"
            change="+12%"
            changeType="positive"
            onClick={() => navigate('/farms')}
          />
          <StatCard
            title="إجمالي النباتات"
            value={statistics?.statistics?.my_plants || statistics?.statistics?.total_plants || 0}
            icon={Activity}
            color="text-blue-600"
            bgColor="bg-blue-50"
            change="+8%"
            changeType="positive"
            onClick={() => navigate('/plants')}
          />
          <StatCard
            title="التشخيصات"
            value={statistics?.statistics?.my_diagnoses || statistics?.statistics?.total_diagnoses || 0}
            icon={TrendingUp}
            color="text-purple-600"
            bgColor="bg-purple-50"
            change="+15%"
            changeType="positive"
            onClick={() => navigate('/diagnosis')}
          />
          <StatCard
            title="النباتات الصحية"
            value={statistics?.statistics?.healthy_plants || 0}
            icon={CheckCircle}
            color="text-emerald-600"
            bgColor="bg-emerald-50"
            change="+5%"
            changeType="positive"
            onClick={() => navigate('/plants?status=healthy')}
          />
        </div>

        {/* الشبكة الرئيسية */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* العمود الأيسر */}
          <div className="lg:col-span-2 space-y-8">
            {/* الرسم البياني الرئيسي */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-900">
                  إحصائيات المزارع
                </h3>
                <div className="flex items-center space-x-2 space-x-reverse">
                  <select
                    value={selectedPeriod}
                    onChange={(e) => setSelectedPeriod(e.target.value)}
                    className="text-sm border border-gray-300 rounded-md px-3 py-1 focus:outline-none focus:ring-2 focus:ring-green-500"
                  >
                    <option value="week">هذا الأسبوع</option>
                    <option value="month">هذا الشهر</option>
                    <option value="year">هذا العام</option>
                  </select>
                </div>
              </div>
              
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="healthy" fill="#10B981" name="نباتات صحية" />
                    <Bar dataKey="sick" fill="#EF4444" name="نباتات مريضة" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* الإجراءات السريعة */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-6">
                الإجراءات السريعة
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {quickActions.map((action, index) => (
                  <button
                    key={index}
                    onClick={action.action}
                    className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-right"
                  >
                    <div className={`p-3 rounded-lg ${action.color} mr-4`}>
                      <action.icon className="h-6 w-6 text-white" />
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900">{action.title}</h4>
                      <p className="text-sm text-gray-500">{action.description}</p>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* العمود الأيمن */}
          <div className="space-y-8">
            {/* الرسم البياني الدائري */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-6">
                حالة النباتات
              </h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={100}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {pieData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* الأنشطة الحديثة */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-900">
                  الأنشطة الحديثة
                </h3>
                <Link
                  to="/activity"
                  className="text-sm text-green-600 hover:text-green-700"
                >
                  عرض الكل
                </Link>
              </div>
              
              <div className="space-y-4">
                {recentActivities.slice(0, 5).map((activity) => (
                  <div
                    key={activity.id}
                    className="flex items-start space-x-3 space-x-reverse cursor-pointer hover:bg-gray-50 p-2 rounded-lg transition-colors"
                    onClick={activity.action}
                  >
                    <div className={`p-2 rounded-lg bg-gray-100 ${activity.color}`}>
                      <activity.icon className="h-4 w-4" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {activity.title}
                      </p>
                      <p className="text-xs text-gray-500 truncate">
                        {activity.description}
                      </p>
                      <p className="text-xs text-gray-400 mt-1">
                        {new Date(activity.time).toLocaleDateString('ar-SA')}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* ويدجت الطقس */}
            <WeatherWidget />
          </div>
        </div>

        {/* روابط سريعة إضافية */}
        <div className="mt-8 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">
            روابط سريعة
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
            <Link
              to="/farms"
              className="flex flex-col items-center p-4 text-center hover:bg-gray-50 rounded-lg transition-colors"
            >
              <Sprout className="h-8 w-8 text-green-600 mb-2" />
              <span className="text-sm font-medium text-gray-900">المزارع</span>
            </Link>
            <Link
              to="/plants"
              className="flex flex-col items-center p-4 text-center hover:bg-gray-50 rounded-lg transition-colors"
            >
              <Activity className="h-8 w-8 text-blue-600 mb-2" />
              <span className="text-sm font-medium text-gray-900">النباتات</span>
            </Link>
            <Link
              to="/diagnosis"
              className="flex flex-col items-center p-4 text-center hover:bg-gray-50 rounded-lg transition-colors"
            >
              <TrendingUp className="h-8 w-8 text-purple-600 mb-2" />
              <span className="text-sm font-medium text-gray-900">التشخيص</span>
            </Link>
            <Link
              to="/reports"
              className="flex flex-col items-center p-4 text-center hover:bg-gray-50 rounded-lg transition-colors"
            >
              <BarChart className="h-8 w-8 text-orange-600 mb-2" />
              <span className="text-sm font-medium text-gray-900">التقارير</span>
            </Link>
            <Link
              to="/settings"
              className="flex flex-col items-center p-4 text-center hover:bg-gray-50 rounded-lg transition-colors"
            >
              <Settings className="h-8 w-8 text-gray-600 mb-2" />
              <span className="text-sm font-medium text-gray-900">الإعدادات</span>
            </Link>
            <Link
              to="/help"
              className="flex flex-col items-center p-4 text-center hover:bg-gray-50 rounded-lg transition-colors"
            >
              <HelpCircle className="h-8 w-8 text-indigo-600 mb-2" />
              <span className="text-sm font-medium text-gray-900">المساعدة</span>
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
};

export default DashboardComplete;

