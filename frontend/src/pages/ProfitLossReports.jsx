import React, { useState, useEffect } from 'react';
import {
  TrendingUp, TrendingDown, DollarSign, Search, Download, Calendar,
  BarChart3, PieChart, FileText, RefreshCw, ArrowUpRight, ArrowDownRight
} from 'lucide-react';
import { toast } from 'react-hot-toast';
import apiClient from '../services/apiClient';

// UI Components
import { Badge } from '../components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow
} from '../components/ui/table';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue
} from '../components/ui/select';

/**
 * تقارير الأرباح والخسائر
 * Profit & Loss Reports Page
 */
const ProfitLossReports = () => {
  const [reportData, setReportData] = useState(null);
  const [dateFrom, setDateFrom] = useState('2024-01-01');
  const [dateTo, setDateTo] = useState('2024-01-31');
  const [period, setPeriod] = useState('monthly');
  const [isLoading, setIsLoading] = useState(true);

  // بيانات نموذجية
  const sampleReportData = {
    summary: {
      totalRevenue: 250000,
      totalCosts: 180000,
      grossProfit: 70000,
      operatingExpenses: 25000,
      netProfit: 45000,
      profitMargin: 18.0,
      revenueGrowth: 12.5,
      costReduction: 3.2
    },
    revenue: {
      sales: 220000,
      services: 20000,
      other: 10000
    },
    costs: {
      costOfGoodsSold: 150000,
      shipping: 15000,
      returns: 5000,
      discounts: 10000
    },
    expenses: {
      salaries: 12000,
      rent: 5000,
      utilities: 2000,
      marketing: 3000,
      other: 3000
    },
    monthlyTrend: [
      { month: 'يناير', revenue: 250000, costs: 180000, profit: 45000 },
      { month: 'ديسمبر', revenue: 230000, costs: 170000, profit: 40000 },
      { month: 'نوفمبر', revenue: 200000, costs: 155000, profit: 32000 },
      { month: 'أكتوبر', revenue: 220000, costs: 165000, profit: 38000 },
      { month: 'سبتمبر', revenue: 195000, costs: 150000, profit: 30000 },
      { month: 'أغسطس', revenue: 210000, costs: 160000, profit: 35000 }
    ],
    categoryProfits: [
      { category: 'إلكترونيات', revenue: 120000, costs: 85000, profit: 35000, margin: 29.2 },
      { category: 'ملابس', revenue: 50000, costs: 35000, profit: 15000, margin: 30.0 },
      { category: 'أثاث', revenue: 40000, costs: 30000, profit: 10000, margin: 25.0 },
      { category: 'مستلزمات مكتبية', revenue: 25000, costs: 18000, profit: 7000, margin: 28.0 },
      { category: 'أخرى', revenue: 15000, costs: 12000, profit: 3000, margin: 20.0 }
    ]
  };

  useEffect(() => {
    fetchReportData();
  }, [dateFrom, dateTo, period]);

  const fetchReportData = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.get('/api/reports/profit-loss', {
        params: { date_from: dateFrom, date_to: dateTo, period }
      });
      if (response.status === 'success' && response.data) {
        setReportData(response.data);
      } else {
        setReportData(sampleReportData);
      }
    } catch (error) {
      console.log('Using sample data:', error);
      setReportData(sampleReportData);
    } finally {
      setIsLoading(false);
    }
  };

  const handleExport = (format) => {
    toast.success(`جاري تصدير التقرير بصيغة ${format.toUpperCase()}`);
  };

  const handleRefresh = () => {
    fetchReportData();
    toast.success('تم تحديث التقرير');
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('ar-SA', {
      style: 'currency',
      currency: 'SAR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  const formatPercent = (value) => {
    return `${value >= 0 ? '+' : ''}${value.toFixed(1)}%`;
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل التقرير...</p>
        </div>
      </div>
    );
  }

  const data = reportData || sampleReportData;

  return (
    <div className="p-6 space-y-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground flex items-center gap-2">
            <BarChart3 className="w-8 h-8" />
            تقارير الأرباح والخسائر
          </h1>
          <p className="text-muted-foreground mt-1">تحليل شامل للإيرادات والمصروفات</p>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={handleRefresh}
            className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            تحديث
          </button>
          <button 
            onClick={() => handleExport('pdf')}
            className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors"
          >
            <FileText className="w-4 h-4" />
            PDF
          </button>
          <button 
            onClick={() => handleExport('excel')}
            className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
          >
            <Download className="w-4 h-4" />
            Excel
          </button>
        </div>
      </div>

      {/* Date Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-wrap gap-4 items-end">
            <div className="min-w-40">
              <Label htmlFor="date-from">من تاريخ</Label>
              <Input
                id="date-from"
                type="date"
                value={dateFrom}
                onChange={(e) => setDateFrom(e.target.value)}
              />
            </div>
            <div className="min-w-40">
              <Label htmlFor="date-to">إلى تاريخ</Label>
              <Input
                id="date-to"
                type="date"
                value={dateTo}
                onChange={(e) => setDateTo(e.target.value)}
              />
            </div>
            <div className="min-w-40">
              <Label htmlFor="period">الفترة</Label>
              <Select value={period} onValueChange={setPeriod}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر الفترة" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="daily">يومي</SelectItem>
                  <SelectItem value="weekly">أسبوعي</SelectItem>
                  <SelectItem value="monthly">شهري</SelectItem>
                  <SelectItem value="quarterly">ربع سنوي</SelectItem>
                  <SelectItem value="yearly">سنوي</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي الإيرادات</p>
                <p className="text-2xl font-bold text-green-700 dark:text-green-400">
                  {formatCurrency(data.summary.totalRevenue)}
                </p>
                <div className="flex items-center gap-1 mt-1 text-green-600">
                  <ArrowUpRight className="w-4 h-4" />
                  <span className="text-sm">{formatPercent(data.summary.revenueGrowth)}</span>
                </div>
              </div>
              <TrendingUp className="w-10 h-10 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-red-50 to-red-100 dark:from-red-900/20 dark:to-red-800/20">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي التكاليف</p>
                <p className="text-2xl font-bold text-red-700 dark:text-red-400">
                  {formatCurrency(data.summary.totalCosts)}
                </p>
                <div className="flex items-center gap-1 mt-1 text-green-600">
                  <ArrowDownRight className="w-4 h-4" />
                  <span className="text-sm">-{data.summary.costReduction}%</span>
                </div>
              </div>
              <TrendingDown className="w-10 h-10 text-red-500" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">صافي الربح</p>
                <p className="text-2xl font-bold text-blue-700 dark:text-blue-400">
                  {formatCurrency(data.summary.netProfit)}
                </p>
                <Badge variant="default" className="mt-1">
                  هامش {data.summary.profitMargin}%
                </Badge>
              </div>
              <DollarSign className="w-10 h-10 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي الربح</p>
                <p className="text-2xl font-bold text-purple-700 dark:text-purple-400">
                  {formatCurrency(data.summary.grossProfit)}
                </p>
                <p className="text-sm text-muted-foreground mt-1">
                  قبل المصروفات التشغيلية
                </p>
              </div>
              <PieChart className="w-10 h-10 text-purple-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Revenue & Costs Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue Breakdown */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-green-500" />
              تفصيل الإيرادات
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center p-3 bg-muted/50 rounded-lg">
                <span>المبيعات</span>
                <span className="font-bold text-green-600">{formatCurrency(data.revenue.sales)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-muted/50 rounded-lg">
                <span>الخدمات</span>
                <span className="font-bold text-green-600">{formatCurrency(data.revenue.services)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-muted/50 rounded-lg">
                <span>أخرى</span>
                <span className="font-bold text-green-600">{formatCurrency(data.revenue.other)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-green-100 dark:bg-green-900/30 rounded-lg border-2 border-green-500">
                <span className="font-bold">الإجمالي</span>
                <span className="font-bold text-green-700 dark:text-green-400">
                  {formatCurrency(data.summary.totalRevenue)}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Costs Breakdown */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingDown className="w-5 h-5 text-red-500" />
              تفصيل التكاليف
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center p-3 bg-muted/50 rounded-lg">
                <span>تكلفة البضاعة المباعة</span>
                <span className="font-bold text-red-600">{formatCurrency(data.costs.costOfGoodsSold)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-muted/50 rounded-lg">
                <span>الشحن</span>
                <span className="font-bold text-red-600">{formatCurrency(data.costs.shipping)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-muted/50 rounded-lg">
                <span>المرتجعات</span>
                <span className="font-bold text-red-600">{formatCurrency(data.costs.returns)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-muted/50 rounded-lg">
                <span>الخصومات</span>
                <span className="font-bold text-red-600">{formatCurrency(data.costs.discounts)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-red-100 dark:bg-red-900/30 rounded-lg border-2 border-red-500">
                <span className="font-bold">الإجمالي</span>
                <span className="font-bold text-red-700 dark:text-red-400">
                  {formatCurrency(data.summary.totalCosts)}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Operating Expenses */}
      <Card>
        <CardHeader>
          <CardTitle>المصروفات التشغيلية</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div className="p-4 bg-muted/50 rounded-lg text-center">
              <p className="text-sm text-muted-foreground">الرواتب</p>
              <p className="text-xl font-bold">{formatCurrency(data.expenses.salaries)}</p>
            </div>
            <div className="p-4 bg-muted/50 rounded-lg text-center">
              <p className="text-sm text-muted-foreground">الإيجار</p>
              <p className="text-xl font-bold">{formatCurrency(data.expenses.rent)}</p>
            </div>
            <div className="p-4 bg-muted/50 rounded-lg text-center">
              <p className="text-sm text-muted-foreground">المرافق</p>
              <p className="text-xl font-bold">{formatCurrency(data.expenses.utilities)}</p>
            </div>
            <div className="p-4 bg-muted/50 rounded-lg text-center">
              <p className="text-sm text-muted-foreground">التسويق</p>
              <p className="text-xl font-bold">{formatCurrency(data.expenses.marketing)}</p>
            </div>
            <div className="p-4 bg-muted/50 rounded-lg text-center">
              <p className="text-sm text-muted-foreground">أخرى</p>
              <p className="text-xl font-bold">{formatCurrency(data.expenses.other)}</p>
            </div>
          </div>
          <div className="mt-4 p-4 bg-yellow-100 dark:bg-yellow-900/30 rounded-lg border-2 border-yellow-500">
            <div className="flex justify-between items-center">
              <span className="font-bold">إجمالي المصروفات التشغيلية</span>
              <span className="font-bold text-yellow-700 dark:text-yellow-400">
                {formatCurrency(data.summary.operatingExpenses)}
              </span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Monthly Trend */}
      <Card>
        <CardHeader>
          <CardTitle>الاتجاه الشهري</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>الشهر</TableHead>
                <TableHead>الإيرادات</TableHead>
                <TableHead>التكاليف</TableHead>
                <TableHead>الربح</TableHead>
                <TableHead>الهامش</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {data.monthlyTrend.map((month, index) => (
                <TableRow key={index}>
                  <TableCell className="font-medium">{month.month}</TableCell>
                  <TableCell className="text-green-600">{formatCurrency(month.revenue)}</TableCell>
                  <TableCell className="text-red-600">{formatCurrency(month.costs)}</TableCell>
                  <TableCell className="text-blue-600 font-bold">{formatCurrency(month.profit)}</TableCell>
                  <TableCell>
                    <Badge variant={month.profit > 0 ? 'default' : 'destructive'}>
                      {((month.profit / month.revenue) * 100).toFixed(1)}%
                    </Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Category Profits */}
      <Card>
        <CardHeader>
          <CardTitle>الأرباح حسب الفئة</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>الفئة</TableHead>
                <TableHead>الإيرادات</TableHead>
                <TableHead>التكاليف</TableHead>
                <TableHead>الربح</TableHead>
                <TableHead>هامش الربح</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {data.categoryProfits.map((cat, index) => (
                <TableRow key={index}>
                  <TableCell className="font-medium">{cat.category}</TableCell>
                  <TableCell className="text-green-600">{formatCurrency(cat.revenue)}</TableCell>
                  <TableCell className="text-red-600">{formatCurrency(cat.costs)}</TableCell>
                  <TableCell className="text-blue-600 font-bold">{formatCurrency(cat.profit)}</TableCell>
                  <TableCell>
                    <Badge variant={cat.margin >= 25 ? 'default' : 'secondary'}>
                      {cat.margin.toFixed(1)}%
                    </Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};

export default ProfitLossReports;

