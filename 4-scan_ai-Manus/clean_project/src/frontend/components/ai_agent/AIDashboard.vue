// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/ai_agent/AIDashboard.vue

<template>
  <div class="ai-dashboard">
    <h1 class="dashboard-title text-center">{{ $t('ai_agent.dashboard_title') }}</h1>
    
    <div class="dashboard-summary">
      <div class="summary-card" v-for="(metric, index) in summaryMetrics" :key="index">
        <div class="card-icon" :class="metric.status">
          <i :class="metric.icon"></i>
        </div>
        <div class="card-content">
          <h3 class="text-center">{{ metric.name }}</h3>
          <div class="metric-value text-center">{{ metric.value }}{{ metric.unit }}</div>
          <div class="metric-status text-center" :class="metric.status">
            {{ metric.statusText }}
          </div>
        </div>
      </div>
    </div>

    <div class="dashboard-charts">
      <div class="chart-container">
        <h2 class="text-center">{{ $t('ai_agent.usage_by_model') }}</h2>
        <resource-usage-chart 
          :chartData="modelUsageChartData" 
          :chartOptions="modelUsageChartOptions"
          chartId="model-usage-chart"
        />
      </div>
      <div class="chart-container">
        <h2 class="text-center">{{ $t('ai_agent.cost_analysis') }}</h2>
        <resource-usage-chart 
          :chartData="costChartData" 
          :chartOptions="costChartOptions"
          chartId="cost-chart"
        />
      </div>
    </div>

    <div class="dashboard-tables">
      <div class="table-container">
        <h2 class="text-center">{{ $t('ai_agent.recent_requests') }}</h2>
        <table class="ai-table">
          <thead>
            <tr>
              <th>{{ $t('ai_agent.timestamp') }}</th>
              <th>{{ $t('ai_agent.model') }}</th>
              <th>{{ $t('ai_agent.tokens') }}</th>
              <th>{{ $t('ai_agent.cost') }}</th>
              <th>{{ $t('ai_agent.status') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="recentRequests.length === 0">
              <td colspan="5" class="no-data text-center">{{ $t('ai_agent.no_data') }}</td>
            </tr>
            <tr v-for="request in recentRequests" :key="request.id">
              <td>{{ formatDate(request.timestamp) }}</td>
              <td>{{ request.model }}</td>
              <td>{{ request.tokens.toLocaleString() }}</td>
              <td>{{ formatCost(request.cost) }}</td>
              <td>
                <span class="status-badge" :class="request.status">
                  {{ getStatusText(request.status) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <div class="model-management">
      <h2 class="text-center">{{ $t('ai_agent.model_management') }}</h2>
      <div class="model-actions text-center">
        <button class="btn btn-primary" @click="showModelSelector">
          <i class="fas fa-cog"></i> {{ $t('ai_agent.configure_models') }}
        </button>
      </div>
    </div>
    
    <!-- Model Selector Dialog -->
    <div v-if="showModelSelectorDialog" class="dialog-overlay" @click.self="closeModelSelector">
      <div class="dialog-container">
        <div class="dialog-header">
          <h2 class="text-center">{{ $t('ai_agent.model_configuration') }}</h2>
          <button class="btn-close" @click="closeModelSelector" aria-label="إغلاق">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="dialog-body">
          <ai-model-selector 
            :initialModelId="currentModelId"
            :initialParameters="currentParameters"
            @model-selected="handleModelSelected"
            @parameters-updated="handleParametersUpdated"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, reactive, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useToast } from 'vue-toastification';
import ResourceUsageChart from '../monitoring/charts/ResourceUsageChart.vue';
import AIModelSelector from './AIModelSelector.vue';

export default {
  name: 'AIDashboard',
  
  components: {
    ResourceUsageChart,
    AIModelSelector
  },
  
  setup() {
    const { t } = useI18n();
    const toast = useToast();
    
    // Summary metrics
    const summaryMetrics = reactive([
      {
        name: t('ai_agent.total_requests'),
        value: '0',
        unit: '',
        icon: 'fas fa-exchange-alt',
        status: 'normal',
        statusText: t('ai_agent.normal')
      },
      {
        name: t('ai_agent.total_tokens'),
        value: '0',
        unit: '',
        icon: 'fas fa-coins',
        status: 'normal',
        statusText: t('ai_agent.normal')
      },
      {
        name: t('ai_agent.monthly_cost'),
        value: '0',
        unit: '$',
        icon: 'fas fa-dollar-sign',
        status: 'normal',
        statusText: t('ai_agent.normal')
      },
      {
        name: t('ai_agent.success_rate'),
        value: '0',
        unit: '%',
        icon: 'fas fa-check-circle',
        status: 'normal',
        statusText: t('ai_agent.normal')
      }
    ]);
    
    // Recent requests data
    const recentRequests = ref([]);
    
    // Model selector dialog
    const showModelSelectorDialog = ref(false);
    const currentModelId = ref(null);
    const currentParameters = ref({});
    
    // Chart data
    const modelUsageChartData = reactive({
      labels: [],
      datasets: [
        {
          label: t('ai_agent.tokens_used'),
          data: [],
          backgroundColor: [
            '#3F51B5',
            '#E91E63',
            '#009688',
            '#FF9800',
            '#9C27B0',
            '#607D8B'
          ],
          borderWidth: 1
        }
      ]
    });
    
    const costChartData = reactive({
      labels: [],
      datasets: [
        {
          label: t('ai_agent.daily_cost'),
          data: [],
          borderColor: '#3F51B5',
          backgroundColor: 'rgba(63, 81, 181, 0.2)',
          fill: true,
          tension: 0.4
        }
      ]
    });
    
    // Chart options
    const modelUsageChartOptions = computed(() => ({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          align: 'center'
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const label = context.label || '';
              const value = context.raw || 0;
              const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
              const percentage = Math.round((value / total) * 100);
              return `${label}: ${value.toLocaleString()} (${percentage}%)`;
            }
          }
        }
      }
    }));
    
    const costChartOptions = computed(() => ({
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: '$'
          }
        },
        x: {
          title: {
            display: true,
            text: t('ai_agent.date')
          }
        }
      },
      plugins: {
        tooltip: {
          mode: 'index',
          intersect: false
        },
        legend: {
          position: 'top',
          align: 'center'
        }
      }
    }));
    
    // Methods
    const fetchAIUsageData = async () => {
      try {
        // Fetch summary data
        const summaryResponse = await fetch('/api/ai-management/usage/summary');
        const summaryData = await summaryResponse.json();
        
        if (summaryData.status === 'success') {
          // Update total requests
          summaryMetrics[0].value = summaryData.data.totalRequests.toLocaleString();
          
          // Update total tokens
          summaryMetrics[1].value = summaryData.data.totalTokens.toLocaleString();
          
          // Update monthly cost
          const monthlyCost = summaryData.data.monthlyCost;
          summaryMetrics[2].value = monthlyCost.toFixed(2);
          
          // Update cost status
          if (monthlyCost > 1000) {
            summaryMetrics[2].status = 'critical';
            summaryMetrics[2].statusText = t('ai_agent.high');
          } else if (monthlyCost > 500) {
            summaryMetrics[2].status = 'warning';
            summaryMetrics[2].statusText = t('ai_agent.moderate');
          } else {
            summaryMetrics[2].status = 'normal';
            summaryMetrics[2].statusText = t('ai_agent.low');
          }
          
          // Update success rate
          const successRate = summaryData.data.successRate;
          summaryMetrics[3].value = successRate.toFixed(1);
          
          // Update success rate status
          if (successRate < 90) {
            summaryMetrics[3].status = 'critical';
            summaryMetrics[3].statusText = t('ai_agent.poor');
          } else if (successRate < 95) {
            summaryMetrics[3].status = 'warning';
            summaryMetrics[3].statusText = t('ai_agent.fair');
          } else {
            summaryMetrics[3].status = 'normal';
            summaryMetrics[3].statusText = t('ai_agent.good');
          }
        }
        
        // Fetch model usage data
        const modelUsageResponse = await fetch('/api/ai-management/usage/by-model');
        const modelUsageData = await modelUsageResponse.json();
        
        if (modelUsageData.status === 'success') {
          modelUsageChartData.labels = modelUsageData.data.map(item => item.model);
          modelUsageChartData.datasets[0].data = modelUsageData.data.map(item => item.tokens);
        }
        
        // Fetch cost data
        const costResponse = await fetch('/api/ai-management/usage/cost-history');
        const costData = await costResponse.json();
        
        if (costData.status === 'success') {
          costChartData.labels = costData.data.map(item => formatDate(item.date));
          costChartData.datasets[0].data = costData.data.map(item => item.cost);
        }
        
        // Fetch recent requests
        const recentRequestsResponse = await fetch('/api/ai-management/usage/recent-requests');
        const recentRequestsData = await recentRequestsResponse.json();
        
        if (recentRequestsData.status === 'success') {
          recentRequests.value = recentRequestsData.data;
        }
        
        // Fetch current model settings
        const settingsResponse = await fetch('/api/ai-management/settings');
        const settingsData = await settingsResponse.json();
        
        if (settingsData.status === 'success') {
          currentModelId.value = settingsData.data.defaultModelId;
          currentParameters.value = settingsData.data.defaultParameters;
        }
      } catch (error) {
        console.error('Error fetching AI usage data:', error);
        toast.error(t('ai_agent.error_fetching_data'));
      }
    };
    
    const formatDate = (dateString) => {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    };
    
    const formatCost = (cost) => {
      return `$${cost.toFixed(4)}`;
    };
    
    const getStatusText = (status) => {
      switch (status) {
        case 'success':
          return t('ai_agent.success');
        case 'error':
          return t('ai_agent.error');
        case 'timeout':
          return t('ai_agent.timeout');
        default:
          return status;
      }
    };
    
    const showModelSelector = () => {
      showModelSelectorDialog.value = true;
    };
    
    const closeModelSelector = () => {
      showModelSelectorDialog.value = false;
    };
    
    const handleModelSelected = (model) => {
      console.log('Model selected:', model);
      // This will be handled by the AIModelSelector component
    };
    
    const handleParametersUpdated = async (parameters) => {
      try {
        const response = await fetch('/api/ai-management/settings', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            defaultModelId: currentModelId.value,
            defaultParameters: parameters
          })
        });
        
        const data = await response.json();
        if (data.status === 'success') {
          currentParameters.value = parameters;
          toast.success(t('ai_agent.settings_saved'));
        } else {
          toast.error(data.message || t('ai_agent.error_saving_settings'));
        }
      } catch (error) {
        console.error('Error saving AI settings:', error);
        toast.error(t('ai_agent.error_saving_settings'));
      }
    };
    
    // Initialize data
    onMounted(() => {
      fetchAIUsageData();
      
      // Set up polling for AI usage data
      const dataInterval = setInterval(fetchAIUsageData, 300000); // Update every 5 minutes
      
      // Clean up interval on component unmount
      return () => {
        clearInterval(dataInterval);
      };
    });
    
    return {
      // Data
      summaryMetrics,
      recentRequests,
      showModelSelectorDialog,
      currentModelId,
      currentParameters,
      
      // Chart data
      modelUsageChartData,
      costChartData,
      modelUsageChartOptions,
      costChartOptions,
      
      // Methods
      formatDate,
      formatCost,
      getStatusText,
      showModelSelector,
      closeModelSelector,
      handleModelSelected,
      handleParametersUpdated
    };
  }
};
</script>

<style scoped>
.ai-dashboard {
  padding: 20px;
  font-family: 'Cairo', 'Roboto', sans-serif;
}

.text-center {
  text-align: center;
}

.dashboard-title {
  color: #333;
  margin-bottom: 20px;
  font-weight: 600;
  font-size: 24px;
}

.dashboard-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.summary-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  align-items: center;
}

.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 24px;
}

.card-icon.normal {
  background-color: rgba(76, 175, 80, 0.2);
  color: #4CAF50;
}

.card-icon.warning {
  background-color: rgba(255, 152, 0, 0.2);
  color: #FF9800;
}

.card-icon.critical {
  background-color: rgba(244, 67, 54, 0.2);
  color: #F44336;
}

.card-content h3 {
  margin: 0 0 5px 0;
  font-size: 16px;
  color: #666;
}

.metric-value {
  font-size: 24px;
  font-weight: 600;
  color: #333;
}

.metric-status {
  font-size: 14px;
  margin-top: 5px;
}

.metric-status.normal {
  color: #4CAF50;
}

.metric-status.warning {
  color: #FF9800;
}

.metric-status.critical {
  color: #F44336;
}

.dashboard-charts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.chart-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  height: 300px;
}

.chart-container h2 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 18px;
  color: #333;
}

.dashboard-tables {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.table-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.table-container h2 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 18px;
  color: #333;
}

.ai-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.ai-table th,
.ai-table td {
  padding: 12px 15px;
  text-align: center;
  border-bottom: 1px solid #e0e0e0;
}

.ai-table th {
  background-color: #f5f5f5;
  font-weight: 600;
  color: #333;
}

.ai-table tr:hover {
  background-color: #f9f9f9;
}

.no-data {
  text-align: center;
  color: #757575;
  padding: 30px 0;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.success {
  background-color: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.status-badge.error {
  background-color: rgba(244, 67, 54, 0.1);
  color: #F44336;
}

.status-badge.timeout {
  background-color: rgba(255, 152, 0, 0.1);
  color: #FF9800;
}

.model-management {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.model-management h2 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 18px;
  color: #333;
}

.model-actions {
  margin-top: 20px;
}

.btn {
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: background-color 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.btn-primary {
  background-color: #1976D2;
  color: white;
}

.btn-primary:hover {
  background-color: #1565C0;
}

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
  width: 90%;
  max-width: 900px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
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

/* Responsive adjustments */
@media (max-width: 768px) {
  .dashboard-charts {
    grid-template-columns: 1fr;
  }
  
  .dashboard-tables {
    grid-template-columns: 1fr;
  }
}
</style>
