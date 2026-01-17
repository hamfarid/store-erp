/**
 * صفحة التقارير الشاملة
 * /home/ubuntu/upload/store_v1.1/complete_inventory_system/frontend/src/pages/Reports.js
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';

const Reports = () => {
  const navigate = useNavigate();
  // permissions hook removed (not used)

  // ==================== State Management ====================

  const [selectedTab, setSelectedTab] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // حالات التقارير
  const [availableReports, setAvailableReports] = useState([]);
  const [recentReports, setRecentReports] = useState([]);
  const [favoriteReports, setFavoriteReports] = useState([]);
  const [scheduledReports, setScheduledReports] = useState([]);

  // حالات النوافذ المنبثقة
  const [generateReportDialogOpen, setGenerateReportDialogOpen] = useState(false);
  const [scheduleReportDialogOpen, setScheduleReportDialogOpen] = useState(false);

  // حالات التقرير المحدد
  const [selectedReport, setSelectedReport] = useState(null);
  const [reportConfig, setReportConfig] = useState({
    title: '',
    subtitle: '',
    date_from: null,
    date_to: null,
    format: 'pdf',
    filters: {},
    include_charts: false,
    include_summary: true,
    page_orientation: 'portrait'
  });

  // حالات الفلاتر
  const [warehouses, setWarehouses] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [categories, setCategories] = useState([]);
  const [salesPersons, setSalesPersons] = useState([]);
  
  // حالات الجدولة
  const [scheduleConfig, setScheduleConfig] = useState({
    frequency: 'daily',
    time: '09:00',
    email_recipients: [],
    auto_delete_after_days: 30
  });

  // ==================== Data Loading ====================

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      setError(null);

      // تحميل البيانات بشكل متوازي
      const [
        reportsData,
        recentData,
        favoritesData,
        scheduledData,
        warehousesData,
        customersData,
        suppliersData,
        productsData,
        categoriesData,
        salesPersonsData
      ] = await Promise.allSettled([
        // reportService.getAvailableReports(),
        // reportService.getRecentReports(),
        // reportService.getFavoriteReports(),
        // reportService.getScheduledReports(),
        // warehouseService.getAll(),
        // customerService.getAll(),
        // supplierService.getAll(),
        // productService.getAll(),
        // categoryService.getAll(),
        // userService.getSalesPersons()
        
        // بيانات تجريبية
        Promise.resolve([
          {
            id: 'inventory_report',
            name: 'تقرير المخزون',
            description: 'تقرير شامل عن حالة المخزون الحالية',
            category: 'inventory',
            icon: 'inventory',
            filters: ['warehouse_id', 'category', 'stock_status'],
            formats: ['pdf', 'excel', 'csv'],
            estimated_time: '2-5 دقائق',
            last_generated: '2024-01-15T10:30:00Z',
            generation_count: 45
          },
          {
            id: 'stock_movement_report',
            name: 'تقرير حركة المخزون',
            description: 'تقرير تفصيلي عن حركات المخزون',
            category: 'inventory',
            icon: 'trending_up',
            filters: ['date_from', 'date_to', 'product_id', 'warehouse_id', 'movement_type'],
            formats: ['pdf', 'excel', 'csv'],
            estimated_time: '3-8 دقائق',
            last_generated: '2024-01-14T15:20:00Z',
            generation_count: 32
          },
          {
            id: 'sales_report',
            name: 'تقرير المبيعات',
            description: 'تقرير شامل عن المبيعات والفواتير',
            category: 'sales',
            icon: 'receipt',
            filters: ['date_from', 'date_to', 'customer_id', 'sales_person_id', 'status'],
            formats: ['pdf', 'excel', 'csv'],
            estimated_time: '2-6 دقائق',
            last_generated: '2024-01-15T09:15:00Z',
            generation_count: 78
          },
          {
            id: 'customer_statement_report',
            name: 'كشف حساب عميل',
            description: 'كشف حساب تفصيلي لعميل محدد',
            category: 'customers',
            icon: 'people',
            filters: ['customer_id', 'date_from', 'date_to'],
            formats: ['pdf', 'excel', 'csv'],
            estimated_time: '1-3 دقائق',
            last_generated: '2024-01-15T11:45:00Z',
            generation_count: 23
          },
          {
            id: 'financial_summary_report',
            name: 'التقرير المالي الموجز',
            description: 'ملخص الوضع المالي للشركة',
            category: 'financial',
            icon: 'account_balance',
            filters: ['date_from', 'date_to', 'include_details'],
            formats: ['pdf', 'excel'],
            estimated_time: '5-10 دقائق',
            last_generated: '2024-01-14T16:30:00Z',
            generation_count: 12
          }
        ]),
        Promise.resolve([
          { id: 1, name: 'تقرير المبيعات - يناير 2024', generated_at: '2024-01-15T11:45:00Z', format: 'pdf', size: '2.3 MB' },
          { id: 2, name: 'تقرير المخزون - الأسبوع الحالي', generated_at: '2024-01-15T10:30:00Z', format: 'excel', size: '1.8 MB' },
          { id: 3, name: 'كشف حساب عميل - شركة الأمل', generated_at: '2024-01-15T09:15:00Z', format: 'pdf', size: '856 KB' }
        ]),
        Promise.resolve([
          { id: 'sales_report', name: 'تقرير المبيعات', added_at: '2024-01-10T00:00:00Z' },
          { id: 'inventory_report', name: 'تقرير المخزون', added_at: '2024-01-12T00:00:00Z' }
        ]),
        Promise.resolve([
          { id: 1, report_id: 'sales_report', name: 'تقرير المبيعات الشهري', frequency: 'monthly', next_run: '2024-02-01T09:00:00Z', active: true },
          { id: 2, report_id: 'inventory_report', name: 'تقرير المخزون الأسبوعي', frequency: 'weekly', next_run: '2024-01-22T08:00:00Z', active: true }
        ]),
        Promise.resolve([
          { id: 1, name: 'المخزن الرئيسي', location: 'القاهرة' },
          { id: 2, name: 'مخزن الفرع', location: 'الإسكندرية' }
        ]),
        Promise.resolve([
          { id: 1, name: 'شركة الأمل للتجارة', phone: '01234567890' },
          { id: 2, name: 'مؤسسة النور', phone: '01234567891' }
        ]),
        Promise.resolve([
          { id: 1, name: 'مورد الأجهزة الإلكترونية', phone: '01234567892' },
          { id: 2, name: 'شركة المواد الغذائية', phone: '01234567893' }
        ]),
        Promise.resolve([
          { id: 1, name: 'لابتوب ديل', sku: 'LAP001', category: 'أجهزة كمبيوتر' },
          { id: 2, name: 'ماوس لاسلكي', sku: 'MOU001', category: 'ملحقات' }
        ]),
        Promise.resolve([
          { id: 1, name: 'أجهزة كمبيوتر' },
          { id: 2, name: 'ملحقات' },
          { id: 3, name: 'مواد غذائية' }
        ]),
        Promise.resolve([
          { id: 1, full_name: 'أحمد محمد', email: 'ahmed@company.com' },
          { id: 2, full_name: 'فاطمة علي', email: 'fatma@company.com' }
        ])
      ]);

      // تعيين البيانات
      if (reportsData.status === 'fulfilled') setAvailableReports(reportsData.value);
      if (recentData.status === 'fulfilled') setRecentReports(recentData.value);
      if (favoritesData.status === 'fulfilled') setFavoriteReports(favoritesData.value);
      if (scheduledData.status === 'fulfilled') setScheduledReports(scheduledData.value);
      if (warehousesData.status === 'fulfilled') setWarehouses(warehousesData.value);
      if (customersData.status === 'fulfilled') setCustomers(customersData.value);
      if (suppliersData.status === 'fulfilled') setSuppliers(suppliersData.value);
      if (productsData.status === 'fulfilled') setProducts(productsData.value);
      if (categoriesData.status === 'fulfilled') setCategories(categoriesData.value);
      if (salesPersonsData.status === 'fulfilled') setSalesPersons(salesPersonsData.value);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // ==================== Event Handlers ====================

  const handleGenerateReport = async () => {
    try {
      setLoading(true);
      
      // إنشاء التقرير
      // const result = await reportService.generateReport(selectedReport.id, reportConfig);
      // محاكاة إنشاء التقرير
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setGenerateReportDialogOpen(false);
      
      // إعادة تحميل التقارير الحديثة
      await loadInitialData();
      
      alert('تم إنشاء التقرير بنجاح!');
      
    } catch (error) {
      alert(`خطأ في إنشاء التقرير: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleScheduleReport = async () => {
    try {
      setLoading(true);
      
      // جدولة التقرير
      // const result = await reportService.scheduleReport(selectedReport.id, reportConfig, scheduleConfig);
      setScheduleReportDialogOpen(false);
      
      // إعادة تحميل التقارير المجدولة
      await loadInitialData();
      
      alert('تم جدولة التقرير بنجاح!');
      
    } catch (error) {
      alert(`خطأ في جدولة التقرير: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleAddToFavorites = async (reportId) => {
    try {
      // await reportService.addToFavorites(reportId);
      await loadInitialData();
    } catch (error) {
      }
  };

  const handleRemoveFromFavorites = async (reportId) => {
    try {
      // await reportService.removeFromFavorites(reportId);
      await loadInitialData();
    } catch (error) {
      }
  };

  const handleDownloadReport = async (reportId) => {
    try {
      // const url = await reportService.getDownloadUrl(reportId);
      // window.open(url, '_blank');
      } catch (error) {
      }
  };

  const openGenerateDialog = (report) => {
    setSelectedReport(report);
    setReportConfig({
      title: report.name,
      subtitle: '',
      date_from: null,
      date_to: null,
      format: 'pdf',
      filters: {},
      include_charts: false,
      include_summary: true,
      page_orientation: 'portrait'
    });
    setGenerateReportDialogOpen(true);
  };

  const openScheduleDialog = (report) => {
    setSelectedReport(report);
    setReportConfig({
      title: report.name,
      subtitle: '',
      date_from: null,
      date_to: null,
      format: 'pdf',
      filters: {},
      include_charts: false,
      include_summary: true,
      page_orientation: 'portrait'
    });
    setScheduleConfig({
      frequency: 'daily',
      time: '09:00',
      email_recipients: [],
      auto_delete_after_days: 30
    });
    setScheduleReportDialogOpen(true);
  };

  // ==================== Helper Functions ====================

  const getReportIcon = (iconName) => {
    const icons = {
      inventory: <InventoryIcon />,
      trending_up: <TrendingUpIcon />,
      receipt: <ReceiptIcon />,
      people: <PeopleIcon />,
      account_balance: <AccountBalanceIcon />,
      business: <BusinessIcon />,
      monetization_on: <MonetizationOnIcon />,
      shopping_cart: <ShoppingCartIcon />,
      local_shipping: <LocalShippingIcon />
    };
    return icons[iconName] || <AssessmentIcon />;
  };

  const getReportCategoryColor = (category) => {
    const colors = {
      inventory: 'primary',
      sales: 'success',
      customers: 'info',
      suppliers: 'warning',
      financial: 'error'
    };
    return colors[category] || 'default';
  };

  const getFormatIcon = (format) => {
    const icons = {
      pdf: <PdfIcon />,
      excel: <ExcelIcon />,
      csv: <CsvIcon />
    };
    return icons[format] || <DownloadIcon />;
  };

  // Removed unused formatFileSize function

  const getTimeAgo = (dateString) => {
    const now = new Date();
    const date = new Date(dateString);
    const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'منذ أقل من ساعة';
    if (diffInHours < 24) return `منذ ${diffInHours} ساعة`;
    
    const diffInDays = Math.floor(diffInHours / 24);
    if (diffInDays < 7) return `منذ ${diffInDays} يوم`;
    
    return date.toLocaleDateString('ar-EG');
  };

  // ==================== Render Functions ====================

  const renderReportCard = (report) => (
    <Card key={report.id} sx={{ height: '100%' }}>
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          {getReportIcon(report.icon)}
          <Box ml={2} flexGrow={1}>
            <Typography variant="h6" component="h3">
              {report.name}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {report.description}
            </Typography>
          </Box>
          <IconButton
            size="small"
            onClick={() => 
              favoriteReports.some(f => f.id === report.id) 
                ? handleRemoveFromFavorites(report.id)
                : handleAddToFavorites(report.id)
            }
          >
            <StarIcon 
              color={favoriteReports.some(f => f.id === report.id) ? 'warning' : 'disabled'} 
            />
          </IconButton>
        </Box>

        <Box mb={2}>
          <Chip
            label={report.category}
            color={getReportCategoryColor(report.category)}
            size="small"
            sx={{ mr: 1 }}
          />
          <Chip
            label={`${report.generation_count} مرة`}
            variant="outlined"
            size="small"
            sx={{ mr: 1 }}
          />
          <Chip
            label={report.estimated_time}
            variant="outlined"
            size="small"
            color="info"
          />
        </Box>

        <Typography variant="caption" color="text.secondary" display="block" mb={2}>
          آخر إنشاء: {getTimeAgo(report.last_generated)}
        </Typography>

        <Box display="flex" gap={1}>
          <ProtectedButton
            variant="contained"
            size="small"
            startIcon={<AssessmentIcon />}
            onClick={() => openGenerateDialog(report)}
            requiredPermission="generate_reports"
          >
            إنشاء
          </ProtectedButton>
          
          <ProtectedButton
            variant="outlined"
            size="small"
            startIcon={<ScheduleIcon />}
            onClick={() => openScheduleDialog(report)}
            requiredPermission="schedule_reports"
          >
            جدولة
          </ProtectedButton>
          
          <IconButton
            size="small"
            onClick={() => navigate(`/reports/${report.id}/history`)}
          >
            <HistoryIcon />
          </IconButton>
        </Box>
      </CardContent>
    </Card>
  );

  const renderFilterField = (filterName) => {
    switch (filterName) {
      case 'warehouse_id':
        return (
          <FormControl fullWidth size="small" sx={{ mb: 2 }}>
            <InputLabel>المخزن</InputLabel>
            <Select
              value={reportConfig.filters.warehouse_id || ''}
              onChange={(e) => setReportConfig({
                ...reportConfig,
                filters: { ...reportConfig.filters, warehouse_id: e.target.value }
              })}
              label="المخزن"
            >
              <MenuItem value="">الكل</MenuItem>
              {warehouses.map(warehouse => (
                <MenuItem key={warehouse.id} value={warehouse.id}>
                  {warehouse.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        );
      
      case 'customer_id':
        return (
          <Autocomplete
            size="small"
            options={customers}
            getOptionLabel={(option) => option.name}
            value={customers.find(c => c.id === reportConfig.filters.customer_id) || null}
            onChange={(_, newValue) => setReportConfig({
              ...reportConfig,
              filters: { ...reportConfig.filters, customer_id: newValue?.id || '' }
            })}
            renderInput={(params) => (
              <TextField {...params} label="العميل" sx={{ mb: 2 }} />
            )}
          />
        );
      
      case 'category':
        return (
          <FormControl fullWidth size="small" sx={{ mb: 2 }}>
            <InputLabel>الفئة</InputLabel>
            <Select
              value={reportConfig.filters.category || ''}
              onChange={(e) => setReportConfig({
                ...reportConfig,
                filters: { ...reportConfig.filters, category: e.target.value }
              })}
              label="الفئة"
            >
              <MenuItem value="">الكل</MenuItem>
              {categories.map(category => (
                <MenuItem key={category.id} value={category.name}>
                  {category.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        );
      
      case 'sales_person_id':
        return (
          <FormControl fullWidth size="small" sx={{ mb: 2 }}>
            <InputLabel>مندوب المبيعات</InputLabel>
            <Select
              value={reportConfig.filters.sales_person_id || ''}
              onChange={(e) => setReportConfig({
                ...reportConfig,
                filters: { ...reportConfig.filters, sales_person_id: e.target.value }
              })}
              label="مندوب المبيعات"
            >
              <MenuItem value="">الكل</MenuItem>
              {salesPersons.map(person => (
                <MenuItem key={person.id} value={person.id}>
                  {person.full_name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        );
      
      default:
        return null;
    }
  };

  if (loading && availableReports.length === 0) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
        <Typography variant="h6" sx={{ ml: 2 }}>
          جاري تحميل التقارير...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        خطأ في تحميل التقارير: {error}
      </Alert>
    );
  }

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box sx={{ p: 3 }}>
        {/* Header */}
        <Box display="flex" justifyContent="between" alignItems="center" mb={3}>
          <Box>
            <Typography variant="h4" component="h1" gutterBottom>
              التقارير
            </Typography>
            <Typography variant="body1" color="text.secondary">
              إنشاء وإدارة التقارير المختلفة
            </Typography>
          </Box>
          
          <Box display="flex" gap={1}>
            <Button
              variant="outlined"
              startIcon={<RefreshIcon />}
              onClick={loadInitialData}
            >
              تحديث
            </Button>
            
            <ProtectedButton
              variant="outlined"
              startIcon={<SettingsIcon />}
              onClick={() => navigate('/reports/settings')}
              requiredPermission="manage_report_settings"
            >
              الإعدادات
            </ProtectedButton>
          </Box>
        </Box>

        {/* Tabs */}
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
          <Tabs value={selectedTab} onChange={(_, newValue) => setSelectedTab(newValue)}>
            <Tab label="جميع التقارير" />
            <Tab label={`المفضلة (${favoriteReports.length})`} />
            <Tab label={`الحديثة (${recentReports.length})`} />
            <Tab label={`المجدولة (${scheduledReports.length})`} />
          </Tabs>
        </Box>

        {/* Tab Content */}
        {selectedTab === 0 && (
          <Grid container spacing={3}>
            {availableReports.map(report => (
              <Grid item xs={12} sm={6} md={4} key={report.id}>
                {renderReportCard(report)}
              </Grid>
            ))}
          </Grid>
        )}

        {selectedTab === 1 && (
          <Grid container spacing={3}>
            {favoriteReports.map(favorite => {
              const report = availableReports.find(r => r.id === favorite.id);
              return report ? (
                <Grid item xs={12} sm={6} md={4} key={report.id}>
                  {renderReportCard(report)}
                </Grid>
              ) : null;
            })}
            {favoriteReports.length === 0 && (
              <Grid item xs={12}>
                <Paper sx={{ p: 4, textAlign: 'center' }}>
                  <StarIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="h6" color="text.secondary">
                    لا توجد تقارير مفضلة
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    أضف التقارير التي تستخدمها بكثرة إلى المفضلة للوصول السريع
                  </Typography>
                </Paper>
              </Grid>
            )}
          </Grid>
        )}

        {selectedTab === 2 && (
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                التقارير المُنشأة مؤخراً
              </Typography>
              <List>
                {recentReports.map((report, index) => (
                  <React.Fragment key={report.id}>
                    <ListItem>
                      <ListItemIcon>
                        {getFormatIcon(report.format)}
                      </ListItemIcon>
                      <ListItemText
                        primary={report.name}
                        secondary={`${getTimeAgo(report.generated_at)} • ${report.size}`}
                      />
                      <Box display="flex" gap={1}>
                        <IconButton
                          size="small"
                          onClick={() => handleDownloadReport(report.id)}
                        >
                          <DownloadIcon />
                        </IconButton>
                        <IconButton size="small">
                          <ShareIcon />
                        </IconButton>
                      </Box>
                    </ListItem>
                    {index < recentReports.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
              {recentReports.length === 0 && (
                <Box textAlign="center" py={4}>
                  <HistoryIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="h6" color="text.secondary">
                    لا توجد تقارير حديثة
                  </Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        )}

        {selectedTab === 3 && (
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                التقارير المجدولة
              </Typography>
              <List>
                {scheduledReports.map((scheduled, index) => (
                  <React.Fragment key={scheduled.id}>
                    <ListItem>
                      <ListItemIcon>
                        <ScheduleIcon />
                      </ListItemIcon>
                      <ListItemText
                        primary={scheduled.name}
                        secondary={`${scheduled.frequency} • التشغيل التالي: ${getTimeAgo(scheduled.next_run)}`}
                      />
                      <Chip
                        label={scheduled.active ? 'نشط' : 'متوقف'}
                        color={scheduled.active ? 'success' : 'error'}
                        size="small"
                        sx={{ mr: 1 }}
                      />
                      <IconButton size="small">
                        <SettingsIcon />
                      </IconButton>
                    </ListItem>
                    {index < scheduledReports.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
              {scheduledReports.length === 0 && (
                <Box textAlign="center" py={4}>
                  <ScheduleIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="h6" color="text.secondary">
                    لا توجد تقارير مجدولة
                  </Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        )}

        {/* Generate Report Dialog */}
        <Dialog 
          open={generateReportDialogOpen} 
          onClose={() => setGenerateReportDialogOpen(false)}
          maxWidth="md"
          fullWidth
        >
          <DialogTitle>
            إنشاء تقرير: {selectedReport?.name}
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              {/* إعدادات أساسية */}
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                  الإعدادات الأساسية
                </Typography>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="عنوان التقرير"
                  value={reportConfig.title}
                  onChange={(e) => setReportConfig({ ...reportConfig, title: e.target.value })}
                />
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>تنسيق التقرير</InputLabel>
                  <Select
                    value={reportConfig.format}
                    onChange={(e) => setReportConfig({ ...reportConfig, format: e.target.value })}
                    label="تنسيق التقرير"
                  >
                    <MenuItem value="pdf">PDF</MenuItem>
                    <MenuItem value="excel">Excel</MenuItem>
                    <MenuItem value="csv">CSV</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="العنوان الفرعي (اختياري)"
                  value={reportConfig.subtitle}
                  onChange={(e) => setReportConfig({ ...reportConfig, subtitle: e.target.value })}
                />
              </Grid>

              {/* فترة التقرير */}
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                  فترة التقرير
                </Typography>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <DatePicker
                  label="من تاريخ"
                  value={reportConfig.date_from}
                  onChange={(newValue) => setReportConfig({ ...reportConfig, date_from: newValue })}
                  renderInput={(params) => <TextField {...params} fullWidth />}
                />
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <DatePicker
                  label="إلى تاريخ"
                  value={reportConfig.date_to}
                  onChange={(newValue) => setReportConfig({ ...reportConfig, date_to: newValue })}
                  renderInput={(params) => <TextField {...params} fullWidth />}
                />
              </Grid>

              {/* الفلاتر */}
              {selectedReport?.filters && selectedReport.filters.length > 0 && (
                <>
                  <Grid item xs={12}>
                    <Typography variant="h6" gutterBottom>
                      الفلاتر
                    </Typography>
                  </Grid>
                  
                  <Grid item xs={12}>
                    {selectedReport.filters.map(filter => (
                      <Box key={filter}>
                        {renderFilterField(filter)}
                      </Box>
                    ))}
                  </Grid>
                </>
              )}

              {/* خيارات متقدمة */}
              <Grid item xs={12}>
                <Accordion>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography variant="h6">خيارات متقدمة</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <FormControlLabel
                          control={
                            <Switch
                              checked={reportConfig.include_charts}
                              onChange={(e) => setReportConfig({ 
                                ...reportConfig, 
                                include_charts: e.target.checked 
                              })}
                            />
                          }
                          label="تضمين الرسوم البيانية"
                        />
                      </Grid>
                      
                      <Grid item xs={12} sm={6}>
                        <FormControlLabel
                          control={
                            <Switch
                              checked={reportConfig.include_summary}
                              onChange={(e) => setReportConfig({ 
                                ...reportConfig, 
                                include_summary: e.target.checked 
                              })}
                            />
                          }
                          label="تضمين الملخص"
                        />
                      </Grid>
                      
                      <Grid item xs={12} sm={6}>
                        <FormControl fullWidth>
                          <InputLabel>اتجاه الصفحة</InputLabel>
                          <Select
                            value={reportConfig.page_orientation}
                            onChange={(e) => setReportConfig({ 
                              ...reportConfig, 
                              page_orientation: e.target.value 
                            })}
                            label="اتجاه الصفحة"
                          >
                            <MenuItem value="portrait">عمودي</MenuItem>
                            <MenuItem value="landscape">أفقي</MenuItem>
                          </Select>
                        </FormControl>
                      </Grid>
                    </Grid>
                  </AccordionDetails>
                </Accordion>
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setGenerateReportDialogOpen(false)}>
              إلغاء
            </Button>
            <Button 
              onClick={handleGenerateReport} 
              variant="contained"
              disabled={loading}
              startIcon={loading ? <CircularProgress size={20} /> : <AssessmentIcon />}
            >
              {loading ? 'جاري الإنشاء...' : 'إنشاء التقرير'}
            </Button>
          </DialogActions>
        </Dialog>

        {/* Schedule Report Dialog */}
        <Dialog 
          open={scheduleReportDialogOpen} 
          onClose={() => setScheduleReportDialogOpen(false)}
          maxWidth="md"
          fullWidth
        >
          <DialogTitle>
            جدولة تقرير: {selectedReport?.name}
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              {/* إعدادات الجدولة */}
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                  إعدادات الجدولة
                </Typography>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>التكرار</InputLabel>
                  <Select
                    value={scheduleConfig.frequency}
                    onChange={(e) => setScheduleConfig({ 
                      ...scheduleConfig, 
                      frequency: e.target.value 
                    })}
                    label="التكرار"
                  >
                    <MenuItem value="daily">يومي</MenuItem>
                    <MenuItem value="weekly">أسبوعي</MenuItem>
                    <MenuItem value="monthly">شهري</MenuItem>
                    <MenuItem value="quarterly">ربع سنوي</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="وقت التشغيل"
                  type="time"
                  value={scheduleConfig.time}
                  onChange={(e) => setScheduleConfig({ 
                    ...scheduleConfig, 
                    time: e.target.value 
                  })}
                  InputLabelProps={{ shrink: true }}
                />
              </Grid>
              
              <Grid item xs={12}>
                <Autocomplete
                  multiple
                  options={salesPersons}
                  getOptionLabel={(option) => option.email}
                  value={scheduleConfig.email_recipients}
                  onChange={(_, newValue) => setScheduleConfig({
                    ...scheduleConfig,
                    email_recipients: newValue
                  })}
                  renderInput={(params) => (
                    <TextField {...params} label="المستلمون عبر البريد الإلكتروني" />
                  )}
                />
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="حذف تلقائي بعد (أيام)"
                  type="number"
                  value={scheduleConfig.auto_delete_after_days}
                  onChange={(e) => setScheduleConfig({ 
                    ...scheduleConfig, 
                    auto_delete_after_days: parseInt(e.target.value) 
                  })}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setScheduleReportDialogOpen(false)}>
              إلغاء
            </Button>
            <Button 
              onClick={handleScheduleReport} 
              variant="contained"
              disabled={loading}
              startIcon={loading ? <CircularProgress size={20} /> : <ScheduleIcon />}
            >
              {loading ? 'جاري الجدولة...' : 'جدولة التقرير'}
            </Button>
          </DialogActions>
        </Dialog>

        {/* Loading Overlay */}
        {loading && (
          <Box
            position="fixed"
            top={0}
            left={0}
            right={0}
            bottom={0}
            bgcolor="rgba(0, 0, 0, 0.5)"
            display="flex"
            alignItems="center"
            justifyContent="center"
            zIndex={9999}
          >
            <Paper sx={{ p: 3, textAlign: 'center' }}>
              <CircularProgress sx={{ mb: 2 }} />
              <Typography variant="h6">
                جاري معالجة التقرير...
              </Typography>
              <LinearProgress sx={{ mt: 2, width: 300 }} />
            </Paper>
          </Box>
        )}
      </Box>
    </LocalizationProvider>
  );
};

export default Reports;

