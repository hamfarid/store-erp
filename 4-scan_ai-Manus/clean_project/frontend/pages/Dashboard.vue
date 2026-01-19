<!-- صفحة لوحة التحكم الرئيسية -->
<template>
  <div class="dashboard-page">
    <!-- إحصائيات سريعة -->
    <div class="row mb-4">
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-primary shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                  إجمالي التشخيصات
                </div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  {{ dashboardStats.total_diagnoses || 0 }}
                </div>
              </div>
              <div class="col-auto">
                <i class="fas fa-stethoscope fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-success shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                  المستخدمين النشطين
                </div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  {{ dashboardStats.active_users || 0 }}
                </div>
              </div>
              <div class="col-auto">
                <i class="fas fa-users fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-info shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
                  استخدام الذكاء الاصطناعي
                </div>
                <div class="row no-gutters align-items-center">
                  <div class="col-auto">
                    <div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">
                      {{ dashboardStats.ai_usage_percentage || 0 }}%
                    </div>
                  </div>
                  <div class="col">
                    <div class="progress progress-sm mr-2">
                      <div class="progress-bar bg-info" role="progressbar"
                           :style="{ width: (dashboardStats.ai_usage_percentage || 0) + '%' }">
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-auto">
                <i class="fas fa-brain fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-warning shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                  الحاويات النشطة
                </div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  {{ dashboardStats.active_containers || 0 }}
                </div>
              </div>
              <div class="col-auto">
                <i class="fab fa-docker fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- الرسوم البيانية والتحليلات -->
    <div class="row">
      <!-- رسم بياني للتشخيصات -->
      <div class="col-xl-8 col-lg-7">
        <div class="card shadow mb-4">
          <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h6 class="m-0 font-weight-bold text-primary">إحصائيات التشخيص الشهرية</h6>
            <div class="dropdown no-arrow">
              <a class="dropdown-toggle" href="#" role="button" data-toggle="dropdown">
                <i class="fas fa-ellipsis-v fa-sm fa-fw text-gray-400"></i>
              </a>
              <div class="dropdown-menu dropdown-menu-right shadow">
                <a class="dropdown-item" href="#" @click="exportChart('diagnosis')">تصدير البيانات</a>
                <a class="dropdown-item" href="#" @click="refreshChart('diagnosis')">تحديث</a>
              </div>
            </div>
          </div>
          <div class="card-body">
            <canvas id="diagnosisChart" ref="diagnosisChart"></canvas>
          </div>
        </div>
      </div>

      <!-- صحة النظام -->
      <div class="col-xl-4 col-lg-5">
        <div class="card shadow mb-4">
          <div class="card-header py-3">
            <h6 class="m-0 font-weight-bold text-primary">صحة النظام</h6>
          </div>
          <div class="card-body">
            <div class="system-health-item" v-for="service in systemHealth" :key="service.name">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <div class="service-info">
                  <div class="service-name">{{ service.name }}</div>
                  <div class="service-status" :class="service.status">
                    <i class="fas fa-circle me-1"></i>
                    {{ getStatusText(service.status) }}
                  </div>
                </div>
                <div class="service-metrics">
                  <div class="metric">
                    <small>CPU: {{ service.cpu }}%</small>
                  </div>
                  <div class="metric">
                    <small>RAM: {{ service.memory }}%</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- الأنشطة الحديثة -->
    <div class="row">
      <div class="col-lg-6 mb-4">
        <div class="card shadow">
          <div class="card-header py-3">
            <h6 class="m-0 font-weight-bold text-primary">الأنشطة الحديثة</h6>
          </div>
          <div class="card-body">
            <div class="activity-item" v-for="activity in recentActivities" :key="activity.id">
              <div class="d-flex align-items-center mb-3">
                <div class="activity-icon me-3">
                  <i :class="getActivityIcon(activity.type)" :style="{ color: getActivityColor(activity.type) }"></i>
                </div>
                <div class="activity-content flex-grow-1">
                  <div class="activity-title">{{ activity.title }}</div>
                  <div class="activity-description">{{ activity.description }}</div>
                  <div class="activity-time">{{ formatTime(activity.timestamp) }}</div>
                </div>
              </div>
            </div>
            
            <div class="text-center mt-3">
              <router-link to="/data/activity-log" class="btn btn-primary btn-sm">
                عرض جميع الأنشطة
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- الإجراءات السريعة -->
      <div class="col-lg-6 mb-4">
        <div class="card shadow">
          <div class="card-header py-3">
            <h6 class="m-0 font-weight-bold text-primary">الإجراءات السريعة</h6>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-6 mb-3">
                <button class="btn btn-outline-primary w-100" @click="navigateTo('/diagnosis/dashboard')">
                  <i class="fas fa-stethoscope mb-2"></i>
                  <br>تشخيص جديد
                </button>
              </div>
              <div class="col-6 mb-3">
                <button class="btn btn-outline-success w-100" @click="navigateTo('/ai/agent')">
                  <i class="fas fa-robot mb-2"></i>
                  <br>المساعد الذكي
                </button>
              </div>
              <div class="col-6 mb-3">
                <button class="btn btn-outline-info w-100" @click="navigateTo('/diagnosis/image-enhancement')">
                  <i class="fas fa-image mb-2"></i>
                  <br>تحسين الصور
                </button>
              </div>
              <div class="col-6 mb-3">
                <button class="btn btn-outline-warning w-100" @click="navigateTo('/docker/management')">
                  <i class="fab fa-docker mb-2"></i>
                  <br>إدارة الحاويات
                </button>
              </div>
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
import { useDataStore, useSystemStore } from '../store/index.js'
import { dashboardAPI } from '../services/api.js'
import Chart from 'chart.js/auto'

export default {
  name: 'Dashboard',
  
  setup() {
    const router = useRouter()
    const dataStore = useDataStore()
    const systemStore = useSystemStore()
    
    const diagnosisChart = ref(null)
    let chartInstance = null
    
    // البيانات المحسوبة
    const dashboardStats = computed(() => dataStore.dashboardStats)
    const recentActivities = computed(() => dataStore.recentActivities)
    const systemHealth = computed(() => dataStore.systemHealth)
    
    // الوظائف
    const navigateTo = (path) => {
      router.push(path)
    }
    
    const getStatusText = (status) => {
      const statusMap = {
        'healthy': 'سليم',
        'warning': 'تحذير',
        'error': 'خطأ',
        'offline': 'غير متصل'
      }
      return statusMap[status] || 'غير معروف'
    }
    
    const getActivityIcon = (type) => {
      const iconMap = {
        'diagnosis': 'fas fa-stethoscope',
        'ai_chat': 'fas fa-robot',
        'user_login': 'fas fa-sign-in-alt',
        'system_update': 'fas fa-sync-alt',
        'backup': 'fas fa-database',
        'error': 'fas fa-exclamation-triangle'
      }
      return iconMap[type] || 'fas fa-info-circle'
    }
    
    const getActivityColor = (type) => {
      const colorMap = {
        'diagnosis': '#4e73df',
        'ai_chat': '#1cc88a',
        'user_login': '#36b9cc',
        'system_update': '#f6c23e',
        'backup': '#858796',
        'error': '#e74a3b'
      }
      return colorMap[type] || '#858796'
    }
    
    const formatTime = (timestamp) => {
      const date = new Date(timestamp)
      const now = new Date()
      const diff = now - date
      
      if (diff < 60000) return 'الآن'
      if (diff < 3600000) return `${Math.floor(diff / 60000)} دقيقة`
      if (diff < 86400000) return `${Math.floor(diff / 3600000)} ساعة`
      return date.toLocaleDateString('ar-SA')
    }
    
    const initChart = async () => {
      try {
        const response = await dashboardAPI.getChartData('diagnosis')
        const data = response.data
        
        const ctx = diagnosisChart.value.getContext('2d')
        chartInstance = new Chart(ctx, {
          type: 'line',
          data: {
            labels: data.labels,
            datasets: [{
              label: 'التشخيصات',
              data: data.values,
              borderColor: '#4e73df',
              backgroundColor: 'rgba(78, 115, 223, 0.1)',
              borderWidth: 2,
              fill: true,
              tension: 0.3
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false
              }
            },
            scales: {
              y: {
                beginAtZero: true,
                grid: {
                  color: 'rgba(0, 0, 0, 0.1)'
                }
              },
              x: {
                grid: {
                  display: false
                }
              }
            }
          }
        })
      } catch (error) {
        console.error('خطأ في تحميل بيانات الرسم البياني:', error)
      }
    }
    
    const refreshChart = async (type) => {
      if (chartInstance) {
        chartInstance.destroy()
      }
      await initChart()
      
      systemStore.addNotification({
        type: 'success',
        title: 'تم التحديث',
        message: 'تم تحديث الرسم البياني بنجاح'
      })
    }
    
    const exportChart = (type) => {
      // تصدير بيانات الرسم البياني
      systemStore.addNotification({
        type: 'info',
        title: 'جاري التصدير',
        message: 'سيتم تحميل الملف قريباً'
      })
    }
    
    // تحميل البيانات عند التحميل
    onMounted(async () => {
      await dataStore.fetchDashboardData()
      await initChart()
    })
    
    return {
      dashboardStats,
      recentActivities,
      systemHealth,
      diagnosisChart,
      navigateTo,
      getStatusText,
      getActivityIcon,
      getActivityColor,
      formatTime,
      refreshChart,
      exportChart
    }
  }
}
</script>

<style scoped>
.dashboard-page {
  padding: 20px;
}

.border-left-primary {
  border-left: 4px solid #4e73df !important;
}

.border-left-success {
  border-left: 4px solid #1cc88a !important;
}

.border-left-info {
  border-left: 4px solid #36b9cc !important;
}

.border-left-warning {
  border-left: 4px solid #f6c23e !important;
}

.system-health-item {
  border-bottom: 1px solid #e3e6f0;
  padding-bottom: 15px;
}

.system-health-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.service-name {
  font-weight: 600;
  color: #5a5c69;
}

.service-status {
  font-size: 0.8rem;
  margin-top: 2px;
}

.service-status.healthy {
  color: #1cc88a;
}

.service-status.warning {
  color: #f6c23e;
}

.service-status.error {
  color: #e74a3b;
}

.service-status.offline {
  color: #858796;
}

.metric {
  font-size: 0.75rem;
  color: #858796;
}

.activity-item {
  border-bottom: 1px solid #e3e6f0;
  padding-bottom: 15px;
}

.activity-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #f8f9fc;
  display: flex;
  align-items: center;
  justify-content: center;
}

.activity-title {
  font-weight: 600;
  color: #5a5c69;
  margin-bottom: 2px;
}

.activity-description {
  font-size: 0.85rem;
  color: #858796;
  margin-bottom: 2px;
}

.activity-time {
  font-size: 0.75rem;
  color: #858796;
}

.btn i {
  font-size: 1.5rem;
}

#diagnosisChart {
  height: 300px;
}
</style>

