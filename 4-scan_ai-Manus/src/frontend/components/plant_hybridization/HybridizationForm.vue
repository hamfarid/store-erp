<template>
  <div class="hybridization-form-container">
    <h1 class="form-title">{{ isEditMode ? $t('hybridization.editExperiment') : $t('hybridization.newExperiment') }}</h1>
    
    <v-form ref="form" v-model="isFormValid" lazy-validation @submit.prevent="saveExperiment">
      <v-card>
        <v-card-text>
          <v-stepper v-model="currentStep" vertical>
            <!-- Step 1: Basic Information -->
            <v-stepper-step :complete="currentStep > 1" step="1">
              {{ $t('hybridization.basicInformation') }}
              <small>{{ $t('hybridization.experimentDetailsAndType') }}</small>
            </v-stepper-step>
            
            <v-stepper-content step="1">
              <v-card flat>
                <v-card-text>
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="experiment.name"
                        :label="$t('hybridization.experimentName')"
                        :rules="[v => !!v || $t('validation.required')]"
                        required
                      ></v-text-field>
                    </v-col>
                    
                    <v-col cols="12" md="6">
                      <v-select
                        v-model="experiment.type"
                        :items="experimentTypes"
                        :label="$t('hybridization.experimentType')"
                        item-text="text"
                        item-value="value"
                        :rules="[v => !!v || $t('validation.required')]"
                        required
                      ></v-select>
                    </v-col>
                  </v-row>
                  
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-menu
                        v-model="startDateMenu"
                        :close-on-content-click="false"
                        transition="scale-transition"
                        min-width="290px"
                      >
                        <template v-slot:activator="{ on, attrs }">
                          <v-text-field
                            v-model="formattedStartDate"
                            :label="$t('hybridization.startDate')"
                            readonly
                            v-bind="attrs"
                            v-on="on"
                            :rules="[v => !!v || $t('validation.required')]"
                            required
                          ></v-text-field>
                        </template>
                        <v-date-picker
                          v-model="experiment.start_date"
                          @input="startDateMenu = false"
                        ></v-date-picker>
                      </v-menu>
                    </v-col>
                    
                    <v-col cols="12" md="6">
                      <v-menu
                        v-model="estimatedEndDateMenu"
                        :close-on-content-click="false"
                        transition="scale-transition"
                        min-width="290px"
                      >
                        <template v-slot:activator="{ on, attrs }">
                          <v-text-field
                            v-model="formattedEstimatedEndDate"
                            :label="$t('hybridization.estimatedEndDate')"
                            readonly
                            v-bind="attrs"
                            v-on="on"
                          ></v-text-field>
                        </template>
                        <v-date-picker
                          v-model="experiment.estimated_end_date"
                          @input="estimatedEndDateMenu = false"
                          :min="experiment.start_date"
                        ></v-date-picker>
                      </v-menu>
                    </v-col>
                  </v-row>
                  
                  <v-row>
                    <v-col cols="12">
                      <v-textarea
                        v-model="experiment.description"
                        :label="$t('hybridization.description')"
                        :rules="[v => !!v || $t('validation.required')]"
                        required
                        rows="3"
                      ></v-textarea>
                    </v-col>
                  </v-row>
                  
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-select
                        v-model="experiment.location_id"
                        :items="locations"
                        :label="$t('hybridization.location')"
                        item-text="name"
                        item-value="id"
                        :rules="[v => !!v || $t('validation.required')]"
                        required
                      ></v-select>
                    </v-col>
                    
                    <v-col cols="12" md="6">
                      <v-select
                        v-model="experiment.responsible_user_id"
                        :items="users"
                        :label="$t('hybridization.responsibleUser')"
                        item-text="name"
                        item-value="id"
                        :rules="[v => !!v || $t('validation.required')]"
                        required
                      ></v-select>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
              
              <v-btn color="primary" @click="currentStep = 2">
                {{ $t('common.continue') }}
              </v-btn>
              
              <v-btn text @click="cancelForm">
                {{ $t('common.cancel') }}
              </v-btn>
            </v-stepper-content>
            
            <!-- Step 2: Parent Strains -->
            <v-stepper-step :complete="currentStep > 2" step="2">
              {{ $t('hybridization.parentStrains') }}
              <small>{{ $t('hybridization.selectParentStrains') }}</small>
            </v-stepper-step>
            
            <v-stepper-content step="2">
              <v-card flat>
                <v-card-text>
                  <v-row>
                    <v-col cols="12">
                      <v-alert
                        v-if="experiment.type === 'self_pollination' && experiment.parent_strains.length > 1"
                        type="warning"
                        text
                      >
                        {{ $t('hybridization.selfPollinationWarning') }}
                      </v-alert>
                      
                      <v-alert
                        v-if="experiment.type === 'cross_pollination' && experiment.parent_strains.length < 2"
                        type="info"
                        text
                      >
                        {{ $t('hybridization.crossPollinationInfo') }}
                      </v-alert>
                    </v-col>
                  </v-row>
                  
                  <v-row>
                    <v-col cols="12">
                      <v-autocomplete
                        v-model="selectedStrain"
                        :items="availableStrains"
                        :label="$t('hybridization.searchStrains')"
                        item-text="name"
                        item-value="id"
                        return-object
                        clearable
                      >
                        <template v-slot:item="{ item }">
                          <v-list-item-avatar>
                            <v-avatar color="green" size="32">
                              <span class="white--text">{{ item.name.charAt(0) }}</span>
                            </v-avatar>
                          </v-list-item-avatar>
                          <v-list-item-content>
                            <v-list-item-title>{{ item.name }}</v-list-item-title>
                            <v-list-item-subtitle>{{ item.species }}</v-list-item-subtitle>
                          </v-list-item-content>
                        </template>
                      </v-autocomplete>
                    </v-col>
                  </v-row>
                  
                  <v-row>
                    <v-col cols="12" class="text-center">
                      <v-btn
                        color="success"
                        @click="addParentStrain"
                        :disabled="!selectedStrain"
                      >
                        <v-icon left>mdi-plus</v-icon>
                        {{ $t('hybridization.addParentStrain') }}
                      </v-btn>
                    </v-col>
                  </v-row>
                  
                  <v-row v-if="experiment.parent_strains.length > 0">
                    <v-col cols="12">
                      <h3>{{ $t('hybridization.selectedParentStrains') }}</h3>
                      <v-simple-table>
                        <template v-slot:default>
                          <thead>
                            <tr>
                              <th>{{ $t('hybridization.strainName') }}</th>
                              <th>{{ $t('hybridization.species') }}</th>
                              <th>{{ $t('hybridization.role') }}</th>
                              <th>{{ $t('common.actions') }}</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="(strain, index) in experiment.parent_strains" :key="strain.id">
                              <td>{{ strain.name }}</td>
                              <td>{{ strain.species }}</td>
                              <td>
                                <v-select
                                  v-model="strain.role"
                                  :items="parentRoles"
                                  dense
                                  :disabled="experiment.type === 'self_pollination'"
                                ></v-select>
                              </td>
                              <td>
                                <v-btn
                                  icon
                                  small
                                  color="error"
                                  @click="removeParentStrain(index)"
                                >
                                  <v-icon>mdi-delete</v-icon>
                                </v-btn>
                              </td>
                            </tr>
                          </tbody>
                        </template>
                      </v-simple-table>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
              
              <v-btn color="primary" @click="currentStep = 3" :disabled="!isParentStrainsValid">
                {{ $t('common.continue') }}
              </v-btn>
              
              <v-btn text @click="currentStep = 1">
                {{ $t('common.back') }}
              </v-btn>
            </v-stepper-content>
            
            <!-- Step 3: Experiment Parameters -->
            <v-stepper-step :complete="currentStep > 3" step="3">
              {{ $t('hybridization.experimentParameters') }}
              <small>{{ $t('hybridization.defineParameters') }}</small>
            </v-stepper-step>
            
            <v-stepper-content step="3">
              <v-card flat>
                <v-card-text>
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model.number="experiment.parameters.temperature"
                        :label="$t('hybridization.temperature')"
                        type="number"
                        suffix="°C"
                      ></v-text-field>
                    </v-col>
                    
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model.number="experiment.parameters.humidity"
                        :label="$t('hybridization.humidity')"
                        type="number"
                        suffix="%"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model.number="experiment.parameters.light_hours"
                        :label="$t('hybridization.lightHours')"
                        type="number"
                        suffix="h/day"
                      ></v-text-field>
                    </v-col>
                    
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model.number="experiment.parameters.watering_frequency"
                        :label="$t('hybridization.wateringFrequency')"
                        type="number"
                        suffix="times/week"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  
                  <v-row>
                    <v-col cols="12">
                      <v-textarea
                        v-model="experiment.parameters.soil_composition"
                        :label="$t('hybridization.soilComposition')"
                        rows="2"
                      ></v-textarea>
                    </v-col>
                  </v-row>
                  
                  <v-row>
                    <v-col cols="12">
                      <v-textarea
                        v-model="experiment.parameters.fertilizer"
                        :label="$t('hybridization.fertilizer')"
                        rows="2"
                      ></v-textarea>
                    </v-col>
                  </v-row>
                  
                  <v-row>
                    <v-col cols="12">
                      <v-textarea
                        v-model="experiment.parameters.notes"
                        :label="$t('hybridization.parameterNotes')"
                        rows="3"
                      ></v-textarea>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
              
              <v-btn color="primary" @click="currentStep = 4">
                {{ $t('common.continue') }}
              </v-btn>
              
              <v-btn text @click="currentStep = 2">
                {{ $t('common.back') }}
              </v-btn>
            </v-stepper-content>
            
            <!-- Step 4: Expected Results and Goals -->
            <v-stepper-step step="4">
              {{ $t('hybridization.expectedResults') }}
              <small>{{ $t('hybridization.defineGoals') }}</small>
            </v-stepper-step>
            
            <v-stepper-content step="4">
              <v-card flat>
                <v-card-text>
                  <v-row>
                    <v-col cols="12">
                      <v-textarea
                        v-model="experiment.expected_results"
                        :label="$t('hybridization.expectedResults')"
                        :rules="[v => !!v || $t('validation.required')]"
                        required
                        rows="3"
                      ></v-textarea>
                    </v-col>
                  </v-row>
                  
                  <v-row>
                    <v-col cols="12">
                      <v-textarea
                        v-model="experiment.success_criteria"
                        :label="$t('hybridization.successCriteria')"
                        :rules="[v => !!v || $t('validation.required')]"
                        required
                        rows="3"
                      ></v-textarea>
                    </v-col>
                  </v-row>
                  
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model.number="experiment.expected_germination_rate"
                        :label="$t('hybridization.expectedGerminationRate')"
                        type="number"
                        suffix="%"
                      ></v-text-field>
                    </v-col>
                    
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model.number="experiment.expected_yield"
                        :label="$t('hybridization.expectedYield')"
                        type="number"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  
                  <v-row>
                    <v-col cols="12">
                      <v-textarea
                        v-model="experiment.notes"
                        :label="$t('hybridization.generalNotes')"
                        rows="3"
                      ></v-textarea>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
              
              <v-btn
                color="success"
                :loading="saving"
                :disabled="!isFormValid"
                type="submit"
                @click="saveExperiment"
              >
                {{ $t('common.save') }}
              </v-btn>
              
              <v-btn text @click="currentStep = 3">
                {{ $t('common.back') }}
              </v-btn>
            </v-stepper-content>
          </v-stepper>
        </v-card-text>
      </v-card>
    </v-form>
  </div>
</template>

<script>
/**
 * @component HybridizationForm
 * @description A form component for creating and editing plant hybridization experiments.
 * This component provides a multi-step form for defining experiment details, parent strains,
 * parameters, and expected results.
 */
export default {
  name: 'HybridizationForm',
  
  props: {
    /**
     * Experiment ID for edit mode
     * @type {String|Number}
     */
    experimentId: {
      type: [String, Number],
      default: null
    }
  },
  
  data() {
    return {
      /**
       * Current step in the form stepper
       * @type {Number}
       */
      currentStep: 1,
      
      /**
       * Form validation state
       * @type {Boolean}
       */
      isFormValid: false,
      
      /**
       * Loading state during save operation
       * @type {Boolean}
       */
      saving: false,
      
      /**
       * Date picker menu states
       * @type {Boolean}
       */
      startDateMenu: false,
      estimatedEndDateMenu: false,
      
      /**
       * Experiment data model
       * @type {Object}
       */
      experiment: {
        name: '',
        type: '',
        description: '',
        start_date: new Date().toISOString().substr(0, 10),
        estimated_end_date: null,
        location_id: null,
        responsible_user_id: null,
        parent_strains: [],
        parameters: {
          temperature: 25,
          humidity: 60,
          light_hours: 12,
          watering_frequency: 3,
          soil_composition: '',
          fertilizer: '',
          notes: ''
        },
        expected_results: '',
        success_criteria: '',
        expected_germination_rate: 80,
        expected_yield: null,
        notes: ''
      },
      
      /**
       * Currently selected strain for adding to parent strains
       * @type {Object|null}
       */
      selectedStrain: null,
      
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
       * Available parent roles
       * @type {Array}
       */
      parentRoles: [
        { text: this.$t('hybridization.roles.male'), value: 'male' },
        { text: this.$t('hybridization.roles.female'), value: 'female' },
        { text: this.$t('hybridization.roles.both'), value: 'both' }
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
      users: [],
      
      /**
       * Available strains
       * @type {Array}
       */
      strains: []
    }
  },
  
  computed: {
    /**
     * Determines if the form is in edit mode
     * @returns {Boolean}
     */
    isEditMode() {
      return !!this.experimentId;
    },
    
    /**
     * Formats the start date for display
     * @returns {String}
     */
    formattedStartDate() {
      return this.formatDate(this.experiment.start_date);
    },
    
    /**
     * Formats the estimated end date for display
     * @returns {String}
     */
    formattedEstimatedEndDate() {
      return this.formatDate(this.experiment.estimated_end_date);
    },
    
    /**
     * Filters available strains to exclude already selected ones
     * @returns {Array}
     */
    availableStrains() {
      const selectedIds = this.experiment.parent_strains.map(strain => strain.id);
      return this.strains.filter(strain => !selectedIds.includes(strain.id));
    },
    
    /**
     * Validates parent strains based on experiment type
     * @returns {Boolean}
     */
    isParentStrainsValid() {
      if (this.experiment.parent_strains.length === 0) {
        return false;
      }
      
      if (this.experiment.type === 'cross_pollination' && this.experiment.parent_strains.length < 2) {
        return false;
      }
      
      return true;
    }
  },
  
  watch: {
    /**
     * Watch for experiment type changes to adjust parent strain roles
     * @param {String} newType - New experiment type
     */
    'experiment.type'(newType) {
      if (newType === 'self_pollination') {
        this.experiment.parent_strains.forEach(strain => {
          strain.role = 'both';
        });
      }
    }
  },
  
  async created() {
    await this.loadFormData();
    
    if (this.isEditMode) {
      await this.loadExperiment();
    }
  },
  
  methods: {
    /**
     * Load reference data for the form
     * @returns {Promise<void>}
     */
    async loadFormData() {
      try {
        const [locationsResponse, usersResponse, strainsResponse] = await Promise.all([
          this.$api.locations.getAll(),
          this.$api.users.getAll(),
          this.$api.strains.getAll()
        ]);
        
        this.locations = locationsResponse.data;
        this.users = usersResponse.data;
        this.strains = strainsResponse.data;
        
        // Set default responsible user to current user
        if (!this.isEditMode) {
          const currentUser = await this.$api.auth.getCurrentUser();
          this.experiment.responsible_user_id = currentUser.data.id;
        }
      } catch (error) {
        console.error('Error loading form data:', error);
      }
    },
    
    /**
     * Load experiment data for edit mode
     * @returns {Promise<void>}
     */
    async loadExperiment() {
      try {
        const response = await this.$api.hybridization.getExperiment(this.experimentId);
        this.experiment = response.data;
      } catch (error) {
        console.error('Error loading experiment:', error);
      }
    },
    
    /**
     * Add selected strain to parent strains
     */
    addParentStrain() {
      if (!this.selectedStrain) return;
      
      const defaultRole = this.experiment.type === 'self_pollination' ? 'both' : 'male';
      
      this.experiment.parent_strains.push({
        ...this.selectedStrain,
        role: defaultRole
      });
      
      this.selectedStrain = null;
    },
    
    /**
     * Remove parent strain at specified index
     * @param {Number} index - Index of strain to remove
     */
    removeParentStrain(index) {
      this.experiment.parent_strains.splice(index, 1);
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
     * Save experiment data
     * @returns {Promise<void>}
     */
    async saveExperiment() {
      if (!this.$refs.form.validate()) return;
      
      this.saving = true;
      
      try {
        let response;
        
        if (this.isEditMode) {
          response = await this.$api.hybridization.updateExperiment(
            this.experimentId,
            this.experiment
          );
        } else {
          response = await this.$api.hybridization.createExperiment(this.experiment);
        }
        
        this.$store.dispatch('notifications/showSuccess', {
          message: this.isEditMode
            ? this.$t('hybridization.experimentUpdated')
            : this.$t('hybridization.experimentCreated')
        });
        
        this.$router.push({
          name: 'hybridization-details',
          params: { id: response.data.id }
        });
      } catch (error) {
        console.error('Error saving experiment:', error);
        
        this.$store.dispatch('notifications/showError', {
          message: this.$t('hybridization.errorSavingExperiment')
        });
      } finally {
        this.saving = false;
      }
    },
    
    /**
     * Cancel form and navigate back
     */
    cancelForm() {
      this.$router.go(-1);
    }
  }
}
</script>

<style scoped>
.hybridization-form-container {
  padding: 20px;
}

.form-title {
  margin-bottom: 24px;
  color: var(--v-primary-base);
  font-weight: 500;
}
</style>
