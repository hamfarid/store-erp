import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu,
  Printer, PieChart, ArrowLeftRight, Wallet, Receipt
} from 'lucide-react'
import DataTable from './ui/DataTable'
import DynamicForm from './ui/DynamicForm'
import { Notification, LoadingSpinner, Modal } from './ui/Notification'
import SearchFilter from './ui/SearchFilter'
import { isSuccess } from '../utils/responseHelper'

const AccountingSystem = () => {
  const [activeTab, setActiveTab] = useState('overview')
  const [currencies, setCurrencies] = useState([])
  const [exchangeRates, setExchangeRates] = useState([])
  const [cashBoxes, setCashBoxes] = useState([])
  const [paymentVouchers, setPaymentVouchers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showModal, setShowModal] = useState(false)
  const [modalType, setModalType] = useState('')
  const [_selectedItem, setSelectedItem] = useState(null)

  // تحميل البيانات عند بدء التشغيل
  useEffect(() => {
    loadAccountingData()
  }, [])

  const loadAccountingData = async () => {
    setLoading(true)
    try {
      await Promise.all([
        loadCurrencies(),
        loadExchangeRates(),
        loadCashBoxes(),
        loadPaymentVouchers()
      ])
    } catch (error) {
      loadMockData()
    } finally {
      setLoading(false)
    }
  }

  const loadCurrencies = async () => {
    try {
      const response = await fetch('http://172.16.16.27:8000/accounting/currencies')
      if (response.ok) {
        const data = await response.json()
        if (isSuccess(data)) {
          setCurrencies(data.currencies)
          return
        }
      }
      throw new Error('API غير متاح')
    } catch (error) {
      // البيانات التجريبية
      const mockCurrencies = [
        {
          id: 1,
          code: 'EGP',
          name: 'الجنيه المصري',
          symbol: 'ج.م',
          is_base: true,
          is_active: true,
          decimal_places: 2
        },
        {
          id: 2,
          code: 'USD',
          name: 'الدولار الأمريكي',
          symbol: '$',
          is_base: false,
          is_active: true,
          decimal_places: 2
        },
        {
          id: 3,
          code: 'EUR',
          name: 'اليورو',
          symbol: '€',
          is_base: false,
          is_active: true,
          decimal_places: 2
        }
      ]
      setCurrencies(mockCurrencies)
    }
  }

  const loadExchangeRates = async () => {
    try {
      const response = await fetch('http://172.16.16.27:8000/accounting/exchange-rates')
      if (response.ok) {
        const data = await response.json()
        if (isSuccess(data)) {
          setExchangeRates(data.exchange_rates)
          return
        }
      }
      throw new Error('API غير متاح')
    } catch (error) {
      // البيانات التجريبية
      const mockRates = [
        {
          id: 1,
          from_currency: 'USD',
          to_currency: 'EGP',
          rate: 30.85,
          date: '2024-07-03',
          created_at: '2024-07-03T10:00:00'
        },
        {
          id: 2,
          from_currency: 'EUR',
          to_currency: 'EGP',
          rate: 33.20,
          date: '2024-07-03',
          created_at: '2024-07-03T10:00:00'
        },
        {
          id: 3,
          from_currency: 'EGP',
          to_currency: 'USD',
          rate: 0.0324,
          date: '2024-07-03',
          created_at: '2024-07-03T10:00:00'
        }
      ]
      setExchangeRates(mockRates)
    }
  }

  const loadCashBoxes = async () => {
    try {
      const response = await fetch('http://172.16.16.27:8000/accounting/cash-boxes')
      if (response.ok) {
        const data = await response.json()
        if (isSuccess(data)) {
          setCashBoxes(data.cash_boxes)
          return
        }
      }
      throw new Error('API غير متاح')
    } catch (error) {
      // البيانات التجريبية
      const mockCashBoxes = [
        {
          id: 1,
          name: 'الخزنة الرئيسية',
          code: 'MAIN-001',
          currency: 'EGP',
          currency_id: 1,
          balance: 125000,
          box_type: 'main',
          description: 'الخزنة الرئيسية للشركة',
          is_active: true,
          assigned_to: 'محمد أحمد'
        },
        {
          id: 2,
          name: 'خزنة المبيعات',
          code: 'SALES-001',
          currency: 'EGP',
          currency_id: 1,
          balance: 45000,
          box_type: 'sales',
          description: 'خزنة قسم المبيعات',
          is_active: true,
          assigned_to: 'فاطمة محمد'
        },
        {
          id: 3,
          name: 'خزنة العملة الأجنبية',
          code: 'USD-001',
          currency: 'USD',
          currency_id: 2,
          balance: 5000,
          box_type: 'foreign',
          description: 'خزنة العملات الأجنبية',
          is_active: true,
          assigned_to: 'أحمد علي'
        }
      ]
      setCashBoxes(mockCashBoxes)
    }
  }

  const loadPaymentVouchers = async () => {
    try {
      const response = await fetch('http://172.16.16.27:8000/accounting/payment-vouchers')
      if (response.ok) {
        const data = await response.json()
        if (isSuccess(data)) {
          setPaymentVouchers(data.vouchers)
          return
        }
      }
      throw new Error('API غير متاح')
    } catch (error) {
      // البيانات التجريبية
      const mockVouchers = [
        {
          id: 1,
          voucher_number: 'PAY-2024-001',
          voucher_type: 'payment',
          partner_name: 'شركة تاكي للبذور',
          partner_type: 'supplier',
          amount: 15000,
          currency: 'EGP',
          payment_method: 'bank_transfer',
          cash_box: 'الخزنة الرئيسية',
          date: '2024-07-01',
          description: 'دفع مستحقات البذور',
          status: 'completed',
          created_by: 'محمد أحمد'
        },
        {
          id: 2,
          voucher_number: 'REC-2024-001',
          voucher_type: 'receipt',
          partner_name: 'مزرعة النيل الكبرى',
          partner_type: 'customer',
          amount: 25000,
          currency: 'EGP',
          payment_method: 'cash',
          cash_box: 'خزنة المبيعات',
          date: '2024-07-02',
          description: 'تحصيل فاتورة مبيعات',
          status: 'completed',
          created_by: 'فاطمة محمد'
        }
      ]
      setPaymentVouchers(mockVouchers)
    }
  }

  const loadMockData = () => {
    loadCurrencies()
    loadExchangeRates()
    loadCashBoxes()
    loadPaymentVouchers()
  }

  // مكون نظرة عامة
  const OverviewTab = () => (
    <div className="space-y-6">
      {/* إحصائيات سريعة */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-gradient-to-r from-green-500 to-green-600 rounded-lg p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100">إجمالي الأرصدة</p>
              <p className="text-2xl font-bold">
                {cashBoxes.reduce((sum, box) => sum + (box.balance || 0), 0).toLocaleString()} ج.م
              </p>
            </div>
            <Wallet className="w-8 h-8 text-green-200" />
          </div>
        </div>

        <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-primary-100">عدد الخزائن</p>
              <p className="text-2xl font-bold">{cashBoxes.length}</p>
            </div>
            <CreditCard className="w-8 h-8 text-primary-200" />
          </div>
        </div>

        <div className="bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-100">العملات النشطة</p>
              <p className="text-2xl font-bold">{currencies.filter(c => c.is_active).length}</p>
            </div>
            <ArrowLeftRight className="w-8 h-8 text-purple-200" />
          </div>
        </div>

        <div className="bg-gradient-to-r from-orange-500 to-orange-600 rounded-lg p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-orange-100">السندات اليوم</p>
              <p className="text-2xl font-bold">
                {paymentVouchers.filter(v => v.date === new Date().toISOString().split('T')[0]).length}
              </p>
            </div>
            <Receipt className="w-8 h-8 text-orange-200" />
          </div>
        </div>
      </div>

      {/* أرصدة الخزائن */}
      <div className="bg-white rounded-lg shadow-sm border border-border p-6">
        <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center">
          <Wallet className="w-5 h-5 ml-2 text-primary-600" />
          أرصدة الخزائن
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {cashBoxes.map((box) => (
            <div key={box.id} className="border border-border rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-medium text-foreground">{box.name}</h4>
                <span className={`px-2 py-1 rounded-full text-xs ${
                  box.box_type === 'main' ? 'bg-primary-100 text-primary-800' :
                  box.box_type === 'sales' ? 'bg-primary/20 text-green-800' :
                  'bg-purple-100 text-purple-800'
                }`}>
                  {box.box_type === 'main' ? 'رئيسية' :
                   box.box_type === 'sales' ? 'مبيعات' : 'أجنبية'}
                </span>
              </div>
              <p className="text-2xl font-bold text-foreground">
                {box.balance?.toLocaleString()} {box.currency}
              </p>
              <p className="text-sm text-muted-foreground mt-1">المسؤول: {box.assigned_to}</p>
            </div>
          ))}
        </div>
      </div>

      {/* أسعار الصرف الحالية */}
      <div className="bg-white rounded-lg shadow-sm border border-border p-6">
        <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center">
          <ArrowLeftRight className="w-5 h-5 ml-2 text-primary" />
          أسعار الصرف الحالية
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {exchangeRates.map((rate) => (
            <div key={rate.id} className="border border-border rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-foreground">
                    {rate.from_currency} → {rate.to_currency}
                  </p>
                  <p className="text-2xl font-bold text-primary-600">{rate.rate}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-muted-foreground">
                    {new Date(rate.date).toLocaleDateString('ar-EG')}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )

  // مكون العملات
  const CurrenciesTab = () => {
    const currencyColumns = [
      {
        key: 'code',
        header: 'رمز العملة',
        sortable: true,
        render: (value, item) => (
          <div className="flex items-center">
            <span className="font-mono bg-muted px-2 py-1 rounded text-sm">{value}</span>
            {item.is_base && (
              <span className="mr-2 px-2 py-1 bg-primary-100 text-primary-800 rounded-full text-xs">
                أساسية
              </span>
            )}
          </div>
        )
      },
      {
        key: 'name',
        header: 'اسم العملة',
        sortable: true,
        filterable: true
      },
      {
        key: 'symbol',
        header: 'الرمز',
        render: (value) => (
          <span className="font-bold text-lg">{value}</span>
        )
      },
      {
        key: 'decimal_places',
        header: 'المنازل العشرية',
        sortable: true
      },
      {
        key: 'is_active',
        header: 'الحالة',
        render: (value) => (
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
            value ? 'bg-primary/20 text-green-800' : 'bg-destructive/20 text-red-800'
          }`}>
            {value ? 'نشطة' : 'غير نشطة'}
          </span>
        )
      }
    ]

    const currencyActions = [
      {
        icon: Edit,
        label: 'تعديل',
        onClick: (item) => {
          setSelectedItem(item)
          setModalType('edit-currency')
          setShowModal(true)
        },
        className: 'text-primary hover:text-green-800 hover:bg-primary/10'
      },
      {
        icon: Trash2,
        label: 'حذف',
        onClick: (item) => {
          if (window.confirm(`هل أنت متأكد من حذف العملة "${item.name}"؟`)) {
            setCurrencies(prev => prev.filter(c => c.id !== item.id))
          }
        },
        className: 'text-destructive hover:text-red-800 hover:bg-destructive/10'
      }
    ]

    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-foreground">إدارة العملات</h3>
          <button
            onClick={() => {
              setSelectedItem(null)
              setModalType('add-currency')
              setShowModal(true)
            }}
            className="btn btn--primary"
          >
            <Plus className="w-4 h-4 ml-1" />
            إضافة عملة
          </button>
        </div>

        <DataTable
          data={currencies}
          columns={currencyColumns}
          actions={currencyActions}
          searchable={true}
          filterable={true}
          exportable={true}
        />
      </div>
    )
  }

  // مكون الخزائن
  const CashBoxesTab = () => {
    const cashBoxColumns = [
      {
        key: 'name',
        header: 'اسم الخزنة',
        sortable: true,
        filterable: true,
        render: (value, item) => (
          <div className="flex items-center">
            <Wallet className="w-4 h-4 text-gray-400 ml-2" />
            <div>
              <div className="font-medium">{value}</div>
              <div className="text-sm text-gray-500">{item.code}</div>
            </div>
          </div>
        )
      },
      {
        key: 'balance',
        header: 'الرصيد',
        sortable: true,
        render: (value, item) => (
          <div className="text-right">
            <div className="font-bold text-lg text-primary">
              {value?.toLocaleString()} {item.currency}
            </div>
          </div>
        )
      },
      {
        key: 'box_type',
        header: 'النوع',
        sortable: true,
        filterable: true,
        render: (value) => {
          const typeConfig = {
            main: { label: 'رئيسية', color: 'bg-primary-100 text-primary-800' },
            sales: { label: 'مبيعات', color: 'bg-primary/20 text-green-800' },
            foreign: { label: 'أجنبية', color: 'bg-purple-100 text-purple-800' },
            general: { label: 'عامة', color: 'bg-muted text-foreground' }
          }
          const config = typeConfig[value] || typeConfig.general
          return (
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>
              {config.label}
            </span>
          )
        }
      },
      {
        key: 'assigned_to',
        header: 'المسؤول',
        sortable: true,
        filterable: true
      },
      {
        key: 'is_active',
        header: 'الحالة',
        render: (value) => (
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
            value ? 'bg-primary/20 text-green-800' : 'bg-destructive/20 text-red-800'
          }`}>
            {value ? 'نشطة' : 'غير نشطة'}
          </span>
        )
      }
    ]

    const cashBoxActions = [
      {
        icon: Eye,
        label: 'عرض التفاصيل',
        onClick: (item) => {
          setSelectedItem(item)
          setModalType('view-cashbox')
          setShowModal(true)
        },
        className: 'text-primary-600 hover:text-primary-800 hover:bg-primary-50'
      },
      {
        icon: Edit,
        label: 'تعديل',
        onClick: (item) => {
          setSelectedItem(item)
          setModalType('edit-cashbox')
          setShowModal(true)
        },
        className: 'text-primary hover:text-green-800 hover:bg-primary/10'
      }
    ]

    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-foreground">إدارة الخزائن</h3>
          <button
            onClick={() => {
              setSelectedItem(null)
              setModalType('add-cashbox')
              setShowModal(true)
            }}
            className="btn btn--primary"
          >
            <Plus className="w-4 h-4 ml-1" />
            إضافة خزنة
          </button>
        </div>

        <DataTable
          data={cashBoxes}
          columns={cashBoxColumns}
          actions={cashBoxActions}
          searchable={true}
          filterable={true}
          exportable={true}
        />
      </div>
    )
  }

  // مكون السندات
  const VouchersTab = () => {
    const voucherColumns = [
      {
        key: 'voucher_number',
        header: 'رقم السند',
        sortable: true,
        filterable: true,
        render: (value) => (
          <span className="font-mono bg-muted px-2 py-1 rounded text-sm">{value}</span>
        )
      },
      {
        key: 'voucher_type',
        header: 'نوع السند',
        sortable: true,
        filterable: true,
        render: (value) => (
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
            value === 'payment' ? 'bg-destructive/20 text-red-800' : 'bg-primary/20 text-green-800'
          }`}>
            {value === 'payment' ? 'سند دفع' : 'سند قبض'}
          </span>
        )
      },
      {
        key: 'partner_name',
        header: 'الشريك',
        sortable: true,
        filterable: true,
        render: (value, item) => (
          <div>
            <div className="font-medium">{value}</div>
            <div className="text-sm text-gray-500">
              {item.partner_type === 'customer' ? 'عميل' : 'مورد'}
            </div>
          </div>
        )
      },
      {
        key: 'amount',
        header: 'المبلغ',
        sortable: true,
        render: (value, item) => (
          <div className="text-right">
            <div className={`font-bold text-lg ${
              item.voucher_type === 'payment' ? 'text-destructive' : 'text-primary'
            }`}>
              {value?.toLocaleString()} {item.currency}
            </div>
          </div>
        )
      },
      {
        key: 'payment_method',
        header: 'طريقة الدفع',
        render: (value) => {
          const methodConfig = {
            cash: 'نقداً',
            bank_transfer: 'تحويل بنكي',
            check: 'شيك',
            credit: 'آجل'
          }
          return methodConfig[value] || value
        }
      },
      {
        key: 'date',
        header: 'التاريخ',
        sortable: true,
        render: (value) => new Date(value).toLocaleDateString('ar-EG')
      },
      {
        key: 'status',
        header: 'الحالة',
        render: (value) => (
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
            value === 'completed' ? 'bg-primary/20 text-green-800' :
            value === 'pending' ? 'bg-accent/20 text-yellow-800' :
            'bg-destructive/20 text-red-800'
          }`}>
            {value === 'completed' ? 'مكتمل' :
             value === 'pending' ? 'في الانتظار' : 'ملغي'}
          </span>
        )
      }
    ]

    const voucherActions = [
      {
        icon: Eye,
        label: 'عرض التفاصيل',
        onClick: (item) => {
          setSelectedItem(item)
          setModalType('view-voucher')
          setShowModal(true)
        },
        className: 'text-primary-600 hover:text-primary-800 hover:bg-primary-50'
      },
      {
        icon: Printer,
        label: 'طباعة',
        onClick: (_item) => {
          /* Print functionality placeholder */
        },
        className: 'text-purple-600 hover:text-purple-800 hover:bg-purple-50'
      }
    ]

    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-foreground">سندات الدفع والقبض</h3>
          <div className="flex space-x-2 space-x-reverse">
            <button
              onClick={() => {
                setSelectedItem({ voucher_type: 'receipt' })
                setModalType('add-voucher')
                setShowModal(true)
              }}
              className="btn btn--success"
            >
              <Plus className="w-4 h-4 ml-1" />
              سند قبض
            </button>
            <button
              onClick={() => {
                setSelectedItem({ voucher_type: 'payment' })
                setModalType('add-voucher')
                setShowModal(true)
              }}
              className="btn btn--error"
            >
              <Plus className="w-4 h-4 ml-1" />
              سند دفع
            </button>
          </div>
        </div>

        <DataTable
          data={paymentVouchers}
          columns={voucherColumns}
          actions={voucherActions}
          searchable={true}
          filterable={true}
          exportable={true}
        />
      </div>
    )
  }

  // مكون التقارير
  const ReportsTab = () => (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold text-foreground">التقارير المالية</h3>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-white border border-border rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer">
          <div className="flex items-center mb-4">
            <BarChart3 className="w-8 h-8 text-primary-600 ml-3" />
            <div>
              <h4 className="font-semibold text-foreground">تقرير الأرصدة</h4>
              <p className="text-sm text-muted-foreground">أرصدة الخزائن والعملات</p>
            </div>
          </div>
          <button className="w-full px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
            عرض التقرير
          </button>
        </div>

        <div className="bg-white border border-border rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer">
          <div className="flex items-center mb-4">
            <TrendingUp className="w-8 h-8 text-primary ml-3" />
            <div>
              <h4 className="font-semibold text-foreground">تقرير المقبوضات</h4>
              <p className="text-sm text-muted-foreground">سندات القبض والتحصيلات</p>
            </div>
          </div>
          <button className="w-full px-4 py-2 bg-primary text-white rounded-lg hover:bg-green-700 transition-colors">
            عرض التقرير
          </button>
        </div>

        <div className="bg-white border border-border rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer">
          <div className="flex items-center mb-4">
            <TrendingDown className="w-8 h-8 text-destructive ml-3" />
            <div>
              <h4 className="font-semibold text-foreground">تقرير المدفوعات</h4>
              <p className="text-sm text-muted-foreground">سندات الدفع والمصروفات</p>
            </div>
          </div>
          <button className="w-full px-4 py-2 bg-destructive text-white rounded-lg hover:bg-red-700 transition-colors">
            عرض التقرير
          </button>
        </div>

        <div className="bg-white border border-border rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer">
          <div className="flex items-center mb-4">
            <ArrowLeftRight className="w-8 h-8 text-purple-600 ml-3" />
            <div>
              <h4 className="font-semibold text-foreground">تقرير أسعار الصرف</h4>
              <p className="text-sm text-muted-foreground">تاريخ أسعار الصرف</p>
            </div>
          </div>
          <button className="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors">
            عرض التقرير
          </button>
        </div>

        <div className="bg-white border border-border rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer">
          <div className="flex items-center mb-4">
            <PieChart className="w-8 h-8 text-accent ml-3" />
            <div>
              <h4 className="font-semibold text-foreground">التحليل المالي</h4>
              <p className="text-sm text-muted-foreground">تحليل الأداء المالي</p>
            </div>
          </div>
          <button className="w-full px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors">
            عرض التقرير
          </button>
        </div>

        <div className="bg-white border border-border rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer">
          <div className="flex items-center mb-4">
            <FileText className="w-8 h-8 text-indigo-600 ml-3" />
            <div>
              <h4 className="font-semibold text-foreground">كشف حساب</h4>
              <p className="text-sm text-muted-foreground">كشف حساب العملاء والموردين</p>
            </div>
          </div>
          <button className="w-full px-4 py-2 bg-secondary text-white rounded-lg hover:bg-secondary/90 transition-colors">
            عرض التقرير
          </button>
        </div>
      </div>
    </div>
  )

  // مكون أسعار الصرف
  const ExchangeRatesTab = () => {
    const rateColumns = [
      {
        key: 'from_currency',
        header: 'من العملة',
        sortable: true,
        filterable: true,
        render: (value) => (
          <span className="font-mono bg-primary-100 px-2 py-1 rounded text-sm">{value}</span>
        )
      },
      {
        key: 'to_currency',
        header: 'إلى العملة',
        sortable: true,
        filterable: true,
        render: (value) => (
          <span className="font-mono bg-primary/20 px-2 py-1 rounded text-sm">{value}</span>
        )
      },
      {
        key: 'rate',
        header: 'السعر',
        sortable: true,
        render: (value) => (
          <span className="font-bold text-lg text-primary-600">{value}</span>
        )
      },
      {
        key: 'date',
        header: 'التاريخ',
        sortable: true,
        render: (value) => new Date(value).toLocaleDateString('ar-EG')
      },
      {
        key: 'created_at',
        header: 'تاريخ الإنشاء',
        sortable: true,
        render: (value) => new Date(value).toLocaleString('ar-EG')
      }
    ]

    const rateActions = [
      {
        icon: Edit,
        label: 'تعديل',
        onClick: (item) => {
          setSelectedItem(item)
          setModalType('edit-rate')
          setShowModal(true)
        },
        className: 'text-primary hover:text-green-800 hover:bg-primary/10'
      },
      {
        icon: Trash2,
        label: 'حذف',
        onClick: (item) => {
          if (window.confirm('هل أنت متأكد من حذف سعر الصرف؟')) {
            setExchangeRates(prev => prev.filter(r => r.id !== item.id))
          }
        },
        className: 'text-destructive hover:text-red-800 hover:bg-destructive/10'
      }
    ]

    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-foreground">أسعار الصرف</h3>
          <button
            onClick={() => {
              setSelectedItem(null)
              setModalType('add-rate')
              setShowModal(true)
            }}
            className="btn btn--primary"
          >
            <Plus className="w-4 h-4 ml-1" />
            إضافة سعر صرف
          </button>
        </div>

        <DataTable
          data={exchangeRates}
          columns={rateColumns}
          actions={rateActions}
          searchable={true}
          filterable={true}
          exportable={true}
        />
      </div>
    )
  }

  // التبويبات
  const tabs = [
    { id: 'overview', label: 'نظرة عامة', icon: PieChart },
    { id: 'currencies', label: 'العملات', icon: DollarSign },
    { id: 'exchange-rates', label: 'أسعار الصرف', icon: ArrowLeftRight },
    { id: 'cash-boxes', label: 'الخزائن', icon: Wallet },
    { id: 'vouchers', label: 'السندات', icon: Receipt },
    { id: 'reports', label: 'التقارير', icon: BarChart3 }
  ]

  if (loading) {
    return <LoadingSpinner size="lg" text="جاري تحميل النظام المحاسبي..." />
  }

  return (
    <div className="p-6" dir="rtl">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-foreground flex items-center">
              <Calculator className="w-6 h-6 ml-2 text-primary-600" />
              النظام المحاسبي المتقدم
            </h1>
            <p className="text-muted-foreground mt-1">إدارة شاملة للعمليات المحاسبية والمالية</p>
          </div>
          
          <div className="flex items-center space-x-3 space-x-reverse">
            <button
              onClick={loadAccountingData}
              className="btn btn--primary"
            >
              <RefreshCw className="w-4 h-4 ml-1" />
              تحديث
            </button>
            
            <button
              onClick={() => console.log('export')}
              className="btn btn--secondary"
            >
              <Download className="w-4 h-4 ml-1" />
              تصدير
            </button>
          </div>
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <Notification
          type="error"
          title="خطأ في تحميل البيانات"
          message={error}
          className="mb-6"
          onDismiss={() => setError(null)}
        />
      )}

      {/* Tabs */}
      <div className="mb-6">
        <div className="border-b border-border">
          <nav className="-mb-px flex space-x-8 space-x-reverse">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-foreground hover:border-border'
                  }`}
                >
                  <Icon className="w-4 h-4 ml-1" />
                  {tab.label}
                </button>
              )
            })}
          </nav>
        </div>
      </div>

      {/* Tab Content */}
      <div>
        {activeTab === 'overview' && <OverviewTab />}
        {activeTab === 'currencies' && <CurrenciesTab />}
        {activeTab === 'exchange-rates' && <ExchangeRatesTab />}
        {activeTab === 'cash-boxes' && <CashBoxesTab />}
        {activeTab === 'vouchers' && <VouchersTab />}
        {activeTab === 'reports' && <ReportsTab />}
      </div>

      {/* Modals */}
      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title={
          modalType === 'add-currency' ? 'إضافة عملة جديدة' :
          modalType === 'edit-currency' ? 'تعديل العملة' :
          modalType === 'add-rate' ? 'إضافة سعر صرف' :
          'تعديل سعر الصرف'
        }
        size="md"
      >
        <div className="p-4">
          <p>نموذج {modalType} قريباً...</p>
        </div>
      </Modal>
    </div>
  )
}

export default AccountingSystem

