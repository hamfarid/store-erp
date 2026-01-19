<template>
  <div class="feedback-details-container">
    <div class="d-flex justify-space-between align-center mb-4">
      <h2 class="details-title">{{ $t('feedback.feedbackDetails') }}</h2>
      <v-btn
        text
        color="primary"
        @click="goBack"
      >
        <v-icon left>mdi-arrow-left</v-icon>
        {{ $t('common.back') }}
      </v-btn>
    </div>
    
    <div v-if="loading" class="d-flex justify-center my-5">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>
    
    <div v-else-if="!feedback" class="text-center my-5">
      <v-icon size="64" color="grey lighten-1">mdi-alert-circle-outline</v-icon>
      <p class="mt-3 grey--text">{{ $t('feedback.feedbackNotFound') }}</p>
    </div>
    
    <template v-else>
      <v-card class="mb-4">
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
          
          <div v-if="feedback.attachments && feedback.attachments.length" class="mt-4">
            <div class="subtitle-1">{{ $t('feedback.attachments') }}:</div>
            <div class="attachment-grid">
              <div v-for="(attachment, index) in feedback.attachments" :key="index" class="attachment-item">
                <v-card class="attachment-card" @click="viewAttachment(attachment)">
                  <div class="attachment-icon">
                    <v-icon size="36">{{ getFileIcon(attachment.name) }}</v-icon>
                  </div>
                  <div class="attachment-name">{{ attachment.name }}</div>
                </v-card>
              </div>
            </div>
          </div>
          
          <div class="d-flex justify-space-between mt-4">
            <div class="caption grey--text">
              {{ $t('feedback.submittedBy') }}: {{ feedback.anonymous ? $t('feedback.anonymous') : feedback.user_name }}
            </div>
            <div class="caption grey--text">
              {{ $t('feedback.submittedOn') }}: {{ formatDate(feedback.created_at) }}
            </div>
          </div>
        </v-card-text>
        
        <v-divider></v-divider>
        
        <v-card-actions>
          <v-btn
            v-if="canUpdateFeedbackStatus"
            text
            color="primary"
            @click="openStatusUpdateDialog"
          >
            <v-icon left>mdi-update</v-icon>
            {{ $t('feedback.updateStatus') }}
          </v-btn>
          
          <v-btn
            v-if="canRespondToFeedback"
            text
            color="primary"
            @click="openResponseDialog"
          >
            <v-icon left>mdi-reply</v-icon>
            {{ $t('feedback.respond') }}
          </v-btn>
          
          <v-spacer></v-spacer>
          
          <v-btn
            v-if="canDeleteFeedback"
            text
            color="error"
            @click="confirmDelete"
          >
            <v-icon left>mdi-delete</v-icon>
            {{ $t('common.delete') }}
          </v-btn>
        </v-card-actions>
      </v-card>
      
      <!-- Responses Section -->
      <v-card v-if="feedback.responses && feedback.responses.length" class="mb-4">
        <v-card-title>
          {{ $t('feedback.responses') }}
          <v-chip class="ml-2" small>{{ feedback.responses.length }}</v-chip>
        </v-card-title>
        
        <v-card-text>
          <div v-for="(response, index) in feedback.responses" :key="index" class="response-item pa-3 mb-3">
            <div class="response-content">{{ response.content }}</div>
            <div class="d-flex justify-space-between mt-2">
              <div class="caption">
                {{ $t('feedback.respondedBy') }}: {{ response.user_name }}
              </div>
              <div class="caption grey--text">
                {{ formatDate(response.created_at) }}
              </div>
            </div>
          </div>
        </v-card-text>
      </v-card>
      
      <!-- New Response Form -->
      <v-card v-if="canRespondToFeedback" class="mb-4">
        <v-card-title>{{ $t('feedback.addResponse') }}</v-card-title>
        
        <v-card-text>
          <v-textarea
            v-model="newResponse"
            :label="$t('feedback.responseContent')"
            :rules="[v => !!v || $t('feedback.responseRequired')]"
            rows="4"
            counter
            required
          ></v-textarea>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            :loading="submittingResponse"
            :disabled="!newResponse || submittingResponse"
            @click="submitResponse"
          >
            {{ $t('feedback.submit') }}
          </v-btn>
        </v-card-actions>
      </v-card>
      
      <!-- History Section -->
      <v-card v-if="feedback.history && feedback.history.length">
        <v-card-title>
          {{ $t('feedback.history') }}
          <v-chip class="ml-2" small>{{ feedback.history.length }}</v-chip>
        </v-card-title>
        
        <v-card-text>
          <v-timeline dense>
            <v-timeline-item
              v-for="(event, index) in feedback.history"
              :key="index"
              :color="getHistoryEventColor(event.type)"
              small
            >
              <div class="d-flex justify-space-between">
                <div>
                  <strong>{{ getHistoryEventLabel(event.type) }}</strong>
                  <div v-if="event.details" class="mt-1">{{ event.details }}</div>
                </div>
                <div class="caption grey--text">
                  {{ formatDate(event.timestamp) }}
                </div>
              </div>
              <div class="caption mt-1">
                {{ $t('feedback.by') }}: {{ event.user_name }}
              </div>
            </v-timeline-item>
          </v-timeline>
        </v-card-text>
      </v-card>
    </template>
    
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
          
          <v-textarea
            v-model="statusDialog.comment"
            :label="$t('feedback.statusUpdateComment')"
            rows="3"
            counter
          ></v-textarea>
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
            @click="submitResponseDialog"
          >
            {{ $t('feedback.submit') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog.show" max-width="400px">
      <v-card>
        <v-card-title class="headline">{{ $t('feedback.confirmDelete') }}</v-card-title>
        <v-card-text>
          {{ $t('feedback.deleteWarning') }}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="deleteDialog.show = false">
            {{ $t('common.cancel') }}
          </v-btn>
          <v-btn
            color="error"
            :loading="deleteDialog.loading"
            @click="deleteFeedback"
          >
            {{ $t('common.delete') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Attachment Viewer Dialog -->
    <v-dialog v-model="attachmentDialog.show" max-width="800px">
      <v-card>
        <v-card-title class="d-flex justify-space-between">
          <span>{{ attachmentDialog.attachment?.name || '' }}</span>
          <v-btn icon @click="attachmentDialog.show = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text class="text-center">
          <div v-if="isImageAttachment(attachmentDialog.attachment)" class="image-preview">
            <img :src="attachmentDialog.attachment?.url" alt="Attachment preview" />
          </div>
          <div v-else class="non-image-preview">
            <v-icon size="64">{{ getFileIcon(attachmentDialog.attachment?.name || '') }}</v-icon>
            <p class="mt-3">{{ $t('feedback.cannotPreviewFile') }}</p>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            @click="downloadAttachment(attachmentDialog.attachment)"
          >
            <v-icon left>mdi-download</v-icon>
            {{ $t('feedback.download') }}
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
 * @component FeedbackDetails
 * @description A component for displaying and managing detailed information about a feedback item.
 * This component allows viewing feedback details, attachments, responses, and history,
 * as well as responding to feedback, updating its status, and deleting it if authorized.
 */
export default {
  name: 'FeedbackDetails',
  
  props: {
    /**
     * ID of the feedback to display
     * @type {String}
     * @required
     */
    id: {
      type: String,
      required: true
    },
    
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
    },
    
    /**
     * Whether the current user can delete feedback
     * @type {Boolean}
     * @default false
     */
    canDeleteFeedback: {
      type: Boolean,
      default: false
    }
  },
  
  data() {
    return {
      /**
       * Feedback data object
       * @type {Object|null}
       */
      feedback: null,
      
      /**
       * Loading state
       * @type {Boolean}
       */
      loading: false,
      
      /**
       * New response content
       * @type {String}
       */
      newResponse: '',
      
      /**
       * Submitting response state
       * @type {Boolean}
       */
      submittingResponse: false,
      
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
       * Status update dialog state
       * @type {Object}
       * @property {Boolean} show - Whether to show the dialog
       * @property {String} status - New status
       * @property {String} comment - Status update comment
       * @property {Boolean} loading - Loading state
       */
      statusDialog: {
        show: false,
        status: '',
        comment: '',
        loading: false
      },
      
      /**
       * Response dialog state
       * @type {Object}
       * @property {Boolean} show - Whether to show the dialog
       * @property {String} content - Response content
       * @property {Boolean} loading - Loading state
       */
      responseDialog: {
        show: false,
        content: '',
        loading: false
      },
      
      /**
       * Delete confirmation dialog state
       * @type {Object}
       * @property {Boolean} show - Whether to show the dialog
       * @property {Boolean} loading - Loading state
       */
      deleteDialog: {
        show: false,
        loading: false
      },
      
      /**
       * Attachment viewer dialog state
       * @type {Object}
       * @property {Boolean} show - Whether to show the dialog
       * @property {Object|null} attachment - Attachment object to view
       */
      attachmentDialog: {
        show: false,
        attachment: null
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
    this.loadFeedbackDetails();
  },
  
  methods: {
    /**
     * Load feedback details from the API
     * @returns {Promise<void>}
     */
    async loadFeedbackDetails() {
      this.loading = true;
      
      try {
        const response = await this.$api.feedback.getFeedbackDetails(this.id);
        this.feedback = response.data;
      } catch (error) {
        console.error('Error loading feedback details:', error);
        this.showSnackbar(
          error.response?.data?.message || this.$t('feedback.loadError'),
          'error'
        );
      } finally {
        this.loading = false;
      }
    },
    
    /**
     * Navigate back to the previous page
     */
    goBack() {
      this.$router.go(-1);
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
     * Get color for history event type
     * @param {String} type - Event type
     * @returns {String} - Color name
     */
    getHistoryEventColor(type) {
      const colors = {
        created: 'green',
        status_updated: 'orange',
        response_added: 'blue',
        edited: 'purple'
      };
      
      return colors[type] || 'grey';
    },
    
    /**
     * Get label for history event type
     * @param {String} type - Event type
     * @returns {String} - Translated label
     */
    getHistoryEventLabel(type) {
      return this.$t(`feedback.historyEvents.${type.replace('_', '')}`) || type;
    },
    
    /**
     * Get icon for file type
     * @param {String} fileName - File name
     * @returns {String} - Icon name
     */
    getFileIcon(fileName) {
      if (!fileName) return 'mdi-file';
      
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
     * Check if attachment is an image
     * @param {Object} attachment - Attachment object
     * @returns {Boolean} - Whether the attachment is an image
     */
    isImageAttachment(attachment) {
      if (!attachment || !attachment.name) return false;
      
      const extension = attachment.name.split('.').pop().toLowerCase();
      return ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'].includes(extension);
    },
    
    /**
     * View attachment in dialog
     * @param {Object} attachment - Attachment object
     */
    viewAttachment(attachment) {
      this.attachmentDialog = {
        show: true,
        attachment
      };
    },
    
    /**
     * Download attachment file
     * @param {Object} attachment - Attachment object
     */
    downloadAttachment(attachment) {
      if (!attachment || !attachment.url) return;
      
      window.open(attachment.url, '_blank');
    },
    
    /**
     * Open status update dialog
     */
    openStatusUpdateDialog() {
      this.statusDialog = {
        show: true,
        status: this.feedback.status,
        comment: '',
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
          this.id,
          {
            status: this.statusDialog.status,
            comment: this.statusDialog.comment
          }
        );
        
        this.showSnackbar(this.$t('feedback.statusUpdateSuccess'), 'success');
        this.statusDialog.show = false;
        this.loadFeedbackDetails(); // Reload to show the updated status
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
     * Open response dialog
     */
    openResponseDialog() {
      this.responseDialog = {
        show: true,
        content: '',
        loading: false
      };
    },
    
    /**
     * Submit response from dialog
     * @returns {Promise<void>}
     */
    async submitResponseDialog() {
      if (!this.responseDialog.content) return;
      
      this.responseDialog.loading = true;
      
      try {
        await this.$api.feedback.respondToFeedback(
          this.id,
          { content: this.responseDialog.content }
        );
        
        this.showSnackbar(this.$t('feedback.responseSuccess'), 'success');
        this.responseDialog.show = false;
        this.loadFeedbackDetails(); // Reload to show the new response
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
     * Submit response from form
     * @returns {Promise<void>}
     */
    async submitResponse() {
      if (!this.newResponse) return;
      
      this.submittingResponse = true;
      
      try {
        await this.$api.feedback.respondToFeedback(
          this.id,
          { content: this.newResponse }
        );
        
        this.showSnackbar(this.$t('feedback.responseSuccess'), 'success');
        this.newResponse = '';
        this.loadFeedbackDetails(); // Reload to show the new response
      } catch (error) {
        console.error('Error submitting response:', error);
        this.showSnackbar(
          error.response?.data?.message || this.$t('feedback.responseError'),
          'error'
        );
      } finally {
        this.submittingResponse = false;
      }
    },
    
    /**
     * Open delete confirmation dialog
     */
    confirmDelete() {
      this.deleteDialog = {
        show: true,
        loading: false
      };
    },
    
    /**
     * Delete feedback
     * @returns {Promise<void>}
     */
    async deleteFeedback() {
      this.deleteDialog.loading = true;
      
      try {
        await this.$api.feedback.deleteFeedback(this.id);
        
        this.showSnackbar(this.$t('feedback.deleteSuccess'), 'success');
        this.deleteDialog.show = false;
        
        // Navigate back to feedback list
        this.$router.push({ name: 'feedback-list' });
      } catch (error) {
        console.error('Error deleting feedback:', error);
        this.showSnackbar(
          error.response?.data?.message || this.$t('feedback.deleteError'),
          'error'
        );
      } finally {
        this.deleteDialog.loading = false;
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
.feedback-details-container {
  padding: 20px;
}

.details-title {
  color: var(--v-primary-base);
  font-weight: 500;
}

.feedback-content {
  white-space: pre-line;
  line-height: 1.6;
}

.attachment-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 16px;
  margin-top: 12px;
}

.attachment-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.attachment-card:hover {
  background-color: #f5f5f5;
}

.attachment-icon {
  margin-bottom: 8px;
}

.attachment-name {
  font-size: 12px;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  width: 100%;
}

.response-item {
  background-color: #f5f5f5;
  border-radius: 4px;
  border-left: 3px solid var(--v-primary-base);
}

.response-content {
  white-space: pre-line;
  line-height: 1.5;
}

.image-preview {
  max-height: 500px;
  overflow: auto;
}

.image-preview img {
  max-width: 100%;
}

.non-image-preview {
  padding: 40px;
}
</style>
