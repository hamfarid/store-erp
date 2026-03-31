/**
 * Modern POS System Page
 * 
 * A professional Point of Sale interface using ShadCN components.
 */
import React, { useState, useEffect, useRef, useCallback } from 'react';
import { 
  Search, 
  ShoppingCart, 
  CreditCard, 
  Banknote, 
  RotateCcw, 
  Receipt, 
  User, 
  Clock, 
  LogOut, 
  Plus, 
  Minus, 
  Trash2, 
  Calculator,
  ScanBarcode,
  Grid,
  List
} from 'lucide-react';

import posService from '../services/posService';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../components/ui/table';
import LoadingSpinner from '../components/LoadingSpinner';

const POSSystem = () => {
  // State
  const [currentShift, setCurrentShift] = useState(null);
  const [cart, setCart] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [discount, setDiscount] = useState(0);
  const [tax, setTax] = useState(15); // 15% VAT
  const [paymentMethod, setPaymentMethod] = useState('cash');
  const [paidAmount, setPaidAmount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [showOpenShift, setShowOpenShift] = useState(false);
  const [openingCash, setOpeningCash] = useState(0);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  // Refs
  const searchInputRef = useRef(null);
  const barcodeInputRef = useRef(null);

  // Initial Load
  useEffect(() => {
    checkCurrentShift();
    // Focus barcode input on load
    if (barcodeInputRef.current) {
      barcodeInputRef.current.focus();
    }
  }, []);

  // Check Shift Status
  const checkCurrentShift = async () => {
    try {
      const userId = localStorage.getItem('user_id');
      const result = await posService.getCurrentShift(userId);
      if (result.success) {
        setCurrentShift(result.shift);
      } else {
        setShowOpenShift(true);
      }
    } catch (error) {
      // If 404 or other error, assume no active shift
      setShowOpenShift(true);
    }
  };

  // Open Shift
  const handleOpenShift = async () => {
    try {
      setLoading(true);
      setError(null);
      const userId = localStorage.getItem('user_id');
      const result = await posService.openShift({
        user_id: userId,
        opening_cash: parseFloat(openingCash)
      });
      
      if (result.success) {
        setCurrentShift(result.shift);
        setShowOpenShift(false);
        setSuccessMessage('تم فتح الوردية بنجاح');
        setTimeout(() => setSuccessMessage(null), 3000);
      }
    } catch (error) {
      setError('خطأ في فتح الوردية: ' + (error.response?.data?.message || error.message));
    } finally {
      setLoading(false);
    }
  };

  // Search Products
  const handleSearch = useCallback(async (query) => {
    setSearchQuery(query);
    if (!query || query.length < 2) {
      setSearchResults([]);
      return;
    }

    try {
      const result = await posService.searchProducts(query);
      if (result.success) {
        setSearchResults(result.products);
      }
    } catch (error) {
      console.error('Error searching products:', error);
    }
  }, []);

  // Add to Cart
  const addToCart = (product, batch = null) => {
    const existingItemIndex = cart.findIndex(item => 
      item.product_id === product.id && 
      (batch ? item.batch_id === batch.id : true)
    );

    if (existingItemIndex > -1) {
      const newCart = [...cart];
      newCart[existingItemIndex].quantity += 1;
      setCart(newCart);
    } else {
      const selectedBatch = batch || (product.batches && product.batches[0]);
      setCart([...cart, {
        product_id: product.id,
        batch_id: selectedBatch?.id,
        product_name: product.name,
        product_code: product.code,
        unit_price: parseFloat(product.selling_price),
        quantity: 1,
        lot_number: selectedBatch?.batch_number,
        image: product.image
      }]);
    }
    
    // Clear search and refocus
    setSearchQuery('');
    setSearchResults([]);
    if (barcodeInputRef.current) {
      barcodeInputRef.current.focus();
    }
  };

  const handleBarcodeInput = async (e) => {
    if (e.key === 'Enter') {
      const barcode = e.target.value.trim();
      if (barcode) {
        // Direct search and add if exact match found
        try {
          const result = await posService.searchProducts(barcode);
          if (result.success && result.products.length > 0) {
            // Assume first match is the product (exact match preferably)
            addToCart(result.products[0]);
            setSuccessMessage(`تم إضافة ${result.products[0].name}`);
            setTimeout(() => setSuccessMessage(null), 1500);
          } else {
            setError("المنتج غير موجود");
            setTimeout(() => setError(null), 3000);
          }
        } catch (err) {
          console.error(err);
        }
        e.target.value = '';
      }
    }
  };

  // Cart Management
  const updateQuantity = (index, delta) => {
    const newCart = [...cart];
    newCart[index].quantity += delta;
    
    if (newCart[index].quantity <= 0) {
      removeFromCart(index);
    } else {
      setCart(newCart);
    }
  };

  const setQuantity = (index, val) => {
    const qty = parseFloat(val);
    if (qty <= 0) {
      removeFromCart(index);
      return;
    }
    const newCart = [...cart];
    newCart[index].quantity = qty;
    setCart(newCart);
  };

  const removeFromCart = (index) => {
    setCart(cart.filter((_, i) => i !== index));
  };

  // Calculations
  const calculateSubtotal = () => cart.reduce((sum, item) => sum + (item.unit_price * item.quantity), 0);
  const calculateDiscount = () => calculateSubtotal() * (discount / 100);
  const calculateTax = () => (calculateSubtotal() - calculateDiscount()) * (tax / 100);
  const calculateTotal = () => calculateSubtotal() - calculateDiscount() + calculateTax();
  const calculateChange = () => paidAmount - calculateTotal();

  // Checkout
  const handleCheckout = async () => {
    if (cart.length === 0) return setError('السلة فارغة');
    if (!currentShift) return setError('يجب فتح وردية أولاً');
    
    const total = calculateTotal();
    if (paymentMethod === 'cash' && paidAmount < total) {
      return setError('المبلغ المدفوع أقل من الإجمالي');
    }

    try {
      setLoading(true);
      setError(null);
      const userId = localStorage.getItem('user_id');
      
      const saleData = {
        user_id: userId,
        shift_id: currentShift.id,
        customer_id: selectedCustomer?.id,
        items: cart,
        discount_percentage: discount,
        tax_percentage: tax,
        payment_method: paymentMethod,
        paid_amount: paymentMethod === 'cash' ? paidAmount : total
      };

      const result = await posService.createSale(saleData);
      
      if (result.success) {
        setSuccessMessage('تم إتمام عملية البيع بنجاح!');
        // Ideally print receipt here
        setCart([]);
        setPaidAmount(0);
        setDiscount(0);
        setSelectedCustomer(null);
        setTimeout(() => setSuccessMessage(null), 3000);
        
        if (barcodeInputRef.current) barcodeInputRef.current.focus();
      }
    } catch (error) {
      setError('فشل عملية البيع: ' + (error.response?.data?.message || error.message));
    } finally {
      setLoading(false);
    }
  };

  // Close Shift
  const handleCloseShift = async () => {
    if (!currentShift) return;
    const closingCash = prompt('أدخل النقدية الموجودة في الدرج للإغلاق:');
    if (closingCash === null) return;

    try {
      setLoading(true);
      const result = await posService.closeShift(currentShift.id, {
        closing_cash: parseFloat(closingCash)
      });

      if (result.success) {
        setSuccessMessage('تم إغلاق الوردية بنجاح');
        setCurrentShift(null);
        setShowOpenShift(true);
      }
    } catch (error) {
      setError('فشل إغلاق الوردية: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  // Render Open Shift Modal
  if (showOpenShift) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm">
        <Card className="w-full max-w-md shadow-2xl border-2">
          <CardHeader className="text-center">
            <div className="mx-auto w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-2">
              <Clock className="w-6 h-6 text-primary" />
            </div>
            <CardTitle className="text-xl">فتح وردية جديدة</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">النقدية الافتتاحية</label>
              <div className="relative">
                <Banknote className="absolute right-3 top-2.5 h-5 w-5 text-muted-foreground" />
                <Input
                  type="number"
                  placeholder="0.00"
                  value={openingCash}
                  onChange={(e) => setOpeningCash(e.target.value)}
                  className="pr-10 text-lg"
                  autoFocus
                />
              </div>
            </div>
            {error && <div className="text-sm text-destructive bg-destructive/10 p-2 rounded">{error}</div>}
          </CardContent>
          <CardFooter>
            <Button onClick={handleOpenShift} className="w-full" size="lg" disabled={loading}>
              {loading ? <LoadingSpinner size="sm" /> : 'بدء الوردية'}
            </Button>
          </CardFooter>
        </Card>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-background text-foreground overflow-hidden" dir="rtl">
      {/* Top Header */}
      <header className="flex-none h-16 border-b bg-card flex items-center justify-between px-6 shadow-sm z-10">
        <div className="flex items-center gap-4">
          <h1 className="text-xl font-bold flex items-center gap-2">
            <ShoppingCart className="text-primary" />
            نقطة البيع (POS)
          </h1>
          <Badge variant="outline" className="text-sm font-normal gap-1">
            <Clock size={14} />
            الوردية: #{currentShift?.shift_number || '--'}
          </Badge>
          <Badge variant="secondary" className="text-sm font-normal">
            {new Date().toLocaleDateString('ar-SA')}
          </Badge>
        </div>
        
        <div className="flex items-center gap-3">
          {successMessage && (
            <div className="bg-emerald-100 text-emerald-800 px-3 py-1 rounded-full text-sm font-medium animate-in fade-in slide-in-from-top-5">
              {successMessage}
            </div>
          )}
          {error && (
            <div className="bg-destructive/15 text-destructive px-3 py-1 rounded-full text-sm font-medium animate-in fade-in slide-in-from-top-5">
              {error}
            </div>
          )}
          <Button variant="outline" size="sm" onClick={() => window.location.reload()}>
            <RotateCcw size={16} className="mr-2" />
            تحديث
          </Button>
          <Button variant="destructive" size="sm" onClick={handleCloseShift}>
            <LogOut size={16} className="mr-2" />
            إغلاق الوردية
          </Button>
        </div>
      </header>

      <div className="flex-1 flex overflow-hidden">
        {/* Left Side: Product Search & Entry (65%) */}
        <div className="w-[65%] flex flex-col border-l border-border bg-muted/20">
          {/* Controls */}
          <div className="p-4 bg-background border-b grid gap-4">
            <div className="flex gap-4">
              <div className="relative flex-1">
                <ScanBarcode className="absolute right-3 top-2.5 h-5 w-5 text-muted-foreground" />
                <Input
                  ref={barcodeInputRef}
                  placeholder="Scan Barcode (Enter)..."
                  onKeyPress={handleBarcodeInput}
                  className="pr-10 h-11 text-lg font-mono focus-visible:ring-primary"
                />
              </div>
              <div className="relative flex-[2]">
                <Search className="absolute right-3 top-2.5 h-5 w-5 text-muted-foreground" />
                <Input
                  ref={searchInputRef}
                  placeholder="بحث عن منتج بالاسم أو الكود..."
                  value={searchQuery}
                  onChange={(e) => handleSearch(e.target.value)}
                  className="pr-10 h-11 text-lg"
                />
              </div>
            </div>
            
            {/* Search Results Dropdown/Overlay */}
            {searchResults.length > 0 && searchQuery && (
              <Card className="absolute top-[130px] left-4 right-[35%] z-20 shadow-xl max-h-[400px] overflow-auto animate-in fade-in zoom-in-95">
                <Table>
                  <TableBody>
                    {searchResults.map((product) => (
                      <TableRow 
                        key={product.id} 
                        className="cursor-pointer hover:bg-muted/50"
                        onClick={() => addToCart(product)}
                      >
                        <TableCell className="font-medium">{product.name}</TableCell>
                        <TableCell className="font-mono text-muted-foreground text-xs">{product.code}</TableCell>
                        <TableCell className="text-left font-bold text-primary">
                          {parseFloat(product.selling_price).toFixed(2)}
                        </TableCell>
                        <TableCell className="text-right">
                          <Badge variant={product.stock > 10 ? 'success' : 'warning'}>
                            {product.stock}
                          </Badge>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </Card>
            )}
          </div>

          {/* Quick Categories/Grid (Placeholder for future V2) */}
          <div className="flex-1 p-6 flex items-center justify-center text-muted-foreground border-2 border-dashed border-border/50 m-6 rounded-xl">
            <div className="text-center">
              <Grid className="w-16 h-16 mx-auto mb-4 opacity-20" />
              <h3 className="text-lg font-medium opacity-50">قائمة المنتجات السريعة</h3>
              <p className="text-sm opacity-40">سيتم إضافة تصنيفات المنتجات هنا لتسهيل الوصول</p>
            </div>
          </div>
        </div>

        {/* Right Side: Cart & Checkout (35%) */}
        <div className="w-[35%] flex flex-col bg-background shadow-xl z-20">
          
          {/* Cart Header */}
          <div className="p-4 border-b flex justify-between items-center bg-muted/10">
            <h2 className="font-bold flex items-center gap-2">
              <List size={20} />
              سلة المشتريات
            </h2>
            <div className="flex gap-2">
                <Button variant="ghost" size="icon" className="text-destructive h-8 w-8" onClick={() => setCart([])}>
                    <Trash2 size={16} />
                </Button>
            </div>
          </div>

          {/* Cart Items List */}
          <div className="flex-1 overflow-auto p-2 space-y-2 scrollbar-thin">
            {cart.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-muted-foreground opacity-50">
                <ShoppingCart size={48} className="mb-4" />
                <p>السلة فارغة</p>
              </div>
            ) : (
              cart.map((item, index) => (
                <Card key={`${item.product_id}-${index}`} className="group relative overflow-hidden border-l-4 border-l-primary shadow-sm hover:shadow-md transition-all">
                  <div className="p-3 flex justify-between items-start">
                    <div className="flex-1">
                      <h4 className="font-bold truncate">{item.product_name}</h4>
                      <p className="text-xs text-muted-foreground font-mono">{item.product_code}</p>
                      {item.lot_number && <Badge variant="outline" className="text-[10px] mt-1 px-1 py-0">{item.lot_number}</Badge>}
                    </div>
                    <div className="text-left">
                       <div className="font-bold text-lg text-primary">
                         {(item.unit_price * item.quantity).toFixed(2)}
                       </div>
                       <div className="text-xs text-muted-foreground">
                         {item.unit_price.toFixed(2)} / وحدة
                       </div>
                    </div>
                  </div>
                  
                  <div className="px-3 pb-3 pt-0 flex items-center justify-between gap-4">
                    <div className="flex items-center gap-1 bg-muted rounded-lg p-1">
                      <Button 
                        variant="ghost" 
                        size="icon" 
                        className="h-6 w-6 rounded-md hover:bg-background shadow-sm"
                        onClick={() => updateQuantity(index, -1)}
                      >
                        <Minus size={12} />
                      </Button>
                      <Input
                        className="h-6 w-12 text-center p-0 border-none bg-transparent focus-visible:ring-0 font-bold"
                        value={item.quantity}
                        onChange={(e) => setQuantity(index, e.target.value)}
                      />
                      <Button 
                        variant="ghost" 
                        size="icon" 
                        className="h-6 w-6 rounded-md hover:bg-background shadow-sm"
                        onClick={() => updateQuantity(index, 1)}
                      >
                        <Plus size={12} />
                      </Button>
                    </div>
                    <Button 
                        variant="ghost" 
                        size="icon" 
                        className="h-6 w-6 text-muted-foreground hover:text-destructive opacity-0 group-hover:opacity-100 transition-opacity"
                        onClick={() => removeFromCart(index)}
                    >
                        <Trash2 size={14} />
                    </Button>
                  </div>
                </Card>
              ))
            )}
          </div>

          {/* Checkout Area */}
          <div className="border-t bg-card p-4 shadow-[0_-4px_20px_-5px_rgba(0,0,0,0.1)] space-y-4">
            {/* Totals Summary */}
            <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                    <span className="text-muted-foreground">المجموع الفرعي:</span>
                    <span className="font-medium">{calculateSubtotal().toFixed(2)}</span>
                </div>
                <div className="flex justify-between items-center group">
                    <span className="text-muted-foreground group-hover:text-primary transition-colors flex items-center gap-1 cursor-help">
                        الخصم (%):
                    </span>
                    <Input 
                        type="number" 
                        className="h-6 w-16 text-right px-1 py-0" 
                        value={discount} 
                        onChange={e => setDiscount(parseFloat(e.target.value)||0)} 
                    />
                </div>
                <div className="flex justify-between items-center">
                    <span className="text-muted-foreground flex items-center gap-1">
                        الضريبة (%):
                    </span>
                    <Input 
                        type="number" 
                        className="h-6 w-16 text-right px-1 py-0" 
                        value={tax} 
                        onChange={e => setTax(parseFloat(e.target.value)||0)} 
                    />
                </div>
                <div className="flex justify-between pt-2 border-t mt-2">
                    <span className="font-bold text-lg">الإجمالي النهائي:</span>
                    <span className="font-bold text-xl text-primary">{calculateTotal().toFixed(2)} ريال</span>
                </div>
            </div>

            {/* Payment Method */}
            <div className="grid grid-cols-2 gap-2">
                <Button 
                    variant={paymentMethod === 'cash' ? 'default' : 'outline'} 
                    onClick={() => setPaymentMethod('cash')}
                    className="gap-2"
                >
                    <Banknote size={16} />
                    نقدي
                </Button>
                <Button 
                    variant={paymentMethod === 'card' ? 'default' : 'outline'} 
                    onClick={() => setPaymentMethod('card')}
                    className="gap-2"
                >
                    <CreditCard size={16} />
                    بطاقة
                </Button>
            </div>

            {/* Amount Paid - Only for Cash */}
            {paymentMethod === 'cash' && (
                <div className="space-y-2 animate-in slide-in-from-bottom-2 fade-in">
                    <div className="relative">
                        <span className="absolute right-3 top-2.5 text-muted-foreground text-sm">المدفوع:</span>
                        <Input 
                            type="number"
                            value={paidAmount}
                            onChange={(e) => setPaidAmount(parseFloat(e.target.value) || 0)}
                            className="pr-16 text-right font-bold text-lg"
                        />
                    </div>
                    <div className="flex justify-between px-2 text-sm font-medium">
                        <span>الباقي:</span>
                        <span className={calculateChange() < 0 ? 'text-destructive' : 'text-emerald-600'}>
                            {calculateChange().toFixed(2)} ريال
                        </span>
                    </div>
                </div>
            )}

            {/* Action Button */}
            <Button 
                size="lg" 
                className="w-full text-lg font-bold shadow-lg shadow-primary/20 hover:shadow-primary/40 transition-all"
                onClick={handleCheckout}
                disabled={loading || cart.length === 0}
            >
                {loading ? <LoadingSpinner size="sm" className="mr-2" /> : <Receipt className="mr-2" />}
                {loading ? 'جاري المعالجة...' : 'إتمام البيع (Enter)'}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default POSSystem;
