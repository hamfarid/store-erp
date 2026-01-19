<!-- صفحة إدارة الذكاء الاصطناعي -->
<template>
  <div class="ai-management-page">
    <!-- Header -->
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h1 class="page-title">
            <i class="fas fa-brain me-3"></i>
            إدارة الذكاء الاصطناعي
          </h1>
          <p class="page-subtitle">إدارة وتكوين نماذج الذكاء الاصطناعي والخدمات المتقدمة</p>
        </div>
        <div class="page-actions">
          <button class="btn btn-primary" @click="refreshData">
            <i class="fas fa-sync-alt me-2"></i>
            تحديث البيانات
          </button>
        </div>
      </div>
    </div>

    <!-- إحصائيات سريعة -->
    <div class="row mb-4">
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card primary">
          <div class="stat-icon">
            <i class="fas fa-robot"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ aiStats.active_models || 0 }}</div>
            <div class="stat-label">النماذج النشطة</div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card success">
          <div class="stat-icon">
            <i class="fas fa-chart-line"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ aiStats.total_requests || 0 }}</div>
            <div class="stat-label">إجمالي الطلبات</div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card info">
          <div class="stat-icon">
            <i class="fas fa-clock"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ aiStats.avg_response_time || 0 }}ms</div>
            <div class="stat-label">متوسط وقت الاستجابة</div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card warning">
          <div class="stat-icon">
            <i class="fas fa-percentage"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ aiStats.accuracy_rate || 0 }}%</div>
            <div class="stat-label">معدل الدقة</div>
          </div>
        </div>
      </div>
    </div>

    <!-- علامات التبويب -->
    <div class="card">
      <div class="card-header">
        <ul class="nav nav-tabs card-header-tabs" role="tablist">
          <li class="nav-item">
            <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#models-tab">
              <i class="fas fa-cubes me-2"></i>
              النماذج
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link" data-bs-toggle="tab" data-bs-target="#services-tab">
              <i class="fas fa-cogs me-2"></i>
              الخدمات
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link" data-bs-toggle="tab" data-bs-target="#monitoring-tab">
              <i class="fas fa-chart-area me-2"></i>
              المراقبة
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link" data-bs-toggle="tab" data-bs-target="#settings-tab">
              <i class="fas fa-sliders-h me-2"></i>
              الإعدادات
            </button>
          </li>
        </ul>
      </div>
      
      <div class="card-body">
        <div class="tab-content">
          <!-- تبويب النماذج -->
          <div class="tab-pane fade show active" id="models-tab">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <h5>نماذج الذكاء الاصطناعي</h5>
              <button class="btn btn-success" @click="showAddModelModal">
                <i class="fas fa-plus me-2"></i>
                إضافة نموذج جديد
              </button>
            </div>
            
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>اسم النموذج</th>
                    <th>النوع</th>
                    <th>الحالة</th>
                    <th>الدقة</th>
                    <th>آخر تحديث</th>
                    <th>الإجراءات</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="model in aiModels" :key="model.id">
                    <td>
                      <div class="d-flex align-items-center">
                        <div class="model-icon me-3">
                          <i :class="getModelIcon(model.type)"></i>
                        </div>
                        <div>
                          <div class="fw-bold">{{ model.name }}</div>
                          <small class="text-muted">{{ model.description }}</small>
                        </div>
                      </div>
                    </td>
                    <td>
                      <span class="badge bg-info">{{ model.type }}</span>
                    </td>
                    <td>
                      <span class="badge" :class="getStatusClass(model.status)">
                        {{ getStatusText(model.status) }}
                      </span>
                    </td>
                    <td>{{ model.accuracy }}%</td>
                    <td>{{ formatDate(model.updated_at) }}</td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" @click="editModel(model)">
                          <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-outline-info" @click="testModel(model)">
                          <i class="fas fa-play"></i>
                        </button>
                        <button class="btn btn-outline-danger" @click="deleteModel(model)">
                          <i class="fas fa-trash"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <!-- تبويب الخدمات -->
          <div class="tab-pane fade" id="services-tab">
            <div class="row">
              <div class="col-md-6 mb-4" v-for="service in aiServices" :key="service.id">
                <div class="service-card">
                  <div class="service-header">
                    <div class="service-icon">
                      <i :class="service.icon"></i>
                    </div>
                    <div class="service-info">
                      <h6>{{ service.name }}</h6>
                      <p>{{ service.description }}</p>
                    </div>
                    <div class="service-status">
                      <span class="status-indicator" :class="service.status"></span>
                    </div>
                  </div>
                  
                  <div class="service-metrics">
                    <div class="metric">
                      <span class="metric-label">الطلبات اليوم:</span>
                      <span class="metric-value">{{ service.requests_today }}</span>
                    </div>
                    <div class="metric">
                      <span class="metric-label">وقت الاستجابة:</span>
                      <span class="metric-value">{{ service.response_time }}ms</span>
                    </div>
                  </div>
                  
                  <div class="service-actions">
                    <button class="btn btn-sm btn-outline-primary" @click="configureService(service)">
                      تكوين
                    </button>
                    <button class="btn btn-sm btn-outline-info" @click="viewServiceLogs(service)">
                      السجلات
                    </button>
                    <button class="btn btn-sm" 
                            :class="service.status === 'active' ? 'btn-outline-warning' : 'btn-outline-success'"
                            @click="toggleService(service)">
                      {{ service.status === 'active' ? 'إيقاف' : 'تشغيل' }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- تبويب المراقبة -->
          <div class="tab-pane fade" id="monitoring-tab">
            <div class="row">
              <div class="col-lg-8 mb-4">
                <div class="chart-container">
                  <h6>أداء النماذج - آخر 24 ساعة</h6>
                  <canvas id="performanceChart" ref="performanceChart"></canvas>
                </div>
              </div>
              
              <div class="col-lg-4 mb-4">
                <div class="alerts-container">
                  <h6>التنبيهات والإشعارات</h6>
                  <div class="alert-item" v-for="alert in alerts" :key="alert.id">
                    <div class="alert-icon" :class="alert.type">
                      <i :class="getAlertIcon(alert.type)"></i>
                    </div>
                    <div class="alert-content">
                      <div class="alert-title">{{ alert.title }}</div>
                      <div class="alert-message">{{ alert.message }}</div>
                      <div class="alert-time">{{ formatTime(alert.timestamp) }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- تبويب الإعدادات -->
          <div class="tab-pane fade" id="settings-tab">
            <div class="row">
              <div class="col-lg-6">
                <div class="settings-section">
                  <h6>إعدادات عامة</h6>
                  
                  <div class="setting-item">
                    <label class="form-label">الحد الأقصى للطلبات المتزامنة</label>
                    <input type="number" class="form-control" v-model="settings.max_concurrent_requests">
                  </div>
                  
                  <div class="setting-item">
                    <label class="form-label">مهلة الاستجابة (ثانية)</label>
                    <input type="number" class="form-control" v-model="settings.response_timeout">
                  </div>
                  
                  <div class="setting-item">
                    <label class="form-label">مستوى السجلات</label>
                    <select class="form-select" v-model="settings.log_level">
                      <option value="DEBUG">تفصيلي</option>
                      <option value="INFO">معلومات</option>
                      <option value="WARNING">تحذيرات</option>
                      <option value="ERROR">أخطاء</option>
                    </select>
                  </div>
                  
                  <div class="setting-item">
                    <div class="form-check">
                      <input class="form-check-input" type="checkbox" v-model="settings.auto_scaling">
                      <label class="form-check-label">التوسع التلقائي</label>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="col-lg-6">
                <div class="settings-section">
                  <h6>إعدادات الأمان</h6>
                  
                  <div class="setting-item">
                    <label class="form-label">مفتاح API</label>
                    <div class="input-group">
                      <input type="password" class="form-control" v-model="settings.api_key">
                      <button class="btn btn-outline-secondary" @click="generateApiKey">
                        توليد جديد
                      </button>
                    </div>
                  </div>
                  
                  <div class="setting-item">
                    <label class="form-label">عناوين IP المسموحة</label>
                    <textarea class="form-control" rows="3" v-model="settings.allowed_ips"
                              placeholder="192.168.1.1&#10;10.0.0.1"></textarea>
                  </div>
                  
                  <div class="setting-item">
                    <div class="form-check">
                      <input class="form-check-input" type="checkbox" v-model="settings.enable_rate_limiting">
                      <label class="form-check-label">تفعيل تحديد المعدل</label>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="settings-actions mt-4">
              <button class="btn btn-primary" @click="saveSettings">
                <i class="fas fa-save me-2"></i>
                حفظ الإعدادات
              </button>
              <button class="btn btn-outline-secondary" @click="resetSettings">
                <i class="fas fa-undo me-2"></i>
                إعادة تعيين
              </button>
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
import { aiManagementAPI } from '../../services/api.js'

export default {
  name: 'AIManagement',
  
  setup() {
    const router = useRouter()
    const aiStore = useAIStore()
    const systemStore = useSystemStore()
    
    // البيانات المحسوبة
    const aiStats = computed(() => aiStore.stats)
    const aiModels = computed(() => aiStore.models)
    const aiServices = computed(() => aiStore.services)
    const alerts = computed(() => aiStore.alerts)
    const settings = ref({
      max_concurrent_requests: 100,
      response_timeout: 30,
      log_level: 'INFO',
      auto_scaling: true,
      api_key: '',
      allowed_ips: '',
      enable_rate_limiting: true
    })
    
    // الوظائف
    const refreshData = async () => {
      try {
        await aiStore.fetchAllData()
        systemStore.addNotification({
          type: 'success',
          title: 'تم التحديث',
          message: 'تم تحديث بيانات الذكاء الاصطناعي بنجاح'
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في التحديث',
          message: 'فشل في تحديث البيانات'
        })
      }
    }
    
    const getModelIcon = (type) => {
      const icons = {
        'classification': 'fas fa-tags',
        'detection': 'fas fa-search',
        'segmentation': 'fas fa-puzzle-piece',
        'nlp': 'fas fa-language',
        'recommendation': 'fas fa-thumbs-up'
      }
      return icons[type] || 'fas fa-cube'
    }
    
    const getStatusClass = (status) => {
      const classes = {
        'active': 'bg-success',
        'inactive': 'bg-secondary',
        'training': 'bg-warning',
        'error': 'bg-danger'
      }
      return classes[status] || 'bg-secondary'
    }
    
    const getStatusText = (status) => {
      const texts = {
        'active': 'نشط',
        'inactive': 'غير نشط',
        'training': 'قيد التدريب',
        'error': 'خطأ'
      }
      return texts[status] || 'غير معروف'
    }
    
    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('ar-SA')
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
    
    const getAlertIcon = (type) => {
      const icons = {
        'info': 'fas fa-info-circle',
        'warning': 'fas fa-exclamation-triangle',
        'error': 'fas fa-times-circle',
        'success': 'fas fa-check-circle'
      }
      return icons[type] || 'fas fa-bell'
    }
    
    // وظائف النماذج
    const showAddModelModal = () => {
      // إظهار نافذة إضافة نموذج جديد
      systemStore.addNotification({
        type: 'info',
        title: 'قريباً',
        message: 'ستتوفر هذه الميزة قريباً'
      })
    }
    
    const editModel = (model) => {
      // تحرير النموذج
      router.push(`/ai/models/${model.id}/edit`)
    }
    
    const testModel = async (model) => {
      try {
        await aiManagementAPI.testModel(model.id)
        systemStore.addNotification({
          type: 'success',
          title: 'اختبار النموذج',
          message: `تم اختبار النموذج ${model.name} بنجاح`
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في الاختبار',
          message: 'فشل في اختبار النموذج'
        })
      }
    }
    
    const deleteModel = async (model) => {
      if (confirm(`هل أنت متأكد من حذف النموذج ${model.name}؟`)) {
        try {
          await aiManagementAPI.deleteModel(model.id)
          await aiStore.fetchModels()
          systemStore.addNotification({
            type: 'success',
            title: 'تم الحذف',
            message: 'تم حذف النموذج بنجاح'
          })
        } catch (error) {
          systemStore.addNotification({
            type: 'error',
            title: 'خطأ في الحذف',
            message: 'فشل في حذف النموذج'
          })
        }
      }
    }
    
    // وظائف الخدمات
    const configureService = (service) => {
      router.push(`/ai/services/${service.id}/config`)
    }
    
    const viewServiceLogs = (service) => {
      router.push(`/ai/services/${service.id}/logs`)
    }
    
    const toggleService = async (service) => {
      try {
        const action = service.status === 'active' ? 'stop' : 'start'
        await aiManagementAPI.toggleService(service.id, action)
        await aiStore.fetchServices()
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم التحديث',
          message: `تم ${action === 'start' ? 'تشغيل' : 'إيقاف'} الخدمة بنجاح`
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ',
          message: 'فشل في تحديث حالة الخدمة'
        })
      }
    }
    
    // وظائف الإعدادات
    const saveSettings = async () => {
      try {
        await aiManagementAPI.updateSettings(settings.value)
        systemStore.addNotification({
          type: 'success',
          title: 'تم الحفظ',
          message: 'تم حفظ الإعدادات بنجاح'
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في الحفظ',
          message: 'فشل في حفظ الإعدادات'
        })
      }
    }
    
    const resetSettings = () => {
      if (confirm('هل أنت متأكد من إعادة تعيين الإعدادات؟')) {
        settings.value = {
          max_concurrent_requests: 100,
          response_timeout: 30,
          log_level: 'INFO',
          auto_scaling: true,
          api_key: '',
          allowed_ips: '',
          enable_rate_limiting: true
        }
      }
    }
    
    const generateApiKey = () => {
      const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
      let result = ''
      for (let i = 0; i < 32; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length))
      }
      settings.value.api_key = result
    }
    
    // تحميل البيانات عند التحميل
    onMounted(async () => {
      await aiStore.fetchAllData()
      
      // تحميل الإعدادات الحالية
      try {
        const response = await aiManagementAPI.getSettings()
        settings.value = { ...settings.value, ...response.data }
      } catch (error) {
        console.error('خطأ في تحميل الإعدادات:', error)
      }
    })
    
    return {
      aiStats,
      aiModels,
      aiServices,
      alerts,
      settings,
      refreshData,
      getModelIcon,
      getStatusClass,
      getStatusText,
      formatDate,
      formatTime,
      getAlertIcon,
      showAddModelModal,
      editModel,
      testModel,
      deleteModel,
      configureService,
      viewServiceLogs,
      toggleService,
      saveSettings,
      resetSettings,
      generateApiKey
    }
  }
}
</script>

<style scoped>
.ai-management-page {
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

.model-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: linear-gradient(45deg, #4e73df, #224abe);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.service-card {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.service-card:hover {
  transform: translateY(-3px);
}

.service-header {
  display: flex;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.service-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  background: linear-gradient(45deg, #4e73df, #224abe);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.2rem;
  margin-left: 1rem;
}

.service-info {
  flex: 1;
}

.service-info h6 {
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.service-info p {
  margin-bottom: 0;
  color: #6c757d;
  font-size: 0.9rem;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
}

.status-indicator.active {
  background-color: #1cc88a;
}

.status-indicator.inactive {
  background-color: #858796;
}

.status-indicator.error {
  background-color: #e74a3b;
}

.service-metrics {
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f8f9fc;
  border-radius: 8px;
}

.metric {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.metric:last-child {
  margin-bottom: 0;
}

.metric-label {
  color: #6c757d;
  font-size: 0.9rem;
}

.metric-value {
  font-weight: 600;
  color: #2c3e50;
}

.service-actions {
  display: flex;
  gap: 0.5rem;
}

.chart-container {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.alerts-container {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  max-height: 400px;
  overflow-y: auto;
}

.alert-item {
  display: flex;
  align-items: flex-start;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  background: #f8f9fc;
}

.alert-item:last-child {
  margin-bottom: 0;
}

.alert-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 1rem;
  color: white;
}

.alert-icon.info {
  background: #36b9cc;
}

.alert-icon.warning {
  background: #f6c23e;
}

.alert-icon.error {
  background: #e74a3b;
}

.alert-icon.success {
  background: #1cc88a;
}

.alert-content {
  flex: 1;
}

.alert-title {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.alert-message {
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.alert-time {
  color: #858796;
  font-size: 0.8rem;
}

.settings-section {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.settings-section h6 {
  margin-bottom: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e3e6f0;
  padding-bottom: 0.5rem;
}

.setting-item {
  margin-bottom: 1.5rem;
}

.setting-item:last-child {
  margin-bottom: 0;
}

.settings-actions {
  text-align: center;
  padding-top: 1.5rem;
  border-top: 1px solid #e3e6f0;
}

.nav-tabs .nav-link {
  font-family: 'Cairo', sans-serif;
  font-weight: 500;
  color: #6c757d;
  border: none;
  border-bottom: 3px solid transparent;
  padding: 1rem 1.5rem;
}

.nav-tabs .nav-link.active {
  color: #4e73df;
  border-bottom-color: #4e73df;
  background: none;
}

.nav-tabs .nav-link:hover {
  color: #4e73df;
  border-color: transparent;
}

@media (max-width: 768px) {
  .page-header .d-flex {
    flex-direction: column;
    gap: 1rem;
  }
  
  .service-actions {
    flex-direction: column;
  }
  
  .service-actions .btn {
    width: 100%;
  }
  
  .settings-actions {
    text-align: center;
  }
  
  .settings-actions .btn {
    width: 100%;
    margin-bottom: 0.5rem;
  }
}
</style>

