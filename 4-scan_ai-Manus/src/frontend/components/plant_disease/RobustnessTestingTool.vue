<!--
مكون اختبار متانة النماذج
يوفر هذا المكون واجهة تفاعلية لاختبار قوة ومتانة نماذج تشخيص أمراض النباتات
ويتيح للمستخدمين تحميل الصور واختيار النماذج وعرض نتائج الاختبار بشكل مرئي

المؤلف: فريق تطوير Gaara ERP
تاريخ الإنشاء: 30 مايو 2025
-->

<template>
  <div class="robustness-testing-tool">
    <v-card class="mb-4">
      <v-card-title class="primary--text">
        <v-icon large color="primary" class="ml-2">mdi-shield-check</v-icon>
        اختبار متانة النماذج
      </v-card-title>
      <v-card-subtitle>
        اختبار قوة ومتانة النماذج في مواجهة التحديات المختلفة مثل الضوضاء والإضاءة والدوران
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

        <!-- قسم اختيار النماذج والصور -->
        <v-row>
          <v-col cols="12" md="6">
            <v-select
              v-model="selectedModels"
              :items="availableModels"
              item-text="name"
              item-value="name"
              label="اختر النماذج للاختبار"
              multiple
              chips
              :disabled="loading"
              :rules="[v => v.length > 0 || 'يرجى اختيار نموذج واحد على الأقل']"
            >
              <template v-slot:selection="{ item, index }">
                <v-chip v-if="index < 3" small>
                  {{ item.name }}
                </v-chip>
                <span v-if="index === 3" class="grey--text caption">
                  (+{{ selectedModels.length - 3 }} أخرى)
                </span>
              </template>
            </v-select>
          </v-col>
          <v-col cols="12" md="6">
            <v-file-input
              v-model="selectedFiles"
              label="اختر صور للاختبار"
              multiple
              chips
              accept="image/*"
              :disabled="loading"
              :rules="[v => v.length > 0 || 'يرجى اختيار صورة واحدة على الأقل']"
              show-size
              counter
            ></v-file-input>
          </v-col>
        </v-row>

        <!-- أزرار التحكم -->
        <v-row class="mt-2">
          <v-col cols="12" md="6">
            <v-btn
              color="primary"
              :loading="loading"
              :disabled="!canTest"
              @click="testRobustness"
              block
            >
              <v-icon left>mdi-shield-check</v-icon>
              اختبار متانة النموذج
            </v-btn>
          </v-col>
          <v-col cols="12" md="6">
            <v-btn
              color="secondary"
              :loading="loading"
              :disabled="!canCompare"
              @click="compareRobustness"
              block
            >
              <v-icon left>mdi-compare</v-icon>
              مقارنة متانة النماذج
            </v-btn>
          </v-col>
        </v-row>

        <!-- شريط التقدم -->
        <v-progress-linear
          v-if="loading"
          indeterminate
          color="primary"
          class="mt-4"
        ></v-progress-linear>
      </v-card-text>
    </v-card>

    <!-- عرض نتائج الاختبار -->
    <v-card v-if="testResults.length > 0" class="mb-4">
      <v-card-title class="primary--text">
        <v-icon large color="primary" class="ml-2">mdi-chart-areaspline</v-icon>
        نتائج اختبار المتانة
      </v-card-title>
      <v-card-text>
        <v-tabs v-model="activeTab" background-color="transparent" grow>
          <v-tab v-for="(result, index) in testResults" :key="index">
            {{ result.model_name }}
          </v-tab>
          <v-tab v-if="comparisonResult">
            مقارنة النماذج
          </v-tab>

          <!-- محتوى التبويبات -->
          <v-tab-item v-for="(result, index) in testResults" :key="index">
            <v-card flat>
              <v-card-text>
                <h3 class="text-h5 mb-4">اختبار متانة النموذج: {{ result.model_name }}</h3>
                
                <!-- مخطط الرادار للمتانة الشاملة -->
                <v-row>
                  <v-col cols="12" md="6">
                    <v-card outlined>
                      <v-card-title class="subtitle-1">المتانة الشاملة</v-card-title>
                      <v-card-text>
                        <v-img
                          v-if="result.chart_paths && result.chart_paths.radar_chart"
                          :src="getImageUrl(result.chart_paths.radar_chart)"
                          max-height="300"
                          contain
                        ></v-img>
                        <div v-else class="text-center pa-4">
                          لا يوجد مخطط رادار متاح
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-card outlined>
                      <v-card-title class="subtitle-1">ملخص المتانة</v-card-title>
                      <v-card-text>
                        <v-simple-table>
                          <template v-slot:default>
                            <tbody>
                              <tr v-for="(value, key) in getOverallRobustness(result)" :key="key">
                                <td>{{ formatTestName(key) }}</td>
                                <td>{{ formatTestValue(value) }}</td>
                              </tr>
                            </tbody>
                          </template>
                        </v-simple-table>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>

                <!-- تفاصيل اختبارات المتانة -->
                <h4 class="text-h6 mt-6 mb-3">تفاصيل اختبارات المتانة</h4>
                
                <!-- اختبار مقاومة الضوضاء -->
                <v-expansion-panels class="mb-4">
                  <v-expansion-panel>
                    <v-expansion-panel-header>
                      <div class="d-flex align-center">
                        <v-icon class="ml-2">mdi-grain</v-icon>
                        مقاومة الضوضاء
                      </div>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <v-row>
                        <v-col cols="12" md="6">
                          <v-img
                            v-if="result.chart_paths && result.chart_paths.noise_chart"
                            :src="getImageUrl(result.chart_paths.noise_chart)"
                            max-height="300"
                            contain
                          ></v-img>
                          <div v-else class="text-center pa-4">
                            لا يوجد مخطط متاح
                          </div>
                        </v-col>
                        <v-col cols="12" md="6">
                          <v-simple-table>
                            <template v-slot:default>
                              <thead>
                                <tr>
                                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    {{ $t('robustness_testing.attack_type') }}
                                  </th>
                                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    {{ $t('robustness_testing.success_rate') }}
                                  </th>
                                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    {{ $t('robustness_testing.confidence') }}
                                  </th>
                                </tr>
                              </thead>
                              <tbody>
                                <tr v-for="(value, key) in getNoiseResults(result)" :key="key">
                                  <td>{{ formatNoiseLevel(key) }}</td>
                                  <td>{{ formatAccuracy(value.accuracy) }}</td>
                                  <td>{{ value.samples_tested }}</td>
                                </tr>
                              </tbody>
                            </template>
                          </v-simple-table>
                        </v-col>
                      </v-row>
                    </v-expansion-panel-content>
                  </v-expansion-panel>
                </v-expansion-panels>

                <!-- اختبار مقاومة الإضاءة -->
                <v-expansion-panels class="mb-4">
                  <v-expansion-panel>
                    <v-expansion-panel-header>
                      <div class="d-flex align-center">
                        <v-icon class="ml-2">mdi-brightness-6</v-icon>
                        مقاومة تغييرات الإضاءة
                      </div>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <v-row>
                        <v-col cols="12" md="6">
                          <v-img
                            v-if="result.chart_paths && result.chart_paths.brightness_chart"
                            :src="getImageUrl(result.chart_paths.brightness_chart)"
                            max-height="300"
                            contain
                          ></v-img>
                          <div v-else class="text-center pa-4">
                            لا يوجد مخطط متاح
                          </div>
                        </v-col>
                        <v-col cols="12" md="6">
                          <v-simple-table>
                            <template v-slot:default>
                              <thead>
                                <tr>
                                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    {{ $t('robustness_testing.attack_type') }}
                                  </th>
                                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    {{ $t('robustness_testing.success_rate') }}
                                  </th>
                                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    {{ $t('robustness_testing.confidence') }}
                                  </th>
                                </tr>
                              </thead>
                              <tbody>
                                <tr v-for="(value, key) in getBrightnessResults(result)" :key="key">
                                  <td>{{ formatBrightnessLevel(key) }}</td>
                                  <td>{{ formatAccuracy(value.accuracy) }}</td>
                                  <td>{{ value.samples_tested }}</td>
                                </tr>
                              </tbody>
                            </template>
                          </v-simple-table>
                        </v-col>
                      </v-row>
                    </v-expansion-panel-content>
                  </v-expansion-panel>
                </v-expansion-panels>

                <!-- اختبار مقاومة الدوران -->
                <v-expansion-panels class="mb-4">
                  <v-expansion-panel>
                    <v-expansion-panel-header>
                      <div class="d-flex align-center">
                        <v-icon class="ml-2">mdi-rotate-3d</v-icon>
                        مقاومة الدوران
                      </div>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <v-row>
                        <v-col cols="12" md="6">
                          <v-img
                            v-if="result.chart_paths && result.chart_paths.rotation_chart"
                            :src="getImageUrl(result.chart_paths.rotation_chart)"
                            max-height="300"
                            contain
                          ></v-img>
                          <div v-else class="text-center pa-4">
                            لا يوجد مخطط متاح
                          </div>
                        </v-col>
                        <v-col cols="12" md="6">
                          <v-simple-table>
                            <template v-slot:default>
                              <thead>
                                <tr>
                                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    {{ $t('robustness_testing.attack_type') }}
                                  </th>
                                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    {{ $t('robustness_testing.success_rate') }}
                                  </th>
                                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    {{ $t('robustness_testing.confidence') }}
                                  </th>
                                </tr>
                              </thead>
                              <tbody>
                                <tr v-for="(value, key) in getRotationResults(result)" :key="key">
                                  <td>{{ formatRotationAngle(key) }}</td>
                                  <td>{{ formatAccuracy(value.accuracy) }}</td>
                                  <td>{{ value.samples_tested }}</td>
                                </tr>
                              </tbody>
                            </template>
                          </v-simple-table>
                        </v-col>
                      </v-row>
                    </v-expansion-panel-content>
                  </v-expansion-panel>
                </v-expansion-panels>

                <!-- اختبارات أخرى (ضبابية، تغيير الحجم، الحجب) -->
                <v-expansion-panels>
                  <v-expansion-panel>
                    <v-expansion-panel-header>
                      <div class="d-flex align-center">
                        <v-icon class="ml-2">mdi-blur</v-icon>
                        اختبارات متانة أخرى
                      </div>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <v-tabs>
                        <v-tab>الضبابية</v-tab>
                        <v-tab>تغيير الحجم</v-tab>
                        <v-tab>الحجب</v-tab>
                        <v-tab>الضغط</v-tab>

                        <v-tab-item>
                          <v-card flat>
                            <v-card-text>
                              <v-row>
                                <v-col cols="12" md="6">
                                  <v-img
                                    v-if="result.chart_paths && result.chart_paths.blur_chart"
                                    :src="getImageUrl(result.chart_paths.blur_chart)"
                                    max-height="300"
                                    contain
                                  ></v-img>
                                </v-col>
                                <v-col cols="12" md="6">
                                  <v-simple-table>
                                    <template v-slot:default>
                                      <thead>
                                        <tr>
                                          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            {{ $t('robustness_testing.attack_type') }}
                                          </th>
                                          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            {{ $t('robustness_testing.success_rate') }}
                                          </th>
                                        </tr>
                                      </thead>
                                      <tbody>
                                        <tr v-for="(value, key) in getBlurResults(result)" :key="key">
                                          <td>{{ formatBlurLevel(key) }}</td>
                                          <td>{{ formatAccuracy(value.accuracy) }}</td>
                                        </tr>
                                      </tbody>
                                    </template>
                                  </v-simple-table>
                                </v-col>
                              </v-row>
                            </v-card-text>
                          </v-card>
                        </v-tab-item>

                        <v-tab-item>
                          <v-card flat>
                            <v-card-text>
                              <v-row>
                                <v-col cols="12" md="6">
                                  <v-img
                                    v-if="result.chart_paths && result.chart_paths.scale_chart"
                                    :src="getImageUrl(result.chart_paths.scale_chart)"
                                    max-height="300"
                                    contain
                                  ></v-img>
                                </v-col>
                                <v-col cols="12" md="6">
                                  <v-simple-table>
                                    <template v-slot:default>
                                      <thead>
                                        <tr>
                                          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            {{ $t('robustness_testing.attack_type') }}
                                          </th>
                                          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            {{ $t('robustness_testing.success_rate') }}
                                          </th>
                                        </tr>
                                      </thead>
                                      <tbody>
                                        <tr v-for="(value, key) in getScaleResults(result)" :key="key">
                                          <td>{{ formatScaleLevel(key) }}</td>
                                          <td>{{ formatAccuracy(value.accuracy) }}</td>
                                        </tr>
                                      </tbody>
                                    </template>
                                  </v-simple-table>
                                </v-col>
                              </v-row>
                            </v-card-text>
                          </v-card>
                        </v-tab-item>

                        <v-tab-item>
                          <v-card flat>
                            <v-card-text>
                              <v-row>
                                <v-col cols="12" md="6">
                                  <v-img
                                    v-if="result.chart_paths && result.chart_paths.occlusion_chart"
                                    :src="getImageUrl(result.chart_paths.occlusion_chart)"
                                    max-height="300"
                                    contain
                                  ></v-img>
                                </v-col>
                                <v-col cols="12" md="6">
                                  <v-simple-table>
                                    <template v-slot:default>
                                      <thead>
                                        <tr>
                                          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            {{ $t('robustness_testing.attack_type') }}
                                          </th>
                                          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            {{ $t('robustness_testing.success_rate') }}
                                          </th>
                                        </tr>
                                      </thead>
                                      <tbody>
                                        <tr v-for="(value, key) in getOcclusionResults(result)" :key="key">
                                          <td>{{ formatOcclusionLevel(key) }}</td>
                                          <td>{{ formatAccuracy(value.accuracy) }}</td>
                                        </tr>
                                      </tbody>
                                    </template>
                                  </v-simple-table>
                                </v-col>
                              </v-row>
                            </v-card-text>
                          </v-card>
                        </v-tab-item>

                        <v-tab-item>
                          <v-card flat>
                            <v-card-text>
                              <v-row>
                                <v-col cols="12" md="6">
                                  <v-img
                                    v-if="result.chart_paths && result.chart_paths.compression_chart"
                                    :src="getImageUrl(result.chart_paths.compression_chart)"
                                    max-height="300"
                                    contain
                                  ></v-img>
                                </v-col>
                                <v-col cols="12" md="6">
                                  <v-simple-table>
                                    <template v-slot:default>
                                      <thead>
                                        <tr>
                                          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            {{ $t('robustness_testing.attack_type') }}
                                          </th>
                                          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            {{ $t('robustness_testing.success_rate') }}
                                          </th>
                                        </tr>
                                      </thead>
                                      <tbody>
                                        <tr v-for="(value, key) in getCompressionResults(result)" :key="key">
                                          <td>{{ formatCompressionLevel(key) }}</td>
                                          <td>{{ formatAccuracy(value.accuracy) }}</td>
                                        </tr>
                                      </tbody>
                                    </template>
                                  </v-simple-table>
                                </v-col>
                              </v-row>
                            </v-card-text>
                          </v-card>
                        </v-tab-item>
                      </v-tabs>
                    </v-expansion-panel-content>
                  </v-expansion-panel>
                </v-expansion-panels>
              </v-card-text>
            </v-card>
          </v-tab-item>

          <!-- تبويب المقارنة -->
          <v-tab-item v-if="comparisonResult">
            <v-card flat>
              <v-card-text>
                <h3 class="text-h5 mb-4">مقارنة متانة النماذج</h3>
                
                <!-- مخطط المقارنة -->
                <v-row>
                  <v-col cols="12">
                    <v-card outlined>
                      <v-card-title class="subtitle-1">مخطط مقارنة المتانة</v-card-title>
                      <v-card-text>
                        <v-img
                          v-if="comparisonResult.comparison_chart_path"
                          :src="getImageUrl(comparisonResult.comparison_chart_path)"
                          max-height="500"
                          contain
                        ></v-img>
                        <div v-else class="text-center pa-4">
                          لا يوجد مخطط مقارنة متاح
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>

                <!-- جدول المقارنة -->
                <v-row class="mt-4">
                  <v-col cols="12">
                    <v-card outlined>
                      <v-card-title class="subtitle-1">جدول مقارنة المتانة</v-card-title>
                      <v-card-text>
                        <v-data-table
                          :headers="comparisonHeaders"
                          :items="comparisonItems"
                          :items-per-page="10"
                          class="elevation-1"
                        ></v-data-table>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>

                <!-- أفضل النماذج -->
                <v-row class="mt-4">
                  <v-col cols="12">
                    <v-card outlined>
                      <v-card-title class="subtitle-1">أفضل النماذج في كل اختبار</v-card-title>
                      <v-card-text>
                        <v-simple-table>
                          <template v-slot:default>
                            <thead>
                              <tr>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                  {{ $t('robustness_testing.test_name') }}
                                </th>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                  {{ $t('robustness_testing.model') }}
                                </th>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                  {{ $t('robustness_testing.success_rate') }}
                                </th>
                              </tr>
                            </thead>
                            <tbody>
                              <tr v-for="(value, key) in getBestModels()" :key="key">
                                <td>{{ formatTestName(key) }}</td>
                                <td>{{ value.model }}</td>
                                <td>{{ formatAccuracy(value.accuracy) }}</td>
                              </tr>
                            </tbody>
                          </template>
                        </v-simple-table>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs>
      </v-card-text>
    </v-card>

    <!-- عرض التقارير السابقة -->
    <v-card v-if="previousReports.length > 0">
      <v-card-title class="primary--text">
        <v-icon large color="primary" class="ml-2">mdi-history</v-icon>
        تقارير اختبار المتانة السابقة
      </v-card-title>
      <v-card-text>
        <v-data-table
          :headers="reportHeaders"
          :items="previousReports"
          :items-per-page="5"
          class="elevation-1"
        >
          <template v-slot:item.actions="{ item }">
            <v-btn
              small
              color="primary"
              text
              @click="viewReport(item)"
            >
              <v-icon small>mdi-eye</v-icon>
              عرض
            </v-btn>
            <v-btn
              small
              color="secondary"
              text
              @click="downloadReport(item)"
            >
              <v-icon small>mdi-download</v-icon>
              تحميل
            </v-btn>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'RobustnessTestingTool',
  
  data() {
    return {
      selectedModels: [],
      selectedFiles: [],
      loading: false,
      error: null,
      testResults: [],
      comparisonResult: null,
      activeTab: 0,
      previousReports: [],
      reportHeaders: [
        { text: 'النموذج', value: 'model_name' },
        { text: 'التاريخ', value: 'timestamp' },
        { text: 'النوع', value: 'type' },
        { text: 'الإجراءات', value: 'actions', sortable: false }
      ],
      comparisonHeaders: [
        { text: 'النموذج', value: 'model' },
        { text: 'متانة الضوضاء', value: 'noise_robustness' },
        { text: 'متانة الإضاءة', value: 'brightness_robustness' },
        { text: 'متانة الدوران', value: 'rotation_robustness' },
        { text: 'متانة شاملة', value: 'overall_robustness' }
      ]
    };
  },
  
  computed: {
    ...mapGetters({
      availableModels: 'plantDisease/getAvailableModels'
    }),
    
    canTest() {
      return this.selectedModels.length > 0 && this.selectedFiles && this.selectedFiles.length > 0;
    },
    
    canCompare() {
      return this.selectedModels.length > 1 && this.selectedFiles && this.selectedFiles.length > 0;
    },
    
    comparisonItems() {
      if (!this.comparisonResult || !this.comparisonResult.comparison_data) {
        return [];
      }
      
      const items = [];
      for (const [model, data] of Object.entries(this.comparisonResult.comparison_data)) {
        items.push({
          model,
          noise_robustness: this.formatAccuracy(data.noise_robustness || 0),
          brightness_robustness: this.formatAccuracy(data.brightness_robustness || 0),
          rotation_robustness: this.formatAccuracy(data.rotation_robustness || 0),
          overall_robustness: this.formatAccuracy(data.overall_robustness || 0)
        });
      }
      
      return items;
    }
  },
  
  mounted() {
    this.fetchAvailableModels();
    this.fetchPreviousReports();
  },
  
  methods: {
    async fetchAvailableModels() {
      try {
        await this.$store.dispatch('plantDisease/fetchAvailableModels');
      } catch (error) {
        this.error = `خطأ في جلب النماذج المتاحة: ${error.message}`;
      }
    },
    
    async fetchPreviousReports() {
      try {
        const response = await this.$store.dispatch('plantDisease/fetchRobustnessReports');
        this.previousReports = response.reports.map(report => ({
          ...report,
          type: report.model_name === 'مقارنة' ? 'مقارنة' : 'اختبار'
        }));
      } catch (error) {
        this.error = `خطأ في جلب التقارير السابقة: ${error.message}`;
      }
    },
    
    async testRobustness() {
      if (!this.canTest) return;
      
      this.loading = true;
      this.error = null;
      
      try {
        // تحميل الصور أولاً
        const uploadResult = await this.uploadImages();
        
        if (!uploadResult || !uploadResult.image_paths || uploadResult.image_paths.length === 0) {
          throw new Error('فشل في تحميل الصور');
        }
        
        // اختبار متانة كل نموذج
        this.testResults = [];
        
        for (const model of this.selectedModels) {
          const result = await this.$store.dispatch('plantDisease/testModelRobustness', {
            model_name: model,
            image_paths: uploadResult.image_paths
          });
          
          if (result.error) {
            throw new Error(`فشل في اختبار متانة النموذج ${model}: ${result.error}`);
          }
          
          this.testResults.push(result);
        }
        
        // تحديث التقارير السابقة
        await this.fetchPreviousReports();
        
        // تعيين التبويب النشط
        this.activeTab = 0;
        
      } catch (error) {
        this.error = `خطأ في اختبار متانة النموذج: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },
    
    async compareRobustness() {
      if (!this.canCompare) return;
      
      this.loading = true;
      this.error = null;
      
      try {
        // تحميل الصور أولاً
        const uploadResult = await this.uploadImages();
        
        if (!uploadResult || !uploadResult.image_paths || uploadResult.image_paths.length === 0) {
          throw new Error('فشل في تحميل الصور');
        }
        
        // مقارنة متانة النماذج
        const result = await this.$store.dispatch('plantDisease/compareModelsRobustness', {
          models: this.selectedModels,
          image_paths: uploadResult.image_paths
        });
        
        if (result.error) {
          throw new Error(`فشل في مقارنة متانة النماذج: ${result.error}`);
        }
        
        this.comparisonResult = result;
        
        // اختبار متانة كل نموذج
        await this.testRobustness();
        
        // تعيين التبويب النشط للمقارنة
        this.activeTab = this.testResults.length;
        
      } catch (error) {
        this.error = `خطأ في مقارنة متانة النماذج: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },
    
    async uploadImages() {
      if (!this.selectedFiles || this.selectedFiles.length === 0) {
        return null;
      }
      
      const formData = new FormData();
      this.selectedFiles.forEach((file, index) => {
        formData.append(`image_${index}`, file);
      });
      
      return await this.$store.dispatch('plantDisease/uploadTestImages', formData);
    },
    
    getOverallRobustness(result) {
      if (!result || !result.overall_robustness) {
        return {};
      }
      
      return result.overall_robustness;
    },
    
    getNoiseResults(result) {
      if (!result || !result.test_results || !result.test_results.noise) {
        return {};
      }
      
      return result.test_results.noise;
    },
    
    getBrightnessResults(result) {
      if (!result || !result.test_results || !result.test_results.brightness) {
        return {};
      }
      
      return result.test_results.brightness;
    },
    
    getRotationResults(result) {
      if (!result || !result.test_results || !result.test_results.rotation) {
        return {};
      }
      
      return result.test_results.rotation;
    },
    
    getBlurResults(result) {
      if (!result || !result.test_results || !result.test_results.blur) {
        return {};
      }
      
      return result.test_results.blur;
    },
    
    getScaleResults(result) {
      if (!result || !result.test_results || !result.test_results.scale) {
        return {};
      }
      
      return result.test_results.scale;
    },
    
    getOcclusionResults(result) {
      if (!result || !result.test_results || !result.test_results.occlusion) {
        return {};
      }
      
      return result.test_results.occlusion;
    },
    
    getCompressionResults(result) {
      if (!result || !result.test_results || !result.test_results.compression) {
        return {};
      }
      
      return result.test_results.compression;
    },
    
    getBestModels() {
      if (!this.comparisonResult || !this.comparisonResult.best_models) {
        return {};
      }
      
      return this.comparisonResult.best_models;
    },
    
    formatTestName(key) {
      const nameMap = {
        noise_robustness: 'مقاومة الضوضاء',
        brightness_robustness: 'مقاومة تغييرات الإضاءة',
        contrast_robustness: 'مقاومة تغييرات التباين',
        rotation_robustness: 'مقاومة الدوران',
        blur_robustness: 'مقاومة الضبابية',
        scale_robustness: 'مقاومة تغيير الحجم',
        occlusion_robustness: 'مقاومة الحجب',
        compression_robustness: 'مقاومة الضغط',
        overall_robustness: 'المتانة الشاملة'
      };
      
      return nameMap[key] || key;
    },
    
    formatTestValue(value) {
      if (value === undefined || value === null) {
        return 'غير متاح';
      }
      
      if (typeof value === 'number') {
        // تنسيق النسب المئوية
        if (value >= 0 && value <= 1) {
          return `${(value * 100).toFixed(2)}%`;
        }
        
        // تنسيق القيم العشرية
        return value.toFixed(3);
      }
      
      return value.toString();
    },
    
    formatNoiseLevel(key) {
      if (key === 'baseline') {
        return 'بدون ضوضاء';
      }
      
      const match = key.match(/noise_(\d+)/);
      if (match) {
        return `${match[1]}%`;
      }
      
      return key;
    },
    
    formatBrightnessLevel(key) {
      if (key === 'baseline') {
        return 'إضاءة عادية';
      }
      
      const match = key.match(/brightness_([+-]\d+)/);
      if (match) {
        const value = parseInt(match[1]);
        return value > 0 ? `+${value}%` : `${value}%`;
      }
      
      return key;
    },
    
    formatRotationAngle(key) {
      if (key === 'baseline') {
        return 'بدون دوران';
      }
      
      const match = key.match(/rotation_(\d+)/);
      if (match) {
        return `${match[1]}°`;
      }
      
      return key;
    },
    
    formatBlurLevel(key) {
      if (key === 'baseline') {
        return 'بدون ضبابية';
      }
      
      const match = key.match(/blur_(\d+)/);
      if (match) {
        return `مستوى ${match[1]}`;
      }
      
      return key;
    },
    
    formatScaleLevel(key) {
      if (key === 'baseline') {
        return 'الحجم الأصلي';
      }
      
      const match = key.match(/scale_(\d+)/);
      if (match) {
        const value = parseInt(match[1]);
        return `${value}%`;
      }
      
      return key;
    },
    
    formatOcclusionLevel(key) {
      if (key === 'baseline') {
        return 'بدون حجب';
      }
      
      const match = key.match(/occlusion_(\d+)percent/);
      if (match) {
        return `${match[1]}%`;
      }
      
      return key;
    },
    
    formatCompressionLevel(key) {
      if (key === 'baseline') {
        return 'بدون ضغط';
      }
      
      const match = key.match(/compression_(\d+)/);
      if (match) {
        return `جودة ${match[1]}%`;
      }
      
      return key;
    },
    
    formatAccuracy(value) {
      if (value === undefined || value === null) {
        return 'غير متاح';
      }
      
      return `${(value * 100).toFixed(2)}%`;
    },
    
    getImageUrl(path) {
      // تحويل المسار المحلي إلى URL للعرض
      if (!path) return '';
      
      if (path.startsWith('http')) {
        return path;
      }
      
      // استخراج اسم الملف من المسار
      const fileName = path.split('/').pop();
      
      // إنشاء URL للملف
      return `/api/files/reports/${fileName}`;
    },
    
    async viewReport(report) {
      try {
        // جلب تفاصيل التقرير
        const reportDetails = await this.$store.dispatch('plantDisease/getRobustnessReportDetails', report.path);
        
        if (report.model_name === 'مقارنة') {
          // عرض تقرير المقارنة
          this.comparisonResult = reportDetails;
          this.activeTab = this.testResults.length;
        } else {
          // عرض تقرير الاختبار
          this.testResults = [reportDetails];
          this.activeTab = 0;
        }
      } catch (error) {
        this.error = `خطأ في عرض التقرير: ${error.message}`;
      }
    },
    
    async downloadReport(report) {
      try {
        // تحميل ملف التقرير
        const response = await this.$axios.get(`/api/plant-disease/reports/robustness/${report.timestamp}`, {
          responseType: 'blob'
        });
        
        // إنشاء رابط تحميل
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `robustness_report_${report.model_name}_${report.timestamp}.json`);
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (error) {
        this.error = `خطأ في تحميل التقرير: ${error.message}`;
      }
    }
  }
};
</script>

<style scoped>
.v-expansion-panels {
  margin-bottom: 16px;
}
</style>
