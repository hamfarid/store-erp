/**
 * Reports Page
 */

import React, { useState } from 'react';
import {
  BarChart3, PieChart, TrendingUp, TrendingDown, DollarSign,
  Calendar, Download, RefreshCw, FileText, ShoppingCart,
  Package, Users, ArrowUpRight, ArrowDownRight
} from 'lucide-react';
import Button from '../components/ui/ModernButton';

const ReportCard = ({ title, description, icon: Icon, color, onClick }) => (
  <div
    onClick={onClick}
    className="bg-white rounded-2xl border border-gray-100 p-6 hover:shadow-xl transition-all duration-300 cursor-pointer group"
  >
    <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${color} flex items-center justify-center mb-4 shadow-lg group-hover:scale-110 transition-transform`}>
      <Icon className="text-white" size={24} />
    </div>
    <h3 className="font-bold text-gray-900 text-lg mb-2">{title}</h3>
    <p className="text-gray-500 text-sm">{description}</p>
  </div>
);

const StatCard = ({ title, value, change, isPositive, icon: Icon, color }) => (
  <div className="bg-white rounded-xl p-5 border border-gray-100">
    <div className="flex items-center justify-between mb-3">
      <div className={`w-10 h-10 rounded-xl ${color} flex items-center justify-center`}>
        <Icon className="text-white" size={18} />
      </div>
      <span className={`flex items-center gap-1 text-sm font-medium ${isPositive ? 'text-emerald-600' : 'text-rose-600'}`}>
        {isPositive ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}
        {change}%
      </span>
    </div>
    <p className="text-gray-500 text-sm mb-1">{title}</p>
    <p className="text-2xl font-bold text-gray-900">{value}</p>
  </div>
);

const ReportsPage = () => {
  const [dateRange, setDateRange] = useState('month');

  const reports = [
    { title: 'تقرير المبيعات', description: 'تحليل شامل لجميع عمليات البيع', icon: ShoppingCart, color: 'from-teal-500 to-teal-600' },
    { title: 'تقرير المشتريات', description: 'ملخص طلبات الشراء من الموردين', icon: FileText, color: 'from-blue-500 to-blue-600' },
    { title: 'تقرير المخزون', description: 'حالة المخزون والمنتجات', icon: Package, color: 'from-purple-500 to-purple-600' },
    { title: 'تقرير العملاء', description: 'تحليل قاعدة العملاء', icon: Users, color: 'from-amber-500 to-amber-600' },
    { title: 'تقرير الأرباح', description: 'تحليل الربحية والهوامش', icon: TrendingUp, color: 'from-emerald-500 to-emerald-600' },
    { title: 'تقرير الضرائب', description: 'ملخص الضرائب المستحقة', icon: DollarSign, color: 'from-rose-500 to-rose-600' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 p-8" dir="rtl">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">التقارير</h1>
          <p className="text-gray-500">تحليلات وإحصائيات شاملة</p>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value)}
            className="px-4 py-2.5 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500"
          >
            <option value="today">اليوم</option>
            <option value="week">هذا الأسبوع</option>
            <option value="month">هذا الشهر</option>
            <option value="quarter">هذا الربع</option>
            <option value="year">هذا العام</option>
          </select>
          <Button variant="secondary" icon={Download}>تصدير</Button>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="stats-grid">
        <StatCard title="إجمالي المبيعات" value="1.2M ر.س" change={12.5} isPositive={true} icon={DollarSign} color="bg-teal-500" />
        <StatCard title="الطلبات" value="1,284" change={8.2} isPositive={true} icon={ShoppingCart} color="bg-blue-500" />
        <StatCard title="صافي الربح" value="245K ر.س" change={5.3} isPositive={true} icon={TrendingUp} color="bg-emerald-500" />
        <StatCard title="المصروفات" value="85K ر.س" change={3.1} isPositive={false} icon={TrendingDown} color="bg-rose-500" />
      </div>

      {/* Charts Section */}
      <div className="grid-container grid-2 mb-8">
        <div className="card-standard">
          <div className="card-header">
            <h2 className="card-title">المبيعات الشهرية</h2>
            <button className="p-2 hover:bg-gray-100 rounded-lg">
              <RefreshCw size={18} className="text-gray-500" />
            </button>
          </div>
          <div className="card-content">
            <div className="h-64 bg-gradient-to-br from-teal-50 to-teal-100 rounded-xl flex items-center justify-center">
              <div className="text-center">
                <BarChart3 size={48} className="text-teal-300 mx-auto mb-2" />
                <p className="text-teal-600 font-medium">رسم بياني للمبيعات</p>
              </div>
            </div>
          </div>
        </div>

        <div className="card-standard">
          <div className="card-header">
            <h2 className="card-title">توزيع المبيعات حسب الفئة</h2>
            <button className="p-2 hover:bg-gray-100 rounded-lg">
              <RefreshCw size={18} className="text-gray-500" />
            </button>
          </div>
          <div className="card-content">
            <div className="h-64 bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl flex items-center justify-center">
              <div className="text-center">
                <PieChart size={48} className="text-purple-300 mx-auto mb-2" />
                <p className="text-purple-600 font-medium">رسم دائري للفئات</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Reports Grid */}
      <div className="mb-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">التقارير المتاحة</h2>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {reports.map((report, index) => (
          <ReportCard
            key={index}
            {...report}
            onClick={() => console.log('Open report:', report.title)}
          />
        ))}
      </div>
    </div>
  );
};

export default ReportsPage;
