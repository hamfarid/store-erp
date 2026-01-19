<template>
  <div class="hybridization-details-container">
    <h1 class="details-title">{{ experiment.name }}</h1>
    
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between">
            <span>{{ $t('hybridization.experimentDetails') }}</span>
            <div>
              <v-btn
                color="primary"
                text
                :to="{ name: 'hybridization-form', params: { experimentId: experiment.id } }"
              >
                <v-icon left>mdi-pencil</v-icon>
                {{ $t('common.edit') }}
              </v-btn>
              
              <v-btn
                color="error"
                text
                @click="confirmDelete"
              >
                <v-icon left>mdi-delete</v-icon>
                {{ $t('common.delete') }}
              </v-btn>
            </div>
          </v-card-title>
          
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-list dense>
                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon>mdi-tag</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ $t('hybridization.experimentType') }}</v-list-item-title>
                      <v-list-item-subtitle>
                        <v-chip
                          small
                          :color="getTypeColor(experiment.type)"
                          text-color="white"
                        >
                          {{ getTypeLabel(experiment.type) }}
                        </v-chip>
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                  
                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon>mdi-check-circle</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ $t('hybridization.status') }}</v-list-item-title>
                      <v-list-item-subtitle>
                        <v-chip
                          small
                          :color="getStatusColor(experiment.status)"
                          text-color="white"
                        >
                          {{ getStatusLabel(experiment.status) }}
                        </v-chip>
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                  
                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon>mdi-calendar-start</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ $t('hybridization.startDate') }}</v-list-item-title>
                      <v-list-item-subtitle>{{ formatDate(experiment.start_date) }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                  
                  <v-list-item v-if="experiment.estimated_end_date">
                    <v-list-item-icon>
                      <v-icon>mdi-calendar-end</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ $t('hybridization.estimatedEndDate') }}</v-list-item-title>
                      <v-list-item-subtitle>{{ formatDate(experiment.estimated_end_date) }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-list dense>
                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon>mdi-account</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ $t('hybridization.responsibleUser') }}</v-list-item-title>
                      <v-list-item-subtitle>{{ experiment.responsible_user_name }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                  
                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon>mdi-map-marker</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ $t('hybridization.location') }}</v-list-item-title>
                      <v-list-item-subtitle>{{ experiment.location_name }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                  
                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon>mdi-calendar-clock</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ $t('hybridization.duration') }}</v-list-item-title>
                      <v-list-item-subtitle>{{ calculateDuration }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                  
                  <v-list-item>
                    <v-list-item-icon>
                      <v-icon>mdi-update</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ $t('hybridization.lastUpdated') }}</v-list-item-title>
                      <v-list-item-subtitle>{{ formatDateTime(experiment.updated_at) }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-col>
            </v-row>
            
            <v-divider class="my-4"></v-divider>
            
            <v-row>
              <v-col cols="12">
                <h3>{{ $t('hybridization.description') }}</h3>
                <p class="mt-2">{{ experiment.description }}</p>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>{{ $t('hybridization.parentStrains') }}</v-card-title>
          <v-card-text>
            <v-simple-table v-if="experiment.parent_strains && experiment.parent_strains.length > 0">
              <template v-slot:default>
                <thead>
                  <tr>
                    <th>{{ $t('hybridization.strainName') }}</th>
                    <th>{{ $t('hybridization.species') }}</th>
                    <th>{{ $t('hybridization.role') }}</th>
                    <th>{{ $t('hybridization.characteristics') }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="strain in experiment.parent_strains" :key="strain.id">
                    <td>
                      <v-btn
                        text
                        color="primary"
                        :to="{ name: 'strain-details', params: { id: strain.id } }"
                      >
                        {{ strain.name }}
                      </v-btn>
                    </td>
                    <td>{{ strain.species }}</td>
                    <td>
                      <v-chip
                        x-small
                        :color="getRoleColor(strain.role)"
                        text-color="white"
                      >
                        {{ getRoleLabel(strain.role) }}
                      </v-chip>
                    </td>
                    <td>{{ strain.characteristics }}</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
            
            <v-alert
              v-else
              type="info"
              text
              class="mt-2"
            >
              {{ $t('hybridization.noParentStrains') }}
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-4">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>{{ $t('hybridization.experimentParameters') }}</v-card-title>
          <v-card-text>
            <v-simple-table>
              <template v-slot:default>
                <tbody>
                  <tr v-if="experiment.parameters.temperature">
                    <td>{{ $t('hybridization.temperature') }}</td>
                    <td>{{ experiment.parameters.temperature }}°C</td>
                  </tr>
                  <tr v-if="experiment.parameters.humidity">
                    <td>{{ $t('hybridization.humidity') }}</td>
                    <td>{{ experiment.parameters.humidity }}%</td>
                  </tr>
                  <tr v-if="experiment.parameters.light_hours">
                    <td>{{ $t('hybridization.lightHours') }}</td>
                    <td>{{ experiment.parameters.light_hours }} h/day</td>
                  </tr>
                  <tr v-if="experiment.parameters.watering_frequency">
                    <td>{{ $t('hybridization.wateringFrequency') }}</td>
                    <td>{{ experiment.parameters.watering_frequency }} times/week</td>
                  </tr>
                  <tr v-if="experiment.parameters.soil_composition">
                    <td>{{ $t('hybridization.soilComposition') }}</td>
                    <td>{{ experiment.parameters.soil_composition }}</td>
                  </tr>
                  <tr v-if="experiment.parameters.fertilizer">
                    <td>{{ $t('hybridization.fertilizer') }}</td>
                    <td>{{ experiment.parameters.fertilizer }}</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
            
            <div v-if="experiment.parameters.notes" class="mt-4">
              <h4>{{ $t('hybridization.parameterNotes') }}</h4>
              <p class="mt-2">{{ experiment.parameters.notes }}</p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>{{ $t('hybridization.expectedResults') }}</v-card-title>
          <v-card-text>
            <h4>{{ $t('hybridization.expectedResults') }}</h4>
            <p class="mt-2">{{ experiment.expected_results }}</p>
            
            <h4 class="mt-4">{{ $t('hybridization.successCriteria') }}</h4>
            <p class="mt-2">{{ experiment.success_criteria }}</p>
            
            <v-simple-table class="mt-4">
              <template v-slot:default>
                <tbody>
                  <tr v-if="experiment.expected_germination_rate">
                    <td>{{ $t('hybridization.expectedGerminationRate') }}</td>
                    <td>{{ experiment.expected_germination_rate }}%</td>
                  </tr>
                  <tr v-if="experiment.expected_yield">
                    <td>{{ $t('hybridization.expectedYield') }}</td>
                    <td>{{ experiment.expected_yield }}</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between">
            <span>{{ $t('hybridization.experimentProgress') }}</span>
            <v-btn
              color="primary"
              @click="showAddProgressDialog = true"
            >
              <v-icon left>mdi-plus</v-icon>
              {{ $t('hybridization.addProgressEntry') }}
            </v-btn>
          </v-card-title>
          
          <v-card-text>
            <v-timeline v-if="experiment.progress && experiment.progress.length > 0">
              <v-timeline-item
                v-for="(entry, index) in experiment.progress"
                :key="index"
                :color="getProgressColor(entry.type)"
                :icon="getProgressIcon(entry.type)"
                :small="true"
              >
                <template v-slot:opposite>
                  <span class="timeline-date">{{ formatDate(entry.date) }}</span>
                </template>
                
                <v-card outlined>
                  <v-card-title class="py-2">
                    <v-chip
                      small
                      :color="getProgressColor(entry.type)"
                      text-color="white"
                      class="mr-2"
                    >
                      {{ getProgressTypeLabel(entry.type) }}
                    </v-chip>
                    {{ entry.title }}
                  </v-card-title>
                  
                  <v-card-text>
                    <p>{{ entry.description }}</p>
                    
                    <div v-if="entry.measurements" class="mt-2">
                      <v-simple-table dense>
                        <template v-slot:default>
                          <tbody>
                            <tr v-for="(value, key) in entry.measurements" :key="key">
                              <td>{{ key }}</td>
                              <td>{{ value }}</td>
                            </tr>
                          </tbody>
                        </template>
                      </v-simple-table>
                    </div>
                    
                    <div v-if="entry.images && entry.images.length > 0" class="mt-2">
                      <v-row>
                        <v-col
                          v-for="(image, imgIndex) in entry.images"
                          :key="imgIndex"
                          cols="6"
                          sm="4"
                          md="3"
                        >
                          <v-img
                            :src="image.url"
                            :alt="image.caption || ''"
                            aspect-ratio="1"
                            class="grey lighten-2"
                            @click="openImageDialog(image)"
                          >
                            <template v-slot:placeholder>
                              <v-row
                                class="fill-height ma-0"
                                align="center"
                                justify="center"
                              >
                                <v-progress-circular
                                  indeterminate
                                  color="grey lighten-5"
                                ></v-progress-circular>
                              </v-row>
                            </template>
                          </v-img>
                        </v-col>
                      </v-row>
                    </div>
                    
                    <div class="d-flex justify-end mt-2">
                      <v-btn
                        x-small
                        text
                        color="primary"
                        @click="editProgressEntry(index)"
                      >
                        <v-icon small left>mdi-pencil</v-icon>
                        {{ $t('common.edit') }}
                      </v-btn>
                      
                      <v-btn
                        x-small
                        text
                        color="error"
                        @click="deleteProgressEntry(index)"
                      >
                        <v-icon small left>mdi-delete</v-icon>
                        {{ $t('common.delete') }}
                      </v-btn>
                    </div>
                  </v-card-text>
                </v-card>
              </v-timeline-item>
            </v-timeline>
            
            <v-alert
              v-else
              type="info"
              text
              class="mt-2"
            >
              {{ $t('hybridization.noProgressEntries') }}
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-4" v-if="experiment.notes">
      <v-col cols="12">
        <v-card>
          <v-card-title>{{ $t('hybridization.generalNotes') }}</v-card-title>
          <v-card-text>
            <p>{{ experiment.notes }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Add Progress Dialog -->
    <v-dialog v-model="showAddProgressDialog" max-width="700px">
      <v-card>
        <v-card-title>
          {{ editingProgressIndex === null ? $t('hybridization.addProgressEntry') : $t('hybridization.editProgressEntry') }}
        </v-card-title>
        
        <v-card-text>
          <v-form ref="progressForm" v-model="isProgressFormValid">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="progressEntry.title"
                  :label="$t('hybridization.entryTitle')"
                  :rules="[v => !!v || $t('validation.required')]"
                  required
                ></v-text-field>
              </v-col>
              
              <v-col cols="12" md="6">
                <v-select
                  v-model="progressEntry.type"
                  :items="progressTypes"
                  :label="$t('hybridization.entryType')"
                  item-text="text"
                  item-value="value"
                  :rules="[v => !!v || $t('validation.required')]"
                  required
                ></v-select>
              </v-col>
            </v-row>
            
            <v-row>
              <v-col cols="12">
                <v-menu
                  v-model="progressDateMenu"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  min-width="290px"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="formattedProgressDate"
                      :label="$t('hybridization.entryDate')"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                      :rules="[v => !!v || $t('validation.required')]"
                      required
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="progressEntry.date"
                    @input="progressDateMenu = false"
                  ></v-date-picker>
                </v-menu>
              </v-col>
            </v-row>
            
            <v-row>
              <v-col cols="12">
                <v-textarea
                  v-model="progressEntry.description"
                  :label="$t('hybridization.entryDescription')"
                  :rules="[v => !!v || $t('validation.required')]"
                  required
                  rows="3"
                ></v-textarea>
              </v-col>
            </v-row>
            
            <v-row>
              <v-col cols="12">
                <h4>{{ $t('hybridization.measurements') }}</h4>
                
                <v-row
                  v-for="(measurement, index) in measurements"
                  :key="index"
                  align="center"
                >
                  <v-col cols="5">
                    <v-text-field
                      v-model="measurement.key"
                      :label="$t('hybridization.measurementName')"
                      dense
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="5">
                    <v-text-field
                      v-model="measurement.value"
                      :label="$t('hybridization.measurementValue')"
                      dense
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="2">
                    <v-btn
                      icon
                      color="error"
                      @click="removeMeasurement(index)"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
                
                <v-btn
                  text
                  color="primary"
                  @click="addMeasurement"
                >
                  <v-icon left>mdi-plus</v-icon>
                  {{ $t('hybridization.addMeasurement') }}
                </v-btn>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="showAddProgressDialog = false">
            {{ $t('common.cancel') }}
          </v-btn>
          <v-btn
            color="primary"
            :disabled="!isProgressFormValid"
            @click="saveProgressEntry"
          >
            {{ $t('common.save') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Image Dialog -->
    <v-dialog v-model="showImageDialog" max-width="800px">
      <v-card>
        <v-card-title>
          {{ selectedImage.caption || $t('hybridization.image') }}
          <v-spacer></v-spacer>
          <v-btn icon @click="showImageDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        
        <v-card-text class="text-center">
          <v-img
            :src="selectedImage.url"
            :alt="selectedImage.caption || ''"
            max-height="600"
            contain
          ></v-img>
          
          <p v-if="selectedImage.description" class="mt-4">
            {{ selectedImage.description }}
          </p>
        </v-card-text>
      </v-card>
    </v-dialog>
    
    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="500px">
      <v-card>
        <v-card-title>{{ $t('common.confirmDelete') }}</v-card-title>
        <v-card-text>
          {{ $t('hybridization.deleteExperimentConfirmation', { name: experiment.name }) }}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="deleteDialog = false">{{ $t('common.cancel') }}</v-btn>
          <v-btn color="error" @click="deleteExperiment">{{ $t('common.delete') }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
/**
 * @component HybridizationDetails
 * @description A component for displaying detailed information about a plant hybridization experiment.
 * This component shows experiment details, parent strains, parameters, progress timeline, and allows
 * adding/editing progress entries.
 */
export default {
  name: 'HybridizationDetails',
  
  props: {
    /**
     * Experiment ID
     * @type {String|Number}
     */
    id: {
      type: [String, Number],
      required: true
    }
  },
  
  data() {
    return {
      /**
       * Loading state
       * @type {Boolean}
       */
      loading: false,
      
      /**
       * Experiment data
       * @type {Object}
       */
      experiment: {
        name: '',
        type: '',
        status: '',
        description: '',
        start_date: null,
        estimated_end_date: null,
        location_id: null,
        location_name: '',
        responsible_user_id: null,
        responsible_user_name: '',
        parent_strains: [],
        parameters: {},
        expected_results: '',
        success_criteria: '',
        expected_germination_rate: null,
        expected_yield: null,
        notes: '',
        progress: []
      },
      
      /**
       * Delete confirmation dialog state
       * @type {Boolean}
       */
      deleteDialog: false,
      
      /**
       * Add/edit progress dialog state
       * @type {Boolean}
       */
      showAddProgressDialog: false,
      
      /**
       * Progress date picker menu state
       * @type {Boolean}
       */
      progressDateMenu: false,
      
      /**
       * Progress form validation state
       * @type {Boolean}
       */
      isProgressFormValid: false,
      
      /**
       * Index of progress entry being edited, null for new entry
       * @type {Number|null}
       */
      editingProgressIndex: null,
      
      /**
       * Current progress entry being added/edited
       * @type {Object}
       */
      progressEntry: {
        title: '',
        type: '',
        date: new Date().toISOString().substr(0, 10),
        description: '',
        measurements: {}
      },
      
      /**
       * Measurements for current progress entry
       * @type {Array}
       */
      measurements: [],
      
      /**
       * Available progress entry types
       * @type {Array}
       */
      progressTypes: [
        { text: this.$t('hybridization.progressTypes.observation'), value: 'observation' },
        { text: this.$t('hybridization.progressTypes.milestone'), value: 'milestone' },
        { text: this.$t('hybridization.progressTypes.issue'), value: 'issue' },
        { text: this.$t('hybridization.progressTypes.result'), value: 'result' }
      ],
      
      /**
       * Image dialog state
       * @type {Boolean}
       */
      showImageDialog: false,
      
      /**
       * Selected image for dialog
       * @type {Object}
       */
      selectedImage: {
        url: '',
        caption: '',
        description: ''
      }
    }
  },
  
  computed: {
    /**
     * Calculate experiment duration
     * @returns {String}
     */
    calculateDuration() {
      if (!this.experiment.start_date) return '';
      
      const startDate = new Date(this.experiment.start_date);
      const endDate = this.experiment.estimated_end_date 
        ? new Date(this.experiment.estimated_end_date)
        : new Date();
      
      const diffTime = Math.abs(endDate - startDate);
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      
      return diffDays === 1 
        ? `${diffDays} ${this.$t('common.day')}` 
        : `${diffDays} ${this.$t('common.days')}`;
    },
    
    /**
     * Format progress entry date for display
     * @returns {String}
     */
    formattedProgressDate() {
      return this.formatDate(this.progressEntry.date);
    }
  },
  
  created() {
    this.loadExperiment();
  },
  
  methods: {
    /**
     * Load experiment data
     * @returns {Promise<void>}
     */
    async loadExperiment() {
      this.loading = true;
      
      try {
        const response = await this.$api.hybridization.getExperiment(this.id);
        this.experiment = response.data;
      } catch (error) {
        console.error('Error loading experiment:', error);
        
        this.$store.dispatch('notifications/showError', {
          message: this.$t('hybridization.errorLoadingExperiment')
        });
      } finally {
        this.loading = false;
      }
    },
    
    /**
     * Get color for experiment type
     * @param {String} type - Experiment type
     * @returns {String} - Color name
     */
    getTypeColor(type) {
      const colors = {
        cross_pollination: '#4CAF50', // green
        self_pollination: '#2196F3', // blue
        backcross: '#9C27B0', // purple
        mutation: '#FF9800', // orange
        tissue_culture: '#795548', // brown
        other: '#757575' // grey
      };
      
      return colors[type] || '#757575';
    },
    
    /**
     * Get label for experiment type
     * @param {String} type - Experiment type
     * @returns {String} - Translated label
     */
    getTypeLabel(type) {
      return this.$t(`hybridization.types.${type.replace('_', '')}`) || type;
    },
    
    /**
     * Get color for experiment status
     * @param {String} status - Experiment status
     * @returns {String} - Color name
     */
    getStatusColor(status) {
      const colors = {
        planned: '#2196F3', // blue
        in_progress: '#FF9800', // orange
        completed: '#4CAF50', // green
        failed: '#F44336', // red
        on_hold: '#9E9E9E' // grey
      };
      
      return colors[status] || '#757575';
    },
    
    /**
     * Get label for experiment status
     * @param {String} status - Experiment status
     * @returns {String} - Translated label
     */
    getStatusLabel(status) {
      return this.$t(`hybridization.status.${status.replace('_', '')}`) || status;
    },
    
    /**
     * Get color for parent strain role
     * @param {String} role - Parent strain role
     * @returns {String} - Color name
     */
    getRoleColor(role) {
      const colors = {
        male: '#2196F3', // blue
        female: '#E91E63', // pink
        both: '#9C27B0' // purple
      };
      
      return colors[role] || '#757575';
    },
    
    /**
     * Get label for parent strain role
     * @param {String} role - Parent strain role
     * @returns {String} - Translated label
     */
    getRoleLabel(role) {
      return this.$t(`hybridization.roles.${role}`) || role;
    },
    
    /**
     * Get color for progress entry type
     * @param {String} type - Progress entry type
     * @returns {String} - Color name
     */
    getProgressColor(type) {
      const colors = {
        observation: '#2196F3', // blue
        milestone: '#4CAF50', // green
        issue: '#F44336', // red
        result: '#9C27B0' // purple
      };
      
      return colors[type] || '#757575';
    },
    
    /**
     * Get icon for progress entry type
     * @param {String} type - Progress entry type
     * @returns {String} - Icon name
     */
    getProgressIcon(type) {
      const icons = {
        observation: 'mdi-eye',
        milestone: 'mdi-flag-checkered',
        issue: 'mdi-alert',
        result: 'mdi-chart-bar'
      };
      
      return icons[type] || 'mdi-circle';
    },
    
    /**
     * Get label for progress entry type
     * @param {String} type - Progress entry type
     * @returns {String} - Translated label
     */
    getProgressTypeLabel(type) {
      return this.$t(`hybridization.progressTypes.${type}`) || type;
    },
    
    /**
     * Format date for display
     * @param {String} dateString - ISO date string
     * @returns {String} - Formatted date
     */
    formatDate(dateString) {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      return date.toLocaleDateString(this.$i18n.locale);
    },
    
    /**
     * Format date and time for display
     * @param {String} dateTimeString - ISO date-time string
     * @returns {String} - Formatted date and time
     */
    formatDateTime(dateTimeString) {
      if (!dateTimeString) return '';
      
      const date = new Date(dateTimeString);
      return date.toLocaleString(this.$i18n.locale);
    },
    
    /**
     * Show delete confirmation dialog
     */
    confirmDelete() {
      this.deleteDialog = true;
    },
    
    /**
     * Delete the experiment
     * @returns {Promise<void>}
     */
    async deleteExperiment() {
      try {
        await this.$api.hybridization.deleteExperiment(this.id);
        
        this.$store.dispatch('notifications/showSuccess', {
          message: this.$t('hybridization.experimentDeleted')
        });
        
        this.$router.push({ name: 'hybridization-list' });
      } catch (error) {
        console.error('Error deleting experiment:', error);
        
        this.$store.dispatch('notifications/showError', {
          message: this.$t('hybridization.errorDeletingExperiment')
        });
      } finally {
        this.deleteDialog = false;
      }
    },
    
    /**
     * Add a new measurement field
     */
    addMeasurement() {
      this.measurements.push({ key: '', value: '' });
    },
    
    /**
     * Remove a measurement field
     * @param {Number} index - Index of measurement to remove
     */
    removeMeasurement(index) {
      this.measurements.splice(index, 1);
    },
    
    /**
     * Initialize progress entry form for adding a new entry
     */
    initNewProgressEntry() {
      this.editingProgressIndex = null;
      this.progressEntry = {
        title: '',
        type: 'observation',
        date: new Date().toISOString().substr(0, 10),
        description: '',
        measurements: {}
      };
      this.measurements = [];
    },
    
    /**
     * Edit an existing progress entry
     * @param {Number} index - Index of progress entry to edit
     */
    editProgressEntry(index) {
      const entry = this.experiment.progress[index];
      this.editingProgressIndex = index;
      
      this.progressEntry = {
        title: entry.title,
        type: entry.type,
        date: entry.date,
        description: entry.description,
        measurements: { ...entry.measurements }
      };
      
      // Convert measurements object to array for form
      this.measurements = Object.entries(entry.measurements || {}).map(([key, value]) => ({
        key,
        value
      }));
      
      this.showAddProgressDialog = true;
    },
    
    /**
     * Delete a progress entry
     * @param {Number} index - Index of progress entry to delete
     */
    async deleteProgressEntry(index) {
      try {
        // Create a copy of the progress array without the deleted entry
        const updatedProgress = [...this.experiment.progress];
        updatedProgress.splice(index, 1);
        
        await this.$api.hybridization.updateExperimentProgress(
          this.id,
          { progress: updatedProgress }
        );
        
        // Update local data
        this.experiment.progress = updatedProgress;
        
        this.$store.dispatch('notifications/showSuccess', {
          message: this.$t('hybridization.progressEntryDeleted')
        });
      } catch (error) {
        console.error('Error deleting progress entry:', error);
        
        this.$store.dispatch('notifications/showError', {
          message: this.$t('hybridization.errorDeletingProgressEntry')
        });
      }
    },
    
    /**
     * Save current progress entry
     * @returns {Promise<void>}
     */
    async saveProgressEntry() {
      if (!this.$refs.progressForm.validate()) return;
      
      // Convert measurements array to object
      const measurementsObj = {};
      this.measurements.forEach(item => {
        if (item.key && item.value) {
          measurementsObj[item.key] = item.value;
        }
      });
      
      this.progressEntry.measurements = measurementsObj;
      
      try {
        let updatedProgress;
        
        if (this.editingProgressIndex !== null) {
          // Update existing entry
          updatedProgress = [...this.experiment.progress];
          updatedProgress[this.editingProgressIndex] = this.progressEntry;
        } else {
          // Add new entry
          updatedProgress = [...(this.experiment.progress || []), this.progressEntry];
        }
        
        await this.$api.hybridization.updateExperimentProgress(
          this.id,
          { progress: updatedProgress }
        );
        
        // Update local data
        this.experiment.progress = updatedProgress;
        
        this.$store.dispatch('notifications/showSuccess', {
          message: this.editingProgressIndex !== null
            ? this.$t('hybridization.progressEntryUpdated')
            : this.$t('hybridization.progressEntryAdded')
        });
        
        this.showAddProgressDialog = false;
      } catch (error) {
        console.error('Error saving progress entry:', error);
        
        this.$store.dispatch('notifications/showError', {
          message: this.$t('hybridization.errorSavingProgressEntry')
        });
      }
    },
    
    /**
     * Open image dialog
     * @param {Object} image - Image to display
     */
    openImageDialog(image) {
      this.selectedImage = image;
      this.showImageDialog = true;
    }
  },
  
  watch: {
    /**
     * Reset progress form when dialog is opened
     * @param {Boolean} val - New dialog state
     */
    showAddProgressDialog(val) {
      if (val && this.editingProgressIndex === null) {
        this.initNewProgressEntry();
      }
    }
  }
}
</script>

<style scoped>
.hybridization-details-container {
  padding: 20px;
}

.details-title {
  margin-bottom: 24px;
  color: var(--v-primary-base);
  font-weight: 500;
}

.timeline-date {
  font-size: 0.875rem;
  color: rgba(0, 0, 0, 0.6);
}
</style>
