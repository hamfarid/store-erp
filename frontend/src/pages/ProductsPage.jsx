/**
 * Modern Products Page
 * 
 * A beautiful, professional products management page with modern UI/UX using ShadCN components.
 */

import React, { useState, useEffect } from 'react';
import {
  Search,
  Plus,
  Filter,
  Download,
  Upload,
  Grid,
  List,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  Package,
  AlertTriangle,
  CheckCircle,
  XCircle,
  ArrowUpDown,
  ChevronRight,
  ChevronLeft,
  SlidersHorizontal,
  Tag,
  Barcode,
  RefreshCw
} from 'lucide-react';

import { productService } from '../services/productService';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Badge } from '../components/ui/badge';
import { 
  Card, 
  CardContent, 
  CardHeader, 
  CardTitle, 
  CardDescription,
  CardFooter 
} from '../components/ui/card';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../components/ui/table';
import LoadingSpinner from '../components/LoadingSpinner';

// ============================================================================
// Status Badge Component
// ============================================================================

// ============================================================================
// Status Badge Component
// ============================================================================

const StatusBadge = ({ status, stock, minStock }) => {
  let variant = 'default';
  let label = 'متوفر';
  let Icon = CheckCircle;

  // Use explicit status if available and valid
  if (status === 'out_of_stock' || stock <= 0) {
    variant = 'destructive'; // Red
    label = 'نفد المخزون';
    Icon = XCircle;
  } else if (status === 'low_stock' || stock <= minStock) {
    variant = 'warning'; // Yellow
    label = 'مخزون منخفض';
    Icon = AlertTriangle;
  } else {
    variant = 'success'; // Green
    label = 'متوفر';
    Icon = CheckCircle;
  }

  return (
    <Badge variant={variant} className="gap-1.5">
      <Icon size={12} />
      {label}
    </Badge>
  );
};
// ============================================================================
// Product Card Component (Grid View)
// ============================================================================

const ProductCard = ({ product, onView, onEdit, onDelete }) => (
  <Card hover className="overflow-hidden group border-border/50 bg-card">
    <div className="relative aspect-square bg-gradient-to-br from-muted/50 to-muted flex items-center justify-center">
      {product.image ? (
        <img src={product.image} alt={product.name} className="w-full h-full object-cover" />
      ) : (
        <Package className="w-16 h-16 text-muted-foreground/30" />
      )}
      
      {/* Quick Actions Overlay */}
      <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2 backdrop-blur-[2px]">
        <Button size="icon" variant="ghost" className="bg-background/90 hover:bg-background rounded-full" onClick={() => onView(product)}>
          <Eye size={18} />
        </Button>
        <Button size="icon" variant="ghost" className="bg-background/90 hover:bg-background rounded-full" onClick={() => onEdit(product)}>
          <Edit size={18} />
        </Button>
        <Button size="icon" variant="ghost" className="bg-background/90 hover:bg-background rounded-full text-destructive hover:text-destructive" onClick={() => onDelete(product)}>
          <Trash2 size={18} />
        </Button>
      </div>

      <div className="absolute top-3 right-3">
        <StatusBadge status={product.status} stock={product.stock} minStock={product.min_stock || 10} />
      </div>
    </div>

    <CardContent className="p-4">
      <div className="flex justify-between items-start mb-2">
        <div>
          <p className="text-xs text-muted-foreground font-mono mb-1">{product.sku}</p>
          <h3 className="font-semibold text-foreground truncate max-w-[180px]" title={product.name}>{product.name}</h3>
        </div>
      </div>
      
      <div className="flex items-center justify-between mt-4">
        <div>
          <p className="text-lg font-bold text-primary">{(product.price || 0).toLocaleString()} ج.م</p>
          <p className="text-xs text-muted-foreground">التكلفة: {(product.cost || 0).toLocaleString()} ج.م</p>
        </div>
        <div className="text-left">
          <p className={`text-lg font-bold ${product.stock <= (product.min_stock || 10) ? 'text-destructive' : 'text-foreground'}`}>
            {product.stock}
          </p>
          <p className="text-xs text-muted-foreground">في المخزون</p>
        </div>
      </div>
    </CardContent>
  </Card>
);

// ============================================================================
// Product Row Component (Table View)
// ============================================================================

const ProductRow = ({ product, onView, onEdit, onDelete }) => (
  <TableRow>
    <TableCell>
      <div className="flex items-center gap-4">
        <div className="w-10 h-10 rounded-lg bg-muted flex items-center justify-center flex-shrink-0 border border-border">
          {product.image ? (
            <img src={product.image} alt="" className="w-full h-full object-cover rounded-lg" />
          ) : (
            <Package className="text-muted-foreground/50" size={20} />
          )}
        </div>
        <div>
          <p className="font-medium text-foreground">{product.name}</p>
          <p className="text-xs text-muted-foreground font-mono">{product.sku}</p>
        </div>
      </div>
    </TableCell>
    <TableCell>
      <Badge variant="secondary" className="font-normal">
        {product.category?.name || product.category || 'غير مصنف'}
      </Badge>
    </TableCell>
    <TableCell>
      <div className="flex flex-col">
        <span className="font-semibold">{(product.price || 0).toLocaleString()} ج.م</span>
        <span className="text-xs text-muted-foreground">{(product.cost || 0).toLocaleString()} ج.م</span>
      </div>
    </TableCell>
    <TableCell>
      <div className="flex flex-col">
        <span className={`font-semibold ${product.stock <= (product.min_stock || 10) ? 'text-destructive' : ''}`}>
          {product.stock}
        </span>
        <span className="text-xs text-muted-foreground">الحد الأدنى: {product.min_stock || 10}</span>
      </div>
    </TableCell>
    <TableCell>
      <StatusBadge status={product.status} stock={product.stock} minStock={product.min_stock || 10} />
    </TableCell>
    <TableCell>
      <div className="flex items-center gap-1">
        <Button variant="ghost" size="icon" onClick={() => onView(product)}>
          <Eye size={16} />
        </Button>
        <Button variant="ghost" size="icon" onClick={() => onEdit(product)}>
          <Edit size={16} />
        </Button>
        <Button variant="ghost" size="icon" className="text-destructive hover:bg-destructive/10" onClick={() => onDelete(product)}>
          <Trash2 size={16} />
        </Button>
      </div>
    </TableCell>
  </TableRow>
);

// ============================================================================
// Main Products Page Component
// ============================================================================

const ProductsPage = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'table'
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [pagination, setPagination] = useState({ page: 1, limit: 12, total: 0, totalPages: 1 });
  
  // Fetch Stats
  const [stats, setStats] = useState({
    total: 0,
    inStock: 0,
    lowStock: 0,
    outOfStock: 0
  });

  const fetchProducts = React.useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      // Fetch products with filters
      const response = await productService.getAll({
        page: pagination.page,
        limit: pagination.limit,
        search: searchQuery,
        category_id: selectedCategory === 'all' ? '' : selectedCategory
      });
      
      setProducts(response.products);
      setPagination(prev => ({
        ...prev,
        total: response.total,
        totalPages: response.totalPages
      }));

      const total = response.total;
      setStats({
        total: total,
        inStock: response.products.filter(p => p.stock > (p.min_stock || 10)).length,
        lowStock: response.products.filter(p => p.stock <= (p.min_stock || 10) && p.stock > 0).length,
        outOfStock: response.products.filter(p => p.stock <= 0).length
      });

    } catch (err) {
      console.error("Error fetching products:", err);
      setError("حدث خطأ أثناء تحميل المنتجات. يرجى المحاولة مرة أخرى.");
    } finally {
      setLoading(false);
    }
  }, [pagination.page, pagination.limit, searchQuery, selectedCategory]);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  // Handlers
  const handleView = (product) => console.log('View:', product);
  const handleEdit = (product) => console.log('Edit:', product);
  const handleDelete = async (product) => {
    if (window.confirm(`هل أنت متأكد من حذف ${product.name}؟`)) {
      try {
        await productService.delete(product.id);
        fetchProducts(); // Refresh
      } catch (err) {
        alert("فشل الحذف: " + err.message);
      }
    }
  };

  const handlePageChange = (newPage) => {
    if (newPage >= 1 && newPage <= pagination.totalPages) {
      setPagination(prev => ({ ...prev, page: newPage }));
    }
  };

  if (loading && products.length === 0) {
    return <div className="h-screen flex items-center justify-center"><LoadingSpinner /></div>;
  }
  
  if (error) {
    return (
      <div className="h-screen flex flex-col items-center justify-center gap-4 text-center p-4">
        <AlertTriangle size={48} className="text-destructive mb-2" />
        <h2 className="text-xl font-bold">خطأ في التحميل</h2>
        <p className="text-muted-foreground">{error}</p>
        <Button onClick={fetchProducts} variant="outline">
          <RefreshCw size={16} className="ml-2" />
          إعادة المحاولة
        </Button>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-8 min-h-screen bg-background text-foreground" dir="rtl">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">المنتجات</h1>
          <p className="text-muted-foreground mt-1">إدارة دليل المنتجات والمخزون</p>
        </div>
        <div className="flex gap-2">
           <Button variant="outline" onClick={fetchProducts}>
            <RefreshCw size={18} className="ml-2" />
            تحديث
          </Button>
          <Button className="bg-primary text-primary-foreground hover:bg-primary/90">
            <Plus size={20} className="ml-2" />
            إضافة منتج
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-6 flex items-center justify-between shadow-sm">
          <div>
            <p className="text-sm font-medium text-muted-foreground">إجمالي المنتجات</p>
            <h3 className="text-2xl font-bold mt-1">{stats.total}</h3>
          </div>
          <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center text-primary">
            <Package size={24} />
          </div>
        </Card>
        
        <Card className="p-6 flex items-center justify-between shadow-sm">
          <div>
            <p className="text-sm font-medium text-muted-foreground">متوفر</p>
            <h3 className="text-2xl font-bold mt-1 text-emerald-600">--</h3>
          </div>
          <div className="w-12 h-12 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600">
            <CheckCircle size={24} />
          </div>
        </Card>
        
        <Card className="p-6 flex items-center justify-between shadow-sm">
          <div>
            <p className="text-sm font-medium text-muted-foreground">مخزون منخفض</p>
            <h3 className="text-2xl font-bold mt-1 text-amber-600">--</h3>
          </div>
          <div className="w-12 h-12 rounded-full bg-amber-100 flex items-center justify-center text-amber-600">
            <AlertTriangle size={24} />
          </div>
        </Card>
        
        <Card className="p-6 flex items-center justify-between shadow-sm">
          <div>
            <p className="text-sm font-medium text-muted-foreground">نفد المخزون</p>
            <h3 className="text-2xl font-bold mt-1 text-rose-600">--</h3>
          </div>
          <div className="w-12 h-12 rounded-full bg-rose-100 flex items-center justify-center text-rose-600">
            <XCircle size={24} />
          </div>
        </Card>
      </div>

      {/* Filters & Actions */}
      <Card className="p-4">
        <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
          <div className="flex flex-1 w-full gap-4 items-center">
             <div className="relative flex-1 max-w-md">
              <Search className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground h-4 w-4" />
              <Input 
                placeholder="بحث..." 
                className="pr-9" 
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            {/* Simple Category Select - Could be replaced with UI Select */}
            <select 
              className="h-10 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
            >
              <option value="all">جميع الفئات</option>
              {/* Should be dynamic from API */}
              <option value="1">إلكترونيات</option>
              <option value="2">ملابس</option>
            </select>
          </div>

          <div className="flex items-center gap-2 w-full md:w-auto">
            <Button variant="outline" size="icon">
              <Filter size={18} />
            </Button>
            <Button variant="outline" size="icon">
              <Download size={18} />
            </Button>
             <div className="bg-muted p-1 rounded-lg flex gap-1">
              <Button 
                variant={viewMode === 'grid' ? 'secondary' : 'ghost'} 
                size="sm" 
                className="h-8 px-2"
                onClick={() => setViewMode('grid')}
              >
                <Grid size={16} />
              </Button>
              <Button 
                variant={viewMode === 'table' ? 'secondary' : 'ghost'} 
                size="sm"
                className="h-8 px-2"
                onClick={() => setViewMode('table')}
              >
                <List size={16} />
              </Button>
            </div>
          </div>
        </div>
      </Card>

      {/* Content */}
      {viewMode === 'grid' ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {products.map(product => (
            <ProductCard
              key={product.id}
              product={product}
              onView={handleView}
              onEdit={handleEdit}
              onDelete={handleDelete}
            />
          ))}
          {products.length === 0 && !loading && (
             <div className="col-span-full text-center py-12 text-muted-foreground">
               لا توجد منتجات لعرضها
             </div>
          )}
        </div>
      ) : (
        <Card className="overflow-hidden">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>المنتج</TableHead>
                <TableHead>الفئة</TableHead>
                <TableHead>السعر</TableHead>
                <TableHead>المخزون</TableHead>
                <TableHead>الحالة</TableHead>
                <TableHead>إجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {products.map(product => (
                <ProductRow
                  key={product.id}
                  product={product}
                  onView={handleView}
                  onEdit={handleEdit}
                  onDelete={handleDelete}
                />
              ))}
               {products.length === 0 && !loading && (
                 <TableRow>
                   <TableCell colSpan={6} className="text-center py-12 text-muted-foreground">
                     لا توجد منتجات لعرضها
                   </TableCell>
                 </TableRow>
               )}
            </TableBody>
          </Table>
        </Card>
      )}

      {/* Pagination */}
      <div className="flex items-center justify-between border-t pt-4">
        <p className="text-sm text-muted-foreground">
          عرض {Math.min((pagination.page - 1) * pagination.limit + 1, pagination.total)} - {Math.min(pagination.page * pagination.limit, pagination.total)} من {pagination.total} منتج
        </p>
        <div className="flex gap-2">
          <Button 
            variant="outline" 
            size="icon" 
            onClick={() => handlePageChange(pagination.page - 1)}
            disabled={pagination.page <= 1}
          >
            <ChevronRight size={16} />
          </Button>
          <Button variant="outline" className="w-10">
            {pagination.page}
          </Button>
          <Button 
            variant="outline" 
            size="icon" 
            onClick={() => handlePageChange(pagination.page + 1)}
            disabled={pagination.page >= pagination.totalPages}
          >
            <ChevronLeft size={16} />
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ProductsPage;

