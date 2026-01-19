// ملف: /home/ubuntu/gaara_ai_COMPREHENSIVE_BACKUP_20250707_054013/gaara_ai_integrated/frontend/src/pages/Dashboard/Dashboard.jsx
// لوحة التحكم الرئيسية لنظام Gaara AI
// الإصدار: 2.0.0
// تم الإنشاء: 2025-01-07
// المطور: Gaara Group & Manus AI

import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  Sprout,
  TreePine,
  Bug,
  Stethoscope,
  Wheat,
  Cpu,
  Users,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Clock,
  Plus,
  Eye,
  BarChart3,
  Activity,
  Thermometer,
  Droplets,
  Sun,
  Wind
} from 'lucide-react';
import { ApiService } from '../../services/ApiService';
import LoadingSpinner from '../../components/UI/LoadingSpinner';
import ErrorMessage from '../../components/UI/ErrorMessage';

const Dashboard = () => {
  const navigate = useNavigate();
  const [selectedTimeRange, setSelectedTimeRange] = useState('week');

  // استعلامات البيانات
  const { data: dashboardStats, isLoading: statsLoading, error: statsError } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => ApiService.getDashboardStats(),
    refetchInterval: 30000, // تحديث كل 30 ثانية
  });

  const { data: recentDiagnoses, isLoading: diagnosesLoading } = useQuery({
    queryKey: ['recent-diagnoses'],
    queryFn: () => ApiService.get('/diagnosis/recent'),
  });

  const { data: weatherData, isLoading: weatherLoading } = useQuery({
    queryKey: ['weather-data'],
    queryFn: () => ApiService.get('/weather/current'),
    refetchInterval: 300000, // تحديث كل 5 دقائق
  });

  const { data: alertsData, isLoading: alertsLoading } = useQuery({
    queryKey: ['alerts'],
    queryFn: () => ApiService.get('/alerts/active'),
  });

  // بيانات وهمية في حالة عدم توفر البيانات من الخادم
  const defaultStats = {
    farms: { total: 12, active: 10, inactive: 2 },
    plants: { total: 156, healthy: 142, diseased: 14 },
    diagnoses: { today: 8, week: 45, month: 180 },
    sensors: { total: 24, online: 22, offline: 2 },
    alerts: { critical: 2, warning: 5, info: 3 }
  };

  const stats = dashboardStats?.data || defaultStats;

  // بطاقات الإحصائيات الرئيسية
  const mainCards = [
    {
      title: 'المزارع',
      total: stats.farms?.total || 0,
      active: stats.farms?.active || 0,
      icon: Sprout,
      color: 'green',
      link: '/farms',
      createLink: '/farms/create'
    },
    {
      title: 'النباتات',
      total: stats.plants?.total || 0,
      active: stats.plants?.healthy || 0,
      icon: TreePine,
      color: 'emerald',
      link: '/plants',
      createLink: '/plants/create'
    },
    {
      title: 'التشخيصات',
      total: stats.diagnoses?.month || 0,
      active: stats.diagnoses?.today || 0,
      icon: Stethoscope,
      color: 'blue',
      link: '/diagnosis',
      createLink: '/diagnosis/create'
    },
    {
      title: 'أجهزة الاستشعار',
      total: stats.sensors?.total || 0,
      active: stats.sensors?.online || 0,
      icon: Cpu,
      color: 'purple',
      link: '/sensors',
      createLink: '/sensors/create'
    }
  ];

  // الإجراءات السريعة
  const quickActions = [
    {
      title: 'تشخيص سريع',
      description: 'تشخيص مرض النبات بالذكاء الاصطناعي',
      icon: Stethoscope,
      color: 'bg-blue-500',
      link: '/diagnosis/create'
    },
    {
      title: 'إضافة مزرعة',
      description: 'تسجيل مزرعة جديدة في النظام',
      icon: Sprout,
      color: 'bg-green-500',
      link: '/farms/create'
    },
    {
      title: 'إضافة نبات',
      description: 'تسجيل نوع نبات جديد',
      icon: TreePine,
      color: 'bg-emerald-500',
      link: '/plants/create'
    },
    {
      title: 'عرض التقارير',
      description: 'مراجعة التقارير والإحصائيات',
      icon: BarChart3,
      color: 'bg-purple-500',
      link: '/reports'
    }
  ];

  if (statsLoading) {
    return <LoadingSpinner />;
  }

  if (statsError) {
    return <ErrorMessage message="خطأ في تحميل بيانات لوحة التحكم" />;
  }

  return (
    <div className="space-y-6">
      {/* العنوان والترحيب */}
      <div className="bg-gradient-to-l from-green-600 to-emerald-600 rounded-lg p-6 text-white">
        <h1 className="text-3xl font-bold mb-2">مرحباً بك في نظام Gaara AI</h1>
        <p className="text-green-100">
          نظام الزراعة الذكية المتطور - لوحة التحكم الرئيسية
        </p>
        <div className="mt-4 flex items-center space-x-4 rtl:space-x-reverse">
          <div className="flex items-center space-x-2 rtl:space-x-reverse">
            <Clock size={16} />
            <span className="text-sm">
              آخر تحديث: {new Date().toLocaleString('ar-SA')}
            </span>
          </div>
        </div>
      </div>

      {/* التنبيهات النشطة */}
      {alertsData?.data && alertsData.data.length > 0 && (
        <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
          <div className="flex items-center space-x-2 rtl:space-x-reverse mb-3">
            <AlertTriangle className="text-yellow-600 dark:text-yellow-400" size={20} />
            <h3 className="text-lg font-semibold text-yellow-800 dark:text-yellow-200">
              تنبيهات نشطة
            </h3>
          </div>
          <div className="space-y-2">
            {alertsData.data.slice(0, 3).map((alert, index) => (
              <div key={index} className="flex items-center justify-between bg-white dark:bg-gray-800 rounded p-3">
                <div>
                  <p className="font-medium text-gray-900 dark:text-white">{alert.title}</p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">{alert.message}</p>
                </div>
                <button
                  onClick={() => navigate(`/alerts/${alert.id}`)}
                  className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300"
                >
                  <Eye size={16} />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* البطاقات الرئيسية */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {mainCards.map((card, index) => (
          <div
            key={index}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 hover:shadow-md transition-shadow"
          >
            <div className="flex items-center justify-between mb-4">
              <div className={`p-3 rounded-lg bg-${card.color}-100 dark:bg-${card.color}-900/20`}>
                <card.icon className={`text-${card.color}-600 dark:text-${card.color}-400`} size={24} />
              </div>
              <div className="flex space-x-2 rtl:space-x-reverse">
                <Link
                  to={card.link}
                  className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                  title="عرض الكل"
                >
                  <Eye size={16} />
                </Link>
                <Link
                  to={card.createLink}
                  className={`p-2 text-${card.color}-600 dark:text-${card.color}-400 hover:text-${card.color}-700 dark:hover:text-${card.color}-300 transition-colors`}
                  title="إضافة جديد"
                >
                  <Plus size={16} />
                </Link>
              </div>
            </div>
            
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              {card.title}
            </h3>
            
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-2xl font-bold text-gray-900 dark:text-white">
                  {card.total}
                </span>
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  الإجمالي
                </span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className={`text-lg font-semibold text-${card.color}-600 dark:text-${card.color}-400`}>
                  {card.active}
                </span>
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  نشط
                </span>
              </div>
            </div>
            
            <Link
              to={card.link}
              className={`mt-4 block w-full text-center py-2 px-4 bg-${card.color}-50 dark:bg-${card.color}-900/20 text-${card.color}-700 dark:text-${card.color}-300 rounded-lg hover:bg-${card.color}-100 dark:hover:bg-${card.color}-900/30 transition-colors`}
            >
              عرض التفاصيل
            </Link>
          </div>
        ))}
      </div>

      {/* الإجراءات السريعة */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
          الإجراءات السريعة
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickActions.map((action, index) => (
            <Link
              key={index}
              to={action.link}
              className="group p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-gray-300 dark:hover:border-gray-600 hover:shadow-sm transition-all"
            >
              <div className={`w-12 h-12 ${action.color} rounded-lg flex items-center justify-center mb-3 group-hover:scale-105 transition-transform`}>
                <action.icon className="text-white" size={24} />
              </div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                {action.title}
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {action.description}
              </p>
            </Link>
          ))}
        </div>
      </div>

      {/* الصف السفلي - معلومات إضافية */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* التشخيصات الأخيرة */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              التشخيصات الأخيرة
            </h3>
            <Link
              to="/diagnosis/history"
              className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 text-sm"
            >
              عرض الكل
            </Link>
          </div>
          
          {diagnosesLoading ? (
            <div className="text-center py-4">
              <LoadingSpinner size="sm" />
            </div>
          ) : (
            <div className="space-y-3">
              {recentDiagnoses?.data?.slice(0, 5).map((diagnosis, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg"
                >
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">
                      {diagnosis.plant_name}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {diagnosis.disease_name}
                    </p>
                  </div>
                  <div className="text-left rtl:text-right">
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {new Date(diagnosis.created_at).toLocaleDateString('ar-SA')}
                    </p>
                    <span className={`inline-block w-2 h-2 rounded-full ${
                      diagnosis.confidence > 0.8 ? 'bg-green-500' :
                      diagnosis.confidence > 0.6 ? 'bg-yellow-500' : 'bg-red-500'
                    }`} />
                  </div>
                </div>
              )) || (
                <p className="text-center text-gray-500 dark:text-gray-400 py-4">
                  لا توجد تشخيصات حديثة
                </p>
              )}
            </div>
          )}
        </div>

        {/* معلومات الطقس */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            حالة الطقس
          </h3>
          
          {weatherLoading ? (
            <div className="text-center py-4">
              <LoadingSpinner size="sm" />
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3 rtl:space-x-reverse">
                  <Sun className="text-yellow-500" size={24} />
                  <div>
                    <p className="font-semibold text-gray-900 dark:text-white">
                      {weatherData?.data?.temperature || '25'}°م
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {weatherData?.data?.description || 'مشمس'}
                    </p>
                  </div>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="flex items-center space-x-2 rtl:space-x-reverse">
                  <Droplets className="text-blue-500" size={16} />
                  <span className="text-gray-600 dark:text-gray-400">
                    الرطوبة: {weatherData?.data?.humidity || '60'}%
                  </span>
                </div>
                <div className="flex items-center space-x-2 rtl:space-x-reverse">
                  <Wind className="text-gray-500" size={16} />
                  <span className="text-gray-600 dark:text-gray-400">
                    الرياح: {weatherData?.data?.wind_speed || '15'} كم/س
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* إحصائيات سريعة */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            إحصائيات اليوم
          </h3>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2 rtl:space-x-reverse">
                <Activity className="text-green-500" size={16} />
                <span className="text-gray-600 dark:text-gray-400">التشخيصات</span>
              </div>
              <span className="font-semibold text-gray-900 dark:text-white">
                {stats.diagnoses?.today || 0}
              </span>
            </div>
            
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2 rtl:space-x-reverse">
                <CheckCircle className="text-blue-500" size={16} />
                <span className="text-gray-600 dark:text-gray-400">المزارع النشطة</span>
              </div>
              <span className="font-semibold text-gray-900 dark:text-white">
                {stats.farms?.active || 0}
              </span>
            </div>
            
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2 rtl:space-x-reverse">
                <AlertTriangle className="text-yellow-500" size={16} />
                <span className="text-gray-600 dark:text-gray-400">التنبيهات</span>
              </div>
              <span className="font-semibold text-gray-900 dark:text-white">
                {stats.alerts?.critical + stats.alerts?.warning || 0}
              </span>
            </div>
            
            <Link
              to="/analytics"
              className="block w-full text-center py-2 px-4 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/30 transition-colors"
            >
              عرض التحليلات المفصلة
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

