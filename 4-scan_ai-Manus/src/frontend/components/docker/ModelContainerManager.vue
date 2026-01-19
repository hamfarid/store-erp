<!--
مكون إدارة حاويات النماذج
يوفر هذا المكون واجهة لإدارة حاويات النماذج وتثبيت واختبار النماذج الخارجية وأدوات التحليل

المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
-->

<template>
  <div class="model-container-manager">
    <v-card>
      <v-card-title class="primary--text">
        <v-icon large color="primary" class="ml-2">mdi-docker</v-icon>
        إدارة حاويات النماذج
      </v-card-title>
      <v-card-subtitle>
        تثبيت وإدارة واختبار النماذج الخارجية وأدوات التحليل
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

        <!-- قسم الحاويات النشطة -->
        <v-card outlined class="mb-4">
          <v-card-title class="subtitle-1">
            <v-icon class="ml-2">mdi-play-circle-outline</v-icon>
            الحاويات النشطة
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="activeContainersHeaders"
              :items="activeContainers"
              :items-per-page="5"
              :loading="loading"
              class="elevation-1"
            >
              <template v-slot:item.status="{ item }">
                <v-chip
                  :color="getStatusColor(item.status)"
                  small
                >
                  {{ item.status }}
                </v-chip>
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn
                  small
                  icon
                  color="primary"
                  @click="viewContainerDetails(item)"
                  :disabled="loading"
                >
                  <v-icon small>mdi-eye</v-icon>
                </v-btn>
                <v-btn
                  small
                  icon
                  color="error"
                  @click="stopContainer(item)"
                  :disabled="loading || item.status !== 'running'"
                >
                  <v-icon small>mdi-stop</v-icon>
                </v-btn>
                <v-btn
                  small
                  icon
                  color="warning"
                  @click="restartContainer(item)"
                  :disabled="loading || item.status !== 'running'"
                >
                  <v-icon small>mdi-restart</v-icon>
                </v-btn>
                <v-btn
                  small
                  icon
                  color="success"
                  @click="testContainer(item)"
                  :disabled="loading || item.status !== 'running'"
                >
                  <v-icon small>mdi-check-circle</v-icon>
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>

        <!-- قسم تثبيت نموذج جديد -->
        <v-card outlined class="mb-4">
          <v-card-title class="subtitle-1">
            <v-icon class="ml-2">mdi-plus-circle-outline</v-icon>
            تثبيت نموذج جديد
          </v-card-title>
          <v-card-text>
            <v-form ref="installForm" v-model="installFormValid">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="newModel.name"
                    label="اسم النموذج"
                    :rules="[v => !!v || 'الاسم مطلوب']"
                    :disabled="loading"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-select
                    v-model="newModel.type"
                    :items="modelTypes"
                    item-text="text"
                    item-value="value"
                    label="نوع النموذج"
                    :rules="[v => !!v || 'النوع مطلوب']"
                    :disabled="loading"
                  ></v-select>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="newModel.source"
                    label="مصدر النموذج"
                    :rules="[v => !!v || 'المصدر مطلوب']"
                    :disabled="loading"
                    :hint="getSourceHint(newModel.type)"
                    persistent-hint
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-select
                    v-model="newModel.gpu"
                    :items="gpuOptions"
                    item-text="text"
                    item-value="value"
                    label="استخدام GPU"
                    :disabled="loading"
                  ></v-select>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <v-textarea
                    v-model="newModel.config"
                    label="إعدادات إضافية (JSON)"
                    :disabled="loading"
                    hint="إعدادات إضافية بتنسيق JSON (اختياري)"
                    persistent-hint
                    :rules="[v => !v || isValidJson(v) || 'يجب أن تكون الإعدادات بتنسيق JSON صحيح']"
                  ></v-textarea>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" md="6">
                  <v-checkbox
                    v-model="newModel.enableAttentionAnalysis"
                    label="تمكين تحليل أنماط الانتباه"
                    :disabled="loading || !supportsAttentionAnalysis(newModel.type)"
                  ></v-checkbox>
                </v-col>
                <v-col cols="12" md="6">
                  <v-checkbox
                    v-model="newModel.enableRobustnessTest"
                    label="تمكين اختبار المتانة"
                    :disabled="loading"
                  ></v-checkbox>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <v-btn
                    color="primary"
                    :loading="loading"
                    :disabled="!installFormValid"
                    @click="installModel"
                    block
                  >
                    <v-icon left>mdi-plus</v-icon>
                    تثبيت النموذج
                  </v-btn>
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>
        </v-card>

        <!-- قسم النماذج المتاحة -->
        <v-card outlined>
          <v-card-title class="subtitle-1">
            <v-icon class="ml-2">mdi-format-list-bulleted</v-icon>
            النماذج المتاحة
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="availableModelsHeaders"
              :items="availableModels"
              :items-per-page="5"
              :loading="loading"
              class="elevation-1"
            >
              <template v-slot:item.type="{ item }">
                <v-chip
                  :color="getModelTypeColor(item.type)"
                  small
                >
                  {{ getModelTypeName(item.type) }}
                </v-chip>
              </template>
              <template v-slot:item.features="{ item }">
                <v-chip
                  v-if="item.features.includes('attention')"
                  color="purple"
                  small
                  class="ml-1"
                >
                  تحليل الانتباه
                </v-chip>
                <v-chip
                  v-if="item.features.includes('robustness')"
                  color="teal"
                  small
                  class="ml-1"
                >
                  اختبار المتانة
                </v-chip>
              </template>
              <template v-slot:item.actions="{ item }">
                <v-btn
                  small
                  icon
                  color="primary"
                  @click="viewModelDetails(item)"
                  :disabled="loading"
                >
                  <v-icon small>mdi-eye</v-icon>
                </v-btn>
                <v-btn
                  small
                  icon
                  color="error"
                  @click="confirmUninstallModel(item)"
                  :disabled="loading"
                >
                  <v-icon small>mdi-delete</v-icon>
                </v-btn>
                <v-btn
                  small
                  icon
                  color="success"
                  @click="testModel(item)"
                  :disabled="loading"
                >
                  <v-icon small>mdi-check-circle</v-icon>
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-card-text>
    </v-card>

    <!-- نافذة تفاصيل الحاوية -->
    <v-dialog
      v-model="containerDetailsDialog"
      max-width="800px"
    >
      <v-card>
        <v-card-title class="primary--text">
          <v-icon large color="primary" class="ml-2">mdi-docker</v-icon>
          تفاصيل الحاوية
        </v-card-title>
        <v-card-text v-if="selectedContainer">
          <v-row>
            <v-col cols="12" md="6">
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>معرف الحاوية</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedContainer.id }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>الاسم</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedContainer.name }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>الحالة</v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip
                      :color="getStatusColor(selectedContainer.status)"
                      small
                    >
                      {{ selectedContainer.status }}
                    </v-chip>
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-col>
            <v-col cols="12" md="6">
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>الصورة</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedContainer.image }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>المنافذ</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedContainer.ports }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>وقت التشغيل</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedContainer.uptime }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <h3 class="subtitle-1 mb-2">استخدام الموارد</h3>
          <v-row>
            <v-col cols="12" md="6">
              <v-card outlined>
                <v-card-title class="subtitle-2">استخدام CPU</v-card-title>
                <v-card-text>
                  <v-progress-linear
                    :value="selectedContainer.resources.cpu_percent"
                    color="blue"
                    height="25"
                  >
                    <template v-slot:default>
                      <strong>{{ selectedContainer.resources.cpu_percent }}%</strong>
                    </template>
                  </v-progress-linear>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" md="6">
              <v-card outlined>
                <v-card-title class="subtitle-2">استخدام الذاكرة</v-card-title>
                <v-card-text>
                  <v-progress-linear
                    :value="selectedContainer.resources.memory_percent"
                    color="green"
                    height="25"
                  >
                    <template v-slot:default>
                      <strong>{{ selectedContainer.resources.memory_percent }}% ({{ selectedContainer.resources.memory_usage }})</strong>
                    </template>
                  </v-progress-linear>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <h3 class="subtitle-1 mb-2">سجل الحاوية</h3>
          <v-card outlined>
            <v-card-text>
              <pre class="container-logs">{{ selectedContainer.logs }}</pre>
            </v-card-text>
          </v-card>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="containerDetailsDialog = false"
          >
            إغلاق
          </v-btn>
          <v-btn
            color="error"
            text
            @click="stopContainer(selectedContainer)"
            :disabled="!selectedContainer || selectedContainer.status !== 'running'"
          >
            <v-icon left>mdi-stop</v-icon>
            إيقاف
          </v-btn>
          <v-btn
            color="warning"
            text
            @click="restartContainer(selectedContainer)"
            :disabled="!selectedContainer || selectedContainer.status !== 'running'"
          >
            <v-icon left>mdi-restart</v-icon>
            إعادة تشغيل
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- نافذة تفاصيل النموذج -->
    <v-dialog
      v-model="modelDetailsDialog"
      max-width="800px"
    >
      <v-card>
        <v-card-title class="primary--text">
          <v-icon large color="primary" class="ml-2">mdi-brain</v-icon>
          تفاصيل النموذج
        </v-card-title>
        <v-card-text v-if="selectedModel">
          <v-row>
            <v-col cols="12" md="6">
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>اسم النموذج</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedModel.name }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>النوع</v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip
                      :color="getModelTypeColor(selectedModel.type)"
                      small
                    >
                      {{ getModelTypeName(selectedModel.type) }}
                    </v-chip>
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>المصدر</v-list-item-title>
                  <v-list-item-subtitle>{{ selectedModel.source }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-col>
            <v-col cols="12" md="6">
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>عدد المعلمات</v-list-item-title>
                  <v-list-item-subtitle>{{ formatParameters(selectedModel.parameters) }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>شكل المدخلات</v-list-item-title>
                  <v-list-item-subtitle>{{ formatShape(selectedModel.input_shape) }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>شكل المخرجات</v-list-item-title>
                  <v-list-item-subtitle>{{ formatShape(selectedModel.output_shape) }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <h3 class="subtitle-1 mb-2">الميزات المدعومة</h3>
          <v-row>
            <v-col cols="12">
              <v-chip
                v-if="selectedModel.features.includes('attention')"
                color="purple"
                class="ml-1 mb-2"
              >
                <v-icon left>mdi-eye-outline</v-icon>
                تحليل أنماط الانتباه
              </v-chip>
              <v-chip
                v-if="selectedModel.features.includes('robustness')"
                color="teal"
                class="ml-1 mb-2"
              >
                <v-icon left>mdi-shield-check</v-icon>
                اختبار المتانة
              </v-chip>
              <v-chip
                v-if="selectedModel.features.includes('ensemble')"
                color="blue"
                class="ml-1 mb-2"
              >
                <v-icon left>mdi-account-group</v-icon>
                دعم التجميع
              </v-chip>
              <v-chip
                v-if="selectedModel.features.includes('gpu')"
                color="deep-orange"
                class="ml-1 mb-2"
              >
                <v-icon left>mdi-gpu</v-icon>
                دعم GPU
              </v-chip>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <h3 class="subtitle-1 mb-2">الوصف</h3>
          <v-card outlined>
            <v-card-text>
              {{ selectedModel.description || 'لا يوجد وصف متاح' }}
            </v-card-text>
          </v-card>

          <v-divider class="my-4"></v-divider>

          <h3 class="subtitle-1 mb-2">الإعدادات</h3>
          <v-card outlined>
            <v-card-text>
              <pre>{{ formatConfig(selectedModel.config) }}</pre>
            </v-card-text>
          </v-card>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="modelDetailsDialog = false"
          >
            إغلاق
          </v-btn>
          <v-btn
            color="error"
            text
            @click="confirmUninstallModel(selectedModel)"
          >
            <v-icon left>mdi-delete</v-icon>
            إزالة
          </v-btn>
          <v-btn
            color="success"
            text
            @click="testModel(selectedModel)"
          >
            <v-icon left>mdi-check-circle</v-icon>
            اختبار
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- نافذة تأكيد إزالة النموذج -->
    <v-dialog
      v-model="confirmUninstallDialog"
      max-width="500px"
    >
      <v-card>
        <v-card-title class="error--text">
          <v-icon large color="error" class="ml-2">mdi-alert</v-icon>
          تأكيد إزالة النموذج
        </v-card-title>
        <v-card-text v-if="selectedModel">
          <p>هل أنت متأكد من رغبتك في إزالة النموذج "{{ selectedModel.name }}"؟</p>
          <p class="red--text">هذا الإجراء لا يمكن التراجع عنه.</p>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="confirmUninstallDialog = false"
          >
            إلغاء
          </v-btn>
          <v-btn
            color="error"
            text
            @click="uninstallModel"
            :loading="loading"
          >
            <v-icon left>mdi-delete</v-icon>
            تأكيد الإزالة
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- نافذة اختبار النموذج -->
    <v-dialog
      v-model="testModelDialog"
      max-width="800px"
    >
      <v-card>
        <v-card-title class="primary--text">
          <v-icon large color="primary" class="ml-2">mdi-check-circle</v-icon>
          اختبار النموذج
        </v-card-title>
        <v-card-text v-if="selectedModel">
          <v-alert
            v-if="testError"
            type="error"
            dense
            dismissible
            class="mb-4"
          >
            {{ testError }}
          </v-alert>

          <v-form ref="testForm" v-model="testFormValid">
            <v-row>
              <v-col cols="12">
                <v-file-input
                  v-model="testImage"
                  label="اختر صورة للاختبار"
                  accept="image/*"
                  :rules="[v => !!v || 'الصورة مطلوبة']"
                  :disabled="loading"
                  show-size
                  prepend-icon="mdi-camera"
                ></v-file-input>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="6">
                <v-checkbox
                  v-model="testOptions.runAttentionAnalysis"
                  label="تشغيل تحليل أنماط الانتباه"
                  :disabled="loading || !selectedModel.features.includes('attention')"
                ></v-checkbox>
              </v-col>
              <v-col cols="12" md="6">
                <v-checkbox
                  v-model="testOptions.runRobustnessTest"
                  label="تشغيل اختبار المتانة"
                  :disabled="loading || !selectedModel.features.includes('robustness')"
                ></v-checkbox>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <v-btn
                  color="primary"
                  :loading="loading"
                  :disabled="!testFormValid"
                  @click="runModelTest"
                  block
                >
                  <v-icon left>mdi-play</v-icon>
                  تشغيل الاختبار
                </v-btn>
              </v-col>
            </v-row>
          </v-form>

          <v-divider v-if="testResult" class="my-4"></v-divider>

          <!-- نتائج الاختبار -->
          <div v-if="testResult">
            <h3 class="subtitle-1 mb-2">نتائج الاختبار</h3>
            
            <v-row>
              <v-col cols="12" md="6">
                <v-card outlined>
                  <v-card-title class="subtitle-2">الصورة الأصلية</v-card-title>
                  <v-card-text class="text-center">
                    <v-img
                      :src="testResult.original_image"
                      max-height="300"
                      contain
                    ></v-img>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card outlined>
                  <v-card-title class="subtitle-2">نتيجة التنبؤ</v-card-title>
                  <v-card-text>
                    <v-list>
                      <v-list-item>
                        <v-list-item-content>
                          <v-list-item-title>التصنيف</v-list-item-title>
                          <v-list-item-subtitle>{{ testResult.prediction }}</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-content>
                          <v-list-item-title>الثقة</v-list-item-title>
                          <v-list-item-subtitle>{{ formatConfidence(testResult.confidence) }}</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-content>
                          <v-list-item-title>وقت المعالجة</v-list-item-title>
                          <v-list-item-subtitle>{{ formatProcessingTime(testResult.processing_time) }}</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>

            <!-- نتائج تحليل أنماط الانتباه -->
            <div v-if="testResult.attention_analysis">
              <h3 class="subtitle-1 my-4">نتائج تحليل أنماط الانتباه</h3>
              <v-row>
                <v-col cols="12" md="6">
                  <v-card outlined>
                    <v-card-title class="subtitle-2">خريطة الانتباه</v-card-title>
                    <v-card-text class="text-center">
                      <v-img
                        :src="testResult.attention_analysis.attention_map"
                        max-height="300"
                        contain
                      ></v-img>
                    </v-card-text>
                  </v-card>
                </v-col>
                <v-col cols="12" md="6">
                  <v-card outlined>
                    <v-card-title class="subtitle-2">إحصائيات الانتباه</v-card-title>
                    <v-card-text>
                      <v-simple-table>
                        <template v-slot:default>
                          <tbody>
                            <tr v-for="(value, key) in testResult.attention_analysis.statistics" :key="key">
                              <td>{{ formatAttentionStatName(key) }}</td>
                              <td>{{ formatAttentionStatValue(value) }}</td>
                            </tr>
                          </tbody>
                        </template>
                      </v-simple-table>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
            </div>

            <!-- نتائج اختبار المتانة -->
            <div v-if="testResult.robustness_test">
              <h3 class="subtitle-1 my-4">نتائج اختبار المتانة</h3>
              <v-row>
                <v-col cols="12">
                  <v-card outlined>
                    <v-card-title class="subtitle-2">مخطط المتانة</v-card-title>
                    <v-card-text class="text-center">
                      <v-img
                        :src="testResult.robustness_test.radar_chart"
                        max-height="300"
                        contain
                      ></v-img>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <v-card outlined>
                    <v-card-title class="subtitle-2">نتائج اختبارات المتانة</v-card-title>
                    <v-card-text>
                      <v-simple-table>
                        <template v-slot:default>
                          <thead>
                            <tr>
                              <th scope="col">نوع الاختبار</th>
                              <th scope="col">الدقة</th>
                              <th scope="col">التقييم</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="(value, key) in testResult.robustness_test.results" :key="key">
                              <td>{{ formatRobustnessTestName(key) }}</td>
                              <td>{{ formatAccuracy(value.accuracy) }}</td>
                              <td>
                                <v-rating
                                  :value="getRatingFromAccuracy(value.accuracy)"
                                  color="amber"
                                  dense
                                  half-increments
                                  readonly
                                  small
                                ></v-rating>
                              </td>
                            </tr>
                          </tbody>
                        </template>
                      </v-simple-table>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
            </div>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="testModelDialog = false"
          >
            إغلاق
          </v-btn>
          <v-btn
            v-if="testResult"
            color="success"
            text
            @click="saveTestReport"
            :loading="loading"
          >
            <v-icon left>mdi-content-save</v-icon>
            حفظ التقرير
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: 'ModelContainerManager',
  
  data() {
    return {
      loading: false,
      error: null,
      success: null,
      
      // الحاويات النشطة
      activeContainers: [],
      activeContainersHeaders: [
        { text: 'المعرف', value: 'id', width: '20%' },
        { text: 'الاسم', value: 'name', width: '20%' },
        { text: 'الصورة', value: 'image', width: '25%' },
        { text: 'الحالة', value: 'status', width: '15%' },
        { text: 'المنافذ', value: 'ports', width: '10%' },
        { text: 'الإجراءات', value: 'actions', sortable: false, width: '10%' }
      ],
      
      // النماذج المتاحة
      availableModels: [],
      availableModelsHeaders: [
        { text: 'الاسم', value: 'name', width: '25%' },
        { text: 'النوع', value: 'type', width: '15%' },
        { text: 'المصدر', value: 'source', width: '25%' },
        { text: 'الميزات', value: 'features', width: '25%' },
        { text: 'الإجراءات', value: 'actions', sortable: false, width: '10%' }
      ],
      
      // تثبيت نموذج جديد
      installFormValid: false,
      newModel: {
        name: '',
        type: '',
        source: '',
        gpu: 'auto',
        config: '',
        enableAttentionAnalysis: false,
        enableRobustnessTest: false
      },
      
      // أنواع النماذج
      modelTypes: [
        { text: 'PyTorch', value: 'pytorch' },
        { text: 'TensorFlow', value: 'tensorflow' },
        { text: 'ONNX', value: 'onnx' },
        { text: 'Hugging Face', value: 'huggingface' },
        { text: 'TensorFlow Hub', value: 'tfhub' },
        { text: 'Keras', value: 'keras' }
      ],
      
      // خيارات GPU
      gpuOptions: [
        { text: 'تلقائي (استخدام GPU إذا كان متاحاً)', value: 'auto' },
        { text: 'إجباري (استخدام GPU فقط)', value: 'required' },
        { text: 'تعطيل (استخدام CPU فقط)', value: 'disabled' }
      ],
      
      // نافذة تفاصيل الحاوية
      containerDetailsDialog: false,
      selectedContainer: null,
      
      // نافذة تفاصيل النموذج
      modelDetailsDialog: false,
      selectedModel: null,
      
      // نافذة تأكيد إزالة النموذج
      confirmUninstallDialog: false,
      
      // نافذة اختبار النموذج
      testModelDialog: false,
      testFormValid: false,
      testImage: null,
      testOptions: {
        runAttentionAnalysis: false,
        runRobustnessTest: false
      },
      testError: null,
      testResult: null
    };
  },
  
  mounted() {
    this.fetchActiveContainers();
    this.fetchAvailableModels();
  },
  
  methods: {
    async fetchActiveContainers() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await this.$store.dispatch('docker/fetchActiveContainers');
        
        if (response.error) {
          throw new Error(response.error);
        }
        
        this.activeContainers = response.containers;
        
      } catch (error) {
        this.error = `خطأ في جلب الحاويات النشطة: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },
    
    async fetchAvailableModels() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await this.$store.dispatch('plantDisease/fetchAvailableModels');
        
        if (response.error) {
          throw new Error(response.error);
        }
        
        this.availableModels = Object.values(response.models).map(model => ({
          ...model,
          features: this.getModelFeatures(model)
        }));
        
      } catch (error) {
        this.error = `خطأ في جلب النماذج المتاحة: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },
    
    getModelFeatures(model) {
      const features = [];
      
      // تحديد الميزات المدعومة بناءً على نوع النموذج وخصائصه
      if (model.type === 'pytorch' || model.type === 'tensorflow' || model.type === 'huggingface') {
        features.push('attention');
      }
      
      // جميع النماذج تدعم اختبار المتانة
      features.push('robustness');
      
      // النماذج التي تدعم التجميع
      if (model.type !== 'custom') {
        features.push('ensemble');
      }
      
      // النماذج التي تدعم GPU
      if (model.type === 'pytorch' || model.type === 'tensorflow' || model.type === 'onnx') {
        features.push('gpu');
      }
      
      return features;
    },
    
    getStatusColor(status) {
      switch (status) {
        case 'running':
          return 'success';
        case 'paused':
          return 'warning';
        case 'exited':
          return 'error';
        default:
          return 'grey';
      }
    },
    
    getModelTypeColor(type) {
      switch (type) {
        case 'pytorch':
          return 'orange';
        case 'tensorflow':
          return 'blue';
        case 'onnx':
          return 'purple';
        case 'huggingface':
          return 'green';
        case 'tfhub':
          return 'deep-orange';
        case 'keras':
          return 'red';
        default:
          return 'grey';
      }
    },
    
    getModelTypeName(type) {
      switch (type) {
        case 'pytorch':
          return 'PyTorch';
        case 'tensorflow':
          return 'TensorFlow';
        case 'onnx':
          return 'ONNX';
        case 'huggingface':
          return 'Hugging Face';
        case 'tfhub':
          return 'TensorFlow Hub';
        case 'keras':
          return 'Keras';
        default:
          return type;
      }
    },
    
    getSourceHint(type) {
      switch (type) {
        case 'pytorch':
          return 'مسار ملف .pt أو .pth أو رابط تحميل';
        case 'tensorflow':
          return 'مسار ملف .pb أو .savedmodel أو رابط تحميل';
        case 'onnx':
          return 'مسار ملف .onnx أو رابط تحميل';
        case 'huggingface':
          return 'اسم النموذج في Hugging Face (مثل: microsoft/resnet-50)';
        case 'tfhub':
          return 'رابط النموذج في TensorFlow Hub';
        case 'keras':
          return 'مسار ملف .h5 أو رابط تحميل';
        default:
          return 'مصدر النموذج';
      }
    },
    
    supportsAttentionAnalysis(type) {
      return ['pytorch', 'tensorflow', 'huggingface'].includes(type);
    },
    
    isValidJson(str) {
      if (!str) return true;
      
      try {
        JSON.parse(str);
        return true;
      } catch (e) {
        return false;
      }
    },
    
    formatParameters(params) {
      if (typeof params === 'number') {
        return params.toLocaleString();
      }
      return params || 'غير متاح';
    },
    
    formatShape(shape) {
      if (Array.isArray(shape)) {
        return shape.join(' × ');
      }
      return shape || 'غير متاح';
    },
    
    formatConfig(config) {
      if (!config) return 'لا توجد إعدادات';
      
      if (typeof config === 'string') {
        try {
          return JSON.stringify(JSON.parse(config), null, 2);
        } catch (error) {
          console.error('Error parsing config JSON:', error);
          return config;
        }
      }
      
      return JSON.stringify(config, null, 2);
    },
    
    formatConfidence(confidence) {
      if (typeof confidence === 'number') {
        return `${(confidence * 100).toFixed(2)}%`;
      }
      return confidence || 'غير متاح';
    },
    
    formatProcessingTime(time) {
      if (typeof time === 'number') {
        return `${time.toFixed(2)} مللي ثانية`;
      }
      return time || 'غير متاح';
    },
    
    formatAccuracy(accuracy) {
      if (typeof accuracy === 'number') {
        return `${(accuracy * 100).toFixed(2)}%`;
      }
      return accuracy || 'غير متاح';
    },
    
    formatAttentionStatName(key) {
      const nameMap = {
        focus_ratio: 'نسبة التركيز',
        attention_spread: 'انتشار الانتباه',
        attention_entropy: 'إنتروبيا الانتباه',
        max_activation: 'أقصى تنشيط'
      };
      
      return nameMap[key] || key;
    },
    
    formatAttentionStatValue(value) {
      if (value === undefined || value === null) {
        return 'غير متاح';
      }
      
      if (typeof value === 'number') {
        // تنسيق النسب المئوية
        if (value >= 0 && value <= 1 && ['focus_ratio'].includes(key)) {
          return `${(value * 100).toFixed(2)}%`;
        }
        
        // تنسيق القيم العشرية
        return value.toFixed(3);
      }
      
      return value.toString();
    },
    
    formatRobustnessTestName(key) {
      const nameMap = {
        noise: 'مقاومة الضوضاء',
        brightness: 'مقاومة تغييرات الإضاءة',
        contrast: 'مقاومة تغييرات التباين',
        rotation: 'مقاومة الدوران',
        blur: 'مقاومة الضبابية',
        scale: 'مقاومة تغيير الحجم',
        occlusion: 'مقاومة الحجب',
        compression: 'مقاومة الضغط',
        overall: 'المتانة الشاملة'
      };
      
      return nameMap[key] || key;
    },
    
    getRatingFromAccuracy(accuracy) {
      if (typeof accuracy !== 'number') return 0;
      
      // تحويل الدقة إلى تقييم من 5 نجوم
      return Math.min(5, Math.max(0, accuracy * 5));
    },
    
    async viewContainerDetails(container) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await this.$store.dispatch('docker/getContainerDetails', container.id);
        
        if (response.error) {
          throw new Error(response.error);
        }
        
        this.selectedContainer = response;
        this.containerDetailsDialog = true;
        
      } catch (error) {
        this.error = `خطأ في جلب تفاصيل الحاوية: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },
    
    async stopContainer(container) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await this.$store.dispatch('docker/stopContainer', container.id);
        
        if (response.error) {
          throw new Error(response.error);
        }
        
        this.success = `تم إيقاف الحاوية ${container.name} بنجاح`;
        this.containerDetailsDialog = false;
        
        // تحديث قائمة الحاويات النشطة
        await this.fetchActiveContainers();
        
      } catch (error) {
        this.error = `خطأ في إيقاف الحاوية: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },
    
    async restartContainer(container) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await this.$store.dispatch('docker/restartContainer', container.id);
        
        if (response.error) {
          throw new Error(response.error);
        }
        
        this.success = `تم إعادة تشغيل الحاوية ${container.name} بنجاح`;
        this.containerDetailsDialog = false;
        
        // تحديث قائمة الحاويات النشطة
        await this.fetchActiveContainers();
        
      } catch (error) {
        this.error = `خطأ في إعادة تشغيل الحاوية: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },
    
    async testContainer(container) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await this.$store.dispatch('docker/testContainer', container.id);
        
        if (response.error) {
          throw new Error(response.error);
        }
        
        this.success = `تم اختبار الحاوية ${container.name} بنجاح: ${response.message}`;
        
      } catch (error) {
        this.error = `خطأ في اختبار الحاوية: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },
    
    viewModelDetails(model) {
      this.selectedModel = model;
      this.modelDetailsDialog = true;
    },
    
    confirmUninstallModel(model) {
      this.selectedModel = model;
      this.confirmUninstallDialog = true;
      this.modelDetailsDialog = false;
    },
    
    async uninstallModel() {
      if (!this.selectedModel) return;
      
      this.loading = true;
      this.error = null;
      
      try {
        const response = await this.$store.dispatch('plantDisease/uninstallModel', this.selectedModel.name);
        
        if (response.error) {
          throw new Error(response.error);
        }
        
        this.success = `تم إزالة النموذج ${this.selectedModel.name} بنجاح`;
        this.confirmUninstallDialog = false;
        
        // تحديث قائمة النماذج المتاحة
        await this.fetchAvailableModels();
        
      } catch (error) {
        this.error = `خطأ في إزالة النموذج: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },
    
    async installModel() {
      if (!this.$refs.installForm.validate()) {
        return;
      }
      
      this.loading = true;
      this.error = null;
      
      try {
        // تحضير إعدادات النموذج
        const modelConfig = this.newModel.config ? JSON.parse(this.newModel.config) : {};
        
        // إضافة إعدادات تحليل الانتباه واختبار المتانة
        if (this.newModel.enableAttentionAnalysis) {
          modelConfig.attention_analysis = true;
        }
        
        if (this.newModel.enableRobustnessTest) {
          modelConfig.robustness_test = true;
        }
        
        // إضافة إعدادات GPU
        modelConfig.gpu = this.newModel.gpu;
        
        const modelInfo = {
          name: this.newModel.name,
          type: this.newModel.type,
          source: this.newModel.source,
          config: modelConfig
        };
        
        const response = await this.$store.dispatch('plantDisease/installExternalModel', modelInfo);
        
        if (response.error) {
          throw new Error(response.error);
        }
        
        this.success = `تم تثبيت النموذج ${this.newModel.name} بنجاح`;
        
        // إعادة تعيين نموذج جديد
        this.newModel = {
          name: '',
          type: '',
          source: '',
          gpu: 'auto',
          config: '',
          enableAttentionAnalysis: false,
          enableRobustnessTest: false
        };
        
        // تحديث قائمة النماذج المتاحة
        await this.fetchAvailableModels();
        
      } catch (error) {
        this.error = `خطأ في تثبيت النموذج: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },
    
    testModel(model) {
      this.selectedModel = model;
      this.testModelDialog = true;
      this.modelDetailsDialog = false;
      this.testImage = null;
      this.testResult = null;
      this.testError = null;
      
      // تعيين خيارات الاختبار بناءً على ميزات النموذج
      this.testOptions.runAttentionAnalysis = model.features.includes('attention');
      this.testOptions.runRobustnessTest = model.features.includes('robustness');
    },
    
    async runModelTest() {
      if (!this.$refs.testForm.validate()) {
        return;
      }
      
      this.loading = true;
      this.testError = null;
      
      try {
        // تحميل الصورة
        const formData = new FormData();
        formData.append('image', this.testImage);
        
        // إضافة خيارات الاختبار
        formData.append('model_name', this.selectedModel.name);
        formData.append('run_attention_analysis', this.testOptions.runAttentionAnalysis);
        formData.append('run_robustness_test', this.testOptions.runRobustnessTest);
        
        const response = await this.$store.dispatch('plantDisease/testModel', formData);
        
        if (response.error) {
          throw new Error(response.error);
        }
        
        this.testResult = response;
        
      } catch (error) {
        this.testError = `خطأ في اختبار النموذج: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },
    
    async saveTestReport() {
      if (!this.testResult) return;
      
      this.loading = true;
      this.testError = null;
      
      try {
        const response = await this.$store.dispatch('plantDisease/saveModelTestReport', {
          model_name: this.selectedModel.name,
          test_result: this.testResult
        });
        
        if (response.error) {
          throw new Error(response.error);
        }
        
        this.success = `تم حفظ تقرير الاختبار بنجاح: ${response.report_path}`;
        
      } catch (error) {
        this.testError = `خطأ في حفظ تقرير الاختبار: ${error.message}`;
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.container-logs {
  max-height: 300px;
  overflow-y: auto;
  background-color: #f5f5f5;
  padding: 8px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 12px;
  white-space: pre-wrap;
}
</style>
