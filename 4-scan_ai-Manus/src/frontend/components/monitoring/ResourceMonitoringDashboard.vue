// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/monitoring/ResourceMonitoringDashboard.vue

<template>
  <div class="resource-monitoring-dashboard">
    <h1 class="dashboard-title">{{ $t('resource_monitoring.dashboard_title') }}</h1>
    
    <div class="dashboard-summary">
      <div class="summary-card" v-for="(metric, index) in summaryMetrics" :key="index">
        <div class="card-icon" :class="metric.status">
          <i :class="metric.icon"></i>
        </div>
        <div class="card-content">
          <h3>{{ metric.name }}</h3>
          <div class="metric-value">{{ metric.value }}{{ metric.unit }}</div>
          <div class="metric-status" :class="metric.status">
            {{ metric.statusText }}
          </div>
        </div>
      </div>
    </div>

    <div class="dashboard-charts">
      <div class="chart-container">
        <h2>{{ $t('resource_monitoring.cpu_usage') }}</h2>
        <resource-usage-chart 
          :chartData="cpuChartData" 
          :chartOptions="cpuChartOptions"
          chartId="cpu-chart"
        />
      </div>
      <div class="chart-container">
        <h2>{{ $t('resource_monitoring.memory_usage') }}</h2>
        <resource-usage-chart 
          :chartData="memoryChartData" 
          :chartOptions="memoryChartOptions"
          chartId="memory-chart"
        />
      </div>
      <div class="chart-container">
        <h2>{{ $t('resource_monitoring.disk_usage') }}</h2>
        <resource-usage-chart 
          :chartData="diskChartData" 
          :chartOptions="diskChartOptions"
          chartId="disk-chart"
        />
      </div>
    </div>

    <div class="dashboard-tables">
      <div class="table-container">
        <h2>{{ $t('resource_monitoring.active_metrics') }}</h2>
        <metrics-table 
          :metrics="metrics" 
          :loading="loadingMetrics"
          @edit-metric="editMetric"
          @delete-metric="deleteMetric"
        />
        <div class="table-actions">
          <button class="btn btn-primary" @click="showAddMetricDialog">
            <i class="fas fa-plus"></i> {{ $t('resource_monitoring.add_metric') }}
          </button>
        </div>
      </div>

      <div class="table-container">
        <h2>{{ $t('resource_monitoring.thresholds') }}</h2>
        <thresholds-table 
          :thresholds="thresholds" 
          :loading="loadingThresholds"
          @edit-threshold="editThreshold"
          @delete-threshold="deleteThreshold"
        />
        <div class="table-actions">
          <button class="btn btn-primary" @click="showAddThresholdDialog">
            <i class="fas fa-plus"></i> {{ $t('resource_monitoring.add_threshold') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Dialogs -->
    <metric-form-dialog
      v-if="showMetricDialog"
      :metric="selectedMetric"
      :isEdit="isEditingMetric"
      @close="closeMetricDialog"
      @save="saveMetric"
    />

    <threshold-form-dialog
      v-if="showThresholdDialog"
      :threshold="selectedThreshold"
      :metrics="metrics"
      :isEdit="isEditingThreshold"
      @close="closeThresholdDialog"
      @save="saveThreshold"
    />
  </div>
</template>

<script>
import { computed, onMounted, reactive, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useToast } from 'vue-toastification';
import ResourceUsageChart from './charts/ResourceUsageChart.vue';
import MetricFormDialog from './dialogs/MetricFormDialog.vue';
import ThresholdFormDialog from './dialogs/ThresholdFormDialog.vue';
import MetricsTable from './tables/MetricsTable.vue';
import ThresholdsTable from './tables/ThresholdsTable.vue';

export default {
  name: 'ResourceMonitoringDashboard',
  
  components: {
    ResourceUsageChart,
    MetricsTable,
    ThresholdsTable,
    MetricFormDialog,
    ThresholdFormDialog
  },
  
  setup() {
    const { t } = useI18n();
    const toast = useToast();
    
    // Metrics data
    const metrics = ref([]);
    const loadingMetrics = ref(true);
    const selectedMetric = ref(null);
    const showMetricDialog = ref(false);
    const isEditingMetric = ref(false);
    
    // Thresholds data
    const thresholds = ref([]);
    const loadingThresholds = ref(true);
    const selectedThreshold = ref(null);
    const showThresholdDialog = ref(false);
    const isEditingThreshold = ref(false);
    
    // Summary metrics
    const summaryMetrics = reactive([
      {
        name: t('resource_monitoring.cpu'),
        value: '0',
        unit: '%',
        icon: 'fas fa-microchip',
        status: 'normal',
        statusText: t('resource_monitoring.normal')
      },
      {
        name: t('resource_monitoring.memory'),
        value: '0',
        unit: '%',
        icon: 'fas fa-memory',
        status: 'normal',
        statusText: t('resource_monitoring.normal')
      },
      {
        name: t('resource_monitoring.disk'),
        value: '0',
        unit: '%',
        icon: 'fas fa-hdd',
        status: 'normal',
        statusText: t('resource_monitoring.normal')
      },
      {
        name: t('resource_monitoring.network'),
        value: '0',
        unit: 'MB/s',
        icon: 'fas fa-network-wired',
        status: 'normal',
        statusText: t('resource_monitoring.normal')
      }
    ]);
    
    // Chart data
    const cpuChartData = reactive({
      labels: [],
      datasets: [
        {
          label: t('resource_monitoring.cpu_usage'),
          data: [],
          borderColor: '#4CAF50',
          backgroundColor: 'rgba(76, 175, 80, 0.2)',
          fill: true,
          tension: 0.4
        }
      ]
    });
    
    const memoryChartData = reactive({
      labels: [],
      datasets: [
        {
          label: t('resource_monitoring.memory_usage'),
          data: [],
          borderColor: '#2196F3',
          backgroundColor: 'rgba(33, 150, 243, 0.2)',
          fill: true,
          tension: 0.4
        }
      ]
    });
    
    const diskChartData = reactive({
      labels: [],
      datasets: [
        {
          label: t('resource_monitoring.disk_usage'),
          data: [],
          borderColor: '#FF9800',
          backgroundColor: 'rgba(255, 152, 0, 0.2)',
          fill: true,
          tension: 0.4
        }
      ]
    });
    
    // Chart options
    const chartOptions = {
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
            text: t('resource_monitoring.time')
          }
        }
      },
      plugins: {
        tooltip: {
          mode: 'index',
          intersect: false
        },
        legend: {
          position: 'top'
        }
      }
    };
    
    const cpuChartOptions = computed(() => ({ ...chartOptions }));
    const memoryChartOptions = computed(() => ({ ...chartOptions }));
    const diskChartOptions = computed(() => ({ ...chartOptions }));
    
    // Methods
    const fetchMetrics = async () => {
      loadingMetrics.value = true;
      try {
        const response = await fetch('/api/resource-monitoring/metrics');
        const data = await response.json();
        if (data.status === 'success') {
          metrics.value = data.data;
        } else {
          toast.error(t('resource_monitoring.error_fetching_metrics'));
        }
      } catch (error) {
        console.error('Error fetching metrics:', error);
        toast.error(t('resource_monitoring.error_fetching_metrics'));
      } finally {
        loadingMetrics.value = false;
      }
    };
    
    const fetchThresholds = async () => {
      loadingThresholds.value = true;
      try {
        const response = await fetch('/api/resource-monitoring/thresholds');
        const data = await response.json();
        if (data.status === 'success') {
          thresholds.value = data.data;
        } else {
          toast.error(t('resource_monitoring.error_fetching_thresholds'));
        }
      } catch (error) {
        console.error('Error fetching thresholds:', error);
        toast.error(t('resource_monitoring.error_fetching_thresholds'));
      } finally {
        loadingThresholds.value = false;
      }
    };
    
    const fetchResourceData = async () => {
      try {
        // Fetch CPU data
        const cpuResponse = await fetch('/api/resource-monitoring/data-points?metric_name=cpu_usage&limit=24');
        const cpuData = await cpuResponse.json();
        
        if (cpuData.status === 'success') {
          cpuChartData.labels = cpuData.data.map(point => new Date(point.timestamp).toLocaleTimeString());
          cpuChartData.datasets[0].data = cpuData.data.map(point => point.value);
          
          // Update summary
          if (cpuData.data.length > 0) {
            const latestCpuValue = cpuData.data[cpuData.data.length - 1].value;
            summaryMetrics[0].value = latestCpuValue.toFixed(1);
            
            // Update status
            if (latestCpuValue > 90) {
              summaryMetrics[0].status = 'critical';
              summaryMetrics[0].statusText = t('resource_monitoring.critical');
            } else if (latestCpuValue > 70) {
              summaryMetrics[0].status = 'warning';
              summaryMetrics[0].statusText = t('resource_monitoring.warning');
            } else {
              summaryMetrics[0].status = 'normal';
              summaryMetrics[0].statusText = t('resource_monitoring.normal');
            }
          }
        }
        
        // Fetch Memory data
        const memoryResponse = await fetch('/api/resource-monitoring/data-points?metric_name=memory_usage&limit=24');
        const memoryData = await memoryResponse.json();
        
        if (memoryData.status === 'success') {
          memoryChartData.labels = memoryData.data.map(point => new Date(point.timestamp).toLocaleTimeString());
          memoryChartData.datasets[0].data = memoryData.data.map(point => point.value);
          
          // Update summary
          if (memoryData.data.length > 0) {
            const latestMemoryValue = memoryData.data[memoryData.data.length - 1].value;
            summaryMetrics[1].value = latestMemoryValue.toFixed(1);
            
            // Update status
            if (latestMemoryValue > 90) {
              summaryMetrics[1].status = 'critical';
              summaryMetrics[1].statusText = t('resource_monitoring.critical');
            } else if (latestMemoryValue > 70) {
              summaryMetrics[1].status = 'warning';
              summaryMetrics[1].statusText = t('resource_monitoring.warning');
            } else {
              summaryMetrics[1].status = 'normal';
              summaryMetrics[1].statusText = t('resource_monitoring.normal');
            }
          }
        }
        
        // Fetch Disk data
        const diskResponse = await fetch('/api/resource-monitoring/data-points?metric_name=disk_usage&limit=24');
        const diskData = await diskResponse.json();
        
        if (diskData.status === 'success') {
          diskChartData.labels = diskData.data.map(point => new Date(point.timestamp).toLocaleTimeString());
          diskChartData.datasets[0].data = diskData.data.map(point => point.value);
          
          // Update summary
          if (diskData.data.length > 0) {
            const latestDiskValue = diskData.data[diskData.data.length - 1].value;
            summaryMetrics[2].value = latestDiskValue.toFixed(1);
            
            // Update status
            if (latestDiskValue > 90) {
              summaryMetrics[2].status = 'critical';
              summaryMetrics[2].statusText = t('resource_monitoring.critical');
            } else if (latestDiskValue > 70) {
              summaryMetrics[2].status = 'warning';
              summaryMetrics[2].statusText = t('resource_monitoring.warning');
            } else {
              summaryMetrics[2].status = 'normal';
              summaryMetrics[2].statusText = t('resource_monitoring.normal');
            }
          }
        }
        
        // Fetch Network data
        const networkResponse = await fetch('/api/resource-monitoring/data-points?metric_name=network_throughput&limit=1');
        const networkData = await networkResponse.json();
        
        if (networkData.status === 'success' && networkData.data.length > 0) {
          const latestNetworkValue = networkData.data[0].value;
          summaryMetrics[3].value = latestNetworkValue.toFixed(2);
          
          // Update status
          if (latestNetworkValue > 50) {
            summaryMetrics[3].status = 'warning';
            summaryMetrics[3].statusText = t('resource_monitoring.high');
          } else {
            summaryMetrics[3].status = 'normal';
            summaryMetrics[3].statusText = t('resource_monitoring.normal');
          }
        }
      } catch (error) {
        console.error('Error fetching resource data:', error);
        toast.error(t('resource_monitoring.error_fetching_data'));
      }
    };
    
    // Dialog methods
    const showAddMetricDialog = () => {
      selectedMetric.value = {
        resourceType: '',
        metricName: '',
        displayName: '',
        unit: '',
        description: ''
      };
      isEditingMetric.value = false;
      showMetricDialog.value = true;
    };
    
    const editMetric = (metric) => {
      selectedMetric.value = { ...metric };
      isEditingMetric.value = true;
      showMetricDialog.value = true;
    };
    
    const closeMetricDialog = () => {
      showMetricDialog.value = false;
      selectedMetric.value = null;
    };
    
    const saveMetric = async (metric) => {
      try {
        let response;
        if (isEditingMetric.value) {
          response = await fetch(`/api/resource-monitoring/metrics/${metric.id}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(metric)
          });
        } else {
          response = await fetch('/api/resource-monitoring/metrics', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(metric)
          });
        }
        
        const data = await response.json();
        if (data.status === 'success') {
          toast.success(isEditingMetric.value 
            ? t('resource_monitoring.metric_updated') 
            : t('resource_monitoring.metric_created'));
          fetchMetrics();
          closeMetricDialog();
        } else {
          toast.error(data.detail || t('resource_monitoring.error_saving_metric'));
        }
      } catch (error) {
        console.error('Error saving metric:', error);
        toast.error(t('resource_monitoring.error_saving_metric'));
      }
    };
    
    const deleteMetric = async (metricId) => {
      if (confirm(t('resource_monitoring.confirm_delete_metric'))) {
        try {
          const response = await fetch(`/api/resource-monitoring/metrics/${metricId}`, {
            method: 'DELETE'
          });
          
          const data = await response.json();
          if (data.status === 'success') {
            toast.success(t('resource_monitoring.metric_deleted'));
            fetchMetrics();
          } else {
            toast.error(data.detail || t('resource_monitoring.error_deleting_metric'));
          }
        } catch (error) {
          console.error('Error deleting metric:', error);
          toast.error(t('resource_monitoring.error_deleting_metric'));
        }
      }
    };
    
    const showAddThresholdDialog = () => {
      selectedThreshold.value = {
        metricId: '',
        warningThreshold: 70,
        criticalThreshold: 90,
        enabled: true
      };
      isEditingThreshold.value = false;
      showThresholdDialog.value = true;
    };
    
    const editThreshold = (threshold) => {
      selectedThreshold.value = { ...threshold };
      isEditingThreshold.value = true;
      showThresholdDialog.value = true;
    };
    
    const closeThresholdDialog = () => {
      showThresholdDialog.value = false;
      selectedThreshold.value = null;
    };
    
    const saveThreshold = async (threshold) => {
      try {
        const response = await fetch('/api/resource-monitoring/thresholds', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(threshold)
        });
        
        const data = await response.json();
        if (data.status === 'success') {
          toast.success(isEditingThreshold.value 
            ? t('resource_monitoring.threshold_updated') 
            : t('resource_monitoring.threshold_created'));
          fetchThresholds();
          closeThresholdDialog();
        } else {
          toast.error(data.detail || t('resource_monitoring.error_saving_threshold'));
        }
      } catch (error) {
        console.error('Error saving threshold:', error);
        toast.error(t('resource_monitoring.error_saving_threshold'));
      }
    };
    
    const deleteThreshold = async (thresholdId) => {
      if (confirm(t('resource_monitoring.confirm_delete_threshold'))) {
        try {
          const response = await fetch(`/api/resource-monitoring/thresholds/${thresholdId}`, {
            method: 'DELETE'
          });
          
          const data = await response.json();
          if (data.status === 'success') {
            toast.success(t('resource_monitoring.threshold_deleted'));
            fetchThresholds();
          } else {
            toast.error(data.detail || t('resource_monitoring.error_deleting_threshold'));
          }
        } catch (error) {
          console.error('Error deleting threshold:', error);
          toast.error(t('resource_monitoring.error_deleting_threshold'));
        }
      }
    };
    
    // Initialize data
    onMounted(() => {
      fetchMetrics();
      fetchThresholds();
      fetchResourceData();
      
      // Set up polling for resource data
      const dataInterval = setInterval(fetchResourceData, 60000); // Update every minute
      
      // Clean up interval on component unmount
      return () => {
        clearInterval(dataInterval);
      };
    });
    
    return {
      // Data
      metrics,
      loadingMetrics,
      thresholds,
      loadingThresholds,
      summaryMetrics,
      
      // Chart data
      cpuChartData,
      memoryChartData,
      diskChartData,
      cpuChartOptions,
      memoryChartOptions,
      diskChartOptions,
      
      // Dialog state
      selectedMetric,
      showMetricDialog,
      isEditingMetric,
      selectedThreshold,
      showThresholdDialog,
      isEditingThreshold,
      
      // Methods
      showAddMetricDialog,
      editMetric,
      closeMetricDialog,
      saveMetric,
      deleteMetric,
      showAddThresholdDialog,
      editThreshold,
      closeThresholdDialog,
      saveThreshold,
      deleteThreshold
    };
  }
};
</script>

<style scoped>
.resource-monitoring-dashboard {
  padding: 20px;
  font-family: 'Cairo', 'Roboto', sans-serif;
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

.table-actions {
  margin-top: 15px;
  display: flex;
  justify-content: flex-end;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.btn-primary {
  background-color: #2196F3;
  color: white;
}

.btn-primary:hover {
  background-color: #1976D2;
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
