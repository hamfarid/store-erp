// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/monitoring/SystemHealthDashboard.vue
<template>
  <div class="system-health-dashboard">
    <v-card class="dashboard-card">
      <v-card-title class="text-center">لوحة صحة النظام</v-card-title>
      
      <v-card-text>
        <div class="status-overview">
          <div class="status-card" :class="getStatusClass(overallStatus)">
            <div class="status-icon">
              <v-icon size="48">{{ getStatusIcon(overallStatus) }}</v-icon>
            </div>
            <div class="status-details">
              <div class="status-title">الحالة العامة</div>
              <div class="status-value">{{ getStatusText(overallStatus) }}</div>
            </div>
          </div>
          
          <div class="metrics-summary">
            <div class="metric-item" v-for="(metric, index) in summaryMetrics" :key="index">
              <div class="metric-label">{{ metric.label }}</div>
              <div class="metric-value" :class="getMetricValueClass(metric.status)">
                {{ metric.value }}
              </div>
            </div>
          </div>
        </div>
        
        <v-divider class="my-4"></v-divider>
        
        <div class="system-components">
          <h3 class="text-center mb-4">مكونات النظام</h3>
          
          <v-expansion-panels>
            <v-expansion-panel
              v-for="(component, index) in systemComponents"
              :key="index"
            >
              <v-expansion-panel-header>
                <div class="component-header">
                  <v-icon :color="getStatusColor(component.status)" class="mr-2">
                    {{ getStatusIcon(component.status) }}
                  </v-icon>
                  <span>{{ component.name }}</span>
                  <span class="status-badge" :class="getStatusClass(component.status)">
                    {{ getStatusText(component.status) }}
                  </span>
                </div>
              </v-expansion-panel-header>
              
              <v-expansion-panel-content>
                <div class="component-details">
                  <div class="component-description">{{ component.description }}</div>
                  
                  <div class="component-metrics">
                    <div 
                      class="metric-detail" 
                      v-for="(metric, mIndex) in component.metrics" 
                      :key="`${index}-${mIndex}`"
                    >
                      <div class="metric-detail-label">{{ metric.label }}:</div>
                      <div class="metric-detail-value" :class="getMetricValueClass(metric.status)">
                        {{ metric.value }}
                        <v-icon 
                          x-small 
                          :color="getStatusColor(metric.status)" 
                          class="ml-1"
                        >
                          {{ getMetricTrendIcon(metric.trend) }}
                        </v-icon>
                      </div>
                    </div>
                  </div>
                  
                  <div class="component-actions">
                    <v-btn 
                      small 
                      text 
                      color="primary" 
                      @click="viewComponentDetails(component.id)"
                    >
                      <v-icon left small>mdi-information</v-icon>
                      التفاصيل
                    </v-btn>
                    
                    <v-btn 
                      small 
                      text 
                      color="primary" 
                      @click="viewComponentLogs(component.id)"
                    >
                      <v-icon left small>mdi-text-box-outline</v-icon>
                      السجلات
                    </v-btn>
                    
                    <v-btn 
                      small 
                      text 
                      :color="component.status === 'error' ? 'success' : 'warning'" 
                      @click="restartComponent(component.id)"
                      :disabled="component.status === 'restarting'"
                    >
                      <v-icon left small>mdi-restart</v-icon>
                      إعادة تشغيل
                    </v-btn>
                  </div>
                </div>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </div>
        
        <v-divider class="my-4"></v-divider>
        
        <div class="alerts-section">
          <h3 class="text-center mb-4">التنبيهات الأخيرة</h3>
          
          <div v-if="recentAlerts.length === 0" class="no-alerts">
            <v-icon color="success" size="36">mdi-check-circle</v-icon>
            <div class="no-alerts-text">لا توجد تنبيهات حديثة</div>
          </div>
          
          <v-timeline v-else dense>
            <v-timeline-item
              v-for="(alert, index) in recentAlerts"
              :key="index"
              :color="getAlertColor(alert.severity)"
              small
            >
              <div class="alert-item">
                <div class="alert-time">{{ formatAlertTime(alert.timestamp) }}</div>
                <div class="alert-title" :class="`text--${getAlertColor(alert.severity)}`">
                  {{ alert.title }}
                </div>
                <div class="alert-message">{{ alert.message }}</div>
                <div class="alert-component">{{ alert.component }}</div>
                <div class="alert-actions">
                  <v-btn 
                    x-small 
                    text 
                    color="primary" 
                    @click="viewAlertDetails(alert.id)"
                  >
                    التفاصيل
                  </v-btn>
                  
                  <v-btn 
                    x-small 
                    text 
                    color="primary" 
                    @click="dismissAlert(alert.id)"
                    v-if="!alert.dismissed"
                  >
                    تجاهل
                  </v-btn>
                </div>
              </div>
            </v-timeline-item>
          </v-timeline>
          
          <div class="text-center mt-4" v-if="recentAlerts.length > 0">
            <v-btn 
              text 
              color="primary" 
              @click="viewAllAlerts"
            >
              عرض جميع التنبيهات
            </v-btn>
          </div>
        </div>
      </v-card-text>
      
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn 
          color="primary" 
          text 
          @click="refreshDashboard"
          :loading="isRefreshing"
        >
          <v-icon left>mdi-refresh</v-icon>
          تحديث
        </v-btn>
        <v-btn 
          color="primary" 
          text 
          @click="exportHealthReport"
        >
          <v-icon left>mdi-file-export</v-icon>
          تصدير التقرير
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
/**
 * مكون لوحة صحة النظام
 * 
 * يعرض هذا المكون حالة صحة النظام بشكل عام ومكوناته المختلفة
 * مع عرض المقاييس الرئيسية والتنبيهات الأخيرة
 */
export default {
  name: 'SystemHealthDashboard',
  
  data() {
    return {
      isRefreshing: false,
      overallStatus: 'healthy', // healthy, warning, error
      
      // مقاييس الملخص
      summaryMetrics: [
        { label: 'وحدات نشطة', value: '12/12', status: 'healthy' },
        { label: 'استخدام المعالج', value: '32%', status: 'healthy' },
        { label: 'استخدام الذاكرة', value: '45%', status: 'healthy' },
        { label: 'استخدام القرص', value: '78%', status: 'warning' },
        { label: 'وقت التشغيل', value: '15 يوم', status: 'healthy' }
      ],
      
      // مكونات النظام
      systemComponents: [
        {
          id: 'core',
          name: 'النواة',
          status: 'healthy',
          description: 'المكون الأساسي للنظام الذي يدير جميع العمليات الأخرى',
          metrics: [
            { label: 'استخدام المعالج', value: '15%', status: 'healthy', trend: 'stable' },
            { label: 'استخدام الذاكرة', value: '320MB', status: 'healthy', trend: 'up' },
            { label: 'عدد العمليات', value: '24', status: 'healthy', trend: 'stable' },
            { label: 'وقت الاستجابة', value: '45ms', status: 'healthy', trend: 'down' }
          ]
        },
        {
          id: 'database',
          name: 'قاعدة البيانات',
          status: 'warning',
          description: 'خدمة قاعدة البيانات الرئيسية للنظام',
          metrics: [
            { label: 'استخدام المعالج', value: '45%', status: 'warning', trend: 'up' },
            { label: 'استخدام الذاكرة', value: '1.2GB', status: 'warning', trend: 'up' },
            { label: 'حجم قاعدة البيانات', value: '4.5GB', status: 'healthy', trend: 'up' },
            { label: 'وقت الاستجابة للاستعلام', value: '120ms', status: 'warning', trend: 'up' }
          ]
        },
        {
          id: 'ai_services',
          name: 'خدمات الذكاء الاصطناعي',
          status: 'healthy',
          description: 'خدمات الذكاء الاصطناعي ومعالجة البيانات',
          metrics: [
            { label: 'استخدام المعالج', value: '65%', status: 'warning', trend: 'stable' },
            { label: 'استخدام الذاكرة', value: '2.8GB', status: 'healthy', trend: 'stable' },
            { label: 'عدد الطلبات', value: '450/دقيقة', status: 'healthy', trend: 'up' },
            { label: 'وقت المعالجة', value: '350ms', status: 'healthy', trend: 'down' }
          ]
        },
        {
          id: 'api_gateway',
          name: 'بوابة API',
          status: 'healthy',
          description: 'بوابة API الرئيسية للنظام',
          metrics: [
            { label: 'استخدام المعالج', value: '25%', status: 'healthy', trend: 'stable' },
            { label: 'استخدام الذاكرة', value: '450MB', status: 'healthy', trend: 'stable' },
            { label: 'عدد الطلبات', value: '1200/دقيقة', status: 'healthy', trend: 'up' },
            { label: 'وقت الاستجابة', value: '85ms', status: 'healthy', trend: 'stable' }
          ]
        },
        {
          id: 'file_storage',
          name: 'تخزين الملفات',
          status: 'error',
          description: 'خدمة تخزين الملفات والوسائط',
          metrics: [
            { label: 'استخدام المعالج', value: '5%', status: 'healthy', trend: 'stable' },
            { label: 'استخدام الذاكرة', value: '120MB', status: 'healthy', trend: 'stable' },
            { label: 'المساحة المستخدمة', value: '78%', status: 'warning', trend: 'up' },
            { label: 'حالة الاتصال', value: 'منقطع', status: 'error', trend: 'stable' }
          ]
        }
      ],
      
      // التنبيهات الأخيرة
      recentAlerts: [
        {
          id: 'alert-001',
          timestamp: new Date(Date.now() - 5 * 60 * 1000), // قبل 5 دقائق
          severity: 'error',
          title: 'فشل الاتصال بخدمة تخزين الملفات',
          message: 'تعذر الاتصال بخدمة تخزين الملفات. يرجى التحقق من إعدادات الاتصال.',
          component: 'تخزين الملفات',
          dismissed: false
        },
        {
          id: 'alert-002',
          timestamp: new Date(Date.now() - 15 * 60 * 1000), // قبل 15 دقيقة
          severity: 'warning',
          title: 'ارتفاع استخدام قاعدة البيانات',
          message: 'ارتفع استخدام موارد قاعدة البيانات عن الحد الطبيعي. يرجى مراقبة الأداء.',
          component: 'قاعدة البيانات',
          dismissed: false
        },
        {
          id: 'alert-003',
          timestamp: new Date(Date.now() - 45 * 60 * 1000), // قبل 45 دقيقة
          severity: 'info',
          title: 'تم تحديث النظام',
          message: 'تم تحديث النظام إلى الإصدار 3.2.1 بنجاح.',
          component: 'النظام',
          dismissed: true
        }
      ]
    };
  },
  
  methods: {
    /**
     * الحصول على صنف CSS لحالة معينة
     * @param {String} status - حالة المكون (healthy, warning, error)
     * @returns {String} - صنف CSS
     */
    getStatusClass(status) {
      switch (status) {
        case 'healthy':
          return 'status-healthy';
        case 'warning':
          return 'status-warning';
        case 'error':
          return 'status-error';
        case 'restarting':
          return 'status-restarting';
        default:
          return '';
      }
    },
    
    /**
     * الحصول على لون حالة معينة
     * @param {String} status - حالة المكون (healthy, warning, error)
     * @returns {String} - لون الحالة
     */
    getStatusColor(status) {
      switch (status) {
        case 'healthy':
          return 'success';
        case 'warning':
          return 'warning';
        case 'error':
          return 'error';
        case 'restarting':
          return 'info';
        default:
          return 'grey';
      }
    },
    
    /**
     * الحصول على أيقونة حالة معينة
     * @param {String} status - حالة المكون (healthy, warning, error)
     * @returns {String} - أيقونة الحالة
     */
    getStatusIcon(status) {
      switch (status) {
        case 'healthy':
          return 'mdi-check-circle';
        case 'warning':
          return 'mdi-alert-circle';
        case 'error':
          return 'mdi-close-circle';
        case 'restarting':
          return 'mdi-restart';
        default:
          return 'mdi-help-circle';
      }
    },
    
    /**
     * الحصول على نص حالة معينة
     * @param {String} status - حالة المكون (healthy, warning, error)
     * @returns {String} - نص الحالة
     */
    getStatusText(status) {
      switch (status) {
        case 'healthy':
          return 'سليم';
        case 'warning':
          return 'تحذير';
        case 'error':
          return 'خطأ';
        case 'restarting':
          return 'إعادة تشغيل';
        default:
          return 'غير معروف';
      }
    },
    
    /**
     * الحصول على صنف CSS لقيمة مقياس
     * @param {String} status - حالة المقياس (healthy, warning, error)
     * @returns {String} - صنف CSS
     */
    getMetricValueClass(status) {
      switch (status) {
        case 'healthy':
          return 'metric-healthy';
        case 'warning':
          return 'metric-warning';
        case 'error':
          return 'metric-error';
        default:
          return '';
      }
    },
    
    /**
     * الحصول على أيقونة اتجاه المقياس
     * @param {String} trend - اتجاه المقياس (up, down, stable)
     * @returns {String} - أيقونة الاتجاه
     */
    getMetricTrendIcon(trend) {
      switch (trend) {
        case 'up':
          return 'mdi-arrow-up';
        case 'down':
          return 'mdi-arrow-down';
        case 'stable':
          return 'mdi-arrow-right';
        default:
          return '';
      }
    },
    
    /**
     * الحصول على لون التنبيه
     * @param {String} severity - شدة التنبيه (info, warning, error)
     * @returns {String} - لون التنبيه
     */
    getAlertColor(severity) {
      switch (severity) {
        case 'info':
          return 'info';
        case 'warning':
          return 'warning';
        case 'error':
          return 'error';
        default:
          return 'grey';
      }
    },
    
    /**
     * تنسيق وقت التنبيه
     * @param {Date} timestamp - الطابع الزمني
     * @returns {String} - الوقت المنسق
     */
    formatAlertTime(timestamp) {
      if (!timestamp) return '';
      
      const now = new Date();
      const diff = Math.floor((now - timestamp) / 1000 / 60); // الفرق بالدقائق
      
      if (diff < 1) {
        return 'الآن';
      } else if (diff < 60) {
        return `منذ ${diff} دقيقة`;
      } else if (diff < 24 * 60) {
        const hours = Math.floor(diff / 60);
        return `منذ ${hours} ساعة`;
      } else {
        const days = Math.floor(diff / (24 * 60));
        return `منذ ${days} يوم`;
      }
    },
    
    /**
     * عرض تفاصيل المكون
     * @param {String} componentId - معرف المكون
     */
    viewComponentDetails(componentId) {
      console.log(`عرض تفاصيل المكون: ${componentId}`);
      // يمكن هنا تنفيذ منطق عرض تفاصيل المكون
    },
    
    /**
     * عرض سجلات المكون
     * @param {String} componentId - معرف المكون
     */
    viewComponentLogs(componentId) {
      console.log(`عرض سجلات المكون: ${componentId}`);
      // يمكن هنا تنفيذ منطق عرض سجلات المكون
    },
    
    /**
     * إعادة تشغيل المكون
     * @param {String} componentId - معرف المكون
     */
    restartComponent(componentId) {
      console.log(`إعادة تشغيل المكون: ${componentId}`);
      
      // تحديث حالة المكون إلى "إعادة تشغيل"
      const component = this.systemComponents.find(c => c.id === componentId);
      if (component) {
        component.status = 'restarting';
        
        // محاكاة إعادة التشغيل
        setTimeout(() => {
          component.status = 'healthy';
        }, 3000);
      }
    },
    
    /**
     * عرض تفاصيل التنبيه
     * @param {String} alertId - معرف التنبيه
     */
    viewAlertDetails(alertId) {
      console.log(`عرض تفاصيل التنبيه: ${alertId}`);
      // يمكن هنا تنفيذ منطق عرض تفاصيل التنبيه
    },
    
    /**
     * تجاهل التنبيه
     * @param {String} alertId - معرف التنبيه
     */
    dismissAlert(alertId) {
      console.log(`تجاهل التنبيه: ${alertId}`);
      
      // تحديث حالة التنبيه إلى "تم تجاهله"
      const alert = this.recentAlerts.find(a => a.id === alertId);
      if (alert) {
        alert.dismissed = true;
      }
    },
    
    /**
     * عرض جميع التنبيهات
     */
    viewAllAlerts() {
      console.log('عرض جميع التنبيهات');
      // يمكن هنا تنفيذ منطق عرض جميع التنبيهات
    },
    
    /**
     * تحديث لوحة المعلومات
     */
    refreshDashboard() {
      this.isRefreshing = true;
      
      // محاكاة تحديث البيانات
      setTimeout(() => {
        // يمكن هنا تنفيذ منطق تحديث البيانات
        this.isRefreshing = false;
      }, 1500);
    },
    
    /**
     * تصدير تقرير صحة النظام
     */
    exportHealthReport() {
      console.log('تصدير تقرير صحة النظام');
      // يمكن هنا تنفيذ منطق تصدير التقرير
    }
  }
};
</script>

<style scoped>
.system-health-dashboard {
  width: 100%;
}

.dashboard-card {
  border-radius: 8px;
  overflow: hidden;
}

.status-overview {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.status-card {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-radius: 8px;
  flex: 1;
  min-width: 250px;
}

.status-healthy {
  background-color: rgba(76, 175, 80, 0.1);
  border: 1px solid rgba(76, 175, 80, 0.3);
}

.status-warning {
  background-color: rgba(255, 193, 7, 0.1);
  border: 1px solid rgba(255, 193, 7, 0.3);
}

.status-error {
  background-color: rgba(244, 67, 54, 0.1);
  border: 1px solid rgba(244, 67, 54, 0.3);
}

.status-restarting {
  background-color: rgba(3, 169, 244, 0.1);
  border: 1px solid rgba(3, 169, 244, 0.3);
}

.status-icon {
  margin-left: 1rem;
}

.status-details {
  flex: 1;
}

.status-title {
  font-weight: bold;
  margin-bottom: 0.25rem;
}

.status-value {
  font-size: 1.25rem;
  font-weight: bold;
}

.metrics-summary {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  flex: 2;
}

.metric-item {
  flex: 1;
  min-width: 120px;
  text-align: center;
  padding: 0.75rem;
  border-radius: 8px;
  background-color: rgba(0, 0, 0, 0.03);
}

.metric-label {
  font-size: 0.85rem;
  color: var(--v-secondary-darken1);
  margin-bottom: 0.25rem;
}

.metric-value {
  font-weight: bold;
  font-size: 1.1rem;
}

.metric-healthy {
  color: var(--v-success-base);
}

.metric-warning {
  color: var(--v-warning-base);
}

.metric-error {
  color: var(--v-error-base);
}

.component-header {
  display: flex;
  align-items: center;
  width: 100%;
}

.status-badge {
  margin-right: auto;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: bold;
}

.component-details {
  padding: 0.5rem 0;
}

.component-description {
  margin-bottom: 1rem;
  color: var(--v-secondary-darken1);
}

.component-metrics {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
}

.metric-detail {
  flex: 1;
  min-width: 150px;
  display: flex;
  align-items: center;
}

.metric-detail-label {
  flex: 1;
  color: var(--v-secondary-darken1);
}

.metric-detail-value {
  font-weight: bold;
  display: flex;
  align-items: center;
}

.component-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.no-alerts {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  color: var(--v-success-base);
}

.no-alerts-text {
  margin-top: 0.5rem;
  font-weight: bold;
}

.alert-item {
  padding: 0.5rem 0;
}

.alert-time {
  font-size: 0.75rem;
  color: var(--v-secondary-darken1);
  margin-bottom: 0.25rem;
}

.alert-title {
  font-weight: bold;
  margin-bottom: 0.25rem;
}

.alert-message {
  margin-bottom: 0.25rem;
}

.alert-component {
  font-size: 0.85rem;
  color: var(--v-secondary-darken1);
  margin-bottom: 0.5rem;
}

.alert-actions {
  display: flex;
  gap: 0.5rem;
}

/* تحسينات للأجهزة المحمولة */
@media (max-width: 600px) {
  .status-overview {
    flex-direction: column;
  }
  
  .metrics-summary {
    flex-direction: column;
  }
  
  .component-metrics {
    flex-direction: column;
  }
}
</style>
