import React, { useState } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu,
  LayoutDashboard, Tags, Warehouse, Database, Truck, Receipt, Calculator, CreditCard, Upload, Shield, UserCog, Building2, Printer, LogOut, ChevronDown
} from 'lucide-react'
import { Link, useLocation } from 'react-router-dom'

import { useAuth } from '../contexts/AuthContext'

const SidebarEnhanced = () => {
  const location = useLocation()
  const { user, logout } = useAuth()
  const [expandedSections, setExpandedSections] = useState({
    inventory: true,
    sales: false,
    accounting: false,
    reports: false,
    advanced: true,
    admin: false
  })

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }))
  }

  const menuSections = [
    {
      id: 'main',
      label: 'الرئيسية',
      items: [
        { path: '/', icon: LayoutDashboard, label: 'لوحة المعلومات', badge: null }
      ]
    },
    {
      id: 'inventory',
      label: 'إدارة المخزون',
      icon: Package,
      expandable: true,
      items: [
        { path: '/products', icon: Package, label: 'المنتجات', badge: '47' },
        { path: '/categories', icon: Tags, label: 'الفئات والتصنيفات', badge: null },
        { path: '/warehouses', icon: Warehouse, label: 'المخازن', badge: '3' },
        { path: '/stock-movements', icon: TrendingUp, label: 'حركات المخزون', badge: null },
        { path: '/lots', icon: Database, label: 'إدارة اللوطات', badge: null }
      ]
    },
    {
      id: 'sales',
      label: 'المبيعات والشراء',
      icon: ShoppingCart,
      expandable: true,
      items: [
        { path: '/customers', icon: Users, label: 'العملاء', badge: '23' },
        { path: '/suppliers', icon: Truck, label: 'الموردين', badge: '12' },
        { path: '/sales-invoices', icon: Receipt, label: 'فواتير المبيعات', badge: null },
        { path: '/purchase-invoices', icon: ShoppingCart, label: 'فواتير المشتريات', badge: null }
      ]
    },
    {
      id: 'accounting',
      label: 'النظام المحاسبي',
      icon: Calculator,
      expandable: true,
      items: [
        { path: '/accounting/currencies', icon: DollarSign, label: 'العملات وأسعار الصرف', badge: null },
        { path: '/accounting/cash-boxes', icon: CreditCard, label: 'الصناديق والحسابات', badge: null },
        { path: '/accounting/vouchers', icon: Receipt, label: 'قسائم الدفع', badge: null },
        { path: '/accounting/profit-loss', icon: TrendingUp, label: 'الأرباح والخسائر', badge: null }
      ]
    },
    {
      id: 'reports',
      label: 'التقارير والتحليلات',
      icon: BarChart3,
      expandable: true,
      items: [
        { path: '/reports/sales', icon: TrendingUp, label: 'تقارير المبيعات', badge: null },
        { path: '/reports/inventory', icon: Package, label: 'تقارير المخزون', badge: null },
        { path: '/reports/financial', icon: DollarSign, label: 'التقارير المالية', badge: null },
        { path: '/reports/comprehensive', icon: BarChart3, label: 'التقارير الشاملة', badge: 'جديد' }
      ]
    },
    {
      id: 'advanced',
      label: 'الميزات المتقدمة',
      icon: Settings,
      expandable: true,
      items: [
        { path: '/warehouses?tab=adjustments', icon: Warehouse, label: 'قيود المخزن', badge: 'جديد' },
        { path: '/warehouses?tab=constraints', icon: Warehouse, label: 'قيود المخازن', badge: 'جديد' },
        { path: '/invoices', icon: Receipt, label: 'إدارة المرتجعات', badge: 'جديد' },
        { path: '/reports/financial', icon: CreditCard, label: 'إدارة المدفوعات والمديونيات', badge: 'جديد' },
        { path: '/stock-movements', icon: Truck, label: 'أوامر الرفع والاستلام', badge: 'جديد' },
        { path: '/accounts/customer-supplier', icon: Users, label: 'حسابات العملاء والموردين', badge: 'جديد' },
        { path: '/treasury/opening-balances', icon: DollarSign, label: 'الأرصدة الافتتاحية للخزنة', badge: 'جديد' }
      ]
    },
    {
      id: 'tools',
      label: 'الأدوات والمساعدات',
      icon: Upload,
      expandable: true,
      items: [
        { path: '/import-export', icon: Upload, label: 'الاستيراد والتصدير', badge: null },
        { path: '/print-export', icon: Printer, label: 'الطباعة والتصدير', badge: null }
      ]
    },
    {
      id: 'admin',
      label: 'الإدارة والأمان',
      icon: Shield,
      expandable: true,
      items: [
        { path: '/admin/users', icon: UserCog, label: 'إدارة المستخدمين', badge: null },
        { path: '/admin/roles', icon: Shield, label: 'الأدوار والصلاحيات', badge: null },
        { path: '/admin/security', icon: Shield, label: 'الأمان والمراقبة', badge: null }
      ]
    },
    {
      id: 'settings',
      label: 'الإعدادات',
      icon: Settings,
      expandable: true,
      items: [
        { path: '/settings/company', icon: Building2, label: 'إعدادات الشركة', badge: null },
        { path: '/system/settings', icon: Settings, label: 'إعدادات النظام المتقدمة', badge: 'جديد' },
        { path: '/settings/categories', icon: Tags, label: 'إعدادات الفئات', badge: null }
      ]
    },
    {
      id: 'system',
      label: 'النظام المتقدم',
      icon: Database,
      expandable: true,
      items: [
        { path: '/dashboard/interactive', icon: BarChart3, label: 'لوحة المعلومات التفاعلية', badge: 'جديد' },
        { path: '/system/setup-wizard', icon: Settings, label: 'معالج الإعداد', badge: 'جديد' },
        { path: '/system/user-management', icon: UserCog, label: 'إدارة المستخدمين المتقدمة', badge: 'جديد' }
      ]
    }
  ]

  const handleLogout = () => {
    logout()
  }

  const SectionHeader = ({ section, icon: Icon, label, isExpanded, onToggle }) => (
    <button
      onClick={onToggle}
      className="flex items-center justify-between w-full px-3 py-2 text-sm font-semibold text-foreground hover:bg-muted rounded-lg transition-colors"
    >
      <div className="flex items-center">
        <Icon className="w-5 h-5 ml-2 text-gray-500" />
        <span>{label}</span>
      </div>
      {section.expandable && (
        <ChevronDown className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-180' : ''}`} />
      )}
    </button>
  )

  const MenuItem = ({ item, isActive }) => {
    const Icon = item.icon
    
    return (
      <Link
        to={item.path}
        className={`flex items-center justify-between px-3 py-2 mr-4 rounded-lg text-sm font-medium transition-all duration-200 ${
          isActive
            ? 'bg-primary-100 text-primary-700 border-r-2 border-primary-500'
            : 'text-muted-foreground hover:bg-muted/50 hover:text-foreground'
        }`}
      >
        <div className="flex items-center">
          <Icon className="w-4 h-4 ml-2" />
          <span>{item.label}</span>
        </div>
        {item.badge && (
          <span className="px-2 py-1 text-xs font-medium bg-primary-100 text-primary-600 rounded-full">
            {item.badge}
          </span>
        )}
      </Link>
    )
  }

  return (
    <div className="w-72 bg-white shadow-xl border-l border-border" dir="rtl">
      {/* Header */}
      <div className="p-6 border-b border-border bg-gradient-to-r from-blue-600 to-blue-700">
        <div>
          <h1 className="text-xl font-bold text-white">نظام ERP المتكامل</h1>
          <p className="text-sm text-primary-100 mt-1">إدارة شاملة للأعمال</p>
        </div>
      </div>

      {/* User Info */}
      {user && (
        <div className="p-4 border-b border-border">
          <div className="flex items-center p-3 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg">
            <div className="w-10 h-10 bg-primary-500 rounded-full flex items-center justify-center">
              <UserCog className="w-5 h-5 text-white" />
            </div>
            <div className="mr-3">
              <p className="text-sm font-semibold text-foreground">{user.name || 'مدير النظام'}</p>
              <p className="text-xs text-muted-foreground">{user.role || 'مدير عام'}</p>
            </div>
          </div>
        </div>
      )}

      {/* Navigation */}
      <div className="flex-1 overflow-y-auto p-4 max-h-96">
        <nav className="space-y-2">
          {menuSections.map((section) => {
            const isExpanded = expandedSections[section.id]
            
            return (
              <div key={section.id} className="space-y-1">
                {section.expandable ? (
                  <>
                    <SectionHeader
                      section={section}
                      icon={section.icon}
                      label={section.label}
                      isExpanded={isExpanded}
                      onToggle={() => toggleSection(section.id)}
                    />
                    {isExpanded && (
                      <div className="space-y-1">
                        {section.items.map((item) => (
                          <MenuItem
                            key={item.path}
                            item={item}
                            isActive={location.pathname === item.path}
                          />
                        ))}
                      </div>
                    )}
                  </>
                ) : (
                  <div className="space-y-1">
                    {section.items.map((item) => (
                      <MenuItem
                        key={item.path}
                        item={item}
                        isActive={location.pathname === item.path}
                      />
                    ))}
                  </div>
                )}
              </div>
            )
          })}
        </nav>
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-border bg-muted/50">
        <button
          onClick={handleLogout}
          className="flex items-center w-full px-3 py-2 text-sm font-medium text-destructive rounded-lg hover:bg-destructive/10 transition-colors"
        >
          <LogOut className="w-5 h-5 ml-2" />
          <span>تسجيل الخروج</span>
        </button>
      </div>
    </div>
  )
}

export default SidebarEnhanced

