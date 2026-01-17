import React, { useState } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu,
  LayoutDashboard, Tags, Warehouse, Database, Truck, Receipt, Calculator, CreditCard, Upload, Printer, Shield, UserCog, Building2, Bell, LogOut, RefreshCw, Activity, ChevronDown
} from 'lucide-react'
import { Link, useLocation } from 'react-router-dom'

import { useAuth } from '../contexts/AuthContext'

const Sidebar = () => {
  const location = useLocation()
  const { user, logout } = useAuth()
  const [expandedSections, setExpandedSections] = useState({
    inventory: true,
    sales: false,
    accounting: false,
    reports: false,
    admin: false
  })
  const [isCollapsed, setIsCollapsed] = useState(false)

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
        { path: '/purchase-invoices', icon: ShoppingCart, label: 'فواتير المشتريات', badge: null },
        { path: '/quotations', icon: FileText, label: 'عروض الأسعار', badge: null }
      ]
    },
    {
      id: 'accounting',
      label: 'النظام المحاسبي',
      icon: Calculator,
      expandable: true,
      items: [
        { path: '/accounting', icon: Calculator, label: 'النظام المحاسبي الشامل', badge: null },
        { path: '/accounting/currencies', icon: DollarSign, label: 'العملات وأسعار الصرف', badge: null },
        { path: '/accounting/cash-boxes', icon: CreditCard, label: 'الصناديق والحسابات', badge: null },
        { path: '/accounting/vouchers', icon: Receipt, label: 'قسائم الدفع', badge: null },
        { path: '/accounting/entries', icon: FileText, label: 'القيود المحاسبية', badge: null },
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
        { path: '/reports/custom', icon: BarChart3, label: 'تقارير مخصصة', badge: null }
      ]
    },
    {
      id: 'tools',
      label: 'الأدوات والمساعدات',
      icon: Upload,
      expandable: true,
      items: [
        { path: '/import-export', icon: Upload, label: 'الاستيراد والتصدير', badge: null },
        { path: '/print-export', icon: Printer, label: 'الطباعة والتصدير', badge: null },
        { path: '/backup', icon: Download, label: 'النسخ الاحتياطية', badge: null }
      ]
    },
    {
      id: 'admin',
      label: 'الإدارة والأمان',
      icon: Shield,
      expandable: true,
      items: [
        { path: '/users', icon: UserCog, label: 'إدارة المستخدمين', badge: null },
        { path: '/admin/roles', icon: Shield, label: 'الأدوار والصلاحيات', badge: null },
        { path: '/admin/security', icon: Shield, label: 'الأمان والمراقبة', badge: null },
        { path: '/admin/logs', icon: FileText, label: 'سجل الأنشطة', badge: null }
      ]
    },
    {
      id: 'settings',
      label: 'الإعدادات',
      icon: Settings,
      expandable: true,
      items: [
        { path: '/company', icon: Building2, label: 'إعدادات الشركة', badge: null },
        { path: '/settings', icon: Settings, label: 'إعدادات النظام', badge: null },
        { path: '/categories', icon: Tags, label: 'إعدادات الفئات', badge: null },
        { path: '/notifications', icon: Bell, label: 'إعدادات التنبيهات', badge: null }
      ]
    }
  ]

  const handleLogout = () => {
    logout()
  }

  return (
    <div className="w-64 bg-white shadow-lg">
      <div className="p-6 border-b">
        <h1 className="text-xl font-bold text-foreground">نظام إدارة المخزون</h1>
        <p className="text-sm text-muted-foreground mt-1">إدارة شاملة للمخزون</p>
      </div>
      
      <nav className="mt-6">
        {menuSections.map((section) => (
          <div key={section.id} className="mb-4">
            {section.expandable ? (
              <div>
                <button
                  onClick={() => toggleSection(section.id)}
                  className="flex items-center justify-between w-full px-6 py-3 text-foreground hover:bg-muted/50 transition-colors"
                >
                  <div className="flex items-center">
                    <section.icon className="w-5 h-5 ml-3" />
                    {section.label}
                  </div>
                  <ChevronDown className={`w-4 h-4 transition-transform ${expandedSections[section.id] ? 'rotate-180' : ''}`} />
                </button>
                {expandedSections[section.id] && (
                  <div className="bg-muted/50">
                    {section.items.map((item) => {
                      const Icon = item.icon
                      const isActive = location.pathname === item.path

                      return (
                        <Link
                          key={item.path}
                          to={item.path}
                          className={`flex items-center px-12 py-2 text-muted-foreground hover:bg-primary-50 hover:text-primary-600 transition-colors ${
                            isActive ? 'bg-primary-50 text-primary-600 border-l-4 border-primary-600' : ''
                          }`}
                        >
                          <Icon className="w-4 h-4 ml-2" />
                          {item.label}
                          {item.badge && (
                            <span className="mr-auto bg-primary-100 text-primary-800 text-xs px-2 py-1 rounded-full">
                              {item.badge}
                            </span>
                          )}
                        </Link>
                      )
                    })}
                  </div>
                )}
              </div>
            ) : (
              section.items.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path

                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center px-6 py-3 text-foreground hover:bg-primary-50 hover:text-primary-600 transition-colors ${
                      isActive ? 'bg-primary-50 text-primary-600 border-l-4 border-primary-600' : ''
                    }`}
                  >
                    <Icon className="w-5 h-5 ml-3" />
                    {item.label}
                  </Link>
                )
              })
            )}
          </div>
        ))}
      </nav>
      
      <div className="absolute bottom-0 w-64 p-6 border-t">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
              <span className="text-white text-sm font-medium">
                {user?.full_name?.charAt(0) || 'م'}
              </span>
            </div>
            <div className="mr-3">
              <p className="text-sm font-medium text-foreground">
                {user?.full_name || 'مدير النظام'}
              </p>
              <p className="text-xs text-gray-500">
                {user?.email || 'admin@system.com'}
              </p>
            </div>
          </div>
          <button
            data-testid="sidebar-logout"
            onClick={handleLogout}
            className="p-2 text-gray-500 hover:text-destructive hover:bg-destructive/10 rounded-lg transition-colors"
            title="تسجيل الخروج"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  )
}

export default Sidebar


