import React, { useState, useEffect } from 'react';
import {
  FileText, RefreshCw, TrendingDown, Calendar, TrendingUp, BarChart3, PieChart,
  Search, Filter, Download, Eye, Plus, Edit, Trash2
} from 'lucide-react';
import { toast } from 'react-hot-toast';

const ComprehensiveReports = () => {
  const [reports, setReports] = useState([]);
  const [filteredReports, setFilteredReports] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState('all');
  const [filterPeriod, setFilterPeriod] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [selectedReport, setSelectedReport] = useState(null);

  // Sample data
  const sampleReports = [
    {
      id: 1,
      name: 'تقرير المبيعات الشامل',
      category: 'sales',
      description: 'تقرير شامل عن المبيعات والأرباح والعملاء',
      period: 'monthly',
      lastGenerated: '2024-01-15T10:00:00',
      status: 'ready',
      fileSize: '2.5 MB',
      format: 'PDF',
      parameters: {
        dateFrom: '2024-01-01',
        dateTo: '2024-01-31',
        includeCharts: true,
        includeDetails: true
      },
      metrics: {
        totalSales: 150000,
        totalOrders: 85,
        avgOrderValue: 1764,
        topCustomers: 15
      }
    },
    {
      id: 2,
      name: 'تقرير المخزون التفصيلي',
      category: 'inventory',
      description: 'تقرير مفصل عن حالة المخزون والحركات',
      period: 'weekly',
      lastGenerated: '2024-01-14T14:30:00',
      status: 'ready',
      fileSize: '1.8 MB',
      format: 'Excel',
      parameters: {
        warehouse: 'all',
        includeMovements: true,
        includeValuation: true
      },
      metrics: {
        totalItems: 245,
        totalValue: 850000,
        lowStockItems: 12,
        outOfStockItems: 3
      }
    },
    {
      id: 3,
      name: 'تقرير المشتريات والموردين',
      category: 'purchases',
      description: 'تحليل شامل للمشتريات وأداء الموردين',
      period: 'monthly',
      lastGenerated: '2024-01-13T11:00:00',
      status: 'generating',
      fileSize: null,
      format: 'PDF',
      parameters: {
        dateFrom: '2024-01-01',
        dateTo: '2024-01-31',
        includeSupplierAnalysis: true
      },
      metrics: {
        totalPurchases: 95000,
        totalOrders: 42,
        activeSuppliers: 18,
        avgDeliveryTime: 5.2
      }
    },
    {
      id: 4,
      name: 'التقرير المالي الموحد',
      category: 'financial',
      description: 'تقرير مالي شامل يتضمن الأرباح والخسائر والتدفقات النقدية',
      period: 'quarterly',
      lastGenerated: '2024-01-12T08:00:00',
      status: 'ready',
      fileSize: '3.2 MB',
      format: 'PDF',
      parameters: {
        quarter: 'Q1-2024',
        includeComparisons: true,
        includeProjections: true
      },
      metrics: {
        totalRevenue: 180000,
        totalExpenses: 125000,
        netProfit: 55000,
        profitMargin: 30.6
      }
    },
    {
      id: 5,
      name: 'تقرير أداء العملاء',
      category: 'customers',
      description: 'تحليل مفصل لسلوك العملاء وأنماط الشراء',
      period: 'monthly',
      lastGenerated: '2024-01-11T16:00:00',
      status: 'ready',
      fileSize: '1.5 MB',
      format: 'Excel',
      parameters: {
        segmentation: 'value',
        includeRetention: true,
        includePredictions: true
      },
      metrics: {
        totalCustomers: 156,
        activeCustomers: 89,
        newCustomers: 23,
        retentionRate: 78.5
      }
    },
    {
      id: 6,
      name: 'تقرير الموظفين والإنتاجية',
      category: 'hr',
      description: 'تقرير عن أداء الموظفين ومؤشرات الإنتاجية',
      period: 'monthly',
      lastGenerated: '2024-01-10T12:00:00',
      status: 'error',
      fileSize: null,
      format: 'PDF',
      parameters: {
        department: 'all',
        includeAttendance: true,
        includePerformance: true
      },
      metrics: {
        totalEmployees: 25,
        attendanceRate: 94.2,
        avgProductivity: 87.5,
        trainingHours: 120
      }
    }
  ];

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setReports(sampleReports);
      setFilteredReports(sampleReports);
      setIsLoading(false);
    }, 1000);
  }, []);

  useEffect(() => {
    let filtered = reports;

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(report =>
        report.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        report.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Filter by category
    if (filterCategory !== 'all') {
      filtered = filtered.filter(report => report.category === filterCategory);
    }

    // Filter by period
    if (filterPeriod !== 'all') {
      filtered = filtered.filter(report => report.period === filterPeriod);
    }

    setFilteredReports(filtered);
  }, [reports, searchTerm, filterCategory, filterPeriod]);

  const getStatusBadge = (status) => {
    const statusConfig = {
      ready: { label: 'جاهز', variant: 'default', icon: FileText, color: 'text-primary' },
      generating: { label: 'قيد الإنشاء', variant: 'secondary', icon: RefreshCw, color: 'text-primary' },
      error: { label: 'خطأ', variant: 'destructive', icon: TrendingDown, color: 'text-destructive' },
      scheduled: { label: 'مجدول', variant: 'outline', icon: Calendar, color: 'text-accent' }
    };

    const config = statusConfig[status] || statusConfig.ready;
    const IconComponent = config.icon;
    
    return (
      <Badge variant={config.variant} className="flex items-center gap-1">
        <IconComponent className="w-3 h-3" />
        {config.label}
      </Badge>
    );
  };

  const getCategoryLabel = (category) => {
    const categories = {
      sales: 'المبيعات',
      inventory: 'المخزون',
      purchases: 'المشتريات',
      financial: 'المالية',
      customers: 'العملاء',
      hr: 'الموارد البشرية'
    };
    return categories[category] || category;
  };

  const getCategoryBadge = (category) => {
    const categoryConfig = {
      sales: { label: 'المبيعات', variant: 'default', icon: TrendingUp },
      inventory: { label: 'المخزون', variant: 'secondary', icon: BarChart3 },
      purchases: { label: 'المشتريات', variant: 'outline', icon: TrendingDown },
      financial: { label: 'المالية', variant: 'default', icon: PieChart },
      customers: { label: 'العملاء', variant: 'secondary', icon: TrendingUp },
      hr: { label: 'الموارد البشرية', variant: 'outline', icon: BarChart3 }
    };

    const config = categoryConfig[category] || categoryConfig.sales;
    const IconComponent = config.icon;
    
    return (
      <Badge variant={config.variant} className="flex items-center gap-1">
        <IconComponent className="w-3 h-3" />
        {config.label}
      </Badge>
    );
  };

  const getPeriodLabel = (period) => {
    const periods = {
      daily: 'يومي',
      weekly: 'أسبوعي',
      monthly: 'شهري',
      quarterly: 'ربع سنوي',
      yearly: 'سنوي'
    };
    return periods[period] || period;
  };

  const handleGenerateReport = (reportId) => {
    setReports(reports.map(report =>
      report.id === reportId
        ? { 
            ...report, 
            status: 'generating',
            lastGenerated: new Date().toISOString()
          }
        : report
    ));
    
    // Simulate report generation
    setTimeout(() => {
      setReports(reports.map(report =>
        report.id === reportId
          ? { 
              ...report, 
              status: 'ready',
              fileSize: '2.1 MB'
            }
          : report
      ));
      toast.success('تم إنشاء التقرير بنجاح');
    }, 3000);
    
    toast.info('جاري إنشاء التقرير...');
  };

  const handleDownloadReport = (report) => {
    if (report.status === 'ready') {
      toast.success(`تم تحميل ${report.name}`);
    } else {
      toast.error('التقرير غير جاهز للتحميل');
    }
  };

  const handleViewReport = (report) => {
    if (report.status === 'ready') {
      setSelectedReport(report);
      toast.success(`تم فتح ${report.name}`);
    } else {
      toast.error('التقرير غير جاهز للعرض');
    }
  };

  const handlePrintReport = (report) => {
    if (report.status === 'ready') {
      toast.success(`تم إرسال ${report.name} للطباعة`);
    } else {
      toast.error('التقرير غير جاهز للطباعة');
    }
  };

  const handleEmailReport = (report) => {
    if (report.status === 'ready') {
      toast.success(`تم إرسال ${report.name} بالبريد الإلكتروني`);
    } else {
      toast.error('التقرير غير جاهز للإرسال');
    }
  };

  const getStatusCounts = () => {
    return {
      total: reports.length,
      ready: reports.filter(r => r.status === 'ready').length,
      generating: reports.filter(r => r.status === 'generating').length,
      error: reports.filter(r => r.status === 'error').length
    };
  };

  const statusCounts = getStatusCounts();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل التقارير الشاملة...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">التقارير الشاملة</h1>
          <p className="text-muted-foreground mt-1">تقارير تفصيلية وتحليلات شاملة للنظام</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <RefreshCw className="w-4 h-4 mr-2" />
            تحديث الكل
          </Button>
        </div>
      </div>

      {/* Status Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي التقارير</p>
                <p className="text-2xl font-bold text-primary">{statusCounts.total}</p>
              </div>
              <FileText className="w-8 h-8 text-primary/100" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">جاهزة</p>
                <p className="text-2xl font-bold text-primary">{statusCounts.ready}</p>
              </div>
              <FileText className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">قيد الإنشاء</p>
                <p className="text-2xl font-bold text-primary">{statusCounts.generating}</p>
              </div>
              <RefreshCw className="w-8 h-8 text-primary/100" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">أخطاء</p>
                <p className="text-2xl font-bold text-destructive">{statusCounts.error}</p>
              </div>
              <TrendingDown className="w-8 h-8 text-red-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-wrap gap-4">
            <div className="flex-1 min-w-64">
              <Label htmlFor="search">البحث</Label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  id="search"
                  placeholder="البحث في أسماء التقارير والأوصاف..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>

            <div className="min-w-48">
              <Label htmlFor="category-filter">الفئة</Label>
              <Select value={filterCategory} onValueChange={setFilterCategory}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر الفئة" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع الفئات</SelectItem>
                  <SelectItem value="sales">المبيعات</SelectItem>
                  <SelectItem value="inventory">المخزون</SelectItem>
                  <SelectItem value="purchases">المشتريات</SelectItem>
                  <SelectItem value="financial">المالية</SelectItem>
                  <SelectItem value="customers">العملاء</SelectItem>
                  <SelectItem value="hr">الموارد البشرية</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="min-w-48">
              <Label htmlFor="period-filter">الفترة</Label>
              <Select value={filterPeriod} onValueChange={setFilterPeriod}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر الفترة" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع الفترات</SelectItem>
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

      {/* Reports Table */}
      <Card>
        <CardHeader>
          <CardTitle>قائمة التقارير ({filteredReports.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>اسم التقرير</TableHead>
                  <TableHead>الفئة</TableHead>
                  <TableHead>الفترة</TableHead>
                  <TableHead>آخر إنشاء</TableHead>
                  <TableHead>الحالة</TableHead>
                  <TableHead>حجم الملف</TableHead>
                  <TableHead>التنسيق</TableHead>
                  <TableHead>الإجراءات</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredReports.map((report) => (
                  <TableRow key={report.id}>
                    <TableCell>
                      <div>
                        <div className="font-medium">{report.name}</div>
                        <div className="text-sm text-gray-500">{report.description}</div>
                      </div>
                    </TableCell>
                    <TableCell>
                      {getCategoryBadge(report.category)}
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">
                        {getPeriodLabel(report.period)}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-1">
                        <Calendar className="w-3 h-3 text-gray-500" />
                        <span className="text-sm">
                          {new Date(report.lastGenerated).toLocaleDateString('ar-SA')}
                        </span>
                      </div>
                    </TableCell>
                    <TableCell>
                      {getStatusBadge(report.status)}
                    </TableCell>
                    <TableCell>
                      <span className="text-sm">
                        {report.fileSize || '-'}
                      </span>
                    </TableCell>
                    <TableCell>
                      <Badge variant="secondary">
                        {report.format}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-1">
                        {report.status === 'ready' ? (
                          <>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleViewReport(report)}
                            >
                              <Eye className="w-4 h-4" />
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleDownloadReport(report)}
                            >
                              <Download className="w-4 h-4" />
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handlePrintReport(report)}
                            >
                              <Printer className="w-4 h-4" />
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleEmailReport(report)}
                            >
                              <Mail className="w-4 h-4" />
                            </Button>
                          </>
                        ) : (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleGenerateReport(report.id)}
                            disabled={report.status === 'generating'}
                          >
                            <RefreshCw className={`w-4 h-4 ${report.status === 'generating' ? 'animate-spin' : ''}`} />
                          </Button>
                        )}
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>

          {filteredReports.length === 0 && (
            <div className="text-center py-8">
              <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">لا توجد تقارير تطابق معايير البحث</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default ComprehensiveReports;

