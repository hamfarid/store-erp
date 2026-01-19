<template>
  <div class="feedback-form-container">
    <h2 class="form-title">{{ $t('feedback.submitFeedback') }}</h2>
    
    <v-form ref="form" v-model="valid" @submit.prevent="submitFeedback">
      <v-card class="pa-4 mb-4">
        <v-card-text>
          <v-select
            v-model="feedback.type"
            :items="feedbackTypes"
            :label="$t('feedback.type')"
            :rules="[v => !!v || $t('feedback.typeRequired')]"
            required
          ></v-select>
          
          <v-text-field
            v-model="feedback.subject"
            :label="$t('feedback.subject')"
            :rules="[v => !!v || $t('feedback.subjectRequired')]"
            required
          ></v-text-field>
          
          <v-textarea
            v-model="feedback.content"
            :label="$t('feedback.content')"
            :rules="[v => !!v || $t('feedback.contentRequired'), v => v.length >= 10 || $t('feedback.contentMinLength')]"
            counter
            required
            rows="5"
          ></v-textarea>
          
          <v-file-input
            v-model="feedback.attachments"
            :label="$t('feedback.attachments')"
            multiple
            prepend-icon="mdi-paperclip"
            :hint="$t('feedback.attachmentsHint')"
            persistent-hint
            accept="image/*, .pdf, .doc, .docx, .xls, .xlsx"
          ></v-file-input>
          
          <v-checkbox
            v-model="feedback.anonymous"
            :label="$t('feedback.submitAnonymously')"
          ></v-checkbox>
        </v-card-text>
      </v-card>
      
      <div class="d-flex justify-end">
        <v-btn
          color="primary"
          type="submit"
          :loading="loading"
          :disabled="!valid || loading"
        >
          {{ $t('feedback.submit') }}
        </v-btn>
      </div>
    </v-form>
    
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
 * @component FeedbackForm
 * @description A form component for submitting user feedback to the system.
 * This component allows users to submit different types of feedback including
 * suggestions, bug reports, feature requests, and general comments.
 */
export default {
  name: 'FeedbackForm',
  
  data() {
    return {
      /**
       * Form validation state
       * @type {Boolean}
       */
      valid: false,
      
      /**
       * Loading state for form submission
       * @type {Boolean}
       */
      loading: false,
      
      /**
       * Feedback data object
       * @type {Object}
       * @property {String} type - Type of feedback (suggestion, bug, feature, etc.)
       * @property {String} subject - Subject/title of the feedback
       * @property {String} content - Detailed content of the feedback
       * @property {Array} attachments - File attachments related to the feedback
       * @property {Boolean} anonymous - Whether to submit feedback anonymously
       */
      feedback: {
        type: '',
        subject: '',
        content: '',
        attachments: [],
        anonymous: false
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
  
  methods: {
    /**
     * Submit feedback to the backend API
     * @async
     * @returns {Promise<void>}
     */
    async submitFeedback() {
      if (!this.$refs.form.validate()) return;
      
      this.loading = true;
      
      try {
        // Prepare form data for file uploads
        const formData = new FormData();
        formData.append('type', this.feedback.type);
        formData.append('subject', this.feedback.subject);
        formData.append('content', this.feedback.content);
        formData.append('anonymous', this.feedback.anonymous);
        
        // Append attachments if any
        if (this.feedback.attachments && this.feedback.attachments.length) {
          this.feedback.attachments.forEach((file, index) => {
            formData.append(`attachment_${index}`, file);
          });
        }
        
        // Send to API
        const response = await this.$api.feedback.submitFeedback(formData);
        
        // Show success message
        this.showSnackbar(this.$t('feedback.submitSuccess'), 'success');
        
        // Reset form
        this.$refs.form.reset();
        this.feedback = {
          type: '',
          subject: '',
          content: '',
          attachments: [],
          anonymous: false
        };
        
        // Emit success event
        this.$emit('feedback-submitted', response.data);
      } catch (error) {
        console.error('Error submitting feedback:', error);
        this.showSnackbar(
          error.response?.data?.message || this.$t('feedback.submitError'),
          'error'
        );
      } finally {
        this.loading = false;
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
.feedback-form-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.form-title {
  margin-bottom: 20px;
  color: var(--v-primary-base);
  font-weight: 500;
}
</style>
