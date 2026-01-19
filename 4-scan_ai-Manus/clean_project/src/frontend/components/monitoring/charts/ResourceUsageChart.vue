// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/monitoring/charts/ResourceUsageChart.vue

<template>
  <div class="chart-wrapper">
    <canvas :id="chartId" ref="chartCanvas"></canvas>
    <div v-if="loading" class="chart-loading">
      <div class="spinner"></div>
      <span>{{ $t('common.loading') }}</span>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';
import { onMounted, onUnmounted, ref, watch } from 'vue';

export default {
  name: 'ResourceUsageChart',
  
  props: {
    chartData: {
      type: Object,
      required: true
    },
    chartOptions: {
      type: Object,
      required: true
    },
    chartId: {
      type: String,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  
  setup(props) {
    const chartCanvas = ref(null);
    let chart = null;
    
    const createChart = () => {
      if (chartCanvas.value) {
        // Destroy existing chart if it exists
        if (chart) {
          chart.destroy();
        }
        
        // Create new chart
        chart = new Chart(chartCanvas.value, {
          type: 'line',
          data: props.chartData,
          options: props.chartOptions
        });
      }
    };
    
    const updateChart = () => {
      if (chart) {
        chart.data = props.chartData;
        chart.options = props.chartOptions;
        chart.update();
      }
    };
    
    onMounted(() => {
      createChart();
    });
    
    onUnmounted(() => {
      if (chart) {
        chart.destroy();
      }
    });
    
    // Watch for changes in chart data and options
    watch(() => props.chartData, () => {
      updateChart();
    }, { deep: true });
    
    watch(() => props.chartOptions, () => {
      updateChart();
    }, { deep: true });
    
    return {
      chartCanvas
    };
  }
};
</script>

<style scoped>
.chart-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}

.chart-loading {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.8);
  z-index: 10;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(33, 150, 243, 0.3);
  border-radius: 50%;
  border-top-color: #2196F3;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
