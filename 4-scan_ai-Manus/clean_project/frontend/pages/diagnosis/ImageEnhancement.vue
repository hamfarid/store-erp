<!-- صفحة تحسين الصور -->
<template>
  <div class="image-enhancement-page">
    <!-- Header -->
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h1 class="page-title">
            <i class="fas fa-image me-3"></i>
            تحسين الصور
          </h1>
          <p class="page-subtitle">تحسين جودة الصور باستخدام تقنيات الذكاء الاصطناعي المتقدمة</p>
        </div>
        <div class="page-actions">
          <button class="btn btn-outline-primary" @click="showPresets">
            <i class="fas fa-magic me-2"></i>
            الإعدادات المسبقة
          </button>
          <button class="btn btn-primary" @click="startNewEnhancement">
            <i class="fas fa-plus me-2"></i>
            تحسين جديد
          </button>
        </div>
      </div>
    </div>

    <!-- إحصائيات سريعة -->
    <div class="row mb-4">
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card primary">
          <div class="stat-icon">
            <i class="fas fa-images"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ enhancementStats.total_processed || 0 }}</div>
            <div class="stat-label">الصور المعالجة</div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card success">
          <div class="stat-icon">
            <i class="fas fa-check-circle"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ enhancementStats.success_rate || 0 }}%</div>
            <div class="stat-label">معدل النجاح</div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card info">
          <div class="stat-icon">
            <i class="fas fa-clock"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ enhancementStats.avg_processing_time || 0 }}s</div>
            <div class="stat-label">متوسط وقت المعالجة</div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="stat-card warning">
          <div class="stat-icon">
            <i class="fas fa-chart-line"></i>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ enhancementStats.quality_improvement || 0 }}%</div>
            <div class="stat-label">تحسن الجودة</div>
          </div>
        </div>
      </div>
    </div>

    <!-- منطقة التحسين الرئيسية -->
    <div class="row mb-4">
      <div class="col-lg-8">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">
              <i class="fas fa-upload me-2"></i>
              رفع الصورة للتحسين
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
              
              <div class="upload-content" v-if="!originalImage">
                <i class="fas fa-cloud-upload-alt upload-icon"></i>
                <h6>اسحب الصورة هنا أو انقر للاختيار</h6>
                <p class="text-muted">يدعم النظام صيغ JPG, PNG, WEBP, TIFF</p>
                <input type="file" 
                       ref="fileInput" 
                       @change="handleFileSelect" 
                       accept="image/*" 
                       class="d-none">
                <button class="btn btn-outline-primary" @click="$refs.fileInput.click()">
                  اختيار صورة
                </button>
              </div>
              
              <div class="image-comparison" v-if="originalImage">
                <div class="comparison-container">
                  <div class="image-side">
                    <h6>الصورة الأصلية</h6>
                    <img :src="originalImage" alt="الصورة الأصلية" class="comparison-image">
                    <div class="image-info">
                      <small class="text-muted">{{ originalImageInfo }}</small>
                    </div>
                  </div>
                  
                  <div class="image-side" v-if="enhancedImage">
                    <h6>الصورة المحسنة</h6>
                    <img :src="enhancedImage" alt="الصورة المحسنة" class="comparison-image">
                    <div class="image-info">
                      <small class="text-success">{{ enhancedImageInfo }}</small>
                    </div>
                  </div>
                  
                  <div class="image-side processing" v-else-if="isProcessing">
                    <h6>جاري التحسين...</h6>
                    <div class="processing-placeholder">
                      <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">جاري التحميل...</span>
                      </div>
                      <p class="mt-3">{{ processingStatus }}</p>
                    </div>
                  </div>
                </div>
                
                <div class="image-actions mt-3">
                  <button class="btn btn-success" 
                          @click="startEnhancement" 
                          :disabled="isProcessing"
                          v-if="!enhancedImage">
                    <i v-if="isProcessing" class="fas fa-spinner fa-spin me-2"></i>
                    <i v-else class="fas fa-magic me-2"></i>
                    {{ isProcessing ? 'جاري التحسين...' : 'بدء التحسين' }}
                  </button>
                  
                  <div v-if="enhancedImage" class="enhanced-actions">
                    <button class="btn btn-primary" @click="downloadEnhanced">
                      <i class="fas fa-download me-2"></i>
                      تحميل الصورة المحسنة
                    </button>
                    <button class="btn btn-outline-info" @click="compareImages">
                      <i class="fas fa-eye me-2"></i>
                      مقارنة تفصيلية
                    </button>
                    <button class="btn btn-outline-success" @click="saveToGallery">
                      <i class="fas fa-save me-2"></i>
                      حفظ في المعرض
                    </button>
                  </div>
                  
                  <button class="btn btn-outline-secondary" @click="clearImages">
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
              <i class="fas fa-sliders-h me-2"></i>
              إعدادات التحسين
            </h5>
          </div>
          <div class="card-body">
            <div class="setting-item">
              <label class="form-label">نوع التحسين</label>
              <select class="form-select" v-model="enhancementSettings.type">
                <option value="auto">تلقائي</option>
                <option value="denoise">إزالة التشويش</option>
                <option value="sharpen">زيادة الحدة</option>
                <option value="upscale">تكبير الحجم</option>
                <option value="color_enhance">تحسين الألوان</option>
                <option value="low_light">تحسين الإضاءة المنخفضة</option>
                <option value="super_resolution">دقة فائقة</option>
              </select>
            </div>
            
            <div class="setting-item">
              <label class="form-label">مستوى التحسين</label>
              <input type="range" 
                     class="form-range" 
                     min="1" 
                     max="10" 
                     v-model="enhancementSettings.intensity">
              <div class="range-labels">
                <span>خفيف</span>
                <span>{{ enhancementSettings.intensity }}</span>
                <span>قوي</span>
              </div>
            </div>
            
            <div class="setting-item" v-if="enhancementSettings.type === 'upscale'">
              <label class="form-label">معامل التكبير</label>
              <select class="form-select" v-model="enhancementSettings.scale_factor">
                <option value="2">2x</option>
                <option value="4">4x</option>
                <option value="8">8x</option>
              </select>
            </div>
            
            <div class="setting-item">
              <label class="form-label">تنسيق الإخراج</label>
              <select class="form-select" v-model="enhancementSettings.output_format">
                <option value="jpg">JPEG</option>
                <option value="png">PNG</option>
                <option value="webp">WebP</option>
                <option value="tiff">TIFF</option>
              </select>
            </div>
            
            <div class="setting-item">
              <label class="form-label">جودة الإخراج</label>
              <input type="range" 
                     class="form-range" 
                     min="50" 
                     max="100" 
                     v-model="enhancementSettings.quality">
              <div class="range-labels">
                <span>50%</span>
                <span>{{ enhancementSettings.quality }}%</span>
                <span>100%</span>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" v-model="enhancementSettings.preserve_metadata">
                <label class="form-check-label">الاحتفاظ بالبيانات الوصفية</label>
              </div>
            </div>
            
            <div class="setting-item">
              <div class="form-check">
                <input class="form-check-input" type="checkbox" v-model="enhancementSettings.batch_mode">
                <label class="form-check-label">وضع المعالجة المجمعة</label>
              </div>
            </div>
          </div>
        </div>
        
        <!-- الإعدادات المسبقة -->
        <div class="card mt-3">
          <div class="card-header">
            <h6 class="card-title mb-0">
              <i class="fas fa-bookmark me-2"></i>
              الإعدادات المسبقة
            </h6>
          </div>
          <div class="card-body">
            <div class="preset-item" v-for="preset in presets" :key="preset.id" @click="applyPreset(preset)">
              <div class="preset-icon">
                <i :class="preset.icon"></i>
              </div>
              <div class="preset-info">
                <div class="preset-name">{{ preset.name }}</div>
                <div class="preset-description">{{ preset.description }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- معرض الصور المحسنة -->
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">
                <i class="fas fa-images me-2"></i>
                معرض الصور المحسنة
              </h5>
              <div class="card-actions">
                <button class="btn btn-sm btn-outline-primary" @click="refreshGallery">
                  <i class="fas fa-sync-alt"></i>
                </button>
                <button class="btn btn-sm btn-outline-success" @click="exportGallery">
                  <i class="fas fa-download"></i>
                </button>
              </div>
            </div>
          </div>
          <div class="card-body">
            <div class="gallery-grid">
              <div class="gallery-item" v-for="item in gallery" :key="item.id" @click="viewGalleryItem(item)">
                <div class="gallery-image">
                  <img :src="item.thumbnail" :alt="item.name" loading="lazy">
                  <div class="gallery-overlay">
                    <div class="gallery-actions">
                      <button class="btn btn-sm btn-light" @click.stop="downloadGalleryItem(item)">
                        <i class="fas fa-download"></i>
                      </button>
                      <button class="btn btn-sm btn-light" @click.stop="shareGalleryItem(item)">
                        <i class="fas fa-share"></i>
                      </button>
                      <button class="btn btn-sm btn-danger" @click.stop="deleteGalleryItem(item)">
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </div>
                </div>
                <div class="gallery-info">
                  <div class="gallery-name">{{ item.name }}</div>
                  <div class="gallery-meta">
                    <small class="text-muted">{{ formatDate(item.created_at) }}</small>
                    <span class="badge bg-primary">{{ item.enhancement_type }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="text-center mt-4" v-if="gallery.length === 0">
              <i class="fas fa-images text-muted" style="font-size: 3rem;"></i>
              <p class="text-muted mt-3">لا توجد صور محسنة بعد</p>
              <button class="btn btn-primary" @click="startNewEnhancement">
                <i class="fas fa-plus me-2"></i>
                ابدأ التحسين الأول
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
import { useImageEnhancementStore, useSystemStore } from '../../store/index.js'
import { imageEnhancementAPI } from '../../services/api.js'

export default {
  name: 'ImageEnhancement',
  
  setup() {
    const router = useRouter()
    const imageEnhancementStore = useImageEnhancementStore()
    const systemStore = useSystemStore()
    
    const fileInput = ref(null)
    const originalImage = ref(null)
    const enhancedImage = ref(null)
    const isDragOver = ref(false)
    const isProcessing = ref(false)
    const processingStatus = ref('')
    const originalImageInfo = ref('')
    const enhancedImageInfo = ref('')
    
    const enhancementSettings = ref({
      type: 'auto',
      intensity: 5,
      scale_factor: 2,
      output_format: 'jpg',
      quality: 95,
      preserve_metadata: true,
      batch_mode: false
    })
    
    const presets = ref([
      {
        id: 1,
        name: 'صور شخصية',
        description: 'تحسين الصور الشخصية والبورتريه',
        icon: 'fas fa-user',
        settings: { type: 'auto', intensity: 6, quality: 95 }
      },
      {
        id: 2,
        name: 'صور المناظر الطبيعية',
        description: 'تحسين صور الطبيعة والمناظر',
        icon: 'fas fa-mountain',
        settings: { type: 'color_enhance', intensity: 7, quality: 90 }
      },
      {
        id: 3,
        name: 'صور قديمة',
        description: 'ترميم وتحسين الصور القديمة',
        icon: 'fas fa-history',
        settings: { type: 'denoise', intensity: 8, quality: 95 }
      },
      {
        id: 4,
        name: 'صور ليلية',
        description: 'تحسين الصور المأخوذة في الإضاءة المنخفضة',
        icon: 'fas fa-moon',
        settings: { type: 'low_light', intensity: 9, quality: 90 }
      }
    ])
    
    // البيانات المحسوبة
    const enhancementStats = computed(() => imageEnhancementStore.stats)
    const gallery = computed(() => imageEnhancementStore.gallery)
    
    // الوظائف
    const startNewEnhancement = () => {
      clearImages()
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
        
        // معلومات الصورة الأصلية
        const img = new Image()
        img.onload = () => {
          originalImageInfo.value = `${img.width} × ${img.height} بكسل`
        }
        img.src = e.target.result
      }
      reader.readAsDataURL(file)
    }
    
    const clearImages = () => {
      originalImage.value = null
      enhancedImage.value = null
      originalImageInfo.value = ''
      enhancedImageInfo.value = ''
      if (fileInput.value) {
        fileInput.value.value = ''
      }
    }
    
    const startEnhancement = async () => {
      if (!originalImage.value) return
      
      isProcessing.value = true
      processingStatus.value = 'تحضير الصورة...'
      
      try {
        const formData = new FormData()
        
        // تحويل base64 إلى blob
        const response = await fetch(originalImage.value)
        const blob = await response.blob()
        formData.append('image', blob, 'image.jpg')
        formData.append('settings', JSON.stringify(enhancementSettings.value))
        
        // تحديث حالة المعالجة
        processingStatus.value = 'تطبيق خوارزميات التحسين...'
        
        const result = await imageEnhancementAPI.enhanceImage(formData)
        
        enhancedImage.value = result.data.enhanced_image_url
        enhancedImageInfo.value = result.data.image_info
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم التحسين',
          message: 'تم تحسين الصورة بنجاح'
        })
        
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في التحسين',
          message: 'فشل في تحسين الصورة'
        })
      } finally {
        isProcessing.value = false
        processingStatus.value = ''
      }
    }
    
    const applyPreset = (preset) => {
      enhancementSettings.value = { ...enhancementSettings.value, ...preset.settings }
      
      systemStore.addNotification({
        type: 'info',
        title: 'تم تطبيق الإعداد المسبق',
        message: `تم تطبيق إعدادات ${preset.name}`
      })
    }
    
    const downloadEnhanced = () => {
      if (!enhancedImage.value) return
      
      const link = document.createElement('a')
      link.href = enhancedImage.value
      link.download = `enhanced-image-${Date.now()}.${enhancementSettings.value.output_format}`
      link.click()
      
      systemStore.addNotification({
        type: 'success',
        title: 'تم التحميل',
        message: 'تم تحميل الصورة المحسنة'
      })
    }
    
    const compareImages = () => {
      // فتح نافذة مقارنة تفصيلية
      systemStore.addNotification({
        type: 'info',
        title: 'قريباً',
        message: 'ستتوفر أداة المقارنة التفصيلية قريباً'
      })
    }
    
    const saveToGallery = async () => {
      try {
        await imageEnhancementAPI.saveToGallery({
          original_image: originalImage.value,
          enhanced_image: enhancedImage.value,
          settings: enhancementSettings.value
        })
        
        await imageEnhancementStore.fetchGallery()
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم الحفظ',
          message: 'تم حفظ الصورة في المعرض'
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في الحفظ',
          message: 'فشل في حفظ الصورة'
        })
      }
    }
    
    const showPresets = () => {
      systemStore.addNotification({
        type: 'info',
        title: 'الإعدادات المسبقة',
        message: 'اختر إعداداً مسبقاً من القائمة الجانبية'
      })
    }
    
    const refreshGallery = async () => {
      await imageEnhancementStore.fetchGallery()
    }
    
    const exportGallery = async () => {
      try {
        const response = await imageEnhancementAPI.exportGallery()
        
        const blob = new Blob([response.data], { type: 'application/zip' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `enhanced-images-gallery-${new Date().toISOString().split('T')[0]}.zip`
        link.click()
        window.URL.revokeObjectURL(url)
        
        systemStore.addNotification({
          type: 'success',
          title: 'تم التصدير',
          message: 'تم تصدير المعرض بنجاح'
        })
      } catch (error) {
        systemStore.addNotification({
          type: 'error',
          title: 'خطأ في التصدير',
          message: 'فشل في تصدير المعرض'
        })
      }
    }
    
    const viewGalleryItem = (item) => {
      // فتح الصورة في عارض مكبر
      window.open(item.enhanced_image_url, '_blank')
    }
    
    const downloadGalleryItem = (item) => {
      const link = document.createElement('a')
      link.href = item.enhanced_image_url
      link.download = item.name
      link.click()
    }
    
    const shareGalleryItem = (item) => {
      if (navigator.share) {
        navigator.share({
          title: item.name,
          text: 'صورة محسنة من Gaara Scan AI',
          url: item.enhanced_image_url
        })
      } else {
        navigator.clipboard.writeText(item.enhanced_image_url)
        systemStore.addNotification({
          type: 'success',
          title: 'تم النسخ',
          message: 'تم نسخ رابط الصورة'
        })
      }
    }
    
    const deleteGalleryItem = async (item) => {
      if (confirm(`هل أنت متأكد من حذف ${item.name}؟`)) {
        try {
          await imageEnhancementAPI.deleteGalleryItem(item.id)
          await imageEnhancementStore.fetchGallery()
          
          systemStore.addNotification({
            type: 'success',
            title: 'تم الحذف',
            message: 'تم حذف الصورة من المعرض'
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
    
    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('ar-SA', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }
    
    // تحميل البيانات عند التحميل
    onMounted(async () => {
      await imageEnhancementStore.fetchStats()
      await imageEnhancementStore.fetchGallery()
    })
    
    return {
      fileInput,
      originalImage,
      enhancedImage,
      isDragOver,
      isProcessing,
      processingStatus,
      originalImageInfo,
      enhancedImageInfo,
      enhancementSettings,
      presets,
      enhancementStats,
      gallery,
      startNewEnhancement,
      handleFileSelect,
      handleDrop,
      clearImages,
      startEnhancement,
      applyPreset,
      downloadEnhanced,
      compareImages,
      saveToGallery,
      showPresets,
      refreshGallery,
      exportGallery,
      viewGalleryItem,
      downloadGalleryItem,
      shareGalleryItem,
      deleteGalleryItem,
      formatDate
    }
  }
}
</script>

<style scoped>
.image-enhancement-page {
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
  padding: 2rem;
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

.image-comparison {
  display: flex;
  flex-direction: column;
}

.comparison-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 1rem;
}

.image-side {
  text-align: center;
}

.image-side h6 {
  margin-bottom: 1rem;
  font-weight: 600;
  color: #2c3e50;
}

.comparison-image {
  max-width: 100%;
  max-height: 300px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.image-info {
  margin-top: 0.5rem;
}

.processing-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  background: #f8f9fc;
  border-radius: 10px;
  border: 2px dashed #e3e6f0;
}

.image-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.enhanced-actions {
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

.preset-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-radius: 10px;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.preset-item:hover {
  background: #f8f9fc;
  border-color: #e3e6f0;
}

.preset-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(45deg, #4e73df, #224abe);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-left: 1rem;
}

.preset-info {
  flex: 1;
}

.preset-name {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.preset-description {
  font-size: 0.8rem;
  color: #6c757d;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.gallery-item {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  cursor: pointer;
}

.gallery-item:hover {
  transform: translateY(-5px);
}

.gallery-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.gallery-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.gallery-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.gallery-item:hover .gallery-overlay {
  opacity: 1;
}

.gallery-actions {
  display: flex;
  gap: 0.5rem;
}

.gallery-info {
  padding: 1rem;
}

.gallery-name {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.gallery-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
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
  
  .comparison-container {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .image-actions,
  .enhanced-actions {
    flex-direction: column;
  }
  
  .gallery-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
  }
  
  .preset-item {
    flex-direction: column;
    text-align: center;
  }
  
  .preset-icon {
    margin: 0 0 1rem 0;
  }
}
</style>

