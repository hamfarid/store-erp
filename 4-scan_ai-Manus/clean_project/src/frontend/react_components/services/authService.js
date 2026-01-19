/**
 * /home/ubuntu/implemented_files/v3/src/frontend/react-components/services/authService.js
 * 
 * خدمة المصادقة لنظام Gaara ERP
 * توفر هذه الخدمة وظائف المصادقة وإدارة الجلسات والتحقق من الصلاحيات
 */

import axios from 'axios';
import jwtDecode from 'jwt-decode';

// تكوين الإعدادات الأساسية
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
const AUTH_ENDPOINTS = {
  LOGIN: `${API_URL}/auth/login`,
  LOGOUT: `${API_URL}/auth/logout`,
  REFRESH: `${API_URL}/auth/refresh`,
  REGISTER: `${API_URL}/auth/register`,
  VERIFY_EMAIL: `${API_URL}/auth/email/verify`,
  PASSWORD_RESET_REQUEST: `${API_URL}/auth/password-reset/request`,
  PASSWORD_RESET_CONFIRM: `${API_URL}/auth/password-reset/confirm`,
  MFA_VERIFY: `${API_URL}/auth/mfa/verify`,
  MFA_CONFIG: `${API_URL}/auth/mfa/config`,
  MFA_METHODS: `${API_URL}/auth/mfa/methods`,
  USER_PROFILE: `${API_URL}/users/profile`,
};

// مفاتيح التخزين المحلي
const TOKEN_KEY = 'gaara_auth_token';
const REFRESH_TOKEN_KEY = 'gaara_refresh_token';
const USER_KEY = 'gaara_user';

/**
 * خدمة المصادقة
 */
const authService = {
  /**
   * تسجيل الدخول
   * @param {string} username - اسم المستخدم
   * @param {string} password - كلمة المرور
   * @returns {Promise<Object>} - بيانات المستخدم والرموز
   */
  async login(username, password) {
    try {
      const response = await axios.post(AUTH_ENDPOINTS.LOGIN, { username, password });
      const { access_token, refresh_token, user, requires_mfa } = response.data;

      if (requires_mfa) {
        return { requires_mfa: true, user_id: user.id };
      }

      this.setTokens(access_token, refresh_token);
      this.setUser(user);
      this.setupTokenRefresh();

      return { user, access_token };
    } catch (error) {
      console.error('Login error:', error);
      throw this.handleError(error);
    }
  },

  /**
   * التحقق من المصادقة متعددة العوامل
   * @param {string} userId - معرف المستخدم
   * @param {string} code - رمز التحقق
   * @param {string} method - طريقة التحقق
   * @returns {Promise<Object>} - بيانات المستخدم والرموز
   */
  async verifyMfa(userId, code, method = 'totp') {
    try {
      const response = await axios.post(AUTH_ENDPOINTS.MFA_VERIFY, {
        user_id: userId,
        code,
        method
      });

      const { access_token, refresh_token, user } = response.data;

      this.setTokens(access_token, refresh_token);
      this.setUser(user);
      this.setupTokenRefresh();

      return { user, access_token };
    } catch (error) {
      console.error('MFA verification error:', error);
      throw this.handleError(error);
    }
  },

  /**
   * تسجيل الخروج
   * @returns {Promise<void>}
   */
  async logout() {
    try {
      const token = this.getToken();
      if (token) {
        await axios.post(AUTH_ENDPOINTS.LOGOUT, {}, {
          headers: this.getAuthHeader()
        });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      this.clearAuth();
    }
  },

  /**
   * تسجيل مستخدم جديد
   * @param {Object} userData - بيانات المستخدم
   * @returns {Promise<Object>} - بيانات المستخدم المسجل
   */
  async register(userData) {
    try {
      const response = await axios.post(AUTH_ENDPOINTS.REGISTER, userData);
      return response.data;
    } catch (error) {
      console.error('Registration error:', error);
      throw this.handleError(error);
    }
  },

  /**
   * طلب إعادة تعيين كلمة المرور
   * @param {string} email - البريد الإلكتروني
   * @returns {Promise<Object>} - رسالة التأكيد
   */
  async requestPasswordReset(email) {
    try {
      const response = await axios.post(AUTH_ENDPOINTS.PASSWORD_RESET_REQUEST, { email });
      return response.data;
    } catch (error) {
      console.error('Password reset request error:', error);
      throw this.handleError(error);
    }
  },

  /**
   * تأكيد إعادة تعيين كلمة المرور
   * @param {string} token - رمز إعادة التعيين
   * @param {string} password - كلمة المرور الجديدة
   * @returns {Promise<Object>} - رسالة التأكيد
   */
  async confirmPasswordReset(token, password) {
    try {
      const response = await axios.post(AUTH_ENDPOINTS.PASSWORD_RESET_CONFIRM, {
        token,
        password
      });
      return response.data;
    } catch (error) {
      console.error('Password reset confirmation error:', error);
      throw this.handleError(error);
    }
  },

  /**
   * التحقق من البريد الإلكتروني
   * @param {string} token - رمز التحقق
   * @returns {Promise<Object>} - رسالة التأكيد
   */
  async verifyEmail(token) {
    try {
      const response = await axios.post(AUTH_ENDPOINTS.VERIFY_EMAIL, { token });
      return response.data;
    } catch (error) {
      console.error('Email verification error:', error);
      throw this.handleError(error);
    }
  },

  /**
   * الحصول على الملف الشخصي للمستخدم
   * @returns {Promise<Object>} - بيانات الملف الشخصي
   */
  async getUserProfile() {
    try {
      const response = await axios.get(AUTH_ENDPOINTS.USER_PROFILE, {
        headers: this.getAuthHeader()
      });
      return response.data;
    } catch (error) {
      console.error('Get user profile error:', error);
      throw this.handleError(error);
    }
  },

  /**
   * تحديث الملف الشخصي للمستخدم
   * @param {Object} profileData - بيانات الملف الشخصي
   * @returns {Promise<Object>} - بيانات الملف الشخصي المحدثة
   */
  async updateUserProfile(profileData) {
    try {
      const response = await axios.put(AUTH_ENDPOINTS.USER_PROFILE, profileData, {
        headers: this.getAuthHeader()
      });
      
      // تحديث بيانات المستخدم المخزنة محلياً
      const currentUser = this.getUser();
      const updatedUser = { ...currentUser, ...response.data };
      this.setUser(updatedUser);
      
      return response.data;
    } catch (error) {
      console.error('Update user profile error:', error);
      throw this.handleError(error);
    }
  },

  /**
   * تجديد رمز الوصول
   * @returns {Promise<string>} - رمز الوصول الجديد
   */
  async refreshToken() {
    try {
      const refreshToken = this.getRefreshToken();
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const response = await axios.post(AUTH_ENDPOINTS.REFRESH, {
        refresh_token: refreshToken
      });

      const { access_token, refresh_token } = response.data;
      this.setTokens(access_token, refresh_token);

      return access_token;
    } catch (error) {
      console.error('Token refresh error:', error);
      this.clearAuth();
      throw error;
    }
  },

  /**
   * إعداد تجديد الرمز التلقائي
   */
  setupTokenRefresh() {
    const token = this.getToken();
    if (!token) return;

    try {
      const decoded = jwtDecode(token);
      const expiryTime = decoded.exp * 1000; // تحويل إلى ميلي ثانية
      const currentTime = Date.now();
      const timeUntilExpiry = expiryTime - currentTime;
      
      // تجديد الرمز قبل انتهاء صلاحيته بدقيقة واحدة
      const refreshTime = timeUntilExpiry - 60000;
      
      if (refreshTime > 0) {
        setTimeout(() => {
          this.refreshToken()
            .then(() => this.setupTokenRefresh())
            .catch(error => console.error('Auto refresh error:', error));
        }, refreshTime);
      } else {
        // إذا كان الرمز منتهي الصلاحية بالفعل، قم بتجديده فوراً
        this.refreshToken()
          .then(() => this.setupTokenRefresh())
          .catch(error => console.error('Immediate refresh error:', error));
      }
    } catch (error) {
      console.error('Token decode error:', error);
      this.clearAuth();
    }
  },

  /**
   * التحقق من حالة المصادقة
   * @returns {boolean} - حالة المصادقة
   */
  isAuthenticated() {
    const token = this.getToken();
    if (!token) return false;

    try {
      const decoded = jwtDecode(token);
      const currentTime = Date.now() / 1000;
      return decoded.exp > currentTime;
    } catch (error) {
      return false;
    }
  },

  /**
   * الحصول على المستخدم الحالي
   * @returns {Object|null} - بيانات المستخدم
   */
  getUser() {
    const userStr = localStorage.getItem(USER_KEY);
    return userStr ? JSON.parse(userStr) : null;
  },

  /**
   * الحصول على رمز الوصول
   * @returns {string|null} - رمز الوصول
   */
  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  },

  /**
   * الحصول على رمز التجديد
   * @returns {string|null} - رمز التجديد
   */
  getRefreshToken() {
    return localStorage.getItem(REFRESH_TOKEN_KEY);
  },

  /**
   * الحصول على رأس المصادقة
   * @returns {Object} - رأس المصادقة
   */
  getAuthHeader() {
    const token = this.getToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
  },

  /**
   * تخزين الرموز
   * @param {string} accessToken - رمز الوصول
   * @param {string} refreshToken - رمز التجديد
   */
  setTokens(accessToken, refreshToken) {
    localStorage.setItem(TOKEN_KEY, accessToken);
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  },

  /**
   * تخزين بيانات المستخدم
   * @param {Object} user - بيانات المستخدم
   */
  setUser(user) {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  },

  /**
   * مسح بيانات المصادقة
   */
  clearAuth() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  },

  /**
   * معالجة أخطاء المصادقة
   * @param {Error} error - الخطأ
   * @returns {Error} - الخطأ المعالج
   */
  handleError(error) {
    if (error.response) {
      const { status, data } = error.response;
      
      // إذا كان الخطأ 401 (غير مصرح) وليس في صفحة تسجيل الدخول
      if (status === 401 && !window.location.pathname.includes('/login')) {
        this.clearAuth();
        window.location.href = '/login';
      }
      
      return new Error(data.message || 'Authentication error');
    }
    
    return error;
  }
};

export default authService;
