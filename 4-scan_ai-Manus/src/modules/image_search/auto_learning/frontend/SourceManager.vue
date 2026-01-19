# /home/ubuntu/image_search_integration/auto_learning/frontend/SourceManager.vue

"""
مكون Vue لإدارة المصادر الموثوقة للبحث الذاتي الذكي

هذا المكون يوفر واجهة رسومية لإدارة المصادر الموثوقة، بما في ذلك:
- عرض المصادر مع فلاتر بحث متقدمة وترقيم الصفحات.
- إضافة وتعديل وحذف المصادر.
- تقييم مستوى الثقة للمصادر بشكل ديناميكي.
- إدارة القائمة السوداء للمصادر غير الموثوقة.
- عرض إحصائيات أداء المصادر.
- التحكم في حالة النشاط.
- التكامل مع نظام الصلاحيات.
"""

<template>
  <div class="source-manager">
    <div class="card shadow-sm">
      <div class="card-header bg-light d-flex justify-content-between align-items-center py-3">
        <h5 class="mb-0 text-primary"><i class="fas fa-globe me-2"></i>{{ $t("إدارة المصادر الموثوقة") }}</h5>
        <button class="btn btn-primary btn-sm rounded-pill px-3" @click="openAddSourceModal" v-if="canCreateSource">
          <i class="fas fa-plus me-1"></i> {{ $t("إضافة مصدر") }}
        </button>
      </div>
      <div class="card-body">
        <!-- فلاتر البحث المتقدمة -->
        <div class="row g-3 mb-4 align-items-center bg-light p-3 rounded">
          <div class="col-md-3">
            <div class="input-group input-group-sm">
              <span class="input-group-text bg-white border-end-0"><i class="fas fa-search text-muted"></i></span>
              <input type="text" class="form-control border-start-0" v-model="filters.domain"
                :placeholder="$t('بحث بالنطاق أو الوصف...')" @input="debouncedFetchSources" />
            </div>
          </div>
          <div class="col-md-2">
            <select class="form-select form-select-sm" v-model="filters.trustLevel" @change="fetchSources">
              <option value="">{{ $t("كل مستويات الثقة") }}</option>
              <option v-for="level in trustLevels" :key="level.value" :value="level.value">
                {{ $t(level.label) }}
              </option>
            </select>
          </div>
          <div class="col-md-2">
            <select class="form-select form-select-sm" v-model="filters.category" @change="fetchSources">
              <option value="">{{ $t("كل التصنيفات") }}</option>
              <option v-for="category in sourceCategories" :key="category.value" :value="category.value">
                {{ $t(category.label) }}
              </option>
            </select>
          </div>
          <div class="col-md-2">
            <select class="form-select form-select-sm" v-model="filters.status" @change="fetchSources">
              <option value="">{{ $t("كل الحالات") }}</option>
              <option value="active">{{ $t("نشط") }}</option>
              <option value="inactive">{{ $t("غير نشط") }}</option>
              <option value="blacklisted">{{ $t("القائمة السوداء") }}</option>
            </select>
          </div>
          <div class="col-md-2">
            <select class="form-select form-select-sm" v-model="filters.sortBy" @change="fetchSources">
              <option value="domain">{{ $t("ترتيب حسب النطاق") }}</option>
              <option value="trust_level">{{ $t("ترتيب حسب مستوى الثقة") }}</option>
              <option value="created_at">{{ $t("ترتيب حسب تاريخ الإضافة") }}</option>
              <option value="usage_count">{{ $t("ترتيب حسب الاستخدام") }}</option>
            </select>
          </div>
          <div class="col-md-1">
            <select class="form-select form-select-sm" v-model="filters.sortOrder" @change="fetchSources">
              <option value="asc">{{ $t("تصاعدي") }}</option>
              <option value="desc">{{ $t("تنازلي") }}</option>
            </select>
          </div>
        </div>

        <!-- رسالة التحميل أو الخطأ -->
        <div v-if="loading" class="text-center p-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">{{ $t("جاري التحميل...") }}</span>
          </div>
        </div>
        <div v-else-if="error" class="alert alert-danger">
          {{ $t("حدث خطأ أثناء تحميل المصادر:") }} {{ error }}
        </div>

        <!-- جدول المصادر -->
        <div v-else class="table-responsive">
          <table class="table table-striped table-hover table-sm align-middle">
            <thead class="table-light">
              <tr>
                <th>{{ $t("النطاق") }}</th>
                <th>{{ $t("الوصف") }}</th>
                <th>{{ $t("التصنيف") }}</th>
                <th>{{ $t("مستوى الثقة") }}</th>
                <th>{{ $t("الإحصائيات") }}</th>
                <th>{{ $t("الحالة") }}</th>
                <th v-if="canUpdateSource || canDeleteSource">{{ $t("الإجراءات") }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="source in sources" :key="source.id">
                <td>
                  <a :href="getFullUrl(source.domain)" target="_blank" class="text-decoration-none">
                    <strong>{{ source.domain }}</strong>
                  </a>
                  <div v-if="source.subdomains && source.subdomains.length > 0" class="small text-muted">
                    <i class="fas fa-sitemap me-1"></i> {{ $t("النطاقات الفرعية:") }} {{ source.subdomains.join(", ") }}
                  </div>
                </td>
                <td class="small">{{ truncateText(source.description, 70) }}</td>
                <td class="small">
                  <span class="badge bg-info">{{ getCategoryLabel(source.category) }}</span>
                </td>
                <td>
                  <div class="d-flex align-items-center">
                    <div class="trust-level-bar me-2"
                      :title="$t('مستوى الثقة: {level}%', { level: source.trust_level })">
                      <div class="trust-level-fill"
                        :style="{ width: `${source.trust_level}%`, backgroundColor: getTrustLevelColor(source.trust_level) }">
                      </div>
                    </div>
                    <span class="small">{{ source.trust_level }}%</span>
                  </div>
                </td>
                <td class="small">
                  <div
                    v-tooltip="$t('إجمالي النتائج: {total}, معدل النجاح: {rate}%', { total: source.total_results || 0, rate: source.success_rate || 0 })">
                    <i class="fas fa-chart-line me-1"></i> {{ $t("استخدام:") }} {{ source.usage_count || 0 }}
                  </div>
                </td>
                <td>
                  <span class="badge rounded-pill" :class="getStatusBadgeClass(source)"
                    @click="canUpdateSource && toggleSourceStatus(source)" v-tooltip="getStatusTooltip(source)">
                    {{ getStatusLabel(source) }}
                  </span>
                </td>
                <td v-if="canUpdateSource || canDeleteSource">
                  <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" @click="openEditSourceModal(source)" v-if="canUpdateSource"
                      v-tooltip="$t('تعديل')">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-outline-danger" @click="confirmDeleteSource(source)" v-if="canDeleteSource"
                      v-tooltip="$t('حذف')">
                      <i class="fas fa-trash"></i>
                    </button>
                    <button class="btn btn-outline-warning" @click="toggleBlacklist(source)" v-if="canUpdateSource"
                      v-tooltip="source.is_blacklisted ? $t('إزالة من القائمة السوداء') : $t('إضافة للقائمة السوداء')">
                      <i :class="source.is_blacklisted ? 'fas fa-check' : 'fas fa-ban'"></i>
                    </button>
                    <button class="btn btn-outline-info" @click="openVerifySourceModal(source)"
                      v-tooltip="$t('التحقق من المصدر')">
                      <i class="fas fa-shield-alt"></i>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="sources.length === 0">
                <td :colspan="canUpdateSource || canDeleteSource ? 7 : 6" class="text-center text-muted py-4">
                  {{ $t("لا توجد مصادر مطابقة للمعايير المحددة.") }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- ترقيم الصفحات -->
        <div v-if="!loading && totalSources > 0" class="d-flex justify-content-between align-items-center mt-3">
          <div class="text-muted small">
            {{ $t("عرض {start} إلى {end} من {total} مصدر", {
              start: (currentPage - 1) * pageSize + 1,
              end: Math.min(currentPage * pageSize, totalSources),
              total: totalSources
            }) }}
          </div>
          <nav aria-label="Page navigation">
            <ul class="pagination pagination-sm mb-0">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">&laquo;</a>
              </li>
              <li v-for="page in paginationPages" :key="page" class="page-item"
                :class="{ active: currentPage === page, disabled: page === '...' }">
                <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">&raquo;</a>
              </li>
            </ul>
          </nav>
          <div>
            <select class="form-select form-select-sm d-inline-block w-auto" v-model="pageSize"
              @change="changePageSize">
              <option value="10">10</option>
              <option value="25">25</option>
              <option value="50">50</option>
              <option value="100">100</option>
            </select>
            <span class="ms-2 text-muted small">{{ $t("عنصر لكل صفحة") }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- نافذة إضافة/تعديل مصدر -->
    <div class="modal fade" id="sourceModal" tabindex="-1" aria-labelledby="sourceModalLabel" aria-hidden="true"
      ref="sourceModalRef">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="sourceModalLabel">
              {{ isEditMode ? $t("تعديل مصدر") : $t("إضافة مصدر") }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveSource">
              <!-- الحقول الأساسية -->
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="domain" class="form-label">{{ $t("النطاق") }} <span class="text-danger">*</span></label>
                  <div class="input-group input-group-sm">
                    <span class="input-group-text">https://</span>
                    <input type="text" class="form-control" id="domain" v-model.trim="currentSource.domain" required
                      :disabled="isEditMode" />
                  </div>
                  <small class="form-text text-muted">{{ $t("مثال: example.com (بدون http:// أو https://)") }}</small>
                </div>
                <div class="col-md-6">
                  <label for="category" class="form-label">{{ $t("التصنيف") }} <span
                      class="text-danger">*</span></label>
                  <select class="form-select form-select-sm" id="category" v-model="currentSource.category" required>
                    <option v-for="category in sourceCategories" :key="category.value" :value="category.value">
                      {{ $t(category.label) }}
                    </option>
                  </select>
                </div>
              </div>

              <!-- الوصف والنطاقات الفرعية -->
              <div class="mb-3">
                <label for="description" class="form-label">{{ $t("الوصف") }}</label>
                <textarea class="form-control form-control-sm" id="description" v-model="currentSource.description"
                  rows="2"></textarea>
              </div>
              <div class="mb-3">
                <label for="subdomains" class="form-label">{{ $t("النطاقات الفرعية (افصل بفاصلة)") }}</label>
                <input type="text" class="form-control form-control-sm" id="subdomains" v-model="subdomainsInput" />
                <small class="form-text text-muted">{{ $t("مثال: blog.example.com, shop.example.com") }}</small>
              </div>

              <!-- مستوى الثقة والحالة -->
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="trust_level" class="form-label">{{ $t("مستوى الثقة") }} ({{ currentSource.trust_level
                  }}%)</label>
                  <input type="range" class="form-range" id="trust_level" v-model.number="currentSource.trust_level"
                    min="0" max="100" step="5" />
                  <div class="d-flex justify-content-between small text-muted">
                    <span>0%</span>
                    <span>50%</span>
                    <span>100%</span>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-check mb-2 mt-4">
                    <input class="form-check-input" type="checkbox" id="is_active" v-model="currentSource.is_active"
                      :disabled="currentSource.is_blacklisted" />
                    <label class="form-check-label" for="is_active">{{ $t("نشط") }}</label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="is_blacklisted"
                      v-model="currentSource.is_blacklisted" />
                    <label class="form-check-label" for="is_blacklisted">{{ $t("إضافة للقائمة السوداء") }}</label>
                  </div>
                </div>
              </div>

              <!-- ملاحظات وتوثيق -->
              <div class="mb-3">
                <label for="notes" class="form-label">{{ $t("ملاحظات") }}</label>
                <textarea class="form-control form-control-sm" id="notes" v-model="currentSource.notes"
                  rows="2"></textarea>
              </div>
              <div class="mb-3">
                <label for="verification_info" class="form-label">{{ $t("معلومات التحقق") }}</label>
                <textarea class="form-control form-control-sm" id="verification_info"
                  v-model="currentSource.verification_info" rows="2"></textarea>
                <small class="form-text text-muted">{{ $t("معلومات حول كيفية التحقق من موثوقية هذا المصدر") }}</small>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">{{ $t("إلغاء") }}</button>
            <button type="button" class="btn btn-primary btn-sm" @click="saveSource" :disabled="isSaving">
              <span v-if="isSaving" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              {{ isSaving ? $t("جاري الحفظ...") : $t("حفظ") }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- نافذة تأكيد الحذف -->
    <div class="modal fade" id="deleteConfirmModal" tabindex="-1" aria-labelledby="deleteConfirmModalLabel"
      aria-hidden="true" ref="deleteConfirmModalRef">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="deleteConfirmModalLabel">{{ $t("تأكيد الحذف") }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            {{ $t("هل أنت متأكد من رغبتك في حذف المصدر") }}: <strong>{{ currentSourceToDelete.domain }}</strong>؟
            <p class="text-danger small mt-2">{{ $t("سيؤدي هذا الإجراء إلى حذف المصدر نهائياً.") }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">{{ $t("إلغاء") }}</button>
            <button type="button" class="btn btn-danger btn-sm" @click="deleteSource" :disabled="isDeleting">
              <span v-if="isDeleting" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              {{ isDeleting ? $t("جاري الحذف...") : $t("حذف") }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- نافذة التحقق من المصدر -->
    <div class="modal fade" id="verifySourceModal" tabindex="-1" aria-labelledby="verifySourceModalLabel"
      aria-hidden="true" ref="verifySourceModalRef">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="verifySourceModalLabel">
              {{ $t("التحقق من المصدر:") }} <strong>{{ currentSourceToVerify.domain }}</strong>
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div v-if="verificationStatus.loading" class="text-center p-5">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">{{ $t("جاري التحميل...") }}</span>
              </div>
              <p class="mt-2">{{ $t("جاري التحقق من المصدر، يرجى الانتظار...") }}</p>
            </div>
            <div v-else-if="verificationStatus.error" class="alert alert-danger">
              {{ $t("حدث خطأ أثناء التحقق:") }} {{ verificationStatus.error }}
            </div>
            <div v-else-if="verificationStatus.result">
              <div class="card mb-3">
                <div class="card-header bg-light">
                  <h6 class="mb-0">{{ $t("معلومات المصدر") }}</h6>
                </div>
                <div class="card-body">
                  <div class="row">
                    <div class="col-md-6">
                      <p><strong>{{ $t("النطاق:") }}</strong> {{ verificationStatus.result.domain }}</p>
                      <p><strong>{{ $t("عنوان IP:") }}</strong> {{ verificationStatus.result.ip_address }}</p>
                      <p><strong>{{ $t("البلد:") }}</strong> {{ verificationStatus.result.country }}</p>
                      <p><strong>{{ $t("تاريخ التسجيل:") }}</strong> {{
                        formatDate(verificationStatus.result.registration_date) }}</p>
                    </div>
                    <div class="col-md-6">
                      <p><strong>{{ $t("مزود الاستضافة:") }}</strong> {{ verificationStatus.result.hosting_provider }}
                      </p>
                      <p><strong>{{ $t("شهادة SSL:") }}</strong>
                        <span :class="verificationStatus.result.has_ssl ? 'text-success' : 'text-danger'">
                          {{ verificationStatus.result.has_ssl ? $t("متوفرة") : $t("غير متوفرة") }}
                        </span>
                      </p>
                      <p><strong>{{ $t("عمر الموقع:") }}</strong> {{ verificationStatus.result.site_age }}</p>
                      <p><strong>{{ $t("تصنيف أليكسا:") }}</strong> {{ verificationStatus.result.alexa_rank || $t("غير
                        متوفر") }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div class="card mb-3">
                <div class="card-header bg-light">
                  <h6 class="mb-0">{{ $t("نتائج التحقق") }}</h6>
                </div>
                <div class="card-body">
                  <div class="row">
                    <div class="col-md-6">
                      <div class="mb-2">
                        <span class="badge"
                          :class="verificationStatus.result.security_score >= 70 ? 'bg-success' : verificationStatus.result.security_score >= 40 ? 'bg-warning text-dark' : 'bg-danger'">
                          {{ $t("درجة الأمان:") }} {{ verificationStatus.result.security_score }}/100
                        </span>
                      </div>
                      <ul class="list-group list-group-flush small">
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                          {{ $t("قائمة سوداء للبريد المزعج") }}
                          <i
                            :class="verificationStatus.result.spam_blacklist ? 'fas fa-times text-danger' : 'fas fa-check text-success'"></i>
                        </li>
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                          {{ $t("قائمة سوداء للبرمجيات الخبيثة") }}
                          <i
                            :class="verificationStatus.result.malware_blacklist ? 'fas fa-times text-danger' : 'fas fa-check text-success'"></i>
                        </li>
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                          {{ $t("سياسة الخصوصية") }}
                          <i
                            :class="verificationStatus.result.has_privacy_policy ? 'fas fa-check text-success' : 'fas fa-times text-danger'"></i>
                        </li>
                      </ul>
                    </div>
                    <div class="col-md-6">
                      <div class="mb-2">
                        <span class="badge"
                          :class="verificationStatus.result.content_score >= 70 ? 'bg-success' : verificationStatus.result.content_score >= 40 ? 'bg-warning text-dark' : 'bg-danger'">
                          {{ $t("درجة المحتوى:") }} {{ verificationStatus.result.content_score }}/100
                        </span>
                      </div>
                      <ul class="list-group list-group-flush small">
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                          {{ $t("محتوى أصلي") }}
                          <i
                            :class="verificationStatus.result.original_content ? 'fas fa-check text-success' : 'fas fa-times text-danger'"></i>
                        </li>
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                          {{ $t("مراجع علمية") }}
                          <i
                            :class="verificationStatus.result.has_citations ? 'fas fa-check text-success' : 'fas fa-times text-danger'"></i>
                        </li>
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                          {{ $t("معلومات الاتصال") }}
                          <i
                            :class="verificationStatus.result.has_contact_info ? 'fas fa-check text-success' : 'fas fa-times text-danger'"></i>
                        </li>
                      </ul>
                    </div>
                  </div>

                  <div class="alert alert-info mt-3">
                    <h6>{{ $t("التوصية:") }}</h6>
                    <p>{{ verificationStatus.result.recommendation }}</p>
                    <div class="d-flex align-items-center">
                      <span class="me-2">{{ $t("مستوى الثقة المقترح:") }}</span>
                      <div class="trust-level-bar me-2" style="width: 200px;">
                        <div class="trust-level-fill"
                          :style="{ width: `${verificationStatus.result.suggested_trust_level}%`, backgroundColor: getTrustLevelColor(verificationStatus.result.suggested_trust_level) }">
                        </div>
                      </div>
                      <span>{{ verificationStatus.result.suggested_trust_level }}%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="alert alert-warning">
              {{ $t("لم يتم إجراء التحقق بعد. اضغط على زر 'بدء التحقق' للبدء.") }}
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">{{ $t("إغلاق") }}</button>
            <button type="button" class="btn btn-info btn-sm" @click="startSourceVerification"
              :disabled="verificationStatus.loading">
              <span v-if="verificationStatus.loading" class="spinner-border spinner-border-sm" role="status"
                aria-hidden="true"></span>
              {{ verificationStatus.loading ? $t("جاري التحقق...") : $t("بدء التحقق") }}
            </button>
            <button type="button" class="btn btn-success btn-sm" @click="applyVerificationResults"
              :disabled="!verificationStatus.result || verificationStatus.loading">
              {{ $t("تطبيق النتائج") }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Replace role="status" with output -->
    <output class="status-message" v-if="statusMessage">{{ statusMessage }}</output>

    <!-- Other status messages -->
    <output class="error-message" v-if="errorMessage">{{ errorMessage }}</output>
    <output class="success-message" v-if="successMessage">{{ successMessage }}</output>
    <output class="warning-message" v-if="warningMessage">{{ warningMessage }}</output>
    <output class="info-message" v-if="infoMessage">{{ infoMessage }}</output>
  </div>
</template>

<script>
import { ref, computed, onMounted, reactive, watch } from "vue";
import { useToast } from "vue-toastification";
import axios from "axios";
import { Modal } from "bootstrap";
import _ from "lodash";
import { useI18n } from "vue-i18n";
import { VTooltip } from "v-tooltip"; // Assuming v-tooltip is globally registered or imported

// Import API service (adjust path as needed)
import SourceApiService from "../services/SourceApiService";
import PermissionService from "../services/PermissionService"; // Service to check permissions

export default {
  name: "SourceManager",
  directives: {
    tooltip: VTooltip, // Register directive locally if needed
  },
  setup() {
    const toast = useToast();
    const { t } = useI18n();

    // --- State Variables ---
    const sources = ref([]);
    const totalSources = ref(0);
    const currentPage = ref(1);
    const pageSize = ref(10);
    const loading = ref(false);
    const error = ref(null);
    const isEditMode = ref(false);
    const isSaving = ref(false);
    const isDeleting = ref(false);

    const sourceModal = ref(null);
    const deleteConfirmModal = ref(null);
    const verifySourceModal = ref(null);
    const sourceModalRef = ref(null);
    const deleteConfirmModalRef = ref(null);
    const verifySourceModalRef = ref(null);

    const currentSource = reactive({
      id: null,
      domain: "",
      description: "",
      category: "ACADEMIC",
      trust_level: 50,
      subdomains: [],
      is_active: true,
      is_blacklisted: false,
      notes: "",
      verification_info: ""
    });

    const currentSourceToDelete = reactive({ id: null, domain: "" });
    const currentSourceToVerify = reactive({ id: null, domain: "" });
    const subdomainsInput = ref("");

    const verificationStatus = reactive({
      loading: false,
      result: null,
      error: null
    });

    const filters = reactive({
      domain: "",
      trustLevel: "",
      category: "",
      status: "",
      sortBy: "domain",
      sortOrder: "asc",
    });

    // --- Permissions ---
    const permissions = reactive({
      canReadSource: false,
      canCreateSource: false,
      canUpdateSource: false,
      canDeleteSource: false,
      canVerifySource: false,
    });

    const canCreateSource = computed(() => permissions.canCreateSource);
    const canUpdateSource = computed(() => permissions.canUpdateSource);
    const canDeleteSource = computed(() => permissions.canDeleteSource);

    // --- Static Data ---
    const trustLevels = [
      { value: "high", label: "ثقة عالية (75-100%)", min: 75, max: 100 },
      { value: "medium", label: "ثقة متوسطة (50-74%)", min: 50, max: 74 },
      { value: "low", label: "ثقة منخفضة (25-49%)", min: 25, max: 49 },
      { value: "untrusted", label: "غير موثوق (0-24%)", min: 0, max: 24 }
    ];

    const sourceCategories = [
      { value: "ACADEMIC", label: "أكاديمي" },
      { value: "GOVERNMENT", label: "حكومي" },
      { value: "RESEARCH", label: "بحثي" },
      { value: "EDUCATIONAL", label: "تعليمي" },
      { value: "COMMERCIAL", label: "تجاري" },
      { value: "NEWS", label: "إخباري" },
      { value: "BLOG", label: "مدونة" },
      { value: "FORUM", label: "منتدى" },
      { value: "SOCIAL_MEDIA", label: "وسائل التواصل الاجتماعي" },
      { value: "OTHER", label: "أخرى" }
    ];

    // --- Computed Properties ---
    const totalPages = computed(() => {
      return Math.ceil(totalSources.value / pageSize.value);
    });

    const paginationPages = computed(() => {
      const pages = [];
      const maxPagesToShow = 5; // Show 5 page numbers max
      const halfMaxPages = Math.floor(maxPagesToShow / 2);
      let startPage = Math.max(1, currentPage.value - halfMaxPages);
      let endPage = Math.min(totalPages.value, currentPage.value + halfMaxPages);

      if (currentPage.value <= halfMaxPages) {
        endPage = Math.min(totalPages.value, maxPagesToShow);
      }
      if (currentPage.value + halfMaxPages >= totalPages.value) {
        startPage = Math.max(1, totalPages.value - maxPagesToShow + 1);
      }

      if (startPage > 1) {
        pages.push(1);
        if (startPage > 2) {
          pages.push("...");
        }
      }

      for (let i = startPage; i <= endPage; i++) {
        pages.push(i);
      }

      if (endPage < totalPages.value) {
        if (endPage < totalPages.value - 1) {
          pages.push("...");
        }
        pages.push(totalPages.value);
      }
      return pages;
    });

    // --- Methods ---
    const fetchPermissions = async () => {
      try {
        // Replace with actual permission fetching logic
        permissions.canReadSource = await PermissionService.hasPermission("read", "source");
        permissions.canCreateSource = await PermissionService.hasPermission("create", "source");
        permissions.canUpdateSource = await PermissionService.hasPermission("update", "source");
        permissions.canDeleteSource = await PermissionService.hasPermission("delete", "source");
        permissions.canVerifySource = await PermissionService.hasPermission("verify", "source");

        if (!permissions.canReadSource) {
          error.value = t("ليس لديك صلاحية عرض المصادر.");
          toast.error(error.value);
        }
      } catch (err) {
        console.error("Error fetching permissions:", err);
        error.value = t("خطأ في تحميل الصلاحيات.");
        toast.error(error.value);
      }
    };

    const fetchSources = async () => {
      if (!permissions.canReadSource) return;
      loading.value = true;
      error.value = null;
      try {
        const params = {
          skip: (currentPage.value - 1) * pageSize.value,
          limit: pageSize.value,
          domain: filters.domain || undefined,
          category: filters.category || undefined,
          sort_by: filters.sortBy,
          sort_order: filters.sortOrder,
        };

        // Handle trust level filter
        if (filters.trustLevel) {
          const level = trustLevels.find(l => l.value === filters.trustLevel);
          if (level) {
            params.trust_level_min = level.min;
            params.trust_level_max = level.max;
          }
        }

        // Handle status filter
        if (filters.status === "active") {
          params.is_active = true;
          params.is_blacklisted = false;
        } else if (filters.status === "inactive") {
          params.is_active = false;
          params.is_blacklisted = false;
        } else if (filters.status === "blacklisted") {
          params.is_blacklisted = true;
        }

        const response = await SourceApiService.getSources(params);
        sources.value = response.data.sources;
        totalSources.value = response.data.total_count;
      } catch (err) {
        console.error("Error fetching sources:", err);
        error.value = err.response?.data?.detail || err.message || t("خطأ غير معروف");
        toast.error(`${t("فشل تحميل المصادر:")} ${error.value}`);
      } finally {
        loading.value = false;
      }
    };

    const debouncedFetchSources = _.debounce(fetchSources, 500);

    const resetCurrentSource = () => {
      currentSource.id = null;
      currentSource.domain = "";
      currentSource.description = "";
      currentSource.category = "ACADEMIC";
      currentSource.trust_level = 50;
      currentSource.subdomains = [];
      currentSource.is_active = true;
      currentSource.is_blacklisted = false;
      currentSource.notes = "";
      currentSource.verification_info = "";
      subdomainsInput.value = "";
    };

    const openAddSourceModal = () => {
      if (!permissions.canCreateSource) {
        toast.error(t("ليس لديك صلاحية إضافة مصادر."));
        return;
      }
      isEditMode.value = false;
      resetCurrentSource();
      sourceModal.value.show();
    };

    const openEditSourceModal = (source) => {
      if (!permissions.canUpdateSource) {
        toast.error(t("ليس لديك صلاحية تعديل المصادر."));
        return;
      }
      isEditMode.value = true;
      Object.assign(currentSource, source);
      // Handle arrays for subdomains
      currentSource.subdomains = Array.isArray(source.subdomains) ? source.subdomains : [];
      subdomainsInput.value = currentSource.subdomains.join(", ");
      sourceModal.value.show();
    };

    const saveSource = async () => {
      if (isSaving.value) return;
      isSaving.value = true;

      // Prepare data
      const sourceData = { ...currentSource };
      sourceData.subdomains = subdomainsInput.value.split(",").map(s => s.trim()).filter(s => s);

      // Ensure domain doesn't have protocol
      sourceData.domain = sourceData.domain.replace(/^https?:\/\//, "");

      // If blacklisted, ensure it's not active
      if (sourceData.is_blacklisted) {
        sourceData.is_active = false;
      }

      try {
        if (isEditMode.value) {
          if (!permissions.canUpdateSource) throw new Error(t("ليس لديك صلاحية التعديل."));
          await SourceApiService.updateSource(currentSource.id, sourceData);
          toast.success(t("تم تحديث المصدر بنجاح!"));
        } else {
          if (!permissions.canCreateSource) throw new Error(t("ليس لديك صلاحية الإنشاء."));
          await SourceApiService.createSource(sourceData);
          toast.success(t("تمت إضافة المصدر بنجاح!"));
        }
        sourceModal.value.hide();
        fetchSources(); // Refresh the list
      } catch (err) {
        console.error("Error saving source:", err);
        const errorMsg = err.response?.data?.detail || err.message || t("خطأ غير معروف");
        toast.error(`${t("فشل حفظ المصدر:")} ${errorMsg}`);
      } finally {
        isSaving.value = false;
      }
    };

    const confirmDeleteSource = (source) => {
      if (!permissions.canDeleteSource) {
        toast.error(t("ليس لديك صلاحية حذف المصادر."));
        return;
      }
      currentSourceToDelete.id = source.id;
      currentSourceToDelete.domain = source.domain;
      deleteConfirmModal.value.show();
    };

    const deleteSource = async () => {
      if (isDeleting.value || !currentSourceToDelete.id) return;
      if (!permissions.canDeleteSource) {
        toast.error(t("ليس لديك صلاحية الحذف."));
        deleteConfirmModal.value.hide();
        return;
      }
      isDeleting.value = true;
      try {
        await SourceApiService.deleteSource(currentSourceToDelete.id);
        toast.success(t("تم حذف المصدر بنجاح!"));
        deleteConfirmModal.value.hide();
        // Adjust pagination if the last item on a page was deleted
        if (sources.value.length === 1 && currentPage.value > 1) {
          currentPage.value--;
        }
        fetchSources(); // Refresh the list
      } catch (err) {
        console.error("Error deleting source:", err);
        const errorMsg = err.response?.data?.detail || err.message || t("خطأ غير معروف");
        toast.error(`${t("فشل حذف المصدر:")} ${errorMsg}`);
      } finally {
        isDeleting.value = false;
      }
    };

    const toggleSourceStatus = async (source) => {
      if (!permissions.canUpdateSource) {
        toast.error(t("ليس لديك صلاحية تعديل حالة المصادر."));
        return;
      }

      // Cannot activate a blacklisted source
      if (source.is_blacklisted && !source.is_active) {
        toast.warning(t("لا يمكن تنشيط مصدر في القائمة السوداء. قم بإزالته من القائمة السوداء أولاً."));
        return;
      }

      const newStatus = !source.is_active;
      try {
        await SourceApiService.updateSource(source.id, { is_active: newStatus });
        toast.success(t("تم تحديث حالة المصدر بنجاح!"));
        fetchSources(); // Refresh the list
      } catch (err) {
        console.error("Error toggling source status:", err);
        const errorMsg = err.response?.data?.detail || err.message || t("خطأ غير معروف");
        toast.error(`${t("فشل تحديث حالة المصدر:")} ${errorMsg}`);
      }
    };

    const toggleBlacklist = async (source) => {
      if (!permissions.canUpdateSource) {
        toast.error(t("ليس لديك صلاحية تعديل حالة المصادر."));
        return;
      }

      const newBlacklistStatus = !source.is_blacklisted;
      const updateData = { is_blacklisted: newBlacklistStatus };

      // If adding to blacklist, also set inactive
      if (newBlacklistStatus) {
        updateData.is_active = false;
      }

      try {
        await SourceApiService.updateSource(source.id, updateData);
        toast.success(newBlacklistStatus
          ? t("تمت إضافة المصدر إلى القائمة السوداء بنجاح!")
          : t("تمت إزالة المصدر من القائمة السوداء بنجاح!")
        );
        fetchSources(); // Refresh the list
      } catch (err) {
        console.error("Error toggling blacklist status:", err);
        const errorMsg = err.response?.data?.detail || err.message || t("خطأ غير معروف");
        toast.error(`${t("فشل تحديث حالة القائمة السوداء:")} ${errorMsg}`);
      }
    };

    const openVerifySourceModal = (source) => {
      if (!permissions.canVerifySource) {
        toast.error(t("ليس لديك صلاحية التحقق من المصادر."));
        return;
      }
      currentSourceToVerify.id = source.id;
      currentSourceToVerify.domain = source.domain;
      verificationStatus.result = null;
      verificationStatus.error = null;
      verifySourceModal.value.show();
    };

    const startSourceVerification = async () => {
      if (!permissions.canVerifySource || verificationStatus.loading || !currentSourceToVerify.id) return;

      verificationStatus.loading = true;
      verificationStatus.result = null;
      verificationStatus.error = null;

      try {
        // Call API to verify source
        const response = await SourceApiService.verifySource(currentSourceToVerify.id);
        verificationStatus.result = response.data;
      } catch (err) {
        console.error("Error verifying source:", err);
        verificationStatus.error = err.response?.data?.detail || err.message || t("خطأ غير معروف");
        toast.error(`${t("فشل التحقق من المصدر:")} ${verificationStatus.error}`);
      } finally {
        verificationStatus.loading = false;
      }
    };

    const applyVerificationResults = async () => {
      if (!permissions.canUpdateSource || !verificationStatus.result || !currentSourceToVerify.id) return;

      try {
        // Apply suggested trust level to the source
        await SourceApiService.updateSource(currentSourceToVerify.id, {
          trust_level: verificationStatus.result.suggested_trust_level,
          verification_info: verificationStatus.result.recommendation
        });
        toast.success(t("تم تطبيق نتائج التحقق بنجاح!"));
        verifySourceModal.value.hide();
        fetchSources(); // Refresh the list
      } catch (err) {
        console.error("Error applying verification results:", err);
        const errorMsg = err.response?.data?.detail || err.message || t("خطأ غير معروف");
        toast.error(`${t("فشل تطبيق نتائج التحقق:")} ${errorMsg}`);
      }
    };

    const changePage = (page) => {
      if (page >= 1 && page <= totalPages.value && page !== currentPage.value && page !== "...") {
        currentPage.value = page;
        fetchSources();
      }
    };

    const changePageSize = () => {
      currentPage.value = 1; // Reset to first page when page size changes
      fetchSources();
    };

    const truncateText = (text, length) => {
      if (!text) return "";
      return text.length > length ? text.substring(0, length) + "..." : text;
    };

    const getCategoryLabel = (value) => {
      const category = sourceCategories.find(c => c.value === value);
      return category ? t(category.label) : t("غير محدد");
    };

    const getTrustLevelColor = (level) => {
      if (level >= 75) return "#28a745"; // Green for high trust
      if (level >= 50) return "#17a2b8"; // Blue for medium trust
      if (level >= 25) return "#ffc107"; // Yellow for low trust
      return "#dc3545"; // Red for untrusted
    };

    const getStatusBadgeClass = (source) => {
      if (source.is_blacklisted) return "bg-danger";
      return source.is_active ? "bg-success-light text-success" : "bg-warning-light text-warning";
    };

    const getStatusLabel = (source) => {
      if (source.is_blacklisted) return t("القائمة السوداء");
      return source.is_active ? t("نشط") : t("غير نشط");
    };

    const getStatusTooltip = (source) => {
      if (source.is_blacklisted) return t("مصدر في القائمة السوداء");
      return source.is_active ? t("تعطيل المصدر") : t("تفعيل المصدر");
    };

    const getFullUrl = (domain) => {
      return `https://${domain}`;
    };

    const formatDate = (dateString) => {
      if (!dateString) return t("غير متوفر");
      return new Date(dateString).toLocaleDateString();
    };

    // --- Lifecycle Hooks ---
    onMounted(async () => {
      await fetchPermissions();
      if (permissions.canReadSource) {
        fetchSources();
      }
      // Initialize Bootstrap modals
      if (sourceModalRef.value) {
        sourceModal.value = new Modal(sourceModalRef.value);
      }
      if (deleteConfirmModalRef.value) {
        deleteConfirmModal.value = new Modal(deleteConfirmModalRef.value);
      }
      if (verifySourceModalRef.value) {
        verifySourceModal.value = new Modal(verifySourceModalRef.value);
      }
    });

    // --- Watchers ---
    watch(() => currentSource.is_blacklisted, (newValue) => {
      if (newValue) {
        currentSource.is_active = false;
      }
    });

    return {
      sources,
      totalSources,
      currentPage,
      pageSize,
      totalPages,
      paginationPages,
      loading,
      error,
      isEditMode,
      isSaving,
      isDeleting,
      currentSource,
      currentSourceToDelete,
      currentSourceToVerify,
      subdomainsInput,
      verificationStatus,
      filters,
      trustLevels,
      sourceCategories,
      sourceModalRef,
      deleteConfirmModalRef,
      verifySourceModalRef,
      canCreateSource,
      canUpdateSource,
      canDeleteSource,
      fetchSources,
      debouncedFetchSources,
      openAddSourceModal,
      openEditSourceModal,
      saveSource,
      confirmDeleteSource,
      deleteSource,
      toggleSourceStatus,
      toggleBlacklist,
      openVerifySourceModal,
      startSourceVerification,
      applyVerificationResults,
      changePage,
      changePageSize,
      truncateText,
      getCategoryLabel,
      getTrustLevelColor,
      getStatusBadgeClass,
      getStatusLabel,
      getStatusTooltip,
      getFullUrl,
      formatDate,
      t, // Make t available in the template
    };
  },
};
</script>

<style scoped>
.source-manager {
  font-size: 0.9rem;
}

.card-header h5 {
  font-weight: 600;
}

.table th {
  font-weight: 600;
  background-color: #f8f9fa;
  font-size: 0.85rem;
}

.table td {
  vertical-align: middle;
}

.badge {
  font-size: 0.75rem;
  padding: 0.3em 0.6em;
}

.cursor-pointer {
  cursor: pointer;
}

.bg-success-light {
  background-color: rgba(40, 167, 69, 0.1);
}

.bg-warning-light {
  background-color: rgba(255, 193, 7, 0.1);
}

.bg-danger-light {
  background-color: rgba(220, 53, 69, 0.1);
}

.trust-level-bar {
  height: 8px;
  width: 100px;
  background-color: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.trust-level-fill {
  height: 100%;
  border-radius: 4px;
}

/* Add custom styles for tooltips if needed */
[v-tooltip] {
  cursor: help;
}
</style>
