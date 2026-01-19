<!--
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/setup/SetupWizardContainer.vue
الوصف: مكون حاوية معالج الإعداد
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
-->

<template>
  <div class="setup-wizard-container" :class="{ 'rtl': isRtl }">
    <!-- شعار النظام -->
    <div class="logo-container">
      <img v-if="logo" :src="logo" alt="Scan AI Logo" class="logo" />
      <h1 v-else class="system-name">{{ systemName }}</h1>
    </div>

    <!-- شريط التقدم -->
    <div class="progress-container">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
      </div>
      <div class="progress-text">{{ currentStepIndex + 1 }} / {{ totalSteps }}</div>
    </div>

    <!-- حاوية الخطوات -->
    <div class="steps-container">
      <!-- قائمة الخطوات الجانبية -->
      <div class="steps-sidebar">
        <ul class="steps-list">
          <li 
            v-for="(step, index) in steps" 
            :key="step.id"
            :class="{
              'active': currentStepIndex === index,
              'completed': isStepCompleted(step.id),
              'clickable': canNavigateToStep(index)
            }"
            @click="canNavigateToStep(index) && navigateToStep(index)"
          >
            <div class="step-indicator">
              <span v-if="isStepCompleted(step.id)" class="step-check">✓</span>
              <span v-else class="step-number">{{ index + 1 }}</span>
            </div>
            <div class="step-info">
              <div class="step-title">{{ step.title }}</div>
              <div class="step-description">{{ step.description }}</div>
            </div>
          </li>
        </ul>
      </div>

      <!-- محتوى الخطوة الحالية -->
      <div class="step-content">
        <transition name="fade" mode="out-in">
          <component 
            :is="currentStepComponent" 
            :key="currentStep.id"
            :step-data="currentStepData"
            @update:step-data="updateStepData"
            @validate="validateCurrentStep"
          ></component>
        </transition>
      </div>
    </div>

    <!-- أزرار التنقل -->
    <div class="navigation-buttons">
      <button 
        v-if="!isFirstStep" 
        class="btn btn-secondary" 
        @click="previousStep"
      >
        {{ $t('setup.buttons.previous') }}
      </button>
      <button 
        v-if="!isLastStep" 
        class="btn btn-primary" 
        @click="nextStep"
        :disabled="!canProceedToNextStep"
      >
        {{ $t('setup.buttons.next') }}
      </button>
      <button 
        v-else 
        class="btn btn-success" 
        @click="completeSetup"
        :disabled="!canCompleteSetup"
      >
        {{ $t('setup.buttons.complete') }}
      </button>
    </div>

    <!-- شريط الحالة -->
    <div class="status-bar">
      <div v-if="statusMessage" class="status-message" :class="statusType">
        <i :class="statusIcon"></i>
        {{ statusMessage }}
      </div>
      <div class="language-selector">
        <select v-model="selectedLanguage" @change="changeLanguage">
          <option v-for="lang in availableLanguages" :key="lang.code" :value="lang.code">
            {{ lang.name_native }}
          </option>
        </select>
      </div>
    </div>

    <!-- مؤشر التحميل -->
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <div class="loading-text">{{ loadingMessage }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { computed, onMounted, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';

// استيراد مكونات الخطوات
import AISettingsStep from './steps/AISettingsStep.vue';
import BackupImportExportStep from './steps/BackupImportExportStep.vue';
import BranchSettingsStep from './steps/BranchSettingsStep.vue';
import CompanySettingsStep from './steps/CompanySettingsStep.vue';
import DatabaseSettingsStep from './steps/DatabaseSettingsStep.vue';
import ModuleSelectionStep from './steps/ModuleSelectionStep.vue';
import NotificationSettingsStep from './steps/NotificationSettingsStep.vue';
import SecuritySettingsStep from './steps/SecuritySettingsStep.vue';
import SummaryStep from './steps/SummaryStep.vue';
import SystemSettingsStep from './steps/SystemSettingsStep.vue';
import UserSettingsStep from './steps/UserSettingsStep.vue';
import WelcomeStep from './steps/WelcomeStep.vue';

export default {
  name: 'SetupWizardContainer',
  components: {
    WelcomeStep,
    SystemSettingsStep,
    DatabaseSettingsStep,
    CompanySettingsStep,
    BranchSettingsStep,
    UserSettingsStep,
    ModuleSelectionStep,
    AISettingsStep,
    NotificationSettingsStep,
    SecuritySettingsStep,
    BackupImportExportStep,
    SummaryStep
  },
  setup() {
    const { t, locale } = useI18n();
    const router = useRouter();

    // حالة المعالج
    const loading = ref(false);
    const loadingMessage = ref('');
    const statusMessage = ref('');
    const statusType = ref('info');
    const setupToken = ref('');
    const selectedLanguage = ref('ar');
    const logo = ref(null);
    const systemName = ref('Scan AI');

    // بيانات الخطوات
    const steps = [
      { 
        id: 'welcome', 
        title: t('setup.steps.welcome.title'), 
        description: t('setup.steps.welcome.description'),
        component: 'WelcomeStep'
      },
      { 
        id: 'system_settings', 
        title: t('setup.steps.system_settings.title'), 
        description: t('setup.steps.system_settings.description'),
        component: 'SystemSettingsStep'
      },
      { 
        id: 'database_settings', 
        title: t('setup.steps.database_settings.title'), 
        description: t('setup.steps.database_settings.description'),
        component: 'DatabaseSettingsStep'
      },
      { 
        id: 'company_settings', 
        title: t('setup.steps.company_settings.title'), 
        description: t('setup.steps.company_settings.description'),
        component: 'CompanySettingsStep'
      },
      { 
        id: 'branch_settings', 
        title: t('setup.steps.branch_settings.title'), 
        description: t('setup.steps.branch_settings.description'),
        component: 'BranchSettingsStep'
      },
      { 
        id: 'user_settings', 
        title: t('setup.steps.user_settings.title'), 
        description: t('setup.steps.user_settings.description'),
        component: 'UserSettingsStep'
      },
      { 
        id: 'module_selection', 
        title: t('setup.steps.module_selection.title'), 
        description: t('setup.steps.module_selection.description'),
        component: 'ModuleSelectionStep'
      },
      { 
        id: 'ai_settings', 
        title: t('setup.steps.ai_settings.title'), 
        description: t('setup.steps.ai_settings.description'),
        component: 'AISettingsStep'
      },
      { 
        id: 'notification_settings', 
        title: t('setup.steps.notification_settings.title'), 
        description: t('setup.steps.notification_settings.description'),
        component: 'NotificationSettingsStep'
      },
      { 
        id: 'security_settings', 
        title: t('setup.steps.security_settings.title'), 
        description: t('setup.steps.security_settings.description'),
        component: 'SecuritySettingsStep'
      },
      { 
        id: 'backup_import_export', 
        title: t('setup.steps.backup_import_export.title'), 
        description: t('setup.steps.backup_import_export.description'),
        component: 'BackupImportExportStep'
      },
      { 
        id: 'summary', 
        title: t('setup.steps.summary.title'), 
        description: t('setup.steps.summary.description'),
        component: 'SummaryStep'
      }
    ];

    const currentStepIndex = ref(0);
    const completedSteps = ref([]);
    const stepsData = ref({});
    const stepsValidation = ref({});
    const availableLanguages = ref([
      { code: 'ar', name: 'العربية', name_native: 'العربية', rtl: true },
      { code: 'en', name: 'English', name_native: 'English', rtl: false }
    ]);

    // الخصائص المحسوبة
    const currentStep = computed(() => steps[currentStepIndex.value]);
    
    const currentStepComponent = computed(() => {
      return currentStep.value ? currentStep.value.component : null;
    });

    const currentStepData = computed(() => {
      return stepsData.value[currentStep.value.id] || {};
    });

    const isFirstStep = computed(() => currentStepIndex.value === 0);
    
    const isLastStep = computed(() => currentStepIndex.value === steps.length - 1);
    
    const totalSteps = computed(() => steps.length);
    
    const progressPercentage = computed(() => {
      return (currentStepIndex.value / (totalSteps.value - 1)) * 100;
    });

    const canProceedToNextStep = computed(() => {
      return stepsValidation.value[currentStep.value.id] === true;
    });

    const canCompleteSetup = computed(() => {
      // التحقق من اكتمال جميع الخطوات الإلزامية
      const requiredSteps = ['system_settings', 'database_settings', 'company_settings', 'user_settings', 'security_settings'];
      return requiredSteps.every(step => completedSteps.value.includes(step));
    });

    const statusIcon = computed(() => {
      switch (statusType.value) {
        case 'success': return 'fas fa-check-circle';
        case 'error': return 'fas fa-exclamation-circle';
        case 'warning': return 'fas fa-exclamation-triangle';
        default: return 'fas fa-info-circle';
      }
    });

    const isRtl = computed(() => {
      return selectedLanguage.value === 'ar';
    });

    // الوظائف
    const initializeSetup = async () => {
      try {
        loading.value = true;
        loadingMessage.value = t('setup.messages.initializing');
        
        const response = await axios.post('/api/setup/initialize');
        
        if (response.data.success) {
          setupToken.value = response.data.setup_token;
          
          // تحديث حالة الخطوات
          if (response.data.current_step) {
            const stepIndex = steps.findIndex(step => step.id === response.data.current_step);
            if (stepIndex !== -1) {
              currentStepIndex.value = stepIndex;
            }
          }
          
          if (response.data.completed_steps) {
            completedSteps.value = response.data.completed_steps;
          }
          
          // تحميل بيانات الخطوة الحالية
          await loadStepData(currentStep.value.id);
          
          showStatus(t('setup.messages.initialized'), 'success');
        } else {
          showStatus(t('setup.messages.initialization_failed'), 'error');
        }
      } catch (error) {
        console.error('Error initializing setup:', error);
        showStatus(t('setup.messages.initialization_failed'), 'error');
      } finally {
        loading.value = false;
      }
    };

    const loadStepData = async (stepId) => {
      try {
        loading.value = true;
        loadingMessage.value = t('setup.messages.loading_step_data');
        
        const response = await axios.get(`/api/setup/steps/${stepId}`, {
          headers: { 'X-Setup-Token': setupToken.value }
        });
        
        if (response.data.success) {
          // تحديث بيانات الخطوة
          stepsData.value = {
            ...stepsData.value,
            [stepId]: response.data.data
          };
        } else {
          showStatus(t('setup.messages.loading_step_data_failed'), 'error');
        }
      } catch (error) {
        console.error(`Error loading step data for ${stepId}:`, error);
        showStatus(t('setup.messages.loading_step_data_failed'), 'error');
      } finally {
        loading.value = false;
      }
    };

    const updateStepData = (data) => {
      stepsData.value = {
        ...stepsData.value,
        [currentStep.value.id]: data
      };
    };

    const validateCurrentStep = async () => {
      try {
        loading.value = true;
        loadingMessage.value = t('setup.messages.validating');
        
        const response = await axios.post(`/api/setup/steps/${currentStep.value.id}/validate`, {
          data: currentStepData.value
        }, {
          headers: { 'X-Setup-Token': setupToken.value }
        });
        
        if (response.data.success) {
          stepsValidation.value = {
            ...stepsValidation.value,
            [currentStep.value.id]: true
          };
          
          showStatus(t('setup.messages.validation_success'), 'success');
          return true;
        } else {
          stepsValidation.value = {
            ...stepsValidation.value,
            [currentStep.value.id]: false
          };
          
          showStatus(t('setup.messages.validation_failed') + ': ' + response.data.errors.join(', '), 'error');
          return false;
        }
      } catch (error) {
        console.error(`Error validating step ${currentStep.value.id}:`, error);
        stepsValidation.value = {
          ...stepsValidation.value,
          [currentStep.value.id]: false
        };
        
        showStatus(t('setup.messages.validation_failed'), 'error');
        return false;
      } finally {
        loading.value = false;
      }
    };

    const saveCurrentStep = async () => {
      try {
        loading.value = true;
        loadingMessage.value = t('setup.messages.saving');
        
        const response = await axios.post(`/api/setup/steps/${currentStep.value.id}`, {
          data: currentStepData.value
        }, {
          headers: { 'X-Setup-Token': setupToken.value }
        });
        
        if (response.data.success) {
          // إضافة الخطوة إلى الخطوات المكتملة
          if (!completedSteps.value.includes(currentStep.value.id)) {
            completedSteps.value.push(currentStep.value.id);
          }
          
          showStatus(t('setup.messages.save_success'), 'success');
          return true;
        } else {
          showStatus(t('setup.messages.save_failed') + ': ' + response.data.message, 'error');
          return false;
        }
      } catch (error) {
        console.error(`Error saving step ${currentStep.value.id}:`, error);
        showStatus(t('setup.messages.save_failed'), 'error');
        return false;
      } finally {
        loading.value = false;
      }
    };

    const nextStep = async () => {
      // التحقق من صحة الخطوة الحالية
      const isValid = await validateCurrentStep();
      if (!isValid) return;
      
      // حفظ الخطوة الحالية
      const isSaved = await saveCurrentStep();
      if (!isSaved) return;
      
      // الانتقال إلى الخطوة التالية
      try {
        loading.value = true;
        loadingMessage.value = t('setup.messages.navigating');
        
        const response = await axios.post('/api/setup/next', {}, {
          headers: { 'X-Setup-Token': setupToken.value }
        });
        
        if (response.data.success) {
          currentStepIndex.value++;
          
          // تحميل بيانات الخطوة التالية
          await loadStepData(currentStep.value.id);
        } else {
          showStatus(t('setup.messages.navigation_failed'), 'error');
        }
      } catch (error) {
        console.error('Error navigating to next step:', error);
        showStatus(t('setup.messages.navigation_failed'), 'error');
      } finally {
        loading.value = false;
      }
    };

    const previousStep = async () => {
      try {
        loading.value = true;
        loadingMessage.value = t('setup.messages.navigating');
        
        const response = await axios.post('/api/setup/previous', {}, {
          headers: { 'X-Setup-Token': setupToken.value }
        });
        
        if (response.data.success) {
          currentStepIndex.value--;
          
          // تحميل بيانات الخطوة السابقة
          await loadStepData(currentStep.value.id);
        } else {
          showStatus(t('setup.messages.navigation_failed'), 'error');
        }
      } catch (error) {
        console.error('Error navigating to previous step:', error);
        showStatus(t('setup.messages.navigation_failed'), 'error');
      } finally {
        loading.value = false;
      }
    };

    const navigateToStep = async (index) => {
      if (index === currentStepIndex.value) return;
      
      try {
        loading.value = true;
        loadingMessage.value = t('setup.messages.navigating');
        
        // حفظ الخطوة الحالية إذا كانت صالحة
        if (stepsValidation.value[currentStep.value.id]) {
          await saveCurrentStep();
        }
        
        currentStepIndex.value = index;
        
        // تحميل بيانات الخطوة المستهدفة
        await loadStepData(currentStep.value.id);
      } catch (error) {
        console.error(`Error navigating to step ${index}:`, error);
        showStatus(t('setup.messages.navigation_failed'), 'error');
      } finally {
        loading.value = false;
      }
    };

    const completeSetup = async () => {
      // التحقق من صحة الخطوة الحالية
      const isValid = await validateCurrentStep();
      if (!isValid) return;
      
      // حفظ الخطوة الحالية
      const isSaved = await saveCurrentStep();
      if (!isSaved) return;
      
      // إكمال الإعداد
      try {
        loading.value = true;
        loadingMessage.value = t('setup.messages.completing');
        
        const response = await axios.post('/api/setup/complete', {}, {
          headers: { 'X-Setup-Token': setupToken.value }
        });
        
        if (response.data.success) {
          showStatus(t('setup.messages.completion_success'), 'success');
          
          // الانتظار لمدة ثانيتين ثم الانتقال إلى لوحة التحكم
          setTimeout(() => {
            router.push('/dashboard');
          }, 2000);
        } else {
          showStatus(t('setup.messages.completion_failed') + ': ' + response.data.message, 'error');
        }
      } catch (error) {
        console.error('Error completing setup:', error);
        showStatus(t('setup.messages.completion_failed'), 'error');
      } finally {
        loading.value = false;
      }
    };

    const isStepCompleted = (stepId) => {
      return completedSteps.value.includes(stepId);
    };

    const canNavigateToStep = (index) => {
      // يمكن الانتقال إلى الخطوة إذا كانت مكتملة أو هي الخطوة الحالية أو الخطوة التالية مباشرة
      const stepId = steps[index].id;
      return isStepCompleted(stepId) || index === currentStepIndex.value || index === currentStepIndex.value + 1;
    };

    const showStatus = (message, type = 'info') => {
      statusMessage.value = message;
      statusType.value = type;
      
      // إخفاء الرسالة بعد 5 ثوانٍ
      setTimeout(() => {
        statusMessage.value = '';
      }, 5000);
    };

    const changeLanguage = () => {
      locale.value = selectedLanguage.value;
      document.documentElement.dir = isRtl.value ? 'rtl' : 'ltr';
      document.documentElement.lang = selectedLanguage.value;
    };

    // دورة حياة المكون
    onMounted(async () => {
      // تعيين اتجاه النص واللغة
      document.documentElement.dir = isRtl.value ? 'rtl' : 'ltr';
      document.documentElement.lang = selectedLanguage.value;
      
      // تهيئة المعالج
      await initializeSetup();
    });

    // مراقبة تغييرات اللغة
    watch(selectedLanguage, () => {
      changeLanguage();
    });

    return {
      // الحالة
      loading,
      loadingMessage,
      statusMessage,
      statusType,
      statusIcon,
      selectedLanguage,
      availableLanguages,
      logo,
      systemName,
      isRtl,
      
      // بيانات الخطوات
      steps,
      currentStepIndex,
      currentStep,
      currentStepComponent,
      currentStepData,
      completedSteps,
      
      // الخصائص المحسوبة
      isFirstStep,
      isLastStep,
      totalSteps,
      progressPercentage,
      canProceedToNextStep,
      canCompleteSetup,
      
      // الوظائف
      updateStepData,
      validateCurrentStep,
      nextStep,
      previousStep,
      navigateToStep,
      completeSetup,
      isStepCompleted,
      canNavigateToStep,
      changeLanguage
    };
  }
};
</script>

<style scoped>
.setup-wizard-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f8f9fa;
  font-family: 'Tajawal', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
  padding: 20px;
}

.rtl {
  direction: rtl;
  text-align: right;
}

.logo-container {
  text-align: center;
  margin-bottom: 20px;
}

.logo {
  max-height: 80px;
  max-width: 200px;
}

.system-name {
  font-size: 28px;
  font-weight: bold;
  color: #007bff;
  margin: 0;
}

.progress-container {
  margin-bottom: 20px;
}

.progress-bar {
  height: 8px;
  background-color: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #007bff;
  transition: width 0.3s ease;
}

.progress-text {
  text-align: center;
  margin-top: 5px;
  font-size: 14px;
  color: #6c757d;
}

.steps-container {
  display: flex;
  flex: 1;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-bottom: 20px;
}

.steps-sidebar {
  width: 280px;
  background-color: #f8f9fa;
  border-right: 1px solid #e9ecef;
  overflow-y: auto;
}

.rtl .steps-sidebar {
  border-right: none;
  border-left: 1px solid #e9ecef;
}

.steps-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.steps-list li {
  display: flex;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #e9ecef;
  opacity: 0.6;
  transition: all 0.2s ease;
}

.steps-list li.active {
  background-color: #e9f5ff;
  opacity: 1;
  border-left: 4px solid #007bff;
}

.rtl .steps-list li.active {
  border-left: none;
  border-right: 4px solid #007bff;
}

.steps-list li.completed {
  opacity: 0.8;
}

.steps-list li.clickable {
  cursor: pointer;
}

.steps-list li.clickable:hover {
  background-color: #f1f8ff;
}

.step-indicator {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #6c757d;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  flex-shrink: 0;
}

.rtl .step-indicator {
  margin-right: 0;
  margin-left: 15px;
}

.steps-list li.active .step-indicator {
  background-color: #007bff;
}

.steps-list li.completed .step-indicator {
  background-color: #28a745;
}

.step-info {
  flex: 1;
}

.step-title {
  font-weight: bold;
  margin-bottom: 5px;
}

.step-description {
  font-size: 12px;
  color: #6c757d;
}

.step-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  padding: 15px 0;
}

.rtl .navigation-buttons {
  flex-direction: row-reverse;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s ease;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
}

.btn-primary:hover:not(:disabled) {
  background-color: #0069d9;
}

.btn-secondary {
  background-color: #6c757d;
  color: #fff;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #5a6268;
}

.btn-success {
  background-color: #28a745;
  color: #fff;
}

.btn-success:hover:not(:disabled) {
  background-color: #218838;
}

.status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  font-size: 14px;
}

.status-message {
  padding: 8px 15px;
  border-radius: 4px;
  display: flex;
  align-items: center;
}

.status-message i {
  margin-right: 8px;
}

.rtl .status-message i {
  margin-right: 0;
  margin-left: 8px;
}

.status-message.info {
  background-color: #cce5ff;
  color: #004085;
}

.status-message.success {
  background-color: #d4edda;
  color: #155724;
}

.status-message.warning {
  background-color: #fff3cd;
  color: #856404;
}

.status-message.error {
  background-color: #f8d7da;
  color: #721c24;
}

.language-selector select {
  padding: 5px 10px;
  border-radius: 4px;
  border: 1px solid #ced4da;
  background-color: #fff;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

.loading-text {
  font-size: 18px;
  color: #007bff;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* تعديلات للأجهزة المحمولة */
@media (max-width: 768px) {
  .steps-container {
    flex-direction: column;
  }
  
  .steps-sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #e9ecef;
    max-height: 200px;
  }
  
  .rtl .steps-sidebar {
    border-left: none;
  }
  
  .step-content {
    padding: 15px;
  }
  
  .btn {
    padding: 8px 15px;
  }
}
</style>
