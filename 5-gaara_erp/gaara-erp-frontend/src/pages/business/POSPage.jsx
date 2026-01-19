/**
 * Point of Sale (POS) Page - نقطة البيع
 * Gaara ERP v12
 *
 * Complete POS system with product selection, cart management, and payment processing.
 *
 * @author Global v35.0 Singularity
 * @version 2.0.0
 */

import { useState, useEffect, useCallback, useMemo } from "react"
import { toast } from "sonner"
import {
  ShoppingCart,
  Search,
  Plus,
  Minus,
  Trash2,
  CreditCard,
  Banknote,
  Smartphone,
  Receipt,
  User,
  Package,
  Barcode,
  Grid3X3,
  List,
  Calculator,
  Percent,
  Tag,
  Clock,
  CheckCircle2,
  XCircle,
  RefreshCw,
  Settings,
  Printer,
  History,
  Pause,
  Play,
  ArrowLeft,
  Keyboard,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

// Mock data
const mockProducts = [
  { id: "P001", name: "بذور قمح سخا 94", category: "بذور", price: 15, stock: 5000, unit: "كجم", barcode: "6281000000001", image: null },
  { id: "P002", name: "سماد يوريا 46%", category: "أسمدة", price: 25, stock: 2000, unit: "كجم", barcode: "6281000000002", image: null },
  { id: "P003", name: "مبيد حشري نيم", category: "مبيدات", price: 85, stock: 150, unit: "لتر", barcode: "6281000000003", image: null },
  { id: "P004", name: "بذور طماطم هجين", category: "بذور", price: 450, stock: 50, unit: "كجم", barcode: "6281000000004", image: null },
  { id: "P005", name: "سماد NPK مركب", category: "أسمدة", price: 35, stock: 1500, unit: "كجم", barcode: "6281000000005", image: null },
  { id: "P006", name: "مبيد فطري", category: "مبيدات", price: 120, stock: 80, unit: "لتر", barcode: "6281000000006", image: null },
  { id: "P007", name: "بذور خيار", category: "بذور", price: 280, stock: 100, unit: "كجم", barcode: "6281000000007", image: null },
  { id: "P008", name: "سماد بوتاسيوم", category: "أسمدة", price: 45, stock: 800, unit: "كجم", barcode: "6281000000008", image: null },
  { id: "P009", name: "معدات ري صغيرة", category: "معدات", price: 250, stock: 25, unit: "قطعة", barcode: "6281000000009", image: null },
  { id: "P010", name: "أدوات زراعية يدوية", category: "معدات", price: 75, stock: 40, unit: "قطعة", barcode: "6281000000010", image: null },
]

const mockCustomers = [
  { id: "C001", name: "عميل نقدي (عام)", phone: "", balance: 0 },
  { id: "C002", name: "شركة الزراعة الحديثة", phone: "0501234567", balance: 15000 },
  { id: "C003", name: "مزرعة النخيل الذهبي", phone: "0559876543", balance: 8000 },
  { id: "C004", name: "أحمد محمد العلي", phone: "0541234567", balance: 0 },
]

const categories = ["الكل", "بذور", "أسمدة", "مبيدات", "معدات"]

const POSPage = () => {
  // State
  const [products, setProducts] = useState(mockProducts)
  const [cart, setCart] = useState([])
  const [searchQuery, setSearchQuery] = useState("")
  const [categoryFilter, setCategoryFilter] = useState("الكل")
  const [selectedCustomer, setSelectedCustomer] = useState(mockCustomers[0])
  const [viewMode, setViewMode] = useState("grid") // grid or list
  const [isPaymentDialogOpen, setIsPaymentDialogOpen] = useState(false)
  const [isCustomerDialogOpen, setIsCustomerDialogOpen] = useState(false)
  const [isReceiptDialogOpen, setIsReceiptDialogOpen] = useState(false)
  const [paymentMethod, setPaymentMethod] = useState("cash")
  const [receivedAmount, setReceivedAmount] = useState("")
  const [discount, setDiscount] = useState(0)
  const [discountType, setDiscountType] = useState("percent") // percent or fixed
  const [lastReceipt, setLastReceipt] = useState(null)
  const [holdOrders, setHoldOrders] = useState([])
  const [barcodeInput, setBarcodeInput] = useState("")

  // Filter products
  const filteredProducts = useMemo(() => {
    return products.filter(p => {
      const matchesSearch = p.name.includes(searchQuery) || 
                           p.barcode?.includes(searchQuery) ||
                           p.id.toLowerCase().includes(searchQuery.toLowerCase())
      const matchesCategory = categoryFilter === "الكل" || p.category === categoryFilter
      return matchesSearch && matchesCategory
    })
  }, [products, searchQuery, categoryFilter])

  // Cart calculations
  const cartSubtotal = useMemo(() => cart.reduce((sum, item) => sum + (item.price * item.quantity), 0), [cart])
  
  const discountAmount = useMemo(() => {
    if (discountType === "percent") {
      return (cartSubtotal * discount) / 100
    }
    return discount
  }, [cartSubtotal, discount, discountType])
  
  const taxRate = 0.15
  const cartTax = useMemo(() => (cartSubtotal - discountAmount) * taxRate, [cartSubtotal, discountAmount])
  const cartTotal = useMemo(() => cartSubtotal - discountAmount + cartTax, [cartSubtotal, discountAmount, cartTax])
  const changeAmount = useMemo(() => Math.max(0, parseFloat(receivedAmount || 0) - cartTotal), [receivedAmount, cartTotal])

  // Barcode handler
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Handle barcode scanner input (typically ends with Enter)
      if (e.key === 'Enter' && barcodeInput) {
        const product = products.find(p => p.barcode === barcodeInput)
        if (product) {
          addToCart(product)
        } else {
          toast.error("المنتج غير موجود")
        }
        setBarcodeInput("")
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [barcodeInput, products])

  // Cart functions
  const addToCart = (product) => {
    if (product.stock <= 0) {
      toast.error("المنتج غير متوفر في المخزون")
      return
    }
    
    setCart(prevCart => {
      const existingItem = prevCart.find(item => item.id === product.id)
      if (existingItem) {
        if (existingItem.quantity >= product.stock) {
          toast.error("لا يمكن إضافة أكثر من الكمية المتاحة")
          return prevCart
        }
        return prevCart.map(item =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        )
      }
      return [...prevCart, { ...product, quantity: 1 }]
    })
  }

  const updateQuantity = (productId, newQuantity) => {
    const product = products.find(p => p.id === productId)
    if (newQuantity > product.stock) {
      toast.error("الكمية المطلوبة أكبر من المتاح")
      return
    }
    if (newQuantity <= 0) {
      removeFromCart(productId)
      return
    }
    setCart(cart.map(item =>
      item.id === productId ? { ...item, quantity: newQuantity } : item
    ))
  }

  const removeFromCart = (productId) => {
    setCart(cart.filter(item => item.id !== productId))
  }

  const clearCart = () => {
    setCart([])
    setDiscount(0)
    setSelectedCustomer(mockCustomers[0])
  }

  // Hold order
  const holdOrder = () => {
    if (cart.length === 0) return
    const holdOrder = {
      id: `HOLD-${Date.now()}`,
      items: cart,
      customer: selectedCustomer,
      discount,
      discountType,
      timestamp: new Date().toISOString(),
    }
    setHoldOrders([...holdOrders, holdOrder])
    clearCart()
    toast.success("تم تعليق الطلب")
  }

  const recallOrder = (holdOrderId) => {
    const order = holdOrders.find(o => o.id === holdOrderId)
    if (!order) return
    setCart(order.items)
    setSelectedCustomer(order.customer)
    setDiscount(order.discount)
    setDiscountType(order.discountType)
    setHoldOrders(holdOrders.filter(o => o.id !== holdOrderId))
    toast.success("تم استرجاع الطلب")
  }

  // Payment
  const processPayment = () => {
    if (cart.length === 0) {
      toast.error("السلة فارغة")
      return
    }
    
    if (paymentMethod === "cash" && parseFloat(receivedAmount || 0) < cartTotal) {
      toast.error("المبلغ المستلم أقل من الإجمالي")
      return
    }

    // Generate receipt
    const receipt = {
      id: `RCP-${Date.now()}`,
      date: new Date().toISOString(),
      customer: selectedCustomer,
      items: cart,
      subtotal: cartSubtotal,
      discount: discountAmount,
      tax: cartTax,
      total: cartTotal,
      paymentMethod,
      received: parseFloat(receivedAmount || cartTotal),
      change: changeAmount,
    }

    // Update stock
    setProducts(products.map(p => {
      const cartItem = cart.find(c => c.id === p.id)
      if (cartItem) {
        return { ...p, stock: p.stock - cartItem.quantity }
      }
      return p
    }))

    setLastReceipt(receipt)
    setIsPaymentDialogOpen(false)
    setIsReceiptDialogOpen(true)
    clearCart()
    setReceivedAmount("")
    toast.success("تمت عملية البيع بنجاح")
  }

  // Quick amount buttons
  const quickAmounts = [50, 100, 200, 500, 1000]

  return (
    <div className="h-[calc(100vh-4rem)] flex">
      {/* Left Panel - Products */}
      <div className="flex-1 flex flex-col p-4 overflow-hidden">
        {/* Search and Filters */}
        <div className="flex gap-4 mb-4">
          <div className="flex-1 relative">
            <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="بحث بالاسم أو الباركود..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pr-10"
            />
          </div>
          <div className="flex gap-2">
            <Button
              variant={viewMode === "grid" ? "default" : "outline"}
              size="icon"
              onClick={() => setViewMode("grid")}
            >
              <Grid3X3 className="w-4 h-4" />
            </Button>
            <Button
              variant={viewMode === "list" ? "default" : "outline"}
              size="icon"
              onClick={() => setViewMode("list")}
            >
              <List className="w-4 h-4" />
            </Button>
          </div>
        </div>

        {/* Categories */}
        <div className="flex gap-2 mb-4 overflow-x-auto pb-2">
          {categories.map((cat) => (
            <Button
              key={cat}
              variant={categoryFilter === cat ? "default" : "outline"}
              size="sm"
              onClick={() => setCategoryFilter(cat)}
            >
              {cat}
            </Button>
          ))}
        </div>

        {/* Products Grid/List */}
        <ScrollArea className="flex-1">
          {viewMode === "grid" ? (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3">
              {filteredProducts.map((product) => (
                <Card
                  key={product.id}
                  className={`cursor-pointer hover:border-primary transition-colors ${product.stock <= 0 ? "opacity-50" : ""}`}
                  onClick={() => addToCart(product)}
                >
                  <CardContent className="p-3">
                    <div className="w-full h-20 bg-muted rounded-lg flex items-center justify-center mb-2">
                      <Package className="w-8 h-8 text-muted-foreground" />
                    </div>
                    <h3 className="font-medium text-sm line-clamp-2 mb-1">{product.name}</h3>
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-primary">{product.price} ر.س</span>
                      <Badge variant={product.stock > 10 ? "secondary" : "destructive"} className="text-xs">
                        {product.stock} {product.unit}
                      </Badge>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <div className="space-y-2">
              {filteredProducts.map((product) => (
                <Card
                  key={product.id}
                  className={`cursor-pointer hover:border-primary transition-colors ${product.stock <= 0 ? "opacity-50" : ""}`}
                  onClick={() => addToCart(product)}
                >
                  <CardContent className="p-3 flex items-center gap-4">
                    <div className="w-12 h-12 bg-muted rounded-lg flex items-center justify-center flex-shrink-0">
                      <Package className="w-6 h-6 text-muted-foreground" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-medium truncate">{product.name}</h3>
                      <p className="text-sm text-muted-foreground">{product.category} • {product.id}</p>
                    </div>
                    <div className="text-left">
                      <p className="font-bold text-primary">{product.price} ر.س</p>
                      <Badge variant={product.stock > 10 ? "secondary" : "destructive"} className="text-xs">
                        {product.stock} {product.unit}
                      </Badge>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </ScrollArea>
      </div>

      {/* Right Panel - Cart */}
      <div className="w-96 border-r bg-card flex flex-col">
        {/* Customer Selection */}
        <div className="p-4 border-b">
          <div
            className="flex items-center gap-3 p-3 rounded-lg bg-muted cursor-pointer hover:bg-muted/80"
            onClick={() => setIsCustomerDialogOpen(true)}
          >
            <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
              <User className="w-5 h-5 text-primary" />
            </div>
            <div className="flex-1">
              <p className="font-medium">{selectedCustomer.name}</p>
              <p className="text-sm text-muted-foreground">{selectedCustomer.phone || "بدون رقم"}</p>
            </div>
          </div>
        </div>

        {/* Cart Items */}
        <ScrollArea className="flex-1 p-4">
          {cart.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <ShoppingCart className="w-16 h-16 text-muted-foreground/30 mb-4" />
              <p className="text-muted-foreground">السلة فارغة</p>
              <p className="text-sm text-muted-foreground">اضغط على منتج لإضافته</p>
            </div>
          ) : (
            <div className="space-y-3">
              {cart.map((item) => (
                <div key={item.id} className="flex items-center gap-3 p-3 rounded-lg bg-muted">
                  <div className="flex-1 min-w-0">
                    <p className="font-medium truncate">{item.name}</p>
                    <p className="text-sm text-muted-foreground">{item.price} ر.س × {item.quantity}</p>
                  </div>
                  <div className="flex items-center gap-1">
                    <Button
                      variant="outline"
                      size="icon"
                      className="h-7 w-7"
                      onClick={() => updateQuantity(item.id, item.quantity - 1)}
                    >
                      <Minus className="w-3 h-3" />
                    </Button>
                    <Input
                      type="number"
                      value={item.quantity}
                      onChange={(e) => updateQuantity(item.id, parseInt(e.target.value) || 0)}
                      className="w-14 h-7 text-center"
                    />
                    <Button
                      variant="outline"
                      size="icon"
                      className="h-7 w-7"
                      onClick={() => updateQuantity(item.id, item.quantity + 1)}
                    >
                      <Plus className="w-3 h-3" />
                    </Button>
                  </div>
                  <div className="w-20 text-left">
                    <p className="font-bold">{(item.price * item.quantity).toLocaleString()} ر.س</p>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-7 w-7 text-red-500"
                    onClick={() => removeFromCart(item.id)}
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              ))}
            </div>
          )}
        </ScrollArea>

        {/* Discount */}
        {cart.length > 0 && (
          <div className="p-4 border-t">
            <div className="flex items-center gap-2">
              <Select value={discountType} onValueChange={setDiscountType}>
                <SelectTrigger className="w-24">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="percent">%</SelectItem>
                  <SelectItem value="fixed">ر.س</SelectItem>
                </SelectContent>
              </Select>
              <Input
                type="number"
                placeholder="خصم"
                value={discount || ""}
                onChange={(e) => setDiscount(parseFloat(e.target.value) || 0)}
                className="flex-1"
              />
            </div>
          </div>
        )}

        {/* Totals */}
        <div className="p-4 border-t bg-muted/50">
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span>المجموع الفرعي</span>
              <span>{cartSubtotal.toLocaleString()} ر.س</span>
            </div>
            {discountAmount > 0 && (
              <div className="flex justify-between text-green-600">
                <span>الخصم</span>
                <span>-{discountAmount.toLocaleString()} ر.س</span>
              </div>
            )}
            <div className="flex justify-between">
              <span>الضريبة (15%)</span>
              <span>{cartTax.toLocaleString()} ر.س</span>
            </div>
            <Separator />
            <div className="flex justify-between text-lg font-bold">
              <span>الإجمالي</span>
              <span className="text-primary">{cartTotal.toLocaleString()} ر.س</span>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="p-4 border-t space-y-2">
          <div className="flex gap-2">
            <Button variant="outline" className="flex-1" onClick={holdOrder} disabled={cart.length === 0}>
              <Pause className="w-4 h-4 ml-2" />
              تعليق
            </Button>
            <Button variant="outline" className="flex-1" onClick={clearCart} disabled={cart.length === 0}>
              <Trash2 className="w-4 h-4 ml-2" />
              مسح
            </Button>
          </div>
          <Button
            className="w-full h-12 text-lg"
            onClick={() => setIsPaymentDialogOpen(true)}
            disabled={cart.length === 0}
          >
            <CreditCard className="w-5 h-5 ml-2" />
            دفع ({cartTotal.toLocaleString()} ر.س)
          </Button>
        </div>

        {/* Hold Orders */}
        {holdOrders.length > 0 && (
          <div className="p-4 border-t">
            <p className="text-sm text-muted-foreground mb-2">الطلبات المعلقة ({holdOrders.length})</p>
            <div className="space-y-2">
              {holdOrders.map((order) => (
                <Button
                  key={order.id}
                  variant="outline"
                  className="w-full justify-start"
                  onClick={() => recallOrder(order.id)}
                >
                  <Play className="w-4 h-4 ml-2" />
                  {order.customer.name} - {order.items.length} منتج
                </Button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Payment Dialog */}
      <Dialog open={isPaymentDialogOpen} onOpenChange={setIsPaymentDialogOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <CreditCard className="w-5 h-5" />
              إتمام عملية الدفع
            </DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div className="p-4 rounded-lg bg-primary/5 text-center">
              <p className="text-sm text-muted-foreground">المبلغ المطلوب</p>
              <p className="text-3xl font-bold text-primary">{cartTotal.toLocaleString()} ر.س</p>
            </div>

            <div>
              <Label>طريقة الدفع</Label>
              <div className="grid grid-cols-3 gap-2 mt-2">
                <Button
                  variant={paymentMethod === "cash" ? "default" : "outline"}
                  className="flex-col h-auto py-3"
                  onClick={() => setPaymentMethod("cash")}
                >
                  <Banknote className="w-6 h-6 mb-1" />
                  <span className="text-xs">نقدي</span>
                </Button>
                <Button
                  variant={paymentMethod === "card" ? "default" : "outline"}
                  className="flex-col h-auto py-3"
                  onClick={() => setPaymentMethod("card")}
                >
                  <CreditCard className="w-6 h-6 mb-1" />
                  <span className="text-xs">بطاقة</span>
                </Button>
                <Button
                  variant={paymentMethod === "transfer" ? "default" : "outline"}
                  className="flex-col h-auto py-3"
                  onClick={() => setPaymentMethod("transfer")}
                >
                  <Smartphone className="w-6 h-6 mb-1" />
                  <span className="text-xs">تحويل</span>
                </Button>
              </div>
            </div>

            {paymentMethod === "cash" && (
              <>
                <div>
                  <Label>المبلغ المستلم</Label>
                  <Input
                    type="number"
                    value={receivedAmount}
                    onChange={(e) => setReceivedAmount(e.target.value)}
                    className="text-lg h-12"
                    placeholder="0"
                  />
                </div>
                <div className="flex flex-wrap gap-2">
                  {quickAmounts.map((amount) => (
                    <Button
                      key={amount}
                      variant="outline"
                      size="sm"
                      onClick={() => setReceivedAmount(String(amount))}
                    >
                      {amount}
                    </Button>
                  ))}
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setReceivedAmount(String(Math.ceil(cartTotal)))}
                  >
                    المبلغ بالضبط
                  </Button>
                </div>
                {parseFloat(receivedAmount || 0) >= cartTotal && (
                  <div className="p-4 rounded-lg bg-green-50 text-center">
                    <p className="text-sm text-green-600">الباقي</p>
                    <p className="text-2xl font-bold text-green-600">{changeAmount.toLocaleString()} ر.س</p>
                  </div>
                )}
              </>
            )}
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsPaymentDialogOpen(false)}>إلغاء</Button>
            <Button onClick={processPayment}>
              <CheckCircle2 className="w-4 h-4 ml-2" />
              تأكيد الدفع
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Customer Dialog */}
      <Dialog open={isCustomerDialogOpen} onOpenChange={setIsCustomerDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>اختيار العميل</DialogTitle>
          </DialogHeader>
          <div className="space-y-2">
            {mockCustomers.map((customer) => (
              <div
                key={customer.id}
                className={`p-3 rounded-lg border cursor-pointer hover:bg-muted ${selectedCustomer.id === customer.id ? "border-primary bg-primary/5" : ""}`}
                onClick={() => { setSelectedCustomer(customer); setIsCustomerDialogOpen(false); }}
              >
                <p className="font-medium">{customer.name}</p>
                <p className="text-sm text-muted-foreground">{customer.phone || "بدون رقم"}</p>
              </div>
            ))}
          </div>
        </DialogContent>
      </Dialog>

      {/* Receipt Dialog */}
      <Dialog open={isReceiptDialogOpen} onOpenChange={setIsReceiptDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Receipt className="w-5 h-5" />
              الفاتورة
            </DialogTitle>
          </DialogHeader>
          {lastReceipt && (
            <div className="space-y-4">
              <div className="text-center border-b pb-4">
                <h3 className="font-bold text-lg">نظام جارا ERP</h3>
                <p className="text-sm text-muted-foreground">فاتورة ضريبية مبسطة</p>
                <p className="text-xs text-muted-foreground mt-2">{lastReceipt.id}</p>
                <p className="text-xs text-muted-foreground">{new Date(lastReceipt.date).toLocaleString('ar-SA')}</p>
              </div>
              
              <div className="space-y-2">
                {lastReceipt.items.map((item) => (
                  <div key={item.id} className="flex justify-between text-sm">
                    <span>{item.name} × {item.quantity}</span>
                    <span>{(item.price * item.quantity).toLocaleString()} ر.س</span>
                  </div>
                ))}
              </div>
              
              <div className="border-t pt-4 space-y-2 text-sm">
                <div className="flex justify-between">
                  <span>المجموع الفرعي</span>
                  <span>{lastReceipt.subtotal.toLocaleString()} ر.س</span>
                </div>
                {lastReceipt.discount > 0 && (
                  <div className="flex justify-between text-green-600">
                    <span>الخصم</span>
                    <span>-{lastReceipt.discount.toLocaleString()} ر.س</span>
                  </div>
                )}
                <div className="flex justify-between">
                  <span>الضريبة (15%)</span>
                  <span>{lastReceipt.tax.toLocaleString()} ر.س</span>
                </div>
                <div className="flex justify-between font-bold text-lg border-t pt-2">
                  <span>الإجمالي</span>
                  <span>{lastReceipt.total.toLocaleString()} ر.س</span>
                </div>
              </div>
              
              <div className="text-center text-sm text-muted-foreground">
                <p>شكراً لتعاملكم معنا</p>
              </div>
            </div>
          )}
          <DialogFooter>
            <Button variant="outline" onClick={() => toast.info("جاري الطباعة...")}>
              <Printer className="w-4 h-4 ml-2" />
              طباعة
            </Button>
            <Button onClick={() => setIsReceiptDialogOpen(false)}>
              إغلاق
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

export default POSPage
