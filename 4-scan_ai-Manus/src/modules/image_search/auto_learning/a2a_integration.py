# /home/ubuntu/image_search_integration/auto_learning/a2a_integration.py
"""
تكامل مع نظام A2A لمديول البحث الذاتي الذكي

يحتوي هذا الملف على الدوال والفئات اللازمة للتكامل مع نظام A2A (Application to Application)،
مما يسمح بالتواصل مع التطبيقات الأخرى وتبادل البيانات المتعلقة بالكلمات المفتاحية والمصادر ومحركات البحث.
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

import requests

from .config import A2A_API_URL, A2A_API_TIMEOUT, A2A_API_KEY
from .utils.constants import EVENT_TYPES
# إعداد التسجيل
logger = logging.getLogger(__name__)


class A2AIntegration:
    """
    فئة للتكامل مع نظام A2A
    """

    def __init__(self, api_url: str = A2A_API_URL, api_key: str = A2A_API_KEY, timeout: int = A2A_API_TIMEOUT):
        """
        تهيئة التكامل مع نظام A2A

        Args:
            api_url: عنوان API نظام A2A
            api_key: مفتاح API نظام A2A
            timeout: مهلة الاتصال بالثواني
        """
        self.api_url = api_url
        self.api_key = api_key
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def send_keyword_data(self, keyword_id: int, keyword_data: Dict[str, Any], target_app: str) -> bool:
        """
        إرسال بيانات الكلمة المفتاحية إلى تطبيق آخر عبر نظام A2A

        Args:
            keyword_id: معرف الكلمة المفتاحية
            keyword_data: بيانات الكلمة المفتاحية
            target_app: التطبيق المستهدف

        Returns:
            True إذا تم الإرسال بنجاح، False خلاف ذلك
        """
        try:
            a2a_data = {
                "source_app": "auto_learning",
                "target_app": target_app,
                "data_type": "keyword",
                "entity_id": keyword_id,
                "data": keyword_data,
                "timestamp": datetime.now().isoformat(),
                "event_type": EVENT_TYPES["KEYWORD_CREATED"]
            }

            response = requests.post(
                f"{self.api_url}/send",
                headers=self.headers,
                json=a2a_data,
                timeout=self.timeout
            )

            if response.status_code == 200:
                logger.info("تم إرسال بيانات الكلمة المفتاحية %s إلى التطبيق %s بنجاح", keyword_id, target_app)
                return True
            else:
                logger.error("فشل إرسال بيانات الكلمة المفتاحية %s إلى التطبيق %s: %s", keyword_id, target_app, response.text)
                return False

        except Exception as e:
            logger.error("خطأ في إرسال بيانات الكلمة المفتاحية %s إلى التطبيق %s: %s", keyword_id, target_app, str(e))
            return False

    def send_source_data(self, source_id: int, source_data: Dict[str, Any], target_app: str) -> bool:
        """
        إرسال بيانات المصدر إلى تطبيق آخر عبر نظام A2A

        Args:
            source_id: معرف المصدر
            source_data: بيانات المصدر
            target_app: التطبيق المستهدف

        Returns:
            True إذا تم الإرسال بنجاح، False خلاف ذلك
        """
        try:
            a2a_data = {
                "source_app": "auto_learning",
                "target_app": target_app,
                "data_type": "source",
                "entity_id": source_id,
                "data": source_data,
                "timestamp": datetime.now().isoformat(),
                "event_type": EVENT_TYPES["SOURCE_CREATED"]
            }

            response = requests.post(
                f"{self.api_url}/send",
                headers=self.headers,
                json=a2a_data,
                timeout=self.timeout
            )

            if response.status_code == 200:
                logger.info("تم إرسال بيانات المصدر %s إلى التطبيق %s بنجاح", source_id, target_app)
                return True
            else:
                logger.error("فشل إرسال بيانات المصدر %s إلى التطبيق %s: %s", source_id, target_app, response.text)
                return False

        except Exception as e:
            logger.error("خطأ في إرسال بيانات المصدر %s إلى التطبيق %s: %s", source_id, target_app, str(e))
            return False

    def send_search_engine_data(self, engine_id: int, engine_data: Dict[str, Any], target_app: str) -> bool:
        """
        إرسال بيانات محرك البحث إلى تطبيق آخر عبر نظام A2A

        Args:
            engine_id: معرف محرك البحث
            engine_data: بيانات محرك البحث
            target_app: التطبيق المستهدف

        Returns:
            True إذا تم الإرسال بنجاح، False خلاف ذلك
        """
        try:
            a2a_data = {
                "source_app": "auto_learning",
                "target_app": target_app,
                "data_type": "search_engine",
                "entity_id": engine_id,
                "data": engine_data,
                "timestamp": datetime.now().isoformat(),
                "event_type": EVENT_TYPES["SEARCH_ENGINE_CREATED"]
            }

            response = requests.post(
                f"{self.api_url}/send",
                headers=self.headers,
                json=a2a_data,
                timeout=self.timeout
            )

            if response.status_code == 200:
                logger.info("تم إرسال بيانات محرك البحث %s إلى التطبيق %s بنجاح", engine_id, target_app)
                return True
            else:
                logger.error("فشل إرسال بيانات محرك البحث %s إلى التطبيق %s: %s", engine_id, target_app, response.text)
                return False

        except Exception as e:
            logger.error("خطأ في إرسال بيانات محرك البحث %s إلى التطبيق %s: %s", engine_id, target_app, str(e))
            return False

    def send_search_result(self, query: str, results: List[Dict[str, Any]], engine_id: int, target_app: str) -> bool:
        """
        إرسال نتائج البحث إلى تطبيق آخر عبر نظام A2A

        Args:
            query: استعلام البحث
            results: نتائج البحث
            engine_id: معرف محرك البحث المستخدم
            target_app: التطبيق المستهدف

        Returns:
            True إذا تم الإرسال بنجاح، False خلاف ذلك
        """
        try:
            a2a_data = {
                "source_app": "auto_learning",
                "target_app": target_app,
                "data_type": "search_result",
                "data": {
                    "query": query,
                    "results": results,
                    "engine_id": engine_id,
                    "result_count": len(results)
                },
                "timestamp": datetime.now().isoformat(),
                "event_type": EVENT_TYPES["SEARCH_PERFORMED"]
            }

            response = requests.post(
                f"{self.api_url}/send",
                headers=self.headers,
                json=a2a_data,
                timeout=self.timeout
            )

            if response.status_code == 200:
                logger.info("تم إرسال نتائج البحث لاستعلام '%s' إلى التطبيق %s بنجاح", query, target_app)
                return True
            else:
                logger.error("فشل إرسال نتائج البحث لاستعلام '%s' إلى التطبيق %s: %s", query, target_app, response.text)
                return False

        except Exception as e:
            logger.error("خطأ في إرسال نتائج البحث لاستعلام '%s' إلى التطبيق %s: %s", query, target_app, str(e))
            return False

    def receive_data(self, data_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        استقبال بيانات من تطبيقات أخرى عبر نظام A2A

        Args:
            data_type: نوع البيانات (اختياري)

        Returns:
            قائمة بالبيانات المستقبلة
        """
        try:
            params = {"target_app": "auto_learning"}

            if data_type:
                params["data_type"] = data_type

            response = requests.get(
                f"{self.api_url}/receive",
                headers=self.headers,
                params=params,
                timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                logger.info("تم استقبال %s من البيانات من نظام A2A بنجاح", len(data))
                return data
            else:
                logger.error("فشل استقبال البيانات من نظام A2A: %s", response.text)
                return []

        except Exception as e:
            logger.error("خطأ في استقبال البيانات من نظام A2A: %s", str(e))
            return []

    def acknowledge_data(self, message_id: str) -> bool:
        """
        تأكيد استلام البيانات من نظام A2A

        Args:
            message_id: معرف الرسالة

        Returns:
            True إذا تم التأكيد بنجاح، False خلاف ذلك
        """
        try:
            response = requests.post(
                f"{self.api_url}/acknowledge",
                headers=self.headers,
                json={"message_id": message_id},
                timeout=self.timeout
            )

            if response.status_code == 200:
                logger.info("تم تأكيد استلام الرسالة %s بنجاح", message_id)
                return True
            else:
                logger.error("فشل تأكيد استلام الرسالة %s: %s", message_id, response.text)
                return False

        except Exception as e:
            logger.error("خطأ في تأكيد استلام الرسالة %s: %s", message_id, str(e))
            return False

    def check_connection(self) -> bool:
        """
        التحقق من الاتصال بنظام A2A

        Returns:
            True إذا كان الاتصال ناجحاً، False خلاف ذلك
        """
        try:
            response = requests.get(
                f"{self.api_url}/health",
                headers=self.headers,
                timeout=self.timeout
            )

            if response.status_code == 200:
                logger.info("تم الاتصال بنظام A2A بنجاح")
                return True
            else:
                logger.error("فشل الاتصال بنظام A2A: %s", response.text)
                return False

        except Exception as e:
            logger.error("خطأ في الاتصال بنظام A2A: %s", str(e))
            return False

    def register_app(self) -> bool:
        """
        تسجيل التطبيق في نظام A2A

        Returns:
            True إذا تم التسجيل بنجاح، False خلاف ذلك
        """
        try:
            app_data = {
                "app_name": "auto_learning",
                "app_description": "مديول البحث الذاتي الذكي",
                "supported_data_types": ["keyword", "source", "search_engine", "search_result"],
                "callback_url": "/api/auto_learning/a2a/callback"
            }

            response = requests.post(
                f"{self.api_url}/register",
                headers=self.headers,
                json=app_data,
                timeout=self.timeout
            )

            if response.status_code == 200:
                logger.info("تم تسجيل التطبيق في نظام A2A بنجاح")
                return True
            else:
                logger.error("فشل تسجيل التطبيق في نظام A2A: %s", response.text)
                return False

        except Exception as e:
            logger.error("خطأ في تسجيل التطبيق في نظام A2A: %s", str(e))
            return False


# إنشاء كائن التكامل مع نظام A2A
a2a_integration = A2AIntegration()
