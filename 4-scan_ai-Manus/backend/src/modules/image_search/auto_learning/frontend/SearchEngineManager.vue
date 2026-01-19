# /home/ubuntu/image_search_integration/auto_learning/frontend/SearchEngineManager.vue

"""
مكون Vue لإدارة محركات البحث للبحث الذاتي الذكي

هذا المكون يوفر واجهة رسومية لإدارة محركات البحث، بما في ذلك:
- عرض محركات البحث مع فلاتر بحث متقدمة وترقيم الصفحات.
- إضافة وتعديل وحذف محركات البحث.
- التحكم في حالة النشاط والأولوية.
- اختبار محركات البحث مباشرة من الواجهة.
- التكامل مع نظام الصلاحيات.
- دعم أنواع مختلفة من محركات البحث (عام، صور، أكاديمي، زراعي).
"""

<template>
  <div class="search-engine-manager">
    <div class="card shadow-sm">
      <div class="card-header bg-light d-flex justify-content-between align-items-center py-3">
        <h5 class="mb-0 text-primary"><i class="fas fa-search-location me-2"></i>{{ $t("إدارة محركات البحث") }}</h5>
        <button 
          class="btn btn-primary btn-sm rounded-pill px-3" 
          @click="openAddEngineModal" 
          v-if="canCreateEngine"
        >
          <i class="fas fa-plus me-1"></i> {{ $t("إضافة محرك بحث") }}
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
                v-model="filters.name" 
                :placeholder="$t("بحث بالاسم أو URL...")" 
                @input="debouncedFetchEngines"
              />
            </div>
          </div>
          <div class="col-md-2">
            <select class="form-select form-select-sm" v-model="filters.type" @change="fetchEngines">
              <option value="">{{ $t("كل الأنواع") }}</option>
              <option v-for="type in engineTypes" :key="type.value" :value="type.value">
                {{ $t(type.label) }}
              </option>
            </select>
          </div>
          <div class="col-md-2">
            <select class="form-select form-select-sm" v-model="filters.status" @change="fetchEngines">
              <option value="">{{ $t("كل الحالات") }}</option>
              <option value="active">{{ $t("نشط") }}</option>
              <option value="inactive">{{ $t("غير نشط") }}</option>
            </select>
          </div>
          <div class="col-md-2">
            <select class="form-select form-select-sm" v-model="filters.sortBy" @change="fetchEngines">
              <option value="name">{{ $t("ترتيب حسب الاسم") }}</option>
              <option value="priority">{{ $t("ترتيب حسب الأولوية") }}</option>
              <option value="created_at">{{ $t("ترتيب حسب تاريخ الإضافة") }}</option>
            </select>
          </div>
          <div class="col-md-1">
            <select class="form-select form-select-sm" v-model="filters.sortOrder" @change="fetchEngines">
              <option value="asc">{{ $t("تصاعدي") }}</option>
              <option value="desc">{{ $t("تنازلي") }}</option>
            </select>
          </div>
          <div class="col-md-2">
            <button class="btn btn-sm btn-outline-secondary w-100" @click="resetFilters">
              <i class="fas fa-undo me-1"></i> {{ $t("إعادة تعيين") }}
            </button>
          </div>
        </div>

        <!-- رسالة التحميل أو الخطأ -->
        <div v-if="loading" class="text-center p-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">{{ $t("جاري التحميل...") }}</span>
          </div>
        </div>
        <div v-else-if="error" class="alert alert-danger">
          {{ $t("حدث خطأ أثناء تحميل محركات البحث:") }} {{ error }}
        </div>

        <!-- جدول محركات البحث -->
        <div v-else class="table-responsive">
          <table class="table table-striped table-hover table-sm align-middle">
            <thead class="table-light">
              <tr>
                <th>{{ $t("الاسم") }}</th>
                <th>{{ $t("النوع") }}</th>
                <th>{{ $t("عنوان URL الأساسي") }}</th>
                <th>{{ $t("الأولوية") }}</th>
                <th>{{ $t("الحالة") }}</th>
                <th v-if="canUpdateEngine || canDeleteEngine || canTestEngine">{{ $t("الإجراءات") }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="engine in engines" :key="engine.id">
                <td>
                  <div class="d-flex align-items-center">
                    <img :src="engine.icon_url || getDefaultIcon(engine.type)" class="engine-icon me-2" alt="أيقونة" />
                    <strong>{{ engine.name }}</strong>
                  </div>
                </td>
                <td>
                  <span class="badge" :class="getEngineTypeBadgeClass(engine.type)">{{ getEngineTypeLabel(engine.type) }}</span>
                </td>
                <td class="small">
                  <a :href="engine.base_url" target="_blank" rel="noopener noreferrer" class="text-decoration-none text-truncate d-inline-block" style="max-width: 250px;" v-tooltip="engine.base_url">
                    {{ engine.base_url }}
                    <i class="fas fa-external-link-alt ms-1 small"></i>
                  </a>
                </td>
                <td>
                  <span class="badge bg-secondary">{{ engine.priority }}</span>
                </td>
                <td>
                  <span 
                    class="badge rounded-pill cursor-pointer"
                    :class="engine.is_active ? 'bg-success-light text-success' : 'bg-warning-light text-warning'"
                    @click="canUpdateEngine && toggleEngineStatus(engine)"
                    v-tooltip="engine.is_active ? $t('تعطيل المحرك') : $t('تفعيل المحرك')"
                  >
                    {{ engine.is_active ? $t("نشط") : $t("غير نشط") }}
                  </span>
                </td>
                <td v-if="canUpdateEngine || canDeleteEngine || canTestEngine">
                  <div class="btn-group btn-group-sm">
                    <button 
                      class="btn btn-outline-primary" 
                      @click="openEditEngineModal(engine)" 
                      v-if="canUpdateEngine"
                      v-tooltip="$t('تعديل')"
                    >
                      <i class="fas fa-edit"></i>
                    </button>
                    <button 
                      class="btn btn-outline-danger" 
                      @click="confirmDeleteEngine(engine)" 
                      v-if="canDeleteEngine"
                      v-tooltip="$t('حذف')"
                    >
                      <i class="fas fa-trash"></i>
                    </button>
                    <button 
                      class="btn btn-outline-info" 
                      @click="openTestEngineModal(engine)" 
                      v-if="canTestEngine"
                      v-tooltip="$t('اختبار')"
                    >
                      <i class="fas fa-vial"></i>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="engines.length === 0">
                <td :colspan="canUpdateEngine || canDeleteEngine || canTestEngine ? 6 : 5" class="text-center text-muted py-4">
                  {{ $t("لا توجد محركات بحث مطابقة للمعايير المحددة.") }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- ترقيم الصفحات -->
        <div v-if="!loading && totalEngines > 0" class="d-flex justify-content-between align-items-center mt-3">
          <div class="text-muted small">
            {{ $t("عرض {start} إلى {end} من {total} محرك بحث", { 
              start: (currentPage - 1) * pageSize + 1, 
              end: Math.min(currentPage * pageSize, totalEngines), 
              total: totalEngines 
            }) }}
          </div>
          <nav aria-label="Page navigation">
            <ul class="pagination pagination-sm mb-0">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">&laquo;</a>
              </li>
              <li v-for="page in paginationPages" :key="page" class="page-item" :class="{ active: currentPage === page, disabled: page === '...' }">
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

    <!-- نافذة إضافة/تعديل محرك بحث -->
    <div class="modal fade" id="engineModal" tabindex="-1" aria-labelledby="engineModalLabel" aria-hidden="true" ref="engineModalRef">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="engineModalLabel">
              {{ isEditMode ? $t("تعديل محرك بحث") : $t("إضافة محرك بحث") }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveEngine">
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="name" class="form-label">{{ $t("الاسم") }} <span class="text-danger">*</span></label>
                  <input type="text" class="form-control form-control-sm" id="name" v-model.trim="currentEngine.name" required />
                </div>
                <div class="col-md-6">
                  <label for="type" class="form-label">{{ $t("النوع") }} <span class="text-danger">*</span></label>
                  <select class="form-select form-select-sm" id="type" v-model="currentEngine.type" required>
                    <option v-for="type in engineTypes" :key="type.value" :value="type.value">
                      {{ $t(type.label) }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="mb-3">
                <label for="base_url" class="form-label">{{ $t("عنوان URL الأساسي") }} <span class="text-danger">*</span></label>
                <input type="url" class="form-control form-control-sm" id="base_url" v-model.trim="currentEngine.base_url" required placeholder="https://www.google.com/search" />
                <div class="form-text text-muted small">{{ $t("عنوان URL الرئيسي للمحرك بدون معلمات الاستعلام.") }}</div>
              </div>
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="query_param" class="form-label">{{ $t("معلمة الاستعلام") }} <span class="text-danger">*</span></label>
                  <input type="text" class="form-control form-control-sm" id="query_param" v-model.trim="currentEngine.query_param" required placeholder="q" />
                  <div class="form-text text-muted small">{{ $t("اسم المعلمة التي تحمل نص البحث (مثل q لـ Google).") }}</div>
                </div>
                <div class="col-md-6">
                  <label for="results_per_page_param" class="form-label">{{ $t("معلمة عدد النتائج") }}</label>
                  <input type="text" class="form-control form-control-sm" id="results_per_page_param" v-model.trim="currentEngine.results_per_page_param" placeholder="num" />
                  <div class="form-text text-muted small">{{ $t("اسم المعلمة لتحديد عدد النتائج في الصفحة (إن وجدت).") }}</div>
                </div>
              </div>
              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="icon_url" class="form-label">{{ $t("رابط الأيقونة") }}</label>
                  <input type="url" class="form-control form-control-sm" id="icon_url" v-model.trim="currentEngine.icon_url" placeholder="https://www.google.com/favicon.ico" />
                </div>
                <div class="col-md-6">
                  <label for="priority" class="form-label">{{ $t("الأولوية") }} <span class="text-danger">*</span></label>
                  <input type="number" class="form-control form-control-sm" id="priority" v-model.number="currentEngine.priority" min="1" max="100" required />
                  <div class="form-text text-muted small">{{ $t("رقم بين 1 (الأعلى) و 100 (الأدنى).") }}</div>
                </div>
              </div>
              <div class="mb-3">
                <label for="additional_params" class="form-label">{{ $t("معلمات إضافية (JSON)") }}</label>
                <textarea class="form-control form-control-sm" id="additional_params" v-model="additionalParamsInput" rows="3" placeholder="{\"hl\": \"ar\", \"tbm\": \"isch\"}"></textarea>
                <div class="form-text text-muted small">{{ $t("أدخل كائن JSON صالح للمعلمات الإضافية الثابتة.") }}</div>
                <div v-if="additionalParamsError" class="text-danger small mt-1">{{ additionalParamsError }}</div>
              </div>
              <div class="form-check mb-3">
                <input class="form-check-input" type="checkbox" id="is_active" v-model="currentEngine.is_active" />
                <label class="form-check-label" for="is_active">{{ $t("نشط") }}</label>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">{{ $t("إلغاء") }}</button>
            <button type="button" class="btn btn-primary btn-sm" @click="saveEngine" :disabled="isSaving || !!additionalParamsError">
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
            {{ $t("هل أنت متأكد من رغبتك في حذف محرك البحث") }}: <strong>{{ currentEngineToDelete.name }}</strong>؟
            <p class="text-danger small mt-2">{{ $t("سيؤدي هذا الإجراء إلى حذف محرك البحث نهائياً.") }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">{{ $t("إلغاء") }}</button>
            <button type="button" class="btn btn-danger btn-sm" @click="deleteEngine" :disabled="isDeleting">
              <span v-if="isDeleting" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              {{ isDeleting ? $t("جاري الحذف...") : $t("حذف") }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- نافذة اختبار محرك البحث -->
    <div class="modal fade" id="testEngineModal" tabindex="-1" aria-labelledby="testEngineModalLabel" aria-hidden="true" ref="testEngineModalRef">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="testEngineModalLabel">
              {{ $t("اختبار محرك البحث:") }} <strong>{{ currentEngineToTest.name }}</strong>
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="row mb-3">
              <div class="col-md-8">
                <label for="test_query" class="form-label">{{ $t("استعلام الاختبار") }}</label>
                <input type="text" class="form-control form-control-sm" id="test_query" v-model="testQuery" :placeholder="$t('مثال: أمراض الطماطم')" />
              </div>
              <div class="col-md-2">
                 <label for="test_num_results" class="form-label">{{ $t("عدد النتائج") }}</label>
                 <input type="number" class="form-control form-control-sm" id="test_num_results" v-model.number="testNumResults" min="1" max="50" />
              </div>
              <div class="col-md-2 d-flex align-items-end">
                <button class="btn btn-primary btn-sm w-100" type="button" @click="runEngineTest" :disabled="testResults.loading || !testQuery">
                  <span v-if="testResults.loading" class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
                  <i v-else class="fas fa-search me-1"></i>
                  {{ testResults.loading ? $t("جاري البحث...") : $t("بحث") }}
                </button>
              </div>
            </div>
            
            <div class="mb-3" v-if="testResults.constructed_url">
              <label class="form-label small text-muted">{{ $t("عنوان URL المُنشأ:") }}</label>
              <input type="text" class="form-control form-control-sm bg-light" :value="testResults.constructed_url" readonly />
            </div>

            <div v-if="testResults.loading" class="text-center p-5">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">{{ $t("جاري التحميل...") }}</span>
              </div>
            </div>
            <div v-else-if="testResults.error" class="alert alert-danger">
              <h6 class="alert-heading">{{ $t("خطأ في الاختبار") }}</h6>
              <p>{{ testResults.error }}</p>
              <hr>
              <p class="mb-0 small">{{ $t("يرجى مراجعة إعدادات محرك البحث أو رسالة الخطأ أعلاه.") }}</p>
            </div>
            <div v-else-if="testResults.results && testResults.results.length > 0">
              <div class="alert alert-success mb-3">
                <i class="fas fa-check-circle me-2"></i>
                {{ $t("تم اختبار محرك البحث بنجاح! تم العثور على {count} نتيجة.", { count: testResults.results.length }) }}
              </div>
              
              <div class="list-group">
                <a v-for="(result, index) in testResults.results" :key="index" :href="result.link" target="_blank" class="list-group-item list-group-item-action flex-column align-items-start">
                  <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1 text-primary">{{ result.title || $t('بدون عنوان') }}</h6>
                    <small class="text-muted">{{ $t("النتيجة") }} #{{ index + 1 }}</small>
                  </div>
                  <p class="mb-1 small">{{ result.snippet || $t('لا يوجد وصف مختصر.') }}</p>
                  <small class="text-success text-truncate d-block">{{ result.link }}</small>
                </a>
              </div>
            </div>
            <div v-else-if="testResults.results && testResults.results.length === 0" class="alert alert-warning">
              <i class="fas fa-exclamation-triangle me-2"></i>
              {{ $t("لم يتم العثور على نتائج للاستعلام المحدد. قد يكون محرك البحث يعمل بشكل صحيح ولكن لا توجد نتائج لهذا البحث.") }}
            </div>
            <div v-else class="alert alert-secondary">
              <i class="fas fa-info-circle me-2"></i>
              {{ $t("أدخل استعلام بحث واضغط على زر البحث لاختبار محرك البحث.") }}
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">{{ $t("إغلاق") }}</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { ref, computed, onMounted, reactive, watch } from "vue";
import { useToast } from "vue-toastification";
import { Modal } from "bootstrap";
import _ from "lodash";
import { useI18n } from "vue-i18n";
import { VTooltip } from "v-tooltip";

// Import API services (adjust paths as needed)
import SearchEngineApiService from "../services/SearchEngineApiService"; 
import PermissionService from "../services/PermissionService";

export default {
  name: "SearchEngineManager",
  directives: {
    tooltip: VTooltip,
  },
  setup() {
    const toast = useToast();
    const { t } = useI18n();

    // --- State Variables ---
    const engines = ref([]);
    const totalEngines = ref(0);
    const currentPage = ref(1);
    const pageSize = ref(10);
    const loading = ref(false);
    const error = ref(null);
    const isEditMode = ref(false);
    const isSaving = ref(false);
    const isDeleting = ref(false);

    const engineModal = ref(null);
    const deleteConfirmModal = ref(null);
    const testEngineModal = ref(null);
    const engineModalRef = ref(null);
    const deleteConfirmModalRef = ref(null);
    const testEngineModalRef = ref(null);

    const currentEngine = reactive({
      id: null,
      name: "",
      type: "GENERAL",
      base_url: "",
      query_param: "",
      results_per_page_param: null,
      icon_url: "",
      priority: 10,
      additional_params: {},
      is_active: true,
    });
    const additionalParamsInput = ref("");
    const additionalParamsError = ref(null);

    const currentEngineToDelete = reactive({ id: null, name: "" });
    const currentEngineToTest = reactive({ id: null, name: "" });
    const testQuery = ref("الزراعة الذكية"); // Default test query
    const testNumResults = ref(5);
    const testResults = reactive({
      loading: false,
      results: null,
      error: null,
      constructed_url: null,
    });

    const filters = reactive({
      name: "",
      type: "",
      status: "",
      sortBy: "priority",
      sortOrder: "asc",
    });

    // --- Permissions ---
    const permissions = reactive({
      canReadEngine: false,
      canCreateEngine: false,
      canUpdateEngine: false,
      canDeleteEngine: false,
      canTestEngine: false,
    });

    const canCreateEngine = computed(() => permissions.canCreateEngine);
    const canUpdateEngine = computed(() => permissions.canUpdateEngine);
    const canDeleteEngine = computed(() => permissions.canDeleteEngine);
    const canTestEngine = computed(() => permissions.canTestEngine);

    // --- Static Data ---
    const engineTypes = [
      { value: "GENERAL", label: "عام", icon: "fas fa-globe", color: "info" },
      { value: "IMAGE", label: "صور", icon: "fas fa-image", color: "success" },
      { value: "ACADEMIC", label: "أكاديمي", icon: "fas fa-graduation-cap", color: "warning" },
      { value: "AGRICULTURAL", label: "زراعي", icon: "fas fa-seedling", color: "primary" },
      { value: "NEWS", label: "إخباري", icon: "fas fa-newspaper", color: "secondary" },
      { value: "VIDEO", label: "فيديو", icon: "fas fa-video", color: "danger" },
      { value: "SHOPPING", label: "تسوق", icon: "fas fa-shopping-cart", color: "dark" },
    ];

    // --- Computed Properties ---
    const totalPages = computed(() => {
      return Math.ceil(totalEngines.value / pageSize.value);
    });

    const paginationPages = computed(() => {
      const pages = [];
      const maxPagesToShow = 5;
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
        permissions.canReadEngine = await PermissionService.hasPermission("read", "search_engine");
        permissions.canCreateEngine = await PermissionService.hasPermission("create", "search_engine");
        permissions.canUpdateEngine = await PermissionService.hasPermission("update", "search_engine");
        permissions.canDeleteEngine = await PermissionService.hasPermission("delete", "search_engine");
        permissions.canTestEngine = await PermissionService.hasPermission("test", "search_engine");
        
        if (!permissions.canReadEngine) {
          error.value = t("ليس لديك صلاحية عرض محركات البحث.");
          toast.error(error.value);
        }
      } catch (err) {
        console.error("Error fetching permissions:", err);
        error.value = t("خطأ في تحميل الصلاحيات.");
        toast.error(error.value);
      }
    };

    const fetchEngines = async () => {
      if (!permissions.canReadEngine) return;
      loading.value = true;
      error.value = null;
      try {
        const params = {
          skip: (currentPage.value - 1) * pageSize.value,
          limit: pageSize.value,
          name: filters.name || undefined,
          type: filters.type || undefined,
          is_active: filters.status === "active" ? true : filters.status === "inactive" ? false : undefined,
          sort_by: filters.sortBy,
          sort_order: filters.sortOrder,
        };
        const response = await SearchEngineApiService.getSearchEngines(params);
        engines.value = response.data.search_engines;
        totalEngines.value = response.data.total_count;
      } catch (err) {
        console.error("Error fetching engines:", err);
        error.value = err.response?.data?.detail || err.message || t("خطأ غير معروف");
        toast.error(`${t("فشل تحميل محركات البحث:")} ${error.value}`);
      } finally {
        loading.value = false;
      }
    };

    const debouncedFetchEngines = _.debounce(fetchEngines, 500);

    const resetFilters = () => {
      filters.name = "";
      filters.type = "";
      filters.status = "";
      filters.sortBy = "priority";
      filters.sortOrder = "asc";
      fetchEngines();
    };

    const resetCurrentEngine = () => {
      currentEngine.id = null;
      currentEngine.name = "";
      currentEngine.type = "GENERAL";
      currentEngine.base_url = "";
      currentEngine.query_param = "";
      currentEngine.results_per_page_param = null;
      currentEngine.icon_url = "";
      currentEngine.priority = 10;
      currentEngine.additional_params = {};
      currentEngine.is_active = true;
      additionalParamsInput.value = "{}";
      additionalParamsError.value = null;
    };

    const openAddEngineModal = () => {
      if (!permissions.canCreateEngine) {
        toast.error(t("ليس لديك صلاحية إضافة محركات بحث."));
        return;
      }
      isEditMode.value = false;
      resetCurrentEngine();
      engineModal.value.show();
    };

    const openEditEngineModal = (engine) => {
      if (!permissions.canUpdateEngine) {
        toast.error(t("ليس لديك صلاحية تعديل محركات البحث."));
        return;
      }
      isEditMode.value = true;
      Object.assign(currentEngine, engine);
      // Ensure additional_params is an object
      currentEngine.additional_params = typeof engine.additional_params === 'object' && engine.additional_params !== null ? engine.additional_params : {};
      additionalParamsInput.value = JSON.stringify(currentEngine.additional_params, null, 2);
      additionalParamsError.value = null;
      engineModal.value.show();
    };

    const saveEngine = async () => {
      if (isSaving.value || additionalParamsError.value) return;
      isSaving.value = true;
      
      // Prepare data
      const engineData = { ...currentEngine };
      try {
        engineData.additional_params = JSON.parse(additionalParamsInput.value || '{}');
      } catch (e) {
        additionalParamsError.value = t("صيغة JSON غير صالحة للمعلمات الإضافية.");
        isSaving.value = false;
        return;
      }
      
      // Clean up empty/null values for optional fields
      if (!engineData.results_per_page_param) engineData.results_per_page_param = null;
      if (!engineData.icon_url) engineData.icon_url = null;

      try {
        if (isEditMode.value) {
          if (!permissions.canUpdateEngine) throw new Error(t("ليس لديك صلاحية التعديل."));
          await SearchEngineApiService.updateSearchEngine(currentEngine.id, engineData);
          toast.success(t("تم تحديث محرك البحث بنجاح!"));
        } else {
          if (!permissions.canCreateEngine) throw new Error(t("ليس لديك صلاحية الإنشاء."));
          await SearchEngineApiService.createSearchEngine(engineData);
          toast.success(t("تمت إضافة محرك البحث بنجاح!"));
        }
        engineModal.value.hide();
        fetchEngines(); // Refresh the list
      } catch (err) {
        console.error("Error saving engine:", err);
        const errorMsg = err.response?.data?.detail || err.message || t("خطأ غير معروف");
        toast.error(`${t("فشل حفظ محرك البحث:")} ${errorMsg}`);
      } finally {
        isSaving.value = false;
      }
    };

    const confirmDeleteEngine = (engine) => {
      if (!permissions.canDeleteEngine) {
        toast.error(t("ليس لديك صلاحية حذف محركات البحث."));
        return;
      }
      currentEngineToDelete.id = engine.id;
      currentEngineToDelete.name = engine.name;
      deleteConfirmModal.value.show();
    };

    const deleteEngine = async () => {
      if (isDeleting.value || !currentEngineToDelete.id) return;
      if (!permissions.canDeleteEngine) {
         toast.error(t("ليس لديك صلاحية الحذف."));
         deleteConfirmModal.value.hide();
         return;
      }
      isDeleting.value = true;
      try {
        await SearchEngineApiService.deleteSearchEngine(currentEngineToDelete.id);
        toast.success(t("تم حذف محرك البحث بنجاح!"));
        deleteConfirmModal.value.hide();
        if (engines.value.length === 1 && currentPage.value > 1) {
          currentPage.value--;
        }
        fetchEngines(); // Refresh the list
      } catch (err) {
        console.error("Error deleting engine:", err);
        const errorMsg = err.response?.data?.detail || err.message || t("خطأ غير معروف");
        toast.error(`${t("فشل حذف محرك البحث:")} ${errorMsg}`);
      } finally {
        isDeleting.value = false;
      }
    };

    const toggleEngineStatus = async (engine) => {
      if (!permissions.canUpdateEngine) {
        toast.error(t("ليس لديك صلاحية تعديل حالة محركات البحث."));
        return;
      }
      const newStatus = !engine.is_active;
      try {
        await SearchEngineApiService.updateSearchEngine(engine.id, { is_active: newStatus });
        toast.success(t("تم تحديث حالة محرك البحث بنجاح!"));
        fetchEngines(); // Refresh the list
      } catch (err) {
        console.error("Error toggling engine status:", err);
        const errorMsg = err.response?.data?.detail || err.message || t("خطأ غير معروف");
        toast.error(`${t("فشل تحديث حالة محرك البحث:")} ${errorMsg}`);
      }
    };
    
    const openTestEngineModal = (engine) => {
      if (!permissions.canTestEngine) {
        toast.error(t("ليس لديك صلاحية اختبار محركات البحث."));
        return;
      }
      currentEngineToTest.id = engine.id;
      currentEngineToTest.name = engine.name;
      testResults.results = null;
      testResults.error = null;
      testResults.loading = false;
      testResults.constructed_url = null;
      testEngineModal.value.show();
    };
    
    const runEngineTest = async () => {
      if (!permissions.canTestEngine || testResults.loading || !currentEngineToTest.id || !testQuery.value) return;
      
      testResults.loading = true;
      testResults.results = null;
      testResults.error = null;
      testResults.constructed_url = null;
      
      try {
        const response = await SearchEngineApiService.testSearchEngine(currentEngineToTest.id, testQuery.value, testNumResults.value);
        testResults.results = response.data.results;
        testResults.constructed_url = response.data.constructed_url;
        if (response.data.results.length === 0) {
           toast.info(t("الاختبار ناجح ولكن لم يتم العثور على نتائج لهذا الاستعلام."));
        }
      } catch (err) {
        console.error("Error testing engine:", err);
        testResults.error = err.response?.data?.detail || err.message || t("خطأ غير معروف");
        toast.error(`${t("فشل اختبار محرك البحث:")} ${testResults.error}`);
      } finally {
        testResults.loading = false;
      }
    };

    const changePage = (page) => {
      if (page >= 1 && page <= totalPages.value && page !== currentPage.value && page !== "...") {
        currentPage.value = page;
        fetchEngines();
      }
    };

    const changePageSize = () => {
      currentPage.value = 1;
      fetchEngines();
    };

    const getEngineTypeLabel = (value) => {
      const type = engineTypes.find(t => t.value === value);
      return type ? t(type.label) : t("غير محدد");
    };
    
    const getEngineTypeBadgeClass = (value) => {
      const type = engineTypes.find(t => t.value === value);
      return type ? `bg-${type.color}-light text-${type.color}` : 'bg-secondary-light text-secondary';
    };

    const getDefaultIcon = (typeValue) => {
      const type = engineTypes.find(t => t.value === typeValue);
      // Return a generic icon path or Font Awesome class
      return type ? `fas ${type.icon}` : 'fas fa-search'; // Placeholder, replace with actual path or logic
      // Or return a path: return '/path/to/default/icon.png';
    };

    // --- Lifecycle Hooks ---
    onMounted(async () => {
      await fetchPermissions();
      if (permissions.canReadEngine) {
        fetchEngines();
      }
      // Initialize Bootstrap modals
      if (engineModalRef.value) {
        engineModal.value = new Modal(engineModalRef.value);
      }
      if (deleteConfirmModalRef.value) {
        deleteConfirmModal.value = new Modal(deleteConfirmModalRef.value);
      }
      if (testEngineModalRef.value) {
        testEngineModal.value = new Modal(testEngineModalRef.value);
      }
    });

    // --- Watchers ---
    watch(additionalParamsInput, (newValue) => {
      try {
        JSON.parse(newValue || '{}');
        additionalParamsError.value = null;
      } catch (e) {
        additionalParamsError.value = t("صيغة JSON غير صالحة.");
      }
    });

    return {
      engines,
      totalEngines,
      currentPage,
      pageSize,
      totalPages,
      paginationPages,
      loading,
      error,
      isEditMode,
      isSaving,
      isDeleting,
      currentEngine,
      additionalParamsInput,
      additionalParamsError,
      currentEngineToDelete,
      currentEngineToTest,
      testQuery,
      testNumResults,
      testResults,
      filters,
      engineTypes,
      engineModalRef,
      deleteConfirmModalRef,
      testEngineModalRef,
      canCreateEngine,
      canUpdateEngine,
      canDeleteEngine,
      canTestEngine,
      fetchEngines,
      debouncedFetchEngines,
      resetFilters,
      openAddEngineModal,
      openEditEngineModal,
      saveEngine,
      confirmDeleteEngine,
      deleteEngine,
      toggleEngineStatus,
      openTestEngineModal,
      runEngineTest,
      changePage,
      changePageSize,
      getEngineTypeLabel,
      getEngineTypeBadgeClass,
      getDefaultIcon,
      t,
    };
  },
};
</script>

<style scoped>
.search-engine-manager {
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

.engine-icon {
  width: 20px;
  height: 20px;
  object-fit: contain;
  vertical-align: middle;
}

.cursor-pointer {
  cursor: pointer;
}

/* Light background colors for badges */
.bg-primary-light { background-color: rgba(var(--bs-primary-rgb), 0.1); }
.bg-secondary-light { background-color: rgba(var(--bs-secondary-rgb), 0.1); }
.bg-success-light { background-color: rgba(var(--bs-success-rgb), 0.1); }
.bg-danger-light { background-color: rgba(var(--bs-danger-rgb), 0.1); }
.bg-warning-light { background-color: rgba(var(--bs-warning-rgb), 0.1); }
.bg-info-light { background-color: rgba(var(--bs-info-rgb), 0.1); }
.bg-dark-light { background-color: rgba(var(--bs-dark-rgb), 0.1); }

/* Text colors matching the light backgrounds */
.text-primary { color: var(--bs-primary) !important; }
.text-secondary { color: var(--bs-secondary) !important; }
.text-success { color: var(--bs-success) !important; }
.text-danger { color: var(--bs-danger) !important; }
.text-warning { color: var(--bs-warning) !important; }
.text-info { color: var(--bs-info) !important; }
.text-dark { color: var(--bs-dark) !important; }

[v-tooltip] {
  cursor: help;
}

.list-group-item h6 {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.list-group-item p {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
