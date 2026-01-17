/**
 * Store ERP - Modern Dashboard
 * 
 * A beautiful, professional dashboard with:
 * - Real-time statistics cards
 * - Interactive charts
 * - Low stock alerts
 * - Recent activity feed
 * - Quick actions
 * 
 * Uses Design System tokens for consistent styling
 */

import React, { useState, useEffect } from 'react';
import {
  Calendar,
  DollarSign,
  Users,
  Package,
  BarChart3,
  TrendingUp,
  TrendingDown,
  Truck,
  RefreshCw,
  AlertTriangle,
  Activity,
  ShoppingCart,
  ArrowUpRight,
  ArrowDownRight,
  Plus,
  Eye
} from 'lucide-react';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  LineChart,
  BarChart,
  Bar,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Line,
  Cell,
  Legend
} from 'recharts';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card';
import { Button } from './ui/button';
import './DashboardNew.css';

const DashboardNew = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    total_products: 0,
    total_customers: 0,
    total_suppliers: 0,
    total_sales: 0,
    total_inventory_value: 0,
    low_stock_count: 0,
    recent_movements: 0,
    monthly_revenue: 0
  });

  const [salesData, setSalesData] = useState([]);
  const [categoryData, setCategoryData] = useState([]);
  const [recentActivities, setRecentActivities] = useState([]);
  const [lowStockProducts, setLowStockProducts] = useState([]);
  const [lastUpdated, setLastUpdated] = useState(null);

  // Fetch dashboard data
  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 60000); // Refresh every minute
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    
    try {
      // Try to fetch from API
      const baseUrl = 'http://127.0.0.1:8000';
      const response = await fetch(`${baseUrl}/api/dashboard/stats`);
      
      if (response.ok) {
        const data = await response.json();
        setStats(data.data);
        setLastUpdated(new Date());
      } else {
        // Use demo data
        loadDemoData();
      }
    } catch (error) {
      // Use demo data if API fails
      loadDemoData();
    } finally {
      setLoading(false);
    }
  };

  const loadDemoData = () => {
    setStats({
      total_products: 247,
      total_customers: 156,
      total_suppliers: 42,
      total_sales: 1248,
      total_inventory_value: 1850000,
      low_stock_count: 12,
      recent_movements: 89,
      monthly_revenue: 485000
    });

    setSalesData([
      { month: 'يناير', sales: 45000, orders: 120 },
      { month: 'فبراير', sales: 52000, orders: 145 },
      { month: 'مارس', sales: 48000, orders: 132 },
      { month: 'أبريل', sales: 61000, orders: 168 },
      { month: 'مايو', sales: 55000, orders: 152 },
      { month: 'يونيو', sales: 68000, orders: 189 },
      { month: 'يوليو', sales: 72000, orders: 201 }
    ]);

    setCategoryData([
      { name: 'بذور', value: 450000, color: 'var(--color-primary-500)' },
      { name: 'أسمدة', value: 380000, color: 'var(--color-secondary-500)' },
      { name: 'مبيدات', value: 320000, color: 'var(--color-success-500)' },
      { name: 'أدوات', value: 280000, color: 'var(--color-warning-500)' },
      { name: 'أخرى', value: 420000, color: 'var(--color-info-500)' }
    ]);

    setRecentActivities([
      {
        id: 1,
        type: 'sale',
        title: 'فاتورة مبيعات جديدة',
        description: 'فاتورة #1248 - 15,500 ريال',
        time: 'منذ 5 دقائق',
        icon: ShoppingCart,
        color: 'success'
      },
      {
        id: 2,
        type: 'stock',
        title: 'تنبيه مخزون منخفض',
        description: 'بذور طماطم F1 - 15 وحدة متبقية',
        time: 'منذ 15 دقيقة',
        icon: AlertTriangle,
        color: 'warning'
      },
      {
        id: 3,
        type: 'purchase',
        title: 'طلب شراء جديد',
        description: 'طلب #456 - 45,000 ريال',
        time: 'منذ 30 دقيقة',
        icon: Truck,
        color: 'info'
      },
      {
        id: 4,
        type: 'customer',
        title: 'عميل جديد',
        description: 'محمد أحمد - مزرعة الأمل',
        time: 'منذ ساعة',
        icon: Users,
        color: 'primary'
      }
    ]);

    setLowStockProducts([
      { id: 1, name: 'بذور طماطم F1', stock: 15, min_stock: 50, unit: 'كيس' },
      { id: 2, name: 'سماد NPK 20-20-20', stock: 8, min_stock: 30, unit: 'كيس' },
      { id: 3, name: 'مبيد حشري عضوي', stock: 12, min_stock: 40, unit: 'لتر' },
      { id: 4, name: 'بذور خيار هجين', stock: 20, min_stock: 60, unit: 'كيس' }
    ]);

    setLastUpdated(new Date());
  };

  // Statistics cards data
  const statsCards = [
    {
      title: 'إجمالي المبيعات',
      value: stats.monthly_revenue?.toLocaleString('ar-SA') || '0',
      suffix: 'ريال',
      change: '+12.5%',
      changeType: 'increase',
      icon: DollarSign,
      color: 'primary',
      description: 'هذا الشهر'
    },
    {
      title: 'عدد الطلبات',
      value: stats.total_sales?.toLocaleString('ar-SA') || '0',
      suffix: 'طلب',
      change: '+8.2%',
      changeType: 'increase',
      icon: ShoppingCart,
      color: 'success',
      description: 'إجمالي الطلبات'
    },
    {
      title: 'المنتجات',
      value: stats.total_products?.toLocaleString('ar-SA') || '0',
      suffix: 'منتج',
      change: '+5',
      changeType: 'increase',
      icon: Package,
      color: 'info',
      description: 'في المخزون'
    },
    {
      title: 'العملاء',
      value: stats.total_customers?.toLocaleString('ar-SA') || '0',
      suffix: 'عميل',
      change: '+15',
      changeType: 'increase',
      icon: Users,
      color: 'secondary',
      description: 'عملاء نشطين'
    }
  ];

  // Quick actions
  const quickActions = [
    { title: 'فاتورة جديدة', icon: Plus, color: 'primary', action: () => navigate('/pos') },
    { title: 'إضافة منتج', icon: Package, color: 'success', action: () => navigate('/products/add') },
    { title: 'طلب شراء', icon: Truck, color: 'info', action: () => navigate('/purchases/add') },
    { title: 'التقارير', icon: BarChart3, color: 'warning', action: () => navigate('/reports') }
  ];

  if (loading) {
    return (
      <div className="dashboard-loading">
        <RefreshCw className="dashboard-loading__icon" />
        <p>جاري تحميل البيانات...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {/* Header */}
      <div className="dashboard__header">
        <div>
          <h1 className="dashboard__title">لوحة التحكم</h1>
          <p className="dashboard__subtitle">
            مرحباً بك في نظام إدارة المتجر
            {lastUpdated && (
              <span className="dashboard__last-updated">
                آخر تحديث: {lastUpdated.toLocaleTimeString('ar-SA')}
              </span>
            )}
          </p>
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={fetchDashboardData}
          className="dashboard__refresh-btn"
        >
          <RefreshCw size={16} />
          تحديث
        </Button>
      </div>

      {/* Statistics Cards */}
      <div className="dashboard__stats">
        {statsCards.map((card, index) => (
          <Card key={index} className="stat-card">
            <CardContent className="stat-card__content">
              <div className="stat-card__header">
                <div className={`stat-card__icon stat-card__icon--${card.color}`}>
                  <card.icon size={24} />
                </div>
                <div className={`stat-card__change stat-card__change--${card.changeType}`}>
                  {card.changeType === 'increase' ? (
                    <TrendingUp size={16} />
                  ) : (
                    <TrendingDown size={16} />
                  )}
                  <span>{card.change}</span>
                </div>
              </div>
              <div className="stat-card__body">
                <p className="stat-card__title">{card.title}</p>
                <div className="stat-card__value">
                  <span className="stat-card__number">{card.value}</span>
                  <span className="stat-card__suffix">{card.suffix}</span>
                </div>
                <p className="stat-card__description">{card.description}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="dashboard__quick-actions">
        <h2 className="dashboard__section-title">إجراءات سريعة</h2>
        <div className="quick-actions">
          {quickActions.map((action, index) => (
            <button
              key={index}
              className={`quick-action quick-action--${action.color}`}
              onClick={action.action}
            >
              <action.icon size={24} />
              <span>{action.title}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Charts Row */}
      <div className="dashboard__charts">
        {/* Sales Chart */}
        <Card className="dashboard__chart-card">
          <CardHeader>
            <CardTitle>المبيعات الشهرية</CardTitle>
            <CardDescription>تطور المبيعات خلال آخر 7 أشهر</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={salesData}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-light)" />
                <XAxis dataKey="month" stroke="var(--color-text-secondary)" />
                <YAxis stroke="var(--color-text-secondary)" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'var(--color-bg-primary)',
                    border: '1px solid var(--color-border-light)',
                    borderRadius: 'var(--radius-md)'
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="sales"
                  stroke="var(--color-primary-600)"
                  strokeWidth={3}
                  dot={{ fill: 'var(--color-primary-600)', r: 5 }}
                  activeDot={{ r: 7 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Category Distribution */}
        <Card className="dashboard__chart-card">
          <CardHeader>
            <CardTitle>توزيع الفئات</CardTitle>
            <CardDescription>قيمة المخزون حسب الفئة</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={categoryData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="var(--color-primary-500)"
                  dataKey="value"
                >
                  {categoryData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'var(--color-bg-primary)',
                    border: '1px solid var(--color-border-light)',
                    borderRadius: 'var(--radius-md)'
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Bottom Row */}
      <div className="dashboard__bottom">
        {/* Recent Activities */}
        <Card className="dashboard__activities">
          <CardHeader>
            <CardTitle>النشاطات الأخيرة</CardTitle>
            <CardDescription>آخر الأحداث في النظام</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="activities-list">
              {recentActivities.map((activity) => (
                <div key={activity.id} className="activity-item">
                  <div className={`activity-item__icon activity-item__icon--${activity.color}`}>
                    <activity.icon size={20} />
                  </div>
                  <div className="activity-item__content">
                    <p className="activity-item__title">{activity.title}</p>
                    <p className="activity-item__description">{activity.description}</p>
                  </div>
                  <span className="activity-item__time">{activity.time}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Low Stock Alert */}
        <Card className="dashboard__low-stock">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle size={20} className="text-warning" />
              تنبيه مخزون منخفض
            </CardTitle>
            <CardDescription>منتجات تحتاج إلى إعادة طلب</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="low-stock-list">
              {lowStockProducts.map((product) => (
                <div key={product.id} className="low-stock-item">
                  <div className="low-stock-item__info">
                    <p className="low-stock-item__name">{product.name}</p>
                    <div className="low-stock-item__stock">
                      <span className="low-stock-item__current">{product.stock}</span>
                      <span className="low-stock-item__separator">/</span>
                      <span className="low-stock-item__min">{product.min_stock}</span>
                      <span className="low-stock-item__unit">{product.unit}</span>
                    </div>
                  </div>
                  <div className="low-stock-item__progress">
                    <div
                      className="low-stock-item__progress-bar"
                      style={{ width: `${(product.stock / product.min_stock) * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
            <Button
              variant="ghost"
              size="sm"
              fullWidth
              className="mt-4"
              onClick={() => navigate('/products?filter=low-stock')}
            >
              عرض جميع المنتجات
              <ArrowUpRight size={16} />
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default DashboardNew;
