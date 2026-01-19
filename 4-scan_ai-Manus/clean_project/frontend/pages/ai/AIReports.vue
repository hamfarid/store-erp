<!-- صفحة تقارير الذكاء الاصطناعي -->
<template>
  <div class="ai-reports-page">
    <!-- Header -->
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h1 class="page-title">
            <i class="fas fa-chart-line me-3"></i>
            تقارير الذكاء الاصطناعي
          </h1>
          <p class="page-subtitle">تقارير شاملة حول أداء واستخدام نماذج الذكاء الاصطناعي</p>
        </div>
        <div class="page-actions">
          <button class="btn btn-outline-primary" @click="refreshReports">
            <i class="fas fa-sync-alt me-2"></i>
            تحديث التقارير
          </button>
          <button class="btn btn-success" @click="exportAllReports">
            <i class="fas fa-download me-2"></i>
            تصدير جميع التقارير
          </button>
        </div>
      </div>
    </div>

    <!-- فلاتر التقارير -->
    <div class="filters-section">
      <div class="card">
        <div class="card-body">
          <div class="row">
            <div class="col-md-3">
              <label class="form-label">الفترة الزمنية</label>
              <select class="form-select" v-model="filters.period">
                <option value="today">اليوم</option>
                <option value="week">هذا الأسبوع</option>
                <option value="month">هذا الشهر</option>
                <option value="quarter">هذا الربع</option>
                <option value="year">هذا العام</option>
                <option value="custom">فترة مخصصة</option>
              </select>
            </div>
            
            <div class="col-md-3" v-if="filters.period === 'custom'">
              <label class="form-label">من تاريخ</label>
              <input type="date" class="form-control" v-model="filters.start_date">
            </div>
            
            <div class="col-md-3" v-if="filters.period === 'custom'">
              <label class="form-label">إلى تاريخ</label>
              <input type="date" class="form-control" v-model="filters.end_date">
            </div>
            
            <div class="col-md-3">
              <label class="form-label">نوع النموذج</label>
              <select class="form-select" v-model="filters.model_type">
                <option value="">جميع النماذج</option>
                <option value="classification">تصنيف</option>
                <option value="detection">كشف</option>
                <option value="segmentation">تقسيم</option>
                <option value="nlp">معالجة اللغة</option>
                <option value="recommendation">توصيات</option>
              </select>
            </div>
            
            <div class="col-md-3">
              <label class="form-label">الخدمة</label>
              <select class="form-select" v-model="filters.service">
                <option value="">جميع الخدمات</option>
                <option value="diagnosis">التشخيص</option>
                <option value="image_enhancement">تحسين الصور</option>
                <option value="plant_hybridization">تهجين النباتات</option>
                <option value="yolo_detection">كشف YOLO</option>
                <option value="ai_agent">المساعد الذكي</option>
              </select>
            </div>
          </div>
          
          <div class="row mt-3">
            <div class="col-12">
              <button class="btn btn-primary" @click="applyFilters">
                <i class="fas fa-filter me-2"></i>
                تطبيق الفلاتر
              </button>
              <button class="btn btn-outline-secondary ms-2" @click="resetFilters">
                <i class="fas fa-undo me-2"></i>
                إعادة تعيين
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- إحصائيات سريعة -->
    <div class="row mb-4">
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card primary">
          <div class="stat-icon">
            <i class="fas fa-chart-bar"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ reportStats.total_requests || 0 }}</div>
            <div class="stat-label">إجمالي الطلبات</div>
            <div class="stat-change positive">
              <i class="fas fa-arrow-up"></i>
              +{{ reportStats.requests_growth || 0 }}%
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card success">
          <div class="stat-icon">
            <i class="fas fa-check-circle"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ reportStats.success_rate || 0 }}%</div>
            <div class="stat-label">معدل النجاح</div>
            <div class="stat-change positive">
              <i class="fas fa-arrow-up"></i>
              +{{ reportStats.success_growth || 0 }}%
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card info">
          <div class="stat-icon">
            <i class="fas fa-clock"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ reportStats.avg_response_time || 0 }}ms</div>
            <div class="stat-label">متوسط وقت الاستجابة</div>
            <div class="stat-change negative">
              <i class="fas fa-arrow-down"></i>
              -{{ reportStats.response_improvement || 0 }}%
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card warning">
          <div class="stat-icon">
            <i class="fas fa-users"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ reportStats.active_users || 0 }}</div>
            <div class="stat-label">المستخدمين النشطين</div>
            <div class="stat-change positive">
              <i class="fas fa-arrow-up"></i>
              +{{ reportStats.users_growth || 0 }}%
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- التقارير الرئيسية -->
    <div class="row">
      <!-- تقرير الاستخدام -->
      <div class="col-lg-8 mb-4">
        <div class="card">
          <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">
                <i class="fas fa-chart-area me-2"></i>
                تقرير الاستخدام
              </h5>
              <div class="card-actions">
                <button class="btn btn-sm btn-outline-primary" @click="exportChart('usage')">
                  <i class="fas fa-download"></i>
                </button>
              </div>
            </div>
          </div>
          <div class="card-body">
            <canvas id="usageChart" ref="usageChart"></canvas>
          </div>
        </div>
      </div>
      
      <!-- أداء النماذج -->
      <div class="col-lg-4 mb-4">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="fas fa-tachometer-alt me-2"></i>
              أداء النماذج
            </h5>
          </div>
          <div class="card-body">
            <div class="model-performance-item" v-for="model in modelPerformance" :key="model.id">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <div class="model-info">
                  <div class="model-name">{{ model.name }}</div>
                  <div class="model-type">{{ model.type }}</div>
                </div>
                <div class="model-score">
                  <div class="score-value" :class="getScoreClass(model.score)">
                    {{ model.score }}%
                  </div>
                </div>
              </div>
              
              <div class="progress mb-2">
                <div class="progress-bar" 
                     :class="getScoreClass(model.score)"
                     :style="{ width: model.score + '%' }">
                </div>
              </div>
              
              <div class="model-metrics">
                <small class="text-muted">
                  الطلبات: {{ model.requests }} | الأخطاء: {{ model.errors }}
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- تقارير تفصيلية -->
    <div class="row">
      <!-- تقرير الأخطاء -->
      <div class="col-lg-6 mb-4">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="fas fa-exclamation-triangle me-2"></i>
              تقرير الأخطاء
            </h5>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-sm">
                <thead>
                  <tr>
                    <th>نوع الخطأ</th>
                    <th>العدد</th>
                    <th>النسبة</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="error in errorReport" :key="error.type">
                    <td>{{ error.type }}</td>
                    <td>{{ error.count }}</td>
                    <td>
                      <span class="badge bg-danger">{{ error.percentage }}%</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      
      <!-- تقرير المستخدمين -->
      <div class="col-lg-6 mb-4">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="fas fa-users me-2"></i>
              تقرير المستخدمين
            </h5>
          </div>
          <div class="card-body">
            <canvas id="usersChart" ref="usersChart"></canvas>
          </div>
        </div>
      </div>
    </div>

    <!-- تقرير الخدمات -->
    <div class="row">
      <div class="col-12 mb-4">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="fas fa-cogs me-2"></i>
              تقرير الخدمات
            </h5>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>الخدمة</th>
                    <th>الطلبات</th>
                    <th>النجاح</th>
                    <th>الفشل</th>
                    <th>متوسط الوقت</th>
                    <th>الحالة</th>
                    <th>الإجراءات</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="service in servicesReport" :key="service.id">
                    <td>
                      <div class="d-flex align-items-center">
                        <i :class="service.icon" class="me-2"></i>
                        {{ service.name }}
                      </div>
                    </td>
                    <td>{{ service.total_requests }}</td>
                    <td>
                      <span class="badge bg-success">{{ service.success_count }}</span>
                    </td>
                    <td>
                      <span class="badge bg-danger">{{ service.error_count }}</span>
                    </td>
                    <td>{{ service.avg_response_time }}ms</td>
                    <td>
                      <span class="badge" :class="getServiceStatusClass(service.status)">
                        {{ getServiceStatusText(service.status) }}
                      </span>
                    </td>
                    <td>
                      <button class="btn btn-sm btn-outline-info" @click="viewServiceDetails(service)">
                        <i class="fas fa-eye"></i>
                      </button>
                      <button class="btn btn-sm btn-outline-primary" @click="exportServiceReport(service)">
                        <i class="fas fa-download"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAIStore, useSystemStore } from '../../store/index.js'
import { aiReportsAPI } from '../../services/api.js'
import Chart from 'chart.js/auto'

export default {
  name: 'AIReports',
  
  setup() {
    const router = useRouter()
    const aiStore = useAIStore()
    const systemStore = useSystemStore()
    
    const usageChart = ref(null)
    const usersChart = ref(null)
    let usageChartInstance = null
    let usersChartInstance = null
    
    // الفلاتر
    const filters = ref({
      period: 'month',
      start_date: '',
      end_date: '',
      model_type: '',
      service: ''
    })
    
    // البيانات المحسوبة
    const reportStats = computed(() => aiStore.reportStats)
    const modelPerformance = computed(() => aiStore.modelPerformance)
    const errorReport = computed(() => aiStore.errorReport)
    const servicesReport = computed(() => aiStore.servicesReport)
    
    // الوظائف
    const refreshReports = async () => {
      try {
        await aiStore.fetchReportsData(filters.value)
        await initCharts()
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم التحديث',
          message: 'تم تحديث التقارير بنجاح'
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في التحديث',
          message: 'فشل في تحديث التقارير'
        })
      }
    }
    
    const applyFilters = async () => {
      await refreshReports()
    }
    
    const resetFilters = () => {
      filters.value = {
        period: 'month',
        start_date: '',
        end_date: '',
        model_type: '',
        service: ''
      }
      refreshReports()
    }
    
    const getScoreClass = (score) => {
      if (score >= 90) return 'bg-success'
      if (score >= 70) return 'bg-warning'
      return 'bg-danger'
    }
    
    const getServiceStatusClass = (status) => {
      const classes = {
        'active': 'bg-success',
        'warning': 'bg-warning',
        'error': 'bg-danger',
        'inactive': 'bg-secondary'
      }
      return classes[status] || 'bg-secondary'
    }
    
    const getServiceStatusText = (status) => {
      const texts = {
        'active': 'نشط',
        'warning': 'تحذير',
        'error': 'خطأ',
        'inactive': 'غير نشط'
      }
      return texts[status] || 'غير معروف'
    }
    
    const initCharts = async () => {
      try {
        // رسم بياني للاستخدام
        if (usageChartInstance) {
          usageChartInstance.destroy()
        }
        
        const usageData = await aiReportsAPI.getUsageChartData(filters.value)
        const usageCtx = usageChart.value.getContext('2d')
        
        usageChartInstance = new Chart(usageCtx, {
          type: 'line',
          data: {
            labels: usageData.data.labels,
            datasets: [
              {
                label: 'الطلبات الناجحة',
                data: usageData.data.success,
                borderColor: '#1cc88a',
                backgroundColor: 'rgba(28, 200, 138, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.3
              },
              {
                label: 'الطلبات الفاشلة',
                data: usageData.data.errors,
                borderColor: '#e74a3b',
                backgroundColor: 'rgba(231, 74, 59, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.3
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'top'
              }
            },
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        })
        
        // رسم بياني للمستخدمين
        if (usersChartInstance) {
          usersChartInstance.destroy()
        }
        
        const usersData = await aiReportsAPI.getUsersChartData(filters.value)
        const usersCtx = usersChart.value.getContext('2d')
        
        usersChartInstance = new Chart(usersCtx, {
          type: 'doughnut',
          data: {
            labels: usersData.data.labels,
            datasets: [{
              data: usersData.data.values,
              backgroundColor: [
                '#4e73df',
                '#1cc88a',
                '#36b9cc',
                '#f6c23e',
                '#e74a3b'
              ]
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'bottom'
              }
            }
          }
        })
        
      } catch (error) {
        console.error('خطأ في تحميل بيانات الرسوم البيانية:', error)
      }
    }
    
    const exportChart = (chartType) => {
      let canvas
      let filename
      
      if (chartType === 'usage') {
        canvas = usageChart.value
        filename = 'usage-chart'
      } else if (chartType === 'users') {
        canvas = usersChart.value
        filename = 'users-chart'
      }
      
      if (canvas) {
        const link = document.createElement('a')
        link.download = `${filename}-${new Date().toISOString().split('T')[0]}.png`
        link.href = canvas.toDataURL()
        link.click()
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم التصدير',
          message: 'تم تصدير الرسم البياني بنجاح'
        })
      }
    }
    
    const exportAllReports = async () => {
      try {
        const response = await aiReportsAPI.exportAllReports(filters.value)
        
        // تحميل الملف
        const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `ai-reports-${new Date().toISOString().split('T')[0]}.xlsx`
        link.click()
        window.URL.revokeObjectURL(url)
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم التصدير',
          message: 'تم تصدير جميع التقارير بنجاح'
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في التصدير',
          message: 'فشل في تصدير التقارير'
        })
      }
    }
    
    const viewServiceDetails = (service) => {
      router.push(`/ai/services/${service.id}/reports`)
    }
    
    const exportServiceReport = async (service) => {
      try {
        const response = await aiReportsAPI.exportServiceReport(service.id, filters.value)
        
        const blob = new Blob([response.data], { type: 'application/json' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `${service.name}-report-${new Date().toISOString().split('T')[0]}.json`
        link.click()
        window.URL.revokeObjectURL(url)
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم التصدير',
          message: `تم تصدير تقرير ${service.name} بنجاح`
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في التصدير',
          message: 'فشل في تصدير تقرير الخدمة'
        })
      }
    }
    
    // تحميل البيانات عند التحميل
    onMounted(async () => {
      await aiStore.fetchReportsData(filters.value)
      await initCharts()
    })
    
    return {
      filters,
      reportStats,
      modelPerformance,
      errorReport,
      servicesReport,
      usageChart,
      usersChart,
      refreshReports,
      applyFilters,
      resetFilters,
      getScoreClass,
      getServiceStatusClass,
      getServiceStatusText,
      exportChart,
      exportAllReports,
      viewServiceDetails,
      exportServiceReport
    }
  }
}
</script>

<style scoped>
.ai-reports-page {
  padding: 20px;
  font-family: 'Cairo', sans-serif;
}

.page-header {
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  color: #6c757d;
  margin-bottom: 0;
}

.filters-section {
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-left: 4px solid;
  display: flex;
  align-items: center;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-card.primary {
  border-left-color: #4e73df;
}

.stat-card.success {
  border-left-color: #1cc88a;
}

.stat-card.info {
  border-left-color: #36b9cc;
}

.stat-card.warning {
  border-left-color: #f6c23e;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 1rem;
  font-size: 1.5rem;
  color: white;
}

.stat-card.primary .stat-icon {
  background: linear-gradient(45deg, #4e73df, #224abe);
}

.stat-card.success .stat-icon {
  background: linear-gradient(45deg, #1cc88a, #13855c);
}

.stat-card.info .stat-icon {
  background: linear-gradient(45deg, #36b9cc, #258391);
}

.stat-card.warning .stat-icon {
  background: linear-gradient(45deg, #f6c23e, #d4a017);
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  line-height: 1;
}

.stat-label {
  color: #6c757d;
  font-size: 0.9rem;
  margin-top: 0.25rem;
}

.stat-change {
  font-size: 0.8rem;
  margin-top: 0.5rem;
}

.stat-change.positive {
  color: #1cc88a;
}

.stat-change.negative {
  color: #e74a3b;
}

.model-performance-item {
  border-bottom: 1px solid #e3e6f0;
  padding-bottom: 1rem;
  margin-bottom: 1rem;
}

.model-performance-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.model-name {
  font-weight: 600;
  color: #2c3e50;
}

.model-type {
  font-size: 0.8rem;
  color: #6c757d;
}

.score-value {
  font-size: 1.2rem;
  font-weight: 700;
  padding: 0.25rem 0.5rem;
  border-radius: 5px;
  color: white;
}

.model-metrics {
  margin-top: 0.5rem;
}

.card {
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border: none;
}

.card-header {
  background: white;
  border-bottom: 1px solid #e3e6f0;
  border-radius: 15px 15px 0 0 !important;
}

.card-title {
  font-weight: 600;
  color: #2c3e50;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

#usageChart,
#usersChart {
  height: 300px;
}

.table th {
  font-weight: 600;
  color: #2c3e50;
  border-top: none;
}

.table td {
  vertical-align: middle;
}

@media (max-width: 768px) {
  .page-header .d-flex {
    flex-direction: column;
    gap: 1rem;
  }
  
  .filters-section .row {
    margin-bottom: 1rem;
  }
  
  .stat-card {
    margin-bottom: 1rem;
  }
  
  .card-actions {
    flex-direction: column;
  }
  
  .table-responsive {
    font-size: 0.85rem;
  }
}
</style>

