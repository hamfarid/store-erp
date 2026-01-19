// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/ai_agent/AIModelSelector.vue

<template>
  <div class="ai-model-selector">
    <h2 class="selector-title text-center">{{ $t('ai_agent.select_model') }}</h2>
    
    <div class="models-container">
      <div 
        v-for="model in availableModels" 
        :key="model.id" 
        class="model-card"
        :class="{ 'selected': selectedModel && selectedModel.id === model.id }"
        @click="selectModel(model)"
      >
        <div class="model-icon">
          <i :class="model.icon"></i>
        </div>
        <div class="model-info">
          <h3 class="text-center">{{ model.name }}</h3>
          <div class="model-description text-center">{{ model.description }}</div>
          <div class="model-capabilities">
            <span 
              v-for="(capability, index) in model.capabilities" 
              :key="index" 
              class="capability-badge"
            >
              {{ capability }}
            </span>
          </div>
          <div class="model-metrics text-center">
            <div class="metric">
              <span class="metric-label">{{ $t('ai_agent.token_limit') }}:</span>
              <span class="metric-value">{{ model.tokenLimit.toLocaleString() }}</span>
            </div>
            <div class="metric">
              <span class="metric-label">{{ $t('ai_agent.cost') }}:</span>
              <span class="metric-value">{{ model.cost }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="selectedModel" class="model-parameters">
      <h3 class="text-center">{{ $t('ai_agent.model_parameters') }}</h3>
      
      <div class="parameter-form">
        <div class="form-group">
          <label for="temperature" class="text-center">{{ $t('ai_agent.temperature') }}</label>
          <div class="slider-container">
            <input 
              type="range" 
              id="temperature" 
              v-model.number="parameters.temperature" 
              min="0" 
              max="2" 
              step="0.1"
            />
            <span class="slider-value">{{ parameters.temperature.toFixed(1) }}</span>
          </div>
          <div class="parameter-description text-center">{{ $t('ai_agent.temperature_description') }}</div>
        </div>
        
        <div class="form-group">
          <label for="maxTokens" class="text-center">{{ $t('ai_agent.max_tokens') }}</label>
          <div class="slider-container">
            <input 
              type="range" 
              id="maxTokens" 
              v-model.number="parameters.maxTokens" 
              :min="100" 
              :max="selectedModel.tokenLimit" 
              step="100"
            />
            <span class="slider-value">{{ parameters.maxTokens.toLocaleString() }}</span>
          </div>
          <div class="parameter-description text-center">{{ $t('ai_agent.max_tokens_description') }}</div>
        </div>
        
        <div class="form-group">
          <label for="topP" class="text-center">{{ $t('ai_agent.top_p') }}</label>
          <div class="slider-container">
            <input 
              type="range" 
              id="topP" 
              v-model.number="parameters.topP" 
              min="0" 
              max="1" 
              step="0.05"
            />
            <span class="slider-value">{{ parameters.topP.toFixed(2) }}</span>
          </div>
          <div class="parameter-description text-center">{{ $t('ai_agent.top_p_description') }}</div>
        </div>
        
        <div class="form-group">
          <label for="presencePenalty" class="text-center">{{ $t('ai_agent.presence_penalty') }}</label>
          <div class="slider-container">
            <input 
              type="range" 
              id="presencePenalty" 
              v-model.number="parameters.presencePenalty" 
              min="-2" 
              max="2" 
              step="0.1"
            />
            <span class="slider-value">{{ parameters.presencePenalty.toFixed(1) }}</span>
          </div>
          <div class="parameter-description text-center">{{ $t('ai_agent.presence_penalty_description') }}</div>
        </div>
        
        <div class="form-group">
          <label for="frequencyPenalty" class="text-center">{{ $t('ai_agent.frequency_penalty') }}</label>
          <div class="slider-container">
            <input 
              type="range" 
              id="frequencyPenalty" 
              v-model.number="parameters.frequencyPenalty" 
              min="-2" 
              max="2" 
              step="0.1"
            />
            <span class="slider-value">{{ parameters.frequencyPenalty.toFixed(1) }}</span>
          </div>
          <div class="parameter-description text-center">{{ $t('ai_agent.frequency_penalty_description') }}</div>
        </div>
      </div>
      
      <div class="actions text-center">
        <button class="btn btn-primary" @click="applyModelSettings">
          {{ $t('ai_agent.apply_settings') }}
        </button>
        <button class="btn btn-secondary" @click="resetParameters">
          {{ $t('ai_agent.reset_defaults') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, reactive, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useToast } from 'vue-toastification';

export default {
  name: 'AIModelSelector',
  
  props: {
    initialModelId: {
      type: String,
      default: null
    },
    initialParameters: {
      type: Object,
      default: () => ({})
    }
  },
  
  emits: ['model-selected', 'parameters-updated'],
  
  setup(props, { emit }) {
    const { t } = useI18n();
    const toast = useToast();
    
    const availableModels = ref([]);
    const selectedModel = ref(null);
    const parameters = reactive({
      temperature: 0.7,
      maxTokens: 1000,
      topP: 1.0,
      presencePenalty: 0.0,
      frequencyPenalty: 0.0
    });
    
    const fetchAvailableModels = async () => {
      try {
        const response = await fetch('/api/ai-management/models');
        const data = await response.json();
        
        if (data.status === 'success') {
          availableModels.value = data.data.map(model => ({
            ...model,
            icon: getModelIcon(model.provider)
          }));
          
          // If initial model ID is provided, select that model
          if (props.initialModelId) {
            const initialModel = availableModels.value.find(model => model.id === props.initialModelId);
            if (initialModel) {
              selectModel(initialModel);
            }
          }
        } else {
          toast.error(t('ai_agent.error_fetching_models'));
        }
      } catch (error) {
        console.error('Error fetching AI models:', error);
        toast.error(t('ai_agent.error_fetching_models'));
      }
    };
    
    const getModelIcon = (provider) => {
      switch (provider.toLowerCase()) {
        case 'openai':
          return 'fab fa-openai';
        case 'google':
          return 'fab fa-google';
        case 'anthropic':
          return 'fas fa-robot';
        case 'meta':
          return 'fab fa-facebook';
        case 'local':
          return 'fas fa-server';
        default:
          return 'fas fa-microchip';
      }
    };
    
    const selectModel = (model) => {
      selectedModel.value = model;
      
      // Set max tokens to half of the model's token limit by default
      parameters.maxTokens = Math.min(parameters.maxTokens, model.tokenLimit);
      
      // Apply initial parameters if provided
      if (props.initialParameters && Object.keys(props.initialParameters).length > 0) {
        Object.keys(props.initialParameters).forEach(key => {
          if (parameters[key] !== undefined) {
            parameters[key] = props.initialParameters[key];
          }
        });
      }
      
      emit('model-selected', model);
    };
    
    const applyModelSettings = () => {
      if (!selectedModel.value) {
        toast.warning(t('ai_agent.select_model_first'));
        return;
      }
      
      emit('parameters-updated', { ...parameters });
      toast.success(t('ai_agent.settings_applied'));
    };
    
    const resetParameters = () => {
      parameters.temperature = 0.7;
      parameters.maxTokens = Math.min(1000, selectedModel.value.tokenLimit);
      parameters.topP = 1.0;
      parameters.presencePenalty = 0.0;
      parameters.frequencyPenalty = 0.0;
      
      emit('parameters-updated', { ...parameters });
      toast.info(t('ai_agent.settings_reset'));
    };
    
    // Watch for changes in parameters
    watch(parameters, () => {
      // Ensure maxTokens doesn't exceed the model's token limit
      if (selectedModel.value && parameters.maxTokens > selectedModel.value.tokenLimit) {
        parameters.maxTokens = selectedModel.value.tokenLimit;
      }
    }, { deep: true });
    
    onMounted(() => {
      fetchAvailableModels();
    });
    
    return {
      availableModels,
      selectedModel,
      parameters,
      selectModel,
      applyModelSettings,
      resetParameters
    };
  }
};
</script>

<style scoped>
.ai-model-selector {
  padding: 20px;
  font-family: 'Cairo', 'Roboto', sans-serif;
}

.text-center {
  text-align: center;
}

.selector-title {
  color: #333;
  margin-bottom: 20px;
  font-weight: 600;
  font-size: 22px;
}

.models-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.model-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.model-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
}

.model-card.selected {
  border-color: #1976D2;
  background-color: rgba(25, 118, 210, 0.05);
}

.model-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: rgba(25, 118, 210, 0.1);
  color: #1976D2;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin: 0 auto 15px;
}

.model-info h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #333;
}

.model-description {
  color: #666;
  font-size: 14px;
  margin-bottom: 15px;
  line-height: 1.4;
}

.model-capabilities {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 15px;
  justify-content: center;
}

.capability-badge {
  background-color: rgba(25, 118, 210, 0.1);
  color: #1976D2;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.model-metrics {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.metric {
  font-size: 14px;
  color: #666;
}

.metric-label {
  font-weight: 500;
  margin-right: 5px;
}

.metric-value {
  color: #333;
}

.model-parameters {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-top: 20px;
}

.model-parameters h3 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 18px;
  color: #333;
}

.parameter-form {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.slider-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.slider-container input[type="range"] {
  flex: 1;
  height: 6px;
  -webkit-appearance: none;
  appearance: none;
  background: #e0e0e0;
  border-radius: 3px;
  outline: none;
}

.slider-container input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #1976D2;
  cursor: pointer;
}

.slider-container input[type="range"]::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #1976D2;
  cursor: pointer;
  border: none;
}

.slider-value {
  min-width: 40px;
  text-align: center;
  font-weight: 500;
  color: #333;
}

.parameter-description {
  font-size: 12px;
  color: #757575;
  margin-top: 5px;
}

.actions {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.btn {
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: background-color 0.2s;
}

.btn-primary {
  background-color: #1976D2;
  color: white;
}

.btn-primary:hover {
  background-color: #1565C0;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #333;
}

.btn-secondary:hover {
  background-color: #e0e0e0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .parameter-form {
    grid-template-columns: 1fr;
  }
  
  .actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}
</style>
