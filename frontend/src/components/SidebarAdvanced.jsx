import React, { useState } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu,
  LayoutDashboard, Building, ArrowRightLeft, Database, Truck, LinkIcon
} from 'lucide-react'
import { Link, useLocation } from 'react-router-dom'

const SidebarAdvanced = ({ isOpen, onToggle, user }) => {
  const location = useLocation()
  const [expandedMenus, setExpandedMenus] = useState({})

  const menuItems = [
    {
      id: 'dashboard',
      name: 'لوحة التحكم',
      icon: LayoutDashboard,
      path: '/dashboard',
      color: 'text-primary-600'
    },
    {
      id: 'inventory',
      name: 'إدارة المخزون',
      icon: Package,
      color: 'text-primary',
      submenu: [
        { name: 'المنتجات المتقدمة', path: '/products', icon: Package },
        { name: 'إدارة المخازن', path: '/warehouses', icon: Building },
        { name: 'حركات المخزون', path: '/stock-movements', icon: ArrowRightLeft },
        { name: 'اللوط والدفعات', path: '/lots', icon: Database }
      ]
    },
    {
      id: 'sales',
      name: 'المبيعات',
      icon: ShoppingCart,
      color: 'text-purple-600',
      submenu: [
        { name: 'فواتير المبيعات', path: '/sales-invoices', icon: FileText },
        { name: 'العملاء', path: '/customers', icon: Users },
        { name: 'عروض الأسعار', path: '/quotations', icon: FileText }
      ]
    },
    {
      id: 'purchases',
      name: 'المشتريات',
      icon: Truck,
      color: 'text-accent',
      submenu: [
        { name: 'فواتير المشتريات', path: '/purchase-invoices', icon: FileText },
        { name: 'الموردين', path: '/suppliers', icon: Building },
        { name: 'أوامر الشراء', path: '/purchase-orders', icon: FileText }
      ]
    },
    {
      id: 'reports',
      name: 'التقارير المتكاملة',
      icon: BarChart3,
      path: '/reports',
      color: 'text-indigo-600'
    },
    {
      id: 'integration',
      name: 'إدارة التكامل',
      icon: LinkIcon,
      path: '/integration',
      color: 'text-cyan-600'
    },
    {
      id: 'admin',
      name: 'الإدارة',
      icon: Settings,
      color: 'text-muted-foreground',
      submenu: [
        { name: 'إدارة المستخدمين', path: '/user-management', icon: Users },
        { name: 'إعدادات الشركة', path: '/company-settings', icon: Building },
        { name: 'الإعدادات المتقدمة', path: '/settings', icon: Settings },
        { name: 'استيراد وتصدير', path: '/import-export', icon: Database }
      ]
    }
  ]

  const toggleSubmenu = (menuId) => {
    setExpandedMenus(prev => ({
      ...prev,
      [menuId]: !prev[menuId]
    }))
  }

  const isActiveMenu = (item) => {
    if (item.path) {
      return location.pathname === item.path
    }
    if (item.submenu) {
      return item.submenu.some(subItem => location.pathname === subItem.path)
    }
    return false
  }

  const isActiveSubMenu = (path) => {
    return location.pathname === path
  }

  return (
    <div className={`fixed right-0 top-0 h-full bg-white shadow-lg border-l transition-all duration-300 z-40 ${
      isOpen ? 'w-64' : 'w-16'
    }`}>
      {/* رأس الشريط الجانبي */}
      <div className="p-4 border-b">
        <div className="flex items-center justify-between">
          {isOpen && (
            <div className="flex items-center">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <Package className="w-5 h-5 text-white" />
              </div>
              <div className="mr-3">
                <h1 className="text-lg font-bold text-foreground">نظام ERP</h1>
                <p className="text-xs text-gray-500">متقدم ومتكامل</p>
              </div>
            </div>
          )}
          <button
            onClick={onToggle}
            className="p-1 rounded-md hover:bg-muted transition-colors"
          >
            <ChevronRight className={`w-5 h-5 text-muted-foreground transition-transform ${isOpen ? 'rotate-180' : ''}`} />
          </button>
        </div>
      </div>

      {/* معلومات المستخدم */}
      {isOpen && user && (
        <div className="p-4 border-b bg-muted/50">
          <div className="flex items-center">
            <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
              <Users className="w-5 h-5 text-primary-600" />
            </div>
            <div className="mr-3">
              <p className="text-sm font-medium text-foreground">{user.name || 'المستخدم'}</p>
              <p className="text-xs text-gray-500">{user.role || 'مدير النظام'}</p>
            </div>
          </div>
        </div>
      )}

      {/* قائمة التنقل */}
      <nav className="flex-1 overflow-y-auto p-2">
        <ul className="space-y-1">
          {menuItems.map((item) => (
            <li key={item.id}>
              {item.submenu ? (
                // عنصر مع قائمة فرعية
                <div>
                  <button
                    onClick={() => toggleSubmenu(item.id)}
                    className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      isActiveMenu(item)
                        ? 'bg-primary-50 text-primary-700 border-l-4 border-primary-600'
                        : 'text-foreground hover:bg-muted'
                    }`}
                  >
                    <div className="flex items-center">
                      <item.icon className={`w-5 h-5 ${item.color} ${!isOpen && 'mx-auto'}`} />
                      {isOpen && <span className="mr-3">{item.name}</span>}
                    </div>
                    {isOpen && (
                      <ChevronDown className={`w-4 h-4 transition-transform ${
                        expandedMenus[item.id] ? 'rotate-180' : ''
                      }`} />
                    )}
                  </button>
                  
                  {/* القائمة الفرعية */}
                  {isOpen && expandedMenus[item.id] && (
                    <ul className="mt-1 mr-4 space-y-1">
                      {item.submenu.map((subItem) => (
                        <li key={subItem.path}>
                          <Link
                            to={subItem.path}
                            className={`flex items-center px-3 py-2 rounded-md text-sm transition-colors ${
                              isActiveSubMenu(subItem.path)
                                ? 'bg-primary-100 text-primary-700 font-medium'
                                : 'text-muted-foreground hover:bg-muted/50 hover:text-foreground'
                            }`}
                          >
                            <subItem.icon className="w-4 h-4" />
                            <span className="mr-2">{subItem.name}</span>
                          </Link>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              ) : (
                // عنصر بسيط
                <Link
                  to={item.path}
                  className={`flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    isActiveMenu(item)
                      ? 'bg-primary-50 text-primary-700 border-l-4 border-primary-600'
                      : 'text-foreground hover:bg-muted'
                  }`}
                  title={!isOpen ? item.name : ''}
                >
                  <item.icon className={`w-5 h-5 ${item.color} ${!isOpen && 'mx-auto'}`} />
                  {isOpen && <span className="mr-3">{item.name}</span>}
                </Link>
              )}
            </li>
          ))}
        </ul>
      </nav>

      {/* تنبيهات سريعة */}
      {isOpen && (
        <div className="p-4 border-t bg-muted/50">
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs">
              <span className="text-muted-foreground">تنبيهات سريعة</span>
              <span className="bg-destructive/20 text-destructive px-2 py-1 rounded-full">3</span>
            </div>
            <div className="space-y-1">
              <div className="flex items-center text-xs text-accent">
                <AlertTriangle className="w-3 h-3 ml-1" />
                <span>5 منتجات منخفضة المخزون</span>
              </div>
              <div className="flex items-center text-xs text-destructive">
                <AlertTriangle className="w-3 h-3 ml-1" />
                <span>3 لوط قريبة الانتهاء</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* معلومات النظام */}
      {isOpen && (
        <div className="p-4 border-t">
          <div className="text-center">
            <div className="flex items-center justify-center mb-2">
              <div className="w-2 h-2 bg-primary/100 rounded-full ml-2"></div>
              <span className="text-xs text-muted-foreground">النظام متصل</span>
            </div>
            <p className="text-xs text-gray-500">الإصدار 2.0.0</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default SidebarAdvanced

