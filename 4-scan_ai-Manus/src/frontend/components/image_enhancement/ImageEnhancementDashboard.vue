<template>
  <div class="image-enhancement-dashboard">
    <!-- Header -->
    <div class="dashboard-header">
      <h2 class="title">
        <i class="fas fa-magic"></i>
        تحسين الصور المتقدم
      </h2>
      <div class="status-indicator" :class="serviceStatus">
        <span class="status-dot"></span>
        {{ serviceStatusText }}
      </div>
    </div>

    <!-- Upload Section -->
    <div class="upload-section">
      <div class="upload-area" @drop="handleDrop" @dragover.prevent @dragenter.prevent>
        <input 
          type="file" 
          ref="fileInput" 
          @change="handleFileSelect" 
          accept="image/*" 
          multiple 
          style="display: none"
        >
        <div class="upload-content" @click="$refs.fileInput.click()">
          <i class="fas fa-image"></i>
          <p>اسحب الصور هنا أو انقر للاختيار</p>
          <small>يدعم: JPG, PNG, BMP</small>
        </div>
      </div>
    </div>

    <!-- Enhancement Settings -->
    <div class="settings-panel">
      <div class="setting-group">
        <label>طريقة التحسين:</label>
        <select v-model="selectedMethod" @change="updateMethod">
          <option v-for="method in availableMethods" :key="method.key" :value="method.key">
            {{ method.name }}
          </option>
        </select>
        <small class="method-description">{{ getMethodDescription(selectedMethod) }}</small>
      </div>
      
      <div class="setting-group" v-if="needsFactor">
        <label>معامل التحسين:</label>
        <input 
          type="range" 
          v-model="enhancementFactor" 
          min="0.5" 
          max="3.0" 
          step="0.1"
          @input="updateFactor"
        >
        <span class="factor-value">{{ enhancementFactor }}</span>
      </div>

      <div class="setting-group">
        <label>
          <input type="checkbox" v-model="returnBase64">
          إرجاع كـ Base64
        </label>
      </div>
    </div>

    <!-- Before/After Comparison -->
    <div class="comparison-section" v-if="enhancementResults.length > 0">
      <h3>نتائج التحسين</h3>
      <div class="results-grid">
        <div 
          v-for="(result, index) in enhancementResults" 
          :key="index" 
          class="result-card"
        >
          <div class="comparison-container">
            <!-- Original Image -->
            <div class="image-side">
              <h4>الصورة الأصلية</h4>
              <img :src="result.originalUrl" :alt="result.filename" />
            </div>
            
            <!-- Enhanced Image -->
            <div class="image-side">
              <h4>الصورة المحسنة</h4>
              <img :src="result.enhancedUrl" :alt="result.filename + ' - محسنة'" />
            </div>
          </div>
          
          <div class="result-info">
            <h4>{{ result.filename }}</h4>
            <p>الطريقة المستخدمة: {{ getMethodDisplayName(result.method_used) }}</p>
            <p v-if="result.factor">معامل التحسين: {{ result.factor }}</p>
            
            <div class="action-buttons">
              <button @click="downloadEnhanced(result)" class="btn btn-primary">
                <i class="fas fa-download"></i>
                تحميل المحسنة
              </button>
              <button @click="compareImages(result)" class="btn btn-secondary">
                <i class="fas fa-eye"></i>
                مقارنة تفصيلية
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Batch Processing -->
    <div class="batch-section" v-if="selectedImages.length > 1">
      <h3>معالجة دفعية</h3>
      <div class="batch-controls">
        <button @click="enhanceAllImages" class="btn btn-success" :disabled="isProcessing">
          <i class="fas fa-play"></i>
          تحسين جميع الصور
        </button>
        <button @click="clearResults" class="btn btn-warning">
          <i class="fas fa-trash"></i>
          مسح النتائج
        </button>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="isProcessing" class="loading-overlay">
      <div class="loading-content">
        <div class="spinner"></div>
        <p>جاري تحسين الصور...</p>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
        </div>
        <p>{{ processedCount }} من {{ totalCount }}</p>
      </div>
    </div>

    <!-- Image Comparison Modal -->
    <div v-if="showComparison" class="modal-overlay" @click="closeComparison">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>مقارنة تفصيلية</h3>
          <button @click="closeComparison" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="comparison-slider">
            <div class="slider-container">
              <img :src="comparisonResult.originalUrl" class="comparison-original" />
              <img :src="comparisonResult.enhancedUrl" class="comparison-enhanced" 
                   :style="{ clipPath: `inset(0 ${100 - sliderPosition}% 0 0)` }" />
              <input 
                type="range" 
                v-model="sliderPosition" 
                min="0" 
                max="100" 
                class="comparison-slider-input"
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getAvailableMethods, enhanceImage, checkEnhancementHealth } from '@/services/imageEnhancementService';

export default {
  name: 'ImageEnhancementDashboard',
  data() {
    return {
      availableMethods: [],
      selectedMethod: 'auto_enhance',
      enhancementFactor: 1.2,
      returnBase64: false,
      enhancementResults: [],
      selectedImages: [],
      isProcessing: false,
      serviceStatus: 'unknown',
      serviceStatusText: 'غير معروف',
      processedCount: 0,
      totalCount: 0,
      showComparison: false,
      comparisonResult: null,
      sliderPosition: 50
    };
  },
  
  computed: {
    needsFactor() {
      const factorMethods = ['brightness', 'contrast', 'saturation', 'sharpness', 'blur', 'gamma_correction'];
      return factorMethods.includes(this.selectedMethod);
    },
    
    progressPercentage() {
      return this.totalCount > 0 ? (this.processedCount / this.totalCount) * 100 : 0;
    }
  },
  
  async mounted() {
    await this.loadAvailableMethods();
    await this.checkServiceHealth();
  },
  
  methods: {
    async loadAvailableMethods() {
      try {
        const response = await getAvailableMethods();
        this.availableMethods = [
          { key: 'auto_enhance', name: 'تحسين تلقائي شامل' },
          { key: 'brightness', name: 'تعديل السطوع' },
          { key: 'contrast', name: 'تعديل التباين' },
          { key: 'saturation', name: 'تعديل التشبع' },
          { key: 'sharpness', name: 'تعديل الحدة' },
          { key: 'denoise', name: 'إزالة الضوضاء' },
          { key: 'blur', name: 'تطبيق الضبابية' },
          { key: 'edge_enhance', name: 'تحسين الحواف' },
          { key: 'histogram_eq', name: 'معادلة الهيستوجرام' },
          { key: 'gamma_correction', name: 'تصحيح جاما' }
        ];
      } catch (error) {
        console.error('خطأ في تحميل طرق التحسين:', error);
        this.$toast.error('فشل في تحميل طرق التحسين');
      }
    },
    
    async checkServiceHealth() {
      try {
        const response = await checkEnhancementHealth();
        this.serviceStatus = response.status === 'healthy' ? 'healthy' : 'unhealthy';
        this.serviceStatusText = response.status === 'healthy' ? 'متصل' : 'غير متصل';
      } catch (error) {
        this.serviceStatus = 'unhealthy';
        this.serviceStatusText = 'غير متصل';
      }
    },
    
    handleFileSelect(event) {
      const files = Array.from(event.target.files);
      this.selectedImages = files;
      this.processImages(files);
    },
    
    handleDrop(event) {
      event.preventDefault();
      const files = Array.from(event.dataTransfer.files);
      this.selectedImages = files;
      this.processImages(files);
    },
    
    async processImages(files) {
      if (files.length === 0) return;
      
      this.isProcessing = true;
      this.enhancementResults = [];
      this.processedCount = 0;
      this.totalCount = files.length;
      
      try {
        for (const file of files) {
          const originalUrl = URL.createObjectURL(file);
          const result = await enhanceImage(file, this.selectedMethod, this.enhancementFactor, this.returnBase64);
          
          this.enhancementResults.push({
            filename: file.name,
            originalUrl: originalUrl,
            enhancedUrl: this.returnBase64 ? `data:image/png;base64,${result.enhanced_image}` : result.enhanced_image_url,
            method_used: result.method_used || this.selectedMethod,
            factor: result.factor || this.enhancementFactor
          });
          
          this.processedCount++;
        }
        
        this.$toast.success(`تم تحسين ${files.length} صورة بنجاح`);
      } catch (error) {
        console.error('خطأ في تحسين الصور:', error);
        this.$toast.error('فشل في تحسين الصور');
      } finally {
        this.isProcessing = false;
      }
    },
    
    async enhanceAllImages() {
      if (this.selectedImages.length === 0) return;
      await this.processImages(this.selectedImages);
    },
    
    clearResults() {
      this.enhancementResults = [];
      this.selectedImages = [];
      this.processedCount = 0;
      this.totalCount = 0;
    },
    
    downloadEnhanced(result) {
      const link = document.createElement('a');
      link.href = result.enhancedUrl;
      link.download = `enhanced_${result.filename}`;
      link.click();
    },
    
    compareImages(result) {
      this.comparisonResult = result;
      this.showComparison = true;
      this.sliderPosition = 50;
    },
    
    closeComparison() {
      this.showComparison = false;
      this.comparisonResult = null;
    },
    
    updateMethod() {
      // يمكن إضافة منطق إضافي هنا
    },
    
    updateFactor() {
      // يمكن إضافة منطق إضافي هنا
    },
    
    getMethodDisplayName(methodKey) {
      const method = this.availableMethods.find(m => m.key === methodKey);
      return method ? method.name : methodKey;
    },
    
    getMethodDescription(methodKey) {
      const descriptions = {
        'auto_enhance': 'تحسين شامل تلقائي يطبق عدة تحسينات',
        'brightness': 'تعديل سطوع الصورة',
        'contrast': 'تعديل التباين بين الألوان',
        'saturation': 'تعديل تشبع الألوان',
        'sharpness': 'تحسين حدة التفاصيل',
        'denoise': 'إزالة الضوضاء والتشويش',
        'blur': 'تطبيق تأثير الضبابية',
        'edge_enhance': 'تحسين وضوح الحواف',
        'histogram_eq': 'معادلة توزيع الألوان',
        'gamma_correction': 'تصحيح مستوى الإضاءة'
      };
      return descriptions[methodKey] || '';
    }
  }
};
</script>

<style scoped>
/* نفس الأنماط الأساسية من YOLO مع تعديلات للتحسين */
.image-enhancement-dashboard {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.comparison-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 15px;
}

.image-side {
  text-align: center;
}

.image-side h4 {
  margin-bottom: 10px;
  color: #2c3e50;
  font-size: 14px;
}

.image-side img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  border: 2px solid #ddd;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.btn {
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}

.btn-success {
  background-color: #27ae60;
  color: white;
}

.btn-warning {
  background-color: #f39c12;
  color: white;
}

.batch-section {
  margin-top: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 10px;
}

.batch-controls {
  display: flex;
  gap: 15px;
}

.progress-bar {
  width: 100%;
  height: 10px;
  background-color: #e0e0e0;
  border-radius: 5px;
  overflow: hidden;
  margin: 15px 0;
}

.progress-fill {
  height: 100%;
  background-color: #3498db;
  transition: width 0.3s ease;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal-content {
  background-color: white;
  border-radius: 10px;
  max-width: 90%;
  max-height: 90%;
  overflow: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
}

.modal-body {
  padding: 20px;
}

.slider-container {
  position: relative;
  width: 600px;
  height: 400px;
  margin: 0 auto;
}

.comparison-original,
.comparison-enhanced {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.comparison-slider-input {
  position: absolute;
  bottom: -30px;
  left: 0;
  width: 100%;
}

.method-description {
  color: #666;
  font-style: italic;
  margin-top: 5px;
}

/* باقي الأنماط مشابهة لـ YOLO Dashboard */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e0e0e0;
}

.title {
  color: #2c3e50;
  margin: 0;
  font-size: 24px;
}

.title i {
  margin-right: 10px;
  color: #9b59b6;
}

.status-indicator {
  display: flex;
  align-items: center;
  padding: 8px 15px;
  border-radius: 20px;
  font-weight: bold;
}

.status-indicator.healthy {
  background-color: #d4edda;
  color: #155724;
}

.status-indicator.unhealthy {
  background-color: #f8d7da;
  color: #721c24;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 8px;
}

.healthy .status-dot {
  background-color: #28a745;
}

.unhealthy .status-dot {
  background-color: #dc3545;
}

.upload-section {
  margin-bottom: 30px;
}

.upload-area {
  border: 2px dashed #9b59b6;
  border-radius: 10px;
  padding: 40px;
  text-align: center;
  background-color: #f8f9fa;
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-area:hover {
  border-color: #8e44ad;
  background-color: #f3e5f5;
}

.upload-content i {
  font-size: 48px;
  color: #9b59b6;
  margin-bottom: 15px;
}

.settings-panel {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 10px;
  flex-wrap: wrap;
}

.setting-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 200px;
}

.setting-group label {
  font-weight: bold;
  color: #2c3e50;
}

.setting-group select,
.setting-group input[type="range"] {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.factor-value {
  font-weight: bold;
  color: #9b59b6;
}

.results-section {
  margin-top: 30px;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.result-card {
  border: 1px solid #ddd;
  border-radius: 10px;
  overflow: hidden;
  background-color: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.result-info {
  padding: 15px;
}

.result-info h4 {
  margin: 0 0 10px 0;
  color: #2c3e50;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-content {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  text-align: center;
  min-width: 300px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #9b59b6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>

