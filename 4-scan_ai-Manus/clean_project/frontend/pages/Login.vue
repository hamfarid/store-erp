<!-- صفحة تسجيل الدخول -->
<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <!-- شعار النظام -->
        <div class="login-header text-center mb-4">
          <img src="/assets/logo.png" alt="Gaara Scan AI" class="login-logo mb-3">
          <h2 class="login-title">Gaara Scan AI</h2>
          <p class="login-subtitle">نظام التشخيص الذكي للنباتات</p>
        </div>

        <!-- نموذج تسجيل الدخول -->
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="mb-3">
            <label for="email" class="form-label">البريد الإلكتروني</label>
            <div class="input-group">
              <span class="input-group-text">
                <i class="fas fa-envelope"></i>
              </span>
              <input 
                type="email" 
                class="form-control" 
                id="email"
                v-model="loginForm.email"
                :class="{ 'is-invalid': errors.email }"
                placeholder="أدخل بريدك الإلكتروني"
                required
              >
              <div class="invalid-feedback" v-if="errors.email">
                {{ errors.email }}
              </div>
            </div>
          </div>

          <div class="mb-3">
            <label for="password" class="form-label">كلمة المرور</label>
            <div class="input-group">
              <span class="input-group-text">
                <i class="fas fa-lock"></i>
              </span>
              <input 
                :type="showPassword ? 'text' : 'password'" 
                class="form-control" 
                id="password"
                v-model="loginForm.password"
                :class="{ 'is-invalid': errors.password }"
                placeholder="أدخل كلمة المرور"
                required
              >
              <button 
                type="button" 
                class="btn btn-outline-secondary"
                @click="togglePassword"
              >
                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
              <div class="invalid-feedback" v-if="errors.password">
                {{ errors.password }}
              </div>
            </div>
          </div>

          <div class="mb-3 form-check">
            <input 
              type="checkbox" 
              class="form-check-input" 
              id="remember"
              v-model="loginForm.remember"
            >
            <label class="form-check-label" for="remember">
              تذكرني
            </label>
          </div>

          <!-- رسالة الخطأ العامة -->
          <div class="alert alert-danger" v-if="generalError">
            <i class="fas fa-exclamation-triangle me-2"></i>
            {{ generalError }}
          </div>

          <!-- زر تسجيل الدخول -->
          <button 
            type="submit" 
            class="btn btn-primary w-100 mb-3"
            :disabled="loading"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            <i v-else class="fas fa-sign-in-alt me-2"></i>
            {{ loading ? 'جاري تسجيل الدخول...' : 'تسجيل الدخول' }}
          </button>

          <!-- روابط إضافية -->
          <div class="text-center">
            <a href="#" class="text-decoration-none" @click="showForgotPassword">
              نسيت كلمة المرور؟
            </a>
          </div>
        </form>

        <!-- معلومات النظام -->
        <div class="login-footer text-center mt-4">
          <small class="text-muted">
            نظام Gaara Scan AI - الإصدار 2.0<br>
            جميع الحقوق محفوظة © 2024
          </small>
        </div>
      </div>
    </div>

    <!-- نافذة استعادة كلمة المرور -->
    <div class="modal fade" id="forgotPasswordModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">استعادة كلمة المرور</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="handleForgotPassword">
              <div class="mb-3">
                <label for="resetEmail" class="form-label">البريد الإلكتروني</label>
                <input 
                  type="email" 
                  class="form-control" 
                  id="resetEmail"
                  v-model="resetForm.email"
                  placeholder="أدخل بريدك الإلكتروني"
                  required
                >
              </div>
              <button type="submit" class="btn btn-primary w-100" :disabled="resetLoading">
                <span v-if="resetLoading" class="spinner-border spinner-border-sm me-2"></span>
                {{ resetLoading ? 'جاري الإرسال...' : 'إرسال رابط الاستعادة' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore, useSystemStore } from '../store/index.js'

export default {
  name: 'Login',
  
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const systemStore = useSystemStore()
    
    // البيانات التفاعلية
    const loading = ref(false)
    const resetLoading = ref(false)
    const showPassword = ref(false)
    const generalError = ref('')
    
    const loginForm = reactive({
      email: '',
      password: '',
      remember: false
    })
    
    const resetForm = reactive({
      email: ''
    })
    
    const errors = reactive({
      email: '',
      password: ''
    })
    
    // الوظائف
    const validateForm = () => {
      errors.email = ''
      errors.password = ''
      
      if (!loginForm.email) {
        errors.email = 'البريد الإلكتروني مطلوب'
        return false
      }
      
      if (!loginForm.email.includes('@')) {
        errors.email = 'البريد الإلكتروني غير صحيح'
        return false
      }
      
      if (!loginForm.password) {
        errors.password = 'كلمة المرور مطلوبة'
        return false
      }
      
      if (loginForm.password.length < 6) {
        errors.password = 'كلمة المرور يجب أن تكون 6 أحرف على الأقل'
        return false
      }
      
      return true
    }
    
    const handleLogin = async () => {
      generalError.value = ''
      
      if (!validateForm()) {
        return
      }
      
      loading.value = true
      
      try {
        await authStore.login({
          email: loginForm.email,
          password: loginForm.password,
          remember: loginForm.remember
        })
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم تسجيل الدخول بنجاح',
          message: `مرحباً بك ${authStore.userName}`
        })
        
        // التوجه للصفحة الرئيسية
        router.push('/')
        
      } catch (error) {
        generalError.value = error.response?.data?.message || 'خطأ في تسجيل الدخول'
      } finally {
        loading.value = false
      }
    }
    
    const togglePassword = () => {
      showPassword.value = !showPassword.value
    }
    
    const showForgotPassword = () => {
      const modal = new bootstrap.Modal(document.getElementById('forgotPasswordModal'))
      modal.show()
    }
    
    const handleForgotPassword = async () => {
      if (!resetForm.email) {
        return
      }
      
      resetLoading.value = true
      
      try {
        // استدعاء API استعادة كلمة المرور
        await authAPI.forgotPassword(resetForm.email)
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم الإرسال',
          message: 'تم إرسال رابط استعادة كلمة المرور إلى بريدك الإلكتروني'
        })
        
        // إغلاق النافذة
        const modal = bootstrap.Modal.getInstance(document.getElementById('forgotPasswordModal'))
        modal.hide()
        
        resetForm.email = ''
        
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ',
          message: 'حدث خطأ في إرسال رابط الاستعادة'
        })
      } finally {
        resetLoading.value = false
      }
    }
    
    return {
      loginForm,
      resetForm,
      errors,
      loading,
      resetLoading,
      showPassword,
      generalError,
      handleLogin,
      togglePassword,
      showForgotPassword,
      handleForgotPassword
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: var(--magseeds-gradient-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 400px;
}

.login-card {
  background: white;
  border-radius: 15px;
  padding: 40px 30px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}

.login-logo {
  width: 80px;
  height: 80px;
}

.login-title {
  color: var(--magseeds-primary);
  font-weight: var(--font-weight-bold);
  margin-bottom: 5px;
}

.login-subtitle {
  color: var(--magseeds-secondary);
  font-size: 0.9rem;
  margin-bottom: 0;
}

.login-form .form-label {
  font-weight: var(--font-weight-medium);
  color: var(--magseeds-dark);
  margin-bottom: 8px;
}

.login-form .form-control {
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 12px 15px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.login-form .form-control:focus {
  border-color: var(--magseeds-primary);
  box-shadow: 0 0 0 0.2rem rgba(78, 115, 223, 0.25);
}

.input-group-text {
  background: #f8f9fa;
  border: 2px solid #e9ecef;
  border-right: none;
  color: var(--magseeds-secondary);
}

.btn-primary {
  background: var(--magseeds-gradient-primary);
  border: none;
  border-radius: 8px;
  padding: 12px 20px;
  font-weight: var(--font-weight-medium);
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(78, 115, 223, 0.4);
}

.btn-primary:disabled {
  transform: none;
  box-shadow: none;
}

.form-check-label {
  font-size: 0.9rem;
  color: var(--magseeds-secondary);
}

.login-footer {
  border-top: 1px solid #e9ecef;
  padding-top: 20px;
  margin-top: 20px;
}

.alert {
  border-radius: 8px;
  border: none;
  font-size: 0.9rem;
}

.modal-content {
  border-radius: 15px;
  border: none;
}

.modal-header {
  border-bottom: 1px solid #e9ecef;
  padding: 20px 30px;
}

.modal-body {
  padding: 30px;
}

@media (max-width: 576px) {
  .login-card {
    padding: 30px 20px;
  }
  
  .login-container {
    max-width: 100%;
  }
}
</style>

