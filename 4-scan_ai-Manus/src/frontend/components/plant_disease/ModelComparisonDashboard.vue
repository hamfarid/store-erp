<!-- 
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/plant_disease/ModelComparisonDashboard.vue

مكون لوحة تحكم مقارنة النماذج
يوفر واجهة تفاعلية لاختبار ومقارنة نماذج تشخيص أمراض النباتات المختلفة
ويعرض النتائج والتقارير البيانية بشكل مرئي
-->

<template>
  <div class="model-comparison-dashboard">
    <div class="dashboard-header">
      <h1 class="dashboard-title">{{ $t('modelComparison.title') }}</h1>
      <p class="dashboard-description">{{ $t('modelComparison.description') }}</p>
    </div>

    <div class="dashboard-content">
      <!-- قسم اختيار النماذج والصور -->
      <div class="setup-section card">
        <h2>{{ $t('modelComparison.setupSection') }}</h2>
        
        <div class="models-selection">
          <h3>{{ $t('modelComparison.selectModels') }}</h3>
          <div class="models-grid">
            <div v-for="model in availableModels" :key="model.id" class="model-item">
              <v-checkbox
                v-model="selectedModels"
                :value="model.id"
                :label="model.name"
                :hint="model.description"
                persistent-hint
              ></v-checkbox>
            </div>
          </div>
        </div>

        <div class="images-selection">
          <h3>{{ $t('modelComparison.selectImages') }}</h3>
          <div class="upload-section">
            <v-file-input
              v-model="testImages"
              :label="$t('modelComparison.uploadImages')"
              multiple
              accept="image/*"
              prepend-icon="mdi-camera"
              show-size
              counter
              chips
              @change="handleImagesUpload"
            ></v-file-input>
            
            <div class="or-divider">{{ $t('common.or') }}</div>
            
            <v-select
              v-model="selectedDataset"
              :items="availableDatasets"
              :label="$t('modelComparison.selectDataset')"
              item-text="name"
              item-value="id"
              @change="loadDataset"
            ></v-select>
          </div>
          
          <div v-if="uploadedImages.length > 0" class="images-preview">
            <h4>{{ $t('modelComparison.uploadedImages') }} ({{ uploadedImages.length }})</h4>
            <div class="images-grid">
              <div v-for="(image, index) in uploadedImagesPreview" :key="index" class="image-preview-item">
                <img :src="image.thumbnail" :alt="image.name" />
                <div class="image-name">{{ image.name }}</div>
              </div>
            </div>
          </div>
        </div>

        <div class="benchmark-options">
          <h3>{{ $t('modelComparison.benchmarkOptions') }}</h3>
          <div class="options-grid">
            <v-text-field
              v-model.number="numIterations"
              :label="$t('modelComparison.iterations')"
              type="number"
              min="1"
              max="10"
            ></v-text-field>
            
            <v-switch
              v-model="measureResourceUsage"
              :label="$t('modelComparison.measureResources')"
            ></v-switch>
            
            <v-switch
              v-model="generateVisualizations"
              :label="$t('modelComparison.generateVisualizations')"
            ></v-switch>
          </div>
        </div>

        <div class="actions">
          <v-btn
            color="primary"
            :loading="isRunningBenchmark"
            :disabled="!canRunBenchmark"
            @click="runBenchmark"
          >
            <v-icon left>mdi-play</v-icon>
            {{ $t('modelComparison.runBenchmark') }}
          </v-btn>
          
          <v-btn
            text
            :disabled="isRunningBenchmark"
            @click="resetForm"
          >
            <v-icon left>mdi-refresh</v-icon>
            {{ $t('common.reset') }}
          </v-btn>
        </div>
      </div>

      <!-- قسم النتائج -->
      <div v-if="benchmarkResults" class="results-section card">
        <h2>{{ $t('modelComparison.resultsSection') }}</h2>
        
        <div class="results-tabs">
          <v-tabs v-model="activeResultTab" background-color="transparent" grow>
            <v-tab>{{ $t('modelComparison.performanceTab') }}</v-tab>
            <v-tab>{{ $t('modelComparison.speedResourcesTab') }}</v-tab>
            <v-tab>{{ $t('modelComparison.visualizationsTab') }}</v-tab>
            <v-tab>{{ $t('modelComparison.recommendationsTab') }}</v-tab>
          </v-tabs>
          
          <v-tabs-items v-model="activeResultTab">
            <!-- جدول الأداء -->
            <v-tab-item>
              <div class="performance-table">
                <h3>{{ $t('modelComparison.performanceMetrics') }}</h3>
                <v-data-table
                  :headers="performanceHeaders"
                  :items="performanceTableData"
                  :items-per-page="10"
                  class="elevation-1"
                  :footer-props="{
                    'items-per-page-options': [5, 10, 15, -1],
                    'items-per-page-text': $t('common.rowsPerPage')
                  }"
                ></v-data-table>
              </div>
            </v-tab-item>
            
            <!-- جدول السرعة والموارد -->
            <v-tab-item>
              <div class="speed-resources-table">
                <h3>{{ $t('modelComparison.speedResourceMetrics') }}</h3>
                <v-data-table
                  :headers="speedResourcesHeaders"
                  :items="speedResourcesTableData"
                  :items-per-page="10"
                  class="elevation-1"
                  :footer-props="{
                    'items-per-page-options': [5, 10, 15, -1],
                    'items-per-page-text': $t('common.rowsPerPage')
                  }"
                ></v-data-table>
              </div>
            </v-tab-item>
            
            <!-- المخططات البيانية -->
            <v-tab-item>
              <div class="visualizations">
                <h3>{{ $t('modelComparison.visualizations') }}</h3>
                
                <div class="charts-grid">
                  <div class="chart-container">
                    <h4>{{ $t('modelComparison.accuracyChart') }}</h4>
                    <canvas ref="accuracyChart"></canvas>
                  </div>
                  
                  <div class="chart-container">
                    <h4>{{ $t('modelComparison.speedChart') }}</h4>
                    <canvas ref="speedChart"></canvas>
                  </div>
                  
                  <div class="chart-container">
                    <h4>{{ $t('modelComparison.memoryChart') }}</h4>
                    <canvas ref="memoryChart"></canvas>
                  </div>
                  
                  <div class="chart-container">
                    <h4>{{ $t('modelComparison.performanceVsSpeedChart') }}</h4>
                    <canvas ref="performanceVsSpeedChart"></canvas>
                  </div>
                </div>
                
                <div class="export-actions">
                  <v-btn
                    color="secondary"
                    @click="exportCharts"
                  >
                    <v-icon left>mdi-download</v-icon>
                    {{ $t('modelComparison.exportCharts') }}
                  </v-btn>
                </div>
              </div>
            </v-tab-item>
            
            <!-- التوصيات -->
            <v-tab-item>
              <div class="recommendations">
                <h3>{{ $t('modelComparison.recommendations') }}</h3>
                
                <div class="recommendations-cards">
                  <v-card class="recommendation-card">
                    <v-card-title class="recommendation-title">
                      <v-icon large color="success" left>mdi-trophy</v-icon>
                      {{ $t('modelComparison.bestAccuracy') }}
                    </v-card-title>
                    <v-card-text>
                      <div class="recommendation-model">{{ bestAccuracyModel.name }}</div>
                      <div class="recommendation-value">{{ bestAccuracyModel.value }}%</div>
                      <div class="recommendation-description">{{ bestAccuracyModel.description }}</div>
                    </v-card-text>
                  </v-card>
                  
                  <v-card class="recommendation-card">
                    <v-card-title class="recommendation-title">
                      <v-icon large color="info" left>mdi-rocket</v-icon>
                      {{ $t('modelComparison.fastestModel') }}
                    </v-card-title>
                    <v-card-text>
                      <div class="recommendation-model">{{ fastestModel.name }}</div>
                      <div class="recommendation-value">{{ fastestModel.value }} FPS</div>
                      <div class="recommendation-description">{{ fastestModel.description }}</div>
                    </v-card-text>
                  </v-card>
                  
                  <v-card class="recommendation-card">
                    <v-card-title class="recommendation-title">
                      <v-icon large color="warning" left>mdi-memory</v-icon>
                      {{ $t('modelComparison.mostEfficient') }}
                    </v-card-title>
                    <v-card-text>
                      <div class="recommendation-model">{{ mostEfficientModel.name }}</div>
                      <div class="recommendation-value">{{ mostEfficientModel.value }} GB</div>
                      <div class="recommendation-description">{{ mostEfficientModel.description }}</div>
                    </v-card-text>
                  </v-card>
                </div>
                
                <div class="usage-recommendations">
                  <h4>{{ $t('modelComparison.usageRecommendations') }}</h4>
                  <ul class="recommendations-list">
                    <li>
                      <strong>{{ $t('modelComparison.forHighAccuracy') }}:</strong> {{ bestAccuracyModel.name }}
                    </li>
                    <li>
                      <strong>{{ $t('modelComparison.forRealTimeApps') }}:</strong> {{ fastestModel.name }}
                    </li>
                    <li>
                      <strong>{{ $t('modelComparison.forLimitedDevices') }}:</strong> {{ mostEfficientModel.name }}
                    </li>
                  </ul>
                </div>
                
                <div class="export-actions">
                  <v-btn
                    color="secondary"
                    @click="exportReport"
                  >
                    <v-icon left>mdi-file-export</v-icon>
                    {{ $t('modelComparison.exportReport') }}
                  </v-btn>
                </div>
              </div>
            </v-tab-item>
          </v-tabs-items>
        </div>
      </div>
      
      <!-- قسم التحليل المتقدم -->
      <div v-if="benchmarkResults" class="advanced-analysis-section card">
        <h2>{{ $t('modelComparison.advancedAnalysisSection') }}</h2>
        
        <div class="model-learning-analysis">
          <h3>{{ $t('modelComparison.modelLearningAnalysis') }}</h3>
          
          <v-select
            v-model="selectedModelForAnalysis"
            :items="modelOptions"
            :label="$t('modelComparison.selectModelForAnalysis')"
            item-text="text"
            item-value="value"
            @change="analyzeModelLearning"
          ></v-select>
          
          <div v-if="modelAnalysis" class="analysis-results">
            <h4>{{ $t('modelComparison.analysisResults') }}</h4>
            
            <div class="analysis-sections">
              <div class="analysis-section">
                <h5>{{ $t('modelComparison.strengths') }}</h5>
                <ul>
                  <li v-for="(strength, index) in modelAnalysis.strengths" :key="'strength-'+index">
                    {{ strength }}
                  </li>
                </ul>
              </div>
              
              <div class="analysis-section">
                <h5>{{ $t('modelComparison.weaknesses') }}</h5>
                <ul>
                  <li v-for="(weakness, index) in modelAnalysis.weaknesses" :key="'weakness-'+index">
                    {{ weakness }}
                  </li>
                </ul>
              </div>
              
              <div class="analysis-section">
                <h5>{{ $t('modelComparison.recommendations') }}</h5>
                <ul>
                  <li v-for="(recommendation, index) in modelAnalysis.recommendations" :key="'recommendation-'+index">
                    {{ recommendation }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- شريط التقدم والرسائل -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
    >
      {{ snackbar.text }}
      <template v-slot:action="{ attrs }">
        <v-btn
          text
          v-bind="attrs"
          @click="snackbar.show = false"
        >
          {{ $t('common.close') }}
        </v-btn>
      </template>
    </v-snackbar>
    
    <v-dialog
      v-model="progressDialog.show"
      persistent
      max-width="400"
    >
      <v-card>
        <v-card-title>{{ progressDialog.title }}</v-card-title>
        <v-card-text>
          <p>{{ progressDialog.message }}</p>
          <v-progress-linear
            :value="progressDialog.progress"
            color="primary"
            height="25"
            striped
          >
            <template v-slot:default>
              <strong>{{ progressDialog.progress }}%</strong>
            </template>
          </v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import plantDiseaseService from '@/services/plantDiseaseService';
import Chart from 'chart.js/auto';
import { mapGetters } from 'vuex';

export default {
  name: 'ModelComparisonDashboard',
  
  data() {
    return {
      // بيانات النماذج والصور
      availableModels: [],
      selectedModels: [],
      testImages: [],
      uploadedImages: [],
      uploadedImagesPreview: [],
      availableDatasets: [],
      selectedDataset: null,
      
      // خيارات الاختبار
      numIterations: 3,
      measureResourceUsage: true,
      generateVisualizations: true,
      
      // حالة الاختبار
      isRunningBenchmark: false,
      benchmarkResults: null,
      
      // علامات التبويب النشطة
      activeResultTab: 0,
      
      // بيانات التحليل المتقدم
      selectedModelForAnalysis: null,
      modelAnalysis: null,
      
      // رسائل وحوارات
      snackbar: {
        show: false,
        text: '',
        color: 'info',
        timeout: 3000
      },
      progressDialog: {
        show: false,
        title: '',
        message: '',
        progress: 0
      },
      
      // مخططات بيانية
      charts: {
        accuracyChart: null,
        speedChart: null,
        memoryChart: null,
        performanceVsSpeedChart: null
      }
    };
  },
  
  computed: {
    ...mapGetters(['isAuthenticated', 'currentUser']),
    
    canRunBenchmark() {
      return this.selectedModels.length > 0 && 
             (this.uploadedImages.length > 0 || this.selectedDataset) && 
             !this.isRunningBenchmark;
    },
    
    performanceHeaders() {
      return [
        { text: this.$t('modelComparison.modelName'), value: 'modelName', align: 'start' },
        { text: this.$t('modelComparison.accuracy'), value: 'accuracy' },
        { text: this.$t('modelComparison.f1Score'), value: 'f1Score' },
        { text: this.$t('modelComparison.avgConfidence'), value: 'avgConfidence' },
        { text: this.$t('modelComparison.stability'), value: 'stability' }
      ];
    },
    
    speedResourcesHeaders() {
      return [
        { text: this.$t('modelComparison.modelName'), value: 'modelName', align: 'start' },
        { text: this.$t('modelComparison.fps'), value: 'fps' },
        { text: this.$t('modelComparison.inferenceTime'), value: 'inferenceTime' },
        { text: this.$t('modelComparison.memoryUsage'), value: 'memoryUsage' },
        { text: this.$t('modelComparison.cpuUsage'), value: 'cpuUsage' }
      ];
    },
    
    performanceTableData() {
      if (!this.benchmarkResults) return [];
      
      return Object.entries(this.benchmarkResults).map(([modelName, results]) => {
        if ('error' in results) return null;
        
        return {
          modelName: modelName,
          accuracy: `${(results.metrics.accuracy.mean * 100).toFixed(2)}% ± ${(results.metrics.accuracy.std * 100).toFixed(2)}%`,
          f1Score: results.metrics.f1_score.mean.toFixed(3),
          avgConfidence: results.metrics.avg_confidence.mean.toFixed(3),
          stability: results.stability.consistency_score.toFixed(3)
        };
      }).filter(item => item !== null);
    },
    
    speedResourcesTableData() {
      if (!this.benchmarkResults) return [];
      
      return Object.entries(this.benchmarkResults).map(([modelName, results]) => {
        if ('error' in results) return null;
        
        return {
          modelName: modelName,
          fps: results.timing.fps.mean.toFixed(2),
          inferenceTime: `${results.timing.avg_inference_time.mean.toFixed(3)}s`,
          memoryUsage: `${results.resource_usage.memory_used.mean.toFixed(2)} GB`,
          cpuUsage: `${results.resource_usage.cpu_usage.mean.toFixed(1)}%`
        };
      }).filter(item => item !== null);
    },
    
    modelOptions() {
      if (!this.benchmarkResults) return [];
      
      return Object.keys(this.benchmarkResults)
        .filter(modelName => !('error' in this.benchmarkResults[modelName]))
        .map(modelName => ({
          text: modelName,
          value: modelName
        }));
    },
    
    bestAccuracyModel() {
      if (!this.benchmarkResults) {
        return { name: '-', value: 0, description: '' };
      }
      
      const validResults = Object.entries(this.benchmarkResults)
        .filter(([_, results]) => !('error' in results));
      
      if (validResults.length === 0) {
        return { name: '-', value: 0, description: '' };
      }
      
      const bestModel = validResults.reduce((best, [modelName, results]) => {
        const accuracy = results.metrics.accuracy.mean;
        if (accuracy > best.accuracy) {
          return { modelName, accuracy };
        }
        return best;
      }, { modelName: '', accuracy: 0 });
      
      return {
        name: bestModel.modelName,
        value: (bestModel.accuracy * 100).toFixed(2),
        description: this.$t('modelComparison.bestAccuracyDesc')
      };
    },
    
    fastestModel() {
      if (!this.benchmarkResults) {
        return { name: '-', value: 0, description: '' };
      }
      
      const validResults = Object.entries(this.benchmarkResults)
        .filter(([_, results]) => !('error' in results));
      
      if (validResults.length === 0) {
        return { name: '-', value: 0, description: '' };
      }
      
      const fastestModel = validResults.reduce((fastest, [modelName, results]) => {
        const fps = results.timing.fps.mean;
        if (fps > fastest.fps) {
          return { modelName, fps };
        }
        return fastest;
      }, { modelName: '', fps: 0 });
      
      return {
        name: fastestModel.modelName,
        value: fastestModel.fps.toFixed(2),
        description: this.$t('modelComparison.fastestModelDesc')
      };
    },
    
    mostEfficientModel() {
      if (!this.benchmarkResults) {
        return { name: '-', value: 0, description: '' };
      }
      
      const validResults = Object.entries(this.benchmarkResults)
        .filter(([_, results]) => !('error' in results));
      
      if (validResults.length === 0) {
        return { name: '-', value: 0, description: '' };
      }
      
      const efficientModel = validResults.reduce((efficient, [modelName, results]) => {
        const memory = results.resource_usage.memory_used.mean;
        if (memory < efficient.memory || efficient.memory === 0) {
          return { modelName, memory };
        }
        return efficient;
      }, { modelName: '', memory: 0 });
      
      return {
        name: efficientModel.modelName,
        value: efficientModel.memory.toFixed(2),
        description: this.$t('modelComparison.mostEfficientDesc')
      };
    }
  },
  
  async created() {
    await this.loadAvailableModels();
    await this.loadAvailableDatasets();
  },
  
  methods: {
    async loadAvailableModels() {
      try {
        const response = await plantDiseaseService.getAvailableModels();
        this.availableModels = response.data.models.map(model => ({
          id: model.id,
          name: model.name,
          description: model.description || ''
        }));
      } catch (error) {
        console.error('Error loading models:', error);
        this.showSnackbar(this.$t('modelComparison.errorLoadingModels'), 'error');
      }
    },
    
    async loadAvailableDatasets() {
      try {
        const response = await plantDiseaseService.getAvailableDatasets();
        this.availableDatasets = response.data.datasets.map(dataset => ({
          id: dataset.id,
          name: dataset.name,
          description: dataset.description || '',
          imageCount: dataset.imageCount || 0
        }));
      } catch (error) {
        console.error('Error loading datasets:', error);
        this.showSnackbar(this.$t('modelComparison.errorLoadingDatasets'), 'error');
      }
    },
    
    handleImagesUpload(files) {
      if (!files || files.length === 0) {
        this.uploadedImages = [];
        this.uploadedImagesPreview = [];
        return;
      }
      
      this.uploadedImages = files;
      
      // إنشاء معاينات للصور
      this.uploadedImagesPreview = [];
      const maxPreviewCount = 12; // الحد الأقصى لعدد الصور المعروضة
      
      for (let i = 0; i < Math.min(files.length, maxPreviewCount); i++) {
        const file = files[i];
        const reader = new FileReader();
        
        reader.onload = (e) => {
          this.uploadedImagesPreview.push({
            name: file.name,
            thumbnail: e.target.result
          });
        };
        
        reader.readAsDataURL(file);
      }
      
      if (files.length > maxPreviewCount) {
        this.showSnackbar(
          this.$t('modelComparison.tooManyImagesForPreview', { count: files.length, shown: maxPreviewCount }),
          'info'
        );
      }
    },
    
    async loadDataset() {
      if (!this.selectedDataset) return;
      
      try {
        this.progressDialog = {
          show: true,
          title: this.$t('modelComparison.loadingDataset'),
          message: this.$t('modelComparison.preparingDataset'),
          progress: 0
        };
        
        // محاكاة تقدم التحميل
        const interval = setInterval(() => {
          if (this.progressDialog.progress < 90) {
            this.progressDialog.progress += 10;
          }
        }, 300);
        
        const response = await plantDiseaseService.getDatasetImages(this.selectedDataset);
        
        clearInterval(interval);
        this.progressDialog.progress = 100;
        
        // إغلاق الحوار بعد ثانية
        setTimeout(() => {
          this.progressDialog.show = false;
        }, 1000);
        
        this.uploadedImages = response.data.images;
        this.showSnackbar(
          this.$t('modelComparison.datasetLoaded', { count: this.uploadedImages.length }),
          'success'
        );
        
        // إنشاء معاينات للصور
        this.uploadedImagesPreview = [];
        const maxPreviewCount = 12;
        
        for (let i = 0; i < Math.min(response.data.images.length, maxPreviewCount); i++) {
          const image = response.data.images[i];
          this.uploadedImagesPreview.push({
            name: image.name || `Image ${i+1}`,
            thumbnail: image.thumbnail || image.url
          });
        }
      } catch (error) {
        console.error('Error loading dataset:', error);
        this.progressDialog.show = false;
        this.showSnackbar(this.$t('modelComparison.errorLoadingDataset'), 'error');
      }
    },
    
    async runBenchmark() {
      if (!this.canRunBenchmark) return;
      
      try {
        this.isRunningBenchmark = true;
        this.progressDialog = {
          show: true,
          title: this.$t('modelComparison.runningBenchmark'),
          message: this.$t('modelComparison.preparingBenchmark'),
          progress: 0
        };
        
        // إعداد البيانات للاختبار
        const benchmarkData = {
          models: this.selectedModels,
          images: this.uploadedImages,
          options: {
            iterations: this.numIterations,
            measureResources: this.measureResourceUsage,
            generateVisualizations: this.generateVisualizations
          }
        };
        
        // محاكاة تقدم الاختبار
        const totalSteps = this.selectedModels.length * this.numIterations;
        let currentStep = 0;
        
        const updateProgress = (step, model, iteration) => {
          currentStep = step;
          const progress = Math.round((currentStep / totalSteps) * 100);
          this.progressDialog.progress = progress;
          this.progressDialog.message = this.$t('modelComparison.testingModel', {
            model,
            iteration: iteration + 1,
            total: this.numIterations
          });
        };
        
        // تنفيذ الاختبار
        const response = await plantDiseaseService.runModelBenchmark(
          benchmarkData,
          updateProgress
        );
        
        this.benchmarkResults = response.data.results;
        
        // إغلاق حوار التقدم
        this.progressDialog.progress = 100;
        this.progressDialog.message = this.$t('modelComparison.benchmarkComplete');
        
        setTimeout(() => {
          this.progressDialog.show = false;
          this.showSnackbar(this.$t('modelComparison.benchmarkCompleted'), 'success');
          
          // إنشاء المخططات البيانية
          this.$nextTick(() => {
            if (this.generateVisualizations) {
              this.createCharts();
            }
          });
        }, 1000);
      } catch (error) {
        console.error('Error running benchmark:', error);
        this.progressDialog.show = false;
        this.showSnackbar(this.$t('modelComparison.errorRunningBenchmark'), 'error');
      } finally {
        this.isRunningBenchmark = false;
      }
    },
    
    createCharts() {
      // تنظيف المخططات السابقة
      Object.values(this.charts).forEach(chart => {
        if (chart) {
          chart.destroy();
        }
      });
      
      // إعداد البيانات للمخططات
      const models = [];
      const accuracies = [];
      const fpsValues = [];
      const memoryUsage = [];
      
      Object.entries(this.benchmarkResults).forEach(([modelName, results]) => {
        if ('error' in results) return;
        
        models.push(modelName);
        accuracies.push(results.metrics.accuracy.mean * 100);
        fpsValues.push(results.timing.fps.mean);
        memoryUsage.push(results.resource_usage.memory_used.mean);
      });
      
      // إنشاء مخطط الدقة
      const accuracyCtx = this.$refs.accuracyChart.getContext('2d');
      this.charts.accuracyChart = new Chart(accuracyCtx, {
        type: 'bar',
        data: {
          labels: models,
          datasets: [{
            label: this.$t('modelComparison.accuracy'),
            data: accuracies,
            backgroundColor: 'rgba(54, 162, 235, 0.7)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: this.$t('modelComparison.accuracyChart')
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: this.$t('modelComparison.accuracyPercent')
              }
            }
          }
        }
      });
      
      // إنشاء مخطط السرعة
      const speedCtx = this.$refs.speedChart.getContext('2d');
      this.charts.speedChart = new Chart(speedCtx, {
        type: 'bar',
        data: {
          labels: models,
          datasets: [{
            label: this.$t('modelComparison.fps'),
            data: fpsValues,
            backgroundColor: 'rgba(75, 192, 192, 0.7)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: this.$t('modelComparison.speedChart')
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: this.$t('modelComparison.framesPerSecond')
              }
            }
          }
        }
      });
      
      // إنشاء مخطط استهلاك الذاكرة
      const memoryCtx = this.$refs.memoryChart.getContext('2d');
      this.charts.memoryChart = new Chart(memoryCtx, {
        type: 'bar',
        data: {
          labels: models,
          datasets: [{
            label: this.$t('modelComparison.memoryUsage'),
            data: memoryUsage,
            backgroundColor: 'rgba(255, 99, 132, 0.7)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: this.$t('modelComparison.memoryChart')
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: this.$t('modelComparison.gigabytes')
              }
            }
          }
        }
      });
      
      // إنشاء مخطط الأداء مقابل السرعة
      const perfVsSpeedCtx = this.$refs.performanceVsSpeedChart.getContext('2d');
      this.charts.performanceVsSpeedChart = new Chart(perfVsSpeedCtx, {
        type: 'scatter',
        data: {
          datasets: [{
            label: this.$t('modelComparison.models'),
            data: models.map((model, index) => ({
              x: fpsValues[index],
              y: accuracies[index],
              r: memoryUsage[index] * 5, // حجم النقطة يعتمد على استهلاك الذاكرة
              model: model
            })),
            backgroundColor: models.map((_, index) => {
              // ألوان مختلفة لكل نموذج
              const hue = (index * 137) % 360;
              return `hsla(${hue}, 70%, 60%, 0.7)`;
            }),
            borderColor: models.map((_, index) => {
              const hue = (index * 137) % 360;
              return `hsla(${hue}, 70%, 60%, 1)`;
            }),
            borderWidth: 1,
            pointRadius: models.map((_, index) => Math.max(5, Math.min(20, memoryUsage[index] * 5)))
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: this.$t('modelComparison.performanceVsSpeedChart')
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const point = context.raw;
                  return [
                    point.model,
                    `${this.$t('modelComparison.accuracy')}: ${point.y.toFixed(2)}%`,
                    `${this.$t('modelComparison.fps')}: ${point.x.toFixed(2)}`,
                    `${this.$t('modelComparison.memory')}: ${memoryUsage[context.dataIndex].toFixed(2)} GB`
                  ];
                }.bind(this)
              }
            }
          },
          scales: {
            x: {
              title: {
                display: true,
                text: this.$t('modelComparison.fps')
              }
            },
            y: {
              title: {
                display: true,
                text: this.$t('modelComparison.accuracyPercent')
              }
            }
          }
        }
      });
    },
    
    async analyzeModelLearning() {
      if (!this.selectedModelForAnalysis) return;
      
      try {
        const response = await plantDiseaseService.analyzeModelLearning(this.selectedModelForAnalysis);
        this.modelAnalysis = response.data.analysis;
      } catch (error) {
        console.error('Error analyzing model:', error);
        this.showSnackbar(this.$t('modelComparison.errorAnalyzingModel'), 'error');
      }
    },
    
    async exportCharts() {
      try {
        // تصدير المخططات كصور
        const charts = [
          { name: 'accuracy', chart: this.charts.accuracyChart },
          { name: 'speed', chart: this.charts.speedChart },
          { name: 'memory', chart: this.charts.memoryChart },
          { name: 'performance_vs_speed', chart: this.charts.performanceVsSpeedChart }
        ];
        
        const images = charts.map(({ name, chart }) => ({
          name: `${name}_chart.png`,
          data: chart.toBase64Image()
        }));
        
        await plantDiseaseService.exportCharts(images);
        this.showSnackbar(this.$t('modelComparison.chartsExported'), 'success');
      } catch (error) {
        console.error('Error exporting charts:', error);
        this.showSnackbar(this.$t('modelComparison.errorExportingCharts'), 'error');
      }
    },
    
    async exportReport() {
      try {
        this.progressDialog = {
          show: true,
          title: this.$t('modelComparison.exportingReport'),
          message: this.$t('modelComparison.preparingReport'),
          progress: 0
        };
        
        // محاكاة تقدم التصدير
        const interval = setInterval(() => {
          if (this.progressDialog.progress < 90) {
            this.progressDialog.progress += 10;
          }
        }, 200);
        
        await plantDiseaseService.exportBenchmarkReport(this.benchmarkResults);
        
        clearInterval(interval);
        this.progressDialog.progress = 100;
        this.progressDialog.message = this.$t('modelComparison.reportExported');
        
        setTimeout(() => {
          this.progressDialog.show = false;
          this.showSnackbar(this.$t('modelComparison.reportExportedSuccess'), 'success');
        }, 1000);
      } catch (error) {
        console.error('Error exporting report:', error);
        this.progressDialog.show = false;
        this.showSnackbar(this.$t('modelComparison.errorExportingReport'), 'error');
      }
    },
    
    resetForm() {
      this.selectedModels = [];
      this.testImages = [];
      this.uploadedImages = [];
      this.uploadedImagesPreview = [];
      this.selectedDataset = null;
      this.numIterations = 3;
      this.measureResourceUsage = true;
      this.generateVisualizations = true;
      this.benchmarkResults = null;
      this.selectedModelForAnalysis = null;
      this.modelAnalysis = null;
      
      // تنظيف المخططات
      Object.values(this.charts).forEach(chart => {
        if (chart) {
          chart.destroy();
        }
      });
      this.charts = {
        accuracyChart: null,
        speedChart: null,
        memoryChart: null,
        performanceVsSpeedChart: null
      };
    },
    
    showSnackbar(text, color = 'info') {
      this.snackbar = {
        show: true,
        text,
        color,
        timeout: color === 'error' ? 6000 : 3000
      };
    }
  }
};
</script>

<style lang="scss" scoped>
.model-comparison-dashboard {
  padding: 20px;
  
  .dashboard-header {
    margin-bottom: 20px;
    text-align: center;
    
    .dashboard-title {
      font-size: 2rem;
      margin-bottom: 10px;
    }
    
    .dashboard-description {
      font-size: 1.1rem;
      color: #666;
    }
  }
  
  .dashboard-content {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .card {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
    
    h2 {
      font-size: 1.5rem;
      margin-bottom: 20px;
      padding-bottom: 10px;
      border-bottom: 1px solid #eee;
    }
    
    h3 {
      font-size: 1.2rem;
      margin: 15px 0;
    }
  }
  
  .setup-section {
    .models-selection, .images-selection, .benchmark-options {
      margin-bottom: 20px;
    }
    
    .models-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
      gap: 10px;
    }
    
    .upload-section {
      margin-bottom: 15px;
    }
    
    .or-divider {
      text-align: center;
      margin: 15px 0;
      color: #666;
      position: relative;
      
      &::before, &::after {
        content: '';
        position: absolute;
        top: 50%;
        width: 45%;
        height: 1px;
        background-color: #ddd;
      }
      
      &::before {
        left: 0;
      }
      
      &::after {
        right: 0;
      }
    }
    
    .images-preview {
      margin-top: 15px;
      
      .images-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
        gap: 10px;
        margin-top: 10px;
      }
      
      .image-preview-item {
        border: 1px solid #ddd;
        border-radius: 4px;
        overflow: hidden;
        
        img {
          width: 100%;
          height: 100px;
          object-fit: cover;
        }
        
        .image-name {
          font-size: 0.8rem;
          padding: 5px;
          text-align: center;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          background-color: #f5f5f5;
        }
      }
    }
    
    .options-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 15px;
    }
    
    .actions {
      display: flex;
      justify-content: flex-end;
      gap: 10px;
      margin-top: 20px;
    }
  }
  
  .results-section {
    .results-tabs {
      margin-top: 20px;
    }
    
    .performance-table, .speed-resources-table {
      margin-top: 15px;
    }
    
    .visualizations {
      margin-top: 15px;
      
      .charts-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        margin-top: 15px;
        
        @media (max-width: 768px) {
          grid-template-columns: 1fr;
        }
      }
      
      .chart-container {
        position: relative;
        height: 300px;
        margin-bottom: 20px;
      }
    }
    
    .recommendations {
      margin-top: 15px;
      
      .recommendations-cards {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin-top: 15px;
        
        @media (max-width: 768px) {
          grid-template-columns: 1fr;
        }
      }
      
      .recommendation-card {
        border-radius: 8px;
        
        .recommendation-title {
          font-size: 1.1rem;
        }
        
        .recommendation-model {
          font-size: 1.2rem;
          font-weight: bold;
          margin-bottom: 5px;
        }
        
        .recommendation-value {
          font-size: 1.5rem;
          font-weight: bold;
          margin-bottom: 10px;
          color: #4caf50;
        }
      }
      
      .usage-recommendations {
        margin-top: 20px;
        
        .recommendations-list {
          list-style-type: none;
          padding: 0;
          
          li {
            padding: 10px;
            margin-bottom: 5px;
            background-color: #f5f5f5;
            border-radius: 4px;
          }
        }
      }
    }
    
    .export-actions {
      display: flex;
      justify-content: center;
      margin-top: 20px;
    }
  }
  
  .advanced-analysis-section {
    .analysis-results {
      margin-top: 15px;
      
      .analysis-sections {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin-top: 15px;
        
        @media (max-width: 768px) {
          grid-template-columns: 1fr;
        }
      }
      
      .analysis-section {
        background-color: #f5f5f5;
        border-radius: 8px;
        padding: 15px;
        
        h5 {
          font-size: 1.1rem;
          margin-bottom: 10px;
          padding-bottom: 5px;
          border-bottom: 1px solid #ddd;
        }
        
        ul {
          padding-left: 20px;
          
          li {
            margin-bottom: 5px;
          }
        }
      }
    }
  }
  
  // تصميم متجاوب
  @media (max-width: 768px) {
    .dashboard-content {
      grid-template-columns: 1fr;
    }
  }
}
</style>
