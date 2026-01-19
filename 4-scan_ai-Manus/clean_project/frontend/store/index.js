/**
 * Pinia Store - إدارة الحالة الرئيسية
 * Main State Management
 */

import { defineStore } from 'pinia'
import axios from 'axios'

// متجر المصادقة
export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('auth_token'),
    isAuthenticated: false,
    loading: false,
    error: null
  }),

  getters: {
    isAdmin: (state) => state.user?.role === 'admin',
    userName: (state) => state.user?.name || 'مستخدم',
    userEmail: (state) => state.user?.email || ''
  },

  actions: {
    async login(credentials) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post('/api/auth/login', credentials)
        
        this.token = response.data.token
        this.user = response.data.user
        this.isAuthenticated = true
        
        localStorage.setItem('auth_token', this.token)
        localStorage.setItem('user_role', this.user.role)
        
        // تعيين token في axios headers
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'خطأ في تسجيل الدخول'
        throw error
      } finally {
        this.loading = false
      }
    },

    async logout() {
      try {
        await axios.post('/api/auth/logout')
      } catch (error) {
        console.error('خطأ في تسجيل الخروج:', error)
      }
      
      this.user = null
      this.token = null
      this.isAuthenticated = false
      
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user_role')
      
      delete axios.defaults.headers.common['Authorization']
    },

    async fetchUser() {
      if (!this.token) return
      
      try {
        const response = await axios.get('/api/auth/user')
        this.user = response.data
        this.isAuthenticated = true
      } catch (error) {
        this.logout()
      }
    },

    initializeAuth() {
      if (this.token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        this.fetchUser()
      }
    }
  }
})

// متجر النظام العام
export const useSystemStore = defineStore('system', {
  state: () => ({
    loading: false,
    notifications: [],
    sidebarOpen: true,
    theme: localStorage.getItem('theme') || 'light',
    language: localStorage.getItem('language') || 'ar'
  }),

  actions: {
    setLoading(status) {
      this.loading = status
    },

    addNotification(notification) {
      const id = Date.now()
      this.notifications.push({
        id,
        type: 'info',
        duration: 5000,
        ...notification
      })

      // إزالة الإشعار تلقائياً
      setTimeout(() => {
        this.removeNotification(id)
      }, notification.duration || 5000)
    },

    removeNotification(id) {
      const index = this.notifications.findIndex(n => n.id === id)
      if (index > -1) {
        this.notifications.splice(index, 1)
      }
    },

    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen
    },

    setTheme(theme) {
      this.theme = theme
      localStorage.setItem('theme', theme)
      document.documentElement.setAttribute('data-theme', theme)
    },

    setLanguage(language) {
      this.language = language
      localStorage.setItem('language', language)
      document.documentElement.setAttribute('lang', language)
      document.documentElement.setAttribute('dir', language === 'ar' ? 'rtl' : 'ltr')
    }
  }
})

// متجر البيانات
export const useDataStore = defineStore('data', {
  state: () => ({
    dashboardStats: {},
    recentActivities: [],
    systemHealth: {},
    loading: false,
    error: null
  }),

  actions: {
    async fetchDashboardData() {
      this.loading = true
      this.error = null
      
      try {
        const [statsResponse, activitiesResponse, healthResponse] = await Promise.all([
          axios.get('/api/dashboard/stats'),
          axios.get('/api/activity-log/recent'),
          axios.get('/api/system/health')
        ])
        
        this.dashboardStats = statsResponse.data
        this.recentActivities = activitiesResponse.data
        this.systemHealth = healthResponse.data
      } catch (error) {
        this.error = error.response?.data?.message || 'خطأ في تحميل البيانات'
        console.error('خطأ في تحميل بيانات لوحة التحكم:', error)
      } finally {
        this.loading = false
      }
    },

    async refreshData() {
      await this.fetchDashboardData()
    }
  }
})

// متجر الذكاء الاصطناعي
export const useAIStore = defineStore('ai', {
  state: () => ({
    models: [],
    activeModel: null,
    chatHistory: [],
    processing: false,
    error: null
  }),

  actions: {
    async fetchModels() {
      try {
        const response = await axios.get('/api/ai-management/models')
        this.models = response.data
      } catch (error) {
        this.error = 'خطأ في تحميل النماذج'
        console.error('خطأ في تحميل النماذج:', error)
      }
    },

    async sendMessage(message) {
      this.processing = true
      this.error = null
      
      try {
        const response = await axios.post('/api/ai-agent/chat', {
          message,
          model: this.activeModel?.id
        })
        
        this.chatHistory.push({
          type: 'user',
          message,
          timestamp: new Date()
        })
        
        this.chatHistory.push({
          type: 'ai',
          message: response.data.response,
          timestamp: new Date()
        })
        
        return response.data
      } catch (error) {
        this.error = 'خطأ في إرسال الرسالة'
        throw error
      } finally {
        this.processing = false
      }
    },

    clearChat() {
      this.chatHistory = []
    },

    setActiveModel(model) {
      this.activeModel = model
    }
  }
})

// متجر التشخيص
export const useDiagnosisStore = defineStore('diagnosis', {
  state: () => ({
    currentImage: null,
    diagnosisResult: null,
    processing: false,
    history: [],
    error: null
  }),

  actions: {
    async uploadImage(file) {
      this.processing = true
      this.error = null
      
      try {
        const formData = new FormData()
        formData.append('image', file)
        
        const response = await axios.post('/api/diagnosis/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        this.currentImage = response.data.image_url
        return response.data
      } catch (error) {
        this.error = 'خطأ في رفع الصورة'
        throw error
      } finally {
        this.processing = false
      }
    },

    async diagnoseImage(imageId) {
      this.processing = true
      this.error = null
      
      try {
        const response = await axios.post('/api/diagnosis/analyze', {
          image_id: imageId
        })
        
        this.diagnosisResult = response.data
        this.history.unshift({
          id: Date.now(),
          image: this.currentImage,
          result: response.data,
          timestamp: new Date()
        })
        
        return response.data
      } catch (error) {
        this.error = 'خطأ في تحليل الصورة'
        throw error
      } finally {
        this.processing = false
      }
    },

    clearCurrentDiagnosis() {
      this.currentImage = null
      this.diagnosisResult = null
    }
  }
})

