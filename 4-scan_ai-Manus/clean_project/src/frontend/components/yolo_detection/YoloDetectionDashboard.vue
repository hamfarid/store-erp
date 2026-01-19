<template>
  <div class="yolo-detection-dashboard">
    <!-- Header -->
    <div class="dashboard-header">
      <h2 class="title">
        <i class="fas fa-search"></i>
        كشف الكائنات باستخدام YOLO
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
          <i class="fas fa-cloud-upload-alt"></i>
          <p>اسحب الصور هنا أو انقر للاختيار</p>
          <small>يدعم: JPG, PNG, BMP</small>
        </div>
      </div>
    </div>

    <!-- Settings Panel -->
    <div class="settings-panel">
      <div class="setting-group">
        <label>نموذج الكشف:</label>
        <select v-model="selectedModel" @change="updateModel">
          <option v-for="model in availableModels" :key="model" :value="model">
            {{ getModelDisplayName(model) }}
          </option>
        </select>
      </div>
      
      <div class="setting-group">
        <label>مستوى الثقة:</label>
        <input 
          type="range" 
          v-model="confidence" 
          min="0.1" 
          max="1.0" 
          step="0.1"
          @input="updateConfidence"
        >
        <span class="confidence-value">{{ confidence }}</span>
      </div>
    </div>

    <!-- Results Section -->
    <div class="results-section" v-if="detectionResults.length > 0">
      <h3>نتائج الكشف</h3>
      <div class="results-grid">
        <div 
          v-for="(result, index) in detectionResults" 
          :key="index" 
          class="result-card"
        >
          <div class="image-container">
            <img :src="result.imageUrl" :alt="result.filename" />
            <div class="detection-overlay">
              <div 
                v-for="(detection, detIndex) in result.detections" 
                :key="detIndex"
                class="detection-box"
                :style="getDetectionBoxStyle(detection)"
              >
                <span class="detection-label">
                  {{ detection.class_name }} ({{ Math.round(detection.confidence * 100) }}%)
                </span>
              </div>
            </div>
          </div>
          
          <div class="result-info">
            <h4>{{ result.filename }}</h4>
            <p>عدد الكائنات المكتشفة: {{ result.count }}</p>
            <p>النموذج المستخدم: {{ getModelDisplayName(result.model_used) }}</p>
            
            <div class="detections-list">
              <div 
                v-for="(detection, detIndex) in result.detections" 
                :key="detIndex"
                class="detection-item"
              >
                <span class="detection-name">{{ detection.class_name }}</span>
                <span class="detection-confidence">{{ Math.round(detection.confidence * 100) }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="isProcessing" class="loading-overlay">
      <div class="loading-content">
        <div class="spinner"></div>
        <p>جاري معالجة الصور...</p>
      </div>
    </div>
  </div>
</template>

<script>
import { getAvailableModels, detectObjects, checkYoloHealth } from '@/services/yoloDetectionService';

export default {
  name: 'YoloDetectionDashboard',
  data() {
    return {
      availableModels: [],
      selectedModel: 'general',
      confidence: 0.5,
      detectionResults: [],
      isProcessing: false,
      serviceStatus: 'unknown',
      serviceStatusText: 'غير معروف'
    };
  },
  
  async mounted() {
    await this.loadAvailableModels();
    await this.checkServiceHealth();
  },
  
  methods: {
    async loadAvailableModels() {
      try {
        const response = await getAvailableModels();
        this.availableModels = response.available_models || [];
        if (this.availableModels.length > 0) {
          this.selectedModel = this.availableModels[0];
        }
      } catch (error) {
        console.error('خطأ في تحميل النماذج:', error);
        this.$toast.error('فشل في تحميل النماذج المتاحة');
      }
    },
    
    async checkServiceHealth() {
      try {
        const response = await checkYoloHealth();
        this.serviceStatus = response.status === 'healthy' ? 'healthy' : 'unhealthy';
        this.serviceStatusText = response.status === 'healthy' ? 'متصل' : 'غير متصل';
      } catch (error) {
        this.serviceStatus = 'unhealthy';
        this.serviceStatusText = 'غير متصل';
      }
    },
    
    handleFileSelect(event) {
      const files = Array.from(event.target.files);
      this.processImages(files);
    },
    
    handleDrop(event) {
      event.preventDefault();
      const files = Array.from(event.dataTransfer.files);
      this.processImages(files);
    },
    
    async processImages(files) {
      if (files.length === 0) return;
      
      this.isProcessing = true;
      this.detectionResults = [];
      
      try {
        for (const file of files) {
          const imageUrl = URL.createObjectURL(file);
          const result = await detectObjects(file, this.selectedModel, this.confidence);
          
          this.detectionResults.push({
            filename: file.name,
            imageUrl: imageUrl,
            detections: result.detections || [],
            count: result.count || 0,
            model_used: result.model_used || this.selectedModel
          });
        }
        
        this.$toast.success(`تم معالجة ${files.length} صورة بنجاح`);
      } catch (error) {
        console.error('خطأ في معالجة الصور:', error);
        this.$toast.error('فشل في معالجة الصور');
      } finally {
        this.isProcessing = false;
      }
    },
    
    updateModel() {
      // يمكن إضافة منطق إضافي هنا
    },
    
    updateConfidence() {
      // يمكن إضافة منطق إضافي هنا
    },
    
    getModelDisplayName(modelName) {
      const modelNames = {
        'general': 'عام',
        'medium': 'متوسط',
        'large': 'كبير',
        'custom': 'مخصص'
      };
      return modelNames[modelName] || modelName;
    },
    
    getDetectionBoxStyle(detection) {
      // تحويل إحداثيات الصندوق إلى CSS
      const [x1, y1, x2, y2] = detection.bbox;
      return {
        left: `${x1}px`,
        top: `${y1}px`,
        width: `${x2 - x1}px`,
        height: `${y2 - y1}px`
      };
    }
  }
};
</script>

<style scoped>
.yolo-detection-dashboard {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

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
  color: #3498db;
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
  border: 2px dashed #3498db;
  border-radius: 10px;
  padding: 40px;
  text-align: center;
  background-color: #f8f9fa;
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-area:hover {
  border-color: #2980b9;
  background-color: #e3f2fd;
}

.upload-content i {
  font-size: 48px;
  color: #3498db;
  margin-bottom: 15px;
}

.settings-panel {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 10px;
}

.setting-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
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

.confidence-value {
  font-weight: bold;
  color: #3498db;
}

.results-section {
  margin-top: 30px;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
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

.image-container {
  position: relative;
  width: 100%;
  height: 300px;
  overflow: hidden;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.detection-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.detection-box {
  position: absolute;
  border: 2px solid #e74c3c;
  background-color: rgba(231, 76, 60, 0.1);
}

.detection-label {
  position: absolute;
  top: -25px;
  left: 0;
  background-color: #e74c3c;
  color: white;
  padding: 2px 8px;
  font-size: 12px;
  border-radius: 3px;
  white-space: nowrap;
}

.result-info {
  padding: 15px;
}

.result-info h4 {
  margin: 0 0 10px 0;
  color: #2c3e50;
}

.detections-list {
  margin-top: 15px;
}

.detection-item {
  display: flex;
  justify-content: space-between;
  padding: 5px 0;
  border-bottom: 1px solid #eee;
}

.detection-name {
  font-weight: bold;
}

.detection-confidence {
  color: #3498db;
  font-weight: bold;
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
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>

