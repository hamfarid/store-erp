<!--
مكون مخطط استهلاك الموارد
يعرض هذا المكون مخططاً بيانياً لمقارنة استهلاك الموارد للنماذج المختلفة من حيث الذاكرة واستخدام المعالج

المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
-->

<template>
  <div class="resources-chart">
    <v-card flat>
      <v-card-text>
        <div ref="resourcesChart" class="chart-container"></div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'ResourcesChart',
  
  props: {
    results: {
      type: Object,
      required: true
    }
  },
  
  data() {
    return {
      chart: null
    };
  },
  
  mounted() {
    this.initChart();
    window.addEventListener('resize', this.resizeChart);
  },
  
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeChart);
    if (this.chart) {
      this.chart.dispose();
    }
  },
  
  methods: {
    initChart() {
      if (!this.results) return;
      
      const chartDom = this.$refs.resourcesChart;
      this.chart = echarts.init(chartDom);
      
      const models = [];
      const memoryData = [];
      const cpuData = [];
      const gpuMemoryData = [];
      
      // استخراج البيانات من النتائج
      for (const [modelName, result] of Object.entries(this.results)) {
        if (!result.resource_usage) continue;
        
        models.push(modelName);
        
        const resources = result.resource_usage;
        memoryData.push(resources.memory_used?.mean?.toFixed(2) || 0);
        cpuData.push(resources.cpu_usage?.mean?.toFixed(2) || 0);
        
        if (resources.gpu_memory_used) {
          gpuMemoryData.push(resources.gpu_memory_used.mean?.toFixed(2) || 0);
        } else {
          gpuMemoryData.push(0);
        }
      }
      
      const option = {
        title: {
          text: 'مقارنة استهلاك الموارد',
          left: 'center',
          textStyle: {
            fontFamily: 'Tajawal, sans-serif'
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: (params) => {
            let result = `<div style="font-weight: bold; margin-bottom: 5px;">${params[0].name}</div>`;
            params.forEach(param => {
              let unit = param.seriesName === 'استهلاك المعالج' ? '%' : ' GB';
              result += `<div style="display: flex; justify-content: space-between; align-items: center; margin: 3px 0;">
                <span style="display: inline-block; margin-right: 5px; border-radius: 10px; width: 10px; height: 10px; background-color: ${param.color};"></span>
                <span style="flex: 1;">${param.seriesName}: </span>
                <span style="font-weight: bold;">${param.value}${unit}</span>
              </div>`;
            });
            return result;
          }
        },
        legend: {
          data: ['استهلاك الذاكرة', 'استهلاك المعالج', 'ذاكرة GPU'],
          top: 30,
          textStyle: {
            fontFamily: 'Tajawal, sans-serif'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: models,
          axisLabel: {
            rotate: 45,
            fontFamily: 'Tajawal, sans-serif'
          }
        },
        yAxis: [
          {
            type: 'value',
            name: 'الذاكرة (GB)',
            position: 'left',
            nameTextStyle: {
              fontFamily: 'Tajawal, sans-serif'
            },
            axisLabel: {
              formatter: '{value} GB',
              fontFamily: 'Tajawal, sans-serif'
            }
          },
          {
            type: 'value',
            name: 'استهلاك المعالج (%)',
            position: 'right',
            nameTextStyle: {
              fontFamily: 'Tajawal, sans-serif'
            },
            axisLabel: {
              formatter: '{value}%',
              fontFamily: 'Tajawal, sans-serif'
            },
            max: 100
          }
        ],
        series: [
          {
            name: 'استهلاك الذاكرة',
            type: 'bar',
            data: memoryData,
            yAxisIndex: 0,
            itemStyle: {
              color: '#E91E63'
            },
            emphasis: {
              focus: 'series'
            },
            label: {
              show: true,
              position: 'top',
              formatter: '{c} GB'
            }
          },
          {
            name: 'استهلاك المعالج',
            type: 'bar',
            data: cpuData,
            yAxisIndex: 1,
            itemStyle: {
              color: '#FF9800'
            },
            emphasis: {
              focus: 'series'
            },
            label: {
              show: true,
              position: 'top',
              formatter: '{c}%'
            }
          },
          {
            name: 'ذاكرة GPU',
            type: 'bar',
            data: gpuMemoryData,
            yAxisIndex: 0,
            itemStyle: {
              color: '#9C27B0'
            },
            emphasis: {
              focus: 'series'
            },
            label: {
              show: true,
              position: 'top',
              formatter: '{c} GB'
            }
          }
        ]
      };
      
      this.chart.setOption(option);
    },
    
    resizeChart() {
      if (this.chart) {
        this.chart.resize();
      }
    }
  },
  
  watch: {
    results: {
      handler() {
        this.$nextTick(() => {
          if (this.chart) {
            this.chart.dispose();
          }
          this.initChart();
        });
      },
      deep: true
    }
  }
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 400px;
}
</style>
