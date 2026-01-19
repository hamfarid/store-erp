<!--
مكون إعدادات تحليل النماذج
يوفر هذا المكون واجهة لتكوين وإدارة إعدادات تحليل النماذج
بما في ذلك تمكين وتعطيل وحدات التحليل المختلفة وتخصيص معلمات التحليل

المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
-->

<template>
  <div class="model-analysis-settings">
    <v-card>
      <v-card-title class="primary--text">
        <v-icon large color="primary" class="ml-2">mdi-cog-outline</v-icon>
        إعدادات تحليل النماذج
      </v-card-title>
      <v-card-subtitle>
        تكوين وإدارة إعدادات تحليل النماذج وتمكين أو تعطيل وحدات التحليل المختلفة
      </v-card-subtitle>
      <v-card-text>
        <v-alert
          v-if="error"
          type="error"
          dense
          dismissible
          class="mb-4"
        >
          {{ error }}
        </v-alert>

        <v-alert
          v-if="success"
          type="success"
          dense
          dismissible
          class="mb-4"
        >
          {{ success }}
        </v-alert>

        <v-form ref="form" v-model="valid">
          <!-- تمكين/تعطيل وحدات التحليل -->
          <v-card outlined class="mb-4">
            <v-card-title class="subtitle-1">وحدات التحليل</v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12" md="6">
                  <v-switch
                    v-model="settings.modules.benchmark_system.enabled"
                    :label="'نظام اختبار ومقارنة النماذج ' + (settings.modules.benchmark_system.enabled ? '(مفعل)' : '(معطل)')"
                    color="primary"
                    :disabled="loading"
                  ></v-switch>
                  <v-switch
                    v-model="settings.modules.learning_system.enabled"
                    :label="'نظام التعلم من النماذج ' + (settings.modules.learning_system.enabled ? '(مفعل)' : '(معطل)')"
                    color="primary"
                    :disabled="loading"
                  ></v-switch>
                </v-col>
                <v-col cols="12" md="6">
                  <v-switch
                    v-model="settings.modules.attention_analyzer.enabled"
                    :label="'محلل أنماط الانتباه ' + (settings.modules.attention_analyzer.enabled ? '(مفعل)' : '(معطل)')"
                    color="primary"
                    :disabled="loading"
                  ></v-switch>
                  <v-switch
                    v-model="settings.modules.robustness_analyzer.enabled"
                    :label="'محلل قوة ومتانة النماذج ' + (settings.modules.robustness_analyzer.enabled ? '(مفعل)' : '(معطل)')"
                    color="primary"
                    :disabled="loading"
                  ></v-switch>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- إعدادات نظام اختبار ومقارنة النماذج -->
          <v-card outlined class="mb-4">
            <v-card-title class="subtitle-1">
              إعدادات نظام اختبار ومقارنة النماذج
              <v-spacer></v-spacer>
              <v-btn
                icon
                small
                @click="expandedCards.benchmark = !expandedCards.benchmark"
              >
                <v-icon>{{ expandedCards.benchmark ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
              </v-btn>
            </v-card-title>
            <v-expand-transition>
              <div v-show="expandedCards.benchmark">
                <v-card-text>
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model.number="settings.modules.benchmark_system.default_iterations"
                        label="عدد التكرارات الافتراضي"
                        type="number"
                        min="1"
                        max="10"
                        :rules="[v => v > 0 || 'يجب أن يكون العدد أكبر من صفر']"
                        :disabled="loading || !settings.modules.benchmark_system.enabled"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-select
                        v-model="settings.modules.benchmark_system.metrics"
                        :items="availableMetrics"
                        label="مقاييس الأداء"
                        multiple
                        chips
                        :disabled="loading || !settings.modules.benchmark_system.enabled"
                      ></v-select>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-switch
                        v-model="settings.modules.benchmark_system.monitor_resources"
                        label="مراقبة استهلاك الموارد"
                        color="primary"
                        :disabled="loading || !settings.modules.benchmark_system.enabled"
                      ></v-switch>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-switch
                        v-model="settings.modules.benchmark_system.save_visualizations"
                        label="حفظ المخططات البيانية"
                        color="primary"
                        :disabled="loading || !settings.modules.benchmark_system.enabled"
                      ></v-switch>
                    </v-col>
                  </v-row>
                </v-card-text>
              </div>
            </v-expand-transition>
          </v-card>

          <!-- إعدادات نظام التعلم من النماذج -->
          <v-card outlined class="mb-4">
            <v-card-title class="subtitle-1">
              إعدادات نظام التعلم من النماذج
              <v-spacer></v-spacer>
              <v-btn
                icon
                small
                @click="expandedCards.learning = !expandedCards.learning"
              >
                <v-icon>{{ expandedCards.learning ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
              </v-btn>
            </v-card-title>
            <v-expand-transition>
              <div v-show="expandedCards.learning">
                <v-card-text>
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-switch
                        v-model="settings.modules.learning_system.auto_learn"
                        label="التعلم التلقائي بعد الاختبار"
                        color="primary"
                        :disabled="loading || !settings.modules.learning_system.enabled"
                      ></v-switch>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-switch
                        v-model="settings.modules.learning_system.save_history"
                        label="حفظ سجل التعلم"
                        color="primary"
                        :disabled="loading || !settings.modules.learning_system.enabled"
                      ></v-switch>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model.number="settings.modules.learning_system.max_history_items"
                        label="الحد الأقصى لعناصر السجل"
                        type="number"
                        min="1"
                        max="100"
                        :rules="[v => v > 0 || 'يجب أن يكون العدد أكبر من صفر']"
                        :disabled="loading || !settings.modules.learning_system.enabled || !settings.modules.learning_system.save_history"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-select
                        v-model="settings.modules.learning_system.learning_mode"
                        :items="learningModes"
                        item-text="text"
                        item-value="value"
                        label="وضع التعلم"
                        :disabled="loading || !settings.modules.learning_system.enabled"
                      ></v-select>
                    </v-col>
                  </v-row>
                </v-card-text>
              </div>
            </v-expand-transition>
          </v-card>

          <!-- إعدادات محلل أنماط الانتباه -->
          <v-card outlined class="mb-4">
            <v-card-title class="subtitle-1">
              إعدادات محلل أنماط الانتباه
              <v-spacer></v-spacer>
              <v-btn
                icon
                small
                @click="expandedCards.attention = !expandedCards.attention"
              >
                <v-icon>{{ expandedCards.attention ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
              </v-btn>
            </v-card-title>
            <v-expand-transition>
              <div v-show="expandedCards.attention">
                <v-card-text>
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-select
                        v-model="settings.modules.attention_analyzer.visualization_method"
                        :items="visualizationMethods"
                        item-text="text"
                        item-value="value"
                        label="طريقة التصور البصري"
                        :disabled="loading || !settings.modules.attention_analyzer.enabled"
                      ></v-select>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-slider
                        v-model="settings.modules.attention_analyzer.overlay_opacity"
                        label="شفافية التراكب"
                        min="0"
                        max="1"
                        step="0.1"
                        thumb-label
                        :disabled="loading || !settings.modules.attention_analyzer.enabled"
                      ></v-slider>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-switch
                        v-model="settings.modules.attention_analyzer.save_attention_maps"
                        label="حفظ خرائط الانتباه"
                        color="primary"
                        :disabled="loading || !settings.modules.attention_analyzer.enabled"
                      ></v-switch>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-select
                        v-model="settings.modules.attention_analyzer.colormap"
                        :items="colormaps"
                        label="خريطة الألوان"
                        :disabled="loading || !settings.modules.attention_analyzer.enabled"
                      ></v-select>
                    </v-col>
                  </v-row>
                </v-card-text>
              </div>
            </v-expand-transition>
          </v-card>

          <!-- إعدادات محلل قوة ومتانة النماذج -->
          <v-card outlined class="mb-4">
            <v-card-title class="subtitle-1">
              إعدادات محلل قوة ومتانة النماذج
              <v-spacer></v-spacer>
              <v-btn
                icon
                small
                @click="expandedCards.robustness = !expandedCards.robustness"
              >
                <v-icon>{{ expandedCards.robustness ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
              </v-btn>
            </v-card-title>
            <v-expand-transition>
              <div v-show="expandedCards.robustness">
                <v-card-text>
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-checkbox
                        v-model="settings.modules.robustness_analyzer.tests.noise"
                        label="اختبار مقاومة الضوضاء"
                        color="primary"
                        :disabled="loading || !settings.modules.robustness_analyzer.enabled"
                      ></v-checkbox>
                      <v-checkbox
                        v-model="settings.modules.robustness_analyzer.tests.brightness"
                        label="اختبار مقاومة الإضاءة"
                        color="primary"
                        :disabled="loading || !settings.modules.robustness_analyzer.enabled"
                      ></v-checkbox>
                      <v-checkbox
                        v-model="settings.modules.robustness_analyzer.tests.rotation"
                        label="اختبار مقاومة الدوران"
                        color="primary"
                        :disabled="loading || !settings.modules.robustness_analyzer.enabled"
                      ></v-checkbox>
                      <v-checkbox
                        v-model="settings.modules.robustness_analyzer.tests.blur"
                        label="اختبار مقاومة الضبابية"
                        color="primary"
                        :disabled="loading || !settings.modules.robustness_analyzer.enabled"
                      ></v-checkbox>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-checkbox
                        v-model="settings.modules.robustness_analyzer.tests.scale"
                        label="اختبار مقاومة تغيير الحجم"
                        color="primary"
                        :disabled="loading || !settings.modules.robustness_analyzer.enabled"
                      ></v-checkbox>
                      <v-checkbox
                        v-model="settings.modules.robustness_analyzer.tests.occlusion"
                        label="اختبار مقاومة الحجب"
                        color="primary"
                        :disabled="loading || !settings.modules.robustness_analyzer.enabled"
                      ></v-checkbox>
                      <v-checkbox
                        v-model="settings.modules.robustness_analyzer.tests.compression"
                        label="اختبار مقاومة الضغط"
                        color="primary"
                        :disabled="loading || !settings.modules.robustness_analyzer.enabled"
                      ></v-checkbox>
                      <v-checkbox
                        v-model="settings.modules.robustness_analyzer.save_visualizations"
                        label="حفظ المخططات البيانية"
                        color="primary"
                        :disabled="loading || !settings.modules.robustness_analyzer.enabled"
                      ></v-checkbox>
                    </v-col>
                  </v-row>
                </v-card-text>
              </div>
            </v-expand-transition>
          </v-card>

          <!-- أزرار التحكم -->
          <v-row>
            <v-col cols="12" md="4">
              <v-btn
                color="primary"
                block
                :loading="loading"
                :disabled="!valid"
                @click="saveSettings"
              >
                <v-icon left>mdi-content-save</v-icon>
                حفظ الإعدادات
              </v-btn>
            </v-col>
            <v-col cols="12" md="4">
              <v-btn
                color="secondary"
                block
                :loading="loading"
                @click="resetSettings"
              >
                <v-icon left>mdi-refresh</v-icon>
                إعادة تعيين
              </v-btn>
            </v-col>
            <v-col cols="12" md="4">
              <v-btn
                color="error"
                block
                :loading="loading"
                @click="restoreDefaults"
              >
                <v-icon left>mdi-restore</v-icon>
                استعادة الإعدادات الافتراضية
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'ModelAnalysisSettings',
  
  data() {
    return {
      valid: true,
      loading: false,
      error: null,
      success: null,
      settings: {
        modules: {
          benchmark_system: {
            enabled: true,
            default_iterations: 3,
            metrics: ['accuracy', 'precision', 'recall', 'f1_score'],
            monitor_resources: true,
            save_visualizations: true
          },
          learning_system: {
            enabled: true,
            auto_learn: true,
            save_history: true,
            max_history_items: 50,
            learning_mode: 'comprehensive'
          },
          attention_analyzer: {
            enabled: true,
            visualization_method: 'gradcam',
            overlay_opacity: 0.7,
            save_attention_maps: true,
            colormap: 'jet'
          },
          robustness_analyzer: {
            enabled: true,
            tests: {
              noise: true,
              brightness: true,
              rotation: true,
              blur: true,
              scale: true,
              occlusion: true,
              compression: true
            },
            save_visualizations: true
          }
        }
      },
      originalSettings: null,
      expandedCards: {
        benchmark: false,
        learning: false,
        attention: false,
        robustness: false
      },
      availableMetrics: [
        'accuracy',
        'precision',
        'recall',
        'f1_score',
        'confusion_matrix',
        'roc_auc',
        'precision_recall_curve'
      ],
      learningModes: [
        { text: 'شامل (جميع المقاييس)', value: 'comprehensive' },
        { text: 'سريع (المقاييس الأساسية فقط)', value: 'fast' },
        { text: 'مخصص', value: 'custom' }
      ],
      visualizationMethods: [
        { text: 'Grad-CAM', value: 'gradcam' },
        { text: 'Grad-CAM++', value: 'gradcam++' },
        { text: 'Score-CAM', value: 'scorecam' },
        { text: 'Layer-CAM', value: 'layercam' }
      ],
      colormaps: [
        'jet',
        'viridis',
        'plasma',
        'inferno',
        'magma',
        'cividis',
        'hot',
        'cool'
      ]
    };
  },
  
  mounted() {
    this.fetchSettings();
  },
  
  methods: {
    async fetchSettings() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await this.$store.dispatch('plantDisease/fetchModelAnalysisSettings');
        
        if (response.error) {
          throw new Error(response.error);
        }
        
        // تحديث الإعدادات
        this.settings = response;
        
        // حفظ نسخة من الإعدادات الأصلية
        this.originalSettings = JSON.parse(JSON.stringify(response));
        
      } catch (error) {
        this.error = `خطأ في جلب الإعدادات: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },
    
    async saveSettings() {
      if (!this.$refs.form.validate()) {
        return;
      }
      
      this.loading = true;
      this.error = null;
      this.success = null;
      
      try {
        const response = await this.$store.dispatch('plantDisease/saveModelAnalysisSettings', this.settings);
        
        if (response.error) {
          throw new Error(response.error);
        }
        
        // تحديث نسخة الإعدادات الأصلية
        this.originalSettings = JSON.parse(JSON.stringify(this.settings));
        
        this.success = 'تم حفظ الإعدادات بنجاح';
        
      } catch (error) {
        this.error = `خطأ في حفظ الإعدادات: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },
    
    resetSettings() {
      if (this.originalSettings) {
        this.settings = JSON.parse(JSON.stringify(this.originalSettings));
      }
    },
    
    async restoreDefaults() {
      this.loading = true;
      this.error = null;
      this.success = null;
      
      try {
        const response = await this.$store.dispatch('plantDisease/restoreDefaultModelAnalysisSettings');
        
        if (response.error) {
          throw new Error(response.error);
        }
        
        // تحديث الإعدادات
        this.settings = response;
        
        // تحديث نسخة الإعدادات الأصلية
        this.originalSettings = JSON.parse(JSON.stringify(response));
        
        this.success = 'تم استعادة الإعدادات الافتراضية بنجاح';
        
      } catch (error) {
        this.error = `خطأ في استعادة الإعدادات الافتراضية: ${error.message}`;
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.v-card {
  margin-bottom: 16px;
}
</style>
