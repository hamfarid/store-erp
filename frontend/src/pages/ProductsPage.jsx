/**
 * Modern Products Page
 * 
 * A beautiful, professional products management page with modern UI/UX.
 */

import React, { useState } from 'react';
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
  Barcode
} from 'lucide-react';

// ============================================================================
// Sample Data
// ============================================================================

const sampleProducts = [
  {
    id: 1,
    name: 'آيفون 15 برو ماكس',
    sku: 'IP15PM-256',
    category: 'هواتف',
    price: 5499,
    cost: 4800,
    stock: 45,
    minStock: 10,
    status: 'in_stock',
    image: null
  },
  {
    id: 2,
    name: 'سماعات إيربودز برو 2',
    sku: 'AP2-WHT',
    category: 'إكسسوارات',
    price: 999,
    cost: 750,
    stock: 120,
    minStock: 20,
    status: 'in_stock',
    image: null
  },
  {
    id: 3,
    name: 'شاحن MagSafe',
    sku: 'MS-CHG',
    category: 'إكسسوارات',
    price: 199,
    cost: 120,
    stock: 8,
    minStock: 15,
    status: 'low_stock',
    image: null
  },
  {
    id: 4,
    name: 'ماك بوك برو 16',
    sku: 'MBP16-M3',
    category: 'لابتوب',
    price: 12999,
    cost: 11000,
    stock: 0,
    minStock: 5,
    status: 'out_of_stock',
    image: null
  },
  {
    id: 5,
    name: 'آيباد برو 12.9',
    sku: 'IPAD-PRO12',
    category: 'أجهزة لوحية',
    price: 4999,
    cost: 4200,
    stock: 32,
    minStock: 8,
    status: 'in_stock',
    image: null
  },
  {
    id: 6,
    name: 'أبل واتش سيريس 9',
    sku: 'AW-S9-45',
    category: 'ساعات',
    price: 1899,
    cost: 1500,
    stock: 67,
    minStock: 15,
    status: 'in_stock',
    image: null
  },
];

// ============================================================================
// Status Badge Component
// ============================================================================

const StatusBadge = ({ status }) => {
  const config = {
    in_stock: { label: 'متوفر', color: 'bg-emerald-100 text-emerald-700', icon: CheckCircle },
    low_stock: { label: 'مخزون منخفض', color: 'bg-amber-100 text-amber-700', icon: AlertTriangle },
    out_of_stock: { label: 'نفد المخزون', color: 'bg-rose-100 text-rose-700', icon: XCircle },
  };

  const { label, color, icon: Icon } = config[status] || config.in_stock;

  return (
    <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold ${color}`}>
      <Icon size={12} />
      {label}
    </span>
  );
};

// ============================================================================
// Product Card Component (Grid View)
// ============================================================================

const ProductCard = ({ product, onView, onEdit, onDelete }) => (
  <div className="bg-white rounded-2xl border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 group">
    {/* Image */}
    <div className="relative aspect-square bg-gradient-to-br from-gray-100 to-gray-50 flex items-center justify-center">
      {product.image ? (
        <img src={product.image} alt={product.name} className="w-full h-full object-cover" />
      ) : (
        <Package className="w-16 h-16 text-gray-300" />
      )}
      
      {/* Quick Actions Overlay */}
      <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
        <button
          onClick={() => onView(product)}
          className="w-10 h-10 rounded-full bg-white flex items-center justify-center hover:scale-110 transition-transform"
        >
          <Eye size={18} className="text-gray-700" />
        </button>
        <button
          onClick={() => onEdit(product)}
          className="w-10 h-10 rounded-full bg-white flex items-center justify-center hover:scale-110 transition-transform"
        >
          <Edit size={18} className="text-gray-700" />
        </button>
        <button
          onClick={() => onDelete(product)}
          className="w-10 h-10 rounded-full bg-white flex items-center justify-center hover:scale-110 transition-transform"
        >
          <Trash2 size={18} className="text-rose-600" />
        </button>
      </div>

      {/* Status Badge */}
      <div className="absolute top-3 right-3">
        <StatusBadge status={product.status} />
      </div>
    </div>

    {/* Info */}
    <div className="p-4">
      <p className="text-xs text-gray-400 mb-1">{product.sku}</p>
      <h3 className="font-semibold text-gray-900 mb-2 truncate">{product.name}</h3>
      
      <div className="flex items-center justify-between">
        <div>
          <p className="text-lg font-bold text-teal-600">{product.price.toLocaleString()} ج.م</p>
          <p className="text-xs text-gray-400">التكلفة: {product.cost.toLocaleString()} ج.م</p>
        </div>
        <div className="text-left">
          <p className={`text-lg font-bold ${product.stock <= product.minStock ? 'text-rose-600' : 'text-gray-900'}`}>
            {product.stock}
          </p>
          <p className="text-xs text-gray-400">في المخزون</p>
        </div>
      </div>
    </div>
  </div>
);

// ============================================================================
// Product Row Component (Table View)
// ============================================================================

const ProductRow = ({ product, onView, onEdit, onDelete }) => (
  <tr className="hover:bg-gray-50 transition-colors">
    <td className="px-6 py-4">
      <div className="flex items-center gap-4">
        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-gray-100 to-gray-50 flex items-center justify-center flex-shrink-0">
          {product.image ? (
            <img src={product.image} alt="" className="w-full h-full object-cover rounded-xl" />
          ) : (
            <Package className="text-gray-300" size={20} />
          )}
        </div>
        <div>
          <p className="font-semibold text-gray-900">{product.name}</p>
          <p className="text-sm text-gray-400">{product.sku}</p>
        </div>
      </div>
    </td>
    <td className="px-6 py-4">
      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-gray-100 text-gray-700 rounded-lg text-sm">
        <Tag size={14} />
        {product.category}
      </span>
    </td>
    <td className="px-6 py-4">
      <p className="font-semibold text-gray-900">{product.price.toLocaleString()} ج.م</p>
      <p className="text-xs text-gray-400">تكلفة: {product.cost.toLocaleString()}</p>
    </td>
    <td className="px-6 py-4">
      <p className={`font-semibold ${product.stock <= product.minStock ? 'text-rose-600' : 'text-gray-900'}`}>
        {product.stock}
      </p>
      <p className="text-xs text-gray-400">حد أدنى: {product.minStock}</p>
    </td>
    <td className="px-6 py-4">
      <StatusBadge status={product.status} />
    </td>
    <td className="px-6 py-4">
      <div className="flex items-center gap-2">
        <button
          onClick={() => onView(product)}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <Eye size={18} className="text-gray-500" />
        </button>
        <button
          onClick={() => onEdit(product)}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <Edit size={18} className="text-gray-500" />
        </button>
        <button
          onClick={() => onDelete(product)}
          className="p-2 hover:bg-rose-50 rounded-lg transition-colors"
        >
          <Trash2 size={18} className="text-rose-500" />
        </button>
      </div>
    </td>
  </tr>
);

// ============================================================================
// Main Products Page Component
// ============================================================================

const ProductsPage = () => {
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'table'
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedStatus, setSelectedStatus] = useState('all');
  // const [currentPage, setCurrentPage] = useState(1); // Currently unused

  const categories = ['all', 'هواتف', 'لابتوب', 'أجهزة لوحية', 'إكسسوارات', 'ساعات'];

  // Handlers
  const handleView = (product) => console.log('View:', product);
  const handleEdit = (product) => console.log('Edit:', product);
  const handleDelete = (product) => console.log('Delete:', product);

  // Filter products
  const filteredProducts = sampleProducts.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         product.sku.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory;
    const matchesStatus = selectedStatus === 'all' || product.status === selectedStatus;
    return matchesSearch && matchesCategory && matchesStatus;
  });

  return (
    <div className="page-container" dir="rtl">
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">المنتجات</h1>
          <p className="text-gray-500 mt-1">إدارة جميع المنتجات في متجرك</p>
        </div>
        <div className="page-actions">
          <button className="flex items-center gap-2 px-6 py-3 bg-gradient-to-l from-teal-500 to-teal-600 text-white font-semibold rounded-xl shadow-lg shadow-teal-500/30 hover:shadow-xl hover:shadow-teal-500/40 transition-all duration-300">
            <Plus size={20} />
            <span>إضافة منتج</span>
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
          <div className="stats-card">
            <div className="stats-card-header">
              <span className="stats-card-title">إجمالي المنتجات</span>
              <div className="w-12 h-12 rounded-xl bg-teal-100 flex items-center justify-center">
                <Package className="text-teal-600" size={24} />
              </div>
            </div>
            <div className="stats-card-value">1,234</div>
          </div>
          <div className="stats-card">
            <div className="stats-card-header">
              <span className="stats-card-title">متوفر</span>
              <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center">
                <CheckCircle className="text-emerald-600" size={24} />
              </div>
            </div>
            <div className="stats-card-value text-emerald-600">1,180</div>
          </div>
          <div className="stats-card">
            <div className="stats-card-header">
              <span className="stats-card-title">مخزون منخفض</span>
              <div className="w-12 h-12 rounded-xl bg-amber-100 flex items-center justify-center">
                <AlertTriangle className="text-amber-600" size={24} />
              </div>
            </div>
            <div className="stats-card-value text-amber-600">42</div>
          </div>
          <div className="stats-card">
            <div className="stats-card-header">
              <span className="stats-card-title">نفد المخزون</span>
              <div className="w-12 h-12 rounded-xl bg-rose-100 flex items-center justify-center">
                <XCircle className="text-rose-600" size={24} />
              </div>
            </div>
            <div className="stats-card-value text-rose-600">12</div>
          </div>
        </div>

        {/* Filters & Search */}
        <div className="search-filter-bar">
          {/* Search */}
          <div className="relative search-input">
            <Search className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="بحث بالاسم أو الكود..."
              className="form-input-standard pr-12"
            />
          </div>

          {/* Category Filter */}
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="form-input-standard filter-select"
          >
            <option value="all">جميع الفئات</option>
            {categories.slice(1).map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>

          {/* Status Filter */}
          <select
            value={selectedStatus}
            onChange={(e) => setSelectedStatus(e.target.value)}
            className="form-input-standard filter-select"
          >
            <option value="all">جميع الحالات</option>
            <option value="in_stock">متوفر</option>
            <option value="low_stock">مخزون منخفض</option>
            <option value="out_of_stock">نفد المخزون</option>
          </select>

          <div className="action-buttons">
            {/* Export */}
            <button className="flex items-center gap-2 px-4 py-3 border-2 border-gray-200 rounded-xl hover:bg-gray-50 transition-colors">
              <Download size={18} className="text-gray-500" />
              <span className="text-sm font-medium text-gray-700">تصدير</span>
            </button>

            {/* Import */}
            <button className="flex items-center gap-2 px-4 py-3 border-2 border-gray-200 rounded-xl hover:bg-gray-50 transition-colors">
              <Upload size={18} className="text-gray-500" />
              <span className="text-sm font-medium text-gray-700">استيراد</span>
            </button>

            {/* View Toggle */}
            <div className="flex items-center bg-gray-100 rounded-xl p-1">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-2.5 rounded-lg transition-colors ${viewMode === 'grid' ? 'bg-white shadow' : 'hover:bg-gray-200'}`}
              >
                <Grid size={18} className={viewMode === 'grid' ? 'text-teal-600' : 'text-gray-500'} />
              </button>
              <button
                onClick={() => setViewMode('table')}
                className={`p-2.5 rounded-lg transition-colors ${viewMode === 'table' ? 'bg-white shadow' : 'hover:bg-gray-200'}`}
              >
                <List size={18} className={viewMode === 'table' ? 'text-teal-600' : 'text-gray-500'} />
              </button>
            </div>
          </div>
        </div>

      {/* Content */}
      {viewMode === 'grid' ? (
        /* Grid View */
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6" data-testid="products-table">
          {filteredProducts.map(product => (
            <ProductCard
              key={product.id}
              product={product}
              onView={handleView}
              onEdit={handleEdit}
              onDelete={handleDelete}
            />
          ))}
        </div>
      ) : (
        /* Table View */
        <div className="table-wrapper" data-testid="products-table">
          <table className="table-standard">
            <thead>
              <tr>
                <th>المنتج</th>
                <th>الفئة</th>
                <th>السعر</th>
                <th>المخزون</th>
                <th>الحالة</th>
                <th>إجراءات</th>
              </tr>
            </thead>
            <tbody>
              {filteredProducts.map(product => (
                <ProductRow
                  key={product.id}
                  product={product}
                  onView={handleView}
                  onEdit={handleEdit}
                  onDelete={handleDelete}
                />
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Pagination */}
      <div className="mt-8 button-group button-group-space-between">
        <p className="text-gray-500 text-sm">
          عرض 1-{filteredProducts.length} من {filteredProducts.length} منتج
        </p>
        <div className="button-group">
          <button className="p-2 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50" disabled>
            <ChevronRight size={18} className="text-gray-500" />
          </button>
          <button className="w-10 h-10 bg-teal-600 text-white rounded-lg font-medium">1</button>
          <button className="w-10 h-10 hover:bg-gray-100 rounded-lg font-medium text-gray-700">2</button>
          <button className="w-10 h-10 hover:bg-gray-100 rounded-lg font-medium text-gray-700">3</button>
          <button className="p-2 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <ChevronLeft size={18} className="text-gray-500" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProductsPage;

