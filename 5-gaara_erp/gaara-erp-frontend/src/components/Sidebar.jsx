import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  LayoutDashboard, 
  Package, 
  Wifi, 
  Brain, 
  ShoppingCart, 
  Calculator,
  Users,
  Settings,
  ChevronDown,
  ChevronRight,
  Zap,
  X
} from 'lucide-react'
import { Button } from '@/components/ui/button'

const menuItems = [
  {
    title: 'لوحة التحكم',
    icon: LayoutDashboard,
    path: '/dashboard',
    color: 'text-blue-500'
  },
  {
    title: 'إدارة المخزون',
    icon: Package,
    path: '/inventory',
    color: 'text-emerald-500',
    subItems: [
      { title: 'المنتجات', path: '/inventory/products' },
      { title: 'المخازن', path: '/inventory/warehouses' },
      { title: 'حركات المخزون', path: '/inventory/movements' },
      { title: 'تقارير المخزون', path: '/inventory/reports' }
    ]
  },
  {
    title: 'مراقبة IoT',
    icon: Wifi,
    path: '/iot',
    color: 'text-purple-500',
    subItems: [
      { title: 'الأجهزة', path: '/iot/devices' },
      { title: 'المستشعرات', path: '/iot/sensors' },
      { title: 'التنبيهات', path: '/iot/alerts' },
      { title: 'التحليلات', path: '/iot/analytics' }
    ]
  },
  {
    title: 'التحليلات الذكية',
    icon: Brain,
    path: '/ai-analytics',
    color: 'text-pink-500',
    subItems: [
      { title: 'التنبؤات', path: '/ai-analytics/predictions' },
      { title: 'تحليل البيانات', path: '/ai-analytics/data-analysis' },
      { title: 'التقارير الذكية', path: '/ai-analytics/smart-reports' }
    ]
  },
  {
    title: 'المبيعات',
    icon: ShoppingCart,
    path: '/sales',
    color: 'text-orange-500',
    subItems: [
      { title: 'العملاء', path: '/sales/customers' },
      { title: 'أوامر البيع', path: '/sales/orders' },
      { title: 'الفواتير', path: '/sales/invoices' },
      { title: 'التقارير', path: '/sales/reports' }
    ]
  },
  {
    title: 'المحاسبة',
    icon: Calculator,
    path: '/accounting',
    color: 'text-indigo-500',
    subItems: [
      { title: 'شجرة الحسابات', path: '/accounting/chart-of-accounts' },
      { title: 'القيود اليومية', path: '/accounting/journal-entries' },
      { title: 'التقارير المالية', path: '/accounting/financial-reports' }
    ]
  },
  {
    title: 'إدارة المستخدمين',
    icon: Users,
    path: '/users',
    color: 'text-cyan-500'
  },
  {
    title: 'الإعدادات',
    icon: Settings,
    path: '/settings',
    color: 'text-slate-500'
  }
]

const Sidebar = ({ onClose }) => {
  const [expandedItems, setExpandedItems] = useState({})
  const location = useLocation()

  const toggleExpanded = (index) => {
    setExpandedItems(prev => ({
      ...prev,
      [index]: !prev[index]
    }))
  }

  const isActive = (path) => {
    return location.pathname === path || location.pathname.startsWith(path + '/')
  }

  return (
    <div className="h-full bg-white dark:bg-slate-900 border-l border-slate-200 dark:border-slate-700 shadow-xl">
      {/* Header */}
      <div className="flex items-center justify-between p-6 border-b border-slate-200 dark:border-slate-700">
        <div className="flex items-center space-x-3 rtl:space-x-reverse">
          <div className="w-10 h-10 bg-gradient-to-r from-emerald-500 to-blue-500 rounded-lg flex items-center justify-center">
            <Zap className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-800 dark:text-white">Gaara ERP</h1>
            <p className="text-sm text-slate-500 dark:text-slate-400">الإصدار 12.0</p>
          </div>
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={onClose}
          className="lg:hidden"
        >
          <X className="w-4 h-4" />
        </Button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto p-4">
        <ul className="space-y-2">
          {menuItems.map((item, index) => (
            <li key={index}>
              <div>
                {item.subItems ? (
                  <button
                    onClick={() => toggleExpanded(index)}
                    className={`w-full flex items-center justify-between p-3 rounded-lg transition-all duration-200 hover:bg-slate-100 dark:hover:bg-slate-800 ${
                      isActive(item.path) ? 'bg-slate-100 dark:bg-slate-800' : ''
                    }`}
                  >
                    <div className="flex items-center space-x-3 rtl:space-x-reverse">
                      <item.icon className={`w-5 h-5 ${item.color}`} />
                      <span className="text-slate-700 dark:text-slate-200 font-medium">
                        {item.title}
                      </span>
                    </div>
                    <motion.div
                      animate={{ rotate: expandedItems[index] ? 90 : 0 }}
                      transition={{ duration: 0.2 }}
                    >
                      <ChevronRight className="w-4 h-4 text-slate-400" />
                    </motion.div>
                  </button>
                ) : (
                  <Link
                    to={item.path}
                    className={`flex items-center space-x-3 rtl:space-x-reverse p-3 rounded-lg transition-all duration-200 hover:bg-slate-100 dark:hover:bg-slate-800 ${
                      isActive(item.path) ? 'bg-slate-100 dark:bg-slate-800 border-r-4 border-emerald-500' : ''
                    }`}
                  >
                    <item.icon className={`w-5 h-5 ${item.color}`} />
                    <span className="text-slate-700 dark:text-slate-200 font-medium">
                      {item.title}
                    </span>
                  </Link>
                )}
              </div>

              {/* Submenu */}
              <AnimatePresence>
                {item.subItems && expandedItems[index] && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                    className="overflow-hidden"
                  >
                    <ul className="mt-2 mr-8 rtl:mr-0 rtl:ml-8 space-y-1">
                      {item.subItems.map((subItem, subIndex) => (
                        <li key={subIndex}>
                          <Link
                            to={subItem.path}
                            className={`block p-2 rounded-md text-sm transition-colors duration-200 hover:bg-slate-50 dark:hover:bg-slate-700 ${
                              isActive(subItem.path) 
                                ? 'text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-900/20' 
                                : 'text-slate-600 dark:text-slate-300'
                            }`}
                          >
                            {subItem.title}
                          </Link>
                        </li>
                      ))}
                    </ul>
                  </motion.div>
                )}
              </AnimatePresence>
            </li>
          ))}
        </ul>
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-slate-200 dark:border-slate-700">
        <div className="bg-gradient-to-r from-emerald-50 to-blue-50 dark:from-emerald-900/20 dark:to-blue-900/20 rounded-lg p-4">
          <h3 className="text-sm font-semibold text-slate-800 dark:text-white mb-1">
            نظام متطور
          </h3>
          <p className="text-xs text-slate-600 dark:text-slate-300 mb-3">
            مدعوم بالذكاء الاصطناعي وإنترنت الأشياء
          </p>
          <div className="flex space-x-2 rtl:space-x-reverse">
            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
            <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Sidebar
