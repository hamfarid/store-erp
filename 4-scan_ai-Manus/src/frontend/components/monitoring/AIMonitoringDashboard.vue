// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/monitoring/AIMonitoringDashboard.vue

<template>
  <div class="ai-monitoring-dashboard">
    <h1 class="dashboard-title text-center">{{ $t('ai_monitoring.dashboard_title') }}</h1>
    
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
        <h2 class="text-center">{{ $t('ai_monitoring.response_time_by_model') }}</h2>
        <resource-usage-chart 
          :chartData="responseTimeChartData" 
          :chartOptions="responseTimeChartOptions"
          chartId="ai-response-time-chart"
        />
      </div>
      <div class="chart-container">
        <h2 class="text-center">{{ $t('ai_monitoring.error_rate_by_model') }}</h2>
        <resource-usage-chart 
          :chartData="errorRateChartData" 
          :chartOptions="errorRateChartOptions"
          chartId="ai-error-rate-chart"
        />
      </div>
    </div>

    <div class="dashboard-tables">
      <div class="table-container">
        <h2 class="text-center">{{ $t('ai_monitoring.model_performance') }}</h2>
        <table class="monitoring-table">
          <thead>
            <tr>
              <th>{{ $t('ai_monitoring.model_name') }}</th>
              <th>{{ $t('ai_monitoring.avg_response_time') }}</th>
              <th>{{ $t('ai_monitoring.error_rate') }}</th>
              <th>{{ $t('ai_monitoring.usage_count') }}</th>
              <th>{{ $t('ai_monitoring.status') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="modelPerformance.length === 0">
              <td colspan="5" class="no-data text-center">{{ $t('ai_monitoring.no_data') }}</td>
            </tr>
            <tr v-for="model in modelPerformance" :key="model.id">
              <td>{{ model.name }}</td>
              <td>{{ model.avgResponseTime }}ms</td>
              <td>{{ model.errorRate }}%</td>
              <td>{{ model.usageCount }}</td>
              <td>
                <span class="status-badge" :class="model.status">
                  {{ getStatusText(model.status) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <div class="alert-settings">
      <h2 class="text-center">{{ $t('ai_monitoring.alert_settings') }}</h2>
      <div class="settings-form">
        <div class="form-group">
          <label for="responseTimeThreshold" class="text-center">{{ $t('ai_monitoring.response_time_threshold') }}</label>
          <div class="threshold-input-group">
            <input 
              type="number" 
              id="responseTimeThreshold" 
              v-model.number="alertSettings.responseTimeThreshold" 
              min="100"
              step="100"
              class="text-center"
            />
            <span class="threshold-unit">ms</span>
          </div>
        </div>
        
        <div class="form-group">
          <label for="errorRateThreshold" class="text-center">{{ $t('ai_monitoring.error_rate_threshold') }}</label>
          <div class="threshold-input-group">
            <input 
              type="number" 
              id="errorRateThreshold" 
              v-model.number="alertSettings.errorRateThreshold" 
              min="0"
              max="100"
              step="1"
              class="text-center"
            />
            <span class="threshold-unit">%</span>
          </div>
        </div>
        
        <div class="form-group form-checkbox">
          <label class="checkbox-label">
            <input type="checkbox" v-model="alertSettings.enableEmailAlerts" />
            <span>{{ $t('ai_monitoring.enable_email_alerts') }}</span>
          </label>
        </div>
        
        <div class="form-group form-checkbox">
          <label class="checkbox-label">
            <input type="checkbox" v-model="alertSettings.enableSystemAlerts" />
            <span>{{ $t('ai_monitoring.enable_system_alerts') }}</span>
          </label>
        </div>
      </div>
      
      <div class="actions text-center">
        <button class="btn btn-primary" @click="saveAlertSettings">
          {{ $t('common.save') }}
        </button>
        <button class="btn btn-secondary" @click="resetAlertSettings">
          {{ $t('common.reset') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, reactive, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useToast } from 'vue-toastification';
import ResourceUsageChart from './charts/ResourceUsageChart.vue';

export default {
  name: 'AIMonitoringDashboard',
  
  components: {
    ResourceUsageChart
  },
  
  setup() {
    const { t } = useI18n();
    const toast = useToast();
    
    // Summary metrics
    const summaryMetrics = reactive([
      {
        name: t('ai_monitoring.avg_response_time'),
        value: '0',
        unit: 'ms',
        icon: 'fas fa-tachometer-alt',
        status: 'normal',
        statusText: t('ai_monitoring.normal')
      },
      {
        name: t('ai_monitoring.error_rate'),
        value: '0',
        unit: '%',
        icon: 'fas fa-exclamation-triangle',
        status: 'normal',
        statusText: t('ai_monitoring.normal')
      },
      {
        name: t('ai_monitoring.active_models'),
        value: '0',
        unit: '',
        icon: 'fas fa-microchip',
        status: 'normal',
        statusText: t('ai_monitoring.normal')
      },
      {
        name: t('ai_monitoring.total_requests'),
        value: '0',
        unit: '',
        icon: 'fas fa-exchange-alt',
        status: 'normal',
        statusText: t('ai_monitoring.normal')
      }
    ]);
    
    // Model performance data
    const modelPerformance = ref([]);
    
    // Alert settings
    const alertSettings = reactive({
      responseTimeThreshold: 2000,
      errorRateThreshold: 5,
      enableEmailAlerts: true,
      enableSystemAlerts: true
    });
    
    // Chart data
    const responseTimeChartData = reactive({
      labels: [],
      datasets: []
    });
    
    const errorRateChartData = reactive({
      labels: [],
      datasets: []
    });
    
    // Chart options
    const responseTimeChartOptions = computed(() => ({
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'ms'
          }
        },
        x: {
          title: {
            display: true,
            text: t('ai_monitoring.time')
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
    
    const errorRateChartOptions = computed(() => ({
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          title: {
            display: true,
            text: '%'
          }
        },
        x: {
          title: {
            display: true,
            text: t('ai_monitoring.time')
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
    const fetchAIMonitoringData = async () => {
      try {
        // Fetch summary data
        const summaryResponse = await fetch('/api/ai-monitoring/summary');
        const summaryData = await summaryResponse.json();
        
        if (summaryData.status === 'success') {
          // Update average response time
          const avgResponseTime = summaryData.data.avgResponseTime;
          summaryMetrics[0].value = avgResponseTime.toFixed(0);
          
          // Update response time status
          if (avgResponseTime > alertSettings.responseTimeThreshold) {
            summaryMetrics[0].status = 'critical';
            summaryMetrics[0].statusText = t('ai_monitoring.slow');
          } else if (avgResponseTime > alertSettings.responseTimeThreshold * 0.7) {
            summaryMetrics[0].status = 'warning';
            summaryMetrics[0].statusText = t('ai_monitoring.moderate');
          } else {
            summaryMetrics[0].status = 'normal';
            summaryMetrics[0].statusText = t('ai_monitoring.fast');
          }
          
          // Update error rate
          const errorRate = summaryData.data.errorRate;
          summaryMetrics[1].value = errorRate.toFixed(2);
          
          // Update error rate status
          if (errorRate > alertSettings.errorRateThreshold) {
            summaryMetrics[1].status = 'critical';
            summaryMetrics[1].statusText = t('ai_monitoring.high');
          } else if (errorRate > alertSettings.errorRateThreshold * 0.7) {
            summaryMetrics[1].status = 'warning';
            summaryMetrics[1].statusText = t('ai_monitoring.elevated');
          } else {
            summaryMetrics[1].status = 'normal';
            summaryMetrics[1].statusText = t('ai_monitoring.low');
          }
          
          // Update active models
          summaryMetrics[2].value = summaryData.data.activeModels.toString();
          
          // Update total requests
          summaryMetrics[3].value = summaryData.data.totalRequests.toLocaleString();
        }
        
        // Fetch model performance data
        const modelPerformanceResponse = await fetch('/api/ai-monitoring/model-performance');
        const modelPerformanceData = await modelPerformanceResponse.json();
        
        if (modelPerformanceData.status === 'success') {
          modelPerformance.value = modelPerformanceData.data;
        }
        
        // Fetch response time by model data
        const responseTimeResponse = await fetch('/api/ai-monitoring/response-time-by-model');
        const responseTimeData = await responseTimeResponse.json();
        
        if (responseTimeData.status === 'success') {
          responseTimeChartData.labels = responseTimeData.data.labels;
          responseTimeChartData.datasets = responseTimeData.data.models.map((model, index) => ({
            label: model.name,
            data: model.data,
            borderColor: getChartColor(index),
            backgroundColor: getChartColor(index, 0.2),
            fill: false,
            tension: 0.4
          }));
        }
        
        // Fetch error rate by model data
        const errorRateResponse = await fetch('/api/ai-monitoring/error-rate-by-model');
        const errorRateData = await errorRateResponse.json();
        
        if (errorRateData.status === 'success') {
          errorRateChartData.labels = errorRateData.data.labels;
          errorRateChartData.datasets = errorRateData.data.models.map((model, index) => ({
            label: model.name,
            data: model.data,
            borderColor: getChartColor(index),
            backgroundColor: getChartColor(index, 0.2),
            fill: false,
            tension: 0.4
          }));
        }
        
        // Fetch alert settings
        const alertSettingsResponse = await fetch('/api/ai-monitoring/alert-settings');
        const alertSettingsData = await alertSettingsResponse.json();
        
        if (alertSettingsData.status === 'success') {
          Object.assign(alertSettings, alertSettingsData.data);
        }
      } catch (error) {
        console.error('Error fetching AI monitoring data:', error);
        toast.error(t('ai_monitoring.error_fetching_data'));
      }
    };
    
    const getChartColor = (index, alpha = 1) => {
      const colors = [
        `rgba(25, 118, 210, ${alpha})`,   // Blue
        `rgba(233, 30, 99, ${alpha})`,    // Pink
        `rgba(0, 150, 136, ${alpha})`,    // Teal
        `rgba(255, 152, 0, ${alpha})`,    // Orange
        `rgba(156, 39, 176, ${alpha})`,   // Purple
        `rgba(76, 175, 80, ${alpha})`,    // Green
        `rgba(244, 67, 54, ${alpha})`,    // Red
        `rgba(121, 85, 72, ${alpha})`,    // Brown
        `rgba(96, 125, 139, ${alpha})`    // Blue Grey
      ];
      
      return colors[index % colors.length];
    };
    
    const getStatusText = (status) => {
      switch (status) {
        case 'online':
          return t('ai_monitoring.online');
        case 'offline':
          return t('ai_monitoring.offline');
        case 'degraded':
          return t('ai_monitoring.degraded');
        case 'maintenance':
          return t('ai_monitoring.maintenance');
        default:
          return status;
      }
    };
    
    const saveAlertSettings = async () => {
      try {
        const response = await fetch('/api/ai-monitoring/alert-settings', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(alertSettings)
        });
        
        const data = await response.json();
        if (data.status === 'success') {
          toast.success(t('ai_monitoring.settings_saved'));
        } else {
          toast.error(data.message || t('ai_monitoring.error_saving_settings'));
        }
      } catch (error) {
        console.error('Error saving alert settings:', error);
        toast.error(t('ai_monitoring.error_saving_settings'));
      }
    };
    
    const resetAlertSettings = async () => {
      try {
        const response = await fetch('/api/ai-monitoring/alert-settings/default');
        const data = await response.json();
        
        if (data.status === 'success') {
          Object.assign(alertSettings, data.data);
          toast.info(t('ai_monitoring.settings_reset'));
        } else {
          toast.error(data.message || t('ai_monitoring.error_resetting_settings'));
        }
      } catch (error) {
        console.error('Error resetting alert settings:', error);
        toast.error(t('ai_monitoring.error_resetting_settings'));
      }
    };
    
    // Initialize data
    onMounted(() => {
      fetchAIMonitoringData();
      
      // Set up polling for AI monitoring data
      const dataInterval = setInterval(fetchAIMonitoringData, 60000); // Update every minute
      
      // Clean up interval on component unmount
      return () => {
        clearInterval(dataInterval);
      };
    });
    
    return {
      // Data
      summaryMetrics,
      modelPerformance,
      alertSettings,
      
      // Chart data
      responseTimeChartData,
      errorRateChartData,
      responseTimeChartOptions,
      errorRateChartOptions,
      
      // Methods
      getStatusText,
      saveAlertSettings,
      resetAlertSettings
    };
  }
};
</script>

<style scoped>
.ai-monitoring-dashboard {
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

.monitoring-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.monitoring-table th,
.monitoring-table td {
  padding: 12px 15px;
  text-align: center;
  border-bottom: 1px solid #e0e0e0;
}

.monitoring-table th {
  background-color: #f5f5f5;
  font-weight: 600;
  color: #333;
}

.monitoring-table tr:hover {
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

.status-badge.online {
  background-color: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.status-badge.offline {
  background-color: rgba(244, 67, 54, 0.1);
  color: #F44336;
}

.status-badge.degraded {
  background-color: rgba(255, 152, 0, 0.1);
  color: #FF9800;
}

.status-badge.maintenance {
  background-color: rgba(96, 125, 139, 0.1);
  color: #607D8B;
}

.alert-settings {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.alert-settings h2 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 18px;
  color: #333;
}

.settings-form {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
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

.threshold-input-group {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.threshold-input-group input {
  width: 100px;
  padding: 8px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
}

.threshold-unit {
  color: #757575;
  font-size: 14px;
}

.form-checkbox {
  display: flex;
  align-items: center;
  justify-content: center;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.checkbox-label input {
  margin-left: 0;
  margin-right: 10px;
}

.checkbox-label span {
  font-size: 14px;
  color: #333;
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
  min-width: 100px;
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
  .dashboard-charts {
    grid-template-columns: 1fr;
  }
  
  .dashboard-tables {
    grid-template-columns: 1fr;
  }
  
  .settings-form {
    grid-template-columns: 1fr;
  }
}
</style>
