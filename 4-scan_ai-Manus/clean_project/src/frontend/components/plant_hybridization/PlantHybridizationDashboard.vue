<template>
  <div class="plant-hybridization-dashboard">
    <!-- Header -->
    <div class="dashboard-header">
      <h2 class="title">
        <i class="fas fa-dna"></i>
        تهجين النباتات المتقدم
      </h2>
      <div class="status-indicator" :class="serviceStatus">
        <span class="status-dot"></span>
        {{ serviceStatusText }}
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="tabs-container">
      <div class="tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.key"
          @click="activeTab = tab.key"
          :class="{ active: activeTab === tab.key }"
          class="tab-button"
        >
          <i :class="tab.icon"></i>
          {{ tab.name }}
        </button>
      </div>
    </div>

    <!-- Varieties Management Tab -->
    <div v-if="activeTab === 'varieties'" class="tab-content">
      <div class="varieties-section">
        <h3>أصناف النباتات المتاحة</h3>
        <div class="varieties-grid">
          <div 
            v-for="variety in availableVarieties" 
            :key="variety.id"
            class="variety-card"
            :class="{ selected: selectedVarieties.includes(variety.id) }"
            @click="toggleVarietySelection(variety.id)"
          >
            <div class="variety-header">
              <h4>{{ variety.name }}</h4>
              <span class="species">{{ variety.species }}</span>
            </div>
            <div class="variety-traits">
              <div 
                v-for="(value, trait) in variety.traits" 
                :key="trait"
                class="trait-item"
              >
                <span class="trait-name">{{ getTraitDisplayName(trait) }}</span>
                <div class="trait-bar">
                  <div class="trait-fill" :style="{ width: (value * 100) + '%' }"></div>
                </div>
                <span class="trait-value">{{ Math.round(value * 100) }}%</span>
              </div>
            </div>
            <div class="variety-info">
              <p><strong>المنشأ:</strong> {{ variety.origin }}</p>
              <p class="description">{{ variety.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Hybridization Tab -->
    <div v-if="activeTab === 'hybridization'" class="tab-content">
      <div class="hybridization-form">
        <h3>إعداد عملية التهجين</h3>
        
        <div class="form-grid">
          <!-- Parent Selection -->
          <div class="form-section">
            <h4>اختيار الوالدين</h4>
            <div class="parent-selection">
              <div class="parent-group">
                <label>الوالد الأول:</label>
                <select v-model="hybridizationForm.parent1_id">
                  <option value="">اختر الوالد الأول</option>
                  <option 
                    v-for="variety in availableVarieties" 
                    :key="variety.id" 
                    :value="variety.id"
                  >
                    {{ variety.name }} ({{ variety.species }})
                  </option>
                </select>
              </div>
              
              <div class="parent-group">
                <label>الوالد الثاني:</label>
                <select v-model="hybridizationForm.parent2_id">
                  <option value="">اختر الوالد الثاني</option>
                  <option 
                    v-for="variety in availableVarieties" 
                    :key="variety.id" 
                    :value="variety.id"
                    :disabled="variety.id === hybridizationForm.parent1_id"
                  >
                    {{ variety.name }} ({{ variety.species }})
                  </option>
                </select>
              </div>
            </div>
          </div>

          <!-- Target Traits -->
          <div class="form-section">
            <h4>الصفات المستهدفة</h4>
            <div class="traits-config">
              <div 
                v-for="(trait, traitKey) in availableTraits" 
                :key="traitKey"
                class="trait-config"
              >
                <label>{{ getTraitDisplayName(traitKey) }}:</label>
                <input 
                  type="range" 
                  v-model="hybridizationForm.target_traits[traitKey]"
                  min="0" 
                  max="1" 
                  step="0.1"
                >
                <span class="trait-target-value">
                  {{ Math.round((hybridizationForm.target_traits[traitKey] || 0) * 100) }}%
                </span>
              </div>
            </div>
          </div>

          <!-- Simulation Parameters -->
          <div class="form-section">
            <h4>معاملات المحاكاة</h4>
            <div class="simulation-params">
              <div class="param-group">
                <label>عدد الأجيال:</label>
                <input 
                  type="number" 
                  v-model="hybridizationForm.generations" 
                  min="1" 
                  max="20"
                >
              </div>
              
              <div class="param-group">
                <label>حجم المجموعة:</label>
                <input 
                  type="number" 
                  v-model="hybridizationForm.population_size" 
                  min="50" 
                  max="1000" 
                  step="50"
                >
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="form-actions">
          <button 
            @click="startHybridization" 
            :disabled="!canStartHybridization || isProcessing"
            class="btn btn-primary"
          >
            <i class="fas fa-play"></i>
            بدء التهجين
          </button>
          
          <button @click="resetForm" class="btn btn-secondary">
            <i class="fas fa-undo"></i>
            إعادة تعيين
          </button>
        </div>
      </div>
    </div>

    <!-- Results Tab -->
    <div v-if="activeTab === 'results'" class="tab-content">
      <div class="results-section">
        <h3>نتائج التهجين</h3>
        
        <div v-if="hybridizationResults.length === 0" class="no-results">
          <i class="fas fa-flask"></i>
          <p>لا توجد نتائج تهجين حتى الآن</p>
          <p>قم بإجراء عملية تهجين من التبويب السابق</p>
        </div>

        <div v-else class="results-grid">
          <div 
            v-for="(result, index) in hybridizationResults" 
            :key="index"
            class="result-card"
          >
            <div class="result-header">
              <h4>{{ result.hybrid_id }}</h4>
              <div class="fitness-score" :class="getFitnessClass(result.fitness_score)">
                <span class="score-label">درجة الملاءمة:</span>
                <span class="score-value">{{ Math.round(result.fitness_score * 100) }}%</span>
              </div>
            </div>

            <div class="result-body">
              <div class="parents-info">
                <p><strong>الوالدان:</strong></p>
                <p>{{ getVarietyName(result.parent1_id) }} × {{ getVarietyName(result.parent2_id) }}</p>
              </div>

              <div class="predicted-traits">
                <h5>الصفات المتوقعة:</h5>
                <div class="traits-comparison">
                  <div 
                    v-for="(value, trait) in result.predicted_traits" 
                    :key="trait"
                    class="trait-comparison"
                  >
                    <span class="trait-name">{{ getTraitDisplayName(trait) }}</span>
                    <div class="trait-bars">
                      <div class="predicted-bar">
                        <div class="bar-fill predicted" :style="{ width: (value * 100) + '%' }"></div>
                      </div>
                      <span class="trait-value">{{ Math.round(value * 100) }}%</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="result-stats">
                <div class="stat-item">
                  <span class="stat-label">الجيل:</span>
                  <span class="stat-value">{{ result.generation }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">احتمالية النجاح:</span>
                  <span class="stat-value">{{ Math.round(result.success_probability * 100) }}%</span>
                </div>
              </div>
            </div>

            <div class="result-actions">
              <button @click="saveHybrid(result)" class="btn btn-success">
                <i class="fas fa-save"></i>
                حفظ الهجين
              </button>
              <button @click="analyzeHybrid(result)" class="btn btn-info">
                <i class="fas fa-chart-line"></i>
                تحليل مفصل
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- History Tab -->
    <div v-if="activeTab === 'history'" class="tab-content">
      <div class="history-section">
        <h3>تاريخ عمليات التهجين</h3>
        
        <div class="history-filters">
          <input 
            type="text" 
            v-model="historyFilter" 
            placeholder="البحث في التاريخ..."
            class="search-input"
          >
          <button @click="loadHistory" class="btn btn-primary">
            <i class="fas fa-sync"></i>
            تحديث
          </button>
        </div>

        <div class="history-list">
          <div 
            v-for="(item, index) in filteredHistory" 
            :key="index"
            class="history-item"
          >
            <div class="history-header">
              <h4>{{ item.hybrid_id }}</h4>
              <span class="history-date">{{ formatDate(item.timestamp) }}</span>
            </div>
            <div class="history-details">
              <p>{{ getVarietyName(item.parent1_id) }} × {{ getVarietyName(item.parent2_id) }}</p>
              <p>درجة الملاءمة: {{ Math.round(item.fitness_score * 100) }}%</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="isProcessing" class="loading-overlay">
      <div class="loading-content">
        <div class="spinner"></div>
        <p>جاري تنفيذ عملية التهجين...</p>
        <p>هذا قد يستغرق بضع دقائق</p>
      </div>
    </div>
  </div>
</template>

<script>
import { 
  getAvailableVarieties, 
  getAvailableTraits, 
  hybridizePlants, 
  getHybridizationHistory,
  checkHybridizationHealth 
} from '@/services/plantHybridizationService';

export default {
  name: 'PlantHybridizationDashboard',
  data() {
    return {
      activeTab: 'varieties',
      tabs: [
        { key: 'varieties', name: 'الأصناف', icon: 'fas fa-seedling' },
        { key: 'hybridization', name: 'التهجين', icon: 'fas fa-dna' },
        { key: 'results', name: 'النتائج', icon: 'fas fa-chart-bar' },
        { key: 'history', name: 'التاريخ', icon: 'fas fa-history' }
      ],
      availableVarieties: [],
      availableTraits: {},
      selectedVarieties: [],
      hybridizationForm: {
        parent1_id: '',
        parent2_id: '',
        target_traits: {},
        generations: 5,
        population_size: 100
      },
      hybridizationResults: [],
      hybridizationHistory: [],
      historyFilter: '',
      isProcessing: false,
      serviceStatus: 'unknown',
      serviceStatusText: 'غير معروف'
    };
  },
  
  computed: {
    canStartHybridization() {
      return this.hybridizationForm.parent1_id && 
             this.hybridizationForm.parent2_id && 
             this.hybridizationForm.parent1_id !== this.hybridizationForm.parent2_id;
    },
    
    filteredHistory() {
      if (!this.historyFilter) return this.hybridizationHistory;
      return this.hybridizationHistory.filter(item => 
        item.hybrid_id.toLowerCase().includes(this.historyFilter.toLowerCase()) ||
        item.parent1_id.toLowerCase().includes(this.historyFilter.toLowerCase()) ||
        item.parent2_id.toLowerCase().includes(this.historyFilter.toLowerCase())
      );
    }
  },
  
  async mounted() {
    await this.loadData();
    await this.checkServiceHealth();
  },
  
  methods: {
    async loadData() {
      try {
        const [varietiesResponse, traitsResponse] = await Promise.all([
          getAvailableVarieties(),
          getAvailableTraits()
        ]);
        
        this.availableVarieties = varietiesResponse.varieties || [];
        this.availableTraits = traitsResponse.traits || {};
        
        // تهيئة الصفات المستهدفة
        Object.keys(this.availableTraits).forEach(trait => {
          this.$set(this.hybridizationForm.target_traits, trait, 0.5);
        });
        
      } catch (error) {
        console.error('خطأ في تحميل البيانات:', error);
        this.$toast.error('فشل في تحميل البيانات');
      }
    },
    
    async checkServiceHealth() {
      try {
        const response = await checkHybridizationHealth();
        this.serviceStatus = response.status === 'healthy' ? 'healthy' : 'unhealthy';
        this.serviceStatusText = response.status === 'healthy' ? 'متصل' : 'غير متصل';
      } catch (error) {
        this.serviceStatus = 'unhealthy';
        this.serviceStatusText = 'غير متصل';
      }
    },
    
    async loadHistory() {
      try {
        const response = await getHybridizationHistory();
        this.hybridizationHistory = response.history || [];
      } catch (error) {
        console.error('خطأ في تحميل التاريخ:', error);
        this.$toast.error('فشل في تحميل التاريخ');
      }
    },
    
    toggleVarietySelection(varietyId) {
      const index = this.selectedVarieties.indexOf(varietyId);
      if (index > -1) {
        this.selectedVarieties.splice(index, 1);
      } else {
        this.selectedVarieties.push(varietyId);
      }
    },
    
    async startHybridization() {
      if (!this.canStartHybridization) return;
      
      this.isProcessing = true;
      
      try {
        const result = await hybridizePlants(this.hybridizationForm);
        this.hybridizationResults.unshift(result);
        this.activeTab = 'results';
        this.$toast.success('تم إجراء التهجين بنجاح');
      } catch (error) {
        console.error('خطأ في التهجين:', error);
        this.$toast.error('فشل في إجراء التهجين');
      } finally {
        this.isProcessing = false;
      }
    },
    
    resetForm() {
      this.hybridizationForm = {
        parent1_id: '',
        parent2_id: '',
        target_traits: {},
        generations: 5,
        population_size: 100
      };
      
      // إعادة تهيئة الصفات المستهدفة
      Object.keys(this.availableTraits).forEach(trait => {
        this.$set(this.hybridizationForm.target_traits, trait, 0.5);
      });
    },
    
    saveHybrid(result) {
      // حفظ الهجين كصنف جديد
      this.$toast.info('ميزة حفظ الهجين قيد التطوير');
    },
    
    analyzeHybrid(result) {
      // تحليل مفصل للهجين
      this.$toast.info('ميزة التحليل المفصل قيد التطوير');
    },
    
    getVarietyName(varietyId) {
      const variety = this.availableVarieties.find(v => v.id === varietyId);
      return variety ? variety.name : varietyId;
    },
    
    getTraitDisplayName(traitKey) {
      const traitNames = {
        'size': 'الحجم',
        'sweetness': 'الحلاوة',
        'yield': 'الإنتاجية',
        'disease_resistance': 'مقاومة الأمراض',
        'shelf_life': 'مدة الحفظ',
        'protein_content': 'محتوى البروتين',
        'drought_tolerance': 'تحمل الجفاف',
        'grain_size': 'حجم الحبة'
      };
      return traitNames[traitKey] || traitKey;
    },
    
    getFitnessClass(score) {
      if (score >= 0.8) return 'excellent';
      if (score >= 0.6) return 'good';
      if (score >= 0.4) return 'average';
      return 'poor';
    },
    
    formatDate(timestamp) {
      return new Date(timestamp).toLocaleDateString('ar-SA');
    }
  }
};
</script>

<style scoped>
.plant-hybridization-dashboard {
  padding: 20px;
  max-width: 1400px;
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
  color: #27ae60;
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

.tabs-container {
  margin-bottom: 30px;
}

.tabs {
  display: flex;
  border-bottom: 2px solid #e0e0e0;
}

.tab-button {
  padding: 12px 20px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 16px;
  color: #666;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
}

.tab-button:hover {
  color: #27ae60;
  background-color: #f8f9fa;
}

.tab-button.active {
  color: #27ae60;
  border-bottom-color: #27ae60;
  font-weight: bold;
}

.tab-button i {
  margin-right: 8px;
}

.tab-content {
  min-height: 500px;
}

.varieties-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.variety-card {
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  padding: 20px;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.variety-card:hover {
  border-color: #27ae60;
  box-shadow: 0 4px 15px rgba(39, 174, 96, 0.1);
}

.variety-card.selected {
  border-color: #27ae60;
  background-color: #f8fff8;
}

.variety-header {
  margin-bottom: 15px;
}

.variety-header h4 {
  margin: 0 0 5px 0;
  color: #2c3e50;
}

.species {
  color: #666;
  font-style: italic;
}

.variety-traits {
  margin-bottom: 15px;
}

.trait-item {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.trait-name {
  min-width: 100px;
  font-size: 14px;
  color: #555;
}

.trait-bar {
  flex: 1;
  height: 8px;
  background-color: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.trait-fill {
  height: 100%;
  background-color: #27ae60;
  transition: width 0.3s ease;
}

.trait-value {
  min-width: 40px;
  text-align: right;
  font-size: 12px;
  font-weight: bold;
  color: #27ae60;
}

.variety-info {
  border-top: 1px solid #e0e0e0;
  padding-top: 15px;
}

.variety-info p {
  margin: 5px 0;
  font-size: 14px;
}

.description {
  color: #666;
  font-style: italic;
}

.hybridization-form {
  background-color: #f8f9fa;
  padding: 30px;
  border-radius: 10px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-bottom: 30px;
}

.form-section h4 {
  color: #2c3e50;
  margin-bottom: 15px;
  border-bottom: 2px solid #27ae60;
  padding-bottom: 5px;
}

.parent-selection {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.parent-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

.parent-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

.traits-config {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.trait-config {
  display: flex;
  align-items: center;
  gap: 10px;
}

.trait-config label {
  min-width: 120px;
  font-weight: bold;
  color: #555;
}

.trait-config input[type="range"] {
  flex: 1;
}

.trait-target-value {
  min-width: 50px;
  text-align: right;
  font-weight: bold;
  color: #27ae60;
}

.simulation-params {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.param-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.param-group label {
  min-width: 120px;
  font-weight: bold;
  color: #555;
}

.param-group input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.btn {
  padding: 12px 25px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #27ae60;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #219a52;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}

.btn-success {
  background-color: #27ae60;
  color: white;
}

.btn-info {
  background-color: #3498db;
  color: white;
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
  background-color: white;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.result-header {
  padding: 15px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.result-header h4 {
  margin: 0;
  color: #2c3e50;
}

.fitness-score {
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 14px;
  font-weight: bold;
}

.fitness-score.excellent {
  background-color: #d4edda;
  color: #155724;
}

.fitness-score.good {
  background-color: #d1ecf1;
  color: #0c5460;
}

.fitness-score.average {
  background-color: #fff3cd;
  color: #856404;
}

.fitness-score.poor {
  background-color: #f8d7da;
  color: #721c24;
}

.result-body {
  padding: 15px;
}

.parents-info {
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e0e0e0;
}

.predicted-traits h5 {
  margin-bottom: 10px;
  color: #2c3e50;
}

.trait-comparison {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.trait-comparison .trait-name {
  min-width: 100px;
  font-size: 14px;
  color: #555;
}

.trait-bars {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
}

.predicted-bar {
  flex: 1;
  height: 8px;
  background-color: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill.predicted {
  height: 100%;
  background-color: #3498db;
}

.result-stats {
  display: flex;
  gap: 20px;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #e0e0e0;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.stat-label {
  font-size: 12px;
  color: #666;
}

.stat-value {
  font-weight: bold;
  color: #2c3e50;
}

.result-actions {
  padding: 15px;
  background-color: #f8f9fa;
  display: flex;
  gap: 10px;
}

.no-results {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.no-results i {
  font-size: 64px;
  color: #ddd;
  margin-bottom: 20px;
}

.history-filters {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.history-item {
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: white;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.history-header h4 {
  margin: 0;
  color: #2c3e50;
}

.history-date {
  color: #666;
  font-size: 14px;
}

.history-details p {
  margin: 5px 0;
  color: #555;
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
  padding: 40px;
  border-radius: 10px;
  text-align: center;
  min-width: 300px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #27ae60;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>

