import { useState } from 'react'
import {
  LayoutDashboard, Tags, Warehouse, Database, Truck, Receipt, Calculator, CreditCard, Upload, Shield, UserCog, Building2, Printer, LogOut, ChevronDown,
  Package, ShoppingCart, BarChart3, TrendingUp, FileText, Settings, Users, Bell, DollarSign
} from 'lucide-react'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const SidebarColorful = () => {
  const location = useLocation()
  const { user, logout } = useAuth()
  const [expandedSections, setExpandedSections] = useState({
    inventory: true,
    sales: false,
    accounting: false,
    reports: false,
    tools: false,
    admin: false,
    settings: false
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
      color: 'from-[#80AA45] to-[#689030]',
      iconBg: 'bg-gradient-to-br from-[#80AA45] to-[#689030]',
      items: [
        { path: '/', icon: LayoutDashboard, label: 'لوحة المعلومات', badge: null, color: 'text-[#80AA45]' }
      ]
    },
    {
      id: 'inventory',
      label: 'إدارة المخزون',
      icon: Package,
      expandable: true,
      color: 'from-[#3B715A] to-[#22523D]',
      iconBg: 'bg-gradient-to-br from-[#3B715A] to-[#22523D]',
      items: [
        { path: '/products', icon: Package, label: 'المنتجات', badge: '47', color: 'text-[#3B715A]' },
        { path: '/categories', icon: Tags, label: 'الفئات والتصنيفات', badge: null, color: 'text-[#3B715A]' },
        { path: '/warehouses', icon: Warehouse, label: 'المخازن', badge: '3', color: 'text-[#22523D]' },
        { path: '/stock-movements', icon: TrendingUp, label: 'حركات المخزون', badge: null, color: 'text-[#3B715A]' },
        { path: '/lots', icon: Database, label: 'إدارة اللوطات', badge: null, color: 'text-[#22523D]' }
      ]
    },
    {
      id: 'sales',
      label: 'المبيعات والشراء',
      icon: ShoppingCart,
      expandable: true,
      color: 'from-[#80AA45] to-[#689030]',
      iconBg: 'bg-gradient-to-br from-[#80AA45] to-[#689030]',
      items: [
        { path: '/customers', icon: Users, label: 'العملاء', badge: '23', color: 'text-[#80AA45]' },
        { path: '/suppliers', icon: Truck, label: 'الموردين', badge: '12', color: 'text-[#689030]' },
        { path: '/sales-invoices', icon: Receipt, label: 'فواتير المبيعات', badge: null, color: 'text-[#80AA45]' },
        { path: '/purchase-invoices', icon: ShoppingCart, label: 'فواتير المشتريات', badge: null, color: 'text-[#689030]' },
        { path: '/quotations', icon: FileText, label: 'عروض الأسعار', badge: null, color: 'text-[#80AA45]' }
      ]
    },
    {
      id: 'accounting',
      label: 'النظام المحاسبي',
      icon: Calculator,
      expandable: true,
      color: 'from-[#E65E36] to-[#C7451F]',
      iconBg: 'bg-gradient-to-br from-[#E65E36] to-[#C7451F]',
      items: [
        { path: '/accounting', icon: Calculator, label: 'النظام المحاسبي الشامل', badge: null, color: 'text-[#E65E36]' },
        { path: '/accounting/currencies', icon: DollarSign, label: 'العملات وأسعار الصرف', badge: null, color: 'text-[#C7451F]' },
        { path: '/accounting/cash-boxes', icon: CreditCard, label: 'الصناديق والحسابات', badge: null, color: 'text-[#E65E36]' },
        { path: '/accounting/vouchers', icon: Receipt, label: 'قسائم الدفع', badge: null, color: 'text-[#C7451F]' },
        { path: '/accounting/entries', icon: FileText, label: 'القيود المحاسبية', badge: null, color: 'text-[#E65E36]' },
        { path: '/accounting/profit-loss', icon: TrendingUp, label: 'الأرباح والخسائر', badge: null, color: 'text-[#C7451F]' }
      ]
    },
    {
      id: 'reports',
      label: 'التقارير والتحليلات',
      icon: BarChart3,
      expandable: true,
      color: 'from-[#3B715A] to-[#22523D]',
      iconBg: 'bg-gradient-to-br from-[#3B715A] to-[#22523D]',
      items: [
        { path: '/reports/sales', icon: TrendingUp, label: 'تقارير المبيعات', badge: null, color: 'text-[#3B715A]' },
        { path: '/reports/inventory', icon: Package, label: 'تقارير المخزون', badge: null, color: 'text-[#22523D]' },
        { path: '/reports/financial', icon: DollarSign, label: 'التقارير المالية', badge: null, color: 'text-[#3B715A]' },
        { path: '/reports/custom', icon: BarChart3, label: 'تقارير مخصصة', badge: null, color: 'text-[#22523D]' }
      ]
    },
    {
      id: 'tools',
      label: 'الأدوات والمساعدات',
      icon: Upload,
      expandable: true,
      color: 'from-[#80AA45] to-[#689030]',
      iconBg: 'bg-gradient-to-br from-[#80AA45] to-[#689030]',
      items: [
        { path: '/import-export', icon: Upload, label: 'الاستيراد والتصدير', badge: null, color: 'text-[#80AA45]' },
        { path: '/print-export', icon: Printer, label: 'الطباعة والتصدير', badge: null, color: 'text-[#689030]' },
        { path: '/backup', icon: Database, label: 'النسخ الاحتياطية', badge: null, color: 'text-[#80AA45]' }
      ]
    },
    {
      id: 'admin',
      label: 'الإدارة والأمان',
      icon: Shield,
      expandable: true,
      color: 'from-[#E65E36] to-[#C7451F]',
      iconBg: 'bg-gradient-to-br from-[#E65E36] to-[#C7451F]',
      items: [
        { path: '/users', icon: UserCog, label: 'إدارة المستخدمين', badge: null, color: 'text-[#E65E36]' },
        { path: '/admin/roles', icon: Shield, label: 'الأدوار والصلاحيات', badge: null, color: 'text-[#C7451F]' },
        { path: '/admin/security', icon: Shield, label: 'الأمان والمراقبة', badge: null, color: 'text-[#E65E36]' },
        { path: '/admin/logs', icon: FileText, label: 'سجل الأنشطة', badge: null, color: 'text-[#C7451F]' }
      ]
    },
    {
      id: 'settings',
      label: 'الإعدادات',
      icon: Settings,
      expandable: true,
      color: 'from-[#708079] to-[#10271D]',
      iconBg: 'bg-gradient-to-br from-[#708079] to-[#10271D]',
      items: [
        { path: '/company', icon: Building2, label: 'إعدادات الشركة', badge: null, color: 'text-[#708079]' },
        { path: '/settings', icon: Settings, label: 'إعدادات النظام', badge: null, color: 'text-[#10271D]' },
        { path: '/categories', icon: Tags, label: 'إعدادات الفئات', badge: null, color: 'text-[#708079]' },
        { path: '/notifications', icon: Bell, label: 'إعدادات التنبيهات', badge: null, color: 'text-[#10271D]' }
      ]
    }
  ]

  const handleLogout = () => {
    logout()
  }

  return (
    <div className="h-full flex flex-col bg-gradient-to-b from-[#E7F0E9] to-white">
      {/* Header */}
      <div className="p-6 border-b border-[#BFCBC2] bg-gradient-to-r from-[#80AA45] to-[#689030]">
        <h1 className="text-xl font-bold text-white">نظام إدارة المخزون</h1>
        <p className="text-sm text-green-100 mt-1">إدارة شاملة ومتقدمة</p>
      </div>
      
      {/* Menu */}
      <nav className="flex-1 overflow-y-auto py-4 px-3">
        {menuSections.map((section) => (
          <div key={section.id} className="mb-3">
            {section.expandable ? (
              <div>
                <button
                  onClick={() => toggleSection(section.id)}
                  className="flex items-center justify-between w-full px-4 py-3 text-gray-700 hover:bg-gradient-to-l hover:from-gray-50 hover:to-gray-100 rounded-lg transition-all duration-200 group"
                >
                  <div className="flex items-center">
                    <div className={`w-8 h-8 ${section.iconBg} rounded-lg flex items-center justify-center mr-3 shadow-md group-hover:shadow-lg transition-shadow`}>
                      <section.icon className="w-4 h-4 text-white" />
                    </div>
                    <span className="font-medium">{section.label}</span>
                  </div>
                  <ChevronDown className={`w-4 h-4 transition-transform duration-200 ${expandedSections[section.id] ? 'rotate-180' : ''}`} />
                </button>
                {expandedSections[section.id] && (
                  <div className="mt-1 ml-2 space-y-1">
                    {section.items.map((item) => {
                      const Icon = item.icon
                      const isActive = location.pathname === item.path

                      return (
                        <Link
                          key={item.path}
                          to={item.path}
                          className={`flex items-center px-4 py-2.5 ml-8 rounded-lg transition-all duration-200 ${
                            isActive
                              ? `bg-gradient-to-l ${section.color} text-white shadow-md border-r-4 border-white`
                              : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                          }`}
                        >
                          <Icon className={`w-4 h-4 mr-2 ${isActive ? 'text-white' : item.color}`} />
                          <span className="text-sm">{item.label}</span>
                          {item.badge && (
                            <span className={`ml-auto text-xs px-2 py-0.5 rounded-full font-medium ${
                              isActive ? 'bg-white/20 text-white' : 'bg-blue-100 text-blue-800'
                            }`}>
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
                    className={`flex items-center px-4 py-3 rounded-lg transition-all duration-200 ${
                      isActive
                        ? `bg-gradient-to-l ${section.color} text-white shadow-md border-r-4 border-white`
                        : 'text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    <div className={`w-8 h-8 ${isActive ? 'bg-white/20' : section.iconBg} rounded-lg flex items-center justify-center mr-3 shadow-sm`}>
                      <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-white'}`} />
                    </div>
                    <span className="font-medium">{item.label}</span>
                  </Link>
                )
              })
            )}
          </div>
        ))}
      </nav>
      
      {/* User section */}
      <div className="p-4 border-t border-[#BFCBC2] bg-gradient-to-r from-[#E7F0E9] to-white">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <div className="w-10 h-10 bg-gradient-to-br from-[#80AA45] to-[#689030] rounded-full flex items-center justify-center shadow-md">
              <span className="text-white text-sm font-bold">
                {user?.full_name?.charAt(0) || 'م'}
              </span>
            </div>
            <div className="mr-3">
              <p className="text-sm font-semibold text-[#10271D]">
                {user?.full_name || 'مدير النظام'}
              </p>
              <p className="text-xs text-[#708079]">
                {user?.email || 'admin@system.com'}
              </p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="p-2.5 text-[#708079] hover:text-[#E65E36] hover:bg-red-50 rounded-lg transition-all duration-200 hover:shadow-md"
            title="تسجيل الخروج"
          >
            <LogOut className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  )
}

export default SidebarColorful

