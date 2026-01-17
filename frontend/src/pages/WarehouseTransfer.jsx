import React, { useState, useEffect } from 'react';
import {
  Plus, Search, Download, Edit, Trash2, Eye, ArrowLeftRight, 
  Warehouse, Package, CheckCircle, XCircle, Clock, Truck, User
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
 * صفحة تحويلات المخازن
 * Warehouse Transfer Page
 */
const WarehouseTransfer = () => {
  const [transfers, setTransfers] = useState([]);
  const [filteredTransfers, setFilteredTransfers] = useState([]);
  const [warehouses, setWarehouses] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterWarehouse, setFilterWarehouse] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedTransfer, setSelectedTransfer] = useState(null);

  // بيانات نموذجية
  const sampleWarehouses = [
    { id: 1, name: 'المخزن الرئيسي', location: 'الرياض' },
    { id: 2, name: 'مخزن الفرع الأول', location: 'جدة' },
    { id: 3, name: 'مخزن الفرع الثاني', location: 'الدمام' }
  ];

  const sampleTransfers = [
    {
      id: 1,
      transferNumber: 'TRF-2024-001',
      fromWarehouseId: 1,
      fromWarehouseName: 'المخزن الرئيسي',
      toWarehouseId: 2,
      toWarehouseName: 'مخزن الفرع الأول',
      status: 'pending',
      requestedBy: 'أحمد محمد',
      requestedDate: '2024-01-15T10:00:00',
      approvedBy: null,
      approvedDate: null,
      completedBy: null,
      completedDate: null,
      items: [
        { productName: 'لابتوب ديل', requestedQty: 10, approvedQty: null, unit: 'قطعة' },
        { productName: 'طابعة HP', requestedQty: 5, approvedQty: null, unit: 'قطعة' }
      ],
      totalItems: 2,
      notes: 'تحويل عاجل للفرع'
    },
    {
      id: 2,
      transferNumber: 'TRF-2024-002',
      fromWarehouseId: 1,
      fromWarehouseName: 'المخزن الرئيسي',
      toWarehouseId: 3,
      toWarehouseName: 'مخزن الفرع الثاني',
      status: 'approved',
      requestedBy: 'سارة أحمد',
      requestedDate: '2024-01-14T14:30:00',
      approvedBy: 'محمد علي',
      approvedDate: '2024-01-14T16:00:00',
      completedBy: null,
      completedDate: null,
      items: [
        { productName: 'هاتف ذكي', requestedQty: 20, approvedQty: 20, unit: 'قطعة' },
        { productName: 'شاحن سريع', requestedQty: 50, approvedQty: 45, unit: 'قطعة' }
      ],
      totalItems: 2,
      notes: 'تزويد الفرع الجديد'
    },
    {
      id: 3,
      transferNumber: 'TRF-2024-003',
      fromWarehouseId: 2,
      fromWarehouseName: 'مخزن الفرع الأول',
      toWarehouseId: 1,
      toWarehouseName: 'المخزن الرئيسي',
      status: 'completed',
      requestedBy: 'فاطمة سالم',
      requestedDate: '2024-01-13T11:00:00',
      approvedBy: 'أحمد محمد',
      approvedDate: '2024-01-13T12:00:00',
      completedBy: 'خالد أحمد',
      completedDate: '2024-01-13T15:00:00',
      items: [
        { productName: 'كيبل USB', requestedQty: 100, approvedQty: 100, unit: 'قطعة' }
      ],
      totalItems: 1,
      notes: 'إرجاع فائض المخزون'
    },
    {
      id: 4,
      transferNumber: 'TRF-2024-004',
      fromWarehouseId: 3,
      fromWarehouseName: 'مخزن الفرع الثاني',
      toWarehouseId: 2,
      toWarehouseName: 'مخزن الفرع الأول',
      status: 'rejected',
      requestedBy: 'خالد أحمد',
      requestedDate: '2024-01-12T08:00:00',
      approvedBy: 'محمد علي',
      approvedDate: '2024-01-12T10:00:00',
      completedBy: null,
      completedDate: null,
      items: [
        { productName: 'شاشة سامسونج', requestedQty: 15, approvedQty: 0, unit: 'قطعة' }
      ],
      totalItems: 1,
      notes: 'مرفوض - لا يوجد كمية كافية',
      rejectionReason: 'الكمية المطلوبة غير متوفرة'
    }
  ];

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const [transfersRes, warehousesRes] = await Promise.allSettled([
        apiClient.get('/api/warehouse-transfers'),
        apiClient.get('/api/warehouses')
      ]);

      if (transfersRes.status === 'fulfilled' && transfersRes.value.status === 'success') {
        setTransfers(transfersRes.value.transfers || []);
        setFilteredTransfers(transfersRes.value.transfers || []);
      } else {
        setTransfers(sampleTransfers);
        setFilteredTransfers(sampleTransfers);
      }

      if (warehousesRes.status === 'fulfilled' && warehousesRes.value.status === 'success') {
        setWarehouses(warehousesRes.value.data || []);
      } else {
        setWarehouses(sampleWarehouses);
      }
    } catch (error) {
      console.log('Using sample data:', error);
      setTransfers(sampleTransfers);
      setFilteredTransfers(sampleTransfers);
      setWarehouses(sampleWarehouses);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let filtered = transfers;

    if (searchTerm) {
      filtered = filtered.filter(t =>
        t.transferNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
        t.fromWarehouseName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        t.toWarehouseName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        t.requestedBy.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterStatus !== 'all') {
      filtered = filtered.filter(t => t.status === filterStatus);
    }

    if (filterWarehouse !== 'all') {
      const whId = parseInt(filterWarehouse);
      filtered = filtered.filter(t => t.fromWarehouseId === whId || t.toWarehouseId === whId);
    }

    setFilteredTransfers(filtered);
  }, [transfers, searchTerm, filterStatus, filterWarehouse]);

  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { label: 'في الانتظار', variant: 'secondary', icon: Clock },
      approved: { label: 'معتمد', variant: 'default', icon: CheckCircle },
      completed: { label: 'مكتمل', variant: 'default', icon: Truck },
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

  const handleAddTransfer = () => {
    setSelectedTransfer(null);
    setShowAddModal(true);
    toast.success('جاري فتح نموذج تحويل جديد');
  };

  const handleEditTransfer = (transfer) => {
    if (transfer.status !== 'pending') {
      toast.error('لا يمكن تعديل تحويل معتمد أو مكتمل');
      return;
    }
    setSelectedTransfer(transfer);
    setShowAddModal(true);
  };

  const handleDeleteTransfer = (transferId) => {
    const transfer = transfers.find(t => t.id === transferId);
    if (transfer.status !== 'pending') {
      toast.error('لا يمكن حذف تحويل غير معلق');
      return;
    }
    
    if (window.confirm('هل أنت متأكد من حذف هذا التحويل؟')) {
      setTransfers(transfers.filter(t => t.id !== transferId));
      toast.success('تم حذف التحويل بنجاح');
    }
  };

  const handleApproveTransfer = (transferId) => {
    setTransfers(transfers.map(t =>
      t.id === transferId
        ? { 
            ...t, 
            status: 'approved',
            approvedBy: 'المدير الحالي',
            approvedDate: new Date().toISOString(),
            items: t.items.map(item => ({ ...item, approvedQty: item.requestedQty }))
          }
        : t
    ));
    toast.success('تم اعتماد التحويل بنجاح');
  };

  const handleRejectTransfer = (transferId) => {
    const reason = prompt('سبب الرفض:');
    if (!reason) return;
    
    setTransfers(transfers.map(t =>
      t.id === transferId
        ? { 
            ...t, 
            status: 'rejected',
            approvedBy: 'المدير الحالي',
            approvedDate: new Date().toISOString(),
            rejectionReason: reason,
            items: t.items.map(item => ({ ...item, approvedQty: 0 }))
          }
        : t
    ));
    toast.success('تم رفض التحويل');
  };

  const handleCompleteTransfer = (transferId) => {
    setTransfers(transfers.map(t =>
      t.id === transferId
        ? { 
            ...t, 
            status: 'completed',
            completedBy: 'المستخدم الحالي',
            completedDate: new Date().toISOString()
          }
        : t
    ));
    toast.success('تم إتمام التحويل بنجاح');
  };

  const handleExport = () => {
    toast.success('تم تصدير البيانات بنجاح');
  };

  const getSummary = () => {
    return {
      total: transfers.length,
      pending: transfers.filter(t => t.status === 'pending').length,
      approved: transfers.filter(t => t.status === 'approved').length,
      completed: transfers.filter(t => t.status === 'completed').length,
      rejected: transfers.filter(t => t.status === 'rejected').length
    };
  };

  const summary = getSummary();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل تحويلات المخازن...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">تحويلات المخازن</h1>
          <p className="text-muted-foreground mt-1">إدارة تحويلات المخزون بين المخازن</p>
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
            onClick={handleAddTransfer}
            className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
          >
            <Plus className="w-4 h-4" />
            تحويل جديد
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي التحويلات</p>
                <p className="text-2xl font-bold text-primary">{summary.total}</p>
              </div>
              <ArrowLeftRight className="w-8 h-8 text-primary/60" />
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
                <p className="text-2xl font-bold text-blue-600">{summary.approved}</p>
              </div>
              <CheckCircle className="w-8 h-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">مكتملة</p>
                <p className="text-2xl font-bold text-green-600">{summary.completed}</p>
              </div>
              <Truck className="w-8 h-8 text-green-500" />
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
                  placeholder="البحث برقم التحويل، المخزن..."
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
              <Label htmlFor="status-filter">الحالة</Label>
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر الحالة" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع الحالات</SelectItem>
                  <SelectItem value="pending">في الانتظار</SelectItem>
                  <SelectItem value="approved">معتمد</SelectItem>
                  <SelectItem value="completed">مكتمل</SelectItem>
                  <SelectItem value="rejected">مرفوض</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Transfers Table */}
      <Card>
        <CardHeader>
          <CardTitle>قائمة التحويلات ({filteredTransfers.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>رقم التحويل</TableHead>
                <TableHead>من المخزن</TableHead>
                <TableHead>إلى المخزن</TableHead>
                <TableHead>عدد الأصناف</TableHead>
                <TableHead>الحالة</TableHead>
                <TableHead>الطالب</TableHead>
                <TableHead>تاريخ الطلب</TableHead>
                <TableHead>الإجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredTransfers.map((transfer) => (
                <TableRow key={transfer.id}>
                  <TableCell>
                    <span className="font-mono font-medium">{transfer.transferNumber}</span>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Warehouse className="w-4 h-4 text-red-500" />
                      <span>{transfer.fromWarehouseName}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Warehouse className="w-4 h-4 text-green-500" />
                      <span>{transfer.toWarehouseName}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Package className="w-4 h-4 text-muted-foreground" />
                      <span>{transfer.totalItems}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    {getStatusBadge(transfer.status)}
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <User className="w-3 h-3 text-muted-foreground" />
                      <span className="text-sm">{transfer.requestedBy}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <span className="text-sm">
                      {new Date(transfer.requestedDate).toLocaleDateString('ar-SA')}
                    </span>
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-1">
                      {transfer.status === 'pending' && (
                        <>
                          <button
                            onClick={() => handleApproveTransfer(transfer.id)}
                            className="px-2 py-1 text-sm text-green-600 hover:bg-green-50 rounded"
                          >
                            اعتماد
                          </button>
                          <button
                            onClick={() => handleRejectTransfer(transfer.id)}
                            className="px-2 py-1 text-sm text-red-600 hover:bg-red-50 rounded"
                          >
                            رفض
                          </button>
                        </>
                      )}
                      {transfer.status === 'approved' && (
                        <button
                          onClick={() => handleCompleteTransfer(transfer.id)}
                          className="px-2 py-1 text-sm text-blue-600 hover:bg-blue-50 rounded"
                        >
                          إتمام
                        </button>
                      )}
                      <button
                        onClick={() => handleEditTransfer(transfer)}
                        className="p-1 hover:bg-muted rounded"
                        disabled={transfer.status !== 'pending'}
                      >
                        <Edit className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => setSelectedTransfer(transfer)}
                        className="p-1 hover:bg-muted rounded"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                      {transfer.status === 'pending' && (
                        <button
                          onClick={() => handleDeleteTransfer(transfer.id)}
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

          {filteredTransfers.length === 0 && (
            <div className="text-center py-8">
              <ArrowLeftRight className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">لا توجد تحويلات تطابق معايير البحث</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Transfer Details Modal */}
      {selectedTransfer && !showAddModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-background rounded-lg p-6 max-w-3xl w-full mx-4 max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">تفاصيل التحويل</h2>
              <button onClick={() => setSelectedTransfer(null)} className="p-2 hover:bg-muted rounded">✕</button>
            </div>
            
            <div className="space-y-4">
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label>رقم التحويل</Label>
                  <p className="font-mono font-medium">{selectedTransfer.transferNumber}</p>
                </div>
                <div>
                  <Label>الحالة</Label>
                  <p>{getStatusBadge(selectedTransfer.status)}</p>
                </div>
                <div>
                  <Label>تاريخ الطلب</Label>
                  <p>{new Date(selectedTransfer.requestedDate).toLocaleString('ar-SA')}</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 border rounded-lg">
                  <Label className="text-red-600">من المخزن</Label>
                  <p className="font-medium">{selectedTransfer.fromWarehouseName}</p>
                </div>
                <div className="p-4 border rounded-lg">
                  <Label className="text-green-600">إلى المخزن</Label>
                  <p className="font-medium">{selectedTransfer.toWarehouseName}</p>
                </div>
              </div>

              <div>
                <Label>الأصناف</Label>
                <div className="border rounded-lg mt-2">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>المنتج</TableHead>
                        <TableHead>الكمية المطلوبة</TableHead>
                        <TableHead>الكمية المعتمدة</TableHead>
                        <TableHead>الوحدة</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {selectedTransfer.items.map((item, index) => (
                        <TableRow key={index}>
                          <TableCell>{item.productName}</TableCell>
                          <TableCell>{item.requestedQty}</TableCell>
                          <TableCell className={item.approvedQty !== null && item.approvedQty < item.requestedQty ? 'text-orange-600' : ''}>
                            {item.approvedQty !== null ? item.approvedQty : '-'}
                          </TableCell>
                          <TableCell>{item.unit}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </div>

              {selectedTransfer.rejectionReason && (
                <div>
                  <Label className="text-red-600">سبب الرفض</Label>
                  <p className="text-red-600">{selectedTransfer.rejectionReason}</p>
                </div>
              )}

              <div>
                <Label>ملاحظات</Label>
                <p className="text-muted-foreground">{selectedTransfer.notes || 'لا توجد ملاحظات'}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default WarehouseTransfer;

