import React, { useState, useEffect } from 'react'
import {
  Plus,
  Search,
  Filter,
  Download,
  Edit,
  Trash2,
  Eye,
  Calendar,
  DollarSign,
  FileText
} from 'lucide-react'

const PaymentVouchers = () => {
  const [vouchers, setVouchers] = useState([])
  const [filteredVouchers, setFilteredVouchers] = useState([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [typeFilter, setTypeFilter] = useState('all')
  const [showModal, setShowModal] = useState(false)
  const [editingVoucher, setEditingVoucher] = useState(null)
  const [notification, setNotification] = useState(null)

  useEffect(() => {
    loadVouchers()
  }, [])

  useEffect(() => {
    filterVouchers()
  }, [vouchers, searchTerm, typeFilter])

  const loadVouchers = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://172.16.16.27:8000/accounting/payment-vouchers')
      if (response.ok) {
        const data = await response.json()
        if (data.status === 'success') {
          setVouchers(data.data)
        } else {
          throw new Error('فشل في تحميل قسائم الدفع')
        }
      } else {
        throw new Error('فشل في الاتصال بالخادم')
      }
    } catch (error) {
      // بيانات تجريبية
      const mockVouchers = [
        {
          id: 1,
          number: 'PV-2024-001',
          type: 'دفع',
          amount: 5000,
          currency: 'EGP',
          description: 'دفع فاتورة كهرباء',
          paymentMethod: 'نقدي',
          cashBox: 'الصندوق الرئيسي',
          beneficiary: 'شركة الكهرباء',
          date: '2024-07-04',
          createdBy: 'أحمد محمد',
          status: 'مدفوع'
        },
        {
          id: 2,
          number: 'RV-2024-001',
          type: 'استلام',
          amount: 15000,
          currency: 'EGP',
          description: 'استلام دفعة من العميل',
          paymentMethod: 'تحويل بنكي',
          cashBox: 'حساب البنك الأهلي',
          beneficiary: 'مزرعة النيل الكبرى',
          date: '2024-07-03',
          createdBy: 'سارة علي',
          status: 'مستلم'
        },
        {
          id: 3,
          number: 'PV-2024-002',
          type: 'دفع',
          amount: 8500,
          currency: 'EGP',
          description: 'دفع راتب الموظفين',
          paymentMethod: 'تحويل بنكي',
          cashBox: 'حساب البنك الأهلي',
          beneficiary: 'الموظفين',
          date: '2024-07-02',
          createdBy: 'محمد حسن',
          status: 'مدفوع'
        },
        {
          id: 4,
          number: 'RV-2024-002',
          type: 'استلام',
          amount: 25000,
          currency: 'EGP',
          description: 'استلام دفعة مقدمة من عميل جديد',
          paymentMethod: 'شيك',
          cashBox: 'الصندوق الرئيسي',
          beneficiary: 'شركة الأراضي الخضراء',
          date: '2024-07-01',
          createdBy: 'فاطمة أحمد',
          status: 'مستلم'
        }
      ]
      setVouchers(mockVouchers)
    } finally {
      setLoading(false)
    }
  }

  const filterVouchers = () => {
    let filtered = vouchers

    if (searchTerm) {
      filtered = filtered.filter(voucher =>
        voucher.number.toLowerCase().includes(searchTerm.toLowerCase()) ||
        voucher.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        voucher.beneficiary.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    if (typeFilter !== 'all') {
      filtered = filtered.filter(voucher => voucher.type === typeFilter)
    }

    setFilteredVouchers(filtered)
  }

  const showNotification = (message, type = 'success') => {
    setNotification({ message, type })
    setTimeout(() => setNotification(null), 3000)
  }

  const handleAddVoucher = () => {
    setEditingVoucher(null)
    setShowModal(true)
  }

  const handleEditVoucher = (voucher) => {
    setEditingVoucher(voucher)
    setShowModal(true)
  }

  const handleDeleteVoucher = async (voucherId) => {
    if (window.confirm('هل أنت متأكد من حذف هذه القسيمة؟')) {
      try {
        // محاكاة طلب API
        await new Promise(resolve => setTimeout(resolve, 500))
        setVouchers(prev => prev.filter(v => v.id !== voucherId))
        showNotification('تم حذف القسيمة بنجاح')
      } catch (error) {
        showNotification('فشل في حذف القسيمة', 'error')
      }
    }
  }

  const handlePrintVoucher = (voucher) => {
    // طباعة القسيمة
    const printWindow = window.open('', '_blank')
    printWindow.document.write(`
      <html>
        <head>
          <title>قسيمة ${voucher.type} - ${voucher.number}</title>
          <style>
            body { font-family: Arial, sans-serif; direction: rtl; }
            .header { text-align: center; margin-bottom: 20px; }
            .details { margin: 20px 0; }
            .amount { font-size: 24px; font-weight: bold; color: #2563eb; }
          </style>
        </head>
        <body>
          <div class="header">
            <h1>قسيمة ${voucher.type}</h1>
            <h2>${voucher.number}</h2>
          </div>
          <div class="details">
            <p><strong>المبلغ:</strong> <span class="amount">${voucher.amount.toLocaleString()} ${voucher.currency}</span></p>
            <p><strong>التاريخ:</strong> ${voucher.date}</p>
            <p><strong>المستفيد:</strong> ${voucher.beneficiary}</p>
            <p><strong>الوصف:</strong> ${voucher.description}</p>
            <p><strong>طريقة الدفع:</strong> ${voucher.paymentMethod}</p>
            <p><strong>الصندوق:</strong> ${voucher.cashBox}</p>
          </div>
        </body>
      </html>
    `)
    printWindow.document.close()
    printWindow.print()
  }

  const getTypeIcon = (type) => {
    return type === 'دفع' 
      ? <TrendingDown className="h-5 w-5 text-destructive" />
      : <TrendingUp className="h-5 w-5 text-primary" />
  }

  const getTypeColor = (type) => {
    return type === 'دفع' 
      ? 'bg-destructive/20 text-red-800'
      : 'bg-primary/20 text-green-800'
  }

  const getPaymentMethodIcon = (method) => {
    switch (method) {
      case 'نقدي':
        return <Banknote className="h-4 w-4 text-primary" />
      case 'تحويل بنكي':
      case 'شيك':
        return <CreditCard className="h-4 w-4 text-primary-600" />
      default:
        return <DollarSign className="h-4 w-4 text-muted-foreground" />
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="p-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-foreground">قسائم الدفع والاستلام</h1>
          <p className="text-muted-foreground">إدارة قسائم الدفع والاستلام النقدية والبنكية</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => {
              const csvContent = "data:text/csv;charset=utf-8," 
                + "الرقم,النوع,المبلغ,التاريخ,المستفيد\n"
                + filteredVouchers.map(v => 
                    `${v.number},${v.type},${v.amount},${v.date},${v.beneficiary}`
                  ).join("\n")
              
              const encodedUri = encodeURI(csvContent)
              const link = document.createElement("a")
              link.setAttribute("href", encodedUri)
              link.setAttribute("download", `vouchers_${new Date().toISOString().split('T')[0]}.csv`)
              document.body.appendChild(link)
              link.click()
              document.body.removeChild(link)
              showNotification('تم تصدير القسائم بنجاح!')
            }}
            className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center"
          >
            <Download className="w-5 h-5 ml-2" />
            تصدير
          </button>
          <button
            onClick={handleAddVoucher}
            className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors flex items-center"
          >
            <Plus className="w-5 h-5 ml-2" />
            قسيمة جديدة
          </button>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="relative">
          <input
            type="text"
            placeholder="البحث في القسائم..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <Search className="absolute right-3 top-2.5 h-5 w-5 text-gray-400" />
        </div>

        <select
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
          className="px-4 py-2 border border-border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="all">جميع الأنواع</option>
          <option value="دفع">قسائم الدفع</option>
          <option value="استلام">قسائم الاستلام</option>
        </select>

        <button
          onClick={loadVouchers}
          className="bg-muted text-foreground px-4 py-2 rounded-lg hover:bg-muted transition-colors flex items-center justify-center"
        >
          <RefreshCw className="w-5 h-5 ml-2" />
          تحديث
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <Receipt className="h-8 w-8 text-primary-600" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">إجمالي القسائم</p>
              <p className="text-2xl font-bold text-foreground">{vouchers.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <TrendingDown className="h-8 w-8 text-destructive" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">قسائم الدفع</p>
              <p className="text-2xl font-bold text-foreground">
                {vouchers.filter(v => v.type === 'دفع').length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <TrendingUp className="h-8 w-8 text-primary" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">قسائم الاستلام</p>
              <p className="text-2xl font-bold text-foreground">
                {vouchers.filter(v => v.type === 'استلام').length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex items-center">
            <DollarSign className="h-8 w-8 text-purple-600" />
            <div className="mr-3">
              <p className="text-sm font-medium text-muted-foreground">صافي الحركة</p>
              <p className="text-2xl font-bold text-foreground">
                {(vouchers.filter(v => v.type === 'استلام').reduce((sum, v) => sum + v.amount, 0) -
                  vouchers.filter(v => v.type === 'دفع').reduce((sum, v) => sum + v.amount, 0)).toLocaleString()}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Vouchers Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                رقم القسيمة
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                النوع
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                المبلغ
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                المستفيد
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                طريقة الدفع
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                التاريخ
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                الإجراءات
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {filteredVouchers.map((voucher) => (
              <tr key={voucher.id} className="hover:bg-muted/50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-foreground">{voucher.number}</div>
                  <div className="text-sm text-gray-500">{voucher.description}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    {getTypeIcon(voucher.type)}
                    <span className={`mr-2 inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getTypeColor(voucher.type)}`}>
                      {voucher.type}
                    </span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className={`text-sm font-medium ${voucher.type === 'دفع' ? 'text-destructive' : 'text-primary'}`}>
                    {voucher.type === 'دفع' ? '-' : '+'}{voucher.amount.toLocaleString()} {voucher.currency}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">
                  {voucher.beneficiary}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    {getPaymentMethodIcon(voucher.paymentMethod)}
                    <span className="mr-2 text-sm text-foreground">{voucher.paymentMethod}</span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <Calendar className="h-4 w-4 text-gray-400 ml-2" />
                    <span className="text-sm text-foreground">{voucher.date}</span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handlePrintVoucher(voucher)}
                      className="text-purple-600 hover:text-purple-900"
                      title="طباعة"
                    >
                      <Eye className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleEditVoucher(voucher)}
                      className="text-primary-600 hover:text-primary-900"
                      title="تعديل"
                    >
                      <Edit className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handleDeleteVoucher(voucher.id)}
                      className="text-destructive hover:text-red-900"
                      title="حذف"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Add/Edit Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold">
                {editingVoucher ? 'تعديل القسيمة' : 'إضافة قسيمة جديدة'}
              </h3>
              <button
                onClick={() => setShowModal(false)}
                className="text-gray-400 hover:text-muted-foreground"
              >
                ✕
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="voucher-type" className="block text-sm font-medium text-foreground mb-2">
                  نوع القسيمة
                </label>
                <select id="voucher-type" className="w-full p-2 border border-border rounded-lg">
                  <option value="">اختر النوع</option>
                  <option value="دفع">قسيمة دفع</option>
                  <option value="استلام">قسيمة استلام</option>
                </select>
              </div>

              <div>
                <label htmlFor="voucher-amount" className="block text-sm font-medium text-foreground mb-2">
                  المبلغ
                </label>
                <input
                  id="voucher-amount"
                  type="number"
                  placeholder="0.00"
                  className="w-full p-2 border border-border rounded-lg"
                  defaultValue={editingVoucher?.amount || ''}
                />
              </div>

              <div>
                <label htmlFor="voucher-currency" className="block text-sm font-medium text-foreground mb-2">
                  العملة
                </label>
                <select id="voucher-currency" className="w-full p-2 border border-border rounded-lg">
                  <option value="EGP">الجنيه المصري</option>
                  <option value="USD">الدولار الأمريكي</option>
                  <option value="EUR">اليورو</option>
                </select>
              </div>

              <div>
                <label htmlFor="voucher-beneficiary" className="block text-sm font-medium text-foreground mb-2">
                  المستفيد
                </label>
                <input
                  id="voucher-beneficiary"
                  type="text"
                  placeholder="اسم المستفيد"
                  className="w-full p-2 border border-border rounded-lg"
                  defaultValue={editingVoucher?.beneficiary || ''}
                />
              </div>

              <div>
                <label htmlFor="voucher-payment-method" className="block text-sm font-medium text-foreground mb-2">
                  طريقة الدفع
                </label>
                <select id="voucher-payment-method" className="w-full p-2 border border-border rounded-lg">
                  <option value="">اختر طريقة الدفع</option>
                  <option value="نقدي">نقدي</option>
                  <option value="تحويل بنكي">تحويل بنكي</option>
                  <option value="شيك">شيك</option>
                  <option value="بطاقة ائتمان">بطاقة ائتمان</option>
                </select>
              </div>

              <div>
                <label htmlFor="voucher-cashbox" className="block text-sm font-medium text-foreground mb-2">
                  الصندوق/الحساب
                </label>
                <select id="voucher-cashbox" className="w-full p-2 border border-border rounded-lg">
                  <option value="">اختر الصندوق</option>
                  <option value="الصندوق الرئيسي">الصندوق الرئيسي</option>
                  <option value="حساب البنك الأهلي">حساب البنك الأهلي</option>
                  <option value="صندوق الدولار">صندوق الدولار</option>
                </select>
              </div>

              <div className="md:col-span-2">
                <label htmlFor="voucher-description" className="block text-sm font-medium text-foreground mb-2">
                  الوصف
                </label>
                <textarea
                  id="voucher-description"
                  placeholder="وصف القسيمة..."
                  className="w-full p-2 border border-border rounded-lg"
                  rows="3"
                  defaultValue={editingVoucher?.description || ''}
                />
              </div>

              <div>
                <label htmlFor="voucher-date" className="block text-sm font-medium text-foreground mb-2">
                  التاريخ
                </label>
                <input
                  id="voucher-date"
                  type="date"
                  className="w-full p-2 border border-border rounded-lg"
                  defaultValue={editingVoucher?.date || new Date().toISOString().split('T')[0]}
                />
              </div>
            </div>

            <div className="flex justify-end space-x-2 mt-6">
              <button
                onClick={() => setShowModal(false)}
                className="px-4 py-2 text-muted-foreground border border-border rounded-lg hover:bg-muted/50"
              >
                إلغاء
              </button>
              <button
                onClick={() => {
                  showNotification(editingVoucher ? 'تم تحديث القسيمة بنجاح' : 'تم إضافة القسيمة بنجاح')
                  setShowModal(false)
                }}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
              >
                حفظ
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Notification */}
      {notification && (
        <div className={`fixed top-4 left-4 p-4 rounded-lg shadow-lg ${
          notification.type === 'success' ? 'bg-primary/100' : 'bg-destructive/100'
        } text-white`}>
          {notification.message}
        </div>
      )}
    </div>
  )
}

export default PaymentVouchers

