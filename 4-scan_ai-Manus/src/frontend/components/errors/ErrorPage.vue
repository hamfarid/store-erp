<!-- 
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/errors/ErrorPage.vue
الوصف: مكون صفحة الخطأ العامة للأخطاء 404/500/504
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
-->

<template>
  <div class="error-page" :class="errorClass">
    <div class="error-container">
      <div class="error-icon">
        <i :class="errorIcon"></i>
      </div>
      <div class="error-code">{{ errorCode }}</div>
      <h1 class="error-title">{{ errorTitle }}</h1>
      <p class="error-message">{{ errorMessage }}</p>
      <div class="error-actions">
        <button class="btn btn-primary" @click="goHome">
          <i class="fas fa-home"></i> {{ $t('errors.goHome') }}
        </button>
        <button class="btn btn-secondary" @click="goBack" v-if="canGoBack">
          <i class="fas fa-arrow-left"></i> {{ $t('errors.goBack') }}
        </button>
        <button class="btn btn-outline" @click="reportError">
          <i class="fas fa-bug"></i> {{ $t('errors.reportProblem') }}
        </button>
      </div>
      <div class="error-details" v-if="showDetails">
        <div class="error-details-header" @click="toggleDetails">
          <i class="fas fa-chevron-down" v-if="!detailsExpanded"></i>
          <i class="fas fa-chevron-up" v-else></i>
          {{ $t('errors.technicalDetails') }}
        </div>
        <div class="error-details-content" v-if="detailsExpanded">
          <pre>{{ errorDetails }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from '@/composables/useToast';
import activityLogService from '@/services/activityLogService';
import { computed, onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute, useRouter } from 'vue-router';

export default {
  name: 'ErrorPage',
  props: {
    errorCode: {
      type: [Number, String],
      required: true
    },
    errorMessage: {
      type: String,
      default: ''
    },
    errorDetails: {
      type: String,
      default: ''
    },
    showDetails: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const { t } = useI18n();
    const router = useRouter();
    const route = useRoute();
    const { showToast } = useToast();
    
    const detailsExpanded = ref(false);
    const canGoBack = ref(window.history.length > 1);
    
    // تحديد عنوان الخطأ حسب رمز الخطأ
    const errorTitle = computed(() => {
      switch (parseInt(props.errorCode)) {
        case 404:
          return t('errors.notFound');
        case 500:
          return t('errors.serverError');
        case 504:
          return t('errors.gatewayTimeout');
        default:
          return t('errors.genericError');
      }
    });
    
    // تحديد أيقونة الخطأ حسب رمز الخطأ
    const errorIcon = computed(() => {
      switch (parseInt(props.errorCode)) {
        case 404:
          return 'fas fa-search';
        case 500:
          return 'fas fa-exclamation-triangle';
        case 504:
          return 'fas fa-clock';
        default:
          return 'fas fa-exclamation-circle';
      }
    });
    
    // تحديد فئة CSS حسب رمز الخطأ
    const errorClass = computed(() => {
      switch (parseInt(props.errorCode)) {
        case 404:
          return 'error-not-found';
        case 500:
          return 'error-server';
        case 504:
          return 'error-timeout';
        default:
          return 'error-generic';
      }
    });
    
    // العودة إلى الصفحة الرئيسية
    const goHome = () => {
      router.push({ name: 'home' });
    };
    
    // العودة إلى الصفحة السابقة
    const goBack = () => {
      router.back();
    };
    
    // تبديل عرض التفاصيل التقنية
    const toggleDetails = () => {
      detailsExpanded.value = !detailsExpanded.value;
    };
    
    // الإبلاغ عن المشكلة
    const reportError = () => {
      // إظهار رسالة تأكيد
      showToast(t('errors.problemReported'), 'success');
      
      // تسجيل الإبلاغ عن المشكلة في سجل النشاط
      activityLogService.logUserAction({
        action: 'report_error',
        target_type: 'error',
        target_id: props.errorCode.toString(),
        details: {
          error_code: props.errorCode,
          error_message: props.errorMessage,
          error_details: props.errorDetails,
          url: window.location.href,
          user_agent: navigator.userAgent,
          timestamp: new Date().toISOString()
        }
      }).catch(error => {
        console.error('Failed to log error report:', error);
      });
    };
    
    // تسجيل الخطأ في سجل النشاط عند تحميل الصفحة
    onMounted(() => {
      activityLogService.logSystemEvent({
        event_type: 'error_page_viewed',
        details: {
          error_code: props.errorCode,
          error_message: props.errorMessage,
          url: window.location.href,
          referrer: document.referrer,
          user_agent: navigator.userAgent,
          timestamp: new Date().toISOString(),
          route: {
            path: route.path,
            query: route.query,
            params: route.params
          }
        }
      }).catch(error => {
        console.error('Failed to log error page view:', error);
      });
    });
    
    return {
      errorTitle,
      errorIcon,
      errorClass,
      detailsExpanded,
      canGoBack,
      goHome,
      goBack,
      toggleDetails,
      reportError
    };
  }
};
</script>

<style scoped>
.error-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
  background-color: #f8f9fa;
  text-align: center;
}

.error-container {
  max-width: 600px;
  padding: 3rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.error-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.error-code {
  font-size: 5rem;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 1rem;
}

.error-title {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.error-message {
  font-size: 1.1rem;
  margin-bottom: 2rem;
  color: #6c757d;
}

.error-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  border: none;
}

.btn-primary:hover {
  background-color: #0069d9;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  border: none;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.btn-outline {
  background-color: transparent;
  color: #007bff;
  border: 1px solid #007bff;
}

.btn-outline:hover {
  background-color: #f0f7ff;
}

.error-details {
  margin-top: 2rem;
  text-align: left;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  overflow: hidden;
}

.error-details-header {
  padding: 0.75rem 1rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.error-details-content {
  padding: 1rem;
  background-color: #f8f9fa;
  overflow-x: auto;
}

.error-details-content pre {
  margin: 0;
  white-space: pre-wrap;
  font-size: 0.875rem;
}

/* تخصيص الألوان حسب نوع الخطأ */
.error-not-found .error-icon {
  color: #17a2b8;
}

.error-not-found .error-code {
  color: #17a2b8;
}

.error-server .error-icon {
  color: #dc3545;
}

.error-server .error-code {
  color: #dc3545;
}

.error-timeout .error-icon {
  color: #ffc107;
}

.error-timeout .error-code {
  color: #ffc107;
}

.error-generic .error-icon {
  color: #6c757d;
}

.error-generic .error-code {
  color: #6c757d;
}

/* تعديلات للغة العربية */
:global([dir="rtl"]) .error-details {
  text-align: right;
}

:global([dir="rtl"]) .error-details-header {
  flex-direction: row-reverse;
}

/* تعديلات للشاشات الصغيرة */
@media (max-width: 576px) {
  .error-container {
    padding: 2rem;
  }
  
  .error-code {
    font-size: 4rem;
  }
  
  .error-title {
    font-size: 1.5rem;
  }
  
  .error-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}
</style>
