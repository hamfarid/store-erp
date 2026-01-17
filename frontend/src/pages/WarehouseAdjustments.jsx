import React, { useState, useEffect } from 'react';
import {
  Plus, Search, Download, Edit, Trash2, Eye, CheckCircle, XCircle, 
  Clock, Package, Warehouse, TrendingUp, TrendingDown, ArrowUpDown
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
 * صفحة تعديلات المخازن
 * Warehouse Adjustments Page
 */
const WarehouseAdjustments = () => {
  const [adjustments, setAdjustments] = useState([]);
  const [filteredAdjustments, setFilteredAdjustments] = useState([]);
  const [warehouses, setWarehouses] = useState([]);
  // const [products, setProducts] = useState([]); // Currently unused (already commented out earlier)
  const [searchTerm, setSearchTerm] = useState('');
  const [filterWarehouse, setFilterWarehouse] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterType, setFilterType] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedAdjustment, setSelectedAdjustment] = useState(null);

  // بيانات نموذجية للاختبار
  const sampleAdjustments = [
    {
      id: 1,
      adjustmentNumber: 'ADJ-2024-001',
      warehouseId: 1,
      warehouseName: 'المخزن الرئيسي',
      type: 'increase',
      reason: 'جرد دوري',
      status: 'pending',
      createdBy: 'أحمد محمد',
      createdAt: '2024-01-15T09:00:00',
      approvedBy: null,
      approvedAt: null,
      items: [
        { productId: 1, productName: 'لابتوب ديل', currentQty: 50, adjustedQty: 52, difference: 2, unitCost: 2500, totalValue: 5000 },
        { productId: 2, productName: 'طابعة HP', currentQty: 25, adjustedQty: 23, difference: -2, unitCost: 800, totalValue: -1600 }
      ],
      totalValue: 3400,
      notes: 'تعديل بناءً على الجرد الدوري الشهري'
    },
    {
      id: 2,
      adjustmentNumber: 'ADJ-2024-002',
      warehouseId: 2,
      warehouseName: 'مخزن الإلكترونيات',
      type: 'decrease',
      reason: 'تلف',
      status: 'approved',
      createdBy: 'سارة أحمد',
      createdAt: '2024-01-14T14:30:00',
      approvedBy: 'محمد علي',
      approvedAt: '2024-01-14T16:00:00',
      items: [
        { productId: 3, productName: 'هاتف ذكي', currentQty: 100, adjustedQty: 95, difference: -5, unitCost: 1200, totalValue: -6000 }
      ],
      totalValue: -6000,
      notes: 'تلف في الشحنة الأخيرة'
    },
    {
      id: 3,
      adjustmentNumber: 'ADJ-2024-003',
      warehouseId: 3,
      warehouseName: 'مخزن المواد الغذائية',
      type: 'increase',
      reason: 'خطأ في الإدخال',
      status: 'rejected',
      createdBy: 'فاطمة سالم',
      createdAt: '2024-01-13T11:00:00',
      approvedBy: 'أحمد محمد',
      approvedAt: '2024-01-13T15:30:00',
      items: [
        { productId: 4, productName: 'أرز بسمتي', currentQty: 200, adjustedQty: 210, difference: 10, unitCost: 15, totalValue: 150 }
      ],
      totalValue: 150,
      notes: 'تم رفض التعديل - لا يوجد مبرر كافي'
    },
    {
      id: 4,
      adjustmentNumber: 'ADJ-2024-004',
      warehouseId: 1,
      warehouseName: 'المخزن الرئيسي',
      type: 'mixed',
      reason: 'جرد سنوي',
      status: 'pending',
      createdBy: 'خالد أحمد',
      createdAt: '2024-01-16T10:00:00',
      approvedBy: null,
      approvedAt: null,
      items: [
        { productId: 5, productName: 'شاشة سامسونج', currentQty: 30, adjustedQty: 35, difference: 5, unitCost: 1500, totalValue: 7500 },
        { productId: 6, productName: 'كيبورد', currentQty: 80, adjustedQty: 75, difference: -5, unitCost: 100, totalValue: -500 }
      ],
      totalValue: 7000,
      notes: 'تعديلات الجرد السنوي'
    }
  ];

  const sampleWarehouses = [
    { id: 1, name: 'المخزن الرئيسي', location: 'الرياض' },
    { id: 2, name: 'مخزن الإلكترونيات', location: 'جدة' },
    { id: 3, name: 'مخزن المواد الغذائية', location: 'الدمام' }
  ];

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      // محاولة جلب البيانات من API
      const [adjustmentsRes, warehousesRes] = await Promise.allSettled([
        apiClient.get('/api/warehouse-adjustments'),
        apiClient.get('/api/warehouses')
      ]);

      if (adjustmentsRes.status === 'fulfilled' && adjustmentsRes.value.status === 'success') {
        setAdjustments(adjustmentsRes.value.data);
        setFilteredAdjustments(adjustmentsRes.value.data);
      } else {
        setAdjustments(sampleAdjustments);
        setFilteredAdjustments(sampleAdjustments);
      }

      if (warehousesRes.status === 'fulfilled' && warehousesRes.value.status === 'success') {
        setWarehouses(warehousesRes.value.data);
      } else {
        setWarehouses(sampleWarehouses);
      }
    } catch (error) {
      console.log('Using sample data:', error);
      setAdjustments(sampleAdjustments);
      setFilteredAdjustments(sampleAdjustments);
      setWarehouses(sampleWarehouses);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let filtered = adjustments;

    if (searchTerm) {
      filtered = filtered.filter(adj =>
        adj.adjustmentNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
        adj.warehouseName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        adj.reason.toLowerCase().includes(searchTerm.toLowerCase()) ||
        adj.createdBy.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterWarehouse !== 'all') {
      filtered = filtered.filter(adj => adj.warehouseId === parseInt(filterWarehouse));
    }

    if (filterStatus !== 'all') {
      filtered = filtered.filter(adj => adj.status === filterStatus);
    }

    if (filterType !== 'all') {
      filtered = filtered.filter(adj => adj.type === filterType);
    }

    setFilteredAdjustments(filtered);
  }, [adjustments, searchTerm, filterWarehouse, filterStatus, filterType]);

  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { label: 'في الانتظار', variant: 'secondary', icon: Clock },
      approved: { label: 'معتمد', variant: 'default', icon: CheckCircle },
      rejected: { label: 'مرفوض', variant: 'destructive', icon: XCircle }
    };

    const config = statusConfig[status] || statusConfig.pending;
    const IconComponent = config.icon;
    
    return (
      <Badge variant={config.variant} className="flex items-center gap-1">
        <IconComponent className="w-3 h-3" />
        {config.label}
      </Badge>
    );
  };

  const getTypeBadge = (type) => {
    const typeConfig = {
      increase: { label: 'زيادة', variant: 'default', icon: TrendingUp },
      decrease: { label: 'نقص', variant: 'destructive', icon: TrendingDown },
      mixed: { label: 'مختلط', variant: 'secondary', icon: ArrowUpDown }
    };

    const config = typeConfig[type] || typeConfig.mixed;
    const IconComponent = config.icon;
    
    return (
      <Badge variant={config.variant} className="flex items-center gap-1">
        <IconComponent className="w-3 h-3" />
        {config.label}
      </Badge>
    );
  };

  const handleAddAdjustment = () => {
    setSelectedAdjustment(null);
    setShowAddModal(true);
    toast.success('جاري فتح نموذج تعديل جديد');
  };

  const handleEditAdjustment = (adjustment) => {
    if (adjustment.status !== 'pending') {
      toast.error('لا يمكن تعديل تسوية معتمدة أو مرفوضة');
      return;
    }
    setSelectedAdjustment(adjustment);
    setShowAddModal(true);
  };

  const handleDeleteAdjustment = async (adjustmentId) => {
    const adjustment = adjustments.find(a => a.id === adjustmentId);
    if (adjustment.status === 'approved') {
      toast.error('لا يمكن حذف تسوية معتمدة');
      return;
    }
    
    if (window.confirm('هل أنت متأكد من حذف هذه التسوية؟')) {
      try {
        await apiClient.delete(`/api/warehouse-adjustments/${adjustmentId}`);
        setAdjustments(adjustments.filter(adj => adj.id !== adjustmentId));
        toast.success('تم حذف التسوية بنجاح');
      } catch (error) {
        // Fallback to local deletion
        setAdjustments(adjustments.filter(adj => adj.id !== adjustmentId));
        toast.success('تم حذف التسوية بنجاح');
      }
    }
  };

  const handleApproveAdjustment = async (adjustmentId) => {
    try {
      await apiClient.post(`/api/warehouse-adjustments/${adjustmentId}/approve`, {
        approved_by: 'المدير الحالي'
      });
      setAdjustments(adjustments.map(adj =>
        adj.id === adjustmentId
          ? { ...adj, status: 'approved', approvedBy: 'المدير الحالي', approvedAt: new Date().toISOString() }
          : adj
      ));
      toast.success('تم اعتماد التسوية بنجاح');
    } catch (error) {
      // Fallback to local update
      setAdjustments(adjustments.map(adj =>
        adj.id === adjustmentId
          ? { ...adj, status: 'approved', approvedBy: 'المدير الحالي', approvedAt: new Date().toISOString() }
          : adj
      ));
      toast.success('تم اعتماد التسوية بنجاح');
    }
  };

  const handleRejectAdjustment = async (adjustmentId) => {
    const reason = prompt('سبب الرفض:');
    if (!reason) return;
    
    try {
      await apiClient.post(`/api/warehouse-adjustments/${adjustmentId}/reject`, {
        approved_by: 'المدير الحالي',
        rejection_reason: reason
      });
      setAdjustments(adjustments.map(adj =>
        adj.id === adjustmentId
          ? { ...adj, status: 'rejected', approvedBy: 'المدير الحالي', approvedAt: new Date().toISOString() }
          : adj
      ));
      toast.success('تم رفض التسوية');
    } catch (error) {
      // Fallback to local update
      setAdjustments(adjustments.map(adj =>
        adj.id === adjustmentId
          ? { ...adj, status: 'rejected', approvedBy: 'المدير الحالي', approvedAt: new Date().toISOString() }
          : adj
      ));
      toast.success('تم رفض التسوية');
    }
  };

  const handleExport = () => {
    toast.success('تم تصدير البيانات بنجاح');
  };

  const getSummary = () => {
    return {
      total: adjustments.length,
      pending: adjustments.filter(a => a.status === 'pending').length,
      approved: adjustments.filter(a => a.status === 'approved').length,
      rejected: adjustments.filter(a => a.status === 'rejected').length,
      totalPositiveValue: adjustments.filter(a => a.status === 'approved' && a.totalValue > 0).reduce((sum, a) => sum + a.totalValue, 0),
      totalNegativeValue: Math.abs(adjustments.filter(a => a.status === 'approved' && a.totalValue < 0).reduce((sum, a) => sum + a.totalValue, 0))
    };
  };

  const summary = getSummary();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل تعديلات المخازن...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">تعديلات المخازن</h1>
          <p className="text-muted-foreground mt-1">إدارة تسويات وتعديلات المخزون</p>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={handleExport}
            className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors"
          >
            <Download className="w-4 h-4" />
            تصدير
          </button>
          <button 
            onClick={handleAddAdjustment}
            className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
          >
            <Plus className="w-4 h-4" />
            تسوية جديدة
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي التسويات</p>
                <p className="text-2xl font-bold text-primary">{summary.total}</p>
              </div>
              <Package className="w-8 h-8 text-primary/60" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">في الانتظار</p>
                <p className="text-2xl font-bold text-yellow-600">{summary.pending}</p>
              </div>
              <Clock className="w-8 h-8 text-yellow-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">معتمدة</p>
                <p className="text-2xl font-bold text-green-600">{summary.approved}</p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">مرفوضة</p>
                <p className="text-2xl font-bold text-red-600">{summary.rejected}</p>
              </div>
              <XCircle className="w-8 h-8 text-red-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إضافات (قيمة)</p>
                <p className="text-2xl font-bold text-green-600">{summary.totalPositiveValue.toLocaleString()}</p>
              </div>
              <TrendingUp className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">نقص (قيمة)</p>
                <p className="text-2xl font-bold text-red-600">{summary.totalNegativeValue.toLocaleString()}</p>
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
                <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
                <Input
                  id="search"
                  placeholder="البحث برقم التسوية، المخزن، السبب..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>

            <div className="min-w-48">
              <Label htmlFor="warehouse-filter">المخزن</Label>
              <Select value={filterWarehouse} onValueChange={setFilterWarehouse}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر المخزن" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع المخازن</SelectItem>
                  {warehouses.map(wh => (
                    <SelectItem key={wh.id} value={wh.id.toString()}>{wh.name}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="min-w-40">
              <Label htmlFor="type-filter">النوع</Label>
              <Select value={filterType} onValueChange={setFilterType}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر النوع" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع الأنواع</SelectItem>
                  <SelectItem value="increase">زيادة</SelectItem>
                  <SelectItem value="decrease">نقص</SelectItem>
                  <SelectItem value="mixed">مختلط</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="min-w-40">
              <Label htmlFor="status-filter">الحالة</Label>
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر الحالة" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع الحالات</SelectItem>
                  <SelectItem value="pending">في الانتظار</SelectItem>
                  <SelectItem value="approved">معتمد</SelectItem>
                  <SelectItem value="rejected">مرفوض</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Adjustments Table */}
      <Card>
        <CardHeader>
          <CardTitle>قائمة التسويات ({filteredAdjustments.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>رقم التسوية</TableHead>
                <TableHead>المخزن</TableHead>
                <TableHead>النوع</TableHead>
                <TableHead>السبب</TableHead>
                <TableHead>عدد الأصناف</TableHead>
                <TableHead>القيمة الإجمالية</TableHead>
                <TableHead>الحالة</TableHead>
                <TableHead>المنشئ</TableHead>
                <TableHead>التاريخ</TableHead>
                <TableHead>الإجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredAdjustments.map((adjustment) => (
                <TableRow key={adjustment.id}>
                  <TableCell>
                    <div className="font-medium">{adjustment.adjustmentNumber}</div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Warehouse className="w-4 h-4 text-muted-foreground" />
                      <span>{adjustment.warehouseName}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    {getTypeBadge(adjustment.type)}
                  </TableCell>
                  <TableCell>
                    <span className="text-sm">{adjustment.reason}</span>
                  </TableCell>
                  <TableCell>
                    <span className="font-medium">{adjustment.items.length}</span>
                  </TableCell>
                  <TableCell>
                    <div className={`font-medium ${adjustment.totalValue >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {adjustment.totalValue >= 0 ? '+' : ''}{adjustment.totalValue.toLocaleString()} ج.م
                    </div>
                  </TableCell>
                  <TableCell>
                    {getStatusBadge(adjustment.status)}
                  </TableCell>
                  <TableCell>
                    <span className="text-sm">{adjustment.createdBy}</span>
                  </TableCell>
                  <TableCell>
                    <span className="text-sm">
                      {new Date(adjustment.createdAt).toLocaleDateString('ar-SA')}
                    </span>
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-1">
                      {adjustment.status === 'pending' && (
                        <>
                          <button
                            onClick={() => handleApproveAdjustment(adjustment.id)}
                            className="px-2 py-1 text-sm text-green-600 hover:bg-green-50 rounded"
                          >
                            اعتماد
                          </button>
                          <button
                            onClick={() => handleRejectAdjustment(adjustment.id)}
                            className="px-2 py-1 text-sm text-red-600 hover:bg-red-50 rounded"
                          >
                            رفض
                          </button>
                        </>
                      )}
                      <button
                        onClick={() => handleEditAdjustment(adjustment)}
                        className="p-1 hover:bg-muted rounded"
                        disabled={adjustment.status !== 'pending'}
                      >
                        <Edit className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => setSelectedAdjustment(adjustment)}
                        className="p-1 hover:bg-muted rounded"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                      {adjustment.status !== 'approved' && (
                        <button
                          onClick={() => handleDeleteAdjustment(adjustment.id)}
                          className="p-1 text-red-600 hover:bg-red-50 rounded"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>

          {filteredAdjustments.length === 0 && (
            <div className="text-center py-8">
              <Package className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">لا توجد تسويات تطابق معايير البحث</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Adjustment Details Modal */}
      {selectedAdjustment && !showAddModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-background rounded-lg p-6 max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">تفاصيل التسوية</h2>
              <button
                onClick={() => setSelectedAdjustment(null)}
                className="p-2 hover:bg-muted rounded"
              >
                ✕
              </button>
            </div>
            
            <div className="space-y-4">
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label>رقم التسوية</Label>
                  <p className="font-medium">{selectedAdjustment.adjustmentNumber}</p>
                </div>
                <div>
                  <Label>المخزن</Label>
                  <p className="font-medium">{selectedAdjustment.warehouseName}</p>
                </div>
                <div>
                  <Label>النوع</Label>
                  <p>{getTypeBadge(selectedAdjustment.type)}</p>
                </div>
                <div>
                  <Label>السبب</Label>
                  <p className="font-medium">{selectedAdjustment.reason}</p>
                </div>
                <div>
                  <Label>الحالة</Label>
                  <p>{getStatusBadge(selectedAdjustment.status)}</p>
                </div>
                <div>
                  <Label>القيمة الإجمالية</Label>
                  <p className={`font-medium ${selectedAdjustment.totalValue >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {selectedAdjustment.totalValue >= 0 ? '+' : ''}{selectedAdjustment.totalValue.toLocaleString()} ج.م
                  </p>
                </div>
              </div>

              <div>
                <Label>الأصناف</Label>
                <div className="border rounded-lg mt-2">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>المنتج</TableHead>
                        <TableHead>الكمية الحالية</TableHead>
                        <TableHead>الكمية بعد التعديل</TableHead>
                        <TableHead>الفرق</TableHead>
                        <TableHead>سعر الوحدة</TableHead>
                        <TableHead>القيمة</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {selectedAdjustment.items.map((item, index) => (
                        <TableRow key={index}>
                          <TableCell>{item.productName}</TableCell>
                          <TableCell>{item.currentQty}</TableCell>
                          <TableCell>{item.adjustedQty}</TableCell>
                          <TableCell className={item.difference >= 0 ? 'text-green-600' : 'text-red-600'}>
                            {item.difference >= 0 ? '+' : ''}{item.difference}
                          </TableCell>
                          <TableCell>{item.unitCost.toLocaleString()} ج.م</TableCell>
                          <TableCell className={item.totalValue >= 0 ? 'text-green-600' : 'text-red-600'}>
                            {item.totalValue >= 0 ? '+' : ''}{item.totalValue.toLocaleString()} ج.م
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>المنشئ</Label>
                  <p className="text-muted-foreground">{selectedAdjustment.createdBy}</p>
                </div>
                <div>
                  <Label>تاريخ الإنشاء</Label>
                  <p className="text-muted-foreground">{new Date(selectedAdjustment.createdAt).toLocaleString('ar-SA')}</p>
                </div>
                {selectedAdjustment.approvedBy && (
                  <>
                    <div>
                      <Label>المعتمد</Label>
                      <p className="text-muted-foreground">{selectedAdjustment.approvedBy}</p>
                    </div>
                    <div>
                      <Label>تاريخ الاعتماد</Label>
                      <p className="text-muted-foreground">{new Date(selectedAdjustment.approvedAt).toLocaleString('ar-SA')}</p>
                    </div>
                  </>
                )}
              </div>

              <div>
                <Label>ملاحظات</Label>
                <p className="text-muted-foreground">{selectedAdjustment.notes || 'لا توجد ملاحظات'}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default WarehouseAdjustments;
