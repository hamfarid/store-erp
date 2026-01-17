/**
 * Point of Sale (POS) Page - صفحة نقطة البيع
 * Gaara ERP v12
 */

import { useState } from 'react'
import { motion } from 'framer-motion'
import { toast } from 'sonner'
import {
  ShoppingCart,
  Search,
  Plus,
  Minus,
  Trash2,
  CreditCard,
  Banknote,
  QrCode,
  User,
  Percent,
  Receipt,
  Calculator,
} from 'lucide-react'

const products = [
  { id: 1, name: 'منتج 1', price: 150, barcode: '123456789', category: 'الكترونيات', stock: 50 },
  { id: 2, name: 'منتج 2', price: 75, barcode: '223456789', category: 'ملابس', stock: 120 },
  { id: 3, name: 'منتج 3', price: 250, barcode: '323456789', category: 'أجهزة', stock: 30 },
  { id: 4, name: 'منتج 4', price: 45, barcode: '423456789', category: 'مستلزمات', stock: 200 },
  { id: 5, name: 'منتج 5', price: 320, barcode: '523456789', category: 'الكترونيات', stock: 15 },
  { id: 6, name: 'منتج 6', price: 89, barcode: '623456789', category: 'ملابس', stock: 85 },
]

const paymentMethods = [
  { id: 'cash', name: 'نقدي', icon: Banknote, color: 'emerald' },
  { id: 'card', name: 'بطاقة', icon: CreditCard, color: 'blue' },
  { id: 'qr', name: 'QR Code', icon: QrCode, color: 'purple' },
]

export default function POSPage() {
  const [cart, setCart] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [discount, setDiscount] = useState(0)
  const [selectedPayment, setSelectedPayment] = useState('cash')

  const filteredProducts = products.filter(p =>
    p.name.includes(searchTerm) || p.barcode.includes(searchTerm)
  )

  const addToCart = (product) => {
    const existing = cart.find(item => item.id === product.id)
    if (existing) {
      setCart(cart.map(item =>
        item.id === product.id
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ))
    } else {
      setCart([...cart, { ...product, quantity: 1 }])
    }
    toast.success(`تم إضافة ${product.name} إلى السلة`)
  }

  const updateQuantity = (id, delta) => {
    setCart(cart.map(item => {
      if (item.id === id) {
        const newQty = item.quantity + delta
        return newQty > 0 ? { ...item, quantity: newQty } : item
      }
      return item
    }).filter(item => item.quantity > 0))
  }

  const removeFromCart = (id) => {
    setCart(cart.filter(item => item.id !== id))
  }

  const subtotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0)
  const discountAmount = subtotal * (discount / 100)
  const tax = (subtotal - discountAmount) * 0.15
  const total = subtotal - discountAmount + tax

  const handleCheckout = () => {
    if (cart.length === 0) {
      toast.error('السلة فارغة')
      return
    }
    toast.success('تم إتمام عملية البيع بنجاح')
    setCart([])
    setDiscount(0)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900" dir="rtl">
      <div className="flex h-screen">
        {/* Products Section */}
        <div className="flex-1 p-6 overflow-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            {/* Header */}
            <div className="flex items-center justify-between">
              <h1 className="text-2xl font-bold text-white flex items-center gap-3">
                <ShoppingCart className="w-7 h-7 text-emerald-400" />
                نقطة البيع
              </h1>
              <div className="flex items-center gap-2 text-slate-400">
                <User className="w-5 h-5" />
                <span>الكاشير: أحمد</span>
              </div>
            </div>

            {/* Search */}
            <div className="relative">
              <Search className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
              <input
                type="text"
                placeholder="البحث بالاسم أو الباركود..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pr-12 pl-4 py-3 bg-slate-800/50 border border-slate-700 rounded-xl text-white placeholder-slate-400 focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            {/* Products Grid */}
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {filteredProducts.map((product) => (
                <motion.button
                  key={product.id}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => addToCart(product)}
                  className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-4 text-right hover:border-emerald-500/50 transition-all"
                >
                  <div className="w-full h-20 bg-slate-700 rounded-lg mb-3 flex items-center justify-center">
                    <ShoppingCart className="w-8 h-8 text-slate-500" />
                  </div>
                  <h3 className="text-white font-medium mb-1">{product.name}</h3>
                  <p className="text-slate-400 text-sm mb-2">{product.category}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-emerald-400 font-bold">{product.price} ر.س</span>
                    <span className="text-slate-500 text-xs">المتاح: {product.stock}</span>
                  </div>
                </motion.button>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Cart Section */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="w-96 bg-slate-800/80 backdrop-blur-sm border-r border-slate-700 flex flex-col"
        >
          {/* Cart Header */}
          <div className="p-4 border-b border-slate-700">
            <h2 className="text-xl font-semibold text-white flex items-center gap-2">
              <Receipt className="w-5 h-5 text-emerald-400" />
              الفاتورة
            </h2>
          </div>

          {/* Cart Items */}
          <div className="flex-1 overflow-auto p-4 space-y-3">
            {cart.length === 0 ? (
              <div className="text-center text-slate-500 py-10">
                <ShoppingCart className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>السلة فارغة</p>
              </div>
            ) : (
              cart.map((item) => (
                <div
                  key={item.id}
                  className="bg-slate-700/50 rounded-lg p-3 flex items-center gap-3"
                >
                  <div className="flex-1">
                    <p className="text-white font-medium">{item.name}</p>
                    <p className="text-emerald-400 text-sm">{item.price} ر.س</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => updateQuantity(item.id, -1)}
                      className="p-1 bg-slate-600 hover:bg-slate-500 rounded transition-colors"
                    >
                      <Minus className="w-4 h-4 text-white" />
                    </button>
                    <span className="text-white w-8 text-center">{item.quantity}</span>
                    <button
                      onClick={() => updateQuantity(item.id, 1)}
                      className="p-1 bg-slate-600 hover:bg-slate-500 rounded transition-colors"
                    >
                      <Plus className="w-4 h-4 text-white" />
                    </button>
                    <button
                      onClick={() => removeFromCart(item.id)}
                      className="p-1 text-red-400 hover:bg-red-500/20 rounded transition-colors"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Discount */}
          <div className="p-4 border-t border-slate-700">
            <div className="flex items-center gap-2">
              <Percent className="w-5 h-5 text-slate-400" />
              <input
                type="number"
                placeholder="الخصم %"
                value={discount || ''}
                onChange={(e) => setDiscount(Number(e.target.value))}
                className="flex-1 px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:ring-2 focus:ring-emerald-500"
              />
            </div>
          </div>

          {/* Totals */}
          <div className="p-4 border-t border-slate-700 space-y-2">
            <div className="flex justify-between text-slate-400">
              <span>المجموع الفرعي</span>
              <span>{subtotal.toFixed(2)} ر.س</span>
            </div>
            {discount > 0 && (
              <div className="flex justify-between text-red-400">
                <span>الخصم ({discount}%)</span>
                <span>-{discountAmount.toFixed(2)} ر.س</span>
              </div>
            )}
            <div className="flex justify-between text-slate-400">
              <span>ضريبة القيمة المضافة (15%)</span>
              <span>{tax.toFixed(2)} ر.س</span>
            </div>
            <div className="flex justify-between text-white text-xl font-bold pt-2 border-t border-slate-700">
              <span>الإجمالي</span>
              <span className="text-emerald-400">{total.toFixed(2)} ر.س</span>
            </div>
          </div>

          {/* Payment Methods */}
          <div className="p-4 border-t border-slate-700">
            <p className="text-slate-400 text-sm mb-3">طريقة الدفع</p>
            <div className="grid grid-cols-3 gap-2">
              {paymentMethods.map((method) => (
                <button
                  key={method.id}
                  onClick={() => setSelectedPayment(method.id)}
                  className={`p-3 rounded-lg border transition-all ${
                    selectedPayment === method.id
                      ? `bg-${method.color}-500/20 border-${method.color}-500`
                      : 'bg-slate-700 border-slate-600 hover:border-slate-500'
                  }`}
                >
                  <method.icon className={`w-5 h-5 mx-auto mb-1 text-${method.color}-400`} />
                  <p className="text-white text-xs">{method.name}</p>
                </button>
              ))}
            </div>
          </div>

          {/* Checkout Button */}
          <div className="p-4">
            <button
              onClick={handleCheckout}
              disabled={cart.length === 0}
              className="w-full py-4 bg-emerald-600 hover:bg-emerald-700 disabled:bg-slate-700 disabled:cursor-not-allowed text-white rounded-xl font-bold text-lg transition-colors flex items-center justify-center gap-2"
            >
              <Calculator className="w-5 h-5" />
              إتمام البيع
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
