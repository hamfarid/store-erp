import React, { useState, useEffect } from 'react';
import {
  Truck,
  Package,
  MapPin,
  Calendar,
  Clock,
  User,
  Phone,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Search,
  Filter,
  Plus,
  Edit,
  Trash2,
  Eye,
  Download,
  Upload
} from 'lucide-react';
import { toast } from 'react-hot-toast';

const PickupDeliveryOrders = () => {
  const [orders, setOrders] = useState([]);
  const [filteredOrders, setFilteredOrders] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState(null);

  // Sample data
  const sampleOrders = [
    {
      id: 1,
      orderNumber: 'PD-2024-001',
      type: 'delivery',
      customerName: 'شركة الأحمد للتجارة',
      customerPhone: '+966501234567',
      address: 'الرياض، حي النخيل، شارع الملك فهد',
      scheduledDate: '2024-01-16',
      scheduledTime: '10:00',
      status: 'pending',
      driverName: 'أحمد محمد',
      driverPhone: '+966507654321',
      vehicleNumber: 'أ ب ج 1234',
      items: [
        { name: 'لابتوب ديل', quantity: 2, weight: 4.5 },
        { name: 'طابعة HP', quantity: 1, weight: 8.2 }
      ],
      totalWeight: 12.7,
      totalValue: 15000,
      notes: 'يرجى التعامل بحذر مع الأجهزة الإلكترونية',
      createdAt: '2024-01-15T09:00:00',
      estimatedDuration: 45
    },
    {
      id: 2,
      orderNumber: 'PD-2024-002',
      type: 'pickup',
      customerName: 'مؤسسة البناء الحديث',
      customerPhone: '+966512345678',
      address: 'جدة، حي الصفا، طريق الملك عبدالعزيز',
      scheduledDate: '2024-01-16',
      scheduledTime: '14:00',
      status: 'in_progress',
      driverName: 'محمد علي',
      driverPhone: '+966509876543',
      vehicleNumber: 'د هـ و 5678',
      items: [
        { name: 'مواد بناء متنوعة', quantity: 50, weight: 250.0 }
      ],
      totalWeight: 250.0,
      totalValue: 8500,
      notes: 'استلام مواد البناء من الموقع',
      createdAt: '2024-01-15T11:30:00',
      estimatedDuration: 90
    },
    {
      id: 3,
      orderNumber: 'PD-2024-003',
      type: 'delivery',
      customerName: 'متجر الإلكترونيات المتقدم',
      customerPhone: '+966555123456',
      address: 'الدمام، حي الشاطئ، شارع الخليج',
      scheduledDate: '2024-01-15',
      scheduledTime: '16:00',
      status: 'completed',
      driverName: 'سالم أحمد',
      driverPhone: '+966508765432',
      vehicleNumber: 'ز ح ط 9012',
      items: [
        { name: 'هواتف ذكية', quantity: 10, weight: 2.5 },
        { name: 'أجهزة تابلت', quantity: 5, weight: 3.0 }
      ],
      totalWeight: 5.5,
      totalValue: 22000,
      notes: 'تم التسليم بنجاح',
      createdAt: '2024-01-15T08:00:00',
      estimatedDuration: 60,
      completedAt: '2024-01-15T16:45:00'
    },
    {
      id: 4,
      orderNumber: 'PD-2024-004',
      type: 'pickup',
      customerName: 'شركة المواد الغذائية',
      customerPhone: '+966566789012',
      address: 'الرياض، حي العليا، طريق العروبة',
      scheduledDate: '2024-01-17',
      scheduledTime: '09:00',
      status: 'cancelled',
      driverName: null,
      driverPhone: null,
      vehicleNumber: null,
      items: [
        { name: 'منتجات غذائية', quantity: 30, weight: 45.0 }
      ],
      totalWeight: 45.0,
      totalValue: 3500,
      notes: 'تم إلغاء الطلب بناءً على طلب العميل',
      createdAt: '2024-01-15T14:00:00',
      estimatedDuration: 30,
      cancelledAt: '2024-01-15T15:30:00'
    }
  ];

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setOrders(sampleOrders);
      setFilteredOrders(sampleOrders);
      setIsLoading(false);
    }, 1000);
  }, []);

  useEffect(() => {
    let filtered = orders;

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(order =>
        order.orderNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
        order.customerName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        order.address.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (order.driverName && order.driverName.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    // Filter by type
    if (filterType !== 'all') {
      filtered = filtered.filter(order => order.type === filterType);
    }

    // Filter by status
    if (filterStatus !== 'all') {
      filtered = filtered.filter(order => order.status === filterStatus);
    }

    setFilteredOrders(filtered);
  }, [orders, searchTerm, filterType, filterStatus]);

  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { label: 'في الانتظار', variant: 'secondary', icon: Clock, color: 'text-accent' },
      in_progress: { label: 'قيد التنفيذ', variant: 'default', icon: Truck, color: 'text-primary' },
      completed: { label: 'مكتمل', variant: 'default', icon: CheckCircle, color: 'text-primary' },
      cancelled: { label: 'ملغي', variant: 'destructive', icon: XCircle, color: 'text-destructive' }
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

  const getTypeLabel = (type) => {
    const types = {
      delivery: 'توصيل',
      pickup: 'استلام'
    };
    return types[type] || type;
  };

  const getTypeIcon = (type) => {
    const icons = {
      delivery: Truck,
      pickup: Package
    };
    return icons[type] || Package;
  };

  const getTypeBadge = (type) => {
    const TypeIcon = getTypeIcon(type);
    const variant = type === 'delivery' ? 'default' : 'secondary';
    
    return (
      <Badge variant={variant} className="flex items-center gap-1">
        <TypeIcon className="w-3 h-3" />
        {getTypeLabel(type)}
      </Badge>
    );
  };

  const handleAddOrder = () => {
    setSelectedOrder(null);
    setShowAddModal(true);
  };

  const handleEditOrder = (order) => {
    setSelectedOrder(order);
    setShowAddModal(true);
  };

  const handleDeleteOrder = (orderId) => {
    if (window.confirm('هل أنت متأكد من حذف هذا الطلب؟')) {
      setOrders(orders.filter(order => order.id !== orderId));
      toast.success('تم حذف الطلب بنجاح');
    }
  };

  const handleUpdateStatus = (orderId, newStatus) => {
    setOrders(orders.map(order =>
      order.id === orderId
        ? { 
            ...order, 
            status: newStatus,
            ...(newStatus === 'completed' && { completedAt: new Date().toISOString() }),
            ...(newStatus === 'cancelled' && { cancelledAt: new Date().toISOString() })
          }
        : order
    ));
    toast.success('تم تحديث حالة الطلب');
  };

  const handleExport = () => {
    toast.success('تم تصدير البيانات بنجاح');
  };

  const getStatusCounts = () => {
    return {
      total: orders.length,
      pending: orders.filter(o => o.status === 'pending').length,
      in_progress: orders.filter(o => o.status === 'in_progress').length,
      completed: orders.filter(o => o.status === 'completed').length,
      cancelled: orders.filter(o => o.status === 'cancelled').length
    };
  };

  const statusCounts = getStatusCounts();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل طلبات الاستلام والتوصيل...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">طلبات الاستلام والتوصيل</h1>
          <p className="text-muted-foreground mt-1">إدارة طلبات الاستلام والتوصيل والمتابعة</p>
        </div>
        <div className="flex gap-2">
          <Button onClick={handleExport} variant="outline">
            <Download className="w-4 h-4 mr-2" />
            تصدير
          </Button>
          <Button onClick={handleAddOrder}>
            <Plus className="w-4 h-4 mr-2" />
            إضافة طلب جديد
          </Button>
        </div>
      </div>

      {/* Status Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي الطلبات</p>
                <p className="text-2xl font-bold text-primary">{statusCounts.total}</p>
              </div>
              <Package className="w-8 h-8 text-primary/100" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">في الانتظار</p>
                <p className="text-2xl font-bold text-accent">{statusCounts.pending}</p>
              </div>
              <Clock className="w-8 h-8 text-yellow-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">قيد التنفيذ</p>
                <p className="text-2xl font-bold text-primary">{statusCounts.in_progress}</p>
              </div>
              <Truck className="w-8 h-8 text-primary/100" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">مكتملة</p>
                <p className="text-2xl font-bold text-primary">{statusCounts.completed}</p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">ملغية</p>
                <p className="text-2xl font-bold text-destructive">{statusCounts.cancelled}</p>
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
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  id="search"
                  placeholder="البحث برقم الطلب، اسم العميل، العنوان، أو السائق..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>

            <div className="min-w-48">
              <Label htmlFor="type-filter">نوع الطلب</Label>
              <Select value={filterType} onValueChange={setFilterType}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر نوع الطلب" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع الأنواع</SelectItem>
                  <SelectItem value="delivery">توصيل</SelectItem>
                  <SelectItem value="pickup">استلام</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="min-w-48">
              <Label htmlFor="status-filter">الحالة</Label>
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر الحالة" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع الحالات</SelectItem>
                  <SelectItem value="pending">في الانتظار</SelectItem>
                  <SelectItem value="in_progress">قيد التنفيذ</SelectItem>
                  <SelectItem value="completed">مكتمل</SelectItem>
                  <SelectItem value="cancelled">ملغي</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Orders Table */}
      <Card>
        <CardHeader>
          <CardTitle>قائمة الطلبات ({filteredOrders.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>رقم الطلب</TableHead>
                  <TableHead>النوع</TableHead>
                  <TableHead>العميل</TableHead>
                  <TableHead>العنوان</TableHead>
                  <TableHead>الموعد المحدد</TableHead>
                  <TableHead>السائق</TableHead>
                  <TableHead>الحالة</TableHead>
                  <TableHead>الإجراءات</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredOrders.map((order) => (
                  <TableRow key={order.id}>
                    <TableCell>
                      <div className="font-medium">{order.orderNumber}</div>
                      <div className="text-sm text-gray-500">
                        {new Date(order.createdAt).toLocaleDateString('ar-SA')}
                      </div>
                    </TableCell>
                    <TableCell>
                      {getTypeBadge(order.type)}
                    </TableCell>
                    <TableCell>
                      <div>
                        <div className="font-medium">{order.customerName}</div>
                        <div className="text-sm text-gray-500 flex items-center gap-1">
                          <Phone className="w-3 h-3" />
                          {order.customerPhone}
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-start gap-1 max-w-xs">
                        <MapPin className="w-3 h-3 mt-1 text-gray-500 flex-shrink-0" />
                        <span className="text-sm">{order.address}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-1">
                        <Calendar className="w-3 h-3 text-gray-500" />
                        <div className="text-sm">
                          <div>{new Date(order.scheduledDate).toLocaleDateString('ar-SA')}</div>
                          <div className="text-gray-500">{order.scheduledTime}</div>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      {order.driverName ? (
                        <div>
                          <div className="font-medium flex items-center gap-1">
                            <User className="w-3 h-3" />
                            {order.driverName}
                          </div>
                          <div className="text-sm text-gray-500">{order.vehicleNumber}</div>
                        </div>
                      ) : (
                        <span className="text-gray-400">غير محدد</span>
                      )}
                    </TableCell>
                    <TableCell>
                      {getStatusBadge(order.status)}
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-1">
                        {order.status === 'pending' && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleUpdateStatus(order.id, 'in_progress')}
                            className="text-primary hover:text-primary/90"
                          >
                            بدء
                          </Button>
                        )}
                        {order.status === 'in_progress' && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleUpdateStatus(order.id, 'completed')}
                            className="text-primary hover:text-primary"
                          >
                            إكمال
                          </Button>
                        )}
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleEditOrder(order)}
                        >
                          <Edit className="w-4 h-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setSelectedOrder(order)}
                        >
                          <Eye className="w-4 h-4" />
                        </Button>
                        {order.status === 'pending' && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleDeleteOrder(order.id)}
                            className="text-destructive hover:text-destructive"
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        )}
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>

          {filteredOrders.length === 0 && (
            <div className="text-center py-8">
              <Truck className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">لا توجد طلبات تطابق معايير البحث</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default PickupDeliveryOrders;