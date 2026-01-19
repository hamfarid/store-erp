/**
 * Analytics Page - Data Visualization & Insights
 * ===============================================
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useEffect, useMemo } from 'react';
import {
  BarChart3, TrendingUp, TrendingDown, PieChart as PieChartIcon,
  Calendar, Download, RefreshCw, Filter, ArrowUpRight, ArrowDownRight,
  Leaf, Bug, Warehouse, Users, Activity, Target, Eye, FileText
} from 'lucide-react';
import {
  AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell,
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, RadialBarChart, RadialBar
} from 'recharts';

import ApiService from '../services/ApiService';
import { Card, CardHeader, CardContent } from '../components/UI/card';
import { Button } from '../components/UI/button';
import { Badge } from '../components/UI/badge';
import { PageHeader } from '../components/UI/page-header';
import { Select } from '../src/components/Form';
import { StatCard } from '../src/components/Card';

// ============================================
// Constants
// ============================================
const COLORS = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4'];

const TIME_RANGES = [
  { value: '7d', label: 'Last 7 Days', labelAr: 'آخر 7 أيام' },
  { value: '30d', label: 'Last 30 Days', labelAr: 'آخر 30 يوم' },
  { value: '90d', label: 'Last 90 Days', labelAr: 'آخر 90 يوم' },
  { value: '1y', label: 'Last Year', labelAr: 'آخر سنة' }
];

// ============================================
// Stat Card with Trend
// ============================================
const TrendStatCard = ({ title, titleAr, value, trend, trendValue, icon: Icon, color }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const isPositive = trend === 'up';

  const colorClasses = {
    emerald: 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600',
    blue: 'bg-blue-100 dark:bg-blue-900/30 text-blue-600',
    amber: 'bg-amber-100 dark:bg-amber-900/30 text-amber-600',
    red: 'bg-red-100 dark:bg-red-900/30 text-red-600',
    purple: 'bg-purple-100 dark:bg-purple-900/30 text-purple-600'
  };

  return (
    <Card className="relative overflow-hidden">
      <div className="p-6">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">
              {isRTL ? titleAr : title}
            </p>
            <h3 className="text-2xl font-bold text-gray-800 dark:text-white">
              {value}
            </h3>
            {trendValue && (
              <div className={`flex items-center gap-1 mt-2 text-sm ${isPositive ? 'text-emerald-600' : 'text-red-500'}`}>
                {isPositive ? <ArrowUpRight className="w-4 h-4" /> : <ArrowDownRight className="w-4 h-4" />}
                <span>{trendValue}%</span>
                <span className="text-gray-500">{isRTL ? 'من الفترة السابقة' : 'from last period'}</span>
              </div>
            )}
          </div>
          <div className={`p-3 rounded-xl ${colorClasses[color]}`}>
            <Icon className="w-6 h-6" />
          </div>
        </div>
      </div>
      <div className={`absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-${color}-500 to-${color}-300`} />
    </Card>
  );
};

// ============================================
// Chart Card Wrapper
// ============================================
const ChartCard = ({ title, titleAr, subtitle, children, actions }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <div>
          <h3 className="font-semibold text-gray-800 dark:text-white">
            {isRTL ? titleAr : title}
          </h3>
          {subtitle && <p className="text-sm text-gray-500">{subtitle}</p>}
        </div>
        {actions}
      </CardHeader>
      <CardContent>{children}</CardContent>
    </Card>
  );
};

// ============================================
// Main Analytics Page
// ============================================
const Analytics = () => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('30d');
  const [data, setData] = useState(null);

  // Load analytics data
  useEffect(() => {
    loadAnalytics();
  }, [timeRange]);

  const loadAnalytics = async () => {
    setLoading(true);
    try {
      const response = await ApiService.getAnalytics({ range: timeRange });
      setData(response);
    } catch (err) {
      console.error('Error loading analytics:', err);
      // Use mock data for demonstration
      setData(generateMockData());
    } finally {
      setLoading(false);
    }
  };

  // Generate mock data for demonstration
  const generateMockData = () => ({
    stats: {
      totalDiagnoses: 1247,
      totalFarms: 45,
      totalCrops: 128,
      totalUsers: 89,
      diagnosesGrowth: 12.5,
      farmsGrowth: 8.3,
      healthyPercentage: 78.5
    },
    diagnosesOverTime: Array.from({ length: 30 }, (_, i) => ({
      date: new Date(Date.now() - (29 - i) * 24 * 60 * 60 * 1000).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      diagnoses: Math.floor(Math.random() * 50) + 20,
      healthy: Math.floor(Math.random() * 30) + 10,
      diseased: Math.floor(Math.random() * 20) + 5
    })),
    diseaseDistribution: [
      { name: 'Healthy', nameAr: 'صحي', value: 45, color: '#10b981' },
      { name: 'Early Blight', nameAr: 'اللفحة المبكرة', value: 15, color: '#f59e0b' },
      { name: 'Late Blight', nameAr: 'اللفحة المتأخرة', value: 12, color: '#ef4444' },
      { name: 'Leaf Mold', nameAr: 'عفن الأوراق', value: 10, color: '#3b82f6' },
      { name: 'Bacterial Spot', nameAr: 'البقع البكتيرية', value: 8, color: '#8b5cf6' },
      { name: 'Other', nameAr: 'أخرى', value: 10, color: '#6b7280' }
    ],
    cropPerformance: [
      { name: 'Tomato', nameAr: 'طماطم', healthy: 85, diseased: 15 },
      { name: 'Potato', nameAr: 'بطاطس', healthy: 72, diseased: 28 },
      { name: 'Pepper', nameAr: 'فلفل', healthy: 90, diseased: 10 },
      { name: 'Cucumber', nameAr: 'خيار', healthy: 78, diseased: 22 },
      { name: 'Wheat', nameAr: 'قمح', healthy: 88, diseased: 12 }
    ],
    monthlyTrends: [
      { month: 'Jan', diagnoses: 180, accuracy: 95 },
      { month: 'Feb', diagnoses: 220, accuracy: 96 },
      { month: 'Mar', diagnoses: 280, accuracy: 94 },
      { month: 'Apr', diagnoses: 350, accuracy: 97 },
      { month: 'May', diagnoses: 420, accuracy: 98 },
      { month: 'Jun', diagnoses: 380, accuracy: 97 }
    ],
    recentActivity: [
      { type: 'diagnosis', message: 'New diagnosis completed', time: '2 min ago' },
      { type: 'farm', message: 'Farm "Green Valley" updated', time: '15 min ago' },
      { type: 'user', message: 'New user registered', time: '1 hour ago' },
      { type: 'report', message: 'Monthly report generated', time: '3 hours ago' }
    ]
  });

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white dark:bg-gray-800 p-3 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
          <p className="font-medium text-gray-800 dark:text-white">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }} className="text-sm">
              {entry.name}: {entry.value}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-6" />
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-32 bg-gray-200 dark:bg-gray-700 rounded-lg" />
            ))}
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-80 bg-gray-200 dark:bg-gray-700 rounded-lg" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <PageHeader
        title={isRTL ? 'التحليلات' : 'Analytics'}
        description={isRTL ? 'رؤى وإحصائيات شاملة عن النظام' : 'Comprehensive insights and statistics'}
        icon={BarChart3}
      >
        <div className="flex items-center gap-3">
          <Select
            value={timeRange}
            onChange={setTimeRange}
            options={TIME_RANGES}
            className="w-40"
          />
          <Button variant="outline" onClick={loadAnalytics}>
            <RefreshCw className="w-4 h-4" />
          </Button>
          <Button variant="outline">
            <Download className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
            {isRTL ? 'تصدير' : 'Export'}
          </Button>
        </div>
      </PageHeader>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <TrendStatCard
          title="Total Diagnoses"
          titleAr="إجمالي التشخيصات"
          value={data?.stats?.totalDiagnoses?.toLocaleString()}
          trend="up"
          trendValue={data?.stats?.diagnosesGrowth}
          icon={Leaf}
          color="emerald"
        />
        <TrendStatCard
          title="Active Farms"
          titleAr="المزارع النشطة"
          value={data?.stats?.totalFarms}
          trend="up"
          trendValue={data?.stats?.farmsGrowth}
          icon={Warehouse}
          color="blue"
        />
        <TrendStatCard
          title="Healthy Rate"
          titleAr="نسبة الصحة"
          value={`${data?.stats?.healthyPercentage}%`}
          trend="up"
          trendValue={2.3}
          icon={Activity}
          color="purple"
        />
        <TrendStatCard
          title="Total Users"
          titleAr="إجمالي المستخدمين"
          value={data?.stats?.totalUsers}
          trend="up"
          trendValue={5.1}
          icon={Users}
          color="amber"
        />
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Diagnoses Over Time */}
        <ChartCard
          title="Diagnoses Over Time"
          titleAr="التشخيصات عبر الوقت"
          subtitle={isRTL ? 'عدد التشخيصات اليومية' : 'Daily diagnosis count'}
        >
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={data?.diagnosesOverTime}>
              <defs>
                <linearGradient id="colorDiagnoses" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="date" stroke="#9ca3af" fontSize={12} />
              <YAxis stroke="#9ca3af" fontSize={12} />
              <Tooltip content={<CustomTooltip />} />
              <Area
                type="monotone"
                dataKey="diagnoses"
                stroke="#10b981"
                strokeWidth={2}
                fill="url(#colorDiagnoses)"
                name={isRTL ? 'التشخيصات' : 'Diagnoses'}
              />
            </AreaChart>
          </ResponsiveContainer>
        </ChartCard>

        {/* Disease Distribution */}
        <ChartCard
          title="Disease Distribution"
          titleAr="توزيع الأمراض"
          subtitle={isRTL ? 'نسب الأمراض المكتشفة' : 'Detected diseases breakdown'}
        >
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={data?.diseaseDistribution}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={2}
                dataKey="value"
                nameKey={isRTL ? 'nameAr' : 'name'}
              >
                {data?.diseaseDistribution?.map((entry, index) => (
                  <Cell key={index} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
              <Legend
                layout="vertical"
                align={isRTL ? 'left' : 'right'}
                verticalAlign="middle"
                formatter={(value, entry) => (
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    {isRTL ? entry.payload.nameAr : entry.payload.name}
                  </span>
                )}
              />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Crop Performance */}
        <ChartCard
          title="Crop Health Performance"
          titleAr="أداء صحة المحاصيل"
          subtitle={isRTL ? 'مقارنة الصحة بين المحاصيل' : 'Health comparison across crops'}
        >
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data?.cropPerformance} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis type="number" stroke="#9ca3af" fontSize={12} />
              <YAxis
                dataKey={isRTL ? 'nameAr' : 'name'}
                type="category"
                stroke="#9ca3af"
                fontSize={12}
                width={80}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              <Bar dataKey="healthy" fill="#10b981" name={isRTL ? 'صحي' : 'Healthy'} stackId="a" />
              <Bar dataKey="diseased" fill="#ef4444" name={isRTL ? 'مصاب' : 'Diseased'} stackId="a" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        {/* Monthly Trends */}
        <ChartCard
          title="Monthly Trends"
          titleAr="الاتجاهات الشهرية"
          subtitle={isRTL ? 'التشخيصات ودقة النظام' : 'Diagnoses and system accuracy'}
        >
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data?.monthlyTrends}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="month" stroke="#9ca3af" fontSize={12} />
              <YAxis yAxisId="left" stroke="#9ca3af" fontSize={12} />
              <YAxis yAxisId="right" orientation="right" stroke="#9ca3af" fontSize={12} domain={[90, 100]} />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              <Line
                yAxisId="left"
                type="monotone"
                dataKey="diagnoses"
                stroke="#3b82f6"
                strokeWidth={2}
                dot={{ r: 4 }}
                name={isRTL ? 'التشخيصات' : 'Diagnoses'}
              />
              <Line
                yAxisId="right"
                type="monotone"
                dataKey="accuracy"
                stroke="#10b981"
                strokeWidth={2}
                dot={{ r: 4 }}
                name={isRTL ? 'الدقة %' : 'Accuracy %'}
              />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      {/* Bottom Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Top Diseases */}
        <Card>
          <CardHeader>
            <h3 className="font-semibold flex items-center gap-2">
              <Bug className="w-5 h-5 text-red-500" />
              {isRTL ? 'أكثر الأمراض شيوعاً' : 'Top Diseases'}
            </h3>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {data?.diseaseDistribution?.slice(1).map((disease, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-3 h-3 rounded-full" style={{ backgroundColor: disease.color }} />
                    <span className="text-sm text-gray-700 dark:text-gray-300">
                      {isRTL ? disease.nameAr : disease.name}
                    </span>
                  </div>
                  <Badge variant="secondary">{disease.value}%</Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Quick Stats */}
        <Card>
          <CardHeader>
            <h3 className="font-semibold flex items-center gap-2">
              <Target className="w-5 h-5 text-emerald-500" />
              {isRTL ? 'إحصائيات سريعة' : 'Quick Stats'}
            </h3>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  {isRTL ? 'دقة التشخيص' : 'Diagnosis Accuracy'}
                </span>
                <span className="text-lg font-bold text-emerald-600">98.5%</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  {isRTL ? 'وقت المعالجة' : 'Processing Time'}
                </span>
                <span className="text-lg font-bold text-blue-600">1.2s</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  {isRTL ? 'وقت التشغيل' : 'Uptime'}
                </span>
                <span className="text-lg font-bold text-purple-600">99.9%</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <h3 className="font-semibold flex items-center gap-2">
              <Activity className="w-5 h-5 text-blue-500" />
              {isRTL ? 'النشاط الأخير' : 'Recent Activity'}
            </h3>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {data?.recentActivity?.map((activity, index) => (
                <div key={index} className="flex items-start gap-3 p-2 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg transition-colors">
                  <div className={`p-2 rounded-lg ${
                    activity.type === 'diagnosis' ? 'bg-emerald-100 text-emerald-600' :
                    activity.type === 'farm' ? 'bg-blue-100 text-blue-600' :
                    activity.type === 'user' ? 'bg-purple-100 text-purple-600' :
                    'bg-amber-100 text-amber-600'
                  }`}>
                    {activity.type === 'diagnosis' ? <Leaf className="w-4 h-4" /> :
                     activity.type === 'farm' ? <Warehouse className="w-4 h-4" /> :
                     activity.type === 'user' ? <Users className="w-4 h-4" /> :
                     <FileText className="w-4 h-4" />}
                  </div>
                  <div className="flex-1">
                    <p className="text-sm text-gray-700 dark:text-gray-300">{activity.message}</p>
                    <p className="text-xs text-gray-500">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Analytics;
