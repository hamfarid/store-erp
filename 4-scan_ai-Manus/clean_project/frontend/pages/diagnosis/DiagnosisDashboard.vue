<!-- صفحة لوحة التشخيص -->
<template>
  <div class="diagnosis-dashboard-page">
    <!-- Header -->
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h1 class="page-title">
            <i class="fas fa-stethoscope me-3"></i>
            لوحة التشخيص
          </h1>
          <p class="page-subtitle">تشخيص أمراض النباتات باستخدام الذكاء الاصطناعي</p>
        </div>
        <div class="page-actions">
          <button class="btn btn-primary" @click="startNewDiagnosis">
            <i class="fas fa-plus me-2"></i>
            تشخيص جديد
          </button>
        </div>
      </div>
    </div>

    <!-- إحصائيات سريعة -->
    <div class="row mb-4">
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card primary">
          <div class="stat-icon">
            <i class="fas fa-microscope"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ diagnosisStats.total_diagnoses || 0 }}</div>
            <div class="stat-label">إجمالي التشخيصات</div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card success">
          <div class="stat-icon">
            <i class="fas fa-check-circle"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ diagnosisStats.successful_diagnoses || 0 }}</div>
            <div class="stat-label">تشخيصات ناجحة</div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card info">
          <div class="stat-icon">
            <i class="fas fa-leaf"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ diagnosisStats.plant_types || 0 }}</div>
            <div class="stat-label">أنواع النباتات</div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card warning">
          <div class="stat-icon">
            <i class="fas fa-bug"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ diagnosisStats.diseases_detected || 0 }}</div>
            <div class="stat-label">الأمراض المكتشفة</div>
          </div>
        </div>
      </div>
    </div>

    <!-- أدوات التشخيص -->
    <div class="row mb-4">
      <div class="col-lg-8">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="fas fa-upload me-2"></i>
              رفع صورة للتشخيص
            </h5>
          </div>
          <div class="card-body">
            <div class="upload-area" 
                 @drop="handleDrop" 
                 @dragover.prevent 
                 @dragenter.prevent
                 :class="{ 'drag-over': isDragOver }"
                 @dragenter="isDragOver = true"
                 @dragleave="isDragOver = false">
              
              <div class="upload-content" v-if="!selectedImage">
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
              
              <div class="image-preview" v-if="selectedImage">
                <img :src="selectedImage" alt="الصورة المختارة" class="preview-image">
                <div class="image-actions">
                  <button class="btn btn-success" @click="startDiagnosis" :disabled="isProcessing">
                    <i v-if="isProcessing" class="fas fa-spinner fa-spin me-2"></i>
                    <i v-else class="fas fa-play me-2"></i>
                    {{ isProcessing ? 'جاري التشخيص...' : 'بدء التشخيص' }}
                  </button>
                  <button class="btn btn-outline-secondary" @click="clearImage">
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
              إعدادات التشخيص
            </h5>
          </div>
          <div class="card-body">
            <div class="setting-item">
              <label class="form-label">نوع النبات</label>
              <select class="form-select" v-model="diagnosisSettings.plant_type">
                <option value="">تحديد تلقائي</option>
                <option value="tomato">طماطم</option>
                <option value="potato">بطاطس</option>
                <option value="corn">ذرة</option>
                <option value="wheat">قمح</option>
                <option value="rice">أرز</option>
                <option value="other">أخرى</option>
              </select>
            </div>
            
            <div class="setting-item">
              <label class="form-label">مستوى التفصيل</label>
              <select class="form-select" v-model="diagnosisSettings.detail_level">
                <option value="basic">أساسي</option>
                <option value="detailed">مفصل</option>
                <option value="expert">خبير</option>
              </select>
            </div>
            
            <div class="setting-item">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" v-model="diagnosisSettings.include_treatment">
                <label class="form-check-label">تضمين خطة العلاج</label>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" v-model="diagnosisSettings.save_history">
                <label class="form-check-label">حفظ في السجل</label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- نتائج التشخيص -->
    <div class="row mb-4" v-if="diagnosisResult">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="fas fa-clipboard-list me-2"></i>
              نتائج التشخيص
            </h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-lg-6">
                <div class="result-section">
                  <h6>التشخيص الأساسي</h6>
                  <div class="diagnosis-item">
                    <div class="diagnosis-header">
                      <span class="diagnosis-name">{{ diagnosisResult.disease_name }}</span>
                      <span class="confidence-badge" :class="getConfidenceClass(diagnosisResult.confidence)">
                        {{ diagnosisResult.confidence }}% ثقة
                      </span>
                    </div>
                    <p class="diagnosis-description">{{ diagnosisResult.description }}</p>
                  </div>
                </div>
                
                <div class="result-section" v-if="diagnosisResult.alternative_diagnoses">
                  <h6>تشخيصات بديلة</h6>
                  <div class="diagnosis-item" v-for="alt in diagnosisResult.alternative_diagnoses" :key="alt.id">
                    <div class="diagnosis-header">
                      <span class="diagnosis-name">{{ alt.disease_name }}</span>
                      <span class="confidence-badge" :class="getConfidenceClass(alt.confidence)">
                        {{ alt.confidence }}% ثقة
                      </span>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="col-lg-6">
                <div class="result-section" v-if="diagnosisResult.treatment_plan">
                  <h6>خطة العلاج</h6>
                  <div class="treatment-steps">
                    <div class="treatment-step" v-for="(step, index) in diagnosisResult.treatment_plan" :key="index">
                      <div class="step-number">{{ index + 1 }}</div>
                      <div class="step-content">
                        <h6>{{ step.title }}</h6>
                        <p>{{ step.description }}</p>
                        <small class="text-muted">{{ step.duration }}</small>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="result-actions">
                  <button class="btn btn-primary" @click="saveDiagnosis">
                    <i class="fas fa-save me-2"></i>
                    حفظ التشخيص
                  </button>
                  <button class="btn btn-outline-info" @click="exportReport">
                    <i class="fas fa-download me-2"></i>
                    تصدير التقرير
                  </button>
                  <button class="btn btn-outline-success" @click="shareResult">
                    <i class="fas fa-share me-2"></i>
                    مشاركة
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- سجل التشخيصات السابقة -->
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">
                <i class="fas fa-history me-2"></i>
                التشخيصات السابقة
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
                    <th>نوع النبات</th>
                    <th>التشخيص</th>
                    <th>مستوى الثقة</th>
                    <th>الحالة</th>
                    <th>الإجراءات</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="diagnosis in diagnosisHistory" :key="diagnosis.id">
                    <td>{{ formatDate(diagnosis.created_at) }}</td>
                    <td>
                      <img :src="diagnosis.image_thumbnail" alt="صورة" class="table-image">
                    </td>
                    <td>{{ diagnosis.plant_type || 'غير محدد' }}</td>
                    <td>{{ diagnosis.disease_name }}</td>
                    <td>
                      <span class="confidence-badge" :class="getConfidenceClass(diagnosis.confidence)">
                        {{ diagnosis.confidence }}%
                      </span>
                    </td>
                    <td>
                      <span class="badge" :class="getStatusClass(diagnosis.status)">
                        {{ getStatusText(diagnosis.status) }}
                      </span>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-info" @click="viewDiagnosis(diagnosis)">
                          <i class="fas fa-eye"></i>
                        </button>
                        <button class="btn btn-outline-primary" @click="downloadReport(diagnosis)">
                          <i class="fas fa-download"></i>
                        </button>
                        <button class="btn btn-outline-danger" @click="deleteDiagnosis(diagnosis)">
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
import { useDiagnosisStore, useSystemStore } from '../../store/index.js'
import { diagnosisAPI } from '../../services/api.js'

export default {
  name: 'DiagnosisDashboard',
  
  setup() {
    const router = useRouter()
    const diagnosisStore = useDiagnosisStore()
    const systemStore = useSystemStore()
    
    const fileInput = ref(null)
    const selectedImage = ref(null)
    const isDragOver = ref(false)
    const isProcessing = ref(false)
    
    const diagnosisSettings = ref({
      plant_type: '',
      detail_level: 'detailed',
      include_treatment: true,
      save_history: true
    })
    
    // البيانات المحسوبة
    const diagnosisStats = computed(() => diagnosisStore.stats)
    const diagnosisResult = computed(() => diagnosisStore.currentResult)
    const diagnosisHistory = computed(() => diagnosisStore.history)
    
    // الوظائف
    const startNewDiagnosis = () => {
      selectedImage.value = null
      diagnosisStore.clearCurrentResult()
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
        selectedImage.value = e.target.result
      }
      reader.readAsDataURL(file)
    }
    
    const clearImage = () => {
      selectedImage.value = null
      diagnosisStore.clearCurrentResult()
      if (fileInput.value) {
        fileInput.value.value = ''
      }
    }
    
    const startDiagnosis = async () => {
      if (!selectedImage.value) return
      
      isProcessing.value = true
      
      try {
        const formData = new FormData()
        
        // تحويل base64 إلى blob
        const response = await fetch(selectedImage.value)
        const blob = await response.blob()
        formData.append('image', blob, 'diagnosis-image.jpg')
        formData.append('settings', JSON.stringify(diagnosisSettings.value))
        
        const result = await diagnosisAPI.performDiagnosis(formData)
        diagnosisStore.setCurrentResult(result.data)
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم التشخيص',
          message: 'تم إجراء التشخيص بنجاح'
        })
        
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في التشخيص',
          message: 'فشل في إجراء التشخيص'
        })
      } finally {
        isProcessing.value = false
      }
    }
    
    const getConfidenceClass = (confidence) => {
      if (confidence >= 90) return 'high-confidence'
      if (confidence >= 70) return 'medium-confidence'
      return 'low-confidence'
    }
    
    const getStatusClass = (status) => {
      const classes = {
        'completed': 'bg-success',
        'pending': 'bg-warning',
        'failed': 'bg-danger',
        'processing': 'bg-info'
      }
      return classes[status] || 'bg-secondary'
    }
    
    const getStatusText = (status) => {
      const texts = {
        'completed': 'مكتمل',
        'pending': 'قيد الانتظار',
        'failed': 'فشل',
        'processing': 'قيد المعالجة'
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
    
    const saveDiagnosis = async () => {
      try {
        await diagnosisAPI.saveDiagnosis(diagnosisResult.value)
        await diagnosisStore.fetchHistory()
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم الحفظ',
          message: 'تم حفظ التشخيص بنجاح'
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في الحفظ',
          message: 'فشل في حفظ التشخيص'
        })
      }
    }
    
    const exportReport = () => {
      if (!diagnosisResult.value) return
      
      const reportData = {
        diagnosis: diagnosisResult.value,
        timestamp: new Date().toISOString(),
        settings: diagnosisSettings.value
      }
      
      const dataStr = JSON.stringify(reportData, null, 2)
      const dataBlob = new Blob([dataStr], { type: 'application/json' })
      const url = URL.createObjectURL(dataBlob)
      
      const link = document.createElement('a')
      link.href = url
      link.download = `diagnosis-report-${new Date().toISOString().split('T')[0]}.json`
      link.click()
      
      URL.revokeObjectURL(url)
    }
    
    const shareResult = () => {
      if (navigator.share && diagnosisResult.value) {
        navigator.share({
          title: 'نتيجة التشخيص',
          text: `تم تشخيص: ${diagnosisResult.value.disease_name} بثقة ${diagnosisResult.value.confidence}%`,
          url: window.location.href
        })
      } else {
        // نسخ الرابط
        navigator.clipboard.writeText(window.location.href)
        systemStore.addNotification({
          type: 'success',
          title: 'تم النسخ',
          message: 'تم نسخ رابط النتيجة'
        })
      }
    }
    
    const refreshHistory = async () => {
      await diagnosisStore.fetchHistory()
    }
    
    const exportHistory = async () => {
      try {
        const response = await diagnosisAPI.exportHistory()
        
        const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `diagnosis-history-${new Date().toISOString().split('T')[0]}.xlsx`
        link.click()
        window.URL.revokeObjectURL(url)
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم التصدير',
          message: 'تم تصدير سجل التشخيصات بنجاح'
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في التصدير',
          message: 'فشل في تصدير السجل'
        })
      }
    }
    
    const viewDiagnosis = (diagnosis) => {
      diagnosisStore.setCurrentResult(diagnosis)
    }
    
    const downloadReport = async (diagnosis) => {
      try {
        const response = await diagnosisAPI.downloadReport(diagnosis.id)
        
        const blob = new Blob([response.data], { type: 'application/pdf' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `diagnosis-${diagnosis.id}.pdf`
        link.click()
        window.URL.revokeObjectURL(url)
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في التحميل',
          message: 'فشل في تحميل التقرير'
        })
      }
    }
    
    const deleteDiagnosis = async (diagnosis) => {
      if (confirm(`هل أنت متأكد من حذف التشخيص؟`)) {
        try {
          await diagnosisAPI.deleteDiagnosis(diagnosis.id)
          await diagnosisStore.fetchHistory()
          
          systemStore.addNotification({
            type: 'success',
            title: 'تم الحذف',
            message: 'تم حذف التشخيص بنجاح'
          })
        } catch (error) {
          systemStore.addNotification({
            type: 'error',
            title: 'خطأ في الحذف',
            message: 'فشل في حذف التشخيص'
          })
        }
      }
    }
    
    // تحميل البيانات عند التحميل
    onMounted(async () => {
      await diagnosisStore.fetchStats()
      await diagnosisStore.fetchHistory()
    })
    
    return {
      fileInput,
      selectedImage,
      isDragOver,
      isProcessing,
      diagnosisSettings,
      diagnosisStats,
      diagnosisResult,
      diagnosisHistory,
      startNewDiagnosis,
      handleFileSelect,
      handleDrop,
      clearImage,
      startDiagnosis,
      getConfidenceClass,
      getStatusClass,
      getStatusText,
      formatDate,
      saveDiagnosis,
      exportReport,
      shareResult,
      refreshHistory,
      exportHistory,
      viewDiagnosis,
      downloadReport,
      deleteDiagnosis
    }
  }
}
</script>

<style scoped>
.diagnosis-dashboard-page {
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

.upload-area {
  border: 2px dashed #e3e6f0;
  border-radius: 15px;
  padding: 3rem;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
}

.upload-area:hover,
.upload-area.drag-over {
  border-color: #4e73df;
  background: rgba(78, 115, 223, 0.05);
}

.upload-icon {
  font-size: 3rem;
  color: #4e73df;
  margin-bottom: 1rem;
}

.image-preview {
  position: relative;
}

.preview-image {
  max-width: 100%;
  max-height: 400px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.image-actions {
  margin-top: 1rem;
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.setting-item {
  margin-bottom: 1.5rem;
}

.setting-item:last-child {
  margin-bottom: 0;
}

.result-section {
  margin-bottom: 2rem;
}

.result-section h6 {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 1rem;
  border-bottom: 2px solid #e3e6f0;
  padding-bottom: 0.5rem;
}

.diagnosis-item {
  background: #f8f9fc;
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.diagnosis-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.diagnosis-name {
  font-weight: 600;
  color: #2c3e50;
}

.confidence-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  color: white;
}

.confidence-badge.high-confidence {
  background: #1cc88a;
}

.confidence-badge.medium-confidence {
  background: #f6c23e;
}

.confidence-badge.low-confidence {
  background: #e74a3b;
}

.diagnosis-description {
  color: #6c757d;
  margin-bottom: 0;
  line-height: 1.5;
}

.treatment-steps {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.treatment-step {
  display: flex;
  align-items: flex-start;
  background: #f8f9fc;
  border-radius: 10px;
  padding: 1rem;
}

.step-number {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #4e73df;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin-left: 1rem;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-content h6 {
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.step-content p {
  margin-bottom: 0.25rem;
  color: #6c757d;
}

.result-actions {
  margin-top: 2rem;
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
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
  
  .upload-area {
    padding: 2rem 1rem;
  }
  
  .image-actions {
    flex-direction: column;
  }
  
  .result-actions {
    flex-direction: column;
  }
  
  .treatment-step {
    flex-direction: column;
    text-align: center;
  }
  
  .step-number {
    margin: 0 auto 1rem auto;
  }
}
</style>

