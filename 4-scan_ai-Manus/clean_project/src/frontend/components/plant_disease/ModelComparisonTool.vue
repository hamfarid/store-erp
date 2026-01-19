<!--
مكون اختبار ومقارنة النماذج
يتيح هذا المكون للمستخدمين اختيار نموذج واحد أو أكثر واختبار أدائها على مجموعة من الصور
مع عرض نتائج المقارنة بشكل تفاعلي ومرئي

المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
-->

<template>
  <div class="model-comparison-tool">
    <v-card class="mb-4">
      <v-card-title class="primary--text">
        <v-icon large class="ml-2">mdi-chart-box</v-icon>
        أداة مقارنة نماذج تشخيص أمراض النباتات
      </v-card-title>
      <v-card-subtitle>
        قم باختيار النماذج وتحميل الصور لمقارنة أداء النماذج المختلفة
      </v-card-subtitle>

      <v-card-text>
        <v-stepper v-model="currentStep" vertical>
          <!-- الخطوة 1: اختيار النماذج -->
          <v-stepper-step :complete="currentStep > 1" step="1">
            اختيار النماذج
            <small>اختر نموذج واحد أو أكثر للمقارنة</small>
          </v-stepper-step>

          <v-stepper-content step="1">
            <v-card flat>
              <v-card-text>
                <v-alert
                  v-if="availableModels.length === 0"
                  type="warning"
                  outlined
                >
                  لا توجد نماذج متاحة حالياً. يرجى التحقق من تثبيت النماذج.
                </v-alert>

                <div v-else>
                  <v-data-table
                    v-model="selectedModels"
                    :headers="modelHeaders"
                    :items="availableModels"
                    item-key="name"
                    show-select
                    class="elevation-1"
                    :footer-props="{
                      'items-per-page-options': [5, 10, 15],
                      'items-per-page-text': 'عدد النماذج في الصفحة',
                    }"
                  >
                    <template v-slot:item.type="{ item }">
                      <v-chip
                        :color="getModelTypeColor(item.type)"
                        text-color="white"
                        small
                      >
                        {{ item.type }}
                      </v-chip>
                    </template>

                    <template v-slot:item.parameters="{ item }">
                      <span v-if="typeof item.parameters === 'number'">
                        {{ formatNumber(item.parameters) }}
                      </span>
                      <span v-else>{{ item.parameters }}</span>
                    </template>
                  </v-data-table>

                  <v-alert
                    v-if="selectedModels.length === 0"
                    type="info"
                    outlined
                    class="mt-4"
                  >
                    يرجى اختيار نموذج واحد على الأقل للمتابعة
                  </v-alert>
                </div>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="primary"
                  :disabled="selectedModels.length === 0"
                  @click="currentStep = 2"
                >
                  التالي
                  <v-icon right>mdi-arrow-left</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-stepper-content>

          <!-- الخطوة 2: تحميل الصور -->
          <v-stepper-step :complete="currentStep > 2" step="2">
            تحميل الصور
            <small>قم بتحميل مجموعة من الصور للاختبار</small>
          </v-stepper-step>

          <v-stepper-content step="2">
            <v-card flat>
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="6">
                    <v-file-input
                      v-model="imageFiles"
                      counter
                      label="اختر صور للاختبار"
                      multiple
                      prepend-icon="mdi-camera"
                      outlined
                      show-size
                      accept="image/*"
                      :rules="[rules.required, rules.maxFiles]"
                      hint="يمكنك اختيار حتى 50 صورة"
                      persistent-hint
                    ></v-file-input>
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-select
                      v-model="datasetType"
                      :items="datasetTypes"
                      label="نوع مجموعة البيانات"
                      outlined
                      hint="اختر نوع مجموعة البيانات لتحديد التسميات تلقائياً"
                      persistent-hint
                    ></v-select>
                  </v-col>
                </v-row>

                <v-alert
                  v-if="imageFiles.length > 0"
                  type="success"
                  outlined
                  class="mt-4"
                >
                  تم اختيار {{ imageFiles.length }} صورة
                </v-alert>

                <v-data-table
                  v-if="imageFiles.length > 0"
                  :headers="imageHeaders"
                  :items="imageFilesWithLabels"
                  class="elevation-1 mt-4"
                  :footer-props="{
                    'items-per-page-options': [5, 10, 15],
                    'items-per-page-text': 'عدد الصور في الصفحة',
                  }"
                >
                  <template v-slot:item.preview="{ item }">
                    <v-avatar size="40" class="mr-2">
                      <v-img
                        :src="getImagePreview(item.file)"
                        contain
                      ></v-img>
                    </v-avatar>
                  </template>

                  <template v-slot:item.label="{ item }">
                    <v-select
                      v-model="item.label"
                      :items="availableLabels"
                      dense
                      outlined
                      hide-details
                      class="label-select"
                    ></v-select>
                  </template>
                </v-data-table>
              </v-card-text>

              <v-card-actions>
                <v-btn text @click="currentStep = 1">
                  <v-icon left>mdi-arrow-right</v-icon>
                  السابق
                </v-btn>
                <v-spacer></v-spacer>
                <v-btn
                  color="primary"
                  :disabled="imageFiles.length === 0"
                  @click="currentStep = 3"
                >
                  التالي
                  <v-icon right>mdi-arrow-left</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-stepper-content>

          <!-- الخطوة 3: إعدادات الاختبار -->
          <v-stepper-step :complete="currentStep > 3" step="3">
            إعدادات الاختبار
            <small>ضبط معلمات الاختبار</small>
          </v-stepper-step>

          <v-stepper-content step="3">
            <v-card flat>
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="6">
                    <v-slider
                      v-model="testIterations"
                      :min="1"
                      :max="10"
                      :step="1"
                      label="عدد تكرارات الاختبار"
                      thumb-label="always"
                      hint="زيادة عدد التكرارات يحسن دقة النتائج ولكن يزيد وقت الاختبار"
                      persistent-hint
                    ></v-slider>
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-switch
                      v-model="monitorResources"
                      label="مراقبة استهلاك الموارد"
                      hint="قياس استهلاك المعالج والذاكرة أثناء الاختبار"
                      persistent-hint
                    ></v-switch>
                  </v-col>
                </v-row>

                <v-row>
                  <v-col cols="12" md="6">
                    <v-switch
                      v-model="generateVisualizations"
                      label="إنشاء مخططات بيانية"
                      hint="إنشاء مخططات بيانية لمقارنة أداء النماذج"
                      persistent-hint
                    ></v-switch>
                  </v-col>

                  <v-col cols="12" md="6">
                    <v-switch
                      v-model="learnFromResults"
                      label="التعلم من النتائج"
                      hint="تحليل النتائج وتوليد توصيات لتحسين الأداء"
                      persistent-hint
                    ></v-switch>
                  </v-col>
                </v-row>

                <v-divider class="my-4"></v-divider>

                <v-row>
                  <v-col cols="12">
                    <v-alert type="info" outlined>
                      <div class="font-weight-bold mb-2">ملخص الاختبار:</div>
                      <ul>
                        <li>
                          النماذج المختارة:
                          {{ selectedModels.length }} نموذج
                        </li>
                        <li>عدد الصور: {{ imageFiles.length }} صورة</li>
                        <li>
                          عدد التكرارات: {{ testIterations }} تكرار
                        </li>
                        <li>
                          الوقت التقديري:
                          {{ estimatedTime }} دقيقة
                        </li>
                      </ul>
                    </v-alert>
                  </v-col>
                </v-row>
              </v-card-text>

              <v-card-actions>
                <v-btn text @click="currentStep = 2">
                  <v-icon left>mdi-arrow-right</v-icon>
                  السابق
                </v-btn>
                <v-spacer></v-spacer>
                <v-btn
                  color="primary"
                  :loading="isRunningBenchmark"
                  :disabled="isRunningBenchmark"
                  @click="runBenchmark"
                >
                  بدء الاختبار
                  <v-icon right>mdi-play</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-stepper-content>

          <!-- الخطوة 4: نتائج الاختبار -->
          <v-stepper-step step="4">
            نتائج الاختبار
            <small>عرض نتائج المقارنة</small>
          </v-stepper-step>

          <v-stepper-content step="4">
            <v-card flat>
              <v-card-text>
                <v-skeleton-loader
                  v-if="isLoadingResults"
                  type="card, list-item-three-line, image, table"
                ></v-skeleton-loader>

                <div v-else-if="benchmarkResults">
                  <v-tabs v-model="activeResultTab" background-color="transparent" grow>
                    <v-tab>
                      <v-icon left>mdi-chart-bar</v-icon>
                      الأداء
                    </v-tab>
                    <v-tab>
                      <v-icon left>mdi-clock-fast</v-icon>
                      السرعة
                    </v-tab>
                    <v-tab>
                      <v-icon left>mdi-memory</v-icon>
                      الموارد
                    </v-tab>
                    <v-tab>
                      <v-icon left>mdi-lightbulb-on</v-icon>
                      التوصيات
                    </v-tab>
                  </v-tabs>

                  <v-tabs-items v-model="activeResultTab">
                    <!-- تبويب الأداء -->
                    <v-tab-item>
                      <v-card flat>
                        <v-card-text>
                          <v-row>
                            <v-col cols="12">
                              <h3 class="text-h5 primary--text mb-4">
                                مقارنة دقة النماذج
                              </h3>
                              <v-img
                                v-if="benchmarkResults.plot_path"
                                :src="getPlotUrl(benchmarkResults.plot_path)"
                                max-height="500"
                                contain
                              ></v-img>
                              <performance-chart
                                v-else
                                :results="benchmarkResults.results"
                              ></performance-chart>
                            </v-col>
                          </v-row>

                          <v-row>
                            <v-col cols="12">
                              <h3 class="text-h5 primary--text mb-4">
                                جدول مقارنة الدقة
                              </h3>
                              <v-data-table
                                :headers="performanceHeaders"
                                :items="performanceItems"
                                class="elevation-1"
                                :footer-props="{
                                  'items-per-page-options': [5, 10, 15],
                                  'items-per-page-text': 'عدد النماذج في الصفحة',
                                }"
                              >
                                <template v-slot:item.accuracy="{ item }">
                                  <v-progress-linear
                                    :value="item.accuracy * 100"
                                    height="20"
                                    striped
                                    color="success"
                                  >
                                    <template v-slot:default="{ value }">
                                      <strong>{{ value.toFixed(1) }}%</strong>
                                    </template>
                                  </v-progress-linear>
                                </template>
                              </v-data-table>
                            </v-col>
                          </v-row>
                        </v-card-text>
                      </v-card>
                    </v-tab-item>

                    <!-- تبويب السرعة -->
                    <v-tab-item>
                      <v-card flat>
                        <v-card-text>
                          <v-row>
                            <v-col cols="12">
                              <h3 class="text-h5 primary--text mb-4">
                                مقارنة سرعة النماذج
                              </h3>
                              <speed-chart
                                :results="benchmarkResults.results"
                              ></speed-chart>
                            </v-col>
                          </v-row>

                          <v-row>
                            <v-col cols="12">
                              <h3 class="text-h5 primary--text mb-4">
                                جدول مقارنة السرعة
                              </h3>
                              <v-data-table
                                :headers="speedHeaders"
                                :items="speedItems"
                                class="elevation-1"
                                :footer-props="{
                                  'items-per-page-options': [5, 10, 15],
                                  'items-per-page-text': 'عدد النماذج في الصفحة',
                                }"
                              >
                                <template v-slot:item.fps="{ item }">
                                  <v-progress-linear
                                    :value="getFpsPercentage(item.fps)"
                                    height="20"
                                    striped
                                    color="info"
                                  >
                                    <template v-slot:default="{ value }">
                                      <strong>{{ item.fps.toFixed(1) }} FPS</strong>
                                    </template>
                                  </v-progress-linear>
                                </template>
                              </v-data-table>
                            </v-col>
                          </v-row>
                        </v-card-text>
                      </v-card>
                    </v-tab-item>

                    <!-- تبويب الموارد -->
                    <v-tab-item>
                      <v-card flat>
                        <v-card-text>
                          <v-row>
                            <v-col cols="12">
                              <h3 class="text-h5 primary--text mb-4">
                                مقارنة استهلاك الموارد
                              </h3>
                              <resources-chart
                                :results="benchmarkResults.results"
                              ></resources-chart>
                            </v-col>
                          </v-row>

                          <v-row>
                            <v-col cols="12">
                              <h3 class="text-h5 primary--text mb-4">
                                جدول مقارنة استهلاك الموارد
                              </h3>
                              <v-data-table
                                :headers="resourceHeaders"
                                :items="resourceItems"
                                class="elevation-1"
                                :footer-props="{
                                  'items-per-page-options': [5, 10, 15],
                                  'items-per-page-text': 'عدد النماذج في الصفحة',
                                }"
                              >
                                <template v-slot:item.memory_used="{ item }">
                                  <v-progress-linear
                                    :value="getMemoryPercentage(item.memory_used)"
                                    height="20"
                                    striped
                                    color="error"
                                  >
                                    <template v-slot:default="{ value }">
                                      <strong>{{ item.memory_used.toFixed(2) }} GB</strong>
                                    </template>
                                  </v-progress-linear>
                                </template>

                                <template v-slot:item.cpu_usage="{ item }">
                                  <v-progress-linear
                                    :value="item.cpu_usage"
                                    height="20"
                                    striped
                                    color="warning"
                                  >
                                    <template v-slot:default="{ value }">
                                      <strong>{{ value.toFixed(1) }}%</strong>
                                    </template>
                                  </v-progress-linear>
                                </template>
                              </v-data-table>
                            </v-col>
                          </v-row>
                        </v-card-text>
                      </v-card>
                    </v-tab-item>

                    <!-- تبويب التوصيات -->
                    <v-tab-item>
                      <v-card flat>
                        <v-card-text>
                          <v-row>
                            <v-col cols="12">
                              <h3 class="text-h5 primary--text mb-4">
                                التوصيات والاستنتاجات
                              </h3>

                              <v-card outlined class="mb-4">
                                <v-card-title class="success--text">
                                  <v-icon left color="success">mdi-trophy</v-icon>
                                  أفضل نموذج من حيث الدقة
                                </v-card-title>
                                <v-card-text>
                                  <div class="d-flex align-center">
                                    <v-avatar color="success" size="40" class="white--text mr-4">
                                      <v-icon>mdi-check</v-icon>
                                    </v-avatar>
                                    <div>
                                      <div class="text-h6">{{ bestAccuracyModel.name }}</div>
                                      <div>الدقة: {{ (bestAccuracyModel.accuracy * 100).toFixed(2) }}%</div>
                                    </div>
                                  </div>
                                </v-card-text>
                              </v-card>

                              <v-card outlined class="mb-4">
                                <v-card-title class="info--text">
                                  <v-icon left color="info">mdi-speedometer</v-icon>
                                  أسرع نموذج
                                </v-card-title>
                                <v-card-text>
                                  <div class="d-flex align-center">
                                    <v-avatar color="info" size="40" class="white--text mr-4">
                                      <v-icon>mdi-flash</v-icon>
                                    </v-avatar>
                                    <div>
                                      <div class="text-h6">{{ fastestModel.name }}</div>
                                      <div>السرعة: {{ fastestModel.fps.toFixed(2) }} FPS</div>
                                    </div>
                                  </div>
                                </v-card-text>
                              </v-card>

                              <v-card outlined class="mb-4">
                                <v-card-title class="warning--text">
                                  <v-icon left color="warning">mdi-memory</v-icon>
                                  الأكثر كفاءة في استهلاك الموارد
                                </v-card-title>
                                <v-card-text>
                                  <div class="d-flex align-center">
                                    <v-avatar color="warning" size="40" class="white--text mr-4">
                                      <v-icon>mdi-leaf</v-icon>
                                    </v-avatar>
                                    <div>
                                      <div class="text-h6">{{ mostEfficientModel.name }}</div>
                                      <div>استهلاك الذاكرة: {{ mostEfficientModel.memory_used.toFixed(2) }} GB</div>
                                    </div>
                                  </div>
                                </v-card-text>
                              </v-card>

                              <v-divider class="my-4"></v-divider>

                              <h3 class="text-h5 primary--text mb-4">
                                توصيات الاستخدام
                              </h3>

                              <v-alert type="success" outlined>
                                <div class="font-weight-bold">للدقة العالية:</div>
                                <p>استخدم نموذج {{ bestAccuracyModel.name }} للحصول على أفضل دقة في تشخيص أمراض النباتات.</p>
                              </v-alert>

                              <v-alert type="info" outlined>
                                <div class="font-weight-bold">للتطبيقات الفورية:</div>
                                <p>استخدم نموذج {{ fastestModel.name }} للحصول على استجابة سريعة في التطبيقات التي تتطلب معالجة فورية.</p>
                              </v-alert>

                              <v-alert type="warning" outlined>
                                <div class="font-weight-bold">للأجهزة المحدودة:</div>
                                <p>استخدم نموذج {{ mostEfficientModel.name }} للأجهزة ذات الموارد المحدودة أو التطبيقات المحمولة.</p>
                              </v-alert>

                              <v-divider class="my-4"></v-divider>

                              <h3 class="text-h5 primary--text mb-4">
                                التعلم من النتائج
                              </h3>

                              <v-alert
                                v-if="benchmarkResults.learning_results"
                                type="info"
                                outlined
                              >
                                <div v-html="formatLearningResults(benchmarkResults.learning_results)"></div>
                              </v-alert>

                              <v-alert v-else type="warning" outlined>
                                لم يتم تفعيل وحدة التعلم من النتائج أو لم يتم العثور على نتائج.
                              </v-alert>
                            </v-col>
                          </v-row>
                        </v-card-text>
                      </v-card>
                    </v-tab-item>
                  </v-tabs-items>
                </div>

                <v-alert
                  v-else-if="benchmarkError"
                  type="error"
                  outlined
                >
                  {{ benchmarkError }}
                </v-alert>

                <v-alert
                  v-else
                  type="info"
                  outlined
                >
                  لم يتم تشغيل أي اختبار بعد. يرجى إكمال الخطوات السابقة وبدء الاختبار.
                </v-alert>
              </v-card-text>

              <v-card-actions>
                <v-btn text @click="currentStep = 3">
                  <v-icon left>mdi-arrow-right</v-icon>
                  السابق
                </v-btn>
                <v-spacer></v-spacer>
                <v-btn
                  v-if="benchmarkResults"
                  color="success"
                  @click="downloadReport"
                >
                  <v-icon left>mdi-download</v-icon>
                  تحميل التقرير
                </v-btn>
                <v-btn
                  color="primary"
                  @click="resetBenchmark"
                >
                  <v-icon left>mdi-refresh</v-icon>
                  اختبار جديد
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-stepper-content>
        </v-stepper>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { plantDiseaseService } from '@/services/plantDiseaseService';

export default {
  name: 'ModelComparisonTool',
  
  components: {
    PerformanceChart: () => import('./charts/PerformanceChart.vue'),
    SpeedChart: () => import('./charts/SpeedChart.vue'),
    ResourcesChart: () => import('./charts/ResourcesChart.vue')
  },
  
  data() {
    return {
      currentStep: 1,
      availableModels: [],
      selectedModels: [],
      imageFiles: [],
      datasetType: 'plantvillage',
      testIterations: 3,
      monitorResources: true,
      generateVisualizations: true,
      learnFromResults: true,
      isRunningBenchmark: false,
      isLoadingResults: false,
      benchmarkResults: null,
      benchmarkError: null,
      activeResultTab: 0,
      
      // جداول البيانات
      modelHeaders: [
        { text: 'اسم النموذج', value: 'name' },
        { text: 'النوع', value: 'type' },
        { text: 'عدد المعلمات', value: 'parameters' },
        { text: 'الوصف', value: 'description' }
      ],
      
      imageHeaders: [
        { text: 'معاينة', value: 'preview', sortable: false },
        { text: 'اسم الملف', value: 'name' },
        { text: 'الحجم', value: 'size' },
        { text: 'التسمية', value: 'label' }
      ],
      
      performanceHeaders: [
        { text: 'النموذج', value: 'name' },
        { text: 'الدقة', value: 'accuracy' },
        { text: 'F1-Score', value: 'f1_score' },
        { text: 'الثقة المتوسطة', value: 'avg_confidence' },
        { text: 'الاستقرار', value: 'consistency' }
      ],
      
      speedHeaders: [
        { text: 'النموذج', value: 'name' },
        { text: 'السرعة (FPS)', value: 'fps' },
        { text: 'زمن التنبؤ (ثانية)', value: 'inference_time' },
        { text: 'الانحراف المعياري', value: 'std_time' }
      ],
      
      resourceHeaders: [
        { text: 'النموذج', value: 'name' },
        { text: 'استهلاك الذاكرة (GB)', value: 'memory_used' },
        { text: 'استهلاك المعالج (%)', value: 'cpu_usage' },
        { text: 'ذاكرة GPU (GB)', value: 'gpu_memory' }
      ],
      
      // القواعد
      rules: {
        required: value => !!value || 'هذا الحقل مطلوب',
        maxFiles: value => !value || value.length <= 50 || 'الحد الأقصى هو 50 صورة'
      },
      
      // أنواع مجموعات البيانات
      datasetTypes: [
        { text: 'PlantVillage', value: 'plantvillage' },
        { text: 'PlantDoc', value: 'plantdoc' },
        { text: 'مخصص', value: 'custom' }
      ],
      
      // التسميات المتاحة
      availableLabels: []
    };
  },
  
  computed: {
    imageFilesWithLabels() {
      return this.imageFiles.map((file, index) => {
        return {
          id: index,
          file: file,
          name: file.name,
          size: this.formatFileSize(file.size),
          label: this.getDefaultLabel(file.name, index)
        };
      });
    },
    
    estimatedTime() {
      // تقدير الوقت بناءً على عدد النماذج والصور والتكرارات
      const modelsCount = this.selectedModels.length || 1;
      const imagesCount = this.imageFiles.length || 1;
      const iterationsCount = this.testIterations || 1;
      
      // تقدير متوسط الوقت لكل صورة (بالثواني)
      const avgTimePerImage = 0.5;
      
      // حساب الوقت الإجمالي بالدقائق
      const totalTimeSeconds = modelsCount * imagesCount * iterationsCount * avgTimePerImage;
      const totalTimeMinutes = totalTimeSeconds / 60;
      
      return totalTimeMinutes.toFixed(1);
    },
    
    performanceItems() {
      if (!this.benchmarkResults || !this.benchmarkResults.results) return [];
      
      return Object.entries(this.benchmarkResults.results).map(([name, result]) => {
        return {
          name: name,
          accuracy: result.metrics.accuracy.mean,
          f1_score: result.metrics.f1_score.mean,
          avg_confidence: result.metrics.avg_confidence.mean,
          consistency: result.stability.consistency_score
        };
      });
    },
    
    speedItems() {
      if (!this.benchmarkResults || !this.benchmarkResults.results) return [];
      
      return Object.entries(this.benchmarkResults.results).map(([name, result]) => {
        return {
          name: name,
          fps: result.timing.fps.mean,
          inference_time: result.timing.avg_inference_time.mean,
          std_time: result.timing.avg_inference_time.std
        };
      });
    },
    
    resourceItems() {
      if (!this.benchmarkResults || !this.benchmarkResults.results) return [];
      
      return Object.entries(this.benchmarkResults.results).map(([name, result]) => {
        return {
          name: name,
          memory_used: result.resource_usage.memory_used.mean,
          cpu_usage: result.resource_usage.cpu_usage.mean,
          gpu_memory: result.resource_usage.gpu_memory_used ? result.resource_usage.gpu_memory_used.mean : 0
        };
      });
    },
    
    bestAccuracyModel() {
      if (!this.performanceItems.length) return { name: 'غير متاح', accuracy: 0 };
      
      return this.performanceItems.reduce((best, current) => {
        return current.accuracy > best.accuracy ? current : best;
      }, { name: '', accuracy: 0 });
    },
    
    fastestModel() {
      if (!this.speedItems.length) return { name: 'غير متاح', fps: 0 };
      
      return this.speedItems.reduce((fastest, current) => {
        return current.fps > fastest.fps ? current : fastest;
      }, { name: '', fps: 0 });
    },
    
    mostEfficientModel() {
      if (!this.resourceItems.length) return { name: 'غير متاح', memory_used: 0 };
      
      return this.resourceItems.reduce((efficient, current) => {
        return current.memory_used < efficient.memory_used ? current : efficient;
      }, { name: '', memory_used: Number.MAX_VALUE });
    }
  },
  
  async created() {
    await this.loadAvailableModels();
    this.loadAvailableLabels();
  },
  
  methods: {
    async loadAvailableModels() {
      try {
        const response = await plantDiseaseService.getAvailableModels();
        if (response && response.models) {
          this.availableModels = Object.entries(response.models).map(([name, details]) => ({
            name,
            ...details
          }));
        }
      } catch (error) {
        console.error('خطأ في تحميل النماذج المتاحة:', error);
        this.$store.dispatch('notifications/addNotification', {
          type: 'error',
          message: 'فشل في تحميل النماذج المتاحة'
        });
      }
    },
    
    loadAvailableLabels() {
      // تحميل التسميات حسب نوع مجموعة البيانات
      if (this.datasetType === 'plantvillage') {
        this.availableLabels = Array.from({ length: 38 }, (_, i) => ({
          text: `الفئة ${i}`,
          value: i
        }));
      } else if (this.datasetType === 'plantdoc') {
        this.availableLabels = Array.from({ length: 27 }, (_, i) => ({
          text: `الفئة ${i}`,
          value: i
        }));
      } else {
        this.availableLabels = Array.from({ length: 10 }, (_, i) => ({
          text: `الفئة ${i}`,
          value: i
        }));
      }
    },
    
    getDefaultLabel(fileName, index) {
      // محاولة استخراج التسمية من اسم الملف
      const labelMatch = fileName.match(/label[_-](\d+)/i);
      if (labelMatch && labelMatch[1]) {
        return parseInt(labelMatch[1]);
      }
      
      // استخدام التسمية الافتراضية
      return 0;
    },
    
    getModelTypeColor(type) {
      const colors = {
        huggingface: 'deep-purple',
        tensorflow: 'orange',
        pytorch: 'red',
        keras: 'blue',
        unknown: 'grey'
      };
      
      return colors[type] || 'grey';
    },
    
    formatNumber(num) {
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
    
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    
    getImagePreview(file) {
      return URL.createObjectURL(file);
    },
    
    getFpsPercentage(fps) {
      // تحويل FPS إلى نسبة مئوية (بحد أقصى 60 FPS)
      return Math.min(100, (fps / 60) * 100);
    },
    
    getMemoryPercentage(memory) {
      // تحويل استهلاك الذاكرة إلى نسبة مئوية (بحد أقصى 8 GB)
      return Math.min(100, (memory / 8) * 100);
    },
    
    getPlotUrl(path) {
      // تحويل مسار الملف إلى URL
      return `/api/files?path=${encodeURIComponent(path)}`;
    },
    
    formatLearningResults(results) {
      if (!results) return 'لا توجد نتائج للتعلم';
      
      // تنسيق نتائج التعلم
      let html = '<div class="learning-results">';
      
      if (results.patterns) {
        html += '<h4>الأنماط المكتشفة:</h4><ul>';
        results.patterns.forEach(pattern => {
          html += `<li>${pattern}</li>`;
        });
        html += '</ul>';
      }
      
      if (results.recommendations) {
        html += '<h4>التوصيات:</h4><ul>';
        results.recommendations.forEach(rec => {
          html += `<li>${rec}</li>`;
        });
        html += '</ul>';
      }
      
      html += '</div>';
      return html;
    },
    
    async runBenchmark() {
      if (this.isRunningBenchmark) return;
      
      this.isRunningBenchmark = true;
      this.benchmarkError = null;
      
      try {
        // تحميل الصور
        const uploadResult = await this.uploadImages();
        
        if (uploadResult.error) {
          throw new Error(uploadResult.error);
        }
        
        // تشغيل الاختبار
        this.isLoadingResults = true;
        this.currentStep = 4;
        
        const benchmarkResult = await plantDiseaseService.runBenchmark({
          image_paths: uploadResult.image_paths,
          ground_truth: uploadResult.ground_truth,
          models: this.selectedModels.map(model => model.name),
          iterations: this.testIterations,
          monitor_resources: this.monitorResources,
          generate_visualizations: this.generateVisualizations,
          learn_from_results: this.learnFromResults
        });
        
        if (benchmarkResult.error) {
          throw new Error(benchmarkResult.error);
        }
        
        this.benchmarkResults = benchmarkResult;
      } catch (error) {
        console.error('خطأ في تشغيل الاختبار:', error);
        this.benchmarkError = `فشل في تشغيل الاختبار: ${error.message || 'خطأ غير معروف'}`;
        this.$store.dispatch('notifications/addNotification', {
          type: 'error',
          message: 'فشل في تشغيل الاختبار'
        });
      } finally {
        this.isRunningBenchmark = false;
        this.isLoadingResults = false;
      }
    },
    
    async uploadImages() {
      try {
        const formData = new FormData();
        
        // إضافة الصور إلى النموذج
        this.imageFiles.forEach((file, index) => {
          formData.append(`images[${index}]`, file);
          
          // البحث عن التسمية المقابلة
          const imageData = this.imageFilesWithLabels.find(img => img.id === index);
          if (imageData) {
            formData.append(`labels[${index}]`, imageData.label);
          }
        });
        
        // تحميل الصور
        const response = await plantDiseaseService.uploadTestImages(formData);
        return response;
      } catch (error) {
        console.error('خطأ في تحميل الصور:', error);
        return { error: 'فشل في تحميل الصور' };
      }
    },
    
    async downloadReport() {
      if (!this.benchmarkResults || !this.benchmarkResults.report_path) {
        this.$store.dispatch('notifications/addNotification', {
          type: 'warning',
          message: 'لا يوجد تقرير متاح للتحميل'
        });
        return;
      }
      
      try {
        const response = await plantDiseaseService.downloadBenchmarkReport(this.benchmarkResults.report_path);
        
        // إنشاء رابط تحميل
        const url = window.URL.createObjectURL(new Blob([response]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `benchmark_report_${new Date().toISOString().slice(0, 10)}.json`);
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (error) {
        console.error('خطأ في تحميل التقرير:', error);
        this.$store.dispatch('notifications/addNotification', {
          type: 'error',
          message: 'فشل في تحميل التقرير'
        });
      }
    },
    
    resetBenchmark() {
      this.currentStep = 1;
      this.selectedModels = [];
      this.imageFiles = [];
      this.benchmarkResults = null;
      this.benchmarkError = null;
      this.activeResultTab = 0;
    }
  },
  
  watch: {
    datasetType() {
      this.loadAvailableLabels();
    }
  }
};
</script>

<style lang="scss" scoped>
.model-comparison-tool {
  .label-select {
    max-width: 120px;
  }
  
  .learning-results {
    h4 {
      margin-top: 16px;
      margin-bottom: 8px;
      color: var(--v-primary-base);
    }
  }
}
</style>
