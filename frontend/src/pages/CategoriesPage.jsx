/**
 * Categories Management Page
 */

import React, { useState } from 'react';
import {
  Search, Plus, Edit, Trash2, Boxes, Package, MoreVertical,
  FolderTree, ChevronRight, ChevronDown
} from 'lucide-react';
import Button from '../components/ui/ModernButton';

const sampleCategories = [
  { id: 1, name: 'إلكترونيات', parent: null, productCount: 245, icon: '📱', color: 'teal' },
  { id: 2, name: 'هواتف', parent: 1, productCount: 89, icon: '📲', color: 'blue' },
  { id: 3, name: 'لابتوب', parent: 1, productCount: 56, icon: '💻', color: 'purple' },
  { id: 4, name: 'إكسسوارات', parent: 1, productCount: 100, icon: '🎧', color: 'amber' },
  { id: 5, name: 'ملابس', parent: null, productCount: 320, icon: '👕', color: 'rose' },
  { id: 6, name: 'رجالي', parent: 5, productCount: 150, icon: '👔', color: 'slate' },
  { id: 7, name: 'نسائي', parent: 5, productCount: 170, icon: '👗', color: 'pink' },
  { id: 8, name: 'أثاث', parent: null, productCount: 89, icon: '🛋️', color: 'emerald' },
];

const CategoryCard = ({ category, onEdit, onDelete }) => {
  const colors = {
    teal: 'from-teal-500 to-teal-600',
    blue: 'from-blue-500 to-blue-600',
    purple: 'from-purple-500 to-purple-600',
    amber: 'from-amber-500 to-amber-600',
    rose: 'from-rose-500 to-rose-600',
    slate: 'from-slate-500 to-slate-600',
    pink: 'from-pink-500 to-pink-600',
    emerald: 'from-emerald-500 to-emerald-600',
  };

  return (
    <div className="bg-white rounded-2xl border border-gray-100 p-6 hover:shadow-xl transition-all duration-300 group">
      <div className="flex items-start justify-between mb-4">
        <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${colors[category.color]} flex items-center justify-center text-2xl shadow-lg`}>
          {category.icon}
        </div>
        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
          <button onClick={() => onEdit(category)} className="p-2 hover:bg-gray-100 rounded-lg">
            <Edit size={16} className="text-gray-500" />
          </button>
          <button onClick={() => onDelete(category)} className="p-2 hover:bg-rose-50 rounded-lg">
            <Trash2 size={16} className="text-rose-500" />
          </button>
        </div>
      </div>
      
      <h3 className="font-bold text-gray-900 text-lg mb-1">{category.name}</h3>
      <div className="flex items-center gap-2 text-gray-500 text-sm">
        <Package size={14} />
        <span>{category.productCount} منتج</span>
      </div>
      
      {category.parent && (
        <div className="mt-3 pt-3 border-t border-gray-100">
          <span className="text-xs text-gray-400">
            ضمن: {sampleCategories.find(c => c.id === category.parent)?.name}
          </span>
        </div>
      )}
    </div>
  );
};

const CategoriesPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  // const [viewMode, setViewMode] = useState('grid'); // Currently unused

  const mainCategories = sampleCategories.filter(c => !c.parent);
  const filteredCategories = sampleCategories.filter(c => 
    c.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="page-container" dir="rtl">
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">الفئات</h1>
          <p className="text-gray-500 mt-1">إدارة فئات المنتجات</p>
        </div>
        <div className="page-actions">
          <Button variant="primary" icon={Plus}>
            إضافة فئة
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">إجمالي الفئات</span>
            <div className="w-12 h-12 rounded-xl bg-teal-100 flex items-center justify-center">
              <Boxes className="text-teal-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value">{sampleCategories.length}</div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">الفئات الرئيسية</span>
            <div className="w-12 h-12 rounded-xl bg-blue-100 flex items-center justify-center">
              <FolderTree className="text-blue-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value">{mainCategories.length}</div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">الفئات الفرعية</span>
            <div className="w-12 h-12 rounded-xl bg-purple-100 flex items-center justify-center">
              <Boxes className="text-purple-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value">{sampleCategories.length - mainCategories.length}</div>
        </div>
        <div className="stats-card">
          <div className="stats-card-header">
            <span className="stats-card-title">إجمالي المنتجات</span>
            <div className="w-12 h-12 rounded-xl bg-amber-100 flex items-center justify-center">
              <Package className="text-amber-600" size={24} />
            </div>
          </div>
          <div className="stats-card-value">
            {sampleCategories.reduce((sum, c) => sum + c.productCount, 0)}
          </div>
        </div>
      </div>

      {/* Search */}
      <div className="search-filter-bar">
        <div className="relative search-input">
          <Search className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="بحث في الفئات..."
            className="form-input-standard pr-12"
          />
        </div>
      </div>

      {/* Categories Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {filteredCategories.map(category => (
          <CategoryCard
            key={category.id}
            category={category}
            onEdit={(c) => console.log('Edit:', c)}
            onDelete={(c) => console.log('Delete:', c)}
          />
        ))}
      </div>
    </div>
  );
};

export default CategoriesPage;



