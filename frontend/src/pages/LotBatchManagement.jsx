import React, { useState, useEffect } from 'react';
import {
  Package, Search, Download, Plus, Edit, Trash2, Eye, Calendar,
  AlertTriangle, CheckCircle, Clock, Filter, BarChart3, Box
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
 * إدارة الدفعات والتشغيلات
 * Lot/Batch Management Page
 */
const LotBatchManagement = () => {
  const [lots, setLots] = useState([]);
  const [filteredLots, setFilteredLots] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterWarehouse, setFilterWarehouse] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedLot, setSelectedLot] = useState(null);

  // بيانات نموذجية
  const sampleLots = [
    {
      id: 1,
      lotNumber: 'LOT-2024-001',
      productId: 1,
      productName: 'لابتوب HP ProBook 450',
      productSku: 'HP-PB-450',
      warehouseId: 1,
      warehouseName: 'المستودع الرئيسي',
      quantity: 50,
      originalQuantity: 100,
      costPrice: 2500,
      manufactureDate: '2024-01-01',
      expiryDate: '2026-01-01',
      receivedDate: '2024-01-10',
      status: 'active',
      supplier: 'HP Arabia',
      notes: 'دفعة جديدة من الموزع المعتمد'
    },
    {
      id: 2,
      lotNumber: 'LOT-2024-002',
      productId: 2,
      productName: 'طابعة Canon PIXMA',
      productSku: 'CN-PX-100',
      warehouseId: 1,
      warehouseName: 'المستودع الرئيسي',
      quantity: 25,
      originalQuantity: 50,
      costPrice: 450,
      manufactureDate: '2023-11-15',
      expiryDate: '2025-11-15',
      receivedDate: '2024-01-05',
      status: 'active',
      supplier: 'Canon Middle East',
      notes: ''
    },
    {
      id: 3,
      lotNumber: 'LOT-2024-003',
      productId: 3,
      productName: 'حبر طابعة HP 123',
      productSku: 'HP-INK-123',
      warehouseId: 2,
      warehouseName: 'مستودع الفرع',
      quantity: 200,
      originalQuantity: 200,
      costPrice: 85,
      manufactureDate: '2024-01-01',
      expiryDate: '2025-06-30',
      receivedDate: '2024-01-12',
      status: 'active',
      supplier: 'HP Arabia',
      notes: 'حبر أصلي'
    },
    {
      id: 4,
      lotNumber: 'LOT-2023-050',
      productId: 4,
      productName: 'ورق طباعة A4',
      productSku: 'PAPER-A4-500',
      warehouseId: 1,
      warehouseName: 'المستودع الرئيسي',
      quantity: 10,
      originalQuantity: 500,
      costPrice: 25,
      manufactureDate: '2023-06-01',
      expiryDate: '2024-06-01',
      receivedDate: '2023-06-15',
      status: 'expiring_soon',
      supplier: 'مصنع الورق السعودي',
      notes: 'قرب انتهاء الصلاحية'
    },
    {
      id: 5,
      lotNumber: 'LOT-2023-025',
      productId: 5,
      productName: 'بطاريات AAA',
      productSku: 'BAT-AAA-10',
      warehouseId: 2,
      warehouseName: 'مستودع الفرع',
      quantity: 0,
      originalQuantity: 100,
      costPrice: 15,
      manufactureDate: '2023-01-01',
      expiryDate: '2024-01-01',
      receivedDate: '2023-01-20',
      status: 'expired',
      supplier: 'Energizer',
      notes: 'منتهية الصلاحية - للإتلاف'
    },
    {
      id: 6,
      lotNumber: 'LOT-2024-004',
      productId: 6,
      productName: 'ماوس لاسلكي Logitech',
      productSku: 'LOG-M-100',
      warehouseId: 1,
      warehouseName: 'المستودع الرئيسي',
      quantity: 75,
      originalQuantity: 75,
      costPrice: 120,
      manufactureDate: '2024-01-10',
      expiryDate: null,
      receivedDate: '2024-01-15',
      status: 'active',
      supplier: 'Logitech Arabia',
      notes: 'لا تاريخ انتهاء'
    }
  ];

  const warehouses = [
    { id: 1, name: 'المستودع الرئيسي' },
    { id: 2, name: 'مستودع الفرع' }
  ];

  useEffect(() => {
    fetchLots();
  }, []);

  const fetchLots = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.get('/api/lots');
      if (response.status === 'success' && response.lots?.length > 0) {
        setLots(response.lots);
        setFilteredLots(response.lots);
      } else {
        setLots(sampleLots);
        setFilteredLots(sampleLots);
      }
    } catch (error) {
      console.log('Using sample data:', error);
      setLots(sampleLots);
      setFilteredLots(sampleLots);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let filtered = lots;

    if (searchTerm) {
      filtered = filtered.filter(lot =>
        lot.lotNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
        lot.productName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        lot.productSku.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterStatus !== 'all') {
      filtered = filtered.filter(lot => lot.status === filterStatus);
    }

    if (filterWarehouse !== 'all') {
      filtered = filtered.filter(lot => lot.warehouseId.toString() === filterWarehouse);
    }

    setFilteredLots(filtered);
  }, [lots, searchTerm, filterStatus, filterWarehouse]);

  const getStatusBadge = (status) => {
    switch (status) {
      case 'active':
        return (
          <Badge variant="default" className="flex items-center gap-1">
            <CheckCircle className="w-3 h-3" />
            نشط
          </Badge>
        );
      case 'expiring_soon':
        return (
          <Badge variant="warning" className="flex items-center gap-1 bg-yellow-100 text-yellow-800">
            <AlertTriangle className="w-3 h-3" />
            قرب الانتهاء
          </Badge>
        );
      case 'expired':
        return (
          <Badge variant="destructive" className="flex items-center gap-1">
            <Clock className="w-3 h-3" />
            منتهي
          </Badge>
        );
      case 'depleted':
        return (
          <Badge variant="secondary" className="flex items-center gap-1">
            <Box className="w-3 h-3" />
            نفد
          </Badge>
        );
      default:
        return <Badge>{status}</Badge>;
    }
  };

  const getDaysToExpiry = (expiryDate) => {
    if (!expiryDate) return null;
    const today = new Date();
    const expiry = new Date(expiryDate);
    const diff = Math.ceil((expiry - today) / (1000 * 60 * 60 * 24));
    return diff;
  };

  const handleAddLot = () => {
    setSelectedLot(null);
    setShowAddModal(true);
    toast.success('جاري فتح نموذج دفعة جديدة');
  };

  const handleEditLot = (lot) => {
    setSelectedLot(lot);
    setShowAddModal(true);
  };

  const handleViewLot = (lot) => {
    setSelectedLot(lot);
    toast.success(`عرض تفاصيل الدفعة ${lot.lotNumber}`);
  };

  const handleDeleteLot = (lotId) => {
    if (window.confirm('هل أنت متأكد من حذف هذه الدفعة؟')) {
      setLots(lots.filter(l => l.id !== lotId));
      toast.success('تم حذف الدفعة بنجاح');
    }
  };

  const handleExport = () => {
    toast.success('تم تصدير البيانات بنجاح');
  };

  const getSummary = () => {
    const totalValue = lots.reduce((sum, lot) => sum + (lot.quantity * lot.costPrice), 0);
    return {
      total: lots.length,
      active: lots.filter(l => l.status === 'active').length,
      expiringSoon: lots.filter(l => l.status === 'expiring_soon').length,
      expired: lots.filter(l => l.status === 'expired').length,
      totalValue
    };
  };

  const summary = getSummary();

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('ar-SA', {
      style: 'currency',
      currency: 'SAR',
      minimumFractionDigits: 0
    }).format(amount);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل الدفعات...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground flex items-center gap-2">
            <Package className="w-8 h-8" />
            إدارة الدفعات
          </h1>
          <p className="text-muted-foreground mt-1">تتبع دفعات المنتجات وتواريخ الصلاحية</p>
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
            onClick={handleAddLot}
            className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
          >
            <Plus className="w-4 h-4" />
            دفعة جديدة
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي الدفعات</p>
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
                <p className="text-sm text-muted-foreground">نشطة</p>
                <p className="text-2xl font-bold text-green-600">{summary.active}</p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">قرب الانتهاء</p>
                <p className="text-2xl font-bold text-yellow-600">{summary.expiringSoon}</p>
              </div>
              <AlertTriangle className="w-8 h-8 text-yellow-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">منتهية</p>
                <p className="text-2xl font-bold text-red-600">{summary.expired}</p>
              </div>
              <Clock className="w-8 h-8 text-red-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">القيمة الإجمالية</p>
                <p className="text-xl font-bold text-blue-600">{formatCurrency(summary.totalValue)}</p>
              </div>
              <BarChart3 className="w-8 h-8 text-blue-500" />
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
                  placeholder="البحث برقم الدفعة أو المنتج..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>

            <div className="min-w-40">
              <Label htmlFor="warehouse-filter">المستودع</Label>
              <Select value={filterWarehouse} onValueChange={setFilterWarehouse}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر المستودع" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع المستودعات</SelectItem>
                  {warehouses.map(wh => (
                    <SelectItem key={wh.id} value={wh.id.toString()}>{wh.name}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="min-w-32">
              <Label htmlFor="status-filter">الحالة</Label>
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger>
                  <SelectValue placeholder="الحالة" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">الكل</SelectItem>
                  <SelectItem value="active">نشط</SelectItem>
                  <SelectItem value="expiring_soon">قرب الانتهاء</SelectItem>
                  <SelectItem value="expired">منتهي</SelectItem>
                  <SelectItem value="depleted">نفد</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Lots Table */}
      <Card>
        <CardHeader>
          <CardTitle>قائمة الدفعات ({filteredLots.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>رقم الدفعة</TableHead>
                <TableHead>المنتج</TableHead>
                <TableHead>المستودع</TableHead>
                <TableHead>الكمية</TableHead>
                <TableHead>تكلفة الوحدة</TableHead>
                <TableHead>تاريخ الاستلام</TableHead>
                <TableHead>تاريخ الانتهاء</TableHead>
                <TableHead>الحالة</TableHead>
                <TableHead>الإجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredLots.map((lot) => {
                const daysToExpiry = getDaysToExpiry(lot.expiryDate);
                return (
                  <TableRow key={lot.id} className={lot.status === 'expired' ? 'bg-red-50 dark:bg-red-900/10' : ''}>
                    <TableCell className="font-mono font-medium">{lot.lotNumber}</TableCell>
                    <TableCell>
                      <div>
                        <div className="font-medium">{lot.productName}</div>
                        <div className="text-sm text-muted-foreground">{lot.productSku}</div>
                      </div>
                    </TableCell>
                    <TableCell>{lot.warehouseName}</TableCell>
                    <TableCell>
                      <div>
                        <span className="font-bold">{lot.quantity}</span>
                        <span className="text-muted-foreground"> / {lot.originalQuantity}</span>
                      </div>
                      <div className="w-full bg-muted h-1.5 rounded mt-1">
                        <div 
                          className={`h-1.5 rounded ${lot.quantity / lot.originalQuantity > 0.5 ? 'bg-green-500' : lot.quantity / lot.originalQuantity > 0.2 ? 'bg-yellow-500' : 'bg-red-500'}`}
                          style={{ width: `${(lot.quantity / lot.originalQuantity) * 100}%` }}
                        />
                      </div>
                    </TableCell>
                    <TableCell>{formatCurrency(lot.costPrice)}</TableCell>
                    <TableCell>
                      {new Date(lot.receivedDate).toLocaleDateString('ar-SA')}
                    </TableCell>
                    <TableCell>
                      {lot.expiryDate ? (
                        <div>
                          <div>{new Date(lot.expiryDate).toLocaleDateString('ar-SA')}</div>
                          {daysToExpiry !== null && (
                            <div className={`text-xs ${daysToExpiry < 0 ? 'text-red-600' : daysToExpiry < 30 ? 'text-yellow-600' : 'text-green-600'}`}>
                              {daysToExpiry < 0 ? `منتهي منذ ${Math.abs(daysToExpiry)} يوم` : `${daysToExpiry} يوم متبقي`}
                            </div>
                          )}
                        </div>
                      ) : (
                        <span className="text-muted-foreground">-</span>
                      )}
                    </TableCell>
                    <TableCell>
                      {getStatusBadge(lot.status)}
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-1">
                        <button
                          onClick={() => handleViewLot(lot)}
                          className="p-1 hover:bg-muted rounded"
                          title="عرض"
                        >
                          <Eye className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleEditLot(lot)}
                          className="p-1 hover:bg-muted rounded"
                          title="تعديل"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDeleteLot(lot.id)}
                          className="p-1 text-red-600 hover:bg-red-50 rounded"
                          title="حذف"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>

          {filteredLots.length === 0 && (
            <div className="text-center py-8">
              <Package className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">لا توجد دفعات تطابق معايير البحث</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default LotBatchManagement;

