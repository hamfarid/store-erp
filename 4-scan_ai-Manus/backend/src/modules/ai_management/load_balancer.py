# File:
# /home/ubuntu/ai_web_organized/src/modules/ai_management/load_balancer.py
"""
from flask import g
آلية توازن الحمل والتحويل التلقائي بين وكلاء الذكاء الاصطناعي
يوفر هذا الملف آليات لتوزيع الحمل وإدارة الفشل بين وكلاء الذكاء الاصطناعي المختلفين
"""

import logging
import random
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class LoadBalancerError(Exception):
    """خطأ في موازن الحمل"""


class NoAvailableAgentsError(LoadBalancerError):
    """لا توجد وكلاء متاحة"""


class AgentSelectionError(LoadBalancerError):
    """خطأ في اختيار الوكيل"""


class LoadBalancer:
    """فئة موازن الحمل بين وكلاء الذكاء الاصطناعي"""

    def __init__(self, db_service, strategy: str = "priority"):
        """
        تهيئة موازن الحمل

        المعلمات:
            db_service: خدمة قاعدة البيانات للوصول إلى معلومات الوكلاء
            strategy (str): استراتيجية توازن الحمل (priority, round_robin, random, cost)
        """
        self.db_service = db_service
        self.strategy = strategy
        self.last_agent_index = -1  # للاستراتيجية round_robin
        self.agent_usage_count = {}  # لتتبع عدد الاستخدامات لكل وكيل
        self.agent_error_count = {}  # لتتبع عدد الأخطاء لكل وكيل
        self.agent_response_times = {}  # لتتبع متوسط أوقات الاستجابة

        logger.info("تم تهيئة موازن الحمل باستراتيجية %s", strategy)

    def select_agent(
        self,
        request: Dict[str, Any],
        user_id: Optional[int] = None
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """
        اختيار وكيل مناسب للطلب

        المعلمات:
            request (dict): بيانات الطلب
            user_id (int, optional): معرف المستخدم

        العائد:
            tuple: (معرف الوكيل المختار، معلومات الوكيل)
        """
        try:
            # الحصول على قائمة الوكلاء المفعلين
            agents = self.db_service.get_enabled_agents()

            if not agents:
                logger.error("لا توجد وكلاء مفعلة متاحة")
                raise NoAvailableAgentsError("لا توجد وكلاء مفعلة متاحة")

            # تطبيق تصفية أولية بناءً على نوع الطلب
            filtered_agents = self._filter_agents_by_request_type(
                agents, request)

            if not filtered_agents:
                logger.warning(
                    "لا توجد وكلاء مناسبة لنوع الطلب، استخدام جميع الوكلاء المفعلة")
                filtered_agents = agents

            # تطبيق تصفية بناءً على تفضيلات المستخدم إذا كان متاحًا
            if user_id:
                filtered_agents = self._filter_agents_by_user_preferences(
                    filtered_agents, user_id)

            if not filtered_agents:
                logger.warning(
                    "لا توجد وكلاء متاحة بعد تطبيق تفضيلات المستخدم، استخدام جميع الوكلاء المفعلة")
                filtered_agents = agents

            # اختيار الوكيل بناءً على الاستراتيجية
            selected_agent = self._apply_selection_strategy(
                filtered_agents, request)

            if not selected_agent:
                logger.error("فشل في اختيار وكيل مناسب")
                raise AgentSelectionError("فشل في اختيار وكيل مناسب")

            logger.info("تم اختيار الوكيل %s للطلب", selected_agent['id'])

            return selected_agent['id'], selected_agent
        except LoadBalancerError:
            raise
        except Exception as e:
            logger.error("خطأ أثناء اختيار الوكيل: %s", str(e))
            raise LoadBalancerError(
                f"خطأ غير متوقع أثناء اختيار الوكيل: {str(e)}")

    def handle_failover(
        self,
        failed_agent_id: str,
        request: Dict[str, Any],
        error: Exception,
        user_id: Optional[int] = None
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """
        معالجة التحويل التلقائي في حالة فشل وكيل

        المعلمات:
            failed_agent_id (str): معرف الوكيل الذي فشل
            request (dict): بيانات الطلب
            error (Exception): الخطأ الذي حدث
            user_id (int, optional): معرف المستخدم

        العائد:
            tuple: (معرف الوكيل البديل، معلومات الوكيل)
        """
        try:
            # تسجيل الفشل
            self._record_agent_failure(failed_agent_id, error)

            # الحصول على قائمة الوكلاء المفعلين باستثناء الوكيل الذي فشل
            agents = self.db_service.get_enabled_agents()
            available_agents = [
                agent for agent in agents if agent['id'] != failed_agent_id]

            if not available_agents:
                logger.error("لا توجد وكلاء بديلة متاحة للتحويل التلقائي")
                raise NoAvailableAgentsError(
                    "لا توجد وكلاء بديلة متاحة للتحويل التلقائي")

            # تطبيق تصفية أولية بناءً على نوع الطلب
            filtered_agents = self._filter_agents_by_request_type(
                available_agents, request)

            if not filtered_agents:
                logger.warning(
                    "لا توجد وكلاء بديلة مناسبة لنوع الطلب، استخدام جميع الوكلاء المتاحة")
                filtered_agents = available_agents

            # تطبيق تصفية بناءً على تفضيلات المستخدم إذا كان متاحًا
            if user_id:
                filtered_agents = self._filter_agents_by_user_preferences(
                    filtered_agents, user_id)

            if not filtered_agents:
                logger.warning(
                    "لا توجد وكلاء بديلة متاحة بعد تطبيق تفضيلات المستخدم، استخدام جميع الوكلاء المتاحة")
                filtered_agents = available_agents

            # اختيار الوكيل البديل بناءً على الاستراتيجية
            # استخدام استراتيجية مختلفة للتحويل التلقائي (الأولوية دائمًا)
            selected_agent = self._select_agent_by_priority(filtered_agents)

            if not selected_agent:
                logger.error("فشل في اختيار وكيل بديل للتحويل التلقائي")
                raise AgentSelectionError(
                    "فشل في اختيار وكيل بديل للتحويل التلقائي")

            logger.info(
                "تم اختيار الوكيل البديل %s للتحويل التلقائي بعد فشل الوكيل {failed_agent_id}",
                selected_agent['id'])

            # تسجيل التحويل التلقائي في قاعدة البيانات
            self.db_service.log_failover(
                request_id=request.get('request_id'),
                original_agent_id=failed_agent_id,
                new_agent_id=selected_agent['id'],
                error_message=str(error),
                user_id=user_id
            )

            return selected_agent['id'], selected_agent
        except LoadBalancerError:
            raise
        except Exception as e:
            logger.error("خطأ أثناء معالجة التحويل التلقائي: %s", str(e))
            raise LoadBalancerError(
                f"خطأ غير متوقع أثناء معالجة التحويل التلقائي: {str(e)}")

    def update_agent_stats(
            self,
            agent_id: str,
            response_time: float,
            success: bool,
            tokens: int = 0) -> None:
        """
        تحديث إحصائيات الوكيل

        المعلمات:
            agent_id (str): معرف الوكيل
            response_time (float): وقت الاستجابة بالثواني
            success (bool): هل كانت العملية ناجحة
            tokens (int): عدد الرموز المستخدمة
        """
        try:
            # تحديث عدد الاستخدامات
            if agent_id not in self.agent_usage_count:
                self.agent_usage_count[agent_id] = 0
            self.agent_usage_count[agent_id] += 1

            # تحديث عدد الأخطاء
            if not success:
                if agent_id not in self.agent_error_count:
                    self.agent_error_count[agent_id] = 0
                self.agent_error_count[agent_id] += 1

            # تحديث متوسط وقت الاستجابة
            if agent_id not in self.agent_response_times:
                self.agent_response_times[agent_id] = response_time
            else:
                # حساب المتوسط المتحرك
                current_avg = self.agent_response_times[agent_id]
                usage_count = self.agent_usage_count[agent_id]
                self.agent_response_times[agent_id] = (
                    (current_avg * (usage_count - 1)) + response_time) / usage_count

            # تحديث إحصائيات الوكيل في قاعدة البيانات
            self.db_service.update_agent_stats(
                agent_id=agent_id,
                response_time=response_time,
                success=success,
                tokens=tokens
            )

            logger.debug(
                "تم تحديث إحصائيات الوكيل %s: وقت الاستجابة={response_time}، نجاح={success}، الرموز={tokens}",
                agent_id)
        except Exception as e:
            logger.error("خطأ أثناء تحديث إحصائيات الوكيل: %s", str(e))

    def _filter_agents_by_request_type(
            self, agents: List[Dict[str, Any]], request: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        تصفية الوكلاء بناءً على نوع الطلب

        المعلمات:
            agents (list): قائمة الوكلاء
            request (dict): بيانات الطلب

        العائد:
            list: قائمة الوكلاء المصفاة
        """
        request_type = request.get('type', 'text')

        # تصفية الوكلاء بناءً على نوع الطلب
        if request_type == 'text':
            # جميع الوكلاء يمكنهم معالجة النصوص
            return agents
        elif request_type == 'image':
            # تصفية الوكلاء التي تدعم معالجة الصور
            return [agent for agent in agents if 'image_processing' in (
                agent.get('capabilities') or '').split(',')]
        elif request_type == 'audio':
            # تصفية الوكلاء التي تدعم معالجة الصوت
            return [agent for agent in agents if 'audio_processing' in (
                agent.get('capabilities') or '').split(',')]
        elif request_type == 'code':
            # تصفية الوكلاء التي تدعم معالجة الكود
            return [agent for agent in agents if 'code_generation' in (
                agent.get('capabilities') or '').split(',')]
        else:
            # إذا كان نوع الطلب غير معروف، استخدم جميع الوكلاء
            return agents

    def _filter_agents_by_user_preferences(
            self, agents: List[Dict[str, Any]], user_id: int) -> List[Dict[str, Any]]:
        """
        تصفية الوكلاء بناءً على تفضيلات المستخدم

        المعلمات:
            agents (list): قائمة الوكلاء
            user_id (int): معرف المستخدم

        العائد:
            list: قائمة الوكلاء المصفاة
        """
        try:
            # الحصول على تفضيلات المستخدم
            user_preferences = self.db_service.get_user_preferences(user_id)

            if not user_preferences:
                # إذا لم تكن هناك تفضيلات، استخدم جميع الوكلاء
                return agents

            # إذا كان هناك وكيل مفضل وهو موجود في القائمة، استخدمه فقط
            if user_preferences.get('preferred_agent_id'):
                preferred_agent = next(
                    (agent for agent in agents if agent['id']
                     == user_preferences['preferred_agent_id']),
                    None)
                if preferred_agent:
                    return [preferred_agent]

            # تصفية الوكلاء المستبعدة
            excluded_agents = (user_preferences.get(
                'excluded_agents') or '').split(',')
            filtered_agents = [
                agent for agent in agents if agent['id'] not in excluded_agents]

            # تصفية الوكلاء المسموح بها فقط إذا كانت محددة
            allowed_agents = (user_preferences.get(
                'allowed_agents') or '').split(',')
            # تأكد من أن القائمة ليست فارغة
            if allowed_agents and allowed_agents[0]:
                filtered_agents = [
                    agent for agent in filtered_agents if agent['id'] in allowed_agents]

            # إذا كانت القائمة المصفاة فارغة، استخدم جميع الوكلاء
            return filtered_agents or agents
        except Exception as e:
            logger.error(
                "خطأ أثناء تصفية الوكلاء بناءً على تفضيلات المستخدم: %s",
                str(e))
            return agents

    def _apply_selection_strategy(
            self, agents: List[Dict[str, Any]], request: Dict[str, Any]) -> Dict[str, Any]:
        """
        تطبيق استراتيجية اختيار الوكيل

        المعلمات:
            agents (list): قائمة الوكلاء
            request (dict): بيانات الطلب

        العائد:
            dict: الوكيل المختار
        """
        if not agents:
            return None

        if self.strategy == "priority":
            return self._select_agent_by_priority(agents)
        elif self.strategy == "round_robin":
            return self._select_agent_by_round_robin(agents)
        elif self.strategy == "random":
            return self._select_agent_by_random(agents)
        elif self.strategy == "cost":
            return self._select_agent_by_cost(agents, request)
        elif self.strategy == "response_time":
            return self._select_agent_by_response_time(agents)
        elif self.strategy == "least_used":
            return self._select_agent_by_least_used(agents)
        elif self.strategy == "weighted":
            return self._select_agent_by_weighted(agents)
        else:
            # استراتيجية افتراضية: الأولوية
            return self._select_agent_by_priority(agents)

    def _select_agent_by_priority(
            self, agents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        اختيار الوكيل بناءً على الأولوية

        المعلمات:
            agents (list): قائمة الوكلاء

        العائد:
            dict: الوكيل المختار
        """
        # ترتيب الوكلاء بناءً على الأولوية (تنازليًا)
        sorted_agents = sorted(
            agents, key=lambda x: x.get(
                'priority', 0), reverse=True)
        return sorted_agents[0] if sorted_agents else None

    def _select_agent_by_round_robin(
            self, agents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        اختيار الوكيل بناءً على التناوب الدائري

        المعلمات:
            agents (list): قائمة الوكلاء

        العائد:
            dict: الوكيل المختار
        """
        # زيادة المؤشر واختيار الوكيل التالي
        self.last_agent_index = (self.last_agent_index + 1) % len(agents)
        return agents[self.last_agent_index]

    def _select_agent_by_random(
            self, agents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        اختيار الوكيل بشكل عشوائي

        المعلمات:
            agents (list): قائمة الوكلاء

        العائد:
            dict: الوكيل المختار
        """
        return random.choice(agents)

    def _select_agent_by_cost(
            self, agents: List[Dict[str, Any]], request: Dict[str, Any]) -> Dict[str, Any]:
        """
        اختيار الوكيل بناءً على التكلفة

        المعلمات:
            agents (list): قائمة الوكلاء
            request (dict): بيانات الطلب

        العائد:
            dict: الوكيل المختار
        """
        # تقدير عدد الرموز في الطلب
        input_text = request.get('input', {}).get('text', '')
        estimated_tokens = len(input_text.split())

        # ترتيب الوكلاء بناءً على التكلفة (تصاعديًا)
        sorted_agents = sorted(
            agents, key=lambda x: x.get(
                'cost_per_token', 0) * estimated_tokens)
        return sorted_agents[0] if sorted_agents else None

    def _select_agent_by_response_time(
            self, agents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        اختيار الوكيل بناءً على وقت الاستجابة

        المعلمات:
            agents (list): قائمة الوكلاء

        العائد:
            dict: الوكيل المختار
        """
        # ترتيب الوكلاء بناءً على وقت الاستجابة (تصاعديًا)
        # استخدم وقت استجابة افتراضي (1 ثانية) للوكلاء التي لم يتم استخدامها
        # بعد
        sorted_agents = sorted(
            agents, key=lambda x: self.agent_response_times.get(
                x['id'], 1.0))
        return sorted_agents[0] if sorted_agents else None

    def _select_agent_by_least_used(
            self, agents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        اختيار الوكيل الأقل استخدامًا

        المعلمات:
            agents (list): قائمة الوكلاء

        العائد:
            dict: الوكيل المختار
        """
        # ترتيب الوكلاء بناءً على عدد الاستخدامات (تصاعديًا)
        sorted_agents = sorted(
            agents, key=lambda x: self.agent_usage_count.get(
                x['id'], 0))
        return sorted_agents[0] if sorted_agents else None

    def _select_agent_by_weighted(
            self, agents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        اختيار الوكيل بناءً على الوزن المركب

        المعلمات:
            agents (list): قائمة الوكلاء

        العائد:
            dict: الوكيل المختار
        """
        # حساب الوزن المركب لكل وكيل بناءً على:
        # - الأولوية (أعلى = أفضل)
        # - وقت الاستجابة (أقل = أفضل)
        # - معدل النجاح (أعلى = أفضل)
        # - التكلفة (أقل = أفضل)

        weights = []
        for agent in agents:
            agent_id = agent['id']
            priority_weight = agent.get(
                'priority', 0) * 2  # مضاعفة وزن الأولوية

            # حساب معدل النجاح
            usage_count = self.agent_usage_count.get(agent_id, 0)
            error_count = self.agent_error_count.get(agent_id, 0)
            success_rate = 1.0 if usage_count == 0 else (
                usage_count - error_count) / usage_count

            # حساب وزن وقت الاستجابة (عكسي)
            response_time = self.agent_response_times.get(agent_id, 1.0)
            response_time_weight = 1.0 / response_time if response_time > 0 else 1.0

            # حساب وزن التكلفة (عكسي)
            # تجنب القسمة على صفر
            cost_weight = 1.0 / (agent.get('cost_per_token', 0.001) + 0.001)

            # حساب الوزن المركب
            combined_weight = (
                priority_weight * 0.4
                + success_rate * 0.3
                + response_time_weight * 0.2
                + cost_weight * 0.1
            )

            weights.append((agent, combined_weight))

        # ترتيب الوكلاء بناءً على الوزن المركب (تنازليًا)
        sorted_agents = sorted(weights, key=lambda x: x[1], reverse=True)
        return sorted_agents[0][0] if sorted_agents else None

    def _record_agent_failure(self, agent_id: str, error: Exception) -> None:
        """
        تسجيل فشل الوكيل

        المعلمات:
            agent_id (str): معرف الوكيل
            error (Exception): الخطأ الذي حدث
        """
        # تحديث عدد الأخطاء
        if agent_id not in self.agent_error_count:
            self.agent_error_count[agent_id] = 0
        self.agent_error_count[agent_id] += 1

        # تسجيل الخطأ في السجل
        logger.error("فشل الوكيل %s: {str(error)}", agent_id)

        # يمكن إضافة منطق إضافي هنا مثل:
        # - تعطيل الوكيل مؤقتًا إذا تجاوز عدد الأخطاء حدًا معينًا
        # - إرسال إشعار للمسؤول
        # - تحديث حالة الوكيل في قاعدة البيانات

        # تحديث إحصائيات الوكيل في قاعدة البيانات
        self.db_service.update_agent_error_stats(
            agent_id=agent_id,
            error_message=str(error),
            timestamp=datetime.now()
        )
