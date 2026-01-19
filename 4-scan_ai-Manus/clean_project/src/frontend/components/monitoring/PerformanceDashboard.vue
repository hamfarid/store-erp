// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/monitoring/PerformanceDashboard.vue

<template>
  <div class="performance-dashboard">
    <h1 class="dashboard-title text-center">{{ $t('performance_monitoring.dashboard_title') }}</h1>
    
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
        <h2 class="text-center">{{ $t('performance_monitoring.response_time') }}</h2>
        <resource-usage-chart 
          :chartData="responseTimeChartData" 
          :chartOptions="responseTimeChartOptions"
          chartId="response-time-chart"
        />
      </div>
      <div class="chart-container">
        <h2 class="text-center">{{ $t('performance_monitoring.error_rate') }}</h2>
        <resource-usage-chart 
          :chartData="errorRateChartData" 
          :chartOptions="errorRateChartOptions"
          chartId="error-rate-chart"
        />
      </div>
      <div class="chart-container">
        <h2 class="text-center">{{ $t('performance_monitoring.throughput') }}</h2>
        <resource-usage-chart 
          :chartData="throughputChartData" 
          :chartOptions="throughputChartOptions"
          chartId="throughput-chart"
        />
      </div>
    </div>

    <div class="dashboard-tables">
      <div class="table-container">
        <h2 class="text-center">{{ $t('performance_monitoring.top_endpoints') }}</h2>
        <table class="performance-table">
          <thead>
            <tr>
              <th>{{ $t('performance_monitoring.endpoint') }}</th>
              <th>{{ $t('performance_monitoring.avg_response_time') }}</th>
              <th>{{ $t('performance_monitoring.error_rate') }}</th>
              <th>{{ $t('performance_monitoring.requests') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="topEndpoints.length === 0">
              <td colspan="4" class="no-data text-center">{{ $t('performance_monitoring.no_data') }}</td>
            </tr>
            <tr v-for="endpoint in topEndpoints" :key="endpoint.path">
              <td>{{ endpoint.path }}</td>
              <td>{{ endpoint.avgResponseTime }}ms</td>
              <td>{{ endpoint.errorRate }}%</td>
              <td>{{ endpoint.requests }}</td>
            </tr>
          </tbody>
        </table>
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
  name: 'PerformanceDashboard',
  
  components: {
    ResourceUsageChart
  },
  
  setup() {
    const { t } = useI18n();
    const toast = useToast();
    
    // Summary metrics
    const summaryMetrics = reactive([
      {
        name: t('performance_monitoring.avg_response_time'),
        value: '0',
        unit: 'ms',
        icon: 'fas fa-tachometer-alt',
        status: 'normal',
        statusText: t('performance_monitoring.normal')
      },
      {
        name: t('performance_monitoring.error_rate'),
        value: '0',
        unit: '%',
        icon: 'fas fa-exclamation-triangle',
        status: 'normal',
        statusText: t('performance_monitoring.normal')
      },
      {
        name: t('performance_monitoring.throughput'),
        value: '0',
        unit: '/s',
        icon: 'fas fa-exchange-alt',
        status: 'normal',
        statusText: t('performance_monitoring.normal')
      },
      {
        name: t('performance_monitoring.uptime'),
        value: '0',
        unit: '%',
        icon: 'fas fa-clock',
        status: 'normal',
        statusText: t('performance_monitoring.normal')
      }
    ]);
    
    // Top endpoints data
    const topEndpoints = ref([]);
    
    // Chart data
    const responseTimeChartData = reactive({
      labels: [],
      datasets: [
        {
          label: t('performance_monitoring.response_time'),
          data: [],
          borderColor: '#3F51B5',
          backgroundColor: 'rgba(63, 81, 181, 0.2)',
          fill: true,
          tension: 0.4
        }
      ]
    });
    
    const errorRateChartData = reactive({
      labels: [],
      datasets: [
        {
          label: t('performance_monitoring.error_rate'),
          data: [],
          borderColor: '#E91E63',
          backgroundColor: 'rgba(233, 30, 99, 0.2)',
          fill: true,
          tension: 0.4
        }
      ]
    });
    
    const throughputChartData = reactive({
      labels: [],
      datasets: [
        {
          label: t('performance_monitoring.throughput'),
          data: [],
          borderColor: '#009688',
          backgroundColor: 'rgba(0, 150, 136, 0.2)',
          fill: true,
          tension: 0.4
        }
      ]
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
            text: t('performance_monitoring.time')
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
            text: t('performance_monitoring.time')
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
    
    const throughputChartOptions = computed(() => ({
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: t('performance_monitoring.requests_per_second')
          }
        },
        x: {
          title: {
            display: true,
            text: t('performance_monitoring.time')
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
    const fetchPerformanceData = async () => {
      try {
        // Fetch response time data
        const responseTimeResponse = await fetch('/api/performance-monitoring/metrics?metric_name=response_time&limit=24');
        const responseTimeData = await responseTimeResponse.json();
        
        if (responseTimeData.status === 'success') {
          responseTimeChartData.labels = responseTimeData.data.map(point => new Date(point.timestamp).toLocaleTimeString());
          responseTimeChartData.datasets[0].data = responseTimeData.data.map(point => point.value);
          
          // Update summary
          if (responseTimeData.data.length > 0) {
            const latestValue = responseTimeData.data[responseTimeData.data.length - 1].value;
            summaryMetrics[0].value = latestValue.toFixed(1);
            
            // Update status
            if (latestValue > 500) {
              summaryMetrics[0].status = 'critical';
              summaryMetrics[0].statusText = t('performance_monitoring.slow');
            } else if (latestValue > 200) {
              summaryMetrics[0].status = 'warning';
              summaryMetrics[0].statusText = t('performance_monitoring.moderate');
            } else {
              summaryMetrics[0].status = 'normal';
              summaryMetrics[0].statusText = t('performance_monitoring.fast');
            }
          }
        }
        
        // Fetch error rate data
        const errorRateResponse = await fetch('/api/performance-monitoring/metrics?metric_name=error_rate&limit=24');
        const errorRateData = await errorRateResponse.json();
        
        if (errorRateData.status === 'success') {
          errorRateChartData.labels = errorRateData.data.map(point => new Date(point.timestamp).toLocaleTimeString());
          errorRateChartData.datasets[0].data = errorRateData.data.map(point => point.value);
          
          // Update summary
          if (errorRateData.data.length > 0) {
            const latestValue = errorRateData.data[errorRateData.data.length - 1].value;
            summaryMetrics[1].value = latestValue.toFixed(2);
            
            // Update status
            if (latestValue > 5) {
              summaryMetrics[1].status = 'critical';
              summaryMetrics[1].statusText = t('performance_monitoring.high');
            } else if (latestValue > 1) {
              summaryMetrics[1].status = 'warning';
              summaryMetrics[1].statusText = t('performance_monitoring.elevated');
            } else {
              summaryMetrics[1].status = 'normal';
              summaryMetrics[1].statusText = t('performance_monitoring.low');
            }
          }
        }
        
        // Fetch throughput data
        const throughputResponse = await fetch('/api/performance-monitoring/metrics?metric_name=throughput&limit=24');
        const throughputData = await throughputResponse.json();
        
        if (throughputData.status === 'success') {
          throughputChartData.labels = throughputData.data.map(point => new Date(point.timestamp).toLocaleTimeString());
          throughputChartData.datasets[0].data = throughputData.data.map(point => point.value);
          
          // Update summary
          if (throughputData.data.length > 0) {
            const latestValue = throughputData.data[throughputData.data.length - 1].value;
            summaryMetrics[2].value = latestValue.toFixed(1);
            
            // Update status based on throughput (this is just an example, thresholds would depend on your system)
            if (latestValue > 100) {
              summaryMetrics[2].status = 'warning';
              summaryMetrics[2].statusText = t('performance_monitoring.high_load');
            } else {
              summaryMetrics[2].status = 'normal';
              summaryMetrics[2].statusText = t('performance_monitoring.normal_load');
            }
          }
        }
        
        // Fetch uptime data
        const uptimeResponse = await fetch('/api/performance-monitoring/metrics?metric_name=uptime&limit=1');
        const uptimeData = await uptimeResponse.json();
        
        if (uptimeData.status === 'success' && uptimeData.data.length > 0) {
          const latestValue = uptimeData.data[0].value;
          summaryMetrics[3].value = latestValue.toFixed(2);
          
          // Update status
          if (latestValue < 99) {
            summaryMetrics[3].status = 'critical';
            summaryMetrics[3].statusText = t('performance_monitoring.degraded');
          } else if (latestValue < 99.9) {
            summaryMetrics[3].status = 'warning';
            summaryMetrics[3].statusText = t('performance_monitoring.stable');
          } else {
            summaryMetrics[3].status = 'normal';
            summaryMetrics[3].statusText = t('performance_monitoring.excellent');
          }
        }
        
        // Fetch top endpoints
        const topEndpointsResponse = await fetch('/api/performance-monitoring/top-endpoints');
        const topEndpointsData = await topEndpointsResponse.json();
        
        if (topEndpointsData.status === 'success') {
          topEndpoints.value = topEndpointsData.data;
        }
      } catch (error) {
        console.error('Error fetching performance data:', error);
        toast.error(t('performance_monitoring.error_fetching_data'));
      }
    };
    
    // Initialize data
    onMounted(() => {
      fetchPerformanceData();
      
      // Set up polling for performance data
      const dataInterval = setInterval(fetchPerformanceData, 60000); // Update every minute
      
      // Clean up interval on component unmount
      return () => {
        clearInterval(dataInterval);
      };
    });
    
    return {
      // Data
      summaryMetrics,
      topEndpoints,
      
      // Chart data
      responseTimeChartData,
      errorRateChartData,
      throughputChartData,
      responseTimeChartOptions,
      errorRateChartOptions,
      throughputChartOptions
    };
  }
};
</script>

<style scoped>
.performance-dashboard {
  padding: 20px;
  font-family: 'Cairo', 'Roboto', sans-serif;
}

.dashboard-title {
  color: #333;
  margin-bottom: 20px;
  font-weight: 600;
  font-size: 24px;
}

.text-center {
  text-align: center;
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

.performance-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.performance-table th,
.performance-table td {
  padding: 12px 15px;
  text-align: center;
  border-bottom: 1px solid #e0e0e0;
}

.performance-table th {
  background-color: #f5f5f5;
  font-weight: 600;
  color: #333;
}

.performance-table tr:hover {
  background-color: #f9f9f9;
}

.no-data {
  text-align: center;
  color: #757575;
  padding: 30px 0;
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
