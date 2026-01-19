# File:
# /home/ubuntu/ai_web_organized/src/modules/ai_management/multi_agent_router.py
"""
نظام توجيه متقدم متعدد الوكلاء للذكاء الاصطناعي
يوفر هذا الملف فئة لتوجيه الطلبات إلى وكلاء ذكاء اصطناعي متعددين
"""

import logging
import time
from datetime import datetime, timezone
from typing import Dict, Optional

from memory_and_learning import (
    EventType,
    ExternalAgentService,
    PerformanceService,
    RoutingStrategy,
)

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MultiAgentRouter:
    """موجه متعدد الوكلاء للذكاء الاصطناعي"""

    def __init__(
            self,
            external_agent_service: ExternalAgentService,
            performance_service: PerformanceService):
        """
        تهيئة موجه متعدد الوكلاء

        Args:
            external_agent_service: خدمة الوكلاء الخارجيين
            performance_service: خدمة تسجيل الأداء
        """
        self.external_agent_service = external_agent_service
        self.performance_service = performance_service
        self.last_agent_index = 0
        self.agent_load = {}

    def route_request(
            self,
            request: Dict,
            user_id: Optional[str] = None,
            strategy: RoutingStrategy = RoutingStrategy.ROUND_ROBIN) -> Dict:
        """
        توجيه طلب إلى الوكيل المناسب

        Args:
            request: الطلب المراد توجيهه
            user_id: معرف المستخدم (اختياري)
            strategy: استراتيجية التوجيه

        Returns:
            استجابة الوكيل
        """
        # الحصول على الوكلاء النشطين
        agents = self.external_agent_service.get_active_agents()

        if not agents:
            logger.error("لا توجد وكلاء نشطة متاحة")
            return {"error": "لا توجد وكلاء نشطة متاحة"}

        # اختيار الوكيل المناسب
        agent = self._select_agent(agents, request, strategy)

        if not agent:
            logger.error("فشل في اختيار وكيل مناسب")
            return {"error": "فشل في اختيار وكيل مناسب"}

        # تسجيل بداية الطلب
        start_time = time.time()

        try:
            # معالجة الطلب
            response = self._process_request(agent, request)

            # حساب وقت الاستجابة
            response_time = time.time() - start_time

            # تسجيل الحدث
            self.performance_service.log_event(
                event_type=EventType.USER_MESSAGE,
                actor_agent_id=str(agent.id),
                user_id=user_id,
                input_data=request,
                output_data=response,
                response_time=response_time,
                status="success"
            )

            # تحديث إحصائيات الاستخدام
            self.external_agent_service.update_usage_stats(agent.id)

            return response

        except Exception as e:
            # تسجيل الخطأ
            logger.error("خطأ أثناء معالجة الطلب: %s", str(e))

            # تسجيل الحدث
            self.performance_service.log_event(
                event_type=EventType.ERROR,
                actor_agent_id=str(agent.id),
                user_id=user_id,
                input_data=request,
                error_message=str(e),
                status="error"
            )

            # محاولة التحويل التلقائي
            return self._failover(agents, agent, request, user_id, strategy)

    def _select_agent(self, agents, request, strategy):
        """
        اختيار الوكيل المناسب بناءً على الاستراتيجية

        Args:
            agents: قائمة الوكلاء المتاحين
            request: الطلب المراد توجيهه
            strategy: استراتيجية التوجيه

        Returns:
            الوكيل المختار
        """
        if strategy == RoutingStrategy.ROUND_ROBIN:
            # التناوب الدائري
            if not agents:
                return None

            agent = agents[self.last_agent_index % len(agents)]
            self.last_agent_index += 1
            return agent

        elif strategy == RoutingStrategy.LEAST_LOAD:
            # الحمل الأقل
            if not agents:
                return None

            # تحديث الحمل لجميع الوكلاء
            for agent in agents:
                if agent.id not in self.agent_load:
                    self.agent_load[agent.id] = 0

            # اختيار الوكيل ذو الحمل الأقل
            agent_id = min(self.agent_load, key=self.agent_load.get)

            # زيادة الحمل للوكيل المختار
            self.agent_load[agent_id] += 1

            # العثور على الوكيل
            for agent in agents:
                if agent.id == agent_id:
                    return agent

            return agents[0]

        elif strategy == RoutingStrategy.CAPABILITY:
            # القدرة
            if "request_type" in request:
                request_type = request["request_type"]
                for agent in agents:
                    if agent.capabilities and request_type in agent.capabilities and agent.capabilities[
                            request_type]:
                        return agent

            return agents[0] if agents else None

        elif strategy == RoutingStrategy.PRIORITY:
            # الأولوية
            # في التنفيذ الحقيقي، يجب تحديد الأولويات
            return agents[0] if agents else None

        elif strategy == RoutingStrategy.RULE_BASED:
            # القواعد
            # في التنفيذ الحقيقي، يجب تنفيذ منطق القواعد
            return agents[0] if agents else None

        elif strategy == RoutingStrategy.FAILOVER:
            # التحويل التلقائي
            # في التنفيذ الحقيقي، يجب تحديد الوكيل الأساسي والوكلاء الاحتياطية
            return agents[0] if agents else None

        # الاستراتيجية الافتراضية
        return agents[0] if agents else None

    def _process_request(self, agent, request):
        """
        معالجة الطلب باستخدام الوكيل المحدد

        Args:
            agent: الوكيل المستخدم لمعالجة الطلب
            request: الطلب المراد معالجته

        Returns:
            استجابة الوكيل
        """
        # في التنفيذ الحقيقي، يجب إرسال الطلب إلى الوكيل وانتظار الاستجابة
        # هذا مجرد تنفيذ وهمي

        # محاكاة معالجة الطلب
        if "query" in request:
            return {
                "response": f"استجابة من الوكيل {agent.name} للاستعلام: {request['query']}",
                "agent_id": agent.id,
                "timestamp": datetime.now(
                    timezone.utc).isoformat()}

        return {
            "response": f"استجابة من الوكيل {agent.name}",
            "agent_id": agent.id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _failover(self, agents, failed_agent, request, user_id, strategy):
        """
        التحويل التلقائي في حالة فشل الوكيل

        Args:
            agents: قائمة الوكلاء المتاحين
            failed_agent: الوكيل الذي فشل
            request: الطلب المراد توجيهه
            user_id: معرف المستخدم
            strategy: استراتيجية التوجيه

        Returns:
            استجابة الوكيل البديل أو رسالة خطأ
        """
        # استبعاد الوكيل الذي فشل
        available_agents = [
            agent for agent in agents if agent.id != failed_agent.id]

        if not available_agents:
            logger.error("لا توجد وكلاء بديلة متاحة للتحويل التلقائي")
            return {"error": "فشل في معالجة الطلب ولا توجد وكلاء بديلة متاحة"}

        # اختيار وكيل بديل
        backup_agent = available_agents[0]

        logger.info(
            "التحويل التلقائي من الوكيل %s إلى الوكيل {backup_agent.id}",
            failed_agent.id)

        try:
            # معالجة الطلب باستخدام الوكيل البديل
            response = self._process_request(backup_agent, request)

            # تسجيل الحدث
            self.performance_service.log_event(
                event_type=EventType.USER_MESSAGE,
                actor_agent_id=str(backup_agent.id),
                user_id=user_id,
                input_data=request,
                output_data=response,
                meta_info={"failover_from": str(failed_agent.id)},
                status="success"
            )

            # تحديث إحصائيات الاستخدام
            self.external_agent_service.update_usage_stats(backup_agent.id)

            return response

        except Exception as e:
            # تسجيل الخطأ
            logger.error("خطأ أثناء التحويل التلقائي: %s", str(e))

            # تسجيل الحدث
            self.performance_service.log_event(
                event_type=EventType.ERROR,
                actor_agent_id=str(backup_agent.id),
                user_id=user_id,
                input_data=request,
                error_message=str(e),
                meta_info={"failover_from": str(failed_agent.id)},
                status="error"
            )

            return {"error": "فشل في معالجة الطلب حتى بعد التحويل التلقائي"}
