<template>
  <div class="feedback-list-container">
    <h2 class="list-title">{{ $t('feedback.feedbackList') }}</h2>
    
    <div class="filters-container mb-4">
      <v-card class="pa-4">
        <v-row>
          <v-col cols="12" sm="4">
            <v-select
              v-model="filters.type"
              :items="feedbackTypes"
              :label="$t('feedback.filterByType')"
              clearable
              @change="loadFeedbacks(1)"
            ></v-select>
          </v-col>
          
          <v-col cols="12" sm="4">
            <v-select
              v-model="filters.status"
              :items="statusTypes"
              :label="$t('feedback.filterByStatus')"
              clearable
              @change="loadFeedbacks(1)"
            ></v-select>
          </v-col>
          
          <v-col cols="12" sm="4">
            <v-text-field
              v-model="filters.search"
              :label="$t('feedback.search')"
              append-icon="mdi-magnify"
              clearable
              @keyup.enter="loadFeedbacks(1)"
              @click:append="loadFeedbacks(1)"
              @click:clear="clearSearch"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card>
    </div>
    
    <div v-if="loading" class="d-flex justify-center my-5">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>
    
    <div v-else-if="feedbacks.length === 0" class="text-center my-5">
      <v-icon size="64" color="grey lighten-1">mdi-comment-text-outline</v-icon>
      <p class="mt-3 grey--text">{{ $t('feedback.noFeedbackFound') }}</p>
    </div>
    
    <v-card v-else v-for="feedback in feedbacks" :key="feedback.id" class="mb-4">
      <v-card-title class="d-flex justify-space-between">
        <div>
          <span class="headline">{{ feedback.subject }}</span>
          <v-chip
            small
            class="ml-2"
            :color="getTypeColor(feedback.type)"
            text-color="white"
          >
            {{ getTypeLabel(feedback.type) }}
          </v-chip>
        </div>
        <v-chip
          small
          :color="getStatusColor(feedback.status)"
          text-color="white"
        >
          {{ getStatusLabel(feedback.status) }}
        </v-chip>
      </v-card-title>
      
      <v-card-text>
        <p class="feedback-content">{{ feedback.content }}</p>
        
        <div v-if="feedback.attachments && feedback.attachments.length" class="mt-3">
          <div class="subtitle-1">{{ $t('feedback.attachments') }}:</div>
          <v-chip
            v-for="(attachment, index) in feedback.attachments"
            :key="index"
            class="ma-1"
            @click="downloadAttachment(attachment)"
          >
            <v-icon left small>{{ getFileIcon(attachment.name) }}</v-icon>
            {{ attachment.name }}
          </v-chip>
        </div>
        
        <div class="d-flex justify-space-between mt-3">
          <div class="caption grey--text">
            {{ feedback.anonymous ? $t('feedback.anonymous') : feedback.user_name }}
          </div>
          <div class="caption grey--text">
            {{ formatDate(feedback.created_at) }}
          </div>
        </div>
      </v-card-text>
      
      <v-divider v-if="feedback.responses && feedback.responses.length"></v-divider>
      
      <v-card-text v-if="feedback.responses && feedback.responses.length">
        <div class="subtitle-1 mb-2">{{ $t('feedback.responses') }}:</div>
        <div v-for="(response, index) in feedback.responses" :key="index" class="response-item pa-2 mb-2">
          <div class="response-content">{{ response.content }}</div>
          <div class="d-flex justify-space-between mt-1">
            <div class="caption">{{ response.user_name }}</div>
            <div class="caption grey--text">{{ formatDate(response.created_at) }}</div>
          </div>
        </div>
      </v-card-text>
      
      <v-card-actions>
        <v-btn
          text
          color="primary"
          @click="viewFeedbackDetails(feedback.id)"
        >
          {{ $t('feedback.viewDetails') }}
        </v-btn>
        
        <v-btn
          v-if="canRespondToFeedback"
          text
          color="primary"
          @click="openResponseDialog(feedback.id)"
        >
          {{ $t('feedback.respond') }}
        </v-btn>
        
        <v-spacer></v-spacer>
        
        <v-btn
          v-if="canUpdateFeedbackStatus"
          text
          color="primary"
          @click="openStatusUpdateDialog(feedback)"
        >
          {{ $t('feedback.updateStatus') }}
        </v-btn>
      </v-card-actions>
    </v-card>
    
    <div class="d-flex justify-center mt-4">
      <v-pagination
        v-if="totalPages > 1"
        v-model="currentPage"
        :length="totalPages"
        @input="loadFeedbacks"
      ></v-pagination>
    </div>
    
    <!-- Response Dialog -->
    <v-dialog v-model="responseDialog.show" max-width="600px">
      <v-card>
        <v-card-title>{{ $t('feedback.respondToFeedback') }}</v-card-title>
        <v-card-text>
          <v-textarea
            v-model="responseDialog.content"
            :label="$t('feedback.responseContent')"
            :rules="[v => !!v || $t('feedback.responseRequired')]"
            rows="5"
            counter
            required
          ></v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="responseDialog.show = false">
            {{ $t('common.cancel') }}
          </v-btn>
          <v-btn
            color="primary"
            :loading="responseDialog.loading"
            :disabled="!responseDialog.content || responseDialog.loading"
            @click="submitResponse"
          >
            {{ $t('feedback.submit') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Status Update Dialog -->
    <v-dialog v-model="statusDialog.show" max-width="400px">
      <v-card>
        <v-card-title>{{ $t('feedback.updateFeedbackStatus') }}</v-card-title>
        <v-card-text>
          <v-select
            v-model="statusDialog.status"
            :items="statusTypes"
            :label="$t('feedback.newStatus')"
            required
          ></v-select>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="statusDialog.show = false">
            {{ $t('common.cancel') }}
          </v-btn>
          <v-btn
            color="primary"
            :loading="statusDialog.loading"
            :disabled="!statusDialog.status || statusDialog.loading"
            @click="updateFeedbackStatus"
          >
            {{ $t('common.update') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      timeout="5000"
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
  </div>
</template>

<script>
/**
 * @component FeedbackList
 * @description A component for displaying and managing feedback items.
 * This component allows administrators and authorized users to view, filter,
 * respond to, and update the status of feedback submitted by users.
 */
export default {
  name: 'FeedbackList',
  
  props: {
    /**
     * Whether the current user can respond to feedback
     * @type {Boolean}
     * @default false
     */
    canRespondToFeedback: {
      type: Boolean,
      default: false
    },
    
    /**
     * Whether the current user can update feedback status
     * @type {Boolean}
     * @default false
     */
    canUpdateFeedbackStatus: {
      type: Boolean,
      default: false
    }
  },
  
  data() {
    return {
      /**
       * List of feedback items
       * @type {Array}
       */
      feedbacks: [],
      
      /**
       * Current page number for pagination
       * @type {Number}
       */
      currentPage: 1,
      
      /**
       * Total number of pages
       * @type {Number}
       */
      totalPages: 1,
      
      /**
       * Loading state
       * @type {Boolean}
       */
      loading: false,
      
      /**
       * Filter options
       * @type {Object}
       * @property {String} type - Filter by feedback type
       * @property {String} status - Filter by feedback status
       * @property {String} search - Search term
       */
      filters: {
        type: null,
        status: null,
        search: ''
      },
      
      /**
       * Available feedback types
       * @type {Array}
       */
      feedbackTypes: [
        { text: this.$t('feedback.types.suggestion'), value: 'suggestion' },
        { text: this.$t('feedback.types.bug'), value: 'bug' },
        { text: this.$t('feedback.types.feature'), value: 'feature' },
        { text: this.$t('feedback.types.comment'), value: 'comment' },
        { text: this.$t('feedback.types.other'), value: 'other' }
      ],
      
      /**
       * Available status types
       * @type {Array}
       */
      statusTypes: [
        { text: this.$t('feedback.status.new'), value: 'new' },
        { text: this.$t('feedback.status.inProgress'), value: 'in_progress' },
        { text: this.$t('feedback.status.resolved'), value: 'resolved' },
        { text: this.$t('feedback.status.closed'), value: 'closed' },
        { text: this.$t('feedback.status.rejected'), value: 'rejected' }
      ],
      
      /**
       * Response dialog state
       * @type {Object}
       * @property {Boolean} show - Whether to show the dialog
       * @property {String} feedbackId - ID of the feedback to respond to
       * @property {String} content - Response content
       * @property {Boolean} loading - Loading state
       */
      responseDialog: {
        show: false,
        feedbackId: null,
        content: '',
        loading: false
      },
      
      /**
       * Status update dialog state
       * @type {Object}
       * @property {Boolean} show - Whether to show the dialog
       * @property {Object} feedback - Feedback object to update
       * @property {String} status - New status
       * @property {Boolean} loading - Loading state
       */
      statusDialog: {
        show: false,
        feedback: null,
        status: '',
        loading: false
      },
      
      /**
       * Snackbar notification state
       * @type {Object}
       * @property {Boolean} show - Whether to show the snackbar
       * @property {String} text - Text message to display
       * @property {String} color - Color of the snackbar (success, error, etc.)
       */
      snackbar: {
        show: false,
        text: '',
        color: ''
      }
    }
  },
  
  created() {
    this.loadFeedbacks();
  },
  
  methods: {
    /**
     * Load feedback items from the API
     * @param {Number} page - Page number to load
     * @returns {Promise<void>}
     */
    async loadFeedbacks(page = this.currentPage) {
      this.loading = true;
      
      try {
        const params = {
          page,
          type: this.filters.type,
          status: this.filters.status,
          search: this.filters.search
        };
        
        const response = await this.$api.feedback.getFeedbacks(params);
        
        this.feedbacks = response.data.items;
        this.totalPages = response.data.total_pages;
        this.currentPage = page;
      } catch (error) {
        console.error('Error loading feedbacks:', error);
        this.showSnackbar(
          error.response?.data?.message || this.$t('feedback.loadError'),
          'error'
        );
      } finally {
        this.loading = false;
      }
    },
    
    /**
     * Clear search filter and reload feedbacks
     */
    clearSearch() {
      this.filters.search = '';
      this.loadFeedbacks(1);
    },
    
    /**
     * Get color for feedback type
     * @param {String} type - Feedback type
     * @returns {String} - Color name
     */
    getTypeColor(type) {
      const colors = {
        suggestion: 'blue',
        bug: 'red',
        feature: 'green',
        comment: 'purple',
        other: 'grey'
      };
      
      return colors[type] || 'grey';
    },
    
    /**
     * Get label for feedback type
     * @param {String} type - Feedback type
     * @returns {String} - Translated label
     */
    getTypeLabel(type) {
      return this.$t(`feedback.types.${type}`) || type;
    },
    
    /**
     * Get color for feedback status
     * @param {String} status - Feedback status
     * @returns {String} - Color name
     */
    getStatusColor(status) {
      const colors = {
        new: 'blue',
        in_progress: 'orange',
        resolved: 'green',
        closed: 'grey',
        rejected: 'red'
      };
      
      return colors[status] || 'grey';
    },
    
    /**
     * Get label for feedback status
     * @param {String} status - Feedback status
     * @returns {String} - Translated label
     */
    getStatusLabel(status) {
      return this.$t(`feedback.status.${status.replace('_', '')}`) || status;
    },
    
    /**
     * Get icon for file type
     * @param {String} fileName - File name
     * @returns {String} - Icon name
     */
    getFileIcon(fileName) {
      const extension = fileName.split('.').pop().toLowerCase();
      
      const icons = {
        pdf: 'mdi-file-pdf',
        doc: 'mdi-file-word',
        docx: 'mdi-file-word',
        xls: 'mdi-file-excel',
        xlsx: 'mdi-file-excel',
        jpg: 'mdi-file-image',
        jpeg: 'mdi-file-image',
        png: 'mdi-file-image',
        gif: 'mdi-file-image'
      };
      
      return icons[extension] || 'mdi-file';
    },
    
    /**
     * Format date to localized string
     * @param {String} dateString - ISO date string
     * @returns {String} - Formatted date
     */
    formatDate(dateString) {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      return date.toLocaleString(this.$i18n.locale, {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    
    /**
     * Download attachment file
     * @param {Object} attachment - Attachment object
     */
    downloadAttachment(attachment) {
      window.open(attachment.url, '_blank');
    },
    
    /**
     * Navigate to feedback details page
     * @param {String} id - Feedback ID
     */
    viewFeedbackDetails(id) {
      this.$router.push({ name: 'feedback-details', params: { id } });
    },
    
    /**
     * Open dialog to respond to feedback
     * @param {String} id - Feedback ID
     */
    openResponseDialog(id) {
      this.responseDialog = {
        show: true,
        feedbackId: id,
        content: '',
        loading: false
      };
    },
    
    /**
     * Submit response to feedback
     * @returns {Promise<void>}
     */
    async submitResponse() {
      if (!this.responseDialog.content) return;
      
      this.responseDialog.loading = true;
      
      try {
        await this.$api.feedback.respondToFeedback(
          this.responseDialog.feedbackId,
          { content: this.responseDialog.content }
        );
        
        this.showSnackbar(this.$t('feedback.responseSuccess'), 'success');
        this.responseDialog.show = false;
        this.loadFeedbacks(); // Reload to show the new response
      } catch (error) {
        console.error('Error submitting response:', error);
        this.showSnackbar(
          error.response?.data?.message || this.$t('feedback.responseError'),
          'error'
        );
      } finally {
        this.responseDialog.loading = false;
      }
    },
    
    /**
     * Open dialog to update feedback status
     * @param {Object} feedback - Feedback object
     */
    openStatusUpdateDialog(feedback) {
      this.statusDialog = {
        show: true,
        feedback,
        status: feedback.status,
        loading: false
      };
    },
    
    /**
     * Update feedback status
     * @returns {Promise<void>}
     */
    async updateFeedbackStatus() {
      if (!this.statusDialog.status) return;
      
      this.statusDialog.loading = true;
      
      try {
        await this.$api.feedback.updateFeedbackStatus(
          this.statusDialog.feedback.id,
          { status: this.statusDialog.status }
        );
        
        this.showSnackbar(this.$t('feedback.statusUpdateSuccess'), 'success');
        this.statusDialog.show = false;
        this.loadFeedbacks(); // Reload to show the updated status
      } catch (error) {
        console.error('Error updating status:', error);
        this.showSnackbar(
          error.response?.data?.message || this.$t('feedback.statusUpdateError'),
          'error'
        );
      } finally {
        this.statusDialog.loading = false;
      }
    },
    
    /**
     * Display a snackbar notification
     * @param {String} text - Message to display
     * @param {String} color - Color of the snackbar (success, error, etc.)
     */
    showSnackbar(text, color = 'info') {
      this.snackbar = {
        show: true,
        text,
        color
      };
    }
  }
}
</script>

<style scoped>
.feedback-list-container {
  padding: 20px;
}

.list-title {
  margin-bottom: 20px;
  color: var(--v-primary-base);
  font-weight: 500;
}

.feedback-content {
  white-space: pre-line;
  max-height: 150px;
  overflow-y: auto;
}

.response-item {
  background-color: #f5f5f5;
  border-radius: 4px;
  border-left: 3px solid var(--v-primary-base);
}

.response-content {
  white-space: pre-line;
}
</style>
