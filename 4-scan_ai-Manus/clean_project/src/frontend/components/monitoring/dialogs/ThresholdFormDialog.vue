// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/monitoring/dialogs/ThresholdFormDialog.vue

<template>
  <div class="dialog-overlay" @click.self="$emit('close')">
    <div class="dialog-container" dir="rtl">
      <div class="dialog-header">
        <h2 class="text-center">{{ isEdit ? $t('resource_monitoring.edit_threshold') : $t('resource_monitoring.add_threshold') }}</h2>
        <button class="btn-close" @click="$emit('close')" aria-label="إغلاق">
          <i class="fas fa-times"></i>
        </button>
      </div>
      
      <div class="dialog-body">
        <form @submit.prevent="handleSubmit" class="threshold-form">
          <div class="form-group">
            <label for="metricId" class="text-center">{{ $t('resource_monitoring.metric') }} <span class="required">*</span></label>
            <select 
              id="metricId" 
              v-model="form.metricId" 
              required
              :class="{ 'is-invalid': errors.metricId }"
            >
              <option value="">{{ $t('common.select_option') }}</option>
              <option v-for="metric in metrics" :key="metric.id" :value="metric.id">
                {{ metric.displayName || metric.metricName }}
              </option>
            </select>
            <div v-if="errors.metricId" class="error-message text-center">{{ errors.metricId }}</div>
          </div>
          
          <div class="form-group">
            <label for="warningThreshold" class="text-center">{{ $t('resource_monitoring.warning_threshold') }} <span class="required">*</span></label>
            <div class="threshold-input-group">
              <input 
                type="number" 
                id="warningThreshold" 
                v-model.number="form.warningThreshold" 
                required
                min="0"
                max="100"
                step="1"
                :class="{ 'is-invalid': errors.warningThreshold }"
              />
              <span class="threshold-unit">{{ selectedMetricUnit }}</span>
            </div>
            <div v-if="errors.warningThreshold" class="error-message text-center">{{ errors.warningThreshold }}</div>
            <div class="form-hint text-center">{{ $t('resource_monitoring.warning_threshold_hint') }}</div>
          </div>
          
          <div class="form-group">
            <label for="criticalThreshold" class="text-center">{{ $t('resource_monitoring.critical_threshold') }} <span class="required">*</span></label>
            <div class="threshold-input-group">
              <input 
                type="number" 
                id="criticalThreshold" 
                v-model.number="form.criticalThreshold" 
                required
                min="0"
                max="100"
                step="1"
                :class="{ 'is-invalid': errors.criticalThreshold }"
              />
              <span class="threshold-unit">{{ selectedMetricUnit }}</span>
            </div>
            <div v-if="errors.criticalThreshold" class="error-message text-center">{{ errors.criticalThreshold }}</div>
            <div class="form-hint text-center">{{ $t('resource_monitoring.critical_threshold_hint') }}</div>
          </div>
          
          <div class="form-group form-checkbox">
            <label class="checkbox-label">
              <input type="checkbox" v-model="form.enabled" />
              <span>{{ $t('resource_monitoring.enable_threshold') }}</span>
            </label>
          </div>
        </form>
      </div>
      
      <div class="dialog-footer">
        <button class="btn btn-secondary" @click="$emit('close')">
          {{ $t('common.cancel') }}
        </button>
        <button class="btn btn-primary" @click="handleSubmit" :disabled="!isFormValid">
          {{ isEdit ? $t('common.save') : $t('common.add') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { useI18n } from 'vue-i18n';

export default defineComponent({
  name: 'ThresholdFormDialog',
  
  props: {
    threshold: {
      type: Object,
      default: () => ({
        metricId: '',
        warningThreshold: 70,
        criticalThreshold: 90,
        enabled: true
      })
    },
    metrics: {
      type: Array,
      default: () => []
    },
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  
  emits: ['close', 'save'],
  
  setup(props, { emit }) {
    const { t } = useI18n();
    
    // Form data
    const form = reactive({
      id: props.threshold.id || null,
      metricId: props.threshold.metricId || '',
      warningThreshold: props.threshold.warningThreshold || 70,
      criticalThreshold: props.threshold.criticalThreshold || 90,
      enabled: props.threshold.enabled !== undefined ? props.threshold.enabled : true
    });
    
    // Form validation
    const errors = reactive({
      metricId: '',
      warningThreshold: '',
      criticalThreshold: ''
    });
    
    // Get selected metric unit
    const selectedMetricUnit = computed(() => {
      if (!form.metricId) return '';
      
      const selectedMetric = props.metrics.find(metric => metric.id === form.metricId);
      return selectedMetric ? selectedMetric.unit : '';
    });
    
    // Watch for changes in thresholds to validate
    watch(() => form.warningThreshold, validateThresholds);
    watch(() => form.criticalThreshold, validateThresholds);
    
    function validateThresholds() {
      // Validate warning threshold
      if (form.warningThreshold === null || form.warningThreshold === undefined) {
        errors.warningThreshold = t('validation.field_required');
      } else if (form.warningThreshold < 0 || form.warningThreshold > 100) {
        errors.warningThreshold = t('validation.value_between', { min: 0, max: 100 });
      } else {
        errors.warningThreshold = '';
      }
      
      // Validate critical threshold
      if (form.criticalThreshold === null || form.criticalThreshold === undefined) {
        errors.criticalThreshold = t('validation.field_required');
      } else if (form.criticalThreshold < 0 || form.criticalThreshold > 100) {
        errors.criticalThreshold = t('validation.value_between', { min: 0, max: 100 });
      } else if (form.criticalThreshold <= form.warningThreshold) {
        errors.criticalThreshold = t('resource_monitoring.critical_must_be_greater');
      } else {
        errors.criticalThreshold = '';
      }
    }
    
    const validateForm = () => {
      let isValid = true;
      
      // Validate metric ID
      if (!form.metricId) {
        errors.metricId = t('validation.field_required');
        isValid = false;
      } else {
        errors.metricId = '';
      }
      
      // Validate thresholds
      validateThresholds();
      if (errors.warningThreshold || errors.criticalThreshold) {
        isValid = false;
      }
      
      return isValid;
    };
    
    const isFormValid = computed(() => {
      return form.metricId && 
             form.warningThreshold !== null && 
             form.criticalThreshold !== null && 
             form.criticalThreshold > form.warningThreshold &&
             !errors.metricId && 
             !errors.warningThreshold && 
             !errors.criticalThreshold;
    });
    
    const handleSubmit = () => {
      if (validateForm()) {
        emit('save', { ...form });
      }
    };
    
    // Initialize form when component is mounted
    onMounted(() => {
      // If editing, populate form with threshold data
      if (props.isEdit && props.threshold) {
        Object.keys(form).forEach(key => {
          if (props.threshold[key] !== undefined) {
            form[key] = props.threshold[key];
          }
        });
      }
      
      validateThresholds();
    });
    
    return {
      form,
      errors,
      selectedMetricUnit,
      isFormValid,
      handleSubmit
    };
  }
});
</script>

<style scoped>
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  font-family: 'Cairo', 'Roboto', sans-serif;
}

.dialog-header {
  padding: 16px 20px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dialog-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
  width: 100%;
}

.text-center {
  text-align: center;
}

.btn-close {
  background: none;
  border: none;
  font-size: 18px;
  color: #757575;
  cursor: pointer;
  padding: 5px;
}

.btn-close:hover {
  color: #333;
}

.dialog-body {
  padding: 20px;
  overflow-y: auto;
}

.dialog-footer {
  padding: 16px 20px;
  border-top: 1px solid #e0e0e0;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.threshold-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 6px;
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.required {
  color: #D32F2F;
}

input, select, textarea {
  padding: 10px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s;
  text-align: center;
}

input:focus, select:focus, textarea:focus {
  border-color: #1976D2;
  outline: none;
}

.is-invalid {
  border-color: #D32F2F;
}

.error-message {
  color: #D32F2F;
  font-size: 12px;
  margin-top: 4px;
}

.form-hint {
  color: #757575;
  font-size: 12px;
  margin-top: 4px;
}

.threshold-input-group {
  display: flex;
  align-items: center;
}

.threshold-input-group input {
  flex: 1;
  text-align: center;
}

.threshold-unit {
  margin-right: 10px;
  color: #757575;
  font-size: 14px;
}

.form-checkbox {
  margin-top: 10px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.checkbox-label input {
  margin-left: 10px;
}

.checkbox-label span {
  font-size: 14px;
  color: #333;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  border: none;
  font-weight: 500;
  min-width: 100px;
  text-align: center;
}

.btn-primary {
  background-color: #1976D2;
  color: white;
}

.btn-primary:hover {
  background-color: #1565C0;
}

.btn-primary:disabled {
  background-color: #BDBDBD;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #333;
}

.btn-secondary:hover {
  background-color: #e0e0e0;
}
</style>
