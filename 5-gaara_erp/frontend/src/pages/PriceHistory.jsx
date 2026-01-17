import React, { useState, useEffect } from 'react';
import {
  TrendingUp, TrendingDown, Search, Filter, Calendar, Package,
  DollarSign, History, BarChart3, ArrowUpRight, ArrowDownRight,
  Minus, Download
} from 'lucide-react';
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
 * صفحة سجل الأسعار
 * Price History Page
 */
const PriceHistory = () => {
  const [priceHistory, setPriceHistory] = useState([]);
  const [filteredHistory, setFilteredHistory] = useState([]);
  const [products, setProducts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterProduct, setFilterProduct] = useState('all');
  const [filterPriceType, setFilterPriceType] = useState('all');
  const [dateRange, setDateRange] = useState({ start: '', end: '' });
  const [isLoading, setIsLoading] = useState(true);

  // بيانات نموذجية
  const sampleHistory = [
    {
      id: 1,
      product_id: 1,
      product_name: 'لابتوب HP ProBook',
      product_sku: 'HP-PB-001',
      price_type: 'sell',
      old_price: 4500,
      new_price: 4800,
      change_percent: 6.67,
      reason: 'زيادة تكلفة الاستيراد',
      changed_by: 'أحمد محمد',
      changed_at: '2024-01-15T10:30:00'
    },
    {
      id: 2,
      product_id: 1,
      product_name: 'لابتوب HP ProBook',
      product_sku: 'HP-PB-001',
      price_type: 'buy',
      old_price: 3800,
      new_price: 4000,
      change_percent: 5.26,
      reason: 'تحديث أسعار الموردين',
      changed_by: 'سارة محمد',
      changed_at: '2024-01-14T09:15:00'
    },
    {
      id: 3,
      product_id: 2,
      product_name: 'طابعة Canon',
      product_sku: 'CN-PR-001',
      price_type: 'sell',
      old_price: 1200,
      new_price: 1100,
      change_percent: -8.33,
      reason: 'عرض خاص',
      changed_by: 'محمد علي',
      changed_at: '2024-01-13T14:00:00'
    },
    {
      id: 4,
      product_id: 3,
      product_name: 'شاشة Samsung 24"',
      product_sku: 'SM-MN-024',
      price_type: 'sell',
      old_price: 800,
      new_price: 850,
      change_percent: 6.25,
      reason: 'تعديل هامش الربح',
      changed_by: 'أحمد محمد',
      changed_at: '2024-01-12T11:45:00'
    },
    {
      id: 5,
      product_id: 4,
      product_name: 'ماوس لاسلكي',
      product_sku: 'MS-WL-001',
      price_type: 'buy',
      old_price: 50,
      new_price: 45,
      change_percent: -10,
      reason: 'خصم من المورد',
      changed_by: 'خالد العلي',
      changed_at: '2024-01-11T16:30:00'
    },
    {
      id: 6,
      product_id: 4,
      product_name: 'ماوس لاسلكي',
      product_sku: 'MS-WL-001',
      price_type: 'sell',
      old_price: 80,
      new_price: 75,
      change_percent: -6.25,
      reason: 'تخفيض تنافسي',
      changed_by: 'سارة محمد',
      changed_at: '2024-01-11T16:35:00'
    },
    {
      id: 7,
      product_id: 5,
      product_name: 'كيبورد ميكانيكي',
      product_sku: 'KB-MC-001',
      price_type: 'sell',
      old_price: 350,
      new_price: 350,
      change_percent: 0,
      reason: 'مراجعة دورية - لا تغيير',
      changed_by: 'محمد علي',
      changed_at: '2024-01-10T09:00:00'
    },
    {
      id: 8,
      product_id: 2,
      product_name: 'طابعة Canon',
      product_sku: 'CN-PR-001',
      price_type: 'buy',
      old_price: 950,
      new_price: 900,
      change_percent: -5.26,
      reason: 'عقد جديد مع المورد',
      changed_by: 'خالد العلي',
      changed_at: '2024-01-09T13:20:00'
    }
  ];

  const sampleProducts = [
    { id: 1, name: 'لابتوب HP ProBook', sku: 'HP-PB-001' },
    { id: 2, name: 'طابعة Canon', sku: 'CN-PR-001' },
    { id: 3, name: 'شاشة Samsung 24"', sku: 'SM-MN-024' },
    { id: 4, name: 'ماوس لاسلكي', sku: 'MS-WL-001' },
    { id: 5, name: 'كيبورد ميكانيكي', sku: 'KB-MC-001' }
  ];

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const [historyResponse, productsResponse] = await Promise.all([
        apiClient.get('/api/price-history'),
        apiClient.get('/api/products')
      ]);

      if (historyResponse.success && historyResponse.data?.length > 0) {
        setPriceHistory(historyResponse.data);
        setFilteredHistory(historyResponse.data);
      } else {
        setPriceHistory(sampleHistory);
        setFilteredHistory(sampleHistory);
      }

      if (productsResponse.success && productsResponse.data?.length > 0) {
        setProducts(productsResponse.data);
      } else {
        setProducts(sampleProducts);
      }
    } catch (error) {
      console.log('Using sample data:', error);
      setPriceHistory(sampleHistory);
      setFilteredHistory(sampleHistory);
      setProducts(sampleProducts);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let filtered = priceHistory;

    if (searchTerm) {
      filtered = filtered.filter(h =>
        h.product_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        h.product_sku.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterProduct !== 'all') {
      filtered = filtered.filter(h => h.product_id === parseInt(filterProduct));
    }

    if (filterPriceType !== 'all') {
      filtered = filtered.filter(h => h.price_type === filterPriceType);
    }

    if (dateRange.start) {
      filtered = filtered.filter(h => new Date(h.changed_at) >= new Date(dateRange.start));
    }

    if (dateRange.end) {
      filtered = filtered.filter(h => new Date(h.changed_at) <= new Date(dateRange.end));
    }

    setFilteredHistory(filtered);
  }, [priceHistory, searchTerm, filterProduct, filterPriceType, dateRange]);

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('ar-SA', {
      style: 'currency',
      currency: 'SAR',
      minimumFractionDigits: 0
    }).format(amount);
  };

  const getChangeIcon = (percent) => {
    if (percent > 0) return <ArrowUpRight className="w-4 h-4 text-red-500" />;
    if (percent < 0) return <ArrowDownRight className="w-4 h-4 text-green-500" />;
    return <Minus className="w-4 h-4 text-gray-500" />;
  };

  const getChangeColor = (percent) => {
    if (percent > 0) return 'text-red-600 bg-red-50';
    if (percent < 0) return 'text-green-600 bg-green-50';
    return 'text-gray-600 bg-gray-50';
  };

  const getPriceTypeBadge = (type) => {
    if (type === 'sell') {
      return <Badge className="bg-blue-100 text-blue-800">سعر البيع</Badge>;
    }
    return <Badge className="bg-purple-100 text-purple-800">سعر الشراء</Badge>;
  };

  // Calculate summary
  const summary = {
    totalChanges: priceHistory.length,
    increases: priceHistory.filter(h => h.change_percent > 0).length,
    decreases: priceHistory.filter(h => h.change_percent < 0).length,
    noChange: priceHistory.filter(h => h.change_percent === 0).length,
    avgChangePercent: priceHistory.length > 0
      ? (priceHistory.reduce((sum, h) => sum + h.change_percent, 0) / priceHistory.length).toFixed(2)
      : 0
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">جاري التحميل...</p>
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
            <History className="w-8 h-8" />
            سجل الأسعار
          </h1>
          <p className="text-muted-foreground mt-1">تتبع تغييرات أسعار المنتجات</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors">
          <Download className="w-4 h-4" />
          تصدير التقرير
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي التغييرات</p>
                <p className="text-2xl font-bold text-primary">{summary.totalChanges}</p>
              </div>
              <History className="w-8 h-8 text-primary/60" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">زيادات السعر</p>
                <p className="text-2xl font-bold text-red-600">{summary.increases}</p>
              </div>
              <TrendingUp className="w-8 h-8 text-red-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">تخفيضات السعر</p>
                <p className="text-2xl font-bold text-green-600">{summary.decreases}</p>
              </div>
              <TrendingDown className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">بدون تغيير</p>
                <p className="text-2xl font-bold text-gray-600">{summary.noChange}</p>
              </div>
              <Minus className="w-8 h-8 text-gray-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">متوسط التغيير</p>
                <p className={`text-2xl font-bold ${parseFloat(summary.avgChangePercent) >= 0 ? 'text-red-600' : 'text-green-600'}`}>
                  {summary.avgChangePercent}%
                </p>
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
                  placeholder="البحث باسم المنتج أو الكود..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>

            <div className="min-w-48">
              <Label htmlFor="product-filter">المنتج</Label>
              <Select value={filterProduct} onValueChange={setFilterProduct}>
                <SelectTrigger>
                  <SelectValue placeholder="الكل" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع المنتجات</SelectItem>
                  {products.map(product => (
                    <SelectItem key={product.id} value={product.id.toString()}>
                      {product.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="min-w-32">
              <Label htmlFor="type-filter">نوع السعر</Label>
              <Select value={filterPriceType} onValueChange={setFilterPriceType}>
                <SelectTrigger>
                  <SelectValue placeholder="الكل" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">الكل</SelectItem>
                  <SelectItem value="sell">سعر البيع</SelectItem>
                  <SelectItem value="buy">سعر الشراء</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="min-w-36">
              <Label htmlFor="date-start">من تاريخ</Label>
              <Input
                id="date-start"
                type="date"
                value={dateRange.start}
                onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
              />
            </div>

            <div className="min-w-36">
              <Label htmlFor="date-end">إلى تاريخ</Label>
              <Input
                id="date-end"
                type="date"
                value={dateRange.end}
                onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })}
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Price History Table */}
      <Card>
        <CardHeader>
          <CardTitle>سجل تغييرات الأسعار ({filteredHistory.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>المنتج</TableHead>
                <TableHead>نوع السعر</TableHead>
                <TableHead>السعر القديم</TableHead>
                <TableHead>السعر الجديد</TableHead>
                <TableHead>التغيير</TableHead>
                <TableHead>السبب</TableHead>
                <TableHead>بواسطة</TableHead>
                <TableHead>التاريخ</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredHistory.map((record) => (
                <TableRow key={record.id}>
                  <TableCell>
                    <div>
                      <div className="font-medium flex items-center gap-1">
                        <Package className="w-4 h-4 text-muted-foreground" />
                        {record.product_name}
                      </div>
                      <div className="text-sm text-muted-foreground font-mono">
                        {record.product_sku}
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>{getPriceTypeBadge(record.price_type)}</TableCell>
                  <TableCell className="font-mono">
                    {formatCurrency(record.old_price)}
                  </TableCell>
                  <TableCell className="font-mono font-bold">
                    {formatCurrency(record.new_price)}
                  </TableCell>
                  <TableCell>
                    <div className={`inline-flex items-center gap-1 px-2 py-1 rounded ${getChangeColor(record.change_percent)}`}>
                      {getChangeIcon(record.change_percent)}
                      <span className="font-bold">
                        {record.change_percent > 0 ? '+' : ''}{record.change_percent.toFixed(2)}%
                      </span>
                    </div>
                  </TableCell>
                  <TableCell className="max-w-xs">
                    <p className="truncate" title={record.reason}>{record.reason}</p>
                  </TableCell>
                  <TableCell>{record.changed_by}</TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1 text-sm">
                      <Calendar className="w-3 h-3 text-muted-foreground" />
                      {new Date(record.changed_at).toLocaleString('ar-SA')}
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>

          {filteredHistory.length === 0 && (
            <div className="text-center py-8">
              <History className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">لا توجد تغييرات في الأسعار</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default PriceHistory;

