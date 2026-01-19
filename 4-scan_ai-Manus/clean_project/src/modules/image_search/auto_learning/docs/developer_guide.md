# دليل المطور لنظام البحث الذاتي الذكي

## مقدمة

هذا الدليل مخصص للمطورين الذين يعملون على صيانة وتطوير نظام البحث الذاتي الذكي. يقدم الدليل نظرة عامة على الهيكل البرمجي للنظام، والمكونات الرئيسية، وكيفية تطوير وتوسيع النظام.

## هيكل المشروع

```
/auto_learning/
├── keyword_management/
│   ├── models.py
│   ├── schemas.py
│   └── service.py
├── source_management/
│   ├── models.py
│   ├── schemas.py
│   └── service.py
├── search_engine_management/
│   ├── models.py
│   ├── schemas.py
│   └── service.py
├── frontend/
│   ├── KeywordManager.vue
│   ├── SourceManager.vue
│   └── SearchEngineManager.vue
├── services/
│   ├── ApiService.js
│   ├── KeywordApiService.js
│   ├── SourceApiService.js
│   ├── SearchEngineApiService.js
│   └── PermissionService.js
├── tests/
│   ├── integration_test.js
│   └── e2e_test.js
└── docs/
    ├── user_guide.md
    └── developer_guide.md
```

## المكونات الرئيسية

### 1. إدارة الكلمات المفتاحية

#### models.py
يحتوي على نماذج قاعدة البيانات للكلمات المفتاحية والعلاقات بينها.

```python
class Keyword(Base):
    __tablename__ = "keywords"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True, nullable=False)
    category = Column(String, nullable=False)
    synonyms = Column(ARRAY(String), nullable=True)
    plant_parts = Column(ARRAY(String), nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # العلاقات
    relations = relationship("KeywordRelation", back_populates="source_keyword")
```

#### schemas.py
يحتوي على مخططات البيانات للتحقق من صحة البيانات المدخلة والمخرجة.

```python
class KeywordBase(BaseModel):
    text: str
    category: str
    synonyms: Optional[List[str]] = []
    plant_parts: Optional[List[str]] = []
    description: Optional[str] = None
    is_active: bool = True

class KeywordCreate(KeywordBase):
    pass

class KeywordUpdate(BaseModel):
    text: Optional[str] = None
    category: Optional[str] = None
    synonyms: Optional[List[str]] = None
    plant_parts: Optional[List[str]] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class Keyword(KeywordBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
```

#### service.py
يحتوي على خدمة إدارة الكلمات المفتاحية مع دعم الصلاحيات والتكامل مع الذاكرة المركزية.

```python
class KeywordService:
    def __init__(self, db: Session, memory_service=None, permission_service=None):
        self.db = db
        self.memory_service = memory_service
        self.permission_service = permission_service
    
    def get_keywords(self, skip: int = 0, limit: int = 100, filters: dict = None):
        """الحصول على قائمة الكلمات المفتاحية مع دعم التصفية"""
        query = self.db.query(models.Keyword)
        
        if filters:
            if 'text' in filters:
                query = query.filter(models.Keyword.text.ilike(f"%{filters['text']}%"))
            if 'category' in filters:
                query = query.filter(models.Keyword.category == filters['category'])
            if 'is_active' in filters:
                query = query.filter(models.Keyword.is_active == filters['is_active'])
        
        return query.offset(skip).limit(limit).all()
    
    def create_keyword(self, keyword: schemas.KeywordCreate, user_id: int):
        """إنشاء كلمة مفتاحية جديدة"""
        # التحقق من الصلاحيات
        if self.permission_service and not self.permission_service.has_permission(user_id, "create", "keyword"):
            raise PermissionError("ليس لديك صلاحية لإنشاء كلمات مفتاحية")
        
        db_keyword = models.Keyword(**keyword.dict())
        self.db.add(db_keyword)
        self.db.commit()
        self.db.refresh(db_keyword)
        
        # تحديث الذاكرة المركزية
        if self.memory_service:
            self.memory_service.add_keyword_to_memory(db_keyword)
        
        return db_keyword
```

### 2. إدارة المصادر الموثوقة

#### models.py
يحتوي على نماذج قاعدة البيانات للمصادر الموثوقة.

```python
class Source(Base):
    __tablename__ = "sources"
    
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, index=True, nullable=False, unique=True)
    category = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    subdomains = Column(ARRAY(String), nullable=True)
    trust_level = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    is_blacklisted = Column(Boolean, default=False)
    blacklist_reason = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    verification_info = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
```

#### schemas.py
يحتوي على مخططات البيانات للتحقق من صحة البيانات المدخلة والمخرجة.

```python
class SourceBase(BaseModel):
    domain: str
    category: str
    description: Optional[str] = None
    subdomains: Optional[List[str]] = []
    trust_level: int
    is_active: bool = True
    is_blacklisted: bool = False
    blacklist_reason: Optional[str] = None
    notes: Optional[str] = None
    verification_info: Optional[Dict[str, Any]] = None

class SourceCreate(SourceBase):
    pass

class SourceUpdate(BaseModel):
    domain: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    subdomains: Optional[List[str]] = None
    trust_level: Optional[int] = None
    is_active: Optional[bool] = None
    is_blacklisted: Optional[bool] = None
    blacklist_reason: Optional[str] = None
    notes: Optional[str] = None
    verification_info: Optional[Dict[str, Any]] = None

class Source(SourceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
```

#### service.py
يحتوي على خدمة إدارة المصادر الموثوقة مع دعم الصلاحيات والتكامل مع الذاكرة المركزية.

```python
class SourceService:
    def __init__(self, db: Session, memory_service=None, permission_service=None):
        self.db = db
        self.memory_service = memory_service
        self.permission_service = permission_service
    
    def get_sources(self, skip: int = 0, limit: int = 100, filters: dict = None):
        """الحصول على قائمة المصادر مع دعم التصفية"""
        query = self.db.query(models.Source)
        
        if filters:
            if 'domain' in filters:
                query = query.filter(models.Source.domain.ilike(f"%{filters['domain']}%"))
            if 'category' in filters:
                query = query.filter(models.Source.category == filters['category'])
            if 'is_active' in filters:
                query = query.filter(models.Source.is_active == filters['is_active'])
            if 'is_blacklisted' in filters:
                query = query.filter(models.Source.is_blacklisted == filters['is_blacklisted'])
            if 'min_trust_level' in filters:
                query = query.filter(models.Source.trust_level >= filters['min_trust_level'])
        
        return query.offset(skip).limit(limit).all()
    
    def verify_source(self, source_id: int, user_id: int):
        """التحقق من مصدر"""
        # التحقق من الصلاحيات
        if self.permission_service and not self.permission_service.has_permission(user_id, "verify", "source"):
            raise PermissionError("ليس لديك صلاحية للتحقق من المصادر")
        
        source = self.db.query(models.Source).filter(models.Source.id == source_id).first()
        if not source:
            raise ValueError("المصدر غير موجود")
        
        # تنفيذ عملية التحقق
        verification_result = self._perform_source_verification(source.domain)
        
        # تحديث معلومات التحقق
        source.verification_info = verification_result
        source.trust_level = verification_result.get("suggested_trust_level", source.trust_level)
        source.updated_at = func.now()
        
        self.db.commit()
        self.db.refresh(source)
        
        return verification_result
```

### 3. إدارة محركات البحث

#### models.py
يحتوي على نماذج قاعدة البيانات لمحركات البحث.

```python
class SearchEngine(Base):
    __tablename__ = "search_engines"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(String, nullable=False)
    base_url = Column(String, nullable=False)
    query_param = Column(String, nullable=False)
    results_param = Column(String, nullable=True)
    icon_url = Column(String, nullable=True)
    priority = Column(Integer, default=100)
    additional_params = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
```

#### schemas.py
يحتوي على مخططات البيانات للتحقق من صحة البيانات المدخلة والمخرجة.

```python
class SearchEngineBase(BaseModel):
    name: str
    type: str
    base_url: str
    query_param: str
    results_param: Optional[str] = None
    icon_url: Optional[str] = None
    priority: int = 100
    additional_params: Optional[Dict[str, Any]] = None
    is_active: bool = True

class SearchEngineCreate(SearchEngineBase):
    pass

class SearchEngineUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    base_url: Optional[str] = None
    query_param: Optional[str] = None
    results_param: Optional[str] = None
    icon_url: Optional[str] = None
    priority: Optional[int] = None
    additional_params: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class SearchEngine(SearchEngineBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
```

#### service.py
يحتوي على خدمة إدارة محركات البحث مع دعم الصلاحيات والتكامل مع الذاكرة المركزية.

```python
class SearchEngineService:
    def __init__(self, db: Session, memory_service=None, permission_service=None):
        self.db = db
        self.memory_service = memory_service
        self.permission_service = permission_service
    
    def get_search_engines(self, skip: int = 0, limit: int = 100, filters: dict = None):
        """الحصول على قائمة محركات البحث مع دعم التصفية"""
        query = self.db.query(models.SearchEngine)
        
        if filters:
            if 'name' in filters:
                query = query.filter(models.SearchEngine.name.ilike(f"%{filters['name']}%"))
            if 'type' in filters:
                query = query.filter(models.SearchEngine.type == filters['type'])
            if 'is_active' in filters:
                query = query.filter(models.SearchEngine.is_active == filters['is_active'])
        
        # ترتيب حسب الأولوية
        query = query.order_by(models.SearchEngine.priority)
        
        return query.offset(skip).limit(limit).all()
    
    def test_search_engine(self, engine_id: int, query: str, limit: int = 5, user_id: int = None):
        """اختبار محرك بحث"""
        # التحقق من الصلاحيات
        if self.permission_service and not self.permission_service.has_permission(user_id, "test", "search_engine"):
            raise PermissionError("ليس لديك صلاحية لاختبار محركات البحث")
        
        engine = self.db.query(models.SearchEngine).filter(models.SearchEngine.id == engine_id).first()
        if not engine:
            raise ValueError("محرك البحث غير موجود")
        
        # بناء عنوان URL للبحث
        search_url = self._build_search_url(engine, query, limit)
        
        # تنفيذ البحث واسترجاع النتائج
        search_results = self._perform_search(search_url, engine)
        
        return {
            "results": search_results,
            "constructed_url": search_url
        }
```

### 4. واجهات المستخدم الأمامية

#### KeywordManager.vue
واجهة إدارة الكلمات المفتاحية.

```vue
<template>
  <div class="keyword-manager">
    <div class="card">
      <div class="card-header">
        <h5>إدارة الكلمات المفتاحية</h5>
        <div class="header-actions">
          <button v-if="canCreateKeyword" class="btn btn-primary" @click="openAddModal">
            <font-awesome-icon icon="plus" /> إضافة كلمة مفتاحية
          </button>
          <button class="btn btn-outline-secondary" @click="refreshKeywords">
            <font-awesome-icon icon="sync" /> تحديث
          </button>
        </div>
      </div>
      <div class="card-body">
        <!-- فلاتر البحث -->
        <div class="filters mb-3">
          <div class="row">
            <div class="col-md-4">
              <input type="text" class="form-control" v-model="filters.text" placeholder="بحث عن كلمة مفتاحية..." @input="debounceSearch" />
            </div>
            <div class="col-md-3">
              <select class="form-select" v-model="filters.category">
                <option value="">جميع التصنيفات</option>
                <option v-for="category in categories" :key="category.value" :value="category.value">
                  {{ category.label }}
                </option>
              </select>
            </div>
            <div class="col-md-3">
              <select class="form-select" v-model="filters.is_active">
                <option value="">جميع الحالات</option>
                <option :value="true">نشط</option>
                <option :value="false">غير نشط</option>
              </select>
            </div>
            <div class="col-md-2">
              <button class="btn btn-outline-primary w-100" @click="applyFilters">
                <font-awesome-icon icon="filter" /> تصفية
              </button>
            </div>
          </div>
        </div>
        
        <!-- جدول الكلمات المفتاحية -->
        <div class="table-responsive">
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th>النص</th>
                <th>التصنيف</th>
                <th>المرادفات</th>
                <th>الحالة</th>
                <th>تاريخ التحديث</th>
                <th>الإجراءات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="keyword in keywords" :key="keyword.id">
                <td>{{ keyword.text }}</td>
                <td>{{ getCategoryLabel(keyword.category) }}</td>
                <td>{{ keyword.synonyms ? keyword.synonyms.join(', ') : '' }}</td>
                <td>
                  <span :class="keyword.is_active ? 'badge bg-success' : 'badge bg-secondary'">
                    {{ keyword.is_active ? 'نشط' : 'غير نشط' }}
                  </span>
                </td>
                <td>{{ formatDate(keyword.updated_at) }}</td>
                <td>
                  <div class="btn-group">
                    <button v-if="canUpdateKeyword" class="btn btn-sm btn-outline-primary" @click="openEditModal(keyword)">
                      <font-awesome-icon icon="edit" />
                    </button>
                    <button class="btn btn-sm btn-outline-info" @click="openRelationsModal(keyword)">
                      <font-awesome-icon icon="project-diagram" />
                    </button>
                    <button v-if="canDeleteKeyword" class="btn btn-sm btn-outline-danger" @click="confirmDelete(keyword)">
                      <font-awesome-icon icon="trash" />
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="keywords.length === 0">
                <td colspan="6" class="text-center">لا توجد كلمات مفتاحية</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- ترقيم الصفحات -->
        <div class="d-flex justify-content-between align-items-center mt-3">
          <div>
            <span>إجمالي: {{ totalCount }} كلمة مفتاحية</span>
          </div>
          <nav>
            <ul class="pagination">
              <li :class="['page-item', { disabled: currentPage === 1 }]">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">السابق</a>
              </li>
              <li v-for="page in totalPages" :key="page" :class="['page-item', { active: currentPage === page }]">
                <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
              </li>
              <li :class="['page-item', { disabled: currentPage === totalPages }]">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">التالي</a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
    
    <!-- نافذة إضافة/تعديل كلمة مفتاحية -->
    <div class="modal fade" id="keywordModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEditing ? 'تعديل كلمة مفتاحية' : 'إضافة كلمة مفتاحية' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="إغلاق"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveKeyword">
              <div class="mb-3">
                <label for="text" class="form-label">النص</label>
                <input type="text" class="form-control" id="text" v-model="currentKeyword.text" required />
              </div>
              <div class="mb-3">
                <label for="category" class="form-label">التصنيف</label>
                <select class="form-select" id="category" v-model="currentKeyword.category" required>
                  <option v-for="category in categories" :key="category.value" :value="category.value">
                    {{ category.label }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label for="synonyms" class="form-label">المرادفات (مفصولة بفواصل)</label>
                <input type="text" class="form-control" id="synonyms" v-model="synonymsText" />
              </div>
              <div class="mb-3" v-if="showPlantParts">
                <label class="form-label">أجزاء النبات</label>
                <div class="form-check" v-for="part in plantParts" :key="part.value">
                  <input class="form-check-input" type="checkbox" :id="'part_' + part.value" :value="part.value" v-model="currentKeyword.plant_parts" />
                  <label class="form-check-label" :for="'part_' + part.value">{{ part.label }}</label>
                </div>
              </div>
              <div class="mb-3">
                <label for="description" class="form-label">الوصف</label>
                <textarea class="form-control" id="description" v-model="currentKeyword.description" rows="3"></textarea>
              </div>
              <div class="form-check mb-3">
                <input class="form-check-input" type="checkbox" id="is_active" v-model="currentKeyword.is_active" />
                <label class="form-check-label" for="is_active">نشط</label>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">إلغاء</button>
            <button type="button" class="btn btn-primary" @click="saveKeyword">حفظ</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- نافذة العلاقات -->
    <div class="modal fade" id="relationsModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">علاقات الكلمة المفتاحية: {{ currentKeyword.text }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="إغلاق"></button>
          </div>
          <div class="modal-body">
            <!-- العلاقات الحالية -->
            <h6>العلاقات الحالية</h6>
            <div class="table-responsive">
              <table class="table table-sm">
                <thead>
                  <tr>
                    <th>الكلمة المفتاحية</th>
                    <th>نوع العلاقة</th>
                    <th>الإجراءات</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="relation in keywordRelations" :key="relation.id">
                    <td>{{ relation.related_keyword.text }}</td>
                    <td>{{ getRelationTypeLabel(relation.relation_type) }}</td>
                    <td>
                      <button v-if="canUpdateKeyword" class="btn btn-sm btn-outline-danger" @click="removeRelation(relation)">
                        <font-awesome-icon icon="times" />
                      </button>
                    </td>
                  </tr>
                  <tr v-if="keywordRelations.length === 0">
                    <td colspan="3" class="text-center">لا توجد علاقات</td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <!-- إضافة علاقة جديدة -->
            <h6 class="mt-4">إضافة علاقة جديدة</h6>
            <form v-if="canUpdateKeyword" @submit.prevent="addRelation">
              <div class="row">
                <div class="col-md-5">
                  <select class="form-select" v-model="newRelation.related_id" required>
                    <option value="" disabled selected>اختر كلمة مفتاحية</option>
                    <option v-for="keyword in availableKeywords" :key="keyword.id" :value="keyword.id">
                      {{ keyword.text }}
                    </option>
                  </select>
                </div>
                <div class="col-md-5">
                  <select class="form-select" v-model="newRelation.relation_type" required>
                    <option value="" disabled selected>اختر نوع العلاقة</option>
                    <option v-for="type in relationTypes" :key="type.value" :value="type.value">
                      {{ type.label }}
                    </option>
                  </select>
                </div>
                <div class="col-md-2">
                  <button type="submit" class="btn btn-primary w-100">إضافة</button>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">إغلاق</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- نافذة تأكيد الحذف -->
    <div class="modal fade" id="deleteModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">تأكيد الحذف</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="إغلاق"></button>
          </div>
          <div class="modal-body">
            <p>هل أنت متأكد من حذف الكلمة المفتاحية "{{ currentKeyword.text }}"؟</p>
            <p class="text-danger">هذا الإجراء لا يمكن التراجع عنه.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">إلغاء</button>
            <button type="button" class="btn btn-danger" @click="deleteKeyword">حذف</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { Modal } from 'bootstrap';
import KeywordApiService from '../services/KeywordApiService';
import PermissionService from '../services/PermissionService';
import { useToast } from 'vue-toastification';

export default {
  name: 'KeywordManager',
  setup() {
    const toast = useToast();
    
    // البيانات
    const keywords = ref([]);
    const totalCount = ref(0);
    const currentPage = ref(1);
    const pageSize = ref(10);
    const filters = ref({
      text: '',
      category: '',
      is_active: ''
    });
    
    // الكلمة المفتاحية الحالية
    const currentKeyword = ref({
      text: '',
      category: 'PLANT',
      synonyms: [],
      plant_parts: [],
      description: '',
      is_active: true
    });
    const isEditing = ref(false);
    const synonymsText = ref('');
    
    // العلاقات
    const keywordRelations = ref([]);
    const availableKeywords = ref([]);
    const newRelation = ref({
      related_id: '',
      relation_type: ''
    });
    
    // الصلاحيات
    const canCreateKeyword = ref(false);
    const canUpdateKeyword = ref(false);
    const canDeleteKeyword = ref(false);
    
    // البيانات الثابتة
    const categories = [
      { value: 'PLANT', label: 'نبات' },
      { value: 'DISEASE', label: 'مرض' },
      { value: 'PEST', label: 'آفة' },
      { value: 'TECHNIQUE', label: 'تقنية' },
      { value: 'FERTILIZER', label: 'سماد' },
      { value: 'EQUIPMENT', label: 'معدات' },
      { value: 'SYMPTOM', label: 'عرض' },
      { value: 'OTHER', label: 'أخرى' }
    ];
    
    const plantParts = [
      { value: 'LEAF', label: 'ورقة' },
      { value: 'STEM', label: 'ساق' },
      { value: 'ROOT', label: 'جذر' },
      { value: 'FLOWER', label: 'زهرة' },
      { value: 'FRUIT', label: 'ثمرة' },
      { value: 'SEED', label: 'بذرة' }
    ];
    
    const relationTypes = [
      { value: 'SYNONYM', label: 'مرادف' },
      { value: 'BROADER', label: 'أوسع' },
      { value: 'NARROWER', label: 'أضيق' },
      { value: 'RELATED', label: 'ذو صلة' },
      { value: 'CAUSE', label: 'سبب' },
      { value: 'EFFECT', label: 'نتيجة' },
      { value: 'PART_OF', label: 'جزء من' },
      { value: 'HAS_PART', label: 'يحتوي على' }
    ];
    
    // الحسابات
    const totalPages = computed(() => {
      return Math.ceil(totalCount.value / pageSize.value);
    });
    
    const showPlantParts = computed(() => {
      return ['PLANT', 'DISEASE'].includes(currentKeyword.value.category);
    });
    
    // الدوال
    const loadKeywords = async () => {
      try {
        const params = {
          skip: (currentPage.value - 1) * pageSize.value,
          limit: pageSize.value
        };
        
        if (filters.value.text) params.text = filters.value.text;
        if (filters.value.category) params.category = filters.value.category;
        if (filters.value.is_active !== '') params.is_active = filters.value.is_active;
        
        const response = await KeywordApiService.getKeywords(params);
        keywords.value = response.data.keywords;
        totalCount.value = response.data.total_count;
      } catch (error) {
        toast.error('حدث خطأ أثناء تحميل الكلمات المفتاحية');
        console.error(error);
      }
    };
    
    const checkPermissions = async () => {
      try {
        canCreateKeyword.value = await PermissionService.hasPermission('create', 'keyword');
        canUpdateKeyword.value = await PermissionService.hasPermission('update', 'keyword');
        canDeleteKeyword.value = await PermissionService.hasPermission('delete', 'keyword');
      } catch (error) {
        console.error('Error checking permissions:', error);
      }
    };
    
    const refreshKeywords = () => {
      loadKeywords();
    };
    
    const debounceSearch = (() => {
      let timeout;
      return () => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
          currentPage.value = 1;
          loadKeywords();
        }, 500);
      };
    })();
    
    const applyFilters = () => {
      currentPage.value = 1;
      loadKeywords();
    };
    
    const changePage = (page) => {
      if (page < 1 || page > totalPages.value) return;
      currentPage.value = page;
      loadKeywords();
    };
    
    const openAddModal = () => {
      isEditing.value = false;
      currentKeyword.value = {
        text: '',
        category: 'PLANT',
        synonyms: [],
        plant_parts: [],
        description: '',
        is_active: true
      };
      synonymsText.value = '';
      new Modal(document.getElementById('keywordModal')).show();
    };
    
    const openEditModal = (keyword) => {
      isEditing.value = true;
      currentKeyword.value = { ...keyword };
      synonymsText.value = keyword.synonyms ? keyword.synonyms.join(', ') : '';
      new Modal(document.getElementById('keywordModal')).show();
    };
    
    const saveKeyword = async () => {
      try {
        // تحويل المرادفات من نص إلى مصفوفة
        if (synonymsText.value) {
          currentKeyword.value.synonyms = synonymsText.value.split(',').map(s => s.trim()).filter(s => s);
        } else {
          currentKeyword.value.synonyms = [];
        }
        
        if (isEditing.value) {
          await KeywordApiService.updateKeyword(currentKeyword.value.id, currentKeyword.value);
          toast.success('تم تحديث الكلمة المفتاحية بنجاح');
        } else {
          await KeywordApiService.createKeyword(currentKeyword.value);
          toast.success('تم إضافة الكلمة المفتاحية بنجاح');
        }
        
        // إغلاق النافذة وتحديث القائمة
        Modal.getInstance(document.getElementById('keywordModal')).hide();
        loadKeywords();
      } catch (error) {
        toast.error('حدث خطأ أثناء حفظ الكلمة المفتاحية');
        console.error(error);
      }
    };
    
    const confirmDelete = (keyword) => {
      currentKeyword.value = { ...keyword };
      new Modal(document.getElementById('deleteModal')).show();
    };
    
    const deleteKeyword = async () => {
      try {
        await KeywordApiService.deleteKeyword(currentKeyword.value.id);
        toast.success('تم حذف الكلمة المفتاحية بنجاح');
        
        // إغلاق النافذة وتحديث القائمة
        Modal.getInstance(document.getElementById('deleteModal')).hide();
        loadKeywords();
      } catch (error) {
        toast.error('حدث خطأ أثناء حذف الكلمة المفتاحية');
        console.error(error);
      }
    };
    
    const openRelationsModal = async (keyword) => {
      currentKeyword.value = { ...keyword };
      
      try {
        // تحميل العلاقات
        const response = await KeywordApiService.getRelatedKeywords(keyword.id);
        keywordRelations.value = response.data.relations;
        
        // تحميل الكلمات المفتاحية المتاحة للعلاقات
        const keywordsResponse = await KeywordApiService.getKeywords({ limit: 1000 });
        availableKeywords.value = keywordsResponse.data.keywords.filter(k => k.id !== keyword.id);
        
        // إعادة تعيين العلاقة الجديدة
        newRelation.value = {
          related_id: '',
          relation_type: ''
        };
        
        new Modal(document.getElementById('relationsModal')).show();
      } catch (error) {
        toast.error('حدث خطأ أثناء تحميل العلاقات');
        console.error(error);
      }
    };
    
    const addRelation = async () => {
      try {
        await KeywordApiService.addKeywordRelation(
          currentKeyword.value.id,
          newRelation.value.related_id,
          newRelation.value.relation_type
        );
        
        toast.success('تم إضافة العلاقة بنجاح');
        
        // إعادة تحميل العلاقات
        const response = await KeywordApiService.getRelatedKeywords(currentKeyword.value.id);
        keywordRelations.value = response.data.relations;
        
        // إعادة تعيين العلاقة الجديدة
        newRelation.value = {
          related_id: '',
          relation_type: ''
        };
      } catch (error) {
        toast.error('حدث خطأ أثناء إضافة العلاقة');
        console.error(error);
      }
    };
    
    const removeRelation = async (relation) => {
      try {
        await KeywordApiService.removeKeywordRelation(currentKeyword.value.id, relation.related_keyword.id);
        toast.success('تم حذف العلاقة بنجاح');
        
        // إعادة تحميل العلاقات
        const response = await KeywordApiService.getRelatedKeywords(currentKeyword.value.id);
        keywordRelations.value = response.data.relations;
      } catch (error) {
        toast.error('حدث خطأ أثناء حذف العلاقة');
        console.error(error);
      }
    };
    
    const getCategoryLabel = (value) => {
      const category = categories.find(c => c.value === value);
      return category ? category.label : value;
    };
    
    const getRelationTypeLabel = (value) => {
      const type = relationTypes.find(t => t.value === value);
      return type ? type.label : value;
    };
    
    const formatDate = (dateString) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('ar-SA', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    };
    
    // تحميل البيانات عند تركيب المكون
    onMounted(() => {
      loadKeywords();
      checkPermissions();
    });
    
    return {
      keywords,
      totalCount,
      currentPage,
      pageSize,
      filters,
      currentKeyword,
      isEditing,
      synonymsText,
      keywordRelations,
      availableKeywords,
      newRelation,
      canCreateKeyword,
      canUpdateKeyword,
      canDeleteKeyword,
      categories,
      plantParts,
      relationTypes,
      totalPages,
      showPlantParts,
      refreshKeywords,
      debounceSearch,
      applyFilters,
      changePage,
      openAddModal,
      openEditModal,
      saveKeyword,
      confirmDelete,
      deleteKeyword,
      openRelationsModal,
      addRelation,
      removeRelation,
      getCategoryLabel,
      getRelationTypeLabel,
      formatDate
    };
  }
};
</script>

<style scoped>
.keyword-manager {
  direction: rtl;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.filters {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 5px;
}
</style>
```

## تطوير وتوسيع النظام

### إضافة نوع جديد من الكلمات المفتاحية

1. أضف القيمة الجديدة إلى قائمة `categories` في ملف `KeywordManager.vue`.
2. قم بتحديث أي منطق خاص بالتصنيفات في الخدمات والواجهات.

### إضافة نوع جديد من العلاقات

1. أضف القيمة الجديدة إلى قائمة `relationTypes` في ملف `KeywordManager.vue`.
2. قم بتحديث أي منطق خاص بالعلاقات في الخدمات.

### إضافة ميزة جديدة للتحقق من المصادر

1. قم بتعديل دالة `_perform_source_verification` في ملف `source_management/service.py`.
2. أضف المنطق الجديد للتحقق.
3. قم بتحديث واجهة المستخدم لعرض المعلومات الجديدة.

### تكامل مع نظام الذاكرة المركزية

```python
class MemoryIntegrationService:
    def __init__(self, memory_api_url, api_key=None):
        self.memory_api_url = memory_api_url
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json'
        }
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'
    
    def add_keyword_to_memory(self, keyword):
        """إضافة كلمة مفتاحية إلى الذاكرة المركزية"""
        try:
            data = {
                'type': 'keyword',
                'content': {
                    'text': keyword.text,
                    'category': keyword.category,
                    'synonyms': keyword.synonyms,
                    'plant_parts': keyword.plant_parts,
                    'description': keyword.description
                },
                'metadata': {
                    'id': keyword.id,
                    'is_active': keyword.is_active,
                    'created_at': keyword.created_at.isoformat(),
                    'updated_at': keyword.updated_at.isoformat()
                }
            }
            
            response = requests.post(
                f'{self.memory_api_url}/memory',
                headers=self.headers,
                json=data
            )
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error adding keyword to memory: {e}")
            return None
    
    def add_source_to_memory(self, source):
        """إضافة مصدر إلى الذاكرة المركزية"""
        try:
            data = {
                'type': 'source',
                'content': {
                    'domain': source.domain,
                    'category': source.category,
                    'description': source.description,
                    'subdomains': source.subdomains,
                    'trust_level': source.trust_level
                },
                'metadata': {
                    'id': source.id,
                    'is_active': source.is_active,
                    'is_blacklisted': source.is_blacklisted,
                    'created_at': source.created_at.isoformat(),
                    'updated_at': source.updated_at.isoformat()
                }
            }
            
            response = requests.post(
                f'{self.memory_api_url}/memory',
                headers=self.headers,
                json=data
            )
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error adding source to memory: {e}")
            return None
```

## اختبارات النظام

### اختبارات الوحدة

```python
def test_keyword_service_create():
    """اختبار إنشاء كلمة مفتاحية"""
    # إعداد
    db = MagicMock()
    memory_service = MagicMock()
    permission_service = MagicMock()
    permission_service.has_permission.return_value = True
    
    service = KeywordService(db, memory_service, permission_service)
    
    keyword_data = schemas.KeywordCreate(
        text="طماطم",
        category="PLANT",
        synonyms=["بندورة"],
        plant_parts=["FRUIT"],
        description="نبات الطماطم",
        is_active=True
    )
    
    # تنفيذ
    service.create_keyword(keyword_data, user_id=1)
    
    # التحقق
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()
    memory_service.add_keyword_to_memory.assert_called_once()
```

### اختبارات التكامل

```python
def test_keyword_api_create():
    """اختبار واجهة API لإنشاء كلمة مفتاحية"""
    # إعداد
    client = TestClient(app)
    
    # تسجيل الدخول
    login_response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    token = login_response.json()["access_token"]
    
    # تنفيذ
    response = client.post(
        "/auto_learning/keywords",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "text": "طماطم",
            "category": "PLANT",
            "synonyms": ["بندورة"],
            "plant_parts": ["FRUIT"],
            "description": "نبات الطماطم",
            "is_active": True
        }
    )
    
    # التحقق
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "طماطم"
    assert data["category"] == "PLANT"
    assert "بندورة" in data["synonyms"]
```

## استكشاف الأخطاء وإصلاحها

### مشاكل قاعدة البيانات

```python
def check_database_connection():
    """التحقق من اتصال قاعدة البيانات"""
    try:
        db = SessionLocal()
        # محاولة تنفيذ استعلام بسيط
        db.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return False
```

### مشاكل الصلاحيات

```python
def debug_permissions(user_id, action, resource):
    """تصحيح مشاكل الصلاحيات"""
    try:
        db = SessionLocal()
        
        # التحقق من وجود المستخدم
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            return {"error": "User not found"}
        
        # الحصول على أدوار المستخدم
        roles = [role.name for role in user.roles]
        
        # الحصول على صلاحيات الأدوار
        permissions = []
        for role_name in roles:
            role = db.query(models.Role).filter(models.Role.name == role_name).first()
            if role:
                for perm in role.permissions:
                    permissions.append(f"{perm.resource}:{perm.action}")
        
        # التحقق من الصلاحية المطلوبة
        required_permission = f"{resource}:{action}"
        has_permission = required_permission in permissions
        
        return {
            "user_id": user_id,
            "username": user.username,
            "roles": roles,
            "permissions": permissions,
            "required_permission": required_permission,
            "has_permission": has_permission
        }
    except Exception as e:
        logger.error(f"Permission debug error: {e}")
        return {"error": str(e)}
```

## الخلاصة

هذا الدليل يقدم نظرة عامة على هيكل وتنفيذ نظام البحث الذاتي الذكي. يمكن للمطورين استخدام هذا الدليل كمرجع لفهم النظام وتطويره وتوسيعه. للمزيد من المعلومات التفصيلية، يرجى الرجوع إلى التعليقات البرمجية في الكود المصدري.
