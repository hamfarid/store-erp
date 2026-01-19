<!-- صفحة كشف الكائنات YOLO -->
<template>
  <div class="yolo-detection-page">
    <!-- Header -->
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h1 class="page-title">
            <i class="fas fa-search me-3"></i>
            كشف الكائنات YOLO
          </h1>
          <p class="page-subtitle">كشف وتحديد الكائنات في الصور باستخدام خوارزميات YOLO المتقدمة</p>
        </div>
        <div class="page-actions">
          <button class="btn btn-outline-info" @click="showModelInfo">
            <i class="fas fa-info-circle me-2"></i>
            معلومات النموذج
          </button>
          <button class="btn btn-primary" @click="startNewDetection">
            <i class="fas fa-plus me-2"></i>
            كشف جديد
          </button>
        </div>
      </div>
    </div>

    <!-- إحصائيات سريعة -->
    <div class="row mb-4">
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card primary">
          <div class="stat-icon">
            <i class="fas fa-eye"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ detectionStats.total_detections || 0 }}</div>
            <div class="stat-label">إجمالي عمليات الكشف</div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card success">
          <div class="stat-icon">
            <i class="fas fa-bullseye"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ detectionStats.objects_detected || 0 }}</div>
            <div class="stat-label">الكائنات المكتشفة</div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card info">
          <div class="stat-icon">
            <i class="fas fa-percentage"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ detectionStats.accuracy_rate || 0 }}%</div>
            <div class="stat-label">معدل الدقة</div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card warning">
          <div class="stat-icon">
            <i class="fas fa-clock"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ detectionStats.avg_processing_time || 0 }}ms</div>
            <div class="stat-label">متوسط وقت المعالجة</div>
          </div>
        </div>
      </div>
    </div>

    <!-- منطقة الكشف الرئيسية -->
    <div class="row mb-4">
      <div class="col-lg-8">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="fas fa-upload me-2"></i>
              رفع الصورة للكشف
            </h5>
          </div>
          <div class="card-body">
            <div class="detection-area">
              <div class="upload-section" v-if="!originalImage">
                <div class="upload-zone" 
                     @drop="handleDrop" 
                     @dragover.prevent 
                     @dragenter.prevent
                     :class="{ 'drag-over': isDragOver }"
                     @dragenter="isDragOver = true"
                     @dragleave="isDragOver = false">
                  
                  <i class="fas fa-cloud-upload-alt upload-icon"></i>
                  <h6>اسحب الصورة هنا أو انقر للاختيار</h6>
                  <p class="text-muted">يدعم النظام صيغ JPG, PNG, WEBP</p>
                  <input type="file" 
                         ref="fileInput" 
                         @change="handleFileSelect" 
                         accept="image/*" 
                         class="d-none">
                  <button class="btn btn-outline-primary" @click="$refs.fileInput.click()">
                    اختيار صورة
                  </button>
                </div>
              </div>
              
              <div class="detection-results" v-if="originalImage">
                <div class="image-container">
                  <div class="original-image-section">
                    <h6>الصورة الأصلية</h6>
                    <div class="image-wrapper">
                      <img :src="originalImage" 
                           alt="الصورة الأصلية" 
                           class="detection-image"
                           ref="originalImageRef">
                    </div>
                  </div>
                  
                  <div class="detected-image-section" v-if="detectedImage">
                    <h6>نتائج الكشف</h6>
                    <div class="image-wrapper">
                      <img :src="detectedImage" 
                           alt="نتائج الكشف" 
                           class="detection-image">
                      
                      <!-- عرض الكائنات المكتشفة -->
                      <div class="detection-overlay" v-if="detectionResults">
                        <div v-for="(detection, index) in detectionResults.objects" 
                             :key="index"
                             class="detection-box"
                             :style="getDetectionBoxStyle(detection)">
                          <div class="detection-label">
                            {{ detection.class_name }}
                            <span class="confidence">{{ Math.round(detection.confidence * 100) }}%</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="processing-section" v-else-if="isProcessing">
                    <h6>جاري الكشف...</h6>
                    <div class="processing-placeholder">
                      <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">جاري المعالجة...</span>
                      </div>
                      <p class="mt-3">{{ processingStatus }}</p>
                      <div class="progress mt-3">
                        <div class="progress-bar" 
                             role="progressbar" 
                             :style="{ width: processingProgress + '%' }">
                          {{ processingProgress }}%
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="detection-actions mt-3">
                  <button class="btn btn-success" 
                          @click="startDetection" 
                          :disabled="isProcessing"
                          v-if="!detectedImage">
                    <i v-if="isProcessing" class="fas fa-spinner fa-spin me-2"></i>
                    <i v-else class="fas fa-play me-2"></i>
                    {{ isProcessing ? 'جاري الكشف...' : 'بدء الكشف' }}
                  </button>
                  
                  <div v-if="detectedImage" class="result-actions">
                    <button class="btn btn-primary" @click="downloadResults">
                      <i class="fas fa-download me-2"></i>
                      تحميل النتائج
                    </button>
                    <button class="btn btn-outline-info" @click="viewDetailedResults">
                      <i class="fas fa-list me-2"></i>
                      النتائج التفصيلية
                    </button>
                    <button class="btn btn-outline-success" @click="saveDetection">
                      <i class="fas fa-save me-2"></i>
                      حفظ الكشف
                    </button>
                  </div>
                  
                  <button class="btn btn-outline-secondary" @click="clearDetection">
                    <i class="fas fa-times me-2"></i>
                    إلغاء
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-4">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="fas fa-cogs me-2"></i>
              إعدادات الكشف
            </h5>
          </div>
          <div class="card-body">
            <div class="setting-item">
              <label class="form-label">نموذج YOLO</label>
              <select class="form-select" v-model="detectionSettings.model">
                <option value="yolov8n">YOLOv8 Nano (سريع)</option>
                <option value="yolov8s">YOLOv8 Small</option>
                <option value="yolov8m">YOLOv8 Medium</option>
                <option value="yolov8l">YOLOv8 Large</option>
                <option value="yolov8x">YOLOv8 XLarge (دقيق)</option>
              </select>
            </div>
            
            <div class="setting-item">
              <label class="form-label">حد الثقة</label>
              <input type="range" 
                     class="form-range" 
                     min="0.1" 
                     max="1" 
                     step="0.05"
                     v-model="detectionSettings.confidence_threshold">
              <div class="range-labels">
                <span>0.1</span>
                <span>{{ detectionSettings.confidence_threshold }}</span>
                <span>1.0</span>
              </div>
            </div>
            
            <div class="setting-item">
              <label class="form-label">حد التداخل (IoU)</label>
              <input type="range" 
                     class="form-range" 
                     min="0.1" 
                     max="0.9" 
                     step="0.05"
                     v-model="detectionSettings.iou_threshold">
              <div class="range-labels">
                <span>0.1</span>
                <span>{{ detectionSettings.iou_threshold }}</span>
                <span>0.9</span>
              </div>
            </div>
            
            <div class="setting-item">
              <label class="form-label">الفئات المستهدفة</label>
              <div class="classes-selection">
                <div class="form-check" v-for="cls in availableClasses" :key="cls.id">
                  <input class="form-check-input" 
                         type="checkbox" 
                         :value="cls.id"
                         v-model="detectionSettings.target_classes">
                  <label class="form-check-label">{{ cls.name }}</label>
                </div>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" v-model="detectionSettings.show_labels">
                <label class="form-check-label">إظهار التسميات</label>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" v-model="detectionSettings.show_confidence">
                <label class="form-check-label">إظهار مستوى الثقة</label>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" v-model="detectionSettings.save_annotations">
                <label class="form-check-label">حفظ التعليقات التوضيحية</label>
              </div>
            </div>
          </div>
        </div>
        
        <!-- النتائج التفصيلية -->
        <div class="card mt-3" v-if="detectionResults">
          <div class="card-header">
            <h6 class="card-title mb-0">
              <i class="fas fa-list me-2"></i>
              الكائنات المكتشفة
            </h6>
          </div>
          <div class="card-body">
            <div class="detected-objects">
              <div class="object-item" v-for="(obj, index) in detectionResults.objects" :key="index">
                <div class="object-info">
                  <div class="object-name">{{ obj.class_name }}</div>
                  <div class="object-confidence">
                    <span class="badge" :class="getConfidenceClass(obj.confidence)">
                      {{ Math.round(obj.confidence * 100) }}%
                    </span>
                  </div>
                </div>
                <div class="object-details">
                  <small class="text-muted">
                    الموقع: ({{ Math.round(obj.bbox.x) }}, {{ Math.round(obj.bbox.y) }})
                    الحجم: {{ Math.round(obj.bbox.width) }} × {{ Math.round(obj.bbox.height) }}
                  </small>
                </div>
              </div>
            </div>
            
            <div class="detection-summary mt-3">
              <div class="summary-item">
                <span class="summary-label">إجمالي الكائنات:</span>
                <span class="summary-value">{{ detectionResults.objects.length }}</span>
              </div>
              <div class="summary-item">
                <span class="summary-label">وقت المعالجة:</span>
                <span class="summary-value">{{ detectionResults.processing_time }}ms</span>
              </div>
              <div class="summary-item">
                <span class="summary-label">دقة النموذج:</span>
                <span class="summary-value">{{ detectionResults.model_accuracy }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- سجل عمليات الكشف -->
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">
                <i class="fas fa-history me-2"></i>
                سجل عمليات الكشف
              </h5>
              <div class="card-actions">
                <button class="btn btn-sm btn-outline-primary" @click="refreshHistory">
                  <i class="fas fa-sync-alt"></i>
                </button>
                <button class="btn btn-sm btn-outline-success" @click="exportHistory">
                  <i class="fas fa-download"></i>
                </button>
              </div>
            </div>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>التاريخ</th>
                    <th>الصورة</th>
                    <th>النموذج</th>
                    <th>الكائنات المكتشفة</th>
                    <th>متوسط الثقة</th>
                    <th>وقت المعالجة</th>
                    <th>الحالة</th>
                    <th>الإجراءات</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="detection in detectionHistory" :key="detection.id">
                    <td>{{ formatDate(detection.created_at) }}</td>
                    <td>
                      <img :src="detection.image_thumbnail" alt="صورة" class="table-image">
                    </td>
                    <td>{{ detection.model_name }}</td>
                    <td>
                      <span class="badge bg-info">{{ detection.objects_count }}</span>
                    </td>
                    <td>
                      <span class="badge" :class="getConfidenceClass(detection.avg_confidence)">
                        {{ Math.round(detection.avg_confidence * 100) }}%
                      </span>
                    </td>
                    <td>{{ detection.processing_time }}ms</td>
                    <td>
                      <span class="badge" :class="getStatusClass(detection.status)">
                        {{ getStatusText(detection.status) }}
                      </span>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-info" @click="viewDetection(detection)">
                          <i class="fas fa-eye"></i>
                        </button>
                        <button class="btn btn-outline-primary" @click="downloadDetectionResults(detection)">
                          <i class="fas fa-download"></i>
                        </button>
                        <button class="btn btn-outline-success" @click="rerunDetection(detection)">
                          <i class="fas fa-redo"></i>
                        </button>
                        <button class="btn btn-outline-danger" @click="deleteDetection(detection)">
                          <i class="fas fa-trash"></i>
                        </button>
                      </div>
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
import { useYoloDetectionStore, useSystemStore } from '../../store/index.js'
import { yoloDetectionAPI } from '../../services/api.js'

export default {
  name: 'YoloDetection',
  
  setup() {
    const router = useRouter()
    const yoloDetectionStore = useYoloDetectionStore()
    const systemStore = useSystemStore()
    
    const fileInput = ref(null)
    const originalImageRef = ref(null)
    const originalImage = ref(null)
    const detectedImage = ref(null)
    const isDragOver = ref(false)
    const isProcessing = ref(false)
    const processingStatus = ref('')
    const processingProgress = ref(0)
    
    const detectionSettings = ref({
      model: 'yolov8m',
      confidence_threshold: 0.5,
      iou_threshold: 0.45,
      target_classes: [],
      show_labels: true,
      show_confidence: true,
      save_annotations: true
    })
    
    const availableClasses = ref([
      { id: 0, name: 'شخص' },
      { id: 1, name: 'دراجة' },
      { id: 2, name: 'سيارة' },
      { id: 3, name: 'دراجة نارية' },
      { id: 5, name: 'حافلة' },
      { id: 7, name: 'شاحنة' },
      { id: 16, name: 'طائر' },
      { id: 17, name: 'قطة' },
      { id: 18, name: 'كلب' },
      { id: 19, name: 'حصان' },
      { id: 20, name: 'خروف' },
      { id: 21, name: 'بقرة' }
    ])
    
    // البيانات المحسوبة
    const detectionStats = computed(() => yoloDetectionStore.stats)
    const detectionResults = computed(() => yoloDetectionStore.currentResults)
    const detectionHistory = computed(() => yoloDetectionStore.history)
    
    // الوظائف
    const startNewDetection = () => {
      clearDetection()
      fileInput.value?.click()
    }
    
    const handleFileSelect = (event) => {
      const file = event.target.files[0]
      if (file) {
        processImageFile(file)
      }
    }
    
    const handleDrop = (event) => {
      event.preventDefault()
      isDragOver.value = false
      
      const files = event.dataTransfer.files
      if (files.length > 0) {
        processImageFile(files[0])
      }
    }
    
    const processImageFile = (file) => {
      if (!file.type.startsWith('image/')) {
        systemStore.addNotification({
          type: 'error',
          title: 'نوع ملف غير صحيح',
          message: 'يرجى اختيار ملف صورة صالح'
        })
        return
      }
      
      const reader = new FileReader()
      reader.onload = (e) => {
        originalImage.value = e.target.result
        detectedImage.value = null
        yoloDetectionStore.clearCurrentResults()
      }
      reader.readAsDataURL(file)
    }
    
    const clearDetection = () => {
      originalImage.value = null
      detectedImage.value = null
      yoloDetectionStore.clearCurrentResults()
      if (fileInput.value) {
        fileInput.value.value = ''
      }
    }
    
    const startDetection = async () => {
      if (!originalImage.value) return
      
      isProcessing.value = true
      processingStatus.value = 'تحضير الصورة...'
      processingProgress.value = 10
      
      try {
        const formData = new FormData()
        
        // تحويل base64 إلى blob
        const response = await fetch(originalImage.value)
        const blob = await response.blob()
        formData.append('image', blob, 'detection-image.jpg')
        formData.append('settings', JSON.stringify(detectionSettings.value))
        
        // تحديث حالة المعالجة
        processingStatus.value = 'تحميل النموذج...'
        processingProgress.value = 30
        
        // محاكاة تقدم المعالجة
        const progressInterval = setInterval(() => {
          if (processingProgress.value < 80) {
            processingProgress.value += 10
            if (processingProgress.value === 50) {
              processingStatus.value = 'تشغيل الكشف...'
            } else if (processingProgress.value === 70) {
              processingStatus.value = 'معالجة النتائج...'
            }
          }
        }, 500)
        
        const result = await yoloDetectionAPI.detectObjects(formData)
        
        clearInterval(progressInterval)
        processingProgress.value = 100
        processingStatus.value = 'اكتمل!'
        
        yoloDetectionStore.setCurrentResults(result.data)
        detectedImage.value = result.data.annotated_image_url
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم الكشف',
          message: `تم كشف ${result.data.objects.length} كائن بنجاح`
        })
        
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في الكشف',
          message: 'فشل في إجراء عملية الكشف'
        })
      } finally {
        isProcessing.value = false
        processingStatus.value = ''
        processingProgress.value = 0
      }
    }
    
    const getDetectionBoxStyle = (detection) => {
      // تحويل إحداثيات الصندوق إلى CSS
      return {
        position: 'absolute',
        left: `${detection.bbox.x}px`,
        top: `${detection.bbox.y}px`,
        width: `${detection.bbox.width}px`,
        height: `${detection.bbox.height}px`,
        border: '2px solid #4e73df',
        backgroundColor: 'rgba(78, 115, 223, 0.1)'
      }
    }
    
    const getConfidenceClass = (confidence) => {
      if (confidence >= 0.8) return 'bg-success'
      if (confidence >= 0.6) return 'bg-warning'
      return 'bg-danger'
    }
    
    const getStatusClass = (status) => {
      const classes = {
        'completed': 'bg-success',
        'processing': 'bg-info',
        'failed': 'bg-danger',
        'pending': 'bg-warning'
      }
      return classes[status] || 'bg-secondary'
    }
    
    const getStatusText = (status) => {
      const texts = {
        'completed': 'مكتمل',
        'processing': 'قيد المعالجة',
        'failed': 'فشل',
        'pending': 'قيد الانتظار'
      }
      return texts[status] || 'غير معروف'
    }
    
    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('ar-SA', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    const downloadResults = () => {
      if (!detectedImage.value) return
      
      const link = document.createElement('a')
      link.href = detectedImage.value
      link.download = `yolo-detection-${Date.now()}.jpg`
      link.click()
      
      systemStore.addNotification({
        type: 'success',
        title: 'تم التحميل',
        message: 'تم تحميل نتائج الكشف'
      })
    }
    
    const viewDetailedResults = () => {
      // فتح نافذة النتائج التفصيلية
      systemStore.addNotification({
        type: 'info',
        title: 'النتائج التفصيلية',
        message: 'يمكنك مشاهدة النتائج في القائمة الجانبية'
      })
    }
    
    const saveDetection = async () => {
      try {
        await yoloDetectionAPI.saveDetection({
          original_image: originalImage.value,
          detected_image: detectedImage.value,
          results: detectionResults.value,
          settings: detectionSettings.value
        })
        
        await yoloDetectionStore.fetchHistory()
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم الحفظ',
          message: 'تم حفظ نتائج الكشف بنجاح'
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في الحفظ',
          message: 'فشل في حفظ النتائج'
        })
      }
    }
    
    const showModelInfo = () => {
      systemStore.addNotification({
        type: 'info',
        title: 'معلومات النموذج',
        message: 'يستخدم النظام نماذج YOLO المتقدمة لكشف الكائنات بدقة عالية'
      })
    }
    
    const refreshHistory = async () => {
      await yoloDetectionStore.fetchHistory()
    }
    
    const exportHistory = async () => {
      try {
        const response = await yoloDetectionAPI.exportHistory()
        
        const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `yolo-detection-history-${new Date().toISOString().split('T')[0]}.xlsx`
        link.click()
        window.URL.revokeObjectURL(url)
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم التصدير',
          message: 'تم تصدير سجل الكشف بنجاح'
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في التصدير',
          message: 'فشل في تصدير السجل'
        })
      }
    }
    
    const viewDetection = (detection) => {
      // عرض تفاصيل الكشف
      router.push(`/diagnosis/yolo-detection/${detection.id}`)
    }
    
    const downloadDetectionResults = async (detection) => {
      try {
        const response = await yoloDetectionAPI.downloadResults(detection.id)
        
        const blob = new Blob([response.data], { type: 'application/zip' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `detection-${detection.id}.zip`
        link.click()
        window.URL.revokeObjectURL(url)
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في التحميل',
          message: 'فشل في تحميل النتائج'
        })
      }
    }
    
    const rerunDetection = (detection) => {
      // إعادة تشغيل الكشف بنفس الإعدادات
      originalImage.value = detection.original_image_url
      detectionSettings.value = { ...detectionSettings.value, ...detection.settings }
      
      systemStore.addNotification({
        type: 'info',
        title: 'تم التحميل',
        message: 'تم تحميل إعدادات الكشف السابق'
      })
    }
    
    const deleteDetection = async (detection) => {
      if (confirm(`هل أنت متأكد من حذف عملية الكشف؟`)) {
        try {
          await yoloDetectionAPI.deleteDetection(detection.id)
          await yoloDetectionStore.fetchHistory()
          
          systemStore.addNotification({
            type: 'success',
            title: 'تم الحذف',
            message: 'تم حذف عملية الكشف بنجاح'
          })
        } catch (error) {
          systemStore.addNotification({
            type: 'error',
            title: 'خطأ في الحذف',
            message: 'فشل في حذف العملية'
          })
        }
      }
    }
    
    // تحميل البيانات عند التحميل
    onMounted(async () => {
      await yoloDetectionStore.fetchStats()
      await yoloDetectionStore.fetchHistory()
    })
    
    return {
      fileInput,
      originalImageRef,
      originalImage,
      detectedImage,
      isDragOver,
      isProcessing,
      processingStatus,
      processingProgress,
      detectionSettings,
      availableClasses,
      detectionStats,
      detectionResults,
      detectionHistory,
      startNewDetection,
      handleFileSelect,
      handleDrop,
      clearDetection,
      startDetection,
      getDetectionBoxStyle,
      getConfidenceClass,
      getStatusClass,
      getStatusText,
      formatDate,
      downloadResults,
      viewDetailedResults,
      saveDetection,
      showModelInfo,
      refreshHistory,
      exportHistory,
      viewDetection,
      downloadDetectionResults,
      rerunDetection,
      deleteDetection
    }
  }
}
</script>

<style scoped>
.yolo-detection-page {
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

.detection-area {
  padding: 2rem;
}

.upload-zone {
  border: 2px dashed #e3e6f0;
  border-radius: 15px;
  padding: 3rem;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
}

.upload-zone:hover,
.upload-zone.drag-over {
  border-color: #4e73df;
  background: rgba(78, 115, 223, 0.05);
}

.upload-icon {
  font-size: 3rem;
  color: #4e73df;
  margin-bottom: 1rem;
}

.image-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 1rem;
}

.image-wrapper {
  position: relative;
  text-align: center;
}

.detection-image {
  max-width: 100%;
  max-height: 400px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.detection-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.detection-box {
  border-radius: 4px;
}

.detection-label {
  position: absolute;
  top: -25px;
  left: 0;
  background: #4e73df;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
  white-space: nowrap;
}

.confidence {
  margin-right: 0.5rem;
  opacity: 0.9;
}

.processing-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
  background: #f8f9fc;
  border-radius: 10px;
  border: 2px dashed #e3e6f0;
}

.detection-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.result-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.setting-item {
  margin-bottom: 1.5rem;
}

.setting-item:last-child {
  margin-bottom: 0;
}

.range-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #6c757d;
  margin-top: 0.25rem;
}

.classes-selection {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #e3e6f0;
  border-radius: 8px;
  padding: 1rem;
}

.detected-objects {
  max-height: 300px;
  overflow-y: auto;
}

.object-item {
  background: #f8f9fc;
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.object-item:last-child {
  margin-bottom: 0;
}

.object-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.object-name {
  font-weight: 600;
  color: #2c3e50;
}

.object-details {
  font-size: 0.8rem;
}

.detection-summary {
  border-top: 1px solid #e3e6f0;
  padding-top: 1rem;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.summary-item:last-child {
  margin-bottom: 0;
}

.summary-label {
  color: #6c757d;
}

.summary-value {
  font-weight: 600;
  color: #2c3e50;
}

.table-image {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 8px;
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
  
  .detection-area {
    padding: 1rem;
  }
  
  .image-container {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .detection-actions,
  .result-actions {
    flex-direction: column;
  }
  
  .upload-zone {
    padding: 2rem 1rem;
  }
}
</style>

