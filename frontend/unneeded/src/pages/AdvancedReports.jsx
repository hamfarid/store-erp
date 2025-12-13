import React, { useState, useEffect } from 'react';
import {
  CheckCircle, Clock, AlertTriangle, Calendar, DollarSign, Users, Truck, TrendingUp, Target,
  Search, Filter, Download, Eye, BarChart3, FileText, RefreshCw
} from 'lucide-react';
import { toast } from 'react-hot-toast';

const AdvancedReports = () => {
  const [reports, setReports] = useState([]);
  const [filteredReports, setFilteredReports] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState('all');
  const [filterComplexity, setFilterComplexity] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [selectedReport, setSelectedReport] = useState(null);

  // Sample advanced reports data
  const sampleReports = [
    {
      id: 1,
      name: 'تحليل الربحية حسب المنتج',
      category: 'profitability',
      complexity: 'advanced',
      description: 'تحليل مفصل للربحية على مستوى المنتج مع مقارنات زمنية',
      estimatedTime: '5-10 دقائق',
      dataPoints: 15000,
      lastGenerated: '2024-01-15T10:00:00',
      status: 'ready',
      insights: [
        'أعلى 10 منتجات ربحية',
        'تحليل هامش الربح',
        'اتجاهات الربحية الشهرية',
        'مقارنة الأداء السنوي'
      ],
      metrics: {
        totalProducts: 245,
        profitableProducts: 198,
        avgProfitMargin: 28.5,
        topProductProfit: 45000
      }
    },
    {
      id: 2,
      name: 'تحليل سلوك العملاء المتقدم',
      category: 'customer_behavior',
      complexity: 'expert',
      description: 'تحليل عميق لأنماط شراء العملاء وتوقع السلوك المستقبلي',
      estimatedTime: '10-15 دقائق',
      dataPoints: 25000,
      lastGenerated: '2024-01-14T14:30:00',
      status: 'generating',
      insights: [
        'تجميع العملاء حسب القيمة',
        'تحليل دورة حياة العميل',
        'توقع معدل الاحتفاظ',
        'أنماط الشراء الموسمية'
      ],
      metrics: {
        totalCustomers: 1250,
        activeCustomers: 890,
        avgLifetimeValue: 15600,
        retentionRate: 78.5
      }
    },
    {
      id: 3,
      name: 'تحليل سلسلة التوريد',
      category: 'supply_chain',
      complexity: 'advanced',
      description: 'تحليل شامل لكفاءة سلسلة التوريد وأداء الموردين',
      estimatedTime: '7-12 دقائق',
      dataPoints: 18000,
      lastGenerated: '2024-01-13T11:00:00',
      status: 'ready',
      insights: [
        'تقييم أداء الموردين',
        'تحليل أوقات التسليم',
        'تحسين مستويات المخزون',
        'تحليل التكاليف اللوجستية'
      ],
      metrics: {
        totalSuppliers: 45,
        avgDeliveryTime: 5.2,
        onTimeDeliveryRate: 92.3,
        supplyCost: 125000
      }
    },
    {
      id: 4,
      name: 'تحليل المخاطر المالية',
      category: 'risk_analysis',
      complexity: 'expert',
      description: 'تقييم شامل للمخاطر المالية وتحليل السيناريوهات',
      estimatedTime: '15-20 دقائق',
      dataPoints: 30000,
      lastGenerated: '2024-01-12T08:00:00',
      status: 'ready',
      insights: [
        'تحليل مخاطر السيولة',
        'تقييم مخاطر الائتمان',
        'تحليل الحساسية',
        'نمذجة السيناريوهات'
      ],
      metrics: {
        riskScore: 3.2,
        liquidityRatio: 1.8,
        creditRisk: 'منخفض',
        stressTestResult: 'مقبول'
      }
    },
    {
      id: 5,
      name: 'تحليل الاتجاهات والتنبؤات',
      category: 'forecasting',
      complexity: 'expert',
      description: 'تحليل الاتجاهات التاريخية والتنبؤ بالطلب المستقبلي',
      estimatedTime: '12-18 دقائق',
      dataPoints: 35000,
      lastGenerated: '2024-01-11T16:00:00',
      status: 'error',
      insights: [
        'تنبؤ الطلب الشهري',
        'تحليل الموسمية',
        'اتجاهات السوق',
        'توقعات النمو'
      ],
      metrics: {
        forecastAccuracy: 87.5,
        seasonalityIndex: 1.3,
        growthRate: 12.8,
        demandVariability: 'متوسط'
      }
    },
    {
      id: 6,
      name: 'تحليل الأداء التشغيلي',
      category: 'operational',
      complexity: 'advanced',
      description: 'تقييم شامل للكفاءة التشغيلية ومؤشرات الأداء الرئيسية',
      estimatedTime: '8-12 دقائق',
      dataPoints: 20000,
      lastGenerated: '2024-01-10T12:00:00',
      status: 'ready',
      insights: [
        'كفاءة العمليات',
        'معدلات الإنتاجية',
        'تحليل الاختناقات',
        'تحسين الموارد'
      ],
      metrics: {
        operationalEfficiency: 89.2,
        productivityRate: 94.5,
        resourceUtilization: 87.8,
        processOptimization: 'عالي'
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
        report.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        report.insights.some(insight => insight.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    // Filter by category
    if (filterCategory !== 'all') {
      filtered = filtered.filter(report => report.category === filterCategory);
    }

    // Filter by complexity
    if (filterComplexity !== 'all') {
      filtered = filtered.filter(report => report.complexity === filterComplexity);
    }

    setFilteredReports(filtered);
  }, [reports, searchTerm, filterCategory, filterComplexity]);

  const getStatusBadge = (status) => {
    const statusConfig = {
      ready: { label: 'جاهز', variant: 'default', icon: CheckCircle, color: 'text-primary' },
      generating: { label: 'قيد الإنشاء', variant: 'secondary', icon: Clock, color: 'text-primary' },
      error: { label: 'خطأ', variant: 'destructive', icon: AlertTriangle, color: 'text-destructive' },
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
      profitability: 'الربحية',
      customer_behavior: 'سلوك العملاء',
      supply_chain: 'سلسلة التوريد',
      risk_analysis: 'تحليل المخاطر',
      forecasting: 'التنبؤات',
      operational: 'الأداء التشغيلي'
    };
    return categories[category] || category;
  };

  const getCategoryBadge = (category) => {
    const categoryConfig = {
      profitability: { label: 'الربحية', variant: 'default', icon: DollarSign },
      customer_behavior: { label: 'سلوك العملاء', variant: 'secondary', icon: Users },
      supply_chain: { label: 'سلسلة التوريد', variant: 'outline', icon: Truck },
      risk_analysis: { label: 'تحليل المخاطر', variant: 'destructive', icon: AlertTriangle },
      forecasting: { label: 'التنبؤات', variant: 'default', icon: TrendingUp },
      operational: { label: 'الأداء التشغيلي', variant: 'secondary', icon: Target }
    };

    const config = categoryConfig[category] || categoryConfig.profitability;
    const IconComponent = config.icon;
    
    return (
      <Badge variant={config.variant} className="flex items-center gap-1">
        <IconComponent className="w-3 h-3" />
        {config.label}
      </Badge>
    );
  };

  const getComplexityBadge = (complexity) => {
    const complexityConfig = {
      basic: { label: 'أساسي', variant: 'outline', color: 'text-primary' },
      advanced: { label: 'متقدم', variant: 'secondary', color: 'text-primary' },
      expert: { label: 'خبير', variant: 'destructive', color: 'text-destructive' }
    };

    const config = complexityConfig[complexity] || complexityConfig.basic;
    
    return (
      <Badge variant={config.variant} className="flex items-center gap-1">
        {config.label}
      </Badge>
    );
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
              status: 'ready'
            }
          : report
      ));
      toast.success('تم إنشاء التقرير المتقدم بنجاح');
    }, 5000);
    
    toast.info('جاري إنشاء التقرير المتقدم...');
  };

  const handleViewReport = (report) => {
    if (report.status === 'ready') {
      setSelectedReport(report);
      toast.success(`تم فتح ${report.name}`);
    } else {
      toast.error('التقرير غير جاهز للعرض');
    }
  };

  const handleDownloadReport = (report) => {
    if (report.status === 'ready') {
      toast.success(`تم تحميل ${report.name}`);
    } else {
      toast.error('التقرير غير جاهز للتحميل');
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
          <p className="mt-4 text-muted-foreground">جاري تحميل التقارير المتقدمة...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">التقارير المتقدمة</h1>
          <p className="text-muted-foreground mt-1">تقارير تحليلية متقدمة ورؤى عميقة للأعمال</p>
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
              <BarChart3 className="w-8 h-8 text-primary/100" />
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
              <CheckCircle className="w-8 h-8 text-green-500" />
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
              <Clock className="w-8 h-8 text-primary/100" />
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
              <AlertTriangle className="w-8 h-8 text-red-500" />
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
                  placeholder="البحث في أسماء التقارير والرؤى..."
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
                  <SelectItem value="profitability">الربحية</SelectItem>
                  <SelectItem value="customer_behavior">سلوك العملاء</SelectItem>
                  <SelectItem value="supply_chain">سلسلة التوريد</SelectItem>
                  <SelectItem value="risk_analysis">تحليل المخاطر</SelectItem>
                  <SelectItem value="forecasting">التنبؤات</SelectItem>
                  <SelectItem value="operational">الأداء التشغيلي</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="min-w-48">
              <Label htmlFor="complexity-filter">مستوى التعقيد</Label>
              <Select value={filterComplexity} onValueChange={setFilterComplexity}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر المستوى" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع المستويات</SelectItem>
                  <SelectItem value="basic">أساسي</SelectItem>
                  <SelectItem value="advanced">متقدم</SelectItem>
                  <SelectItem value="expert">خبير</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Reports Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredReports.map((report) => (
          <Card key={report.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex justify-between items-start">
                <CardTitle className="text-lg">{report.name}</CardTitle>
                {getStatusBadge(report.status)}
              </div>
              <div className="flex gap-2">
                {getCategoryBadge(report.category)}
                {getComplexityBadge(report.complexity)}
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm text-muted-foreground">{report.description}</p>
              
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">وقت الإنشاء المتوقع:</span>
                  <span className="font-medium">{report.estimatedTime}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">نقاط البيانات:</span>
                  <span className="font-medium">{report.dataPoints.toLocaleString()}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">آخر إنشاء:</span>
                  <span className="font-medium">
                    {new Date(report.lastGenerated).toLocaleDateString('ar-SA')}
                  </span>
                </div>
              </div>

              <div>
                <Label className="text-sm font-medium">الرؤى المتضمنة:</Label>
                <ul className="mt-2 space-y-1">
                  {report.insights.slice(0, 3).map((insight, index) => (
                    <li key={index} className="text-sm text-muted-foreground flex items-center gap-2">
                      <div className="w-1.5 h-1.5 bg-primary/100 rounded-full"></div>
                      {insight}
                    </li>
                  ))}
                  {report.insights.length > 3 && (
                    <li className="text-sm text-gray-500">
                      +{report.insights.length - 3} رؤى أخرى
                    </li>
                  )}
                </ul>
              </div>

              <div className="flex gap-2 pt-4">
                {report.status === 'ready' ? (
                  <>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleViewReport(report)}
                      className="flex-1"
                    >
                      <Eye className="w-4 h-4 mr-2" />
                      عرض
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDownloadReport(report)}
                      className="flex-1"
                    >
                      <Download className="w-4 h-4 mr-2" />
                      تحميل
                    </Button>
                  </>
                ) : (
                  <Button
                    onClick={() => handleGenerateReport(report.id)}
                    disabled={report.status === 'generating'}
                    className="w-full"
                  >
                    {report.status === 'generating' ? (
                      <>
                        <Clock className="w-4 h-4 mr-2 animate-spin" />
                        جاري الإنشاء...
                      </>
                    ) : (
                      <>
                        <BarChart3 className="w-4 h-4 mr-2" />
                        إنشاء التقرير
                      </>
                    )}
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredReports.length === 0 && (
        <Card>
          <CardContent className="text-center py-8">
            <BarChart3 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">لا توجد تقارير تطابق معايير البحث</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default AdvancedReports;

