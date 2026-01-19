<!--
مكون مخطط السرعة
يعرض هذا المكون مخططاً بيانياً لمقارنة سرعة النماذج المختلفة من حيث FPS وزمن التنبؤ

المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
-->

<template>
  <div class="speed-chart">
    <v-card flat>
      <v-card-text>
        <div ref="speedChart" class="chart-container"></div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'SpeedChart',
  
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
      
      const chartDom = this.$refs.speedChart;
      this.chart = echarts.init(chartDom);
      
      const models = [];
      const fpsData = [];
      const inferenceTimeData = [];
      const stdTimeData = [];
      
      // استخراج البيانات من النتائج
      for (const [modelName, result] of Object.entries(this.results)) {
        if (!result.timing) continue;
        
        models.push(modelName);
        fpsData.push(result.timing.fps.mean.toFixed(2));
        inferenceTimeData.push((result.timing.avg_inference_time.mean * 1000).toFixed(2)); // تحويل إلى مللي ثانية
        stdTimeData.push((result.timing.avg_inference_time.std * 1000).toFixed(2)); // تحويل إلى مللي ثانية
      }
      
      const option = {
        title: {
          text: 'مقارنة سرعة النماذج',
          left: 'center',
          textStyle: {
            fontFamily: 'Tajawal, sans-serif'
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          },
          formatter: (params) => {
            let result = `<div style="font-weight: bold; margin-bottom: 5px;">${params[0].name}</div>`;
            params.forEach(param => {
              let unit = param.seriesName === 'FPS' ? ' FPS' : ' مللي ثانية';
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
          data: ['FPS', 'زمن التنبؤ', 'الانحراف المعياري'],
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
            name: 'FPS',
            position: 'left',
            nameTextStyle: {
              fontFamily: 'Tajawal, sans-serif'
            },
            axisLabel: {
              formatter: '{value} FPS',
              fontFamily: 'Tajawal, sans-serif'
            }
          },
          {
            type: 'value',
            name: 'زمن التنبؤ (مللي ثانية)',
            position: 'right',
            nameTextStyle: {
              fontFamily: 'Tajawal, sans-serif'
            },
            axisLabel: {
              formatter: '{value} ms',
              fontFamily: 'Tajawal, sans-serif'
            }
          }
        ],
        series: [
          {
            name: 'FPS',
            type: 'bar',
            data: fpsData,
            yAxisIndex: 0,
            itemStyle: {
              color: '#2196F3'
            },
            emphasis: {
              focus: 'series'
            },
            label: {
              show: true,
              position: 'top',
              formatter: '{c} FPS'
            }
          },
          {
            name: 'زمن التنبؤ',
            type: 'bar',
            data: inferenceTimeData,
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
              formatter: '{c} ms'
            }
          },
          {
            name: 'الانحراف المعياري',
            type: 'line',
            data: stdTimeData,
            yAxisIndex: 1,
            itemStyle: {
              color: '#E91E63'
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
