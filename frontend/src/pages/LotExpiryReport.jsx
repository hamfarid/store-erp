/**
 * Lot Expiry Report Page
 * تقرير انتهاء صلاحية اللوتات
 * 
 * @file frontend/src/pages/LotExpiryReport.jsx
 * @author Store ERP v2.0.0
 */

import React, { useState, useEffect } from 'react';
import {
  AlertTriangle, Calendar, Package, Download, FileText,
  RefreshCw, Clock, CheckCircle, XCircle, Filter, Search
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

// Export utilities
import { exportToCSV, exportToExcel } from '../utils/export';
import { exportLotExpiryPDF } from '../utils/pdfExport';

/**
 * تقرير انتهاء صلاحية اللوتات
 */
const LotExpiryReport = () => {
  const [lots, setLots] = useState([]);
  const [filteredLots, setFilteredLots] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [daysFilter, setDaysFilter] = useState('30');
  const [statusFilter, setStatusFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  // Sample data
  const sampleLots = [
    {
      id: 1,
      lotNumber: 'LOT-2024-001',
      productName: 'حبر طابعة HP 123',
      productSku: 'HP-INK-123',
      quantity: 50,
      warehouseName: 'المستودع الرئيسي',
      expiryDate: '2024-02-15',
      daysRemaining: 30,
      status: 'warning'
    },
    {
      id: 2,
      lotNumber: 'LOT-2024-002',
      productName: 'بطاريات Duracell AA',
      productSku: 'DUR-AA-12',
      quantity: 200,
      warehouseName: 'المستودع الرئيسي',
      expiryDate: '2024-02-01',
      daysRemaining: 15,
      status: 'warning'
    },
    {
      id: 3,
      lotNumber: 'LOT-2023-055',
      productName: 'مواد تنظيف صناعية',
      productSku: 'CLN-IND-001',
      quantity: 25,
      warehouseName: 'مستودع الفرع',
      expiryDate: '2024-01-10',
      daysRemaining: -5,
      status: 'expired'
    },
    {
      id: 4,
      lotNumber: 'LOT-2024-003',
      productName: 'زيت ماكينات',
      productSku: 'OIL-MCH-500',
      quantity: 30,
      warehouseName: 'المستودع الرئيسي',
      expiryDate: '2024-03-30',
      daysRemaining: 74,
      status: 'active'
    },
    {
      id: 5,
      lotNumber: 'LOT-2024-004',
      productName: 'أدوات مكتبية متنوعة',
      productSku: 'OFF-MIX-001',
      quantity: 100,
      warehouseName: 'المستودع الرئيسي',
      expiryDate: '2024-01-25',
      daysRemaining: 10,
      status: 'warning'
    }
  ];

  useEffect(() => {
    fetchLots();
  }, [daysFilter]);

  useEffect(() => {
    applyFilters();
  }, [lots, statusFilter, searchTerm]);

  const fetchLots = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.get('/api/reports/inventory/expiring-lots', {
        params: { days: parseInt(daysFilter) }
      });
      if (response.status === 'success' && response.data) {
        setLots(response.data);
      } else {
        setLots(sampleLots);
      }
    } catch (error) {
      console.log('Using sample data:', error);
      setLots(sampleLots);
    } finally {
      setIsLoading(false);
    }
  };

  const applyFilters = () => {
    let result = [...lots];

    // Status filter
    if (statusFilter !== 'all') {
      result = result.filter(lot => lot.status === statusFilter);
    }

    // Search filter
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      result = result.filter(lot =>
        lot.lotNumber?.toLowerCase().includes(term) ||
        lot.productName?.toLowerCase().includes(term) ||
        lot.productSku?.toLowerCase().includes(term)
      );
    }

    setFilteredLots(result);
  };

  const handleRefresh = () => {
    fetchLots();
    toast.success('تم تحديث التقرير');
  };

  const handleExportPDF = async () => {
    await exportLotExpiryPDF(filteredLots, daysFilter);
  };

  const handleExportExcel = () => {
    const data = filteredLots.map(lot => ({
      'رقم اللوت': lot.lotNumber,
      'المنتج': lot.productName,
      'SKU': lot.productSku,
      'الكمية': lot.quantity,
      'المستودع': lot.warehouseName,
      'تاريخ الانتهاء': lot.expiryDate,
      'أيام متبقية': lot.daysRemaining,
      'الحالة': getStatusLabel(lot.status)
    }));
    exportToExcel('lot-expiry-report', data, { sheetName: 'Lot Expiry' });
  };

  const handleExportCSV = () => {
    const data = filteredLots.map(lot => ({
      lot_number: lot.lotNumber,
      product_name: lot.productName,
      product_sku: lot.productSku,
      quantity: lot.quantity,
      warehouse: lot.warehouseName,
      expiry_date: lot.expiryDate,
      days_remaining: lot.daysRemaining,
      status: lot.status
    }));
    exportToCSV('lot-expiry-report.csv', data);
  };

  const getStatusLabel = (status) => {
    switch (status) {
      case 'expired': return 'منتهي';
      case 'warning': return 'قريب الانتهاء';
      case 'active': return 'نشط';
      default: return status;
    }
  };

  const getStatusBadge = (status, daysRemaining) => {
    if (status === 'expired' || daysRemaining < 0) {
      return (
        <Badge variant="destructive" className="flex items-center gap-1">
          <XCircle className="w-3 h-3" />
          منتهي
        </Badge>
      );
    }
    if (status === 'warning' || daysRemaining <= 30) {
      return (
        <Badge variant="warning" className="flex items-center gap-1 bg-yellow-500">
          <AlertTriangle className="w-3 h-3" />
          قريب الانتهاء
        </Badge>
      );
    }
    return (
      <Badge variant="default" className="flex items-center gap-1 bg-green-500">
        <CheckCircle className="w-3 h-3" />
        نشط
      </Badge>
    );
  };

  // Statistics
  const stats = {
    total: filteredLots.length,
    expired: filteredLots.filter(l => l.status === 'expired' || l.daysRemaining < 0).length,
    warning: filteredLots.filter(l => l.status === 'warning' && l.daysRemaining >= 0 && l.daysRemaining <= 30).length,
    active: filteredLots.filter(l => l.status === 'active' || l.daysRemaining > 30).length,
    totalQuantity: filteredLots.reduce((sum, l) => sum + (l.quantity || 0), 0)
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

  return (
    <div className="p-6 space-y-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground flex items-center gap-2">
            <Calendar className="w-8 h-8" />
            تقرير انتهاء صلاحية اللوتات
          </h1>
          <p className="text-muted-foreground mt-1">متابعة تواريخ انتهاء صلاحية المنتجات</p>
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
            onClick={handleExportPDF}
            className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors"
          >
            <FileText className="w-4 h-4" />
            PDF
          </button>
          <button 
            onClick={handleExportExcel}
            className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
          >
            <Download className="w-4 h-4" />
            Excel
          </button>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي اللوتات</p>
                <p className="text-2xl font-bold">{stats.total}</p>
              </div>
              <Package className="w-8 h-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-red-50 dark:bg-red-900/20">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">منتهية الصلاحية</p>
                <p className="text-2xl font-bold text-red-600">{stats.expired}</p>
              </div>
              <XCircle className="w-8 h-8 text-red-500" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-yellow-50 dark:bg-yellow-900/20">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">قريبة الانتهاء</p>
                <p className="text-2xl font-bold text-yellow-600">{stats.warning}</p>
              </div>
              <AlertTriangle className="w-8 h-8 text-yellow-500" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-green-50 dark:bg-green-900/20">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">نشطة</p>
                <p className="text-2xl font-bold text-green-600">{stats.active}</p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي الكمية</p>
                <p className="text-2xl font-bold">{stats.totalQuantity.toLocaleString('ar-SA')}</p>
              </div>
              <Package className="w-8 h-8 text-purple-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-wrap gap-4 items-end">
            <div className="min-w-48">
              <Label htmlFor="search">بحث</Label>
              <div className="relative">
                <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  id="search"
                  placeholder="رقم اللوت أو المنتج..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>
            <div className="min-w-40">
              <Label htmlFor="days">فترة الانتهاء</Label>
              <Select value={daysFilter} onValueChange={setDaysFilter}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر الفترة" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="7">7 أيام</SelectItem>
                  <SelectItem value="15">15 يوم</SelectItem>
                  <SelectItem value="30">30 يوم</SelectItem>
                  <SelectItem value="60">60 يوم</SelectItem>
                  <SelectItem value="90">90 يوم</SelectItem>
                  <SelectItem value="180">180 يوم</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="min-w-40">
              <Label htmlFor="status">الحالة</Label>
              <Select value={statusFilter} onValueChange={setStatusFilter}>
                <SelectTrigger>
                  <SelectValue placeholder="جميع الحالات" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع الحالات</SelectItem>
                  <SelectItem value="expired">منتهي</SelectItem>
                  <SelectItem value="warning">قريب الانتهاء</SelectItem>
                  <SelectItem value="active">نشط</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Data Table */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="w-5 h-5" />
            اللوتات المتأثرة ({filteredLots.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>رقم اللوت</TableHead>
                <TableHead>المنتج</TableHead>
                <TableHead>SKU</TableHead>
                <TableHead>الكمية</TableHead>
                <TableHead>المستودع</TableHead>
                <TableHead>تاريخ الانتهاء</TableHead>
                <TableHead>أيام متبقية</TableHead>
                <TableHead>الحالة</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredLots.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={8} className="text-center py-10 text-muted-foreground">
                    لا توجد لوتات تنتهي خلال الفترة المحددة
                  </TableCell>
                </TableRow>
              ) : (
                filteredLots.map((lot) => (
                  <TableRow key={lot.id} className={
                    lot.daysRemaining < 0 ? 'bg-red-50 dark:bg-red-900/10' :
                    lot.daysRemaining <= 7 ? 'bg-orange-50 dark:bg-orange-900/10' :
                    lot.daysRemaining <= 30 ? 'bg-yellow-50 dark:bg-yellow-900/10' : ''
                  }>
                    <TableCell className="font-mono font-medium">{lot.lotNumber}</TableCell>
                    <TableCell>{lot.productName}</TableCell>
                    <TableCell className="font-mono text-sm">{lot.productSku}</TableCell>
                    <TableCell>{lot.quantity?.toLocaleString('ar-SA')}</TableCell>
                    <TableCell>{lot.warehouseName}</TableCell>
                    <TableCell>{lot.expiryDate}</TableCell>
                    <TableCell className={
                      lot.daysRemaining < 0 ? 'text-red-600 font-bold' :
                      lot.daysRemaining <= 7 ? 'text-orange-600 font-bold' :
                      lot.daysRemaining <= 30 ? 'text-yellow-600 font-bold' :
                      'text-green-600'
                    }>
                      {lot.daysRemaining < 0 
                        ? `متأخر ${Math.abs(lot.daysRemaining)} يوم`
                        : `${lot.daysRemaining} يوم`
                      }
                    </TableCell>
                    <TableCell>{getStatusBadge(lot.status, lot.daysRemaining)}</TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Legend */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-wrap gap-6 items-center text-sm">
            <span className="text-muted-foreground">دليل الألوان:</span>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded bg-red-200"></div>
              <span>منتهي الصلاحية</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded bg-orange-200"></div>
              <span>أقل من 7 أيام</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded bg-yellow-200"></div>
              <span>أقل من 30 يوم</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded bg-green-200"></div>
              <span>أكثر من 30 يوم</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default LotExpiryReport;
