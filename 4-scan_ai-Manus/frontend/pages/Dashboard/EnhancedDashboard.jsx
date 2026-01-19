/**
 * ملف: /home/ubuntu/gaara-ai-system/gaara_ai_integrated/frontend/src/pages/Dashboard/EnhancedDashboard.jsx
 * لوحة التحكم الرئيسية المحسنة لنظام Gaara AI
 * الإصدار: 2.0.0 - Enhanced Dashboard
 * تاريخ الإنشاء: 2025-01-21
 * المطور: Gaara AI Development Team
 */

import React, { useState, useEffect, useCallback } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  LineChart, Line, PieChart, Pie, Cell, AreaChart, Area
} from 'recharts';
import { 
  Leaf, Droplets, Thermometer, Sun, AlertTriangle, TrendingUp, 
  Users, Package, DollarSign, Activity, Calendar, Bell,
  Settings, RefreshCw, Download, Upload, Eye, Edit, Trash2,
  Plus, Search, Filter, MapPin, Wifi, WifiOff
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Alert, AlertDescription, AlertTitle } from '../../components/ui/alert';
import { Progress } from '../../components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';

// بيانات تجريبية للرسوم البيانية
const farmProductionData = [
  { month: 'يناير', production: 4000, target: 4500, efficiency: 89 },
  { month: 'فبراير', production: 3000, target: 3500, efficiency: 86 },
  { month: 'مارس', production: 5000, target: 4800, efficiency: 104 },
  { month: 'أبريل', production: 4500, target: 4200, efficiency: 107 },
  { month: 'مايو', production: 6000, target: 5500, efficiency: 109 },
  { month: 'يونيو', production: 5500, target: 5800, efficiency: 95 }
];

const cropDistributionData = [
  { name: 'القمح', value: 35, color: '#8884d8' },
  { name: 'الذرة', value: 25, color: '#82ca9d' },
  { name: 'الأرز', value: 20, color: '#ffc658' },
  { name: 'الشعير', value: 15, color: '#ff7300' },
  { name: 'أخرى', value: 5, color: '#00ff88' }
];

const weatherData = [
  { day: 'السبت', temp: 28, humidity: 65, rainfall: 0 },
  { day: 'الأحد', temp: 30, humidity: 70, rainfall: 2 },
  { day: 'الاثنين', temp: 32, humidity: 68, rainfall: 0 },
  { day: 'الثلاثاء', temp: 29, humidity: 72, rainfall: 5 },
  { day: 'الأربعاء', temp: 27, humidity: 75, rainfall: 8 },
  { day: 'الخميس', temp: 31, humidity: 63, rainfall: 0 },
  { day: 'الجمعة', temp: 33, humidity: 60, rainfall: 0 }
];

const EnhancedDashboard = () => {
  const [dashboardData, setDashboardData] = useState({
    totalFarms: 25,
    totalCrops: 150,
    activeAlerts: 8,
    totalRevenue: 2500000,
    weatherStatus: 'مشمس',
    soilMoisture: 65,
    temperature: 28,
    humidity: 70,
    lastUpdate: new Date().toLocaleString('ar-SA')
  });

  const [alerts, setAlerts] = useState([
    { id: 1, type: 'warning', title: 'انخفاض رطوبة التربة', description: 'المزرعة الشمالية تحتاج ري فوري', time: '10:30 ص' },
    { id: 2, type: 'info', title: 'موعد الحصاد', description: 'محصول القمح جاهز للحصاد خلال 3 أيام', time: '09:15 ص' },
    { id: 3, type: 'error', title: 'عطل في نظام الري', description: 'توقف نظام الري في القطاع الجنوبي', time: '08:45 ص' },
    { id: 4, type: 'success', title: 'اكتمال الزراعة', description: 'تم زراعة 50 هكتار بنجاح', time: '07:30 ص' }
  ]);

  const [isOnline, setIsOnline] = useState(true);
  const [isLoading, setIsLoading] = useState(false);

  // تحديث البيانات تلقائياً
  useEffect(() => {
    const interval = setInterval(() => {
      setDashboardData(prev => ({
        ...prev,
        lastUpdate: new Date().toLocaleString('ar-SA'),
        soilMoisture: Math.max(30, Math.min(90, prev.soilMoisture + (Math.random() - 0.5) * 5)),
        temperature: Math.max(20, Math.min(40, prev.temperature + (Math.random() - 0.5) * 2)),
        humidity: Math.max(40, Math.min(90, prev.humidity + (Math.random() - 0.5) * 3))
      }));
    }, 30000); // تحديث كل 30 ثانية

    return () => clearInterval(interval);
  }, []);

  const handleRefreshData = useCallback(async () => {
    setIsLoading(true);
    try {
      // محاكاة استدعاء API
      await new Promise(resolve => setTimeout(resolve, 2000));
      setDashboardData(prev => ({
        ...prev,
        lastUpdate: new Date().toLocaleString('ar-SA')
      }));
    } catch (error) {
      console.error('خطأ في تحديث البيانات:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const getAlertIcon = (type) => {
    switch (type) {
      case 'warning': return <AlertTriangle className="h-4 w-4 text-yellow-500" />;
      case 'error': return <AlertTriangle className="h-4 w-4 text-red-500" />;
      case 'info': return <Bell className="h-4 w-4 text-blue-500" />;
      case 'success': return <Activity className="h-4 w-4 text-green-500" />;
      default: return <Bell className="h-4 w-4" />;
    }
  };

  const getAlertVariant = (type) => {
    switch (type) {
      case 'warning': return 'default';
      case 'error': return 'destructive';
      case 'info': return 'default';
      case 'success': return 'default';
      default: return 'default';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 p-6" dir="rtl">
      {/* Header */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              🌱 لوحة تحكم Gaara AI
            </h1>
            <p className="text-gray-600">
              نظام إدارة الزراعة الذكية - آخر تحديث: {dashboardData.lastUpdate}
            </p>
          </div>
          <div className="flex items-center gap-4">
            <Badge variant={isOnline ? "default" : "destructive"} className="flex items-center gap-2">
              {isOnline ? <Wifi className="h-4 w-4" /> : <WifiOff className="h-4 w-4" />}
              {isOnline ? 'متصل' : 'غير متصل'}
            </Badge>
            <Button 
              onClick={handleRefreshData} 
              disabled={isLoading}
              className="flex items-center gap-2"
            >
              <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
              تحديث البيانات
            </Button>
          </div>
        </div>
      </div>

      {/* إحصائيات سريعة */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card className="bg-gradient-to-r from-green-500 to-green-600 text-white">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">إجمالي المزارع</CardTitle>
            <Leaf className="h-4 w-4" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{dashboardData.totalFarms}</div>
            <p className="text-xs opacity-80">+2 منذ الشهر الماضي</p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-r from-blue-500 to-blue-600 text-white">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">إجمالي المحاصيل</CardTitle>
            <Package className="h-4 w-4" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{dashboardData.totalCrops}</div>
            <p className="text-xs opacity-80">+15 منذ الأسبوع الماضي</p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-r from-yellow-500 to-orange-500 text-white">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">التنبيهات النشطة</CardTitle>
            <AlertTriangle className="h-4 w-4" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{dashboardData.activeAlerts}</div>
            <p className="text-xs opacity-80">-3 منذ أمس</p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-r from-purple-500 to-pink-500 text-white">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">الإيرادات</CardTitle>
            <DollarSign className="h-4 w-4" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {dashboardData.totalRevenue.toLocaleString('ar-SA')} ر.س
            </div>
            <p className="text-xs opacity-80">+12% منذ الشهر الماضي</p>
          </CardContent>
        </Card>
      </div>

      {/* المحتوى الرئيسي */}
      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">نظرة عامة</TabsTrigger>
          <TabsTrigger value="production">الإنتاج</TabsTrigger>
          <TabsTrigger value="weather">الطقس</TabsTrigger>
          <TabsTrigger value="alerts">التنبيهات</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* رسم بياني للإنتاج */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  الإنتاج الشهري
                </CardTitle>
                <CardDescription>
                  مقارنة الإنتاج الفعلي مع المستهدف
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={farmProductionData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="production" fill="#8884d8" name="الإنتاج الفعلي" />
                    <Bar dataKey="target" fill="#82ca9d" name="المستهدف" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* توزيع المحاصيل */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Leaf className="h-5 w-5" />
                  توزيع المحاصيل
                </CardTitle>
                <CardDescription>
                  نسبة كل نوع محصول من إجمالي المساحة المزروعة
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={cropDistributionData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {cropDistributionData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* حالة البيئة */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="h-5 w-5" />
                حالة البيئة الحالية
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="flex items-center justify-center mb-2">
                    <Droplets className="h-8 w-8 text-blue-500" />
                  </div>
                  <h3 className="font-semibold mb-1">رطوبة التربة</h3>
                  <div className="text-2xl font-bold text-blue-600 mb-2">
                    {Math.round(dashboardData.soilMoisture)}%
                  </div>
                  <Progress value={dashboardData.soilMoisture} className="w-full" />
                </div>

                <div className="text-center">
                  <div className="flex items-center justify-center mb-2">
                    <Thermometer className="h-8 w-8 text-red-500" />
                  </div>
                  <h3 className="font-semibold mb-1">درجة الحرارة</h3>
                  <div className="text-2xl font-bold text-red-600 mb-2">
                    {Math.round(dashboardData.temperature)}°م
                  </div>
                  <Progress value={(dashboardData.temperature / 50) * 100} className="w-full" />
                </div>

                <div className="text-center">
                  <div className="flex items-center justify-center mb-2">
                    <Sun className="h-8 w-8 text-yellow-500" />
                  </div>
                  <h3 className="font-semibold mb-1">الرطوبة النسبية</h3>
                  <div className="text-2xl font-bold text-yellow-600 mb-2">
                    {Math.round(dashboardData.humidity)}%
                  </div>
                  <Progress value={dashboardData.humidity} className="w-full" />
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="production" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>تحليل الإنتاجية المفصل</CardTitle>
              <CardDescription>
                تتبع الأداء والكفاءة عبر الوقت
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={farmProductionData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="production" stroke="#8884d8" name="الإنتاج" />
                  <Line type="monotone" dataKey="efficiency" stroke="#82ca9d" name="الكفاءة %" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="weather" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sun className="h-5 w-5" />
                توقعات الطقس لـ 7 أيام
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={weatherData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="day" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Area type="monotone" dataKey="temp" stackId="1" stroke="#8884d8" fill="#8884d8" name="درجة الحرارة" />
                  <Area type="monotone" dataKey="humidity" stackId="2" stroke="#82ca9d" fill="#82ca9d" name="الرطوبة" />
                  <Area type="monotone" dataKey="rainfall" stackId="3" stroke="#ffc658" fill="#ffc658" name="الأمطار" />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="alerts" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Bell className="h-5 w-5" />
                التنبيهات والإشعارات
              </CardTitle>
              <CardDescription>
                آخر التنبيهات والتحديثات المهمة
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {alerts.map((alert) => (
                  <Alert key={alert.id} variant={getAlertVariant(alert.type)}>
                    <div className="flex items-start gap-3">
                      {getAlertIcon(alert.type)}
                      <div className="flex-1">
                        <AlertTitle className="mb-1">{alert.title}</AlertTitle>
                        <AlertDescription className="mb-2">
                          {alert.description}
                        </AlertDescription>
                        <div className="flex items-center justify-between">
                          <span className="text-xs text-gray-500">{alert.time}</span>
                          <div className="flex gap-2">
                            <Button size="sm" variant="outline">
                              <Eye className="h-3 w-3 mr-1" />
                              عرض
                            </Button>
                            <Button size="sm" variant="outline">
                              <Edit className="h-3 w-3 mr-1" />
                              تعديل
                            </Button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </Alert>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* أزرار الإجراءات السريعة */}
      <div className="fixed bottom-6 left-6 flex flex-col gap-3">
        <Button size="lg" className="rounded-full shadow-lg">
          <Plus className="h-5 w-5 mr-2" />
          إضافة مزرعة جديدة
        </Button>
        <Button size="lg" variant="outline" className="rounded-full shadow-lg">
          <Download className="h-5 w-5 mr-2" />
          تصدير التقرير
        </Button>
        <Button size="lg" variant="outline" className="rounded-full shadow-lg">
          <Settings className="h-5 w-5 mr-2" />
          الإعدادات
        </Button>
      </div>
    </div>
  );
};

export default EnhancedDashboard;
