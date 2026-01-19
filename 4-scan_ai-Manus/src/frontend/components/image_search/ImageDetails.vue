<template>
  <div class="image-details-container">
    <div v-if="image" class="image-details-modal">
      <div class="modal-header">
        <h2>{{ $t('image_search.image_details') }}</h2>
        <button class="close-button" @click="closeDetails">
          <i class="fas fa-times"></i>
        </button>
      </div>
      
      <div class="modal-body">
        <div class="image-preview">
          <img :src="image" alt="Details" />
        </div>
        
        <div class="image-info">
          <div class="info-group">
            <h3>{{ $t('image_search.image_info') }}</h3>
            <div class="info-item">
              <span class="info-label">{{ $t('image_search.image_url') }}:</span>
              <span class="info-value">{{ image }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">{{ $t('image_search.image_index') }}:</span>
              <span class="info-value">{{ index + 1 }}</span>
            </div>
          </div>
          
          <div class="info-group" v-if="metadata">
            <h3>{{ $t('image_search.metadata') }}</h3>
            <div v-for="(value, key) in metadata" :key="key" class="info-item">
              <span class="info-label">{{ key }}:</span>
              <span class="info-value">{{ value }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="btn btn-primary" @click="collectImage">
          <i class="fas fa-download"></i> {{ $t('image_search.collect_image') }}
        </button>
        <button class="btn btn-secondary" @click="closeDetails">
          <i class="fas fa-times"></i> {{ $t('image_search.close') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useToast } from 'vue-toastification';

/**
 * @component ImageDetails
 * @description مكون عرض تفاصيل الصورة الذي يعرض صورة محددة ومعلوماتها
 */
export default {
  name: 'ImageDetails',
  
  props: {
    /**
     * عنوان URL للصورة المراد عرض تفاصيلها
     * @type {String}
     */
    image: {
      type: String,
      default: ''
    },
    
    /**
     * فهرس الصورة في قائمة النتائج
     * @type {Number}
     */
    index: {
      type: Number,
      default: -1
    },
    
    /**
     * ما إذا كان مكون التفاصيل مرئيًا
     * @type {Boolean}
     */
    visible: {
      type: Boolean,
      default: false
    }
  },
  
  /**
   * @emits close - ينبعث عند إغلاق تفاصيل الصورة
   * @emits collect - ينبعث عند طلب جمع الصورة
   */
  emits: ['close', 'collect'],
  
  setup(props, { emit }) {
    const { t } = useI18n();
    const toast = useToast();
    
    // بيانات وصفية للصورة
    const metadata = ref(null);
    
    /**
     * جلب البيانات الوصفية للصورة
     */
    const fetchMetadata = async () => {
      if (!props.image) return;
      
      try {
        // محاولة جلب البيانات الوصفية للصورة من الخادم
        const response = await fetch('/api/image-search/metadata', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            image_url: props.image
          })
        });
        
        if (response.ok) {
          const data = await response.json();
          metadata.value = data.metadata;
        } else {
          console.error('Error fetching image metadata');
          metadata.value = null;
        }
      } catch (error) {
        console.error('Error fetching image metadata:', error);
        metadata.value = null;
      }
    };
    
    /**
     * مراقبة تغييرات الصورة لجلب البيانات الوصفية
     */
    watch(() => props.image, (newImage) => {
      if (newImage) {
        fetchMetadata();
      } else {
        metadata.value = null;
      }
    });
    
    /**
     * مراقبة تغييرات الرؤية لجلب البيانات الوصفية
     */
    watch(() => props.visible, (newVisible) => {
      if (newVisible && props.image) {
        fetchMetadata();
      }
    });
    
    /**
     * إغلاق تفاصيل الصورة
     * @emits close - ينبعث عند إغلاق التفاصيل
     */
    const closeDetails = () => {
      emit('close');
    };
    
    /**
     * جمع الصورة
     * @emits collect - ينبعث مع عنوان URL للصورة
     */
    const collectImage = () => {
      if (!props.image) return;
      
      emit('collect', props.image);
      toast.success(t('image_search.image_collected'));
    };
    
    return {
      metadata,
      closeDetails,
      collectImage
    };
  }
};
</script>

<style scoped>
.image-details-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.image-details-modal {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 900px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 15px 20px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
  font-size: 18px;
  color: #495057;
}

.close-button {
  background: none;
  border: none;
  font-size: 18px;
  color: #6c757d;
  cursor: pointer;
}

.close-button:hover {
  color: #343a40;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.image-preview {
  text-align: center;
}

.image-preview img {
  max-width: 100%;
  max-height: 400px;
  object-fit: contain;
  border-radius: 4px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.image-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-group {
  background-color: #f8f9fa;
  border-radius: 4px;
  padding: 15px;
}

.info-group h3 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 16px;
  color: #495057;
}

.info-item {
  margin-bottom: 8px;
  display: flex;
  flex-wrap: wrap;
}

.info-label {
  font-weight: 500;
  color: #495057;
  margin-right: 8px;
  min-width: 100px;
}

.info-value {
  color: #6c757d;
  word-break: break-all;
}

.modal-footer {
  padding: 15px 20px;
  background-color: #f8f9fa;
  border-top: 1px solid #e9ecef;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background-color: #4caf50;
  color: white;
  border: none;
}

.btn-primary:hover {
  background-color: #43a047;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  border: none;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

/* تحسينات للأجهزة المحمولة */
@media (max-width: 768px) {
  .image-details-modal {
    width: 95%;
  }
  
  .modal-body {
    padding: 15px;
  }
  
  .info-item {
    flex-direction: column;
  }
  
  .info-label {
    margin-bottom: 4px;
  }
}
</style>
