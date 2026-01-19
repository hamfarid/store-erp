<template>
  <div class="image-search-dashboard">
    <h1 class="page-title">{{ $t('image_search.title') }}</h1>
    
    <!-- لوحة الإحصائيات -->
    <div v-if="hasPermission('view_statistics')" class="statistics-panel">
      <div class="panel-header">
        <h2>{{ $t('image_search.statistics_title') }}</h2>
        <button class="refresh-button" @click="fetchStatistics" :disabled="isLoadingStats">
          <i class="fas" :class="isLoadingStats ? 'fa-spinner fa-spin' : 'fa-sync-alt'"></i>
        </button>
      </div>
      
      <div class="statistics-grid">
        <div class="stat-card">
          <div class="stat-icon">
            <i class="fas fa-image"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ statistics.totalImages }}</div>
            <div class="stat-label">{{ $t('image_search.total_images') }}</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <i class="fas fa-search"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ statistics.searchCount }}</div>
            <div class="stat-label">{{ $t('image_search.search_count') }}</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <i class="fas fa-seedling"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ statistics.cropCount }}</div>
            <div class="stat-label">{{ $t('image_search.crop_count') }}</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <i class="fas fa-bug"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ statistics.pestCount }}</div>
            <div class="stat-label">{{ $t('image_search.pest_count') }}</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <i class="fas fa-biohazard"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ statistics.diseaseCount }}</div>
            <div class="stat-label">{{ $t('image_search.disease_count') }}</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <i class="fas fa-flask"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ statistics.nutrientDeficiencyCount }}</div>
            <div class="stat-label">{{ $t('image_search.nutrient_deficiency_count') }}</div>
          </div>
        </div>
      </div>
      
      <div v-if="hasPermission('view_advanced_statistics')" class="advanced-statistics">
        <div class="panel-header">
          <h3>{{ $t('image_search.advanced_statistics') }}</h3>
        </div>
        
        <div class="chart-container">
          <canvas ref="searchTrendsChart"></canvas>
        </div>
        
        <div class="chart-container">
          <canvas ref="categoryDistributionChart"></canvas>
        </div>
      </div>
      
      <div v-if="hasPermission('view_system_usage')" class="system-usage">
        <div class="panel-header">
          <h3>{{ $t('image_search.system_usage') }}</h3>
        </div>
        
        <div class="usage-grid">
          <div class="usage-card">
            <div class="usage-label">{{ $t('image_search.cpu_usage') }}</div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: `${systemUsage.cpuUsage}%` }"></div>
            </div>
            <div class="usage-value">{{ systemUsage.cpuUsage }}%</div>
          </div>
          
          <div class="usage-card">
            <div class="usage-label">{{ $t('image_search.memory_usage') }}</div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: `${systemUsage.memoryUsage}%` }"></div>
            </div>
            <div class="usage-value">{{ systemUsage.memoryUsage }}%</div>
          </div>
          
          <div class="usage-card">
            <div class="usage-label">{{ $t('image_search.disk_usage') }}</div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: `${systemUsage.diskUsage}%` }"></div>
            </div>
            <div class="usage-value">{{ systemUsage.diskUsage }}%</div>
          </div>
        </div>
        
        <div class="online-users">
          <div class="online-users-header">
            <h4>{{ $t('image_search.online_users') }} ({{ onlineUsers.length }})</h4>
          </div>
          
          <div class="online-users-list">
            <div v-for="user in onlineUsers" :key="user.id" class="online-user">
              <div class="user-avatar">
                <i class="fas fa-user"></i>
              </div>
              <div class="user-info">
                <div class="user-name">{{ user.name }}</div>
                <div class="user-role">{{ user.role }}</div>
              </div>
              <div class="user-status">
                <span class="status-indicator"></span>
                {{ $t('image_search.online') }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- مكون نموذج البحث -->
    <ImageSearchForm
      ref="searchForm"
      @search-images="handleSearchImages"
      @search-disease-images="handleSearchDiseaseImages"
      @search-pest-images="handleSearchPestImages"
      @search-crop-images="handleSearchCropImages"
    />
    
    <!-- مكون نتائج البحث -->
    <ImageSearchResults
      ref="searchResultsRef"
      :search-results="searchResults"
      :has-searched="hasSearched"
      @collect-images="handleCollectImages"
      @view-image-details="handleViewImageDetails"
    />
    
    <!-- مكون تفاصيل الصورة -->
    <ImageDetails
      v-if="showImageDetails"
      :image="selectedImage"
      :index="selectedImageIndex"
      :visible="showImageDetails"
      @close="closeImageDetails"
      @collect="handleCollectSingleImage"
    />
  </div>
</template>

<script>
import Chart from 'chart.js/auto';
import { onMounted, onUnmounted, reactive, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useToast } from 'vue-toastification';
import { useStore } from 'vuex';
import ImageDetails from './ImageDetails.vue';
import ImageSearchForm from './ImageSearchForm.vue';
import ImageSearchResults from './ImageSearchResults.vue';

/**
 * @component ImageSearchDashboard
 * @description مكون لوحة تحكم البحث عن الصور الذي يجمع بين مكونات البحث والنتائج والتفاصيل ويعرض إحصائيات النظام
 */
export default {
  name: 'ImageSearchDashboard',
  
  components: {
    ImageSearchForm,
    ImageSearchResults,
    ImageDetails
  },
  
  setup() {
    const { t } = useI18n();
    const toast = useToast();
    const store = useStore();
    
    // مراجع المكونات
    const searchForm = ref(null);
    const searchResultsRef = ref(null);
    
    // حالة البحث
    const searchResults = ref([]);
    const hasSearched = ref(false);
    const isLoading = ref(false);
    
    // حالة تفاصيل الصورة
    const showImageDetails = ref(false);
    const selectedImage = ref('');
    const selectedImageIndex = ref(-1);
    
    // الإحصائيات
    const isLoadingStats = ref(false);
    const statistics = reactive({
      totalImages: 0,
      searchCount: 0,
      cropCount: 0,
      pestCount: 0,
      diseaseCount: 0,
      nutrientDeficiencyCount: 0
    });
    
    // استخدام النظام
    const systemUsage = reactive({
      cpuUsage: 0,
      memoryUsage: 0,
      diskUsage: 0
    });
    
    // المستخدمون المتصلون
    const onlineUsers = ref([]);
    
    // مراجع الرسوم البيانية
    const searchTrendsChart = ref(null);
    const categoryDistributionChart = ref(null);
    
    // كائنات الرسوم البيانية
    let searchTrendsChartInstance = null;
    let categoryDistributionChartInstance = null;
    
    // مؤقت تحديث الإحصائيات
    let statsUpdateInterval = null;
    
    /**
     * التحقق من صلاحيات المستخدم
     * @param {string} permission - الصلاحية المطلوبة
     * @returns {boolean} ما إذا كان المستخدم يملك الصلاحية
     */
    const hasPermission = (permission) => {
      const user = store.getters['auth/user'];
      if (!user) return false;
      
      // التحقق من صلاحيات المستخدم
      return user.permissions && user.permissions.includes(permission);
    };
    
    /**
     * جلب إحصائيات البحث عن الصور
     */
    const fetchStatistics = async () => {
      if (isLoadingStats.value) return;
      
      isLoadingStats.value = true;
      
      try {
        const response = await fetch('/api/image-search/statistics');
        
        if (response.ok) {
          const data = await response.json();
          
          // تحديث الإحصائيات
          statistics.totalImages = data.total_images || 0;
          statistics.searchCount = data.search_count || 0;
          statistics.cropCount = data.crop_count || 0;
          statistics.pestCount = data.pest_count || 0;
          statistics.diseaseCount = data.disease_count || 0;
          statistics.nutrientDeficiencyCount = data.nutrient_deficiency_count || 0;
          
          // تحديث الرسوم البيانية إذا كانت متاحة
          if (hasPermission('view_advanced_statistics')) {
            updateCharts(data);
          }
        } else {
          console.error('Error fetching statistics');
        }
      } catch (error) {
        console.error('Error fetching statistics:', error);
      } finally {
        isLoadingStats.value = false;
      }
    };
    
    /**
     * جلب معلومات استخدام النظام
     */
    const fetchSystemUsage = async () => {
      if (!hasPermission('view_system_usage')) return;
      
      try {
        const response = await fetch('/api/system/usage');
        
        if (response.ok) {
          const data = await response.json();
          
          // تحديث استخدام النظام
          systemUsage.cpuUsage = data.cpu_usage || 0;
          systemUsage.memoryUsage = data.memory_usage || 0;
          systemUsage.diskUsage = data.disk_usage || 0;
        } else {
          console.error('Error fetching system usage');
        }
      } catch (error) {
        console.error('Error fetching system usage:', error);
      }
    };
    
    /**
     * جلب قائمة المستخدمين المتصلين
     */
    const fetchOnlineUsers = async () => {
      if (!hasPermission('view_system_usage')) return;
      
      try {
        const response = await fetch('/api/users/online');
        
        if (response.ok) {
          const data = await response.json();
          onlineUsers.value = data.users || [];
        } else {
          console.error('Error fetching online users');
        }
      } catch (error) {
        console.error('Error fetching online users:', error);
      }
    };
    
    /**
     * تحديث الرسوم البيانية
     * @param {Object} data - بيانات الإحصائيات
     */
    const updateCharts = (data) => {
      // تحديث رسم اتجاهات البحث
      if (searchTrendsChartInstance) {
        searchTrendsChartInstance.data.labels = data.search_trends.labels || [];
        searchTrendsChartInstance.data.datasets[0].data = data.search_trends.values || [];
        searchTrendsChartInstance.update();
      }
      
      // تحديث رسم توزيع الفئات
      if (categoryDistributionChartInstance) {
        categoryDistributionChartInstance.data.labels = data.category_distribution.labels || [];
        categoryDistributionChartInstance.data.datasets[0].data = data.category_distribution.values || [];
        categoryDistributionChartInstance.update();
      }
    };
    
    /**
     * تهيئة الرسوم البيانية
     */
    const initCharts = () => {
      if (!hasPermission('view_advanced_statistics')) return;
      
      // تهيئة رسم اتجاهات البحث
      const searchTrendsCtx = searchTrendsChart.value.getContext('2d');
      searchTrendsChartInstance = new Chart(searchTrendsCtx, {
        type: 'line',
        data: {
          labels: [],
          datasets: [{
            label: t('image_search.search_trends'),
            data: [],
            borderColor: '#4caf50',
            backgroundColor: 'rgba(76, 175, 80, 0.1)',
            tension: 0.4,
            fill: true
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: 'top'
            },
            tooltip: {
              mode: 'index',
              intersect: false
            }
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
      
      // تهيئة رسم توزيع الفئات
      const categoryDistributionCtx = categoryDistributionChart.value.getContext('2d');
      categoryDistributionChartInstance = new Chart(categoryDistributionCtx, {
        type: 'doughnut',
        data: {
          labels: [],
          datasets: [{
            data: [],
            backgroundColor: [
              '#4caf50',
              '#2196f3',
              '#ff9800',
              '#f44336',
              '#9c27b0',
              '#607d8b'
            ]
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right'
            }
          }
        }
      });
    };
    
    /**
     * معالجة البحث العام عن الصور
     * @param {Object} params - معلمات البحث
     */
    const handleSearchImages = async (params) => {
      isLoading.value = true;
      
      try {
        const response = await fetch('/api/image-search/search', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(params)
        });
        
        if (response.ok) {
          const data = await response.json();
          searchResults.value = data.image_urls;
          hasSearched.value = true;
          
          if (data.image_urls.length === 0) {
            toast.info(t('image_search.no_results_found'));
          } else {
            toast.success(t('image_search.search_success', { count: data.image_urls.length }));
          }
        } else {
          const error = await response.json();
          toast.error(t('image_search.search_error', { message: error.detail }));
        }
      } catch (error) {
        console.error('Error searching images:', error);
        toast.error(t('image_search.search_error', { message: error.message }));
      } finally {
        isLoading.value = false;
        if (searchForm.value) {
          searchForm.value.setLoading(false);
        }
      }
    };
    
    /**
     * معالجة البحث عن صور المرض
     * @param {Object} params - معلمات البحث
     */
    const handleSearchDiseaseImages = async (params) => {
      isLoading.value = true;
      
      try {
        const response = await fetch('/api/image-search/search/disease', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(params)
        });
        
        if (response.ok) {
          const data = await response.json();
          searchResults.value = data.image_urls;
          hasSearched.value = true;
          
          if (data.image_urls.length === 0) {
            toast.info(t('image_search.no_results_found'));
          } else {
            toast.success(t('image_search.search_success', { count: data.image_urls.length }));
          }
        } else {
          const error = await response.json();
          toast.error(t('image_search.search_error', { message: error.detail }));
        }
      } catch (error) {
        console.error('Error searching disease images:', error);
        toast.error(t('image_search.search_error', { message: error.message }));
      } finally {
        isLoading.value = false;
        if (searchForm.value) {
          searchForm.value.setLoading(false);
        }
      }
    };
    
    /**
     * معالجة البحث عن صور الآفة
     * @param {Object} params - معلمات البحث
     */
    const handleSearchPestImages = async (params) => {
      isLoading.value = true;
      
      try {
        const response = await fetch('/api/image-search/search/pest', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(params)
        });
        
        if (response.ok) {
          const data = await response.json();
          searchResults.value = data.image_urls;
          hasSearched.value = true;
          
          if (data.image_urls.length === 0) {
            toast.info(t('image_search.no_results_found'));
          } else {
            toast.success(t('image_search.search_success', { count: data.image_urls.length }));
          }
        } else {
          const error = await response.json();
          toast.error(t('image_search.search_error', { message: error.detail }));
        }
      } catch (error) {
        console.error('Error searching pest images:', error);
        toast.error(t('image_search.search_error', { message: error.message }));
      } finally {
        isLoading.value = false;
        if (searchForm.value) {
          searchForm.value.setLoading(false);
        }
      }
    };
    
    /**
     * معالجة البحث عن صور المحصول
     * @param {Object} params - معلمات البحث
     */
    const handleSearchCropImages = async (params) => {
      isLoading.value = true;
      
      try {
        const response = await fetch('/api/image-search/search/crop', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(params)
        });
        
        if (response.ok) {
          const data = await response.json();
          searchResults.value = data.image_urls;
          hasSearched.value = true;
          
          if (data.image_urls.length === 0) {
            toast.info(t('image_search.no_results_found'));
          } else {
            toast.success(t('image_search.search_success', { count: data.image_urls.length }));
          }
        } else {
          const error = await response.json();
          toast.error(t('image_search.search_error', { message: error.detail }));
        }
      } catch (error) {
        console.error('Error searching crop images:', error);
        toast.error(t('image_search.search_error', { message: error.message }));
      } finally {
        isLoading.value = false;
        if (searchForm.value) {
          searchForm.value.setLoading(false);
        }
      }
    };
    
    /**
     * معالجة جمع الصور المحددة
     * @param {Array} selectedImages - قائمة الصور المحددة
     */
    const handleCollectImages = async (selectedImages) => {
      if (selectedImages.length === 0) {
        toast.warning(t('image_search.no_images_selected'));
        return;
      }
      
      isLoading.value = true;
      
      try {
        const response = await fetch('/api/image-search/collect', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            keywords: ['search'],
            image_urls: selectedImages
          })
        });
        
        if (response.ok) {
          const data = await response.json();
          toast.success(t('image_search.collect_success', { count: data.total_collected }));
          
          // إعادة تعيين التحديد بعد الجمع
          if (searchResults.value) {
            searchResults.value.resetSelection();
          }
          
          // تحديث الإحصائيات
          fetchStatistics();
        } else {
          const error = await response.json();
          toast.error(t('image_search.collect_error', { message: error.detail }));
        }
      } catch (error) {
        console.error('Error collecting images:', error);
        toast.error(t('image_search.collect_error', { message: error.message }));
      } finally {
        isLoading.value = false;
      }
    };
    
    /**
     * معالجة جمع صورة واحدة
     * @param {string} image - عنوان URL للصورة
     */
    const handleCollectSingleImage = async (image) => {
      isLoading.value = true;
      
      try {
        const response = await fetch('/api/image-search/collect', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            keywords: ['search'],
            image_urls: [image]
          })
        });
        
        if (response.ok) {
          const data = await response.json();
          toast.success(t('image_search.collect_success', { count: data.total_collected }));
          
          // تحديث الإحصائيات
          fetchStatistics();
        } else {
          const error = await response.json();
          toast.error(t('image_search.collect_error', { message: error.detail }));
        }
      } catch (error) {
        console.error('Error collecting image:', error);
        toast.error(t('image_search.collect_error', { message: error.message }));
      } finally {
        isLoading.value = false;
      }
    };
    
    /**
     * معالجة عرض تفاصيل الصورة
     * @param {Object} params - معلمات الصورة
     */
    const handleViewImageDetails = (params) => {
      selectedImage.value = params.image;
      selectedImageIndex.value = params.index;
      showImageDetails.value = true;
    };
    
    /**
     * إغلاق تفاصيل الصورة
     */
    const closeImageDetails = () => {
      showImageDetails.value = false;
      selectedImage.value = '';
      selectedImageIndex.value = -1;
    };
    
    // تهيئة المكون
    onMounted(() => {
      // جلب الإحصائيات
      fetchStatistics();
      
      // جلب استخدام النظام والمستخدمين المتصلين
      if (hasPermission('view_system_usage')) {
        fetchSystemUsage();
        fetchOnlineUsers();
      }
      
      // تهيئة الرسوم البيانية
      if (hasPermission('view_advanced_statistics')) {
        initCharts();
      }
      
      // إعداد مؤقت لتحديث الإحصائيات
      statsUpdateInterval = setInterval(() => {
        fetchStatistics();
        
        if (hasPermission('view_system_usage')) {
          fetchSystemUsage();
          fetchOnlineUsers();
        }
      }, 60000); // تحديث كل دقيقة
    });
    
    // تنظيف المكون
    onUnmounted(() => {
      // إيقاف مؤقت تحديث الإحصائيات
      if (statsUpdateInterval) {
        clearInterval(statsUpdateInterval);
      }
      
      // تدمير الرسوم البيانية
      if (searchTrendsChartInstance) {
        searchTrendsChartInstance.destroy();
      }
      
      if (categoryDistributionChartInstance) {
        categoryDistributionChartInstance.destroy();
      }
    });
    
    return {
      // مراجع المكونات
      searchForm,
      searchResultsRef,
      searchTrendsChart,
      categoryDistributionChart,
      
      // حالة البحث
      searchResults,
      hasSearched,
      isLoading,
      
      // حالة تفاصيل الصورة
      showImageDetails,
      selectedImage,
      selectedImageIndex,
      
      // الإحصائيات
      statistics,
      isLoadingStats,
      
      // استخدام النظام
      systemUsage,
      onlineUsers,
      
      // الصلاحيات
      hasPermission,
      
      // وظائف البحث
      handleSearchImages,
      handleSearchDiseaseImages,
      handleSearchPestImages,
      handleSearchCropImages,
      
      // وظائف جمع الصور
      handleCollectImages,
      handleCollectSingleImage,
      
      // وظائف تفاصيل الصورة
      handleViewImageDetails,
      closeImageDetails,
      
      // وظائف الإحصائيات
      fetchStatistics
    };
  }
};
</script>

<style scoped>
.image-search-dashboard {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  margin-bottom: 20px;
  color: #2c3e50;
  font-size: 24px;
}

/* لوحة الإحصائيات */
.statistics-panel {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  overflow: hidden;
}

.panel-header {
  background-color: #f8f9fa;
  padding: 15px 20px;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-header h2, .panel-header h3 {
  margin: 0;
  font-size: 18px;
  color: #495057;
}

.panel-header h3 {
  font-size: 16px;
}

.refresh-button {
  background: none;
  border: none;
  color: #6c757d;
  cursor: pointer;
  font-size: 16px;
}

.refresh-button:hover {
  color: #4caf50;
}

.refresh-button:disabled {
  color: #adb5bd;
  cursor: not-allowed;
}

.statistics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 15px;
  padding: 20px;
}

.stat-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  align-items: center;
  transition: all 0.2s;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 40px;
  height: 40px;
  background-color: #e3f2fd;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  color: #2196f3;
  font-size: 18px;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 20px;
  font-weight: 500;
  color: #2c3e50;
}

.stat-label {
  font-size: 12px;
  color: #6c757d;
  margin-top: 5px;
}

/* الإحصائيات المتقدمة */
.advanced-statistics {
  padding: 0 20px 20px;
}

.chart-container {
  height: 300px;
  margin-bottom: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
}

/* استخدام النظام */
.system-usage {
  padding: 0 20px 20px;
}

.usage-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.usage-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
}

.usage-label {
  font-size: 14px;
  color: #495057;
  margin-bottom: 10px;
}

.progress-bar {
  height: 8px;
  background-color: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 5px;
}

.progress-fill {
  height: 100%;
  background-color: #4caf50;
  border-radius: 4px;
}

.usage-value {
  font-size: 12px;
  color: #6c757d;
  text-align: right;
}

/* المستخدمون المتصلون */
.online-users {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
}

.online-users-header {
  margin-bottom: 15px;
}

.online-users-header h4 {
  margin: 0;
  font-size: 16px;
  color: #495057;
}

.online-users-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 10px;
}

.online-user {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.user-avatar {
  width: 30px;
  height: 30px;
  background-color: #e3f2fd;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
  color: #2196f3;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 14px;
  color: #495057;
}

.user-role {
  font-size: 12px;
  color: #6c757d;
}

.user-status {
  font-size: 12px;
  color: #4caf50;
  display: flex;
  align-items: center;
}

.status-indicator {
  width: 8px;
  height: 8px;
  background-color: #4caf50;
  border-radius: 50%;
  margin-right: 5px;
}

/* تحسينات للأجهزة المحمولة */
@media (max-width: 768px) {
  .statistics-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
  
  .usage-grid {
    grid-template-columns: 1fr;
  }
  
  .online-users-list {
    grid-template-columns: 1fr;
  }
}
</style>
