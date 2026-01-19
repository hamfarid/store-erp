<!-- صفحة إدارة Docker -->
<template>
  <div class="docker-management-page">
    <!-- Header -->
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h1 class="page-title">
            <i class="fab fa-docker me-3"></i>
            إدارة Docker
          </h1>
          <p class="page-subtitle">مراقبة وإدارة حاويات Docker والخدمات المصغرة</p>
        </div>
        <div class="page-actions">
          <button class="btn btn-outline-info" @click="refreshAll">
            <i class="fas fa-sync-alt me-2"></i>
            تحديث الكل
          </button>
          <button class="btn btn-outline-warning" @click="showLogs">
            <i class="fas fa-file-alt me-2"></i>
            عرض السجلات
          </button>
          <button class="btn btn-primary" @click="deployServices">
            <i class="fas fa-rocket me-2"></i>
            نشر الخدمات
          </button>
        </div>
      </div>
    </div>

    <!-- إحصائيات سريعة -->
    <div class="row mb-4">
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card primary">
          <div class="stat-icon">
            <i class="fas fa-cube"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ dockerStats.total_containers || 0 }}</div>
            <div class="stat-label">إجمالي الحاويات</div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card success">
          <div class="stat-icon">
            <i class="fas fa-play-circle"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ dockerStats.running_containers || 0 }}</div>
            <div class="stat-label">حاويات نشطة</div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card warning">
          <div class="stat-icon">
            <i class="fas fa-pause-circle"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ dockerStats.stopped_containers || 0 }}</div>
            <div class="stat-label">حاويات متوقفة</div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card info">
          <div class="stat-icon">
            <i class="fas fa-hdd"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ dockerStats.total_images || 0 }}</div>
            <div class="stat-label">الصور المحفوظة</div>
          </div>
        </div>
      </div>
    </div>

    <!-- حالة الخدمات -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">
                <i class="fas fa-server me-2"></i>
                حالة الخدمات
              </h5>
              <div class="card-actions">
                <button class="btn btn-sm btn-outline-success" @click="startAllServices">
                  <i class="fas fa-play"></i>
                  تشغيل الكل
                </button>
                <button class="btn btn-sm btn-outline-danger" @click="stopAllServices">
                  <i class="fas fa-stop"></i>
                  إيقاف الكل
                </button>
                <button class="btn btn-sm btn-outline-warning" @click="restartAllServices">
                  <i class="fas fa-redo"></i>
                  إعادة تشغيل
                </button>
              </div>
            </div>
          </div>
          <div class="card-body">
            <div class="services-grid">
              <div class="service-card" 
                   v-for="service in services" 
                   :key="service.name"
                   :class="getServiceStatusClass(service.status)">
                <div class="service-header">
                  <div class="service-info">
                    <div class="service-name">{{ service.display_name }}</div>
                    <div class="service-description">{{ service.description }}</div>
                  </div>
                  <div class="service-status">
                    <span class="status-indicator" :class="service.status"></span>
                    <span class="status-text">{{ getStatusText(service.status) }}</span>
                  </div>
                </div>
                
                <div class="service-metrics" v-if="service.status === 'running'">
                  <div class="metric">
                    <span class="metric-label">CPU:</span>
                    <span class="metric-value">{{ service.cpu_usage || 0 }}%</span>
                  </div>
                  <div class="metric">
                    <span class="metric-label">RAM:</span>
                    <span class="metric-value">{{ service.memory_usage || 0 }}MB</span>
                  </div>
                  <div class="metric">
                    <span class="metric-label">الشبكة:</span>
                    <span class="metric-value">{{ service.network_io || 0 }}KB/s</span>
                  </div>
                </div>
                
                <div class="service-actions">
                  <button class="btn btn-sm btn-success" 
                          @click="startService(service)"
                          :disabled="service.status === 'running'"
                          v-if="service.status !== 'running'">
                    <i class="fas fa-play"></i>
                  </button>
                  
                  <button class="btn btn-sm btn-danger" 
                          @click="stopService(service)"
                          :disabled="service.status !== 'running'"
                          v-if="service.status === 'running'">
                    <i class="fas fa-stop"></i>
                  </button>
                  
                  <button class="btn btn-sm btn-warning" 
                          @click="restartService(service)"
                          :disabled="service.status !== 'running'">
                    <i class="fas fa-redo"></i>
                  </button>
                  
                  <button class="btn btn-sm btn-info" @click="viewServiceLogs(service)">
                    <i class="fas fa-file-alt"></i>
                  </button>
                  
                  <button class="btn btn-sm btn-outline-secondary" @click="serviceSettings(service)">
                    <i class="fas fa-cog"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- مراقبة الموارد -->
    <div class="row mb-4">
      <div class="col-lg-6">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="fas fa-chart-line me-2"></i>
              استخدام الموارد
            </h5>
          </div>
          <div class="card-body">
            <div class="resource-monitor">
              <div class="resource-item">
                <div class="resource-header">
                  <span class="resource-label">استخدام المعالج</span>
                  <span class="resource-value">{{ systemResources.cpu_usage || 0 }}%</span>
                </div>
                <div class="progress">
                  <div class="progress-bar" 
                       :class="getCpuProgressClass(systemResources.cpu_usage)"
                       :style="{ width: (systemResources.cpu_usage || 0) + '%' }">
                  </div>
                </div>
              </div>
              
              <div class="resource-item">
                <div class="resource-header">
                  <span class="resource-label">استخدام الذاكرة</span>
                  <span class="resource-value">{{ systemResources.memory_usage || 0 }}%</span>
                </div>
                <div class="progress">
                  <div class="progress-bar" 
                       :class="getMemoryProgressClass(systemResources.memory_usage)"
                       :style="{ width: (systemResources.memory_usage || 0) + '%' }">
                  </div>
                </div>
              </div>
              
              <div class="resource-item">
                <div class="resource-header">
                  <span class="resource-label">استخدام القرص</span>
                  <span class="resource-value">{{ systemResources.disk_usage || 0 }}%</span>
                </div>
                <div class="progress">
                  <div class="progress-bar" 
                       :class="getDiskProgressClass(systemResources.disk_usage)"
                       :style="{ width: (systemResources.disk_usage || 0) + '%' }">
                  </div>
                </div>
              </div>
              
              <div class="resource-item">
                <div class="resource-header">
                  <span class="resource-label">حركة الشبكة</span>
                  <span class="resource-value">{{ systemResources.network_io || 0 }}MB/s</span>
                </div>
                <div class="network-stats">
                  <div class="network-stat">
                    <i class="fas fa-arrow-up text-success"></i>
                    <span>{{ systemResources.network_out || 0 }}MB/s</span>
                  </div>
                  <div class="network-stat">
                    <i class="fas fa-arrow-down text-info"></i>
                    <span>{{ systemResources.network_in || 0 }}MB/s</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-6">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="fas fa-images me-2"></i>
              إدارة الصور
            </h5>
          </div>
          <div class="card-body">
            <div class="images-list">
              <div class="image-item" v-for="image in dockerImages" :key="image.id">
                <div class="image-info">
                  <div class="image-name">{{ image.repository }}:{{ image.tag }}</div>
                  <div class="image-details">
                    <small class="text-muted">
                      الحجم: {{ formatBytes(image.size) }} | 
                      تم الإنشاء: {{ formatDate(image.created) }}
                    </small>
                  </div>
                </div>
                <div class="image-actions">
                  <button class="btn btn-sm btn-outline-primary" @click="pullImage(image)">
                    <i class="fas fa-download"></i>
                  </button>
                  <button class="btn btn-sm btn-outline-danger" @click="removeImage(image)">
                    <i class="fas fa-trash"></i>
                  </button>
                </div>
              </div>
            </div>
            
            <div class="mt-3">
              <div class="input-group">
                <input type="text" 
                       class="form-control" 
                       placeholder="اسم الصورة:العلامة"
                       v-model="newImageName">
                <button class="btn btn-outline-primary" @click="pullNewImage">
                  <i class="fas fa-download me-2"></i>
                  سحب صورة
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- سجل العمليات -->
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">
                <i class="fas fa-history me-2"></i>
                سجل العمليات
              </h5>
              <div class="card-actions">
                <button class="btn btn-sm btn-outline-primary" @click="refreshLogs">
                  <i class="fas fa-sync-alt"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" @click="clearLogs">
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
          </div>
          <div class="card-body">
            <div class="logs-container">
              <div class="log-entry" 
                   v-for="log in dockerLogs" 
                   :key="log.id"
                   :class="getLogLevelClass(log.level)">
                <div class="log-timestamp">{{ formatDateTime(log.timestamp) }}</div>
                <div class="log-service">{{ log.service }}</div>
                <div class="log-message">{{ log.message }}</div>
                <div class="log-level">
                  <span class="badge" :class="getLogBadgeClass(log.level)">
                    {{ log.level.toUpperCase() }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- نافذة إعدادات الخدمة -->
    <div class="modal fade" id="serviceSettingsModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">إعدادات الخدمة: {{ selectedService?.display_name }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="row" v-if="selectedService">
              <div class="col-md-6">
                <div class="setting-item">
                  <label class="form-label">عدد النسخ</label>
                  <input type="number" 
                         class="form-control" 
                         v-model="selectedService.replicas"
                         min="1" 
                         max="10">
                </div>
                
                <div class="setting-item">
                  <label class="form-label">حد الذاكرة (MB)</label>
                  <input type="number" 
                         class="form-control" 
                         v-model="selectedService.memory_limit"
                         min="128" 
                         max="8192">
                </div>
                
                <div class="setting-item">
                  <label class="form-label">حد المعالج (%)</label>
                  <input type="number" 
                         class="form-control" 
                         v-model="selectedService.cpu_limit"
                         min="10" 
                         max="100">
                </div>
              </div>
              
              <div class="col-md-6">
                <div class="setting-item">
                  <label class="form-label">متغيرات البيئة</label>
                  <textarea class="form-control" 
                            rows="5"
                            v-model="selectedService.environment"
                            placeholder="KEY=VALUE"></textarea>
                </div>
                
                <div class="setting-item">
                  <div class="form-check">
                    <input class="form-check-input" 
                           type="checkbox" 
                           v-model="selectedService.auto_restart">
                    <label class="form-check-label">إعادة التشغيل التلقائي</label>
                  </div>
                </div>
                
                <div class="setting-item">
                  <div class="form-check">
                    <input class="form-check-input" 
                           type="checkbox" 
                           v-model="selectedService.health_check">
                    <label class="form-check-label">فحص الحالة</label>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">إلغاء</button>
            <button type="button" class="btn btn-primary" @click="saveServiceSettings">حفظ التغييرات</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useDockerStore, useSystemStore } from '../../store/index.js'
import { dockerAPI } from '../../services/api.js'

export default {
  name: 'DockerManagement',
  
  setup() {
    const router = useRouter()
    const dockerStore = useDockerStore()
    const systemStore = useSystemStore()
    
    const selectedService = ref(null)
    const newImageName = ref('')
    
    // البيانات المحسوبة
    const dockerStats = computed(() => dockerStore.stats)
    const services = computed(() => dockerStore.services)
    const dockerImages = computed(() => dockerStore.images)
    const dockerLogs = computed(() => dockerStore.logs)
    const systemResources = computed(() => dockerStore.systemResources)
    
    // الوظائف
    const refreshAll = async () => {
      await Promise.all([
        dockerStore.fetchStats(),
        dockerStore.fetchServices(),
        dockerStore.fetchImages(),
        dockerStore.fetchLogs(),
        dockerStore.fetchSystemResources()
      ])
      
      systemStore.addNotification({
        type: 'success',
        title: 'تم التحديث',
        message: 'تم تحديث جميع البيانات بنجاح'
      })
    }
    
    const deployServices = async () => {
      try {
        await dockerAPI.deployServices()
        await dockerStore.fetchServices()
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم النشر',
          message: 'تم نشر الخدمات بنجاح'
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في النشر',
          message: 'فشل في نشر الخدمات'
        })
      }
    }
    
    const startService = async (service) => {
      try {
        await dockerAPI.startService(service.name)
        await dockerStore.fetchServices()
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم التشغيل',
          message: `تم تشغيل خدمة ${service.display_name}`
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في التشغيل',
          message: `فشل في تشغيل خدمة ${service.display_name}`
        })
      }
    }
    
    const stopService = async (service) => {
      try {
        await dockerAPI.stopService(service.name)
        await dockerStore.fetchServices()
        
        systemStore.addNotification({
          type: 'warning',
          title: 'تم الإيقاف',
          message: `تم إيقاف خدمة ${service.display_name}`
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في الإيقاف',
          message: `فشل في إيقاف خدمة ${service.display_name}`
        })
      }
    }
    
    const restartService = async (service) => {
      try {
        await dockerAPI.restartService(service.name)
        await dockerStore.fetchServices()
        
        systemStore.addNotification({
          type: 'info',
          title: 'تم إعادة التشغيل',
          message: `تم إعادة تشغيل خدمة ${service.display_name}`
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في إعادة التشغيل',
          message: `فشل في إعادة تشغيل خدمة ${service.display_name}`
        })
      }
    }
    
    const startAllServices = async () => {
      try {
        await dockerAPI.startAllServices()
        await dockerStore.fetchServices()
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم التشغيل',
          message: 'تم تشغيل جميع الخدمات'
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في التشغيل',
          message: 'فشل في تشغيل بعض الخدمات'
        })
      }
    }
    
    const stopAllServices = async () => {
      if (confirm('هل أنت متأكد من إيقاف جميع الخدمات؟')) {
        try {
          await dockerAPI.stopAllServices()
          await dockerStore.fetchServices()
          
          systemStore.addNotification({
            type: 'warning',
            title: 'تم الإيقاف',
            message: 'تم إيقاف جميع الخدمات'
          })
        } catch (error) {
          systemStore.addNotification({
            type: 'error',
            title: 'خطأ في الإيقاف',
            message: 'فشل في إيقاف بعض الخدمات'
          })
        }
      }
    }
    
    const restartAllServices = async () => {
      if (confirm('هل أنت متأكد من إعادة تشغيل جميع الخدمات؟')) {
        try {
          await dockerAPI.restartAllServices()
          await dockerStore.fetchServices()
          
          systemStore.addNotification({
            type: 'info',
            title: 'تم إعادة التشغيل',
            message: 'تم إعادة تشغيل جميع الخدمات'
          })
        } catch (error) {
          systemStore.addNotification({
            type: 'error',
            title: 'خطأ في إعادة التشغيل',
            message: 'فشل في إعادة تشغيل بعض الخدمات'
          })
        }
      }
    }
    
    const viewServiceLogs = (service) => {
      router.push(`/admin/docker/logs/${service.name}`)
    }
    
    const serviceSettings = (service) => {
      selectedService.value = { ...service }
      const modal = new bootstrap.Modal(document.getElementById('serviceSettingsModal'))
      modal.show()
    }
    
    const saveServiceSettings = async () => {
      try {
        await dockerAPI.updateServiceSettings(selectedService.value.name, selectedService.value)
        await dockerStore.fetchServices()
        
        const modal = bootstrap.Modal.getInstance(document.getElementById('serviceSettingsModal'))
        modal.hide()
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم الحفظ',
          message: 'تم حفظ إعدادات الخدمة'
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في الحفظ',
          message: 'فشل في حفظ الإعدادات'
        })
      }
    }
    
    const pullNewImage = async () => {
      if (!newImageName.value) return
      
      try {
        await dockerAPI.pullImage(newImageName.value)
        await dockerStore.fetchImages()
        newImageName.value = ''
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم السحب',
          message: 'تم سحب الصورة بنجاح'
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في السحب',
          message: 'فشل في سحب الصورة'
        })
      }
    }
    
    const removeImage = async (image) => {
      if (confirm(`هل أنت متأكد من حذف الصورة ${image.repository}:${image.tag}؟`)) {
        try {
          await dockerAPI.removeImage(image.id)
          await dockerStore.fetchImages()
          
          systemStore.addNotification({
            type: 'success',
            title: 'تم الحذف',
            message: 'تم حذف الصورة بنجاح'
          })
        } catch (error) {
          systemStore.addNotification({
            type: 'error',
            title: 'خطأ في الحذف',
            message: 'فشل في حذف الصورة'
          })
        }
      }
    }
    
    const showLogs = () => {
      router.push('/admin/docker/logs')
    }
    
    const refreshLogs = async () => {
      await dockerStore.fetchLogs()
    }
    
    const clearLogs = async () => {
      if (confirm('هل أنت متأكد من مسح السجلات؟')) {
        try {
          await dockerAPI.clearLogs()
          await dockerStore.fetchLogs()
          
          systemStore.addNotification({
            type: 'success',
            title: 'تم المسح',
            message: 'تم مسح السجلات بنجاح'
          })
        } catch (error) {
          systemStore.addNotification({
            type: 'error',
            title: 'خطأ في المسح',
            message: 'فشل في مسح السجلات'
          })
        }
      }
    }
    
    // وظائف مساعدة
    const getServiceStatusClass = (status) => {
      const classes = {
        'running': 'service-running',
        'stopped': 'service-stopped',
        'error': 'service-error',
        'starting': 'service-starting'
      }
      return classes[status] || 'service-unknown'
    }
    
    const getStatusText = (status) => {
      const texts = {
        'running': 'يعمل',
        'stopped': 'متوقف',
        'error': 'خطأ',
        'starting': 'يبدأ'
      }
      return texts[status] || 'غير معروف'
    }
    
    const getCpuProgressClass = (usage) => {
      if (usage >= 80) return 'bg-danger'
      if (usage >= 60) return 'bg-warning'
      return 'bg-success'
    }
    
    const getMemoryProgressClass = (usage) => {
      if (usage >= 85) return 'bg-danger'
      if (usage >= 70) return 'bg-warning'
      return 'bg-info'
    }
    
    const getDiskProgressClass = (usage) => {
      if (usage >= 90) return 'bg-danger'
      if (usage >= 75) return 'bg-warning'
      return 'bg-primary'
    }
    
    const getLogLevelClass = (level) => {
      const classes = {
        'error': 'log-error',
        'warning': 'log-warning',
        'info': 'log-info',
        'debug': 'log-debug'
      }
      return classes[level] || 'log-info'
    }
    
    const getLogBadgeClass = (level) => {
      const classes = {
        'error': 'bg-danger',
        'warning': 'bg-warning',
        'info': 'bg-info',
        'debug': 'bg-secondary'
      }
      return classes[level] || 'bg-info'
    }
    
    const formatBytes = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('ar-SA', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }
    
    const formatDateTime = (date) => {
      return new Date(date).toLocaleString('ar-SA', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
    }
    
    // تحديث البيانات دورياً
    let refreshInterval
    
    onMounted(async () => {
      await refreshAll()
      
      // تحديث البيانات كل 30 ثانية
      refreshInterval = setInterval(async () => {
        await dockerStore.fetchStats()
        await dockerStore.fetchServices()
        await dockerStore.fetchSystemResources()
      }, 30000)
    })
    
    // تنظيف المؤقت عند إلغاء التحميل
    onUnmounted(() => {
      if (refreshInterval) {
        clearInterval(refreshInterval)
      }
    })
    
    return {
      selectedService,
      newImageName,
      dockerStats,
      services,
      dockerImages,
      dockerLogs,
      systemResources,
      refreshAll,
      deployServices,
      startService,
      stopService,
      restartService,
      startAllServices,
      stopAllServices,
      restartAllServices,
      viewServiceLogs,
      serviceSettings,
      saveServiceSettings,
      pullNewImage,
      removeImage,
      showLogs,
      refreshLogs,
      clearLogs,
      getServiceStatusClass,
      getStatusText,
      getCpuProgressClass,
      getMemoryProgressClass,
      getDiskProgressClass,
      getLogLevelClass,
      getLogBadgeClass,
      formatBytes,
      formatDate,
      formatDateTime
    }
  }
}
</script>

<style scoped>
.docker-management-page {
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

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.service-card {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-left: 4px solid;
  transition: transform 0.3s ease;
}

.service-card:hover {
  transform: translateY(-5px);
}

.service-card.service-running {
  border-left-color: #1cc88a;
}

.service-card.service-stopped {
  border-left-color: #e74a3b;
}

.service-card.service-error {
  border-left-color: #f6c23e;
}

.service-card.service-starting {
  border-left-color: #36b9cc;
}

.service-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.service-name {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.service-description {
  color: #6c757d;
  font-size: 0.9rem;
}

.service-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.status-indicator.running {
  background: #1cc88a;
  box-shadow: 0 0 10px rgba(28, 200, 138, 0.5);
}

.status-indicator.stopped {
  background: #e74a3b;
}

.status-indicator.error {
  background: #f6c23e;
}

.status-indicator.starting {
  background: #36b9cc;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

.status-text {
  font-size: 0.9rem;
  font-weight: 500;
  color: #2c3e50;
}

.service-metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f8f9fc;
  border-radius: 10px;
}

.metric {
  text-align: center;
}

.metric-label {
  display: block;
  font-size: 0.8rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
}

.metric-value {
  font-weight: 600;
  color: #2c3e50;
}

.service-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.resource-monitor {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.resource-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.resource-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.resource-label {
  font-weight: 600;
  color: #2c3e50;
}

.resource-value {
  font-weight: 600;
  color: #4e73df;
}

.network-stats {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
}

.network-stat {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.images-list {
  max-height: 300px;
  overflow-y: auto;
}

.image-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-radius: 10px;
  margin-bottom: 0.5rem;
  background: #f8f9fc;
  transition: background 0.3s ease;
}

.image-item:hover {
  background: #e3e6f0;
}

.image-name {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.image-actions {
  display: flex;
  gap: 0.5rem;
}

.logs-container {
  max-height: 400px;
  overflow-y: auto;
  background: #1a1a1a;
  border-radius: 10px;
  padding: 1rem;
}

.log-entry {
  display: grid;
  grid-template-columns: auto auto 1fr auto;
  gap: 1rem;
  padding: 0.5rem;
  border-radius: 5px;
  margin-bottom: 0.5rem;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
}

.log-entry.log-error {
  background: rgba(231, 74, 59, 0.1);
  border-left: 3px solid #e74a3b;
}

.log-entry.log-warning {
  background: rgba(246, 194, 62, 0.1);
  border-left: 3px solid #f6c23e;
}

.log-entry.log-info {
  background: rgba(54, 185, 204, 0.1);
  border-left: 3px solid #36b9cc;
}

.log-entry.log-debug {
  background: rgba(108, 117, 125, 0.1);
  border-left: 3px solid #6c757d;
}

.log-timestamp {
  color: #6c757d;
  white-space: nowrap;
}

.log-service {
  color: #4e73df;
  font-weight: 600;
  white-space: nowrap;
}

.log-message {
  color: #e9ecef;
  word-break: break-word;
}

.log-level {
  white-space: nowrap;
}

.setting-item {
  margin-bottom: 1.5rem;
}

.setting-item:last-child {
  margin-bottom: 0;
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

@media (max-width: 768px) {
  .page-header .d-flex {
    flex-direction: column;
    gap: 1rem;
  }
  
  .services-grid {
    grid-template-columns: 1fr;
  }
  
  .service-metrics {
    grid-template-columns: 1fr;
  }
  
  .service-actions {
    flex-wrap: wrap;
  }
  
  .log-entry {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .resource-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}
</style>

