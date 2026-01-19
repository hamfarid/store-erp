<!--
مكون مخطط الأداء
يعرض هذا المكون مخططاً بيانياً لمقارنة أداء النماذج المختلفة من حيث الدقة والجودة

المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
-->

<template>
  <div class="performance-chart">
    <v-card flat>
      <v-card-text>
        <div ref="accuracyChart" class="chart-container"></div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'PerformanceChart',
  
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
      
      const chartDom = this.$refs.accuracyChart;
      this.chart = echarts.init(chartDom);
      
      const models = [];
      const accuracyData = [];
      const f1ScoreData = [];
      const confidenceData = [];
      const consistencyData = [];
      
      // استخراج البيانات من النتائج
      for (const [modelName, result] of Object.entries(this.results)) {
        if (!result.metrics) continue;
        
        models.push(modelName);
        accuracyData.push((result.metrics.accuracy.mean * 100).toFixed(2));
        f1ScoreData.push((result.metrics.f1_score.mean * 100).toFixed(2));
        confidenceData.push((result.metrics.avg_confidence.mean * 100).toFixed(2));
        
        if (result.stability && result.stability.consistency_score) {
          consistencyData.push((result.stability.consistency_score * 100).toFixed(2));
        } else {
          consistencyData.push(0);
        }
      }
      
      const option = {
        title: {
          text: 'مقارنة أداء النماذج',
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
              result += `<div style="display: flex; justify-content: space-between; align-items: center; margin: 3px 0;">
                <span style="display: inline-block; margin-right: 5px; border-radius: 10px; width: 10px; height: 10px; background-color: ${param.color};"></span>
                <span style="flex: 1;">${param.seriesName}: </span>
                <span style="font-weight: bold;">${param.value}%</span>
              </div>`;
            });
            return result;
          }
        },
        legend: {
          data: ['الدقة', 'F1-Score', 'الثقة', 'الاستقرار'],
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
        yAxis: {
          type: 'value',
          name: 'النسبة المئوية (%)',
          nameTextStyle: {
            fontFamily: 'Tajawal, sans-serif'
          },
          axisLabel: {
            formatter: '{value}%',
            fontFamily: 'Tajawal, sans-serif'
          },
          max: 100
        },
        series: [
          {
            name: 'الدقة',
            type: 'bar',
            data: accuracyData,
            itemStyle: {
              color: '#4CAF50'
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
            name: 'F1-Score',
            type: 'bar',
            data: f1ScoreData,
            itemStyle: {
              color: '#2196F3'
            },
            emphasis: {
              focus: 'series'
            }
          },
          {
            name: 'الثقة',
            type: 'bar',
            data: confidenceData,
            itemStyle: {
              color: '#FF9800'
            },
            emphasis: {
              focus: 'series'
            }
          },
          {
            name: 'الاستقرار',
            type: 'bar',
            data: consistencyData,
            itemStyle: {
              color: '#9C27B0'
            },
            emphasis: {
              focus: 'series'
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
