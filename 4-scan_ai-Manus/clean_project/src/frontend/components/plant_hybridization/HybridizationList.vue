<template>
  <div class="hybridization-list-container">
    <h1 class="list-title">{{ $t('hybridization.experimentsList') }}</h1>
    
    <v-card>
      <v-card-title>
        <v-row align="center">
          <v-col cols="12" sm="6" md="4">
            <v-text-field
              v-model="search"
              :label="$t('common.search')"
              prepend-inner-icon="mdi-magnify"
              clearable
              hide-details
              outlined
              dense
            ></v-text-field>
          </v-col>
          
          <v-spacer></v-spacer>
          
          <v-col cols="12" sm="6" md="8" class="d-flex justify-end">
            <v-btn-toggle v-model="viewMode" mandatory>
              <v-btn small value="table">
                <v-icon>mdi-table</v-icon>
              </v-btn>
              <v-btn small value="grid">
                <v-icon>mdi-view-grid</v-icon>
              </v-btn>
            </v-btn-toggle>
            
            <v-btn
              color="primary"
              class="ml-2"
              :to="{ name: 'hybridization-form' }"
            >
              <v-icon left>mdi-plus</v-icon>
              {{ $t('hybridization.newExperiment') }}
            </v-btn>
          </v-col>
        </v-row>
      </v-card-title>
      
      <v-card-text>
        <v-row>
          <v-col cols="12" md="3">
            <v-card outlined>
              <v-card-title>{{ $t('common.filters') }}</v-card-title>
              <v-card-text>
                <v-select
                  v-model="filters.type"
                  :items="experimentTypes"
                  :label="$t('hybridization.experimentType')"
                  item-text="text"
                  item-value="value"
                  multiple
                  chips
                  small-chips
                  clearable
                ></v-select>
                
                <v-select
                  v-model="filters.status"
                  :items="experimentStatuses"
                  :label="$t('hybridization.status')"
                  item-text="text"
                  item-value="value"
                  multiple
                  chips
                  small-chips
                  clearable
                ></v-select>
                
                <v-select
                  v-model="filters.location"
                  :items="locations"
                  :label="$t('hybridization.location')"
                  item-text="name"
                  item-value="id"
                  multiple
                  chips
                  small-chips
                  clearable
                ></v-select>
                
                <v-select
                  v-model="filters.responsible"
                  :items="users"
                  :label="$t('hybridization.responsibleUser')"
                  item-text="name"
                  item-value="id"
                  multiple
                  chips
                  small-chips
                  clearable
                ></v-select>
                
                <v-menu
                  v-model="startDateMenu"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  min-width="290px"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="formattedStartDate"
                      :label="$t('hybridization.startDateFrom')"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                      clearable
                      @click:clear="filters.startDate = null"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="filters.startDate"
                    @input="startDateMenu = false"
                  ></v-date-picker>
                </v-menu>
                
                <v-menu
                  v-model="endDateMenu"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  min-width="290px"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="formattedEndDate"
                      :label="$t('hybridization.startDateTo')"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                      clearable
                      @click:clear="filters.endDate = null"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="filters.endDate"
                    @input="endDateMenu = false"
                    :min="filters.startDate"
                  ></v-date-picker>
                </v-menu>
                
                <v-btn
                  color="primary"
                  block
                  class="mt-4"
                  @click="applyFilters"
                >
                  {{ $t('common.applyFilters') }}
                </v-btn>
                
                <v-btn
                  text
                  block
                  class="mt-2"
                  @click="resetFilters"
                >
                  {{ $t('common.resetFilters') }}
                </v-btn>
              </v-card-text>
            </v-card>
          </v-col>
          
          <v-col cols="12" md="9">
            <!-- Table View -->
            <v-data-table
              v-if="viewMode === 'table'"
              :headers="headers"
              :items="experiments"
              :search="search"
              :loading="loading"
              :items-per-page="10"
              :footer-props="{
                'items-per-page-options': [10, 20, 50, 100],
              }"
              class="elevation-1"
            >
              <template v-slot:item.type="{ item }">
                <v-chip
                  small
                  :color="getTypeColor(item.type)"
                  text-color="white"
                >
                  {{ getTypeLabel(item.type) }}
                </v-chip>
              </template>
              
              <template v-slot:item.status="{ item }">
                <v-chip
                  small
                  :color="getStatusColor(item.status)"
                  text-color="white"
                >
                  {{ getStatusLabel(item.status) }}
                </v-chip>
              </template>
              
              <template v-slot:item.start_date="{ item }">
                {{ formatDate(item.start_date) }}
              </template>
              
              <template v-slot:item.estimated_end_date="{ item }">
                {{ formatDate(item.estimated_end_date) }}
              </template>
              
              <template v-slot:item.actions="{ item }">
                <v-btn
                  icon
                  small
                  :to="{ name: 'hybridization-details', params: { id: item.id } }"
                  title="View Details"
                >
                  <v-icon>mdi-eye</v-icon>
                </v-btn>
                
                <v-btn
                  icon
                  small
                  :to="{ name: 'hybridization-form', params: { experimentId: item.id } }"
                  title="Edit"
                >
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                
                <v-btn
                  icon
                  small
                  @click="confirmDelete(item)"
                  title="Delete"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
              
              <template v-slot:no-data>
                <v-alert
                  type="info"
                  text
                  class="ma-4"
                >
                  {{ $t('hybridization.noExperimentsFound') }}
                </v-alert>
              </template>
            </v-data-table>
            
            <!-- Grid View -->
            <div v-else>
              <v-row>
                <v-col
                  v-for="experiment in experiments"
                  :key="experiment.id"
                  cols="12"
                  sm="6"
                  md="4"
                >
                  <v-card
                    outlined
                    class="experiment-card"
                    :to="{ name: 'hybridization-details', params: { id: experiment.id } }"
                  >
                    <v-card-title class="experiment-card-title">
                      {{ experiment.name }}
                    </v-card-title>
                    
                    <v-card-subtitle>
                      <v-chip
                        x-small
                        :color="getTypeColor(experiment.type)"
                        text-color="white"
                        class="mr-1"
                      >
                        {{ getTypeLabel(experiment.type) }}
                      </v-chip>
                      
                      <v-chip
                        x-small
                        :color="getStatusColor(experiment.status)"
                        text-color="white"
                      >
                        {{ getStatusLabel(experiment.status) }}
                      </v-chip>
                    </v-card-subtitle>
                    
                    <v-card-text>
                      <div class="experiment-card-info">
                        <v-icon small class="mr-1">mdi-calendar</v-icon>
                        {{ formatDate(experiment.start_date) }}
                      </div>
                      
                      <div class="experiment-card-info">
                        <v-icon small class="mr-1">mdi-account</v-icon>
                        {{ experiment.responsible_user_name }}
                      </div>
                      
                      <div class="experiment-card-info">
                        <v-icon small class="mr-1">mdi-map-marker</v-icon>
                        {{ experiment.location_name }}
                      </div>
                      
                      <div class="experiment-card-description">
                        {{ experiment.description | truncate(100) }}
                      </div>
                    </v-card-text>
                    
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      
                      <v-btn
                        icon
                        small
                        :to="{ name: 'hybridization-form', params: { experimentId: experiment.id } }"
                        title="Edit"
                        @click.stop
                      >
                        <v-icon>mdi-pencil</v-icon>
                      </v-btn>
                      
                      <v-btn
                        icon
                        small
                        @click.stop="confirmDelete(experiment)"
                        title="Delete"
                      >
                        <v-icon>mdi-delete</v-icon>
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-col>
              </v-row>
              
              <v-alert
                v-if="experiments.length === 0 && !loading"
                type="info"
                text
                class="ma-4"
              >
                {{ $t('hybridization.noExperimentsFound') }}
              </v-alert>
            </div>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    
    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="500px">
      <v-card>
        <v-card-title>{{ $t('common.confirmDelete') }}</v-card-title>
        <v-card-text>
          {{ $t('hybridization.deleteExperimentConfirmation', { name: selectedExperiment ? selectedExperiment.name : '' }) }}
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
 * @component HybridizationList
 * @description A component for displaying and managing a list of plant hybridization experiments.
 * This component provides table and grid views, filtering, searching, and CRUD operations.
 */
export default {
  name: 'HybridizationList',
  
  filters: {
    /**
     * Truncate text to specified length
     * @param {String} text - Text to truncate
     * @param {Number} length - Maximum length
     * @returns {String} - Truncated text
     */
    truncate(text, length) {
      if (!text) return '';
      if (text.length <= length) return text;
      return text.substring(0, length) + '...';
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
       * Search query
       * @type {String}
       */
      search: '',
      
      /**
       * View mode (table or grid)
       * @type {String}
       */
      viewMode: 'table',
      
      /**
       * List of experiments
       * @type {Array}
       */
      experiments: [],
      
      /**
       * Filter values
       * @type {Object}
       */
      filters: {
        type: [],
        status: [],
        location: [],
        responsible: [],
        startDate: null,
        endDate: null
      },
      
      /**
       * Date picker menu states
       * @type {Boolean}
       */
      startDateMenu: false,
      endDateMenu: false,
      
      /**
       * Delete confirmation dialog state
       * @type {Boolean}
       */
      deleteDialog: false,
      
      /**
       * Selected experiment for deletion
       * @type {Object|null}
       */
      selectedExperiment: null,
      
      /**
       * Data table headers
       * @type {Array}
       */
      headers: [
        { text: this.$t('hybridization.experimentName'), value: 'name', sortable: true },
        { text: this.$t('hybridization.type'), value: 'type', sortable: true },
        { text: this.$t('hybridization.status'), value: 'status', sortable: true },
        { text: this.$t('hybridization.startDate'), value: 'start_date', sortable: true },
        { text: this.$t('hybridization.estimatedEndDate'), value: 'estimated_end_date', sortable: true },
        { text: this.$t('hybridization.responsibleUser'), value: 'responsible_user_name', sortable: true },
        { text: this.$t('hybridization.location'), value: 'location_name', sortable: true },
        { text: this.$t('common.actions'), value: 'actions', sortable: false, align: 'center' }
      ],
      
      /**
       * Available experiment types
       * @type {Array}
       */
      experimentTypes: [
        { text: this.$t('hybridization.types.crosspollination'), value: 'cross_pollination' },
        { text: this.$t('hybridization.types.selfpollination'), value: 'self_pollination' },
        { text: this.$t('hybridization.types.backcross'), value: 'backcross' },
        { text: this.$t('hybridization.types.mutation'), value: 'mutation' },
        { text: this.$t('hybridization.types.tissueculture'), value: 'tissue_culture' },
        { text: this.$t('hybridization.types.other'), value: 'other' }
      ],
      
      /**
       * Available experiment statuses
       * @type {Array}
       */
      experimentStatuses: [
        { text: this.$t('hybridization.status.planned'), value: 'planned' },
        { text: this.$t('hybridization.status.inprogress'), value: 'in_progress' },
        { text: this.$t('hybridization.status.completed'), value: 'completed' },
        { text: this.$t('hybridization.status.failed'), value: 'failed' },
        { text: this.$t('hybridization.status.onhold'), value: 'on_hold' }
      ],
      
      /**
       * Available locations
       * @type {Array}
       */
      locations: [],
      
      /**
       * Available users
       * @type {Array}
       */
      users: []
    }
  },
  
  computed: {
    /**
     * Formats the start date filter for display
     * @returns {String}
     */
    formattedStartDate() {
      return this.formatDate(this.filters.startDate);
    },
    
    /**
     * Formats the end date filter for display
     * @returns {String}
     */
    formattedEndDate() {
      return this.formatDate(this.filters.endDate);
    }
  },
  
  created() {
    this.loadReferenceData();
    this.loadExperiments();
  },
  
  methods: {
    /**
     * Load reference data for filters
     * @returns {Promise<void>}
     */
    async loadReferenceData() {
      try {
        const [locationsResponse, usersResponse] = await Promise.all([
          this.$api.locations.getAll(),
          this.$api.users.getAll()
        ]);
        
        this.locations = locationsResponse.data;
        this.users = usersResponse.data;
      } catch (error) {
        console.error('Error loading reference data:', error);
      }
    },
    
    /**
     * Load experiments with current filters
     * @returns {Promise<void>}
     */
    async loadExperiments() {
      this.loading = true;
      
      try {
        const response = await this.$api.hybridization.getExperiments({
          type: this.filters.type,
          status: this.filters.status,
          location_id: this.filters.location,
          responsible_user_id: this.filters.responsible,
          start_date_from: this.filters.startDate,
          start_date_to: this.filters.endDate
        });
        
        this.experiments = response.data;
      } catch (error) {
        console.error('Error loading experiments:', error);
        
        this.$store.dispatch('notifications/showError', {
          message: this.$t('hybridization.errorLoadingExperiments')
        });
      } finally {
        this.loading = false;
      }
    },
    
    /**
     * Apply current filters and reload experiments
     */
    applyFilters() {
      this.loadExperiments();
    },
    
    /**
     * Reset all filters to default values
     */
    resetFilters() {
      this.filters = {
        type: [],
        status: [],
        location: [],
        responsible: [],
        startDate: null,
        endDate: null
      };
      
      this.loadExperiments();
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
     * Show delete confirmation dialog
     * @param {Object} experiment - Experiment to delete
     */
    confirmDelete(experiment) {
      this.selectedExperiment = experiment;
      this.deleteDialog = true;
    },
    
    /**
     * Delete the selected experiment
     * @returns {Promise<void>}
     */
    async deleteExperiment() {
      if (!this.selectedExperiment) return;
      
      try {
        await this.$api.hybridization.deleteExperiment(this.selectedExperiment.id);
        
        this.$store.dispatch('notifications/showSuccess', {
          message: this.$t('hybridization.experimentDeleted')
        });
        
        // Remove from local list
        this.experiments = this.experiments.filter(
          exp => exp.id !== this.selectedExperiment.id
        );
      } catch (error) {
        console.error('Error deleting experiment:', error);
        
        this.$store.dispatch('notifications/showError', {
          message: this.$t('hybridization.errorDeletingExperiment')
        });
      } finally {
        this.deleteDialog = false;
        this.selectedExperiment = null;
      }
    }
  }
}
</script>

<style scoped>
.hybridization-list-container {
  padding: 20px;
}

.list-title {
  margin-bottom: 24px;
  color: var(--v-primary-base);
  font-weight: 500;
}

.experiment-card {
  height: 100%;
  transition: transform 0.2s;
}

.experiment-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.experiment-card-title {
  line-height: 1.2;
  max-height: 2.4em;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.experiment-card-info {
  display: flex;
  align-items: center;
  margin-bottom: 4px;
  font-size: 0.875rem;
  color: rgba(0, 0, 0, 0.6);
}

.experiment-card-description {
  margin-top: 8px;
  font-size: 0.875rem;
  color: rgba(0, 0, 0, 0.87);
  max-height: 3.6em;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}
</style>
