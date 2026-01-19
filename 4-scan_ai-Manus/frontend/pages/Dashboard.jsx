/**
 * Dashboard Page - Modern Dashboard with Charts and Stats
 * @file pages/Dashboard.jsx
 * 
 * Features:
 * - Stats cards with trends
 * - Interactive charts
 * - Recent activity feed
 * - Quick actions
 * - Arabic RTL support
 * - Dark mode support
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import {
  LayoutDashboard,
  Home,
  Bug,
  Leaf,
  Thermometer,
  Droplet,
  Sun,
  Wind,
  Activity,
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  CheckCircle,
  Clock,
  ArrowUpRight,
  Plus,
  Camera,
  FileText,
  BarChart3,
  Calendar,
  Users,
  Building
} from 'lucide-react';

// UI Components
import { Card, CardHeader, CardTitle, CardDescription, CardContent, StatsCard } from '../components/UI/card';
import { Button } from '../components/UI/button';
import { Badge, StatusBadge } from '../components/UI/badge';
import { PageHeader, Section } from '../components/UI/page-header';
import { cn, formatDate, formatNumber } from '../lib/utils';

// Services
import ApiService from '../services/ApiService';

// ============================================
// Chart Colors
// ============================================
const CHART_COLORS = {
  primary: '#10b981',
  secondary: '#3b82f6',
  warning: '#f59e0b',
  danger: '#ef4444',
  purple: '#8b5cf6',
  pink: '#ec4899',
};

const PIE_COLORS = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

// ============================================
// Mock Data (Replace with API calls)
// ============================================
const mockStats = {
  totalFarms: 24,
  activeDiagnosis: 156,
  healthyCrops: 892,
  alerts: 12,
};

const mockTrendData = [
  { month: 'يناير', diagnoses: 65, healthy: 80, infected: 15 },
  { month: 'فبراير', diagnoses: 72, healthy: 85, infected: 12 },
  { month: 'مارس', diagnoses: 89, healthy: 90, infected: 8 },
  { month: 'أبريل', diagnoses: 95, healthy: 88, infected: 10 },
  { month: 'مايو', diagnoses: 110, healthy: 92, infected: 6 },
  { month: 'يونيو', diagnoses: 125, healthy: 95, infected: 5 },
];

const mockDiseaseData = [
  { name: 'البياض الدقيقي', value: 35, color: '#10b981' },
  { name: 'الصدأ', value: 25, color: '#3b82f6' },
  { name: 'تبقع الأوراق', value: 20, color: '#f59e0b' },
  { name: 'العفن الرمادي', value: 12, color: '#ef4444' },
  { name: 'أخرى', value: 8, color: '#8b5cf6' },
];

const mockRecentActivity = [
  { id: 1, type: 'diagnosis', title: 'تشخيص جديد', description: 'تم رفع صورة للتحليل من مزرعة الوادي', time: 'منذ 5 دقائق', status: 'success' },
  { id: 2, type: 'alert', title: 'تنبيه', description: 'تم اكتشاف مرض البياض الدقيقي', time: 'منذ 15 دقيقة', status: 'warning' },
  { id: 3, type: 'farm', title: 'مزرعة جديدة', description: 'تم إضافة مزرعة السهل الشمالي', time: 'منذ ساعة', status: 'info' },
  { id: 4, type: 'report', title: 'تقرير جاهز', description: 'تقرير الأداء الشهري متاح للتحميل', time: 'منذ 3 ساعات', status: 'success' },
  { id: 5, type: 'sensor', title: 'قراءة المستشعر', description: 'رطوبة التربة منخفضة في القطاع الشرقي', time: 'منذ 5 ساعات', status: 'warning' },
];

const mockSensorData = [
  { name: 'الرطوبة', value: 72, unit: '%', icon: Droplet, color: 'blue', trend: 'up', change: '+5%' },
  { name: 'درجة الحرارة', value: 28, unit: '°C', icon: Thermometer, color: 'amber', trend: 'down', change: '-2°' },
  { name: 'شدة الضوء', value: 850, unit: 'lux', icon: Sun, color: 'emerald', trend: 'up', change: '+120' },
  { name: 'سرعة الرياح', value: 12, unit: 'km/h', icon: Wind, color: 'purple', trend: 'stable', change: '0' },
];

// ============================================
// Dashboard Components
// ============================================

// Quick Actions Component
const QuickActions = ({ navigate }) => {
  const actions = [
    { icon: Camera, label: 'تشخيص جديد', path: '/diagnosis', color: 'emerald' },
    { icon: Home, label: 'إضافة مزرعة', path: '/farms', color: 'blue' },
    { icon: FileText, label: 'تقرير جديد', path: '/reports', color: 'purple' },
    { icon: BarChart3, label: 'التحليلات', path: '/analytics', color: 'amber' },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {actions.map((action) => {
        const Icon = action.icon;
        const colorClasses = {
          emerald: 'hover:bg-emerald-50 dark:hover:bg-emerald-900/20 hover:border-emerald-200',
          blue: 'hover:bg-blue-50 dark:hover:bg-blue-900/20 hover:border-blue-200',
          purple: 'hover:bg-purple-50 dark:hover:bg-purple-900/20 hover:border-purple-200',
          amber: 'hover:bg-amber-50 dark:hover:bg-amber-900/20 hover:border-amber-200',
        };
        const iconClasses = {
          emerald: 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400',
          blue: 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400',
          purple: 'bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400',
          amber: 'bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400',
        };

        return (
          <button
            key={action.path}
            onClick={() => navigate(action.path)}
            className={cn(
              "flex flex-col items-center gap-3 p-6 rounded-xl border border-gray-200 dark:border-gray-700",
              "bg-white dark:bg-gray-800 transition-all duration-200",
              colorClasses[action.color]
            )}
          >
            <div className={cn("w-12 h-12 rounded-xl flex items-center justify-center", iconClasses[action.color])}>
              <Icon className="h-6 w-6" />
            </div>
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{action.label}</span>
          </button>
        );
      })}
    </div>
  );
};

// Recent Activity Component
const RecentActivity = ({ activities }) => {
  const getStatusIcon = (status) => {
    switch (status) {
      case 'success': return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'warning': return <AlertTriangle className="h-4 w-4 text-amber-500" />;
      case 'error': return <AlertTriangle className="h-4 w-4 text-red-500" />;
      default: return <Activity className="h-4 w-4 text-blue-500" />;
    }
  };

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <div>
          <CardTitle>النشاط الأخير</CardTitle>
          <CardDescription>آخر الأنشطة والتحديثات</CardDescription>
        </div>
        <Button variant="ghost" size="sm">عرض الكل</Button>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {activities.map((activity) => (
            <div key={activity.id} className="flex items-start gap-4 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
              <div className="mt-1">{getStatusIcon(activity.status)}</div>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-gray-900 dark:text-gray-100">{activity.title}</p>
                <p className="text-sm text-gray-500 dark:text-gray-400 truncate">{activity.description}</p>
              </div>
              <span className="text-xs text-gray-400 whitespace-nowrap">{activity.time}</span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

// Sensor Cards Component
const SensorCards = ({ sensors }) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {sensors.map((sensor) => {
        const Icon = sensor.icon;
        const colorClasses = {
          blue: 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400',
          amber: 'bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400',
          emerald: 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400',
          purple: 'bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400',
        };

        return (
          <Card key={sensor.name} className="p-4">
            <div className="flex items-center justify-between mb-3">
              <div className={cn("w-10 h-10 rounded-lg flex items-center justify-center", colorClasses[sensor.color])}>
                <Icon className="h-5 w-5" />
              </div>
              <span className={cn(
                "flex items-center gap-1 text-sm font-medium",
                sensor.trend === 'up' ? 'text-green-500' :
                sensor.trend === 'down' ? 'text-red-500' : 'text-gray-500'
              )}>
                {sensor.trend === 'up' && <TrendingUp className="h-4 w-4" />}
                {sensor.trend === 'down' && <TrendingDown className="h-4 w-4" />}
                {sensor.change}
              </span>
            </div>
            <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
              {sensor.value}<span className="text-base font-normal text-gray-500">{sensor.unit}</span>
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{sensor.name}</p>
          </Card>
        );
      })}
    </div>
  );
};

// Custom Tooltip for Charts
const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white dark:bg-gray-800 p-3 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
        <p className="font-medium text-gray-900 dark:text-gray-100 mb-2">{label}</p>
        {payload.map((item, index) => (
          <p key={index} className="text-sm" style={{ color: item.color }}>
            {item.name}: {item.value}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

// ============================================
// Main Dashboard Component
// ============================================
const Dashboard = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(mockStats);
  const [activities, setActivities] = useState(mockRecentActivity);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        setLoading(true);
        // TODO: Replace with actual API calls
        // const response = await ApiService.getDashboardData();
        // setStats(response.stats);
        await new Promise(resolve => setTimeout(resolve, 500));
      } catch (error) {
        console.error('Error loading dashboard:', error);
        toast.error('فشل في تحميل بيانات لوحة التحكم');
      } finally {
        setLoading(false);
      }
    };

    loadDashboardData();
  }, []);

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <PageHeader
        title="لوحة التحكم"
        description={`مرحباً! هذا ملخص نظام Gaara Scan AI الخاص بك`}
        icon={LayoutDashboard}
      >
        <Button variant="outline" onClick={() => window.location.reload()}>
          تحديث البيانات
        </Button>
      </PageHeader>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="إجمالي المزارع"
          value={formatNumber(stats.totalFarms)}
          icon={Home}
          variant="default"
          trend="up"
          trendValue="+3 هذا الشهر"
        />
        <StatsCard
          title="التشخيصات النشطة"
          value={formatNumber(stats.activeDiagnosis)}
          icon={Bug}
          variant="blue"
          trend="up"
          trendValue="+24%"
        />
        <StatsCard
          title="المحاصيل السليمة"
          value={formatNumber(stats.healthyCrops)}
          icon={Leaf}
          variant="purple"
          trend="up"
          trendValue="95%"
        />
        <StatsCard
          title="التنبيهات"
          value={formatNumber(stats.alerts)}
          icon={AlertTriangle}
          variant="red"
          trend="down"
          trendValue="-8%"
        />
      </div>

      {/* Quick Actions */}
      <Section title="إجراءات سريعة" description="ابدأ مهمة جديدة">
        <QuickActions navigate={navigate} />
      </Section>

      {/* Sensor Data */}
      <Section title="بيانات المستشعرات" description="قراءات حية من الحقل">
        <SensorCards sensors={mockSensorData} />
      </Section>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Trend Chart */}
        <Card>
          <CardHeader>
            <CardTitle>تحليل التشخيصات</CardTitle>
            <CardDescription>اتجاه التشخيصات خلال الأشهر الماضية</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={mockTrendData}>
                  <defs>
                    <linearGradient id="colorHealthy" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor={CHART_COLORS.primary} stopOpacity={0.3}/>
                      <stop offset="95%" stopColor={CHART_COLORS.primary} stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="colorInfected" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor={CHART_COLORS.danger} stopOpacity={0.3}/>
                      <stop offset="95%" stopColor={CHART_COLORS.danger} stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="month" stroke="#6b7280" fontSize={12} />
                  <YAxis stroke="#6b7280" fontSize={12} />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend />
                  <Area
                    type="monotone"
                    dataKey="healthy"
                    name="سليم"
                    stroke={CHART_COLORS.primary}
                    fillOpacity={1}
                    fill="url(#colorHealthy)"
                  />
                  <Area
                    type="monotone"
                    dataKey="infected"
                    name="مصاب"
                    stroke={CHART_COLORS.danger}
                    fillOpacity={1}
                    fill="url(#colorInfected)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Disease Distribution Pie Chart */}
        <Card>
          <CardHeader>
            <CardTitle>توزيع الأمراض</CardTitle>
            <CardDescription>نسبة الأمراض المكتشفة</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] flex items-center justify-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={mockDiseaseData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {mockDiseaseData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip content={<CustomTooltip />} />
                  <Legend layout="vertical" align="left" verticalAlign="middle" />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity */}
      <RecentActivity activities={activities} />
    </div>
  );
};

export default Dashboard;
