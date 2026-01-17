import React, { useState, useEffect } from 'react';
import {
Warehouse,
  Package,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Settings,
  BarChart3,
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

const WarehouseConstraints = () => {
  const [constraints, setConstraints] = useState([]);
  const [filteredConstraints, setFilteredConstraints] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedConstraint, setSelectedConstraint] = useState(null);

  // Sample data
  const sampleConstraints = [
    {
      id: 1,
      warehouseName: 'المخزن الرئيسي',
      warehouseId: 1,
      constraintType: 'capacity',
      constraintName: 'الحد الأقصى للسعة',
      currentValue: 850,
      maxValue: 1000,
      minValue: 0,
      unit: 'قطعة',
      status: 'warning',
      description: 'تحذير عند الوصول إلى 85% من السعة',
      lastChecked: '2024-01-15T10:30:00',
      isActive: true
    },
    {
      id: 2,
      warehouseName: 'مخزن الإلكترونيات',
      warehouseId: 2,
      constraintType: 'temperature',
      constraintName: 'درجة الحرارة',
      currentValue: 22,
      maxValue: 25,
      minValue: 18,
      unit: '°C',
      status: 'ok',
      description: 'مراقبة درجة الحرارة للمنتجات الحساسة',
      lastChecked: '2024-01-15T11:00:00',
      isActive: true
    },
    {
      id: 3,
      warehouseName: 'مخزن المواد الغذائية',
      warehouseId: 3,
      constraintType: 'humidity',
      constraintName: 'الرطوبة',
      currentValue: 65,
      maxValue: 60,
      minValue: 40,
      unit: '%',
      status: 'critical',
      description: 'مستوى الرطوبة مرتفع جداً',
      lastChecked: '2024-01-15T11:15:00',
      isActive: true
    },
    {
      id: 4,
      warehouseName: 'المخزن الرئيسي',
      warehouseId: 1,
      constraintType: 'weight',
      constraintName: 'الوزن الإجمالي',
      currentValue: 4500,
      maxValue: 5000,
      minValue: 0,
      unit: 'كيلو',
      status: 'warning',
      description: 'تحذير عند الاقتراب من الحد الأقصى للوزن',
      lastChecked: '2024-01-15T09:45:00',
      isActive: true
    }
  ];

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setConstraints(sampleConstraints);
      setFilteredConstraints(sampleConstraints);
      setIsLoading(false);
    }, 1000);
  }, []);

  useEffect(() => {
    let filtered = constraints;

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(constraint =>
        constraint.warehouseName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        constraint.constraintName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        constraint.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Filter by type
    if (filterType !== 'all') {
      filtered = filtered.filter(constraint => constraint.constraintType === filterType);
    }

    // Filter by status
    if (filterStatus !== 'all') {
      filtered = filtered.filter(constraint => constraint.status === filterStatus);
    }

    setFilteredConstraints(filtered);
  }, [constraints, searchTerm, filterType, filterStatus]);

  const getStatusBadge = (status) => {
    const statusConfig = {
      ok: { label: 'طبيعي', variant: 'default', icon: CheckCircle, color: 'text-primary' },
      warning: { label: 'تحذير', variant: 'secondary', icon: AlertTriangle, color: 'text-accent' },
      critical: { label: 'حرج', variant: 'destructive', icon: XCircle, color: 'text-destructive' }
    };

    const config = statusConfig[status] || statusConfig.ok;
    const IconComponent = config.icon;
    
    return (
      <Badge variant={config.variant} className="flex items-center gap-1">
        <IconComponent className="w-3 h-3" />
        {config.label}
      </Badge>
    );
  };

  const getConstraintTypeLabel = (type) => {
    const types = {
      capacity: 'السعة',
      temperature: 'درجة الحرارة',
      humidity: 'الرطوبة',
      weight: 'الوزن',
      security: 'الأمان',
      access: 'الوصول'
    };
    return types[type] || type;
  };

  const getConstraintTypeIcon = (type) => {
    const icons = {
      capacity: Package,
      temperature: BarChart3,
      humidity: BarChart3,
      weight: BarChart3,
      security: Settings,
      access: Settings
    };
    return icons[type] || Settings;
  };

  const getProgressPercentage = (current, min, max) => {
    if (max === min) return 0;
    return ((current - min) / (max - min)) * 100;
  };

  const getProgressColor = (status) => {
    const colors = {
      ok: 'bg-primary/100',
      warning: 'bg-accent/100',
      critical: 'bg-destructive/100'
    };
    return colors[status] || 'bg-muted/500';
  };

  const handleAddConstraint = () => {
    setSelectedConstraint(null);
    setShowAddModal(true);
  };

  const handleEditConstraint = (constraint) => {
    setSelectedConstraint(constraint);
    setShowAddModal(true);
  };

  const handleDeleteConstraint = (constraintId) => {
    if (window.confirm('هل أنت متأكد من حذف هذا القيد؟')) {
      setConstraints(constraints.filter(constraint => constraint.id !== constraintId));
      toast.success('تم حذف القيد بنجاح');
    }
  };

  const handleToggleConstraint = (constraintId) => {
    setConstraints(constraints.map(constraint =>
      constraint.id === constraintId
        ? { ...constraint, isActive: !constraint.isActive }
        : constraint
    ));
    toast.success('تم تحديث حالة القيد');
  };

  const handleExport = () => {
    toast.success('تم تصدير البيانات بنجاح');
  };

  const getStatusCounts = () => {
    return {
      total: constraints.length,
      ok: constraints.filter(c => c.status === 'ok').length,
      warning: constraints.filter(c => c.status === 'warning').length,
      critical: constraints.filter(c => c.status === 'critical').length
    };
  };

  const statusCounts = getStatusCounts();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل قيود المخازن...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">قيود المخازن</h1>
          <p className="text-muted-foreground mt-1">مراقبة وإدارة قيود وحدود المخازن</p>
        </div>
        <div className="flex gap-2">
          <Button onClick={handleExport} variant="outline">
            <Download className="w-4 h-4 mr-2" />
            تصدير
          </Button>
          <Button onClick={handleAddConstraint}>
            <Plus className="w-4 h-4 mr-2" />
            إضافة قيد جديد
          </Button>
        </div>
      </div>

      {/* Status Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي القيود</p>
                <p className="text-2xl font-bold text-primary">{statusCounts.total}</p>
              </div>
              <Warehouse className="w-8 h-8 text-primary/100" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">حالة طبيعية</p>
                <p className="text-2xl font-bold text-primary">{statusCounts.ok}</p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">تحذيرات</p>
                <p className="text-2xl font-bold text-accent">{statusCounts.warning}</p>
              </div>
              <AlertTriangle className="w-8 h-8 text-yellow-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">حالات حرجة</p>
                <p className="text-2xl font-bold text-destructive">{statusCounts.critical}</p>
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
                  placeholder="البحث بالمخزن، نوع القيد، أو الوصف..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>

            <div className="min-w-48">
              <Label htmlFor="type-filter">نوع القيد</Label>
              <Select value={filterType} onValueChange={setFilterType}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر نوع القيد" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع الأنواع</SelectItem>
                  <SelectItem value="capacity">السعة</SelectItem>
                  <SelectItem value="temperature">درجة الحرارة</SelectItem>
                  <SelectItem value="humidity">الرطوبة</SelectItem>
                  <SelectItem value="weight">الوزن</SelectItem>
                  <SelectItem value="security">الأمان</SelectItem>
                  <SelectItem value="access">الوصول</SelectItem>
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
                  <SelectItem value="ok">طبيعي</SelectItem>
                  <SelectItem value="warning">تحذير</SelectItem>
                  <SelectItem value="critical">حرج</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Constraints Table */}
      <Card>
        <CardHeader>
          <CardTitle>قائمة القيود ({filteredConstraints.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>المخزن</TableHead>
                  <TableHead>نوع القيد</TableHead>
                  <TableHead>القيمة الحالية</TableHead>
                  <TableHead>النطاق المسموح</TableHead>
                  <TableHead>التقدم</TableHead>
                  <TableHead>الحالة</TableHead>
                  <TableHead>آخر فحص</TableHead>
                  <TableHead>الإجراءات</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredConstraints.map((constraint) => {
                  const TypeIcon = getConstraintTypeIcon(constraint.constraintType);
                  const progressPercentage = getProgressPercentage(
                    constraint.currentValue,
                    constraint.minValue,
                    constraint.maxValue
                  );
                  
                  return (
                    <TableRow key={constraint.id} className={!constraint.isActive ? 'opacity-50' : ''}>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <Warehouse className="w-4 h-4 text-gray-500" />
                          <div>
                            <div className="font-medium">{constraint.warehouseName}</div>
                            <div className="text-sm text-gray-500">{constraint.constraintName}</div>
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <TypeIcon className="w-4 h-4 text-gray-500" />
                          <Badge variant="outline">
                            {getConstraintTypeLabel(constraint.constraintType)}
                          </Badge>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="font-medium">
                          {constraint.currentValue} {constraint.unit}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="text-sm">
                          <div>{constraint.minValue} - {constraint.maxValue} {constraint.unit}</div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="w-full">
                          <div className="flex justify-between text-xs mb-1">
                            <span>{constraint.minValue}</span>
                            <span>{constraint.maxValue}</span>
                          </div>
                          <div className="w-full bg-muted rounded-full h-2">
                            <div
                              className={`h-2 rounded-full ${getProgressColor(constraint.status)}`}
                              style={{ width: `${Math.min(100, Math.max(0, progressPercentage))}%` }}
                            ></div>
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        {getStatusBadge(constraint.status)}
                      </TableCell>
                      <TableCell>
                        <div className="text-sm">
                          {new Date(constraint.lastChecked).toLocaleString('ar-SA')}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex gap-1">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleToggleConstraint(constraint.id)}
                            className={constraint.isActive ? 'text-accent' : 'text-primary'}
                          >
                            {constraint.isActive ? '⏸️' : '▶️'}
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleEditConstraint(constraint)}
                          >
                            <Edit className="w-4 h-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => setSelectedConstraint(constraint)}
                          >
                            <Eye className="w-4 h-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleDeleteConstraint(constraint.id)}
                            className="text-destructive hover:text-destructive"
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </div>

          {filteredConstraints.length === 0 && (
            <div className="text-center py-8">
              <Warehouse className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">لا توجد قيود تطابق معايير البحث</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default WarehouseConstraints;