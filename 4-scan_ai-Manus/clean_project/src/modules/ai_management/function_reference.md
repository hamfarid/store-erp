# File: /home/ubuntu/ai_web_organized/src/modules/ai_management/function_reference.md

# مرجع الدوال - وحدة إدارة الذكاء الاصطناعي المتعدد الوكلاء

## وحدة الذاكرة والتعلم (memory_and_learning.py)

### خدمة الذاكرة (MemoryService)

#### get_memory(agent_id, memory_type, key=None)

- **الوصف**: الحصول على ذاكرة وكيل معين
- **المعاملات**:
  - `agent_id`: معرف الوكيل
  - `memory_type`: نوع الذاكرة (قصيرة المدى، طويلة المدى، سياق، معرفة، تفضيلات)
  - `key`: مفتاح الذاكرة (اختياري)
- **القيمة المرجعة**: قائمة بعناصر الذاكرة الصالحة

#### store_memory(agent_id, memory_type, key, value, access_level=AccessLevel.PRIVATE, metadata=None, tags=None, expires_at=None)

- **الوصف**: تخزين ذاكرة لوكيل معين
- **المعاملات**:
  - `agent_id`: معرف الوكيل
  - `memory_type`: نوع الذاكرة
  - `key`: مفتاح الذاكرة
  - `value`: قيمة الذاكرة
  - `access_level`: مستوى الوصول (خاص، مشترك، عام)
  - `metadata`: بيانات وصفية (اختياري)
  - `tags`: علامات (اختياري)
  - `expires_at`: وقت انتهاء الصلاحية (اختياري)
- **القيمة المرجعة**: عنصر الذاكرة المخزن

#### delete_memory(agent_id, memory_type, key=None)

- **الوصف**: حذف ذاكرة وكيل معين
- **المعاملات**:
  - `agent_id`: معرف الوكيل
  - `memory_type`: نوع الذاكرة
  - `key`: مفتاح الذاكرة (اختياري)
- **القيمة المرجعة**: عدد عناصر الذاكرة المحذوفة

### خدمة المعرفة (KnowledgeService)

#### add_knowledge(content, keywords=None, source=None, confidence=1.0, entity_links=None)

- **الوصف**: إضافة معرفة جديدة
- **المعاملات**:
  - `content`: محتوى المعرفة
  - `keywords`: الكلمات المفتاحية (اختياري)
  - `source`: مصدر المعرفة (اختياري)
  - `confidence`: درجة الثقة (اختياري)
  - `entity_links`: روابط الكيانات (اختياري)
- **القيمة المرجعة**: عنصر المعرفة المضاف

#### get_knowledge(knowledge_id)

- **الوصف**: الحصول على معرفة محددة
- **المعاملات**:
  - `knowledge_id`: معرف المعرفة
- **القيمة المرجعة**: عنصر المعرفة

#### update_knowledge(knowledge_id, content=None, keywords=None, source=None, confidence=None, entity_links=None)

- **الوصف**: تحديث معرفة موجودة
- **المعاملات**:
  - `knowledge_id`: معرف المعرفة
  - `content`: محتوى المعرفة (اختياري)
  - `keywords`: الكلمات المفتاحية (اختياري)
  - `source`: مصدر المعرفة (اختياري)
  - `confidence`: درجة الثقة (اختياري)
  - `entity_links`: روابط الكيانات (اختياري)
- **القيمة المرجعة**: عنصر المعرفة المحدث

#### delete_knowledge(knowledge_id)

- **الوصف**: حذف معرفة
- **المعاملات**:
  - `knowledge_id`: معرف المعرفة
- **القيمة المرجعة**: قيمة منطقية تشير إلى نجاح العملية

### خدمة النماذج (ModelService)

#### start_training(model_name, dataset_description=None, hyperparameters=None, created_by=None, notes=None)

- **الوصف**: بدء تدريب نموذج
- **المعاملات**:
  - `model_name`: اسم النموذج
  - `dataset_description`: وصف مجموعة البيانات (اختياري)
  - `hyperparameters`: المعلمات الفائقة (اختياري)
  - `created_by`: المستخدم الذي بدأ التدريب (اختياري)
  - `notes`: ملاحظات (اختياري)
- **القيمة المرجعة**: جلسة التدريب المنشأة

#### complete_training(training_id, model_path, metrics=None, status='completed')

- **الوصف**: إكمال تدريب نموذج
- **المعاملات**:
  - `training_id`: معرف جلسة التدريب
  - `model_path`: مسار النموذج المدرب
  - `metrics`: مقاييس التدريب (اختياري)
  - `status`: حالة التدريب (اختياري)
- **القيمة المرجعة**: جلسة التدريب المحدثة

#### deploy_model(model_name, agent_type, model_category, cost_level, capabilities=None, model_path=None, api_endpoint=None, config=None)

- **الوصف**: نشر نموذج
- **المعاملات**:
  - `model_name`: اسم النموذج
  - `agent_type`: نوع الوكيل
  - `model_category`: فئة النموذج
  - `cost_level`: مستوى التكلفة
  - `capabilities`: القدرات (اختياري)
  - `model_path`: مسار النموذج (اختياري)
  - `api_endpoint`: نقطة نهاية واجهة برمجة التطبيقات (اختياري)
  - `config`: إعدادات التكوين (اختياري)
- **القيمة المرجعة**: نشر النموذج المنشأ

#### get_active_deployments(agent_type=None)

- **الوصف**: الحصول على النشرات النشطة
- **المعاملات**:
  - `agent_type`: نوع الوكيل (اختياري)
- **القيمة المرجعة**: قائمة بنشرات النماذج النشطة

### خدمة الأداء (PerformanceService)

#### log_event(event_type, actor_agent_id=None, target_agent_id=None, user_id=None, input_data=None, output_data=None, metadata=None, response_time=None, status=None, error_message=None)

- **الوصف**: تسجيل حدث أداء
- **المعاملات**:
  - `event_type`: نوع الحدث
  - `actor_agent_id`: معرف الوكيل الفاعل (اختياري)
  - `target_agent_id`: معرف الوكيل المستهدف (اختياري)
  - `user_id`: معرف المستخدم (اختياري)
  - `input_data`: بيانات الإدخال (اختياري)
  - `output_data`: بيانات الإخراج (اختياري)
  - `metadata`: بيانات وصفية (اختياري)
  - `response_time`: زمن الاستجابة (اختياري)
  - `status`: الحالة (اختياري)
  - `error_message`: رسالة الخطأ (اختياري)
- **القيمة المرجعة**: سجل الأداء المنشأ

#### get_agent_performance(agent_id, start_time=None, end_time=None)

- **الوصف**: الحصول على أداء وكيل
- **المعاملات**:
  - `agent_id`: معرف الوكيل
  - `start_time`: وقت البدء (اختياري)
  - `end_time`: وقت الانتهاء (اختياري)
- **القيمة المرجعة**: إحصائيات أداء الوكيل

### خدمة الوكلاء الخارجيين (ExternalAgentService)

#### register_agent(name, provider_type, pricing_type, api_key=None, api_endpoint=None, model_name=None, capabilities=None, rate_limits=None, config=None)

- **الوصف**: تسجيل وكيل خارجي
- **المعاملات**:
  - `name`: اسم الوكيل
  - `provider_type`: نوع المزود
  - `pricing_type`: نوع التسعير
  - `api_key`: مفتاح واجهة برمجة التطبيقات (اختياري)
  - `api_endpoint`: نقطة نهاية واجهة برمجة التطبيقات (اختياري)
  - `model_name`: اسم النموذج (اختياري)
  - `capabilities`: القدرات (اختياري)
  - `rate_limits`: حدود معدل الاستخدام (اختياري)
  - `config`: إعدادات التكوين (اختياري)
- **القيمة المرجعة**: الوكيل الخارجي المسجل

#### get_active_agents(provider_type=None, capabilities=None)

- **الوصف**: الحصول على الوكلاء النشطين
- **المعاملات**:
  - `provider_type`: نوع المزود (اختياري)
  - `capabilities`: القدرات المطلوبة (اختياري)
- **القيمة المرجعة**: قائمة بالوكلاء الخارجيين النشطين

### خدمة التوجيه (RouterService)

#### create_router(name, routing_strategy, routing_rules=None, failover_settings=None, load_balancing_window=60, config=None)

- **الوصف**: إنشاء موجه
- **المعاملات**:
  - `name`: اسم الموجه
  - `routing_strategy`: استراتيجية التوجيه
  - `routing_rules`: قواعد التوجيه (اختياري)
  - `failover_settings`: إعدادات التحويل التلقائي (اختياري)
  - `load_balancing_window`: نافذة توازن الحمل (اختياري)
  - `config`: إعدادات التكوين (اختياري)
- **القيمة المرجعة**: الموجه المنشأ

#### route_request(router_id, request, user_id=None)

- **الوصف**: توجيه طلب
- **المعاملات**:
  - `router_id`: معرف الموجه
  - `request`: الطلب
  - `user_id`: معرف المستخدم (اختياري)
- **القيمة المرجعة**: الوكيل المختار للطلب

### خدمة الصلاحيات (PermissionService)

#### grant_permission(agent_id, permission_type, resource_type, resource_id=None, conditions=None, scope=None, granted_by=None, expires_at=None)

- **الوصف**: منح صلاحية
- **المعاملات**:
  - `agent_id`: معرف الوكيل
  - `permission_type`: نوع الصلاحية
  - `resource_type`: نوع المورد
  - `resource_id`: معرف المورد (اختياري)
  - `conditions`: شروط (اختياري)
  - `scope`: نطاق (اختياري)
  - `granted_by`: الممنوح من قبل (اختياري)
  - `expires_at`: وقت انتهاء الصلاحية (اختياري)
- **القيمة المرجعة**: الصلاحية الممنوحة

#### check_permission(agent_id, permission_type, resource_type, resource_id=None)

- **الوصف**: التحقق من صلاحية
- **المعاملات**:
  - `agent_id`: معرف الوكيل
  - `permission_type`: نوع الصلاحية
  - `resource_type`: نوع المورد
  - `resource_id`: معرف المورد (اختياري)
- **القيمة المرجعة**: قيمة منطقية تشير إلى وجود الصلاحية

## وحدة التوجيه متعدد الوكلاء (multi_agent_router.py)

### MultiAgentRouter

#### **init**(self, db_session, external_agent_service, performance_service)

- **الوصف**: تهيئة موجه متعدد الوكلاء
- **المعاملات**:
  - `db_session`: جلسة قاعدة البيانات
  - `external_agent_service`: خدمة الوكلاء الخارجيين
  - `performance_service`: خدمة الأداء

#### route_request(self, request, user_id=None, user_preferences=None)

- **الوصف**: توجيه طلب إلى الوكيل المناسب
- **المعاملات**:
  - `request`: الطلب
  - `user_id`: معرف المستخدم (اختياري)
  - `user_preferences`: تفضيلات المستخدم (اختياري)
- **القيمة المرجعة**: استجابة الوكيل المختار

#### process_request(self, request, agent_id)

- **الوصف**: معالجة طلب باستخدام وكيل محدد
- **المعاملات**:
  - `request`: الطلب
  - `agent_id`: معرف الوكيل
- **القيمة المرجعة**: استجابة الوكيل

## وحدة موازنة الحمل (load_balancer.py)

### LoadBalancer

#### **init**(self, db_session, external_agent_service)

- **الوصف**: تهيئة موازن الحمل
- **المعاملات**:
  - `db_session`: جلسة قاعدة البيانات
  - `external_agent_service`: خدمة الوكلاء الخارجيين

#### get_least_loaded_agent(self, agents)

- **الوصف**: الحصول على الوكيل الأقل حملاً
- **المعاملات**:
  - `agents`: قائمة الوكلاء
- **القيمة المرجعة**: الوكيل الأقل حملاً

#### get_agent_by_strategy(self, agents, strategy, request=None)

- **الوصف**: الحصول على وكيل باستخدام استراتيجية محددة
- **المعاملات**:
  - `agents`: قائمة الوكلاء
  - `strategy`: استراتيجية الاختيار
  - `request`: الطلب (اختياري)
- **القيمة المرجعة**: الوكيل المختار

## وحدة محلل الاستخدام (usage_analyzer.py)

### UsageAnalyzer

#### **init**(self, db_session)

- **الوصف**: تهيئة محلل الاستخدام
- **المعاملات**:
  - `db_session`: جلسة قاعدة البيانات

#### get_agent_usage(self, agent_id, start_time=None, end_time=None)

- **الوصف**: الحصول على استخدام وكيل
- **المعاملات**:
  - `agent_id`: معرف الوكيل
  - `start_time`: وقت البدء (اختياري)
  - `end_time`: وقت الانتهاء (اختياري)
- **القيمة المرجعة**: إحصائيات استخدام الوكيل

#### get_user_agent_interactions(self, user_id, agent_id=None, start_time=None, end_time=None)

- **الوصف**: الحصول على تفاعلات المستخدم مع الوكلاء
- **المعاملات**:
  - `user_id`: معرف المستخدم
  - `agent_id`: معرف الوكيل (اختياري)
  - `start_time`: وقت البدء (اختياري)
  - `end_time`: وقت الانتهاء (اختياري)
- **القيمة المرجعة**: تفاعلات المستخدم مع الوكلاء

#### generate_usage_report(self, start_time=None, end_time=None, group_by='agent')

- **الوصف**: إنشاء تقرير استخدام
- **المعاملات**:
  - `start_time`: وقت البدء (اختياري)
  - `end_time`: وقت الانتهاء (اختياري)
  - `group_by`: التجميع حسب (اختياري)
- **القيمة المرجعة**: تقرير الاستخدام

## وحدة الاتصال بالوكلاء (ai_connectors/base_connector.py)

### BaseConnector

#### **init**(self, config)

- **الوصف**: تهيئة موصل أساسي
- **المعاملات**:
  - `config`: إعدادات التكوين

#### process_request(self, request)

- **الوصف**: معالجة طلب
- **المعاملات**:
  - `request`: الطلب
- **القيمة المرجعة**: استجابة الطلب

#### validate_request(self, request)

- **الوصف**: التحقق من صحة الطلب
- **المعاملات**:
  - `request`: الطلب
- **القيمة المرجعة**: قيمة منطقية تشير إلى صحة الطلب

#### format_response(self, response)

- **الوصف**: تنسيق الاستجابة
- **المعاملات**:
  - `response`: الاستجابة
- **القيمة المرجعة**: الاستجابة المنسقة
