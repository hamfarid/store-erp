/**
 * صفحة نظام نقطة البيع (POS)
 */
import React, { useState, useEffect, useRef } from 'react';
import posService from '../services/posService';
import './POSSystem.css';

const POSSystem = () => {
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
  
  const searchInputRef = useRef(null);
  const barcodeInputRef = useRef(null);

  useEffect(() => {
    checkCurrentShift();
    // Focus on barcode input
    if (barcodeInputRef.current) {
      barcodeInputRef.current.focus();
    }
  }, []);

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
      setShowOpenShift(true);
    }
  };

  const handleOpenShift = async () => {
    try {
      setLoading(true);
      const userId = localStorage.getItem('user_id');
      const result = await posService.openShift({
        user_id: userId,
        opening_cash: parseFloat(openingCash)
      });
      
      if (result.success) {
        setCurrentShift(result.shift);
        setShowOpenShift(false);
        alert('تم فتح الوردية بنجاح');
      }
    } catch (error) {
      alert('خطأ في فتح الوردية: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (query) => {
    setSearchQuery(query);
    if (query.length < 2) {
      setSearchResults([]);
      return;
    }

    try {
      const result = await posService.searchProducts(query);
      if (result.success) {
        setSearchResults(result.products);
      }
    } catch (error) {
      console.error('خطأ في البحث:', error);
    }
  };

  const handleBarcodeInput = async (e) => {
    if (e.key === 'Enter') {
      const barcode = e.target.value.trim();
      if (barcode) {
        await handleSearch(barcode);
        if (searchResults.length > 0) {
          addToCart(searchResults[0]);
        }
        e.target.value = '';
      }
    }
  };

  const addToCart = (product, batch = null) => {
    const existingItem = cart.find(item => 
      item.product_id === product.id && 
      (batch ? item.batch_id === batch.id : true)
    );

    if (existingItem) {
      setCart(cart.map(item =>
        item.product_id === product.id && (batch ? item.batch_id === batch.id : true)
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ));
    } else {
      const selectedBatch = batch || (product.batches && product.batches[0]);
      setCart([...cart, {
        product_id: product.id,
        batch_id: selectedBatch?.id,
        product_name: product.name,
        product_code: product.code,
        unit_price: product.selling_price,
        quantity: 1,
        lot_number: selectedBatch?.batch_number,
        expiry_date: selectedBatch?.expiry_date
      }]);
    }
    
    setSearchQuery('');
    setSearchResults([]);
    if (barcodeInputRef.current) {
      barcodeInputRef.current.focus();
    }
  };

  const updateQuantity = (index, quantity) => {
    if (quantity <= 0) {
      removeFromCart(index);
      return;
    }
    
    setCart(cart.map((item, i) =>
      i === index ? { ...item, quantity: parseFloat(quantity) } : item
    ));
  };

  const removeFromCart = (index) => {
    setCart(cart.filter((_, i) => i !== index));
  };

  const calculateSubtotal = () => {
    return cart.reduce((sum, item) => sum + (item.unit_price * item.quantity), 0);
  };

  const calculateDiscount = () => {
    return calculateSubtotal() * (discount / 100);
  };

  const calculateTax = () => {
    return (calculateSubtotal() - calculateDiscount()) * (tax / 100);
  };

  const calculateTotal = () => {
    return calculateSubtotal() - calculateDiscount() + calculateTax();
  };

  const calculateChange = () => {
    return paidAmount - calculateTotal();
  };

  const handleCheckout = async () => {
    if (cart.length === 0) {
      alert('السلة فارغة');
      return;
    }

    if (!currentShift) {
      alert('يجب فتح وردية أولاً');
      return;
    }

    if (paymentMethod === 'cash' && paidAmount < calculateTotal()) {
      alert('المبلغ المدفوع أقل من الإجمالي');
      return;
    }

    try {
      setLoading(true);
      const userId = localStorage.getItem('user_id');
      
      const saleData = {
        user_id: userId,
        shift_id: currentShift.id,
        customer_id: selectedCustomer?.id,
        customer_name: selectedCustomer?.name,
        items: cart,
        discount_percentage: discount,
        tax_percentage: tax,
        payment_method: paymentMethod,
        paid_amount: paymentMethod === 'cash' ? paidAmount : calculateTotal()
      };

      const result = await posService.createSale(saleData);
      
      if (result.success) {
        alert('تم إتمام عملية البيع بنجاح');
        // Print receipt
        printReceipt(result.sale);
        // Clear cart
        setCart([]);
        setPaidAmount(0);
        setDiscount(0);
        setSelectedCustomer(null);
        if (barcodeInputRef.current) {
          barcodeInputRef.current.focus();
        }
      }
    } catch (error) {
      alert('خطأ في إتمام عملية البيع: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const printReceipt = (sale) => {
    // TODO: Implement receipt printing
    console.log('Printing receipt:', sale);
  };

  const handleCloseShift = async () => {
    if (!currentShift) return;

    const closingCash = prompt('أدخل النقدية في الدرج:');
    if (closingCash === null) return;

    try {
      setLoading(true);
      const result = await posService.closeShift(currentShift.id, {
        closing_cash: parseFloat(closingCash)
      });

      if (result.success) {
        alert('تم إغلاق الوردية بنجاح');
        setCurrentShift(null);
        setShowOpenShift(true);
      }
    } catch (error) {
      alert('خطأ في إغلاق الوردية: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  if (showOpenShift) {
    return (
      <div className="pos-open-shift">
        <div className="open-shift-dialog">
          <h2>فتح وردية جديدة</h2>
          <div className="form-group">
            <label>النقدية الافتتاحية:</label>
            <input
              type="number"
              value={openingCash}
              onChange={(e) => setOpeningCash(e.target.value)}
              placeholder="0.00"
              step="0.01"
            />
          </div>
          <button onClick={handleOpenShift} disabled={loading}>
            {loading ? 'جاري الفتح...' : 'فتح الوردية'}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="pos-system">
      {/* Header */}
      <div className="pos-header">
        <div className="shift-info">
          <span>الوردية: {currentShift?.shift_number}</span>
          <span>الوقت: {new Date().toLocaleTimeString('ar-SA')}</span>
        </div>
        <button onClick={handleCloseShift} className="btn-close-shift">
          إغلاق الوردية
        </button>
      </div>

      <div className="pos-content">
        {/* Left Panel - Products */}
        <div className="pos-left">
          {/* Barcode Scanner */}
          <div className="barcode-input">
            <input
              ref={barcodeInputRef}
              type="text"
              placeholder="امسح الباركود أو ابحث عن منتج..."
              onKeyPress={handleBarcodeInput}
              autoFocus
            />
          </div>

          {/* Search */}
          <div className="product-search">
            <input
              ref={searchInputRef}
              type="text"
              value={searchQuery}
              onChange={(e) => handleSearch(e.target.value)}
              placeholder="ابحث عن منتج..."
            />
            {searchResults.length > 0 && (
              <div className="search-results">
                {searchResults.map(product => (
                  <div
                    key={product.id}
                    className="search-result-item"
                    onClick={() => addToCart(product)}
                  >
                    <div className="product-info">
                      <strong>{product.name}</strong>
                      <span>{product.code}</span>
                    </div>
                    <div className="product-price">
                      {product.selling_price.toFixed(2)} ريال
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right Panel - Cart */}
        <div className="pos-right">
          {/* Cart Items */}
          <div className="cart-items">
            <h3>السلة</h3>
            {cart.length === 0 ? (
              <p className="empty-cart">السلة فارغة</p>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>المنتج</th>
                    <th>السعر</th>
                    <th>الكمية</th>
                    <th>الإجمالي</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  {cart.map((item, index) => (
                    <tr key={index}>
                      <td>
                        <div>{item.product_name}</div>
                        {item.lot_number && (
                          <small>لوط: {item.lot_number}</small>
                        )}
                      </td>
                      <td>{item.unit_price.toFixed(2)}</td>
                      <td>
                        <input
                          type="number"
                          value={item.quantity}
                          onChange={(e) => updateQuantity(index, e.target.value)}
                          min="1"
                          step="1"
                        />
                      </td>
                      <td>{(item.unit_price * item.quantity).toFixed(2)}</td>
                      <td>
                        <button onClick={() => removeFromCart(index)}>×</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          {/* Totals */}
          <div className="cart-totals">
            <div className="total-row">
              <span>المجموع الفرعي:</span>
              <span>{calculateSubtotal().toFixed(2)} ريال</span>
            </div>
            <div className="total-row">
              <span>الخصم ({discount}%):</span>
              <input
                type="number"
                value={discount}
                onChange={(e) => setDiscount(parseFloat(e.target.value) || 0)}
                min="0"
                max="100"
                step="1"
              />
              <span>-{calculateDiscount().toFixed(2)} ريال</span>
            </div>
            <div className="total-row">
              <span>الضريبة ({tax}%):</span>
              <span>+{calculateTax().toFixed(2)} ريال</span>
            </div>
            <div className="total-row total">
              <span>الإجمالي:</span>
              <span>{calculateTotal().toFixed(2)} ريال</span>
            </div>
          </div>

          {/* Payment */}
          <div className="payment-section">
            <div className="payment-method">
              <label>طريقة الدفع:</label>
              <select
                value={paymentMethod}
                onChange={(e) => setPaymentMethod(e.target.value)}
              >
                <option value="cash">نقدي</option>
                <option value="card">بطاقة</option>
                <option value="mixed">مختلط</option>
              </select>
            </div>

            {paymentMethod === 'cash' && (
              <>
                <div className="paid-amount">
                  <label>المبلغ المدفوع:</label>
                  <input
                    type="number"
                    value={paidAmount}
                    onChange={(e) => setPaidAmount(parseFloat(e.target.value) || 0)}
                    step="0.01"
                  />
                </div>
                <div className="change-amount">
                  <span>الباقي:</span>
                  <span className={calculateChange() < 0 ? 'negative' : ''}>
                    {calculateChange().toFixed(2)} ريال
                  </span>
                </div>
              </>
            )}

            <button
              className="btn-checkout"
              onClick={handleCheckout}
              disabled={loading || cart.length === 0}
            >
              {loading ? 'جاري المعالجة...' : 'إتمام البيع'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default POSSystem;
