# /home/ubuntu/image_search_integration/auto_learning/frontend/charts/KeywordPerformanceChart.vue
<template>
  <div class="keyword-performance-chart">
    <div ref="chartContainer" class="chart-container"></div>
    <div v-if="loading" class="loading-overlay">
      <el-spinner size="medium"></el-spinner>
    </div>
    <div v-if="error" class="error-message">
      {{ $t('حدث خطأ أثناء تحميل البيانات') }}
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'KeywordPerformanceChart',
  props: {
    data: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      chart: null,
      loading: false,
      error: false
    };
  },
  watch: {
    data: {
      handler(newData) {
        this.renderChart(newData);
      },
      deep: true
    }
  },
  mounted() {
    this.initChart();
    if (this.data && this.data.length > 0) {
      this.renderChart(this.data);
    }
    
    window.addEventListener('resize', this.resizeChart);
  },
  beforeDestroy() {
    if (this.chart) {
      this.chart.dispose();
      this.chart = null;
    }
    
    window.removeEventListener('resize', this.resizeChart);
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$refs.chartContainer, null, {
        renderer: 'canvas'
      });
    },
    renderChart(data) {
      if (!this.chart || !data || data.length === 0) return;
      
      this.loading = true;
      this.error = false;
      
      try {
        const keywords = data.map(item => item.keyword);
        const searchCounts = data.map(item => item.searchCount);
        const resultCounts = data.map(item => item.resultCount);
        const successRates = data.map(item => item.successRate);
        
        const option = {
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          legend: {
            data: [
              this.$t('عدد عمليات البحث'),
              this.$t('عدد النتائج'),
              this.$t('معدل النجاح')
            ],
            textStyle: {
              fontFamily: 'Cairo, sans-serif'
            }
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: [
            {
              type: 'category',
              data: keywords,
              axisLabel: {
                rotate: 45,
                fontFamily: 'Cairo, sans-serif'
              }
            }
          ],
          yAxis: [
            {
              type: 'value',
              name: this.$t('العدد'),
              position: 'left',
              axisLabel: {
                formatter: '{value}'
              }
            },
            {
              type: 'value',
              name: this.$t('معدل النجاح (%)'),
              position: 'right',
              axisLabel: {
                formatter: '{value}%'
              },
              max: 100,
              min: 0
            }
          ],
          series: [
            {
              name: this.$t('عدد عمليات البحث'),
              type: 'bar',
              data: searchCounts,
              itemStyle: {
                color: '#409EFF'
              }
            },
            {
              name: this.$t('عدد النتائج'),
              type: 'bar',
              data: resultCounts,
              itemStyle: {
                color: '#67C23A'
              }
            },
            {
              name: this.$t('معدل النجاح'),
              type: 'line',
              yAxisIndex: 1,
              data: successRates,
              itemStyle: {
                color: '#E6A23C'
              }
            }
          ]
        };
        
        this.chart.setOption(option);
        this.loading = false;
      } catch (error) {
        console.error('Error rendering keyword performance chart:', error);
        this.loading = false;
        this.error = true;
      }
    },
    resizeChart() {
      if (this.chart) {
        this.chart.resize();
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.keyword-performance-chart {
  position: relative;
  width: 100%;
  height: 400px;
  
  .chart-container {
    width: 100%;
    height: 100%;
  }
  
  .loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(255, 255, 255, 0.7);
  }
  
  .error-message {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: #F56C6C;
    font-size: 16px;
    text-align: center;
  }
}
</style>
