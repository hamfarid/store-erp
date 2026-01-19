<template>
  <div class="search-results-container">
    <!-- نتائج البحث -->
    <div v-if="searchResults.length > 0" class="search-results">
      <h2>{{ $t('image_search.results_title') }} ({{ searchResults.length }})</h2>
      
      <div class="results-actions">
        <button 
          @click="collectSelectedImages" 
          class="btn btn-success" 
          :disabled="selectedImages.length === 0"
        >
          <i class="fas fa-download"></i> 
          {{ $t('image_search.collect_selected', { count: selectedImages.length }) }}
        </button>
        
        <button 
          @click="selectAllImages" 
          class="btn btn-outline-primary"
        >
          <i class="fas fa-check-square"></i> 
          {{ $t('image_search.select_all') }}
        </button>
        
        <button 
          @click="deselectAllImages" 
          class="btn btn-outline-secondary"
          :disabled="selectedImages.length === 0"
        >
          <i class="fas fa-square"></i> 
          {{ $t('image_search.deselect_all') }}
        </button>
      </div>
      
      <div class="image-grid">
        <div 
          v-for="(image, index) in searchResults" 
          :key="index" 
          class="image-item"
          :class="{ selected: isImageSelected(image) }"
          @click="toggleImageSelection(image)"
        >
          <div class="image-wrapper">
            <img :src="image" :alt="$t('image_search.search_result', { number: index + 1 })" />
            <div class="image-overlay">
              <div class="checkbox">
                <i 
                  :class="[
                    'fas', 
                    isImageSelected(image) ? 'fa-check-square' : 'fa-square'
                  ]"
                ></i>
              </div>
              <div class="image-actions">
                <button 
                  class="btn btn-sm btn-light" 
                  @click.stop="viewImageDetails(image, index)"
                >
                  <i class="fas fa-search-plus"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- رسالة عدم وجود نتائج -->
    <div v-else-if="hasSearched" class="no-results">
      <div class="alert alert-info">
        <i class="fas fa-info-circle"></i>
        {{ $t('image_search.no_results') }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useToast } from 'vue-toastification';

/**
 * @component ImageSearchResults
 * @description مكون عرض نتائج البحث عن الصور الذي يعرض الصور التي تم العثور عليها ويتيح للمستخدمين تحديد الصور وجمعها
 */
export default {
  name: 'ImageSearchResults',
  
  props: {
    /**
     * نتائج البحث (قائمة من عناوين URL للصور)
     * @type {Array}
     */
    searchResults: {
      type: Array,
      default: () => []
    },
    
    /**
     * ما إذا كان قد تم إجراء بحث
     * @type {Boolean}
     */
    hasSearched: {
      type: Boolean,
      default: false
    }
  },
  
  /**
   * @emits collect-images - ينبعث عند طلب جمع الصور المحددة
   * @emits view-image-details - ينبعث عند طلب عرض تفاصيل صورة
   */
  emits: ['collect-images', 'view-image-details'],
  
  setup(props, { emit }) {
    const { t } = useI18n();
    const toast = useToast();
    
    // الصور المحددة
    const selectedImages = ref([]);
    
    /**
     * التحقق مما إذا كانت الصورة محددة
     * @param {string} image - عنوان URL للصورة
     * @returns {boolean} ما إذا كانت الصورة محددة
     */
    const isImageSelected = (image) => {
      return selectedImages.value.includes(image);
    };
    
    /**
     * تبديل تحديد الصورة
     * @param {string} image - عنوان URL للصورة
     */
    const toggleImageSelection = (image) => {
      if (isImageSelected(image)) {
        selectedImages.value = selectedImages.value.filter(img => img !== image);
      } else {
        selectedImages.value.push(image);
      }
    };
    
    /**
     * تحديد جميع الصور
     */
    const selectAllImages = () => {
      selectedImages.value = [...props.searchResults];
      toast.success(t('image_search.all_images_selected'));
    };
    
    /**
     * إلغاء تحديد جميع الصور
     */
    const deselectAllImages = () => {
      selectedImages.value = [];
      toast.info(t('image_search.all_images_deselected'));
    };
    
    /**
     * جمع الصور المحددة
     * @emits collect-images - ينبعث مع قائمة الصور المحددة
     */
    const collectSelectedImages = () => {
      if (selectedImages.value.length === 0) {
        toast.warning(t('image_search.no_images_selected'));
        return;
      }
      
      // إرسال حدث جمع الصور إلى المكون الأب
      emit('collect-images', selectedImages.value);
    };
    
    /**
     * عرض تفاصيل الصورة
     * @param {string} image - عنوان URL للصورة
     * @param {number} index - فهرس الصورة في قائمة النتائج
     * @emits view-image-details - ينبعث مع عنوان URL للصورة وفهرسها
     */
    const viewImageDetails = (image, index) => {
      emit('view-image-details', { image, index });
    };
    
    /**
     * إعادة تعيين الصور المحددة
     */
    const resetSelection = () => {
      selectedImages.value = [];
    };
    
    return {
      selectedImages,
      isImageSelected,
      toggleImageSelection,
      selectAllImages,
      deselectAllImages,
      collectSelectedImages,
      viewImageDetails,
      resetSelection
    };
  }
};
</script>

<style scoped>
.search-results-container {
  margin-top: 20px;
}

.search-results h2 {
  margin-bottom: 15px;
  font-size: 20px;
  color: #2c3e50;
}

.results-actions {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-sm {
  padding: 4px 8px;
  font-size: 12px;
}

.btn-success {
  background-color: #2196f3;
  color: white;
  border: none;
}

.btn-success:hover {
  background-color: #1e88e5;
}

.btn-success:disabled {
  background-color: #90caf9;
  cursor: not-allowed;
}

.btn-outline-primary {
  background-color: transparent;
  color: #4caf50;
  border: 1px solid #4caf50;
}

.btn-outline-primary:hover {
  background-color: #f1f8e9;
}

.btn-outline-secondary {
  background-color: transparent;
  color: #757575;
  border: 1px solid #757575;
}

.btn-outline-secondary:hover {
  background-color: #f5f5f5;
}

.btn-outline-secondary:disabled {
  color: #bdbdbd;
  border-color: #bdbdbd;
  cursor: not-allowed;
}

.btn-light {
  background-color: white;
  color: #333;
  border: 1px solid #ddd;
}

.btn-light:hover {
  background-color: #f5f5f5;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
}

.image-item {
  position: relative;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
}

.image-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.image-item.selected {
  box-shadow: 0 0 0 3px #4caf50;
}

.image-wrapper {
  position: relative;
  padding-top: 75%; /* 4:3 Aspect Ratio */
}

.image-wrapper img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  opacity: 0;
  transition: opacity 0.2s;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 10px;
}

.image-item:hover .image-overlay,
.image-item.selected .image-overlay {
  opacity: 1;
}

.checkbox {
  align-self: flex-end;
  background-color: white;
  width: 24px;
  height: 24px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4caf50;
}

.image-item:not(.selected) .checkbox {
  color: #757575;
}

.image-actions {
  align-self: center;
  margin-top: auto;
}

.no-results {
  margin-top: 30px;
}

.alert {
  padding: 15px;
  border-radius: 4px;
}

.alert-info {
  background-color: #e3f2fd;
  color: #0d47a1;
  border: 1px solid #bbdefb;
}

/* تحسينات للأجهزة المحمولة */
@media (max-width: 768px) {
  .image-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
  
  .results-actions {
    flex-direction: column;
  }
}
</style>
