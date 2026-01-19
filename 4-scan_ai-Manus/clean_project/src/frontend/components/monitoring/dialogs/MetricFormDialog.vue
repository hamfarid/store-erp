// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/monitoring/dialogs/MetricFormDialog.vue

<template>
  <div class="dialog-overlay" @click.self="$emit('close')">
    <div class="dialog-container" dir="rtl">
      <div class="dialog-header">
        <h2>{{ isEdit ? $t('resource_monitoring.edit_metric') : $t('resource_monitoring.add_metric') }}</h2>
        <button class="btn-close" @click="$emit('close')" aria-label="إغلاق">
          <i class="fas fa-times"></i>
        </button>
      </div>
      
      <div class="dialog-body">
        <form @submit.prevent="handleSubmit" class="metric-form">
          <div class="form-group">
            <label for="resourceType">{{ $t('resource_monitoring.resource_type') }} <span class="required">*</span></label>
            <select 
              id="resourceType" 
              v-model="form.resourceType" 
              required
              :class="{ 'is-invalid': errors.resourceType }"
            >
              <option value="">{{ $t('common.select_option') }}</option>
              <option value="system">{{ $t('resource_monitoring.system') }}</option>
              <option value="application">{{ $t('resource_monitoring.application') }}</option>
              <option value="database">{{ $t('resource_monitoring.database') }}</option>
              <option value="network">{{ $t('resource_monitoring.network') }}</option>
              <option value="ai">{{ $t('resource_monitoring.ai') }}</option>
              <option value="custom">{{ $t('resource_monitoring.custom') }}</option>
            </select>
            <div v-if="errors.resourceType" class="error-message">{{ errors.resourceType }}</div>
          </div>
          
          <div class="form-group">
            <label for="metricName">{{ $t('resource_monitoring.metric_name') }} <span class="required">*</span></label>
            <input 
              type="text" 
              id="metricName" 
              v-model="form.metricName" 
              required
              :class="{ 'is-invalid': errors.metricName }"
              @input="validateMetricName"
            />
            <div v-if="errors.metricName" class="error-message">{{ errors.metricName }}</div>
            <div class="form-hint">{{ $t('resource_monitoring.metric_name_hint') }}</div>
          </div>
          
          <div class="form-group">
            <label for="displayName">{{ $t('resource_monitoring.display_name') }}</label>
            <input 
              type="text" 
              id="displayName" 
              v-model="form.displayName"
              :class="{ 'is-invalid': errors.displayName }"
            />
            <div v-if="errors.displayName" class="error-message">{{ errors.displayName }}</div>
          </div>
          
          <div class="form-group">
            <label for="unit">{{ $t('resource_monitoring.unit') }}</label>
            <input 
              type="text" 
              id="unit" 
              v-model="form.unit"
              :class="{ 'is-invalid': errors.unit }"
            />
            <div v-if="errors.unit" class="error-message">{{ errors.unit }}</div>
            <div class="form-hint">{{ $t('resource_monitoring.unit_hint') }}</div>
          </div>
          
          <div class="form-group">
            <label for="description">{{ $t('resource_monitoring.description') }}</label>
            <textarea 
              id="description" 
              v-model="form.description"
              rows="3"
              :class="{ 'is-invalid': errors.description }"
            ></textarea>
            <div v-if="errors.description" class="error-message">{{ errors.description }}</div>
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
import { computed, onMounted, reactive } from 'vue';
import { useI18n } from 'vue-i18n';

export default {
  name: 'MetricFormDialog',
  
  props: {
    metric: {
      type: Object,
      default: () => ({
        resourceType: '',
        metricName: '',
        displayName: '',
        unit: '',
        description: ''
      })
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
      id: props.metric.id || null,
      resourceType: props.metric.resourceType || '',
      metricName: props.metric.metricName || '',
      displayName: props.metric.displayName || '',
      unit: props.metric.unit || '',
      description: props.metric.description || ''
    });
    
    // Form validation
    const errors = reactive({
      resourceType: '',
      metricName: '',
      displayName: '',
      unit: '',
      description: ''
    });
    
    const validateMetricName = () => {
      if (!form.metricName) {
        errors.metricName = t('validation.field_required');
        return false;
      }
      
      // Check if metric name contains only alphanumeric characters, underscores, and dots
      const metricNameRegex = /^[a-z0-9_\.]+$/;
      if (!metricNameRegex.test(form.metricName)) {
        errors.metricName = t('resource_monitoring.metric_name_invalid');
        return false;
      }
      
      errors.metricName = '';
      return true;
    };
    
    const validateForm = () => {
      let isValid = true;
      
      // Validate resource type
      if (!form.resourceType) {
        errors.resourceType = t('validation.field_required');
        isValid = false;
      } else {
        errors.resourceType = '';
      }
      
      // Validate metric name
      if (!validateMetricName()) {
        isValid = false;
      }
      
      // Validate display name (optional but with max length)
      if (form.displayName && form.displayName.length > 100) {
        errors.displayName = t('validation.max_length', { max: 100 });
        isValid = false;
      } else {
        errors.displayName = '';
      }
      
      // Validate unit (optional)
      if (form.unit && form.unit.length > 20) {
        errors.unit = t('validation.max_length', { max: 20 });
        isValid = false;
      } else {
        errors.unit = '';
      }
      
      // Validate description (optional but with max length)
      if (form.description && form.description.length > 500) {
        errors.description = t('validation.max_length', { max: 500 });
        isValid = false;
      } else {
        errors.description = '';
      }
      
      return isValid;
    };
    
    const isFormValid = computed(() => {
      return form.resourceType && form.metricName && !errors.resourceType && !errors.metricName && 
             !errors.displayName && !errors.unit && !errors.description;
    });
    
    const handleSubmit = () => {
      if (validateForm()) {
        emit('save', { ...form });
      }
    };
    
    // Initialize form when component is mounted
    onMounted(() => {
      // If editing, populate form with metric data
      if (props.isEdit && props.metric) {
        Object.keys(form).forEach(key => {
          if (props.metric[key] !== undefined) {
            form[key] = props.metric[key];
          }
        });
      }
    });
    
    return {
      form,
      errors,
      isFormValid,
      validateMetricName,
      handleSubmit
    };
  }
};
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
  justify-content: flex-end;
  gap: 10px;
}

.metric-form {
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
  color: #F44336;
}

input, select, textarea {
  padding: 10px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s;
}

input:focus, select:focus, textarea:focus {
  border-color: #2196F3;
  outline: none;
}

.is-invalid {
  border-color: #F44336;
}

.error-message {
  color: #F44336;
  font-size: 12px;
  margin-top: 4px;
}

.form-hint {
  color: #757575;
  font-size: 12px;
  margin-top: 4px;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  border: none;
  font-weight: 500;
}

.btn-primary {
  background-color: #2196F3;
  color: white;
}

.btn-primary:hover {
  background-color: #1976D2;
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
