/**
 * Cart Context
 * @file frontend/src/contexts/CartContext.jsx
 * 
 * سياق سلة المشتريات لنظام نقاط البيع
 */

import React, { createContext, useContext, useReducer, useCallback, useMemo, useEffect } from 'react';
import { useLocalStorage } from '../hooks/useLocalStorage';
import { STORAGE_KEYS, TAX_RATES, TAX_TYPES } from '../constants';

// ============================================
// Cart Actions
// ============================================
const CART_ACTIONS = {
  ADD_ITEM: 'ADD_ITEM',
  REMOVE_ITEM: 'REMOVE_ITEM',
  UPDATE_QUANTITY: 'UPDATE_QUANTITY',
  UPDATE_DISCOUNT: 'UPDATE_DISCOUNT',
  CLEAR_CART: 'CLEAR_CART',
  SET_CUSTOMER: 'SET_CUSTOMER',
  SET_PAYMENT_METHOD: 'SET_PAYMENT_METHOD',
  SET_NOTES: 'SET_NOTES',
  APPLY_DISCOUNT: 'APPLY_DISCOUNT',
  REMOVE_DISCOUNT: 'REMOVE_DISCOUNT',
  HOLD_CART: 'HOLD_CART',
  RESTORE_CART: 'RESTORE_CART',
  SET_WAREHOUSE: 'SET_WAREHOUSE'
};

// ============================================
// Initial State
// ============================================
const initialState = {
  items: [],
  customer: null,
  paymentMethod: 'cash',
  notes: '',
  discount: {
    type: null, // 'percentage' | 'fixed'
    value: 0
  },
  warehouse_id: null,
  held_carts: []
};

// ============================================
// Cart Reducer
// ============================================
function cartReducer(state, action) {
  switch (action.type) {
    case CART_ACTIONS.ADD_ITEM: {
      const existingIndex = state.items.findIndex(
        item => item.product_id === action.payload.product_id && 
                item.lot_id === action.payload.lot_id
      );

      if (existingIndex >= 0) {
        // Update existing item quantity
        const newItems = [...state.items];
        newItems[existingIndex] = {
          ...newItems[existingIndex],
          quantity: newItems[existingIndex].quantity + (action.payload.quantity || 1)
        };
        return { ...state, items: newItems };
      }

      // Add new item
      return {
        ...state,
        items: [...state.items, {
          ...action.payload,
          quantity: action.payload.quantity || 1,
          discount: 0
        }]
      };
    }

    case CART_ACTIONS.REMOVE_ITEM: {
      return {
        ...state,
        items: state.items.filter((_, index) => index !== action.payload)
      };
    }

    case CART_ACTIONS.UPDATE_QUANTITY: {
      const { index, quantity } = action.payload;
      if (quantity <= 0) {
        return {
          ...state,
          items: state.items.filter((_, i) => i !== index)
        };
      }
      
      const newItems = [...state.items];
      newItems[index] = { ...newItems[index], quantity };
      return { ...state, items: newItems };
    }

    case CART_ACTIONS.UPDATE_DISCOUNT: {
      const { index, discount } = action.payload;
      const newItems = [...state.items];
      newItems[index] = { ...newItems[index], discount };
      return { ...state, items: newItems };
    }

    case CART_ACTIONS.CLEAR_CART: {
      return {
        ...state,
        items: [],
        customer: null,
        notes: '',
        discount: { type: null, value: 0 }
      };
    }

    case CART_ACTIONS.SET_CUSTOMER: {
      return { ...state, customer: action.payload };
    }

    case CART_ACTIONS.SET_PAYMENT_METHOD: {
      return { ...state, paymentMethod: action.payload };
    }

    case CART_ACTIONS.SET_NOTES: {
      return { ...state, notes: action.payload };
    }

    case CART_ACTIONS.APPLY_DISCOUNT: {
      return { ...state, discount: action.payload };
    }

    case CART_ACTIONS.REMOVE_DISCOUNT: {
      return { ...state, discount: { type: null, value: 0 } };
    }

    case CART_ACTIONS.SET_WAREHOUSE: {
      return { ...state, warehouse_id: action.payload };
    }

    case CART_ACTIONS.HOLD_CART: {
      if (state.items.length === 0) return state;
      
      const heldCart = {
        id: Date.now(),
        items: state.items,
        customer: state.customer,
        notes: state.notes,
        discount: state.discount,
        timestamp: new Date().toISOString()
      };

      return {
        ...state,
        items: [],
        customer: null,
        notes: '',
        discount: { type: null, value: 0 },
        held_carts: [...state.held_carts, heldCart]
      };
    }

    case CART_ACTIONS.RESTORE_CART: {
      const cartToRestore = state.held_carts.find(c => c.id === action.payload);
      if (!cartToRestore) return state;

      return {
        ...state,
        items: cartToRestore.items,
        customer: cartToRestore.customer,
        notes: cartToRestore.notes,
        discount: cartToRestore.discount,
        held_carts: state.held_carts.filter(c => c.id !== action.payload)
      };
    }

    default:
      return state;
  }
}

// ============================================
// Cart Context
// ============================================
const CartContext = createContext(null);

export function CartProvider({ children }) {
  const [savedCart, setSavedCart] = useLocalStorage(STORAGE_KEYS.CART, initialState);
  const [state, dispatch] = useReducer(cartReducer, savedCart);

  // Persist cart to localStorage
  useEffect(() => {
    setSavedCart(state);
  }, [state, setSavedCart]);

  // ============================================
  // Actions
  // ============================================
  const addItem = useCallback((product, lot = null) => {
    dispatch({
      type: CART_ACTIONS.ADD_ITEM,
      payload: {
        product_id: product.id,
        lot_id: lot?.id || null,
        name: product.name,
        sku: product.sku,
        barcode: product.barcode,
        price: product.selling_price,
        cost: product.cost_price,
        tax_type: product.tax_type || TAX_TYPES.VAT,
        unit: product.unit?.name || 'قطعة',
        max_quantity: lot?.quantity || product.current_stock,
        lot_number: lot?.lot_number,
        expiry_date: lot?.expiry_date
      }
    });
  }, []);

  const removeItem = useCallback((index) => {
    dispatch({ type: CART_ACTIONS.REMOVE_ITEM, payload: index });
  }, []);

  const updateQuantity = useCallback((index, quantity) => {
    dispatch({
      type: CART_ACTIONS.UPDATE_QUANTITY,
      payload: { index, quantity }
    });
  }, []);

  const updateItemDiscount = useCallback((index, discount) => {
    dispatch({
      type: CART_ACTIONS.UPDATE_DISCOUNT,
      payload: { index, discount }
    });
  }, []);

  const clearCart = useCallback(() => {
    dispatch({ type: CART_ACTIONS.CLEAR_CART });
  }, []);

  const setCustomer = useCallback((customer) => {
    dispatch({ type: CART_ACTIONS.SET_CUSTOMER, payload: customer });
  }, []);

  const setPaymentMethod = useCallback((method) => {
    dispatch({ type: CART_ACTIONS.SET_PAYMENT_METHOD, payload: method });
  }, []);

  const setNotes = useCallback((notes) => {
    dispatch({ type: CART_ACTIONS.SET_NOTES, payload: notes });
  }, []);

  const applyDiscount = useCallback((type, value) => {
    dispatch({
      type: CART_ACTIONS.APPLY_DISCOUNT,
      payload: { type, value }
    });
  }, []);

  const removeDiscount = useCallback(() => {
    dispatch({ type: CART_ACTIONS.REMOVE_DISCOUNT });
  }, []);

  const setWarehouse = useCallback((warehouseId) => {
    dispatch({ type: CART_ACTIONS.SET_WAREHOUSE, payload: warehouseId });
  }, []);

  const holdCart = useCallback(() => {
    dispatch({ type: CART_ACTIONS.HOLD_CART });
  }, []);

  const restoreCart = useCallback((cartId) => {
    dispatch({ type: CART_ACTIONS.RESTORE_CART, payload: cartId });
  }, []);

  // ============================================
  // Computed Values
  // ============================================
  const calculations = useMemo(() => {
    // Calculate subtotal
    const subtotal = state.items.reduce((sum, item) => {
      const itemTotal = item.price * item.quantity;
      const itemDiscount = item.discount || 0;
      return sum + (itemTotal - itemDiscount);
    }, 0);

    // Calculate total items discount
    const itemsDiscount = state.items.reduce((sum, item) => {
      return sum + (item.discount || 0);
    }, 0);

    // Calculate cart discount
    let cartDiscount = 0;
    if (state.discount.type === 'percentage') {
      cartDiscount = (subtotal * state.discount.value) / 100;
    } else if (state.discount.type === 'fixed') {
      cartDiscount = state.discount.value;
    }

    // Calculate tax
    const taxableAmount = subtotal - cartDiscount;
    const tax = state.items.reduce((sum, item) => {
      if (item.tax_type === TAX_TYPES.VAT) {
        const itemTotal = (item.price * item.quantity) - (item.discount || 0);
        const itemDiscountRatio = cartDiscount > 0 ? (itemTotal / subtotal) : 0;
        const itemCartDiscount = cartDiscount * itemDiscountRatio;
        const taxableItem = itemTotal - itemCartDiscount;
        return sum + (taxableItem * TAX_RATES[TAX_TYPES.VAT] / 100);
      }
      return sum;
    }, 0);

    // Calculate total
    const total = taxableAmount + tax;

    // Calculate profit
    const totalCost = state.items.reduce((sum, item) => {
      return sum + (item.cost * item.quantity);
    }, 0);
    const profit = total - totalCost - tax;

    return {
      subtotal,
      itemsDiscount,
      cartDiscount,
      totalDiscount: itemsDiscount + cartDiscount,
      tax,
      total,
      totalCost,
      profit,
      itemCount: state.items.length,
      totalQuantity: state.items.reduce((sum, item) => sum + item.quantity, 0)
    };
  }, [state.items, state.discount]);

  // ============================================
  // Context Value
  // ============================================
  const value = useMemo(() => ({
    // State
    items: state.items,
    customer: state.customer,
    paymentMethod: state.paymentMethod,
    notes: state.notes,
    discount: state.discount,
    warehouse_id: state.warehouse_id,
    heldCarts: state.held_carts,

    // Calculations
    ...calculations,

    // Actions
    addItem,
    removeItem,
    updateQuantity,
    updateItemDiscount,
    clearCart,
    setCustomer,
    setPaymentMethod,
    setNotes,
    applyDiscount,
    removeDiscount,
    setWarehouse,
    holdCart,
    restoreCart,

    // Helpers
    isEmpty: state.items.length === 0,
    hasCustomer: !!state.customer,
    hasDiscount: state.discount.type !== null
  }), [
    state,
    calculations,
    addItem,
    removeItem,
    updateQuantity,
    updateItemDiscount,
    clearCart,
    setCustomer,
    setPaymentMethod,
    setNotes,
    applyDiscount,
    removeDiscount,
    setWarehouse,
    holdCart,
    restoreCart
  ]);

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  );
}

// ============================================
// Hook
// ============================================
export function useCart() {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
}

export default CartContext;
