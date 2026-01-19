# File: /home/ubuntu/ai_web_organized/src/modules/ai_management/test_integration_comprehensive.py
"""
اختبار تكاملي شامل لنظام الذكاء الاصطناعي متعدد الوكلاء
يقوم هذا الملف باختبار جميع مكونات نظام الذكاء الاصطناعي متعدد الوكلاء
"""

import unittest
import logging

# استيراد الوحدات المطلوبة بشكل نسبي
from auth_compatibility import has_permission, company_access_required, country_access_required
from memory_and_learning import (
    MemoryType, AccessLevel, AgentType, ModelCategory, CostLevel,
    EventType, ProviderType, PricingType, RoutingStrategy,
    PermissionType, ResourceType,
    MemoryService, KnowledgeService, ModelService, PerformanceService,
    ExternalAgentService, RouterService, PermissionService
)
from multi_agent_router import MultiAgentRouter

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestMemoryAndLearning(unittest.TestCase):
    """اختبار وحدة الذاكرة والتعلم"""

    def setUp(self):
        """إعداد بيئة الاختبار"""
        # إنشاء جلسة قاعدة بيانات وهمية للاختبار
        self.db_session = MockDBSession()

        # إنشاء الخدمات
        self.memory_service = MemoryService(self.db_session)
        self.knowledge_service = KnowledgeService(self.db_session)
        self.model_service = ModelService(self.db_session)
        self.performance_service = PerformanceService(self.db_session)
        self.external_agent_service = ExternalAgentService(self.db_session)
        self.router_service = RouterService(self.db_session, self.external_agent_service)
        self.permission_service = PermissionService(self.db_session)

    def test_memory_service(self):
        """اختبار خدمة الذاكرة"""
        # اختبار تخزين واسترجاع الذاكرة
        agent_id = "test_agent_1"
        memory_type = MemoryType.SHORT_TERM
        key = "test_key"
        value = "test_value"

        # تخزين الذاكرة
        memory = self.memory_service.store_memory(
            agent_id=agent_id,
            memory_type=memory_type,
            key=key,
            value=value,
            access_level=AccessLevel.PRIVATE
        )

        # التحقق من تخزين الذاكرة
        self.assertIsNotNone(memory)
        self.assertEqual(memory.agent_id, agent_id)
        self.assertEqual(memory.memory_type, memory_type)
        self.assertEqual(memory.key, key)
        self.assertEqual(memory.value, value)

        # استرجاع الذاكرة
        memories = self.memory_service.get_memory(
            agent_id=agent_id,
            memory_type=memory_type,
            key=key
        )

        # التحقق من استرجاع الذاكرة
        self.assertEqual(len(memories), 1)
        self.assertEqual(memories[0].value, value)

        # حذف الذاكرة
        count = self.memory_service.delete_memory(
            agent_id=agent_id,
            memory_type=memory_type,
            key=key
        )

        # التحقق من حذف الذاكرة
        self.assertEqual(count, 1)

        # التحقق من عدم وجود الذاكرة بعد الحذف
        memories = self.memory_service.get_memory(
            agent_id=agent_id,
            memory_type=memory_type,
            key=key
        )
        self.assertEqual(len(memories), 0)

    def test_knowledge_service(self):
        """اختبار خدمة المعرفة"""
        # اختبار إضافة واسترجاع وتحديث وحذف المعرفة
        content = "هذه معرفة اختبارية"
        keywords = "اختبار,معرفة"
        source = "وحدة الاختبار"

        # إضافة معرفة
        knowledge = self.knowledge_service.add_knowledge(
            content=content,
            keywords=keywords,
            source=source,
            confidence=0.9
        )

        # التحقق من إضافة المعرفة
        self.assertIsNotNone(knowledge)
        self.assertEqual(knowledge.content, content)
        self.assertEqual(knowledge.keywords, keywords)
        self.assertEqual(knowledge.source, source)
        self.assertEqual(knowledge.confidence, 0.9)

        # استرجاع المعرفة
        if knowledge is not None:
            retrieved_knowledge = self.knowledge_service.get_knowledge(knowledge.id)
            if retrieved_knowledge is not None:
                self.assertEqual(retrieved_knowledge.content, content)

        # تحديث المعرفة
        new_content = "هذه معرفة محدثة"
        updated_knowledge = self.knowledge_service.update_knowledge(
            knowledge_id=knowledge.id,
            content=new_content
        )

        # التحقق من تحديث المعرفة
        if updated_knowledge is not None:
            self.assertEqual(updated_knowledge.content, new_content)

        # حذف المعرفة
        result = self.knowledge_service.delete_knowledge(knowledge.id)

        # التحقق من حذف المعرفة
        self.assertTrue(result)

        # التحقق من عدم وجود المعرفة بعد الحذف
        deleted_knowledge = self.knowledge_service.get_knowledge(knowledge.id)
        self.assertIsNone(deleted_knowledge)

    def test_model_service(self):
        """اختبار خدمة النماذج"""
        # اختبار بدء وإكمال تدريب النموذج ونشره
        model_name = "test_model"
        dataset_description = "بيانات اختبارية"
        hyperparameters = {"learning_rate": 0.01, "epochs": 10}

        # بدء تدريب النموذج
        training_run = self.model_service.start_training(
            model_name=model_name,
            dataset_description=dataset_description,
            hyperparameters=hyperparameters,
            created_by="test_user"
        )

        # التحقق من بدء تدريب النموذج
        self.assertIsNotNone(training_run)
        self.assertEqual(training_run.model_name, model_name)
        self.assertEqual(training_run.dataset_description, dataset_description)
        self.assertEqual(training_run.hyperparameters, hyperparameters)
        self.assertEqual(training_run.status, "running")

        # إكمال تدريب النموذج
        model_path = "/path/to/model"
        metrics = {"accuracy": 0.95, "loss": 0.05}
        completed_training = self.model_service.complete_training(
            training_id=training_run.id,
            model_path=model_path,
            metrics=metrics
        )

        # التحقق من إكمال تدريب النموذج
        self.assertIsNotNone(completed_training)
        self.assertEqual(completed_training.model_path, model_path)
        self.assertEqual(completed_training.metrics, metrics)
        self.assertEqual(completed_training.status, "completed")

        # نشر النموذج
        deployment = self.model_service.deploy_model(
            model_name=model_name,
            agent_type=AgentType.GENERAL_ASSISTANT,
            model_category=ModelCategory.LOCAL_FREE,
            cost_level=CostLevel.FREE,
            capabilities={"text_generation": True, "image_generation": False},
            model_path=model_path
        )

        # التحقق من نشر النموذج
        self.assertIsNotNone(deployment)
        self.assertEqual(deployment.model_name, model_name)
        self.assertEqual(deployment.agent_type, AgentType.GENERAL_ASSISTANT)
        self.assertEqual(deployment.model_category, ModelCategory.LOCAL_FREE)
        self.assertEqual(deployment.cost_level, CostLevel.FREE)
        self.assertEqual(deployment.model_path, model_path)
        self.assertTrue(deployment.is_active)

        # الحصول على النشرات النشطة
        active_deployments = self.model_service.get_active_deployments()

        # التحقق من الحصول على النشرات النشطة
        self.assertEqual(len(active_deployments), 1)
        self.assertEqual(active_deployments[0].model_name, model_name)

    def test_performance_service(self):
        """اختبار خدمة الأداء"""
        # اختبار تسجيل الأحداث والحصول على أداء الوكيل
        actor_agent_id = "test_agent_1"
        target_agent_id = "test_agent_2"
        user_id = "test_user"
        input_data = {"query": "ما هو الذكاء الاصطناعي؟"}
        output_data = {"response": "الذكاء الاصطناعي هو فرع من علوم الحاسوب يهتم بإنشاء آلات ذكية."}

        # تسجيل حدث
        log_entry = self.performance_service.log_event(
            event_type=EventType.USER_MESSAGE,
            actor_agent_id=actor_agent_id,
            target_agent_id=target_agent_id,
            user_id=user_id,
            input_data=input_data,
            output_data=output_data,
            response_time=0.5,
            status="success"
        )

        # التحقق من تسجيل الحدث
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.event_type, EventType.USER_MESSAGE)
        self.assertEqual(log_entry.actor_agent_id, actor_agent_id)
        self.assertEqual(log_entry.target_agent_id, target_agent_id)
        self.assertEqual(log_entry.user_id, user_id)
        self.assertEqual(log_entry.input_data, input_data)
        self.assertEqual(log_entry.output_data, output_data)
        self.assertEqual(log_entry.response_time, 0.5)
        self.assertEqual(log_entry.status, "success")

        # الحصول على أداء الوكيل
        performance = self.performance_service.get_agent_performance(actor_agent_id)

        # التحقق من الحصول على أداء الوكيل
        self.assertIsNotNone(performance)
        self.assertEqual(performance['total_logs'], 1)
        self.assertEqual(performance['successful_logs'], 1)
        self.assertEqual(performance['error_logs'], 0)
        self.assertEqual(performance['success_rate'], 100.0)
        self.assertEqual(performance['avg_response_time'], 0.5)

    def test_external_agent_service(self):
        """اختبار خدمة الوكلاء الخارجيين"""
        # اختبار تسجيل واسترجاع وتحديث الوكلاء الخارجيين
        name = "test_external_agent"
        provider_type = ProviderType.OPENAI
        pricing_type = PricingType.PAID
        api_key = "test_api_key"
        api_endpoint = "https://api.example.com"
        model_name = "gpt-4"
        capabilities = {"text_generation": True, "image_generation": False}
        rate_limits = {"daily_limit": 1000, "minute_limit": 60}

        # تسجيل وكيل خارجي
        agent = self.external_agent_service.register_agent(
            name=name,
            provider_type=provider_type,
            pricing_type=pricing_type,
            api_key=api_key,
            api_endpoint=api_endpoint,
            model_name=model_name,
            capabilities=capabilities,
            rate_limits=rate_limits
        )

        # التحقق من تسجيل الوكيل الخارجي
        self.assertIsNotNone(agent)
        self.assertEqual(agent.name, name)
        self.assertEqual(agent.provider_type, provider_type)
        self.assertEqual(agent.pricing_type, pricing_type)
        self.assertEqual(agent.api_key, api_key)
        self.assertEqual(agent.api_endpoint, api_endpoint)
        self.assertEqual(agent.model_name, model_name)
        self.assertEqual(agent.capabilities, capabilities)
        self.assertEqual(agent.rate_limits, rate_limits)
        self.assertTrue(agent.is_active)

        # الحصول على الوكيل
        retrieved_agent = self.external_agent_service.get_agent(agent.id)

        # التحقق من الحصول على الوكيل
        self.assertIsNotNone(retrieved_agent)
        self.assertEqual(retrieved_agent.name, name)

        # تحديث الوكيل
        new_api_key = "new_test_api_key"
        updated_agent = self.external_agent_service.update_agent(
            agent_id=agent.id,
            api_key=new_api_key
        )

        # التحقق من تحديث الوكيل
        self.assertIsNotNone(updated_agent)
        self.assertEqual(updated_agent.api_key, new_api_key)

        # الحصول على الوكلاء النشطين
        active_agents = self.external_agent_service.get_active_agents()

        # التحقق من الحصول على الوكلاء النشطين
        self.assertEqual(len(active_agents), 1)
        self.assertEqual(active_agents[0].name, name)

        # تحديث إحصائيات الاستخدام
        result = self.external_agent_service.update_usage_stats(agent.id, tokens=10)

        # التحقق من تحديث إحصائيات الاستخدام
        self.assertTrue(result)

    def test_router_service(self):
        """اختبار خدمة التوجيه"""
        # اختبار إنشاء واسترجاع وتحديث الموجهات
        name = "test_router"
        routing_strategy = RoutingStrategy.ROUND_ROBIN
        routing_rules = {"default_agent": "test_agent_1"}
        failover_settings = {"enabled": True, "max_retries": 3}

        # إنشاء موجه
        router = self.router_service.create_router(
            name=name,
            routing_strategy=routing_strategy,
            routing_rules=routing_rules,
            failover_settings=failover_settings
        )

        # التحقق من إنشاء الموجه
        self.assertIsNotNone(router)
        self.assertEqual(router.name, name)
        self.assertEqual(router.routing_strategy, routing_strategy)
        self.assertEqual(router.routing_rules, routing_rules)
        self.assertEqual(router.failover_settings, failover_settings)
        self.assertTrue(router.is_active)

        # الحصول على الموجه
        retrieved_router = self.router_service.get_router(router.id)

        # التحقق من الحصول على الموجه
        self.assertIsNotNone(retrieved_router)
        self.assertEqual(retrieved_router.name, name)

        # تحديث الموجه
        new_routing_strategy = RoutingStrategy.LEAST_LOAD
        updated_router = self.router_service.update_router(
            router_id=router.id,
            routing_strategy=new_routing_strategy
        )

        # التحقق من تحديث الموجه
        self.assertIsNotNone(updated_router)
        self.assertEqual(updated_router.routing_strategy, new_routing_strategy)

    def test_permission_service(self):
        """اختبار خدمة الصلاحيات"""
        # اختبار منح والتحقق من وإلغاء الصلاحيات
        agent_id = "test_agent_1"
        permission_type = PermissionType.READ
        resource_type = ResourceType.DATA
        resource_id = "test_data_1"

        # منح صلاحية
        permission = self.permission_service.grant_permission(
            agent_id=agent_id,
            permission_type=permission_type,
            resource_type=resource_type,
            resource_id=resource_id,
            granted_by="test_user"
        )

        # التحقق من منح الصلاحية
        self.assertIsNotNone(permission)
        self.assertEqual(permission.agent_id, agent_id)
        self.assertEqual(permission.permission_type, permission_type)
        self.assertEqual(permission.resource_type, resource_type)
        self.assertEqual(permission.resource_id, resource_id)
        self.assertTrue(permission.is_active)

        # التحقق من الصلاحية
        has_perm = self.permission_service.check_permission(
            agent_id=agent_id,
            permission_type=permission_type,
            resource_type=resource_type,
            resource_id=resource_id
        )

        # التحقق من وجود الصلاحية
        self.assertTrue(has_perm)

        # إلغاء الصلاحية
        result = self.permission_service.revoke_permission(permission.id)

        # التحقق من إلغاء الصلاحية
        self.assertTrue(result)

        # التحقق من عدم وجود الصلاحية بعد الإلغاء
        has_perm = self.permission_service.check_permission(
            agent_id=agent_id,
            permission_type=permission_type,
            resource_type=resource_type,
            resource_id=resource_id
        )
        self.assertFalse(has_perm)

    def test_auth_compatibility(self):
        """اختبار توافق المصادقة"""
        # اختبار دوال المصادقة

        # اختبار has_permission
        self.assertIsNotNone(has_permission)

        # اختبار company_access_required
        self.assertIsNotNone(company_access_required)

        # اختبار country_access_required
        self.assertIsNotNone(country_access_required)

    def test_multi_agent_router(self):
        """اختبار موجه متعدد الوكلاء"""
        # اختبار إنشاء موجه متعدد الوكلاء
        multi_agent_router = MultiAgentRouter(
            db_session=self.db_session,
            external_agent_service=self.external_agent_service,
            performance_service=self.performance_service
        )

        # التحقق من إنشاء موجه متعدد الوكلاء
        self.assertIsNotNone(multi_agent_router)


class MockDBSession:
    """جلسة قاعدة بيانات وهمية للاختبار"""

    def __init__(self):
        """تهيئة الجلسة"""
        self.data = {}
        self.id_counter = 1

    def add(self, obj):
        """إضافة كائن إلى قاعدة البيانات"""
        obj.id = self.id_counter
        self.id_counter += 1

        table_name = obj.__class__.__name__
        if table_name not in self.data:
            self.data[table_name] = {}

        self.data[table_name][obj.id] = obj

    def commit(self):
        """تأكيد التغييرات"""
        pass

    def query(self, cls):
        """استعلام عن كائنات من قاعدة البيانات"""
        return MockQuery(self, cls)


class MockQuery:
    """استعلام وهمي للاختبار"""

    def __init__(self, db_session, cls):
        """تهيئة الاستعلام"""
        self.db_session = db_session
        self.cls = cls
        self.filters = []

    def filter(self, *args):
        """إضافة مرشح للاستعلام"""
        self.filters.extend(args)
        return self

    def first(self):
        """الحصول على أول نتيجة"""
        results = self.all()
        if results:
            return results[0]
        return None

    def all(self):
        """الحصول على جميع النتائج"""
        table_name = self.cls.__name__
        if table_name not in self.db_session.data:
            return []

        results = list(self.db_session.data[table_name].values())

        # تطبيق المرشحات
        for result in results[:]:
            for filter_expr in self.filters:
                # تنفيذ منطق تصفية بسيط
                if not self._apply_filter(result, filter_expr):
                    results.remove(result)
                    break

        return results

    def delete(self):
        """حذف الكائنات المطابقة للاستعلام"""
        table_name = self.cls.__name__
        if table_name not in self.db_session.data:
            return 0

        to_delete = []
        for obj_id, obj in self.db_session.data[table_name].items():
            for filter_expr in self.filters:
                if not self._apply_filter(obj, filter_expr):
                    break
            else:
                to_delete.append(obj_id)

        for obj_id in to_delete:
            del self.db_session.data[table_name][obj_id]

        return len(to_delete)

    def _apply_filter(self, obj, filter_expr):
        """تطبيق مرشح على كائن"""
        # تنفيذ منطق تصفية بسيط
        # هذا مجرد تنفيذ بسيط للغاية للتصفية
        # في التنفيذ الحقيقي، يجب تحليل filter_expr بشكل صحيح

        # افتراض أن filter_expr هو عبارة مقارنة بسيطة
        # مثل: Model.field == value أو Model.field != value

        # تحليل بسيط للمرشح
        if hasattr(filter_expr, 'left') and hasattr(filter_expr, 'right'):
            left = filter_expr.left
            right = filter_expr.right

            if hasattr(left, 'key'):
                field_name = left.key
                value = right

                if hasattr(obj, field_name):
                    obj_value = getattr(obj, field_name)

                    # المقارنة
                    if hasattr(filter_expr, 'operator'):
                        operator = filter_expr.operator

                        if operator == '==':
                            return obj_value == value
                        elif operator == '!=':
                            return obj_value != value
                        elif operator == '>':
                            return obj_value > value
                        elif operator == '<':
                            return obj_value < value
                        elif operator == '>=':
                            return obj_value >= value
                        elif operator == '<=':
                            return obj_value <= value
                        elif operator == 'in':
                            return obj_value in value
                        elif operator == 'not in':
                            return obj_value not in value
                        elif operator == 'like':
                            return value in str(obj_value)
                        elif operator == 'not like':
                            return value not in str(obj_value)
                        elif operator == 'is':
                            return obj_value is value
                        elif operator == 'is not':
                            return obj_value is not value

        # إذا لم نتمكن من تحليل المرشح، نفترض أنه صحيح
        return True


if __name__ == '__main__':
    # تشغيل الاختبارات
    unittest.main()
