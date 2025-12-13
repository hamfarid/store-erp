// Enhanced State Management System
// نظام إدارة الحالة المحسن

import { configureStore } from '@reduxjs/toolkit';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import { combineReducers } from '@reduxjs/toolkit';

// Import reducers
import authReducer from './slices/authSlice';
import productsReducer from './slices/productsSlice';
import cartReducer from './slices/cartSlice';
import favoritesReducer from './slices/favoritesSlice';
import uiReducer from './slices/uiSlice';
import inventoryReducer from './slices/inventorySlice';
import ordersReducer from './slices/ordersSlice';
import customersReducer from './slices/customersSlice';
import reportsReducer from './slices/reportsSlice';

// Persist configuration
const persistConfig = {
  key: 'root',
  storage,
  whitelist: ['auth', 'cart', 'favorites', 'ui'], // Only persist these slices
  blacklist: ['products', 'inventory', 'orders', 'customers', 'reports'] // Don't persist these (they should be fetched fresh)
};

// Auth persist config (separate for sensitive data)
const authPersistConfig = {
  key: 'auth',
  storage,
  whitelist: ['user', 'token', 'refreshToken', 'permissions']
};

// UI persist config
const uiPersistConfig = {
  key: 'ui',
  storage,
  whitelist: ['theme', 'language', 'layout', 'preferences']
};

// Root reducer
const rootReducer = combineReducers({
  auth: persistReducer(authPersistConfig, authReducer),
  products: productsReducer,
  cart: cartReducer,
  favorites: favoritesReducer,
  ui: persistReducer(uiPersistConfig, uiReducer),
  inventory: inventoryReducer,
  orders: ordersReducer,
  customers: customersReducer,
  reports: reportsReducer
});

// Persisted reducer
const persistedReducer = persistReducer(persistConfig, rootReducer);

// Configure store
export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
        ignoredPaths: ['register', 'rehydrate']
      },
      immutableCheck: {
        warnAfter: 128
      }
    }).concat([
      // Add custom middleware here if needed
    ]),
  devTools: process.env.NODE_ENV !== 'production',
  preloadedState: undefined
});

// Create persistor
export const persistor = persistStore(store);

// Export types for TypeScript (if using TypeScript)
// These type exports only work in .ts/.tsx files
// export type RootState = ReturnType<typeof store.getState>;
// export type AppDispatch = typeof store.dispatch;

// Action creators for common operations
export const clearPersistedState = () => {
  persistor.purge();
};

export const resetStore = () => {
  store.dispatch({ type: 'RESET_STORE' });
};

// Selectors
export const selectAuth = (state) => state.auth;
export const selectProducts = (state) => state.products;
export const selectCart = (state) => state.cart;
export const selectFavorites = (state) => state.favorites;
export const selectUI = (state) => state.ui;
export const selectInventory = (state) => state.inventory;
export const selectOrders = (state) => state.orders;
export const selectCustomers = (state) => state.customers;
export const selectReports = (state) => state.reports;

// Enhanced selectors with memoization
export const selectCartTotal = (state) => {
  const cart = selectCart(state);
  return cart.items.reduce((total, item) => total + (item.price * item.quantity), 0);
};

export const selectCartItemCount = (state) => {
  const cart = selectCart(state);
  return cart.items.reduce((count, item) => count + item.quantity, 0);
};

export const selectIsProductInCart = (productId) => (state) => {
  const cart = selectCart(state);
  return cart.items.some(item => item.id === productId);
};

export const selectIsProductFavorite = (productId) => (state) => {
  const favorites = selectFavorites(state);
  return favorites.items.includes(productId);
};

export const selectUserPermissions = (state) => {
  const auth = selectAuth(state);
  return auth.user?.permissions || [];
};

export const selectHasPermission = (permission) => (state) => {
  const permissions = selectUserPermissions(state);
  return permissions.includes(permission);
};

export const selectFilteredProducts = (filters) => (state) => {
  const products = selectProducts(state);
  let filtered = [...products.items];

  if (filters.search) {
    const searchTerm = filters.search.toLowerCase();
    filtered = filtered.filter(product =>
      product.name.toLowerCase().includes(searchTerm) ||
      product.name_ar?.toLowerCase().includes(searchTerm) ||
      product.description?.toLowerCase().includes(searchTerm) ||
      product.sku?.toLowerCase().includes(searchTerm)
    );
  }

  if (filters.category) {
    filtered = filtered.filter(product => product.category_id === filters.category);
  }

  if (filters.brand) {
    filtered = filtered.filter(product => product.brand_id === filters.brand);
  }

  if (filters.priceRange) {
    const [min, max] = filters.priceRange;
    filtered = filtered.filter(product => product.price >= min && product.price <= max);
  }

  if (filters.inStock !== undefined) {
    filtered = filtered.filter(product =>
      filters.inStock ? product.stock_quantity > 0 : product.stock_quantity <= 0
    );
  }

  // Apply sorting
  if (filters.sortBy) {
    filtered.sort((a, b) => {
      let aValue = a[filters.sortBy];
      let bValue = b[filters.sortBy];

      if (typeof aValue === 'string') {
        aValue = aValue.toLowerCase();
        bValue = bValue.toLowerCase();
      }

      if (filters.sortOrder === 'desc') {
        return aValue < bValue ? 1 : aValue > bValue ? -1 : 0;
      } else {
        return aValue > bValue ? 1 : aValue < bValue ? -1 : 0;
      }
    });
  }

  return filtered;
};

// Store enhancement for development
if (process.env.NODE_ENV === 'development') {
  // Add store to window for debugging
  window.__STORE__ = store;
  
  // Log state changes
  store.subscribe(() => {
    console.log('State updated:', store.getState());
  });
}

export default store;

