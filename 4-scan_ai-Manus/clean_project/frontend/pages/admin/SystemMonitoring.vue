<!-- File: /home/ubuntu/clean_project/frontend/pages/admin/SystemMonitoring.vue -->
<template>
  <div class="system-monitoring-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <i class="fas fa-chart-line"></i>
          مراقبة النظام
        </h1>
        <p class="page-description">
          مراقبة أداء النظام والخوادم والخدمات في الوقت الفعلي
        </p>
      </div>
      <div class="header-actions">
        <button class="btn btn-primary" @click="refreshData">
          <i class="fas fa-sync-alt" :class="{ 'fa-spin': refreshing }"></i>
          تحديث البيانات
        </button>
        <button class="btn btn-outline-primary" @click="exportReport">
          <i class="fas fa-download"></i>
          تصدير التقرير
        </button>
      </div>
    </div>

    <!-- System Status Overview -->
    <div class="status-overview">
      <div class="status-card" :class="systemStatus.overall">
        <div class="status-icon">
          <i :class="getStatusIcon(systemStatus.overall)"></i>
        </div>
        <div class="status-info">
          <h3>حالة النظام العامة</h3>
          <p>{{ getStatusText(systemStatus.overall) }}</p>
          <small>آخر تحديث: {{ formatTime(lastUpdate) }}</small>
        </div>
      </div>

      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-icon cpu">
            <i class="fas fa-microchip"></i>
          </div>
          <div class="metric-info">
            <h4>استخدام المعالج</h4>
            <div class="metric-value">{{ systemMetrics.cpu }}%</div>
            <div class="metric-bar">
              <div class="metric-fill" :style="{ width: systemMetrics.cpu + '%' }"></div>
            </div>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon memory">
            <i class="fas fa-memory"></i>
          </div>
          <div class="metric-info">
            <h4>استخدام الذاكرة</h4>
            <div class="metric-value">{{ systemMetrics.memory }}%</div>
            <div class="metric-bar">
              <div class="metric-fill" :style="{ width: systemMetrics.memory + '%' }"></div>
            </div>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon disk">
            <i class="fas fa-hdd"></i>
          </div>
          <div class="metric-info">
            <h4>استخدام القرص</h4>
            <div class="metric-value">{{ systemMetrics.disk }}%</div>
            <div class="metric-bar">
              <div class="metric-fill" :style="{ width: systemMetrics.disk + '%' }"></div>
            </div>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon network">
            <i class="fas fa-network-wired"></i>
          </div>
          <div class="metric-info">
            <h4>الشبكة</h4>
            <div class="metric-value">{{ systemMetrics.network }} MB/s</div>
            <div class="metric-status">{{ systemMetrics.networkStatus }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Services Status -->
    <div class="services-section">
      <div class="section-header">
        <h2>حالة الخدمات</h2>
        <div class="section-actions">
          <button class="btn btn-sm btn-outline-primary" @click="restartAllServices">
            <i class="fas fa-redo"></i>
            إعادة تشغيل جميع الخدمات
          </button>
        </div>
      </div>

      <div class="services-grid">
        <div 
          v-for="service in services" 
          :key="service.name"
          class="service-card"
          :class="service.status"
        >
          <div class="service-header">
            <div class="service-icon">
              <i :class="service.icon"></i>
            </div>
            <div class="service-info">
              <h4>{{ service.displayName }}</h4>
              <p>{{ service.description }}</p>
            </div>
            <div class="service-status">
              <span :class="['status-badge', service.status]">
                {{ getServiceStatusText(service.status) }}
              </span>
            </div>
          </div>

          <div class="service-metrics">
            <div class="metric">
              <label>وقت التشغيل:</label>
              <span>{{ service.uptime }}</span>
            </div>
            <div class="metric">
              <label>استخدام الذاكرة:</label>
              <span>{{ service.memoryUsage }} MB</span>
            </div>
            <div class="metric">
              <label>استخدام المعالج:</label>
              <span>{{ service.cpuUsage }}%</span>
            </div>
          </div>

          <div class="service-actions">
            <button 
              class="btn btn-sm btn-success" 
              @click="startService(service)"
              :disabled="service.status === 'running'"
            >
              <i class="fas fa-play"></i>
              تشغيل
            </button>
            <button 
              class="btn btn-sm btn-warning" 
              @click="restartService(service)"
              :disabled="service.status === 'stopped'"
            >
              <i class="fas fa-redo"></i>
              إعادة تشغيل
            </button>
            <button 
              class="btn btn-sm btn-danger" 
              @click="stopService(service)"
              :disabled="service.status === 'stopped'"
            >
              <i class="fas fa-stop"></i>
              إيقاف
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Performance Charts -->
    <div class="charts-section">
      <div class="section-header">
        <h2>مخططات الأداء</h2>
        <div class="chart-controls">
          <select v-model="chartTimeRange" @change="updateCharts" class="form-control">
            <option value="1h">آخر ساعة</option>
            <option value="6h">آخر 6 ساعات</option>
            <option value="24h">آخر 24 ساعة</option>
            <option value="7d">آخر 7 أيام</option>
          </select>
        </div>
      </div>

      <div class="charts-grid">
        <div class="chart-container">
          <h3>استخدام المعالج</h3>
          <canvas ref="cpuChart" class="chart"></canvas>
        </div>

        <div class="chart-container">
          <h3>استخدام الذاكرة</h3>
          <canvas ref="memoryChart" class="chart"></canvas>
        </div>

        <div class="chart-container">
          <h3>حركة الشبكة</h3>
          <canvas ref="networkChart" class="chart"></canvas>
        </div>

        <div class="chart-container">
          <h3>استخدام القرص</h3>
          <canvas ref="diskChart" class="chart"></canvas>
        </div>
      </div>
    </div>

    <!-- System Logs -->
    <div class="logs-section">
      <div class="section-header">
        <h2>سجلات النظام</h2>
        <div class="log-controls">
          <select v-model="selectedLogLevel" @change="filterLogs" class="form-control">
            <option value="">جميع المستويات</option>
            <option value="error">أخطاء</option>
            <option value="warning">تحذيرات</option>
            <option value="info">معلومات</option>
            <option value="debug">تصحيح</option>
          </select>
          <button class="btn btn-sm btn-outline-danger" @click="clearLogs">
            <i class="fas fa-trash"></i>
            مسح السجلات
          </button>
        </div>
      </div>

      <div class="logs-container">
        <div class="log-entry" v-for="log in filteredLogs" :key="log.id" :class="log.level">
          <div class="log-time">{{ formatTime(log.timestamp) }}</div>
          <div class="log-level">
            <span :class="['level-badge', log.level]">{{ log.level.toUpperCase() }}</span>
          </div>
          <div class="log-service">{{ log.service }}</div>
          <div class="log-message">{{ log.message }}</div>
        </div>
      </div>
    </div>

    <!-- Alerts -->
    <div v-if="alerts.length > 0" class="alerts-section">
      <div class="section-header">
        <h2>التنبيهات النشطة</h2>
        <button class="btn btn-sm btn-outline-secondary" @click="dismissAllAlerts">
          <i class="fas fa-times"></i>
          إغلاق جميع التنبيهات
        </button>
      </div>

      <div class="alerts-list">
        <div 
          v-for="alert in alerts" 
          :key="alert.id"
          class="alert-item"
          :class="alert.severity"
        >
          <div class="alert-icon">
            <i :class="getAlertIcon(alert.severity)"></i>
          </div>
          <div class="alert-content">
            <h4>{{ alert.title }}</h4>
            <p>{{ alert.message }}</p>
            <small>{{ formatTime(alert.timestamp) }}</small>
          </div>
          <button class="alert-dismiss" @click="dismissAlert(alert.id)">
            <i class="fas fa-times"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SystemMonitoring',
  data() {
    return {
      refreshing: false,
      lastUpdate: new Date(),
      chartTimeRange: '1h',
      selectedLogLevel: '',
      
      systemStatus: {
        overall: 'healthy' // healthy, warning, critical
      },
      
      systemMetrics: {
        cpu: 45,
        memory: 62,
        disk: 78,
        network: 12.5,
        networkStatus: 'مستقر'
      },
      
      services: [
        {
          name: 'api_server',
          displayName: 'خادم API',
          description: 'خادم واجهة برمجة التطبيقات الرئيسي',
          icon: 'fas fa-server',
          status: 'running',
          uptime: '5 أيام 12 ساعة',
          memoryUsage: 256,
          cpuUsage: 15
        },
        {
          name: 'database',
          displayName: 'قاعدة البيانات',
          description: 'خادم قاعدة البيانات PostgreSQL',
          icon: 'fas fa-database',
          status: 'running',
          uptime: '5 أيام 12 ساعة',
          memoryUsage: 512,
          cpuUsage: 8
        },
        {
          name: 'ai_service',
          displayName: 'خدمة الذكاء الاصطناعي',
          description: 'خدمة معالجة نماذج الذكاء الاصطناعي',
          icon: 'fas fa-brain',
          status: 'running',
          uptime: '2 أيام 8 ساعات',
          memoryUsage: 1024,
          cpuUsage: 35
        },
        {
          name: 'redis',
          displayName: 'Redis Cache',
          description: 'خادم التخزين المؤقت',
          icon: 'fas fa-memory',
          status: 'running',
          uptime: '5 أيام 12 ساعة',
          memoryUsage: 128,
          cpuUsage: 2
        },
        {
          name: 'nginx',
          displayName: 'خادم الويب',
          description: 'خادم Nginx للواجهة الأمامية',
          icon: 'fas fa-globe',
          status: 'running',
          uptime: '5 أيام 12 ساعة',
          memoryUsage: 64,
          cpuUsage: 5
        },
        {
          name: 'backup_service',
          displayName: 'خدمة النسخ الاحتياطي',
          description: 'خدمة النسخ الاحتياطي التلقائي',
          icon: 'fas fa-archive',
          status: 'warning',
          uptime: '1 يوم 4 ساعات',
          memoryUsage: 32,
          cpuUsage: 1
        }
      ],
      
      logs: [
        {
          id: 1,
          timestamp: new Date(Date.now() - 5 * 60 * 1000),
          level: 'info',
          service: 'API Server',
          message: 'تم بدء تشغيل الخادم بنجاح على المنفذ 8000'
        },
        {
          id: 2,
          timestamp: new Date(Date.now() - 10 * 60 * 1000),
          level: 'warning',
          service: 'AI Service',
          message: 'استخدام الذاكرة مرتفع: 85%'
        },
        {
          id: 3,
          timestamp: new Date(Date.now() - 15 * 60 * 1000),
          level: 'error',
          service: 'Database',
          message: 'فشل في الاتصال بقاعدة البيانات، محاولة إعادة الاتصال...'
        },
        {
          id: 4,
          timestamp: new Date(Date.now() - 20 * 60 * 1000),
          level: 'info',
          service: 'Backup Service',
          message: 'تم إنشاء نسخة احتياطية بنجاح'
        },
        {
          id: 5,
          timestamp: new Date(Date.now() - 25 * 60 * 1000),
          level: 'debug',
          service: 'Redis',
          message: 'تم مسح ذاكرة التخزين المؤقت'
        }
      ],
      
      filteredLogs: [],
      
      alerts: [
        {
          id: 1,
          severity: 'warning',
          title: 'استخدام مرتفع للذاكرة',
          message: 'استخدام الذاكرة وصل إلى 85% من السعة الإجمالية',
          timestamp: new Date(Date.now() - 30 * 60 * 1000)
        },
        {
          id: 2,
          severity: 'info',
          title: 'تحديث النظام متاح',
          message: 'يتوفر تحديث جديد للنظام، يُنصح بتطبيقه',
          timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000)
        }
      ],
      
      charts: {
        cpu: null,
        memory: null,
        network: null,
        disk: null
      }
    }
  },
  
  mounted() {
    this.filteredLogs = [...this.logs]
    this.initializeCharts()
    this.startRealTimeUpdates()
  },
  
  beforeUnmount() {
    if (this.updateInterval) {
      clearInterval(this.updateInterval)
    }
  },
  
  methods: {
    async refreshData() {
      this.refreshing = true
      
      try {
        // محاكاة تحديث البيانات
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // تحديث المقاييس
        this.systemMetrics.cpu = Math.floor(Math.random() * 100)
        this.systemMetrics.memory = Math.floor(Math.random() * 100)
        this.systemMetrics.disk = Math.floor(Math.random() * 100)
        this.systemMetrics.network = (Math.random() * 50).toFixed(1)
        
        this.lastUpdate = new Date()
        this.updateCharts()
        
        this.$toast.success('تم تحديث البيانات بنجاح')
      } catch (error) {
        this.$toast.error('فشل في تحديث البيانات')
      } finally {
        this.refreshing = false
      }
    },
    
    async exportReport() {
      try {
        // محاكاة تصدير التقرير
        const reportData = {
          timestamp: new Date().toISOString(),
          systemMetrics: this.systemMetrics,
          services: this.services,
          alerts: this.alerts
        }
        
        const blob = new Blob([JSON.stringify(reportData, null, 2)], {
          type: 'application/json'
        })
        
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `system_report_${new Date().toISOString().split('T')[0]}.json`
        a.click()
        window.URL.revokeObjectURL(url)
        
        this.$toast.success('تم تصدير التقرير بنجاح')
      } catch (error) {
        this.$toast.error('فشل في تصدير التقرير')
      }
    },
    
    async startService(service) {
      try {
        // محاكاة بدء تشغيل الخدمة
        await new Promise(resolve => setTimeout(resolve, 1000))
        service.status = 'running'
        this.$toast.success(`تم تشغيل ${service.displayName} بنجاح`)
      } catch (error) {
        this.$toast.error(`فشل في تشغيل ${service.displayName}`)
      }
    },
    
    async stopService(service) {
      if (confirm(`هل أنت متأكد من إيقاف ${service.displayName}؟`)) {
        try {
          await new Promise(resolve => setTimeout(resolve, 1000))
          service.status = 'stopped'
          this.$toast.success(`تم إيقاف ${service.displayName} بنجاح`)
        } catch (error) {
          this.$toast.error(`فشل في إيقاف ${service.displayName}`)
        }
      }
    },
    
    async restartService(service) {
      try {
        await new Promise(resolve => setTimeout(resolve, 2000))
        service.status = 'running'
        this.$toast.success(`تم إعادة تشغيل ${service.displayName} بنجاح`)
      } catch (error) {
        this.$toast.error(`فشل في إعادة تشغيل ${service.displayName}`)
      }
    },
    
    async restartAllServices() {
      if (confirm('هل أنت متأكد من إعادة تشغيل جميع الخدمات؟')) {
        try {
          for (const service of this.services) {
            if (service.status === 'running') {
              await this.restartService(service)
            }
          }
          this.$toast.success('تم إعادة تشغيل جميع الخدمات بنجاح')
        } catch (error) {
          this.$toast.error('فشل في إعادة تشغيل بعض الخدمات')
        }
      }
    },
    
    filterLogs() {
      if (this.selectedLogLevel) {
        this.filteredLogs = this.logs.filter(log => log.level === this.selectedLogLevel)
      } else {
        this.filteredLogs = [...this.logs]
      }
    },
    
    clearLogs() {
      if (confirm('هل أنت متأكد من مسح جميع السجلات؟')) {
        this.logs = []
        this.filteredLogs = []
        this.$toast.success('تم مسح السجلات بنجاح')
      }
    },
    
    dismissAlert(alertId) {
      this.alerts = this.alerts.filter(alert => alert.id !== alertId)
    },
    
    dismissAllAlerts() {
      this.alerts = []
      this.$toast.success('تم إغلاق جميع التنبيهات')
    },
    
    initializeCharts() {
      // محاكاة إنشاء المخططات
      // في التطبيق الحقيقي، سيتم استخدام مكتبة مثل Chart.js
      console.log('تم تهيئة المخططات')
    },
    
    updateCharts() {
      // محاكاة تحديث المخططات
      console.log('تم تحديث المخططات للفترة:', this.chartTimeRange)
    },
    
    startRealTimeUpdates() {
      this.updateInterval = setInterval(() => {
        // تحديث المقاييس كل 30 ثانية
        this.systemMetrics.cpu = Math.max(0, Math.min(100, 
          this.systemMetrics.cpu + (Math.random() - 0.5) * 10))
        this.systemMetrics.memory = Math.max(0, Math.min(100, 
          this.systemMetrics.memory + (Math.random() - 0.5) * 5))
        this.systemMetrics.network = Math.max(0, 
          this.systemMetrics.network + (Math.random() - 0.5) * 5).toFixed(1)
        
        this.lastUpdate = new Date()
      }, 30000)
    },
    
    getStatusIcon(status) {
      const icons = {
        healthy: 'fas fa-check-circle',
        warning: 'fas fa-exclamation-triangle',
        critical: 'fas fa-times-circle'
      }
      return icons[status] || 'fas fa-question-circle'
    },
    
    getStatusText(status) {
      const texts = {
        healthy: 'النظام يعمل بشكل طبيعي',
        warning: 'يوجد تحذيرات تحتاج انتباه',
        critical: 'يوجد مشاكل حرجة تحتاج تدخل فوري'
      }
      return texts[status] || 'حالة غير معروفة'
    },
    
    getServiceStatusText(status) {
      const texts = {
        running: 'يعمل',
        stopped: 'متوقف',
        warning: 'تحذير',
        error: 'خطأ'
      }
      return texts[status] || status
    },
    
    getAlertIcon(severity) {
      const icons = {
        info: 'fas fa-info-circle',
        warning: 'fas fa-exclamation-triangle',
        error: 'fas fa-times-circle',
        critical: 'fas fa-skull-crossbones'
      }
      return icons[severity] || 'fas fa-bell'
    },
    
    formatTime(date) {
      return new Date(date).toLocaleString('ar-SA', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.system-monitoring-page {
  padding: 2rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2E7D32;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.page-description {
  color: #666;
  margin: 0.5rem 0 0 0;
  font-size: 1.1rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.status-overview {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.status-card {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  border-left: 5px solid;
}

.status-card.healthy {
  border-left-color: #28a745;
}

.status-card.warning {
  border-left-color: #ffc107;
}

.status-card.critical {
  border-left-color: #dc3545;
}

.status-icon {
  font-size: 3rem;
  color: #2E7D32;
}

.status-card.warning .status-icon {
  color: #ffc107;
}

.status-card.critical .status-icon {
  color: #dc3545;
}

.status-info h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 1.5rem;
}

.status-info p {
  margin: 0 0 0.5rem 0;
  color: #666;
  font-size: 1.1rem;
}

.status-info small {
  color: #999;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.metric-card {
  background: white;
  padding: 1.5rem;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.metric-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.metric-icon.cpu {
  background: linear-gradient(135deg, #007bff, #0056b3);
}

.metric-icon.memory {
  background: linear-gradient(135deg, #28a745, #1e7e34);
}

.metric-icon.disk {
  background: linear-gradient(135deg, #ffc107, #e0a800);
}

.metric-icon.network {
  background: linear-gradient(135deg, #17a2b8, #117a8b);
}

.metric-info {
  flex: 1;
}

.metric-info h4 {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 1rem;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2E7D32;
  margin-bottom: 0.5rem;
}

.metric-bar {
  width: 100%;
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.metric-fill {
  height: 100%;
  background: linear-gradient(90deg, #28a745, #20c997);
  transition: width 0.3s ease;
}

.metric-status {
  font-size: 0.9rem;
  color: #666;
}

.services-section,
.charts-section,
.logs-section,
.alerts-section {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
  overflow: hidden;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.section-header h2 {
  margin: 0;
  color: #2E7D32;
  font-size: 1.5rem;
}

.section-actions,
.chart-controls,
.log-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  padding: 1.5rem;
}

.service-card {
  border: 2px solid #e9ecef;
  border-radius: 10px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.service-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

.service-card.running {
  border-color: #28a745;
  background: rgba(40, 167, 69, 0.05);
}

.service-card.warning {
  border-color: #ffc107;
  background: rgba(255, 193, 7, 0.05);
}

.service-card.stopped {
  border-color: #dc3545;
  background: rgba(220, 53, 69, 0.05);
}

.service-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.service-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2E7D32, #4CAF50);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.service-info {
  flex: 1;
}

.service-info h4 {
  margin: 0 0 0.25rem 0;
  color: #333;
}

.service-info p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-badge.running {
  background: #d4edda;
  color: #155724;
}

.status-badge.warning {
  background: #fff3cd;
  color: #856404;
}

.status-badge.stopped {
  background: #f8d7da;
  color: #721c24;
}

.service-metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.metric {
  text-align: center;
}

.metric label {
  display: block;
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.metric span {
  font-weight: 600;
  color: #333;
}

.service-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  padding: 1.5rem;
}

.chart-container {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 1.5rem;
}

.chart-container h3 {
  margin: 0 0 1rem 0;
  color: #333;
  font-size: 1.1rem;
  text-align: center;
}

.chart {
  width: 100%;
  height: 200px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.logs-container {
  max-height: 400px;
  overflow-y: auto;
  padding: 1rem;
}

.log-entry {
  display: grid;
  grid-template-columns: 120px 80px 120px 1fr;
  gap: 1rem;
  padding: 0.75rem;
  border-bottom: 1px solid #f0f0f0;
  align-items: center;
}

.log-entry:hover {
  background: #f8f9fa;
}

.log-time {
  font-size: 0.85rem;
  color: #666;
}

.level-badge {
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
  font-size: 0.7rem;
  font-weight: 600;
  text-align: center;
}

.level-badge.error {
  background: #f8d7da;
  color: #721c24;
}

.level-badge.warning {
  background: #fff3cd;
  color: #856404;
}

.level-badge.info {
  background: #d1ecf1;
  color: #0c5460;
}

.level-badge.debug {
  background: #e2e3e5;
  color: #383d41;
}

.log-service {
  font-weight: 600;
  color: #2E7D32;
  font-size: 0.9rem;
}

.log-message {
  color: #333;
}

.alerts-list {
  padding: 1rem;
}

.alert-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 10px;
  margin-bottom: 1rem;
  border-left: 4px solid;
}

.alert-item.info {
  background: #d1ecf1;
  border-left-color: #17a2b8;
}

.alert-item.warning {
  background: #fff3cd;
  border-left-color: #ffc107;
}

.alert-item.error {
  background: #f8d7da;
  border-left-color: #dc3545;
}

.alert-item.critical {
  background: #f5c6cb;
  border-left-color: #721c24;
}

.alert-icon {
  font-size: 1.5rem;
  color: #17a2b8;
}

.alert-item.warning .alert-icon {
  color: #ffc107;
}

.alert-item.error .alert-icon,
.alert-item.critical .alert-icon {
  color: #dc3545;
}

.alert-content {
  flex: 1;
}

.alert-content h4 {
  margin: 0 0 0.25rem 0;
  color: #333;
}

.alert-content p {
  margin: 0 0 0.25rem 0;
  color: #666;
}

.alert-content small {
  color: #999;
}

.alert-dismiss {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #666;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.alert-dismiss:hover {
  background: rgba(0,0,0,0.1);
  color: #333;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}

.btn-primary {
  background: linear-gradient(135deg, #2E7D32, #4CAF50);
  color: white;
}

.btn-outline-primary {
  background: transparent;
  color: #2E7D32;
  border: 2px solid #2E7D32;
}

.btn-outline-secondary {
  background: transparent;
  color: #6c757d;
  border: 2px solid #6c757d;
}

.btn-outline-danger {
  background: transparent;
  color: #dc3545;
  border: 2px solid #dc3545;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-warning {
  background: #ffc107;
  color: #000;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.form-control {
  padding: 0.5rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  min-width: 120px;
}

.fa-spin {
  animation: fa-spin 1s infinite linear;
}

@keyframes fa-spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 1200px) {
  .status-overview {
    grid-template-columns: 1fr;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .system-monitoring-page {
    padding: 1rem;
  }
  
  .page-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .services-grid {
    grid-template-columns: 1fr;
  }
  
  .service-metrics {
    grid-template-columns: 1fr;
  }
  
  .service-actions {
    flex-direction: column;
  }
  
  .log-entry {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .alert-item {
    flex-direction: column;
    text-align: center;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>

