import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { useAuth } from './AuthContext';

// إنشاء Context
const AppContext = createContext();

// الحالة الأولية
const initialState = {
  // إعدادات التطبيق
  settings: {
    theme: 'light',
    language: 'ar',
    currency: 'EGP',
    dateFormat: 'DD/MM/YYYY',
    notifications: true,
    autoSave: true
  },
  
  // بيانات لوحة التحكم
  dashboard: {
    stats: null,
    loading: false,
    error: null,
    lastUpdated: null
  },
  
  // بيانات المنتجات
  products: {
    list: [],
    loading: false,
    error: null,
    filters: {
      search: '',
      category: '',
      warehouse: '',
      status: 'all'
    },
    pagination: {
      page: 1,
      perPage: 20,
      total: 0
    }
  },
  
  // بيانات العملاء
  customers: {
    list: [],
    loading: false,
    error: null,
    filters: {
      search: '',
      type: '',
      status: 'all'
    }
  },
  
  // بيانات الموردين
  suppliers: {
    list: [],
    loading: false,
    error: null,
    filters: {
      search: '',
      type: '',
      status: 'all'
    }
  },
  
  // بيانات الفواتير
  invoices: {
    list: [],
    loading: false,
    error: null,
    filters: {
      type: 'all',
      status: 'all',
      dateFrom: '',
      dateTo: ''
    }
  },
  
  // الإشعارات
  notifications: [],
  
  // حالة التحميل العامة
  loading: false,
  
  // الأخطاء العامة
  errors: []
};

// أنواع الإجراءات
const actionTypes = {
  // إعدادات التطبيق
  SET_THEME: 'SET_THEME',
  SET_LANGUAGE: 'SET_LANGUAGE',
  SET_CURRENCY: 'SET_CURRENCY',
  UPDATE_SETTINGS: 'UPDATE_SETTINGS',
  
  // لوحة التحكم
  SET_DASHBOARD_LOADING: 'SET_DASHBOARD_LOADING',
  SET_DASHBOARD_STATS: 'SET_DASHBOARD_STATS',
  SET_DASHBOARD_ERROR: 'SET_DASHBOARD_ERROR',
  
  // المنتجات
  SET_PRODUCTS_LOADING: 'SET_PRODUCTS_LOADING',
  SET_PRODUCTS_LIST: 'SET_PRODUCTS_LIST',
  SET_PRODUCTS_ERROR: 'SET_PRODUCTS_ERROR',
  SET_PRODUCTS_FILTERS: 'SET_PRODUCTS_FILTERS',
  SET_PRODUCTS_PAGINATION: 'SET_PRODUCTS_PAGINATION',
  ADD_PRODUCT: 'ADD_PRODUCT',
  UPDATE_PRODUCT: 'UPDATE_PRODUCT',
  DELETE_PRODUCT: 'DELETE_PRODUCT',
  
  // العملاء
  SET_CUSTOMERS_LOADING: 'SET_CUSTOMERS_LOADING',
  SET_CUSTOMERS_LIST: 'SET_CUSTOMERS_LIST',
  SET_CUSTOMERS_ERROR: 'SET_CUSTOMERS_ERROR',
  SET_CUSTOMERS_FILTERS: 'SET_CUSTOMERS_FILTERS',
  ADD_CUSTOMER: 'ADD_CUSTOMER',
  UPDATE_CUSTOMER: 'UPDATE_CUSTOMER',
  DELETE_CUSTOMER: 'DELETE_CUSTOMER',
  
  // الموردين
  SET_SUPPLIERS_LOADING: 'SET_SUPPLIERS_LOADING',
  SET_SUPPLIERS_LIST: 'SET_SUPPLIERS_LIST',
  SET_SUPPLIERS_ERROR: 'SET_SUPPLIERS_ERROR',
  SET_SUPPLIERS_FILTERS: 'SET_SUPPLIERS_FILTERS',
  ADD_SUPPLIER: 'ADD_SUPPLIER',
  UPDATE_SUPPLIER: 'UPDATE_SUPPLIER',
  DELETE_SUPPLIER: 'DELETE_SUPPLIER',
  
  // الفواتير
  SET_INVOICES_LOADING: 'SET_INVOICES_LOADING',
  SET_INVOICES_LIST: 'SET_INVOICES_LIST',
  SET_INVOICES_ERROR: 'SET_INVOICES_ERROR',
  SET_INVOICES_FILTERS: 'SET_INVOICES_FILTERS',
  ADD_INVOICE: 'ADD_INVOICE',
  UPDATE_INVOICE: 'UPDATE_INVOICE',
  DELETE_INVOICE: 'DELETE_INVOICE',
  
  // الإشعارات
  ADD_NOTIFICATION: 'ADD_NOTIFICATION',
  REMOVE_NOTIFICATION: 'REMOVE_NOTIFICATION',
  CLEAR_NOTIFICATIONS: 'CLEAR_NOTIFICATIONS',
  
  // عام
  SET_LOADING: 'SET_LOADING',
  ADD_ERROR: 'ADD_ERROR',
  REMOVE_ERROR: 'REMOVE_ERROR',
  CLEAR_ERRORS: 'CLEAR_ERRORS'
};

// Reducer للحالة
const appReducer = (state, action) => {
  switch (action.type) {
    // إعدادات التطبيق
    case actionTypes.SET_THEME:
      return {
        ...state,
        settings: { ...state.settings, theme: action.payload }
      };
    
    case actionTypes.SET_LANGUAGE:
      return {
        ...state,
        settings: { ...state.settings, language: action.payload }
      };
    
    case actionTypes.UPDATE_SETTINGS:
      return {
        ...state,
        settings: { ...state.settings, ...action.payload }
      };
    
    // لوحة التحكم
    case actionTypes.SET_DASHBOARD_LOADING:
      return {
        ...state,
        dashboard: { ...state.dashboard, loading: action.payload }
      };
    
    case actionTypes.SET_DASHBOARD_STATS:
      return {
        ...state,
        dashboard: {
          ...state.dashboard,
          stats: action.payload,
          loading: false,
          error: null,
          lastUpdated: new Date()
        }
      };
    
    case actionTypes.SET_DASHBOARD_ERROR:
      return {
        ...state,
        dashboard: {
          ...state.dashboard,
          error: action.payload,
          loading: false
        }
      };
    
    // المنتجات
    case actionTypes.SET_PRODUCTS_LOADING:
      return {
        ...state,
        products: { ...state.products, loading: action.payload }
      };
    
    case actionTypes.SET_PRODUCTS_LIST:
      return {
        ...state,
        products: {
          ...state.products,
          list: action.payload,
          loading: false,
          error: null
        }
      };
    
    case actionTypes.SET_PRODUCTS_FILTERS:
      return {
        ...state,
        products: {
          ...state.products,
          filters: { ...state.products.filters, ...action.payload }
        }
      };
    
    case actionTypes.ADD_PRODUCT:
      return {
        ...state,
        products: {
          ...state.products,
          list: [...state.products.list, action.payload]
        }
      };
    
    case actionTypes.UPDATE_PRODUCT:
      return {
        ...state,
        products: {
          ...state.products,
          list: state.products.list.map(product =>
            product.id === action.payload.id ? action.payload : product
          )
        }
      };
    
    case actionTypes.DELETE_PRODUCT:
      return {
        ...state,
        products: {
          ...state.products,
          list: state.products.list.filter(product => product.id !== action.payload)
        }
      };
    
    // الإشعارات
    case actionTypes.ADD_NOTIFICATION:
      return {
        ...state,
        notifications: [...state.notifications, {
          id: Date.now(),
          ...action.payload,
          timestamp: new Date()
        }]
      };
    
    case actionTypes.REMOVE_NOTIFICATION:
      return {
        ...state,
        notifications: state.notifications.filter(
          notification => notification.id !== action.payload
        )
      };
    
    case actionTypes.CLEAR_NOTIFICATIONS:
      return {
        ...state,
        notifications: []
      };
    
    // عام
    case actionTypes.SET_LOADING:
      return {
        ...state,
        loading: action.payload
      };
    
    case actionTypes.ADD_ERROR:
      return {
        ...state,
        errors: [...state.errors, {
          id: Date.now(),
          ...action.payload,
          timestamp: new Date()
        }]
      };
    
    case actionTypes.CLEAR_ERRORS:
      return {
        ...state,
        errors: []
      };
    
    default:
      return state;
  }
};

// مزود السياق
export const AppProvider = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);
  const { user: _user } = useAuth();

  // تحميل الإعدادات من localStorage عند بدء التطبيق
  useEffect(() => {
    const savedSettings = localStorage.getItem('appSettings');
    if (savedSettings) {
      try {
        const settings = JSON.parse(savedSettings);
        dispatch({
          type: actionTypes.UPDATE_SETTINGS,
          payload: settings
        });
      } catch (error) {
        }
    }
  }, []);

  // حفظ الإعدادات في localStorage عند تغييرها
  useEffect(() => {
    localStorage.setItem('appSettings', JSON.stringify(state.settings));
  }, [state.settings]);

  // دوال مساعدة
  const actions = {
    // إعدادات التطبيق
    setTheme: (theme) => dispatch({ type: actionTypes.SET_THEME, payload: theme }),
    setLanguage: (language) => dispatch({ type: actionTypes.SET_LANGUAGE, payload: language }),
    updateSettings: (settings) => dispatch({ type: actionTypes.UPDATE_SETTINGS, payload: settings }),
    
    // لوحة التحكم
    setDashboardLoading: (loading) => dispatch({ type: actionTypes.SET_DASHBOARD_LOADING, payload: loading }),
    setDashboardStats: (stats) => dispatch({ type: actionTypes.SET_DASHBOARD_STATS, payload: stats }),
    setDashboardError: (error) => dispatch({ type: actionTypes.SET_DASHBOARD_ERROR, payload: error }),
    
    // المنتجات
    setProductsLoading: (loading) => dispatch({ type: actionTypes.SET_PRODUCTS_LOADING, payload: loading }),
    setProductsList: (products) => dispatch({ type: actionTypes.SET_PRODUCTS_LIST, payload: products }),
    setProductsFilters: (filters) => dispatch({ type: actionTypes.SET_PRODUCTS_FILTERS, payload: filters }),
    addProduct: (product) => dispatch({ type: actionTypes.ADD_PRODUCT, payload: product }),
    updateProduct: (product) => dispatch({ type: actionTypes.UPDATE_PRODUCT, payload: product }),
    deleteProduct: (productId) => dispatch({ type: actionTypes.DELETE_PRODUCT, payload: productId }),
    
    // الإشعارات
    addNotification: (notification) => dispatch({ type: actionTypes.ADD_NOTIFICATION, payload: notification }),
    removeNotification: (id) => dispatch({ type: actionTypes.REMOVE_NOTIFICATION, payload: id }),
    clearNotifications: () => dispatch({ type: actionTypes.CLEAR_NOTIFICATIONS }),
    
    // عام
    setLoading: (loading) => dispatch({ type: actionTypes.SET_LOADING, payload: loading }),
    addError: (error) => dispatch({ type: actionTypes.ADD_ERROR, payload: error }),
    clearErrors: () => dispatch({ type: actionTypes.CLEAR_ERRORS })
  };

  const value = {
    state,
    dispatch,
    actions,
    actionTypes
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

// Hook لاستخدام السياق
export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};

export default AppContext;
