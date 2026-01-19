# /home/ubuntu/image_search_integration/auto_learning/frontend/KeywordManager.vue

"""
مكون Vue لإدارة الكلمات المفتاحية المتقدمة للبحث الذاتي الذكي

هذا المكون يوفر واجهة رسومية لإدارة الكلمات المفتاحية، بما في ذلك:
- عرض الكلمات المفتاحية مع فلاتر بحث متقدمة وترقيم الصفحات.
- إضافة وتعديل وحذف الكلمات المفتاحية.
- دعم التصنيف المتقدم (جزء النبات، نوع الإصابة، ربط بإصابة محددة).
- إدارة العلاقات الدلالية (مرادفات، كلمات ذات صلة).
- عرض إحصائيات أداء الكلمات المفتاحية.
- تشغيل بحث فوري باستخدام كلمة مفتاحية.
- التحكم في حالة النشاط.
- التكامل مع نظام الصلاحيات.
"""

<template>
  <div class="keyword-manager">
    <div class="card shadow-sm">
      <div class="card-header bg-light d-flex justify-content-between align-items-center py-3">
        <h5 class="mb-0 text-primary"><i class="fas fa-key me-2"></i>{{ $t("إدارة الكلمات المفتاحية") }}</h5>
        <button 
          class="btn btn-primary btn-sm rounded-pill px-3" 
          @click="openAddKeywordModal" 
          v-if="canCreateKeyword"
        >
          <i class="fas fa-plus me-1"></i> {{ $t("إضافة كلمة مفتاحية") }}
        </button>
      </div>
      <div class="card-body">
        <!-- فلاتر البحث المتقدمة -->
        <div class="row g-3 mb-4 align-items-center bg-light p-3 rounded">
          <div class="col-md-3">
            <div class="input-group input-group-sm">
              <span class="input-group-text bg-white border-end-0"><i class="fas fa-search text-muted"></i></span>
              <input 
                type="text" 
                class="form-control border-start-0" 
                v-model="filters.keyword" 
                :placeholder="$t("بحث بالكلمة أو الوصف...")" 
                @input="debouncedFetchKeywords"
              />
            </div>
          </div>
          <div class="col-md-2">
            <select class="form-select form-select-sm" v-model="filters.plantPart" @change="fetchKeywords">
              <option value="">{{ $t("كل أجزاء النبات") }}</option>
              <option v-for="part in plantParts" :key="part.value" :value="part.value">
                {{ $t(part.label) }}
              </option>
            </select>
          </div>
          <div class="col-md-2">
            <select class="form-select form-select-sm" v-model="filters.conditionType" @change="fetchKeywords">
              <option value="">{{ $t("كل أنواع الإصابات") }}</option>
              <option v-for="type in conditionTypes" :key="type.value" :value="type.value">
                {{ $t(type.label) }}
              </option>
            </select>
          </div>
          <div class="col-md-2">
            <select class="form-select form-select-sm" v-model="filters.status" @change="fetchKeywords">
              <option value="">{{ $t("كل الحالات") }}</option>
              <option value="active">{{ $t("نشط") }}</option>
              <option value="inactive">{{ $t("غير نشط") }}</option>
            </select>
          </div>
          <div class="col-md-2">
            <select class="form-select form-select-sm" v-model="filters.sortBy" @change="fetchKeywords">
              <option value="keyword">{{ $t("ترتيب حسب الكلمة") }}</option>
              <option value="created_at">{{ $t("ترتيب حسب تاريخ الإنشاء") }}</option>
              <option value="usage_count">{{ $t("ترتيب حسب الاستخدام") }}</option>
              <option value="performance_score">{{ $t("ترتيب حسب الأداء") }}</option>
            </select>
          </div>
          <div class="col-md-1">
            <select class="form-select form-select-sm" v-model="filters.sortOrder" @change="fetchKeywords">
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
          {{ $t("حدث خطأ أثناء تحميل الكلمات المفتاحية:") }} {{ error }}
        </div>

        <!-- جدول الكلمات المفتاحية -->
        <div v-else class="table-responsive">
          <table class="table table-striped table-hover table-sm align-middle">
            <thead class="table-light">
              <tr>
                <th>{{ $t("الكلمة المفتاحية") }}</th>
                <th>{{ $t("الوصف") }}</th>
                <th>{{ $t("التصنيف") }}</th>
                <th>{{ $t("الربط") }}</th>
                <th>{{ $t("الجدول") }}</th>
                <th>{{ $t("الأداء") }}</th>
                <th>{{ $t("الحالة") }}</th>
                <th v-if="canUpdateKeyword || canDeleteKeyword">{{ $t("الإجراءات") }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="keyword in keywords" :key="keyword.id">
                <td>
                  <strong>{{ keyword.keyword }}</strong>
                  <div v-if="keyword.synonyms && keyword.synonyms.length > 0" class="small text-muted">
                    <i class="fas fa-tags me-1"></i> {{ $t("مرادفات:") }} {{ keyword.synonyms.join(", ") }}
                  </div>
                </td>
                <td class="small">{{ truncateText(keyword.description, 70) }}</td>
                <td class="small">
                  <span v-if="keyword.plant_part" class="badge bg-info me-1">{{ getPlantPartLabel(keyword.plant_part) }}</span>
                  <span v-if="keyword.condition_type" class="badge bg-warning text-dark">{{ getConditionTypeLabel(keyword.condition_type) }}</span>
                </td>
                <td class="small">
                  <span v-if="keyword.condition_id">{{ $t("إصابة:") }} {{ getConditionName(keyword.condition_id) }}</span>
                  <span v-else class="text-muted">{{ $t("غير مرتبط") }}</span>
                </td>
                <td class="small">{{ keyword.schedule ? keyword.schedule.name : $t("بدون جدول") }}</td>
                <td class="small text-center">
                  <span 
                    class="badge rounded-pill"
                    :class="getPerformanceBadgeClass(keyword.performance_score)"
                    v-tooltip="`${$t("الاستخدام:")} ${keyword.usage_count || 0}, ${$t("النجاح:")} ${keyword.success_rate || 0}%`"
                  >
                    {{ keyword.performance_score ? keyword.performance_score.toFixed(1) : $t("لا يوجد") }}
                  </span>
                </td>
                <td>
                  <span 
                    class="badge rounded-pill cursor-pointer"
                    :class="keyword.is_active ? "bg-success-light text-success" : "bg-danger-light text-danger""
                    @click="canUpdateKeyword && toggleKeywordStatus(keyword)"
                    v-tooltip="keyword.is_active ? $t("تعطيل") : $t("تفعيل")"
                  >
                    {{ keyword.is_active ? $t("نشط") : $t("غير نشط") }}
                  </span>
                </td>
                <td v-if="canUpdateKeyword || canDeleteKeyword">
                  <div class="btn-group btn-group-sm">
                    <button 
                      class="btn btn-outline-primary" 
                      @click="openEditKeywordModal(keyword)" 
                      v-if="canUpdateKeyword"
                      v-tooltip="$t("تعديل")"
                    >
                      <i class="fas fa-edit"></i>
                    </button>
                    <button 
                      class="btn btn-outline-danger" 
                      @click="confirmDeleteKeyword(keyword)" 
                      v-if="canDeleteKeyword"
                      v-tooltip="$t("حذف")"
                    >
                      <i class="fas fa-trash"></i>
                    </button>
                    <button 
                      class="btn btn-outline-info" 
                      @click="runImmediateSearch(keyword)"
                      v-tooltip="$t("بحث فوري")"
                    >
                      <i class="fas fa-search"></i>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="keywords.length === 0">
                <td :colspan="canUpdateKeyword || canDeleteKeyword ? 8 : 7" class="text-center text-muted py-4">
                  {{ $t("لا توجد كلمات مفتاحية مطابقة للمعايير المحددة.") }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- ترقيم الصفحات -->
        <div v-if="!loading && totalKeywords > 0" class="d-flex justify-content-between align-items-center mt-3">
          <div class="text-muted small">
            {{ $t("عرض {start} إلى {end} من {total} كلمة مفتاحية", { 
              start: (currentPage - 1) * pageSize + 1, 
              end: Math.min(currentPage * pageSize, totalKeywords), 
              total: totalKeywords 
            }) }}
          </div>
          <nav aria-label="Page navigation">
            <ul class="pagination pagination-sm mb-0">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">&laquo;</a>
              </li>
              <li v-for="page in paginationPages" :key="page" class="page-item" :class="{ active: currentPage === page, disabled: page === "..." }">
                <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">&raquo;</a>
              </li>
            </ul>
          </nav>
          <div>
            <select class="form-select form-select-sm d-inline-block w-auto" v-model="pageSize" @change="changePageSize">
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

    <!-- نافذة إضافة/تعديل كلمة مفتاحية -->
    <div class="modal fade" id="keywordModal" tabindex="-1" aria-labelledby="keywordModalLabel" aria-hidden="true" ref="keywordModalRef">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="keywordModalLabel">
              {{ isEditMode ? $t("تعديل كلمة مفتاحية") : $t("إضافة كلمة مفتاحية") }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveKeyword">
              <!-- الحقول الأساسية -->
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="keyword" class="form-label">{{ $t("الكلمة المفتاحية") }} <span class="text-danger">*</span></label>
                  <input type="text" class="form-control form-control-sm" id="keyword" v-model.trim="currentKeyword.keyword" required />
                </div>
                <div class="col-md-6">
                  <label for="schedule" class="form-label">{{ $t("الجدول") }}</label>
                  <select class="form-select form-select-sm" id="schedule" v-model="currentKeyword.schedule_id">
                    <option :value="null">{{ $t("بدون جدول") }}</option>
                    <option v-for="schedule in schedules" :key="schedule.id" :value="schedule.id">
                      {{ schedule.name }}
                    </option>
                  </select>
                </div>
              </div>
              
              <!-- التصنيف -->
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="plant_part" class="form-label">{{ $t("جزء النبات") }}</label>
                  <select class="form-select form-select-sm" id="plant_part" v-model="currentKeyword.plant_part">
                    <option :value="null">{{ $t("غير محدد") }}</option>
                    <option v-for="part in plantParts" :key="part.value" :value="part.value">
                      {{ $t(part.label) }}
                    </option>
                  </select>
                </div>
                <div class="col-md-6">
                  <label for="condition_type" class="form-label">{{ $t("نوع الإصابة") }}</label>
                  <select class="form-select form-select-sm" id="condition_type" v-model="currentKeyword.condition_type">
                    <option :value="null">{{ $t("غير محدد") }}</option>
                    <option v-for="type in conditionTypes" :key="type.value" :value="type.value">
                      {{ $t(type.label) }}
                    </option>
                  </select>
                </div>
              </div>
              
              <!-- الوصف والربط -->
              <div class="mb-3">
                <label for="description" class="form-label">{{ $t("الوصف") }}</label>
                <textarea class="form-control form-control-sm" id="description" v-model="currentKeyword.description" rows="2"></textarea>
              </div>
              <div class="mb-3">
                <label for="condition_id" class="form-label">{{ $t("ربط بإصابة محددة") }}</label>
                <select class="form-select form-select-sm" id="condition_id" v-model="currentKeyword.condition_id">
                  <option :value="null">{{ $t("بدون ربط") }}</option>
                  <option v-for="condition in conditions" :key="condition.id" :value="condition.id">
                    {{ condition.name }}
                  </option>
                </select>
              </div>
              
              <!-- العلاقات الدلالية -->
              <div class="row mb-3">
                 <div class="col-md-6">
                   <label for="synonyms" class="form-label">{{ $t("مرادفات (افصل بفاصلة)") }}</label>
                   <input type="text" class="form-control form-control-sm" id="synonyms" v-model="synonymsInput" />
                 </div>
                 <div class="col-md-6">
                   <label for="related_keywords" class="form-label">{{ $t("كلمات ذات صلة (افصل بفاصلة)") }}</label>
                   <input type="text" class="form-control form-control-sm" id="related_keywords" v-model="relatedKeywordsInput" />
                 </div>
              </div>
              
              <!-- الحالة -->
              <div class="form-check mb-3">
                <input class="form-check-input" type="checkbox" id="is_active" v-model="currentKeyword.is_active" />
                <label class="form-check-label" for="is_active">{{ $t("نشط") }}</label>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">{{ $t("إلغاء") }}</button>
            <button type="button" class="btn btn-primary btn-sm" @click="saveKeyword" :disabled="isSaving">
              <span v-if="isSaving" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              {{ isSaving ? $t("جاري الحفظ...") : $t("حفظ") }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- نافذة تأكيد الحذف -->
    <div class="modal fade" id="deleteConfirmModal" tabindex="-1" aria-labelledby="deleteConfirmModalLabel" aria-hidden="true" ref="deleteConfirmModalRef">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="deleteConfirmModalLabel">{{ $t("تأكيد الحذف") }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            {{ $t("هل أنت متأكد من رغبتك في حذف الكلمة المفتاحية") }}: <strong>{{ currentKeywordToDelete.keyword }}</strong>؟
            <p class="text-danger small mt-2">{{ $t("سيؤدي هذا الإجراء إلى حذف الكلمة المفتاحية نهائياً.") }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">{{ $t("إلغاء") }}</button>
            <button type="button" class="btn btn-danger btn-sm" @click="deleteKeyword" :disabled="isDeleting">
              <span v-if="isDeleting" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              {{ isDeleting ? $t("جاري الحذف...") : $t("حذف") }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- نافذة نتائج البحث الفوري -->
    <div class="modal fade" id="searchResultsModal" tabindex="-1" aria-labelledby="searchResultsModalLabel" aria-hidden="true" ref="searchResultsModalRef">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="searchResultsModalLabel">
              {{ $t("نتائج البحث الفوري عن:") }} <strong class="text-primary">{{ currentKeywordForSearch.keyword }}</strong>
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body" style="max-height: 70vh; overflow-y: auto;">
            <div v-if="searchResults.loading" class="text-center p-5">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">{{ $t("جاري التحميل...") }}</span>
              </div>
              <p class="mt-2">{{ $t("جاري البحث باستخدام محركات البحث النشطة، يرجى الانتظار...") }}</p>
            </div>
            <div v-else-if="searchResults.error" class="alert alert-danger">
              {{ $t("حدث خطأ أثناء البحث:") }} {{ searchResults.error }}
            </div>
            <div v-else-if="searchResults.results && searchResults.results.length > 0">
              <div class="alert alert-info small">
                {{ $t("تم العثور على {count} نتيجة. يمكنك حفظ النتائج المفيدة.", { count: searchResults.results.length }) }}
              </div>
              <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 row-cols-xl-4 g-3">
                <div v-for="(result, index) in searchResults.results" :key="index" class="col">
                  <div class="card h-100 shadow-sm search-result-card">
                    <img 
                      :src="result.thumbnail_url || result.image_url || defaultImageUrl" 
                      class="card-img-top" 
                      alt="صورة النتيجة" 
                      style="height: 150px; object-fit: cover; cursor: pointer;" 
                      @error="handleImageError"
                      @click="openImagePreview(result.image_url || result.thumbnail_url)"
                    />
                    <div class="card-body p-2">
                      <h6 class="card-title small text-truncate mb-1" v-tooltip="result.title || $t("بدون عنوان")">
                        {{ result.title || $t("بدون عنوان") }}
                      </h6>
                      <p class="card-text small text-muted text-truncate mb-1" v-tooltip="result.source_url">
                        <i class="fas fa-link me-1"></i>{{ result.source_url }}
                      </p>
                      <p class="card-text small text-muted text-truncate mb-1" v-tooltip="result.description">
                        <i class="fas fa-info-circle me-1"></i>{{ result.description || $t("لا يوجد وصف") }}
                      </p>
                    </div>
                    <div class="card-footer p-2 d-flex justify-content-between bg-light">
                      <button 
                        class="btn btn-sm btn-outline-success" 
                        @click="saveSearchResult(result)" 
                        :disabled="result.isSaving"
                        v-tooltip="$t("حفظ هذه النتيجة")"
                      >
                        <span v-if="result.isSaving" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                        <i v-else class="fas fa-save"></i>
                      </button>
                      <a :href="result.source_url" target="_blank" class="btn btn-sm btn-outline-info" v-tooltip="$t("فتح المصدر")">
                        <i class="fas fa-external-link-alt"></i>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="alert alert-warning text-center">
              <i class="fas fa-exclamation-triangle me-2"></i>{{ $t("لم يتم العثور على نتائج بحث لهذه الكلمة المفتاحية.") }}
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">{{ $t("إغلاق") }}</button>
            <button 
              type="button" 
              class="btn btn-success btn-sm" 
              @click="saveAllSearchResults" 
              :disabled="!searchResults.results || searchResults.results.length === 0 || isSavingAll"
            >
              <span v-if="isSavingAll" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              {{ isSavingAll ? $t("جاري حفظ الكل...") : $t("حفظ كل النتائج") }}
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- نافذة عرض الصورة -->
    <div class="modal fade" id="imagePreviewModal" tabindex="-1" aria-labelledby="imagePreviewModalLabel" aria-hidden="true" ref="imagePreviewModalRef">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="imagePreviewModalLabel">{{ $t("عرض الصورة") }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body text-center">
            <img :src="currentImageUrl" class="img-fluid rounded" alt="صورة مكبرة" style="max-height: 70vh;"/>
          </div>
        </div>
      </div>
    </div>

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
import KeywordApiService from "../services/KeywordApiService"; 
import ScheduleApiService from "../services/ScheduleApiService";
import ConditionApiService from "../services/ConditionApiService";
import AutoSearchApiService from "../services/AutoSearchApiService";
import PermissionService from "../services/PermissionService"; // Service to check permissions

export default {
  name: "KeywordManager",
  directives: {
    tooltip: VTooltip, // Register directive locally if needed
  },
  setup() {
    const toast = useToast();
    const { t } = useI18n();

    // --- State Variables ---
    const keywords = ref([]);
    const schedules = ref([]);
    const conditions = ref([]);
    const totalKeywords = ref(0);
    const currentPage = ref(1);
    const pageSize = ref(10);
    const loading = ref(false);
    const error = ref(null);
    const isEditMode = ref(false);
    const isSaving = ref(false);
    const isDeleting = ref(false);
    const isSavingAll = ref(false);

    const keywordModal = ref(null);
    const deleteConfirmModal = ref(null);
    const searchResultsModal = ref(null);
    const imagePreviewModal = ref(null);
    const keywordModalRef = ref(null);
    const deleteConfirmModalRef = ref(null);
    const searchResultsModalRef = ref(null);
    const imagePreviewModalRef = ref(null);

    const defaultImageUrl = "/placeholder-image.png"; // Path to a default placeholder image
    const currentImageUrl = ref("");

    const currentKeyword = reactive({
      id: null,
      keyword: "",
      description: "",
      plant_part: null,
      condition_type: null,
      schedule_id: null,
      condition_id: null,
      synonyms: [],
      related_keywords: [],
      is_active: true,
    });
    const currentKeywordToDelete = reactive({ id: null, keyword: "" });
    const currentKeywordForSearch = reactive({ id: null, keyword: "" });

    const synonymsInput = ref("");
    const relatedKeywordsInput = ref("");

    const searchResults = reactive({
      loading: false,
      results: [],
      error: null,
    });

    const filters = reactive({
      keyword: "",
      plantPart: "",
      conditionType: "",
      status: "",
      sortBy: "keyword",
      sortOrder: "asc",
    });

    // --- Permissions ---
    const permissions = reactive({
      canReadKeyword: false,
      canCreateKeyword: false,
      canUpdateKeyword: false,
      canDeleteKeyword: false,
      canRunSearch: false,
    });

    const canCreateKeyword = computed(() => permissions.canCreateKeyword);
    const canUpdateKeyword = computed(() => permissions.canUpdateKeyword);
    const canDeleteKeyword = computed(() => permissions.canDeleteKeyword);

    // --- Static Data ---
    const plantParts = [
      { value: "LEAF", label: "أوراق" },
      { value: "STEM", label: "ساق" },
      { value: "ROOT", label: "جذور" },
      { value: "FRUIT", label: "ثمار" },
      { value: "FLOWER", label: "أزهار" },
      { value: "SEED", label: "بذور" },
      { value: "WHOLE_PLANT", label: "النبات بالكامل" },
    ];

    const conditionTypes = [
      { value: "FUNGAL", label: "فطري" },
      { value: "BACTERIAL", label: "بكتيري" },
      { value: "VIRAL", label: "فيروسي" },
      { value: "INSECT", label: "حشري" },
      { value: "NUTRIENT_DEFICIENCY", label: "نقص عناصر" },
      { value: "NUTRIENT_EXCESS", label: "زيادة عناصر" },
      { value: "WATER_DEFICIENCY", label: "نقص مياه" },
      { value: "WATER_EXCESS", label: "زيادة مياه" },
      { value: "SALINITY", label: "ملوحة" },
      { value: "ENVIRONMENTAL", label: "بيئي" },
      { value: "OTHER", label: "أخرى" },
    ];

    // --- Computed Properties ---
    const totalPages = computed(() => {
      return Math.ceil(totalKeywords.value / pageSize.value);
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
        permissions.canReadKeyword = await PermissionService.hasPermission("read", "keyword");
        permissions.canCreateKeyword = await PermissionService.hasPermission("create", "keyword");
        permissions.canUpdateKeyword = await PermissionService.hasPermission("update", "keyword");
        permissions.canDeleteKeyword = await PermissionService.hasPermission("delete", "keyword");
        permissions.canRunSearch = await PermissionService.hasPermission("execute", "auto_search");
        
        if (!permissions.canReadKeyword) {
          error.value = t("ليس لديك صلاحية عرض الكلمات المفتاحية.");
          toast.error(error.value);
        }
      } catch (err) {
        console.error("Error fetching permissions:", err);
        error.value = t("خطأ في تحميل الصلاحيات.");
        toast.error(error.value);
      }
    };

    const fetchKeywords = async () => {
      if (!permissions.canReadKeyword) return;
      loading.value = true;
      error.value = null;
      try {
        const params = {
          skip: (currentPage.value - 1) * pageSize.value,
          limit: pageSize.value,
          keyword: filters.keyword || undefined,
          plant_part: filters.plantPart || undefined,
          condition_type: filters.conditionType || undefined,
          is_active: filters.status === "active" ? true : filters.status === "inactive" ? false : undefined,
          sort_by: filters.sortBy,
          sort_order: filters.sortOrder,
        };
        const response = await KeywordApiService.getKeywords(params);
        keywords.value = response.data.keywords;
        totalKeywords.value = response.data.total_count;
      } catch (err) {
        console.error("Error fetching keywords:", err);
        error.value = err.response?.data?.detail || err.message || t("خطأ غير معروف");
        toast.error(`${t("فشل تحميل الكلمات المفتاحية:")} ${error.value}`);
      } finally {
        loading.value = false;
      }
    };

    const debouncedFetchKeywords = _.debounce(fetchKeywords, 500);

    const fetchSchedules = async () => {
      try {
        const response = await ScheduleApiService.getSchedules({ limit: 1000 }); // Fetch all schedules
        schedules.value = response.data.schedules;
      } catch (err) {
        console.error("Error fetching schedules:", err);
        toast.error(t("فشل تحميل الجداول الزمنية."));
      }
    };

    const fetchConditions = async () => {
      try {
        const response = await ConditionApiService.getConditions({ limit: 1000 }); // Fetch all conditions
        conditions.value = response.data.conditions;
      } catch (err) {
        console.error("Error fetching conditions:", err);
        toast.error(t("فشل تحميل الإصابات."));
      }
    };

    const resetCurrentKeyword = () => {
      currentKeyword.id = null;
      currentKeyword.keyword = "";
      currentKeyword.description = "";
      currentKeyword.plant_part = null;
      currentKeyword.condition_type = null;
      currentKeyword.schedule_id = null;
      currentKeyword.condition_id = null;
      currentKeyword.synonyms = [];
      currentKeyword.related_keywords = [];
      currentKeyword.is_active = true;
      synonymsInput.value = "";
      relatedKeywordsInput.value = "";
    };

    const openAddKeywordModal = () => {
      if (!permissions.canCreateKeyword) {
        toast.error(t("ليس لديك صلاحية إضافة كلمات مفتاحية."));
        return;
      }
      isEditMode.value = false;
      resetCurrentKeyword();
      keywordModal.value.show();
    };

    const openEditKeywordModal = (keyword) => {
      if (!permissions.canUpdateKeyword) {
        toast.error(t("ليس لديك صلاحية تعديل الكلمات المفتاحية."));
        return;
      }
      isEditMode.value = true;
      Object.assign(currentKeyword, keyword);
      // Ensure IDs are numbers or null
      currentKeyword.schedule_id = keyword.schedule_id ? Number(keyword.schedule_id) : null;
      currentKeyword.condition_id = keyword.condition_id ? Number(keyword.condition_id) : null;
      // Handle arrays for synonyms and related keywords
      currentKeyword.synonyms = Array.isArray(keyword.synonyms) ? keyword.synonyms : [];
      currentKeyword.related_keywords = Array.isArray(keyword.related_keywords) ? keyword.related_keywords : [];
      synonymsInput.value = currentKeyword.synonyms.join(", ");
      relatedKeywordsInput.value = currentKeyword.related_keywords.join(", ");
      keywordModal.value.show();
    };

    const saveKeyword = async () => {
      if (isSaving.value) return;
      isSaving.value = true;
      
      // Prepare data
      const keywordData = { ...currentKeyword };
      keywordData.synonyms = synonymsInput.value.split(",").map(s => s.trim()).filter(s => s);
      keywordData.related_keywords = relatedKeywordsInput.value.split(",").map(s => s.trim()).filter(s => s);
      // Ensure null values for empty selects
      if (!keywordData.plant_part) keywordData.plant_part = null;
      if (!keywordData.condition_type) keywordData.condition_type = null;
      if (!keywordData.schedule_id) keywordData.schedule_id = null;
      if (!keywordData.condition_id) keywordData.condition_id = null;

      try {
        if (isEditMode.value) {
          if (!permissions.canUpdateKeyword) throw new Error(t("ليس لديك صلاحية التعديل."));
          await KeywordApiService.updateKeyword(currentKeyword.id, keywordData);
          toast.success(t("تم تحديث الكلمة المفتاحية بنجاح!"));
        } else {
          if (!permissions.canCreateKeyword) throw new Error(t("ليس لديك صلاحية الإنشاء."));
          await KeywordApiService.createKeyword(keywordData);
          toast.success(t("تمت إضافة الكلمة المفتاحية بنجاح!"));
        }
        keywordModal.value.hide();
        fetchKeywords(); // Refresh the list
      } catch (err) {
        console.error("Error saving keyword:", err);
        const errorMsg = err.response?.data?.detail || err.message || t("خطأ غير معروف");
        toast.error(`${t("فشل حفظ الكلمة المفتاحية:")} ${errorMsg}`);
      } finally {
        isSaving.value = false;
      }
    };

    const confirmDeleteKeyword = (keyword) => {
      if (!permissions.canDeleteKeyword) {
        toast.error(t("ليس لديك صلاحية حذف الكلمات المفتاحية."));
        return;
      }
      currentKeywordToDelete.id = keyword.id;
      currentKeywordToDelete.keyword = keyword.keyword;
      deleteConfirmModal.value.show();
    };

    const deleteKeyword = async () => {
      if (isDeleting.value || !currentKeywordToDelete.id) return;
      if (!permissions.canDeleteKeyword) {
         toast.error(t("ليس لديك صلاحية الحذف."));
         deleteConfirmModal.value.hide();
         return;
      }
      isDeleting.value = true;
      try {
        await KeywordApiService.deleteKeyword(currentKeywordToDelete.id);
        toast.success(t("تم حذف الكلمة المفتاحية بنجاح!"));
        deleteConfirmModal.value.hide();
        // Adjust pagination if the last item on a page was deleted
        if (keywords.value.length === 1 && currentPage.value > 1) {
          currentPage.value--;
        }
        fetchKeywords(); // Refresh the list
      } catch (err) {
        console.error("Error deleting keyword:", err);
        const errorMsg = err.response?.data?.detail || err.message || t("خطأ غير معروف");
        toast.error(`${t("فشل حذف الكلمة المفتاحية:")} ${errorMsg}`);
      } finally {
        isDeleting.value = false;
      }
    };

    const toggleKeywordStatus = async (keyword) => {
      if (!permissions.canUpdateKeyword) {
        toast.error(t("ليس لديك صلاحية تعديل حالة الكلمات المفتاحية."));
        return;
      }
      const newStatus = !keyword.is_active;
      try {
        await KeywordApiService.updateKeyword(keyword.id, { is_active: newStatus });
        toast.success(t("تم تحديث حالة الكلمة المفتاحية بنجاح!"));
        fetchKeywords(); // Refresh the list
      } catch (err) {
        console.error("Error toggling keyword status:", err);
        const errorMsg = err.response?.data?.detail || err.message || t("خطأ غير معروف");
        toast.error(`${t("فشل تحديث حالة الكلمة المفتاحية:")} ${errorMsg}`);
      }
    };

    const runImmediateSearch = async (keyword) => {
       if (!permissions.canRunSearch) {
        toast.error(t("ليس لديك صلاحية تشغيل البحث الفوري."));
        return;
      }
      currentKeywordForSearch.id = keyword.id;
      currentKeywordForSearch.keyword = keyword.keyword;
      searchResults.loading = true;
      searchResults.results = [];
      searchResults.error = null;
      searchResultsModal.value.show();
      try {
        const response = await AutoSearchApiService.runImmediateSearch(keyword.id);
        searchResults.results = response.data.results.map(r => ({ ...r, isSaving: false })); // Add isSaving flag
      } catch (err) {
        console.error("Error running immediate search:", err);
        searchResults.error = err.response?.data?.detail || err.message || t("خطأ غير معروف");
        toast.error(`${t("فشل البحث الفوري:")} ${searchResults.error}`);
      } finally {
        searchResults.loading = false;
      }
    };
    
    const saveSearchResult = async (result) => {
      result.isSaving = true;
      try {
        // Assuming an API endpoint exists to save individual search results
        // await SomeApiService.saveResult(result);
        // Mock saving for now
        await new Promise(resolve => setTimeout(resolve, 500)); 
        toast.success(t("تم حفظ النتيجة بنجاح (محاكاة)."));
        // Optionally remove the saved result from the list or mark it as saved
        // searchResults.results = searchResults.results.filter(r => r !== result);
      } catch (err) {
        console.error("Error saving search result:", err);
        toast.error(t("فشل حفظ نتيجة البحث."));
      } finally {
        result.isSaving = false;
      }
    };

    const saveAllSearchResults = async () => {
      if (isSavingAll.value || !searchResults.results || searchResults.results.length === 0) return;
      isSavingAll.value = true;
      try {
        // Assuming an API endpoint exists to save all search results for a keyword
        // await SomeApiService.saveAllResults(currentKeywordForSearch.id, searchResults.results);
        // Mock saving for now
        await new Promise(resolve => setTimeout(resolve, 1500)); 
        toast.success(t("تم حفظ جميع النتائج بنجاح (محاكاة)."));
        searchResultsModal.value.hide();
      } catch (err) {
        console.error("Error saving all search results:", err);
        toast.error(t("فشل حفظ جميع نتائج البحث."));
      } finally {
        isSavingAll.value = false;
      }
    };

    const changePage = (page) => {
      if (page >= 1 && page <= totalPages.value && page !== currentPage.value && page !== "...") {
        currentPage.value = page;
        fetchKeywords();
      }
    };

    const changePageSize = () => {
      currentPage.value = 1; // Reset to first page when page size changes
      fetchKeywords();
    };

    const truncateText = (text, length) => {
      if (!text) return "";
      return text.length > length ? text.substring(0, length) + "..." : text;
    };

    const getPlantPartLabel = (value) => {
      const part = plantParts.find(p => p.value === value);
      return part ? t(part.label) : t("غير محدد");
    };

    const getConditionTypeLabel = (value) => {
      const type = conditionTypes.find(t => t.value === value);
      return type ? t(type.label) : t("غير محدد");
    };

    const getConditionName = (id) => {
      const condition = conditions.value.find(c => c.id === id);
      return condition ? condition.name : t("غير معروف");
    };
    
    const getPerformanceBadgeClass = (score) => {
      if (score === null || score === undefined) return "bg-secondary";
      if (score >= 8) return "bg-success";
      if (score >= 5) return "bg-warning text-dark";
      return "bg-danger";
    };
    
    const handleImageError = (event) => {
      event.target.src = defaultImageUrl;
    };
    
    const openImagePreview = (imageUrl) => {
      if (!imageUrl) return;
      currentImageUrl.value = imageUrl;
      imagePreviewModal.value.show();
    };

    // --- Lifecycle Hooks ---
    onMounted(async () => {
      await fetchPermissions();
      if (permissions.canReadKeyword) {
        fetchKeywords();
        fetchSchedules();
        fetchConditions();
      }
      // Initialize Bootstrap modals
      if (keywordModalRef.value) {
        keywordModal.value = new Modal(keywordModalRef.value);
      }
      if (deleteConfirmModalRef.value) {
        deleteConfirmModal.value = new Modal(deleteConfirmModalRef.value);
      }
      if (searchResultsModalRef.value) {
        searchResultsModal.value = new Modal(searchResultsModalRef.value);
      }
      if (imagePreviewModalRef.value) {
        imagePreviewModal.value = new Modal(imagePreviewModalRef.value);
      }
    });

    // --- Watchers ---
    // Optional: Watch filters if not using @change or debounced input
    // watch(filters, fetchKeywords, { deep: true });

    return {
      keywords,
      schedules,
      conditions,
      totalKeywords,
      currentPage,
      pageSize,
      totalPages,
      paginationPages,
      loading,
      error,
      isEditMode,
      isSaving,
      isDeleting,
      isSavingAll,
      currentKeyword,
      currentKeywordToDelete,
      currentKeywordForSearch,
      synonymsInput,
      relatedKeywordsInput,
      searchResults,
      filters,
      plantParts,
      conditionTypes,
      keywordModalRef,
      deleteConfirmModalRef,
      searchResultsModalRef,
      imagePreviewModalRef,
      currentImageUrl,
      defaultImageUrl,
      canCreateKeyword,
      canUpdateKeyword,
      canDeleteKeyword,
      fetchKeywords,
      debouncedFetchKeywords,
      openAddKeywordModal,
      openEditKeywordModal,
      saveKeyword,
      confirmDeleteKeyword,
      deleteKeyword,
      toggleKeywordStatus,
      runImmediateSearch,
      saveSearchResult,
      saveAllSearchResults,
      changePage,
      changePageSize,
      truncateText,
      getPlantPartLabel,
      getConditionTypeLabel,
      getConditionName,
      getPerformanceBadgeClass,
      handleImageError,
      openImagePreview,
      t, // Make t available in the template
    };
  },
};
</script>

<style scoped>
.keyword-manager {
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

.bg-danger-light {
  background-color: rgba(220, 53, 69, 0.1);
}

.search-result-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transition: all 0.2s ease-in-out;
}

/* Add custom styles for tooltips if needed */
[v-tooltip] {
  cursor: help;
}
</style>

