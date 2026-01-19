# /home/ubuntu/image_search_integration/auto_learning/memory_integration.py
"""
تكامل مع الذاكرة المركزية لمديول البحث الذاتي الذكي

يحتوي هذا الملف على الدوال والفئات اللازمة للتكامل مع مديول الذاكرة المركزية،
مما يسمح بتخزين واسترجاع المعلومات المتعلقة بالكلمات المفتاحية والمصادر ومحركات البحث.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import requests

from .config import MEMORY_API_TIMEOUT, MEMORY_API_URL
from .utils.constants import EVENT_TYPES

# إعداد التسجيل
logger = logging.getLogger(__name__)


class MemoryIntegration:
    """
    فئة للتكامل مع الذاكرة المركزية
    """

    def __init__(
        self, api_url: str = MEMORY_API_URL, timeout: int = MEMORY_API_TIMEOUT
    ):
        """
        تهيئة التكامل مع الذاكرة المركزية

        Args:
            api_url: عنوان API الذاكرة المركزية
            timeout: مهلة الاتصال بالثواني
        """
        self.api_url = api_url
        self.timeout = timeout

    def store_keyword_data(self, keyword_id: int,
                           keyword_data: Dict[str, Any]) -> bool:
        """
        تخزين بيانات الكلمة المفتاحية في الذاكرة المركزية

        Args:
            keyword_id: معرف الكلمة المفتاحية
            keyword_data: بيانات الكلمة المفتاحية

        Returns:
            True إذا تم التخزين بنجاح، False خلاف ذلك
        """
        try:
            memory_data = {
                "entity_type": "keyword",
                "entity_id": keyword_id,
                "data": keyword_data,
                "timestamp": datetime.now().isoformat(),
                "event_type": EVENT_TYPES["KEYWORD_CREATED"],
            }

            response = requests.post(
                f"{self.api_url}/store", json=memory_data, timeout=self.timeout
            )

            if response.status_code == 200:
                logger.info(
                    f"تم تخزين بيانات الكلمة المفتاحية {keyword_id} في الذاكرة المركزية بنجاح"
                )
                return True
            else:
                logger.error(
                    f"فشل تخزين بيانات الكلمة المفتاحية {keyword_id} في الذاكرة المركزية: {response.text}"
                )
                return False

        except Exception as e:
            logger.error(
                f"خطأ في تخزين بيانات الكلمة المفتاحية {keyword_id} في الذاكرة المركزية: {str(e)}"
            )
            return False

    def store_source_data(self, source_id: int,
                          source_data: Dict[str, Any]) -> bool:
        """
        تخزين بيانات المصدر في الذاكرة المركزية

        Args:
            source_id: معرف المصدر
            source_data: بيانات المصدر

        Returns:
            True إذا تم التخزين بنجاح، False خلاف ذلك
        """
        try:
            memory_data = {
                "entity_type": "source",
                "entity_id": source_id,
                "data": source_data,
                "timestamp": datetime.now().isoformat(),
                "event_type": EVENT_TYPES["SOURCE_CREATED"],
            }

            response = requests.post(
                f"{self.api_url}/store", json=memory_data, timeout=self.timeout
            )

            if response.status_code == 200:
                logger.info(
                    f"تم تخزين بيانات المصدر {source_id} في الذاكرة المركزية بنجاح"
                )
                return True
            else:
                logger.error(
                    f"فشل تخزين بيانات المصدر {source_id} في الذاكرة المركزية: {response.text}"
                )
                return False

        except Exception as e:
            logger.error(
                f"خطأ في تخزين بيانات المصدر {source_id} في الذاكرة المركزية: {str(e)}"
            )
            return False

    def store_search_engine_data(
        self, engine_id: int, engine_data: Dict[str, Any]
    ) -> bool:
        """
        تخزين بيانات محرك البحث في الذاكرة المركزية

        Args:
            engine_id: معرف محرك البحث
            engine_data: بيانات محرك البحث

        Returns:
            True إذا تم التخزين بنجاح، False خلاف ذلك
        """
        try:
            memory_data = {
                "entity_type": "search_engine",
                "entity_id": engine_id,
                "data": engine_data,
                "timestamp": datetime.now().isoformat(),
                "event_type": EVENT_TYPES["SEARCH_ENGINE_CREATED"],
            }

            response = requests.post(
                f"{self.api_url}/store", json=memory_data, timeout=self.timeout
            )

            if response.status_code == 200:
                logger.info(
                    f"تم تخزين بيانات محرك البحث {engine_id} في الذاكرة المركزية بنجاح"
                )
                return True
            else:
                logger.error(
                    f"فشل تخزين بيانات محرك البحث {engine_id} في الذاكرة المركزية: {response.text}"
                )
                return False

        except Exception as e:
            logger.error(
                f"خطأ في تخزين بيانات محرك البحث {engine_id} في الذاكرة المركزية: {str(e)}"
            )
            return False

    def store_search_result(
        self, query: str, results: List[Dict[str, Any]], engine_id: int
    ) -> bool:
        """
        تخزين نتائج البحث في الذاكرة المركزية

        Args:
            query: استعلام البحث
            results: نتائج البحث
            engine_id: معرف محرك البحث المستخدم

        Returns:
            True إذا تم التخزين بنجاح، False خلاف ذلك
        """
        try:
            memory_data = {
                "entity_type": "search_result",
                "data": {
                    "query": query,
                    "results": results,
                    "engine_id": engine_id,
                    "result_count": len(results),
                },
                "timestamp": datetime.now().isoformat(),
                "event_type": EVENT_TYPES["SEARCH_PERFORMED"],
            }

            response = requests.post(
                f"{self.api_url}/store", json=memory_data, timeout=self.timeout
            )

            if response.status_code == 200:
                logger.info(
                    f"تم تخزين نتائج البحث لاستعلام '{query}' في الذاكرة المركزية بنجاح"
                )
                return True
            else:
                logger.error(
                    f"فشل تخزين نتائج البحث لاستعلام '{query}' في الذاكرة المركزية: {response.text}"
                )
                return False

        except Exception as e:
            logger.error(
                f"خطأ في تخزين نتائج البحث لاستعلام '{query}' في الذاكرة المركزية: {str(e)}"
            )
            return False

    def retrieve_keyword_data(
        self, keyword_id: Optional[int] = None, text: Optional[str] = None
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], None]:
        """
        استرجاع بيانات الكلمة المفتاحية من الذاكرة المركزية

        Args:
            keyword_id: معرف الكلمة المفتاحية (اختياري)
            text: نص الكلمة المفتاحية (اختياري)

        Returns:
            بيانات الكلمة المفتاحية أو قائمة بالكلمات المفتاحية أو None إذا لم يتم العثور على بيانات
        """
        try:
            params = {"entity_type": "keyword"}
            if keyword_id:
                params["entity_id"] = keyword_id
            if text:
                params["text"] = text

            response = requests.get(
                f"{self.api_url}/retrieve", params=params, timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                logger.info(
                    "تم استرجاع بيانات الكلمة المفتاحية من الذاكرة المركزية بنجاح")
                return data
            else:
                logger.error(
                    "فشل استرجاع بيانات الكلمة المفتاحية من الذاكرة المركزية")
                return None

        except Exception as e:
            logger.error(
                f"خطأ في استرجاع بيانات الكلمة المفتاحية من الذاكرة المركزية: {str(e)}"
            )
            return None

    def retrieve_source_data(
        self, source_id: Optional[int] = None, domain: Optional[str] = None
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], None]:
        """
        استرجاع بيانات المصدر من الذاكرة المركزية

        Args:
            source_id: معرف المصدر (اختياري)
            domain: نطاق المصدر (اختياري)

        Returns:
            بيانات المصدر أو قائمة بالمصادر أو None إذا لم يتم العثور على بيانات
        """
        try:
            params = {"entity_type": "source"}
            if source_id:
                params["entity_id"] = source_id
            if domain:
                params["domain"] = domain

            response = requests.get(
                f"{self.api_url}/retrieve", params=params, timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                logger.info(
                    "تم استرجاع بيانات المصدر من الذاكرة المركزية بنجاح")
                return data
            else:
                logger.error("فشل استرجاع بيانات المصدر من الذاكرة المركزية")
                return None

        except Exception as e:
            logger.error(
                f"خطأ في استرجاع بيانات المصدر من الذاكرة المركزية: {str(e)}")
            return None

    def retrieve_search_engine_data(
        self, engine_id: Optional[int] = None, name: Optional[str] = None
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], None]:
        """
        استرجاع بيانات محرك البحث من الذاكرة المركزية

        Args:
            engine_id: معرف محرك البحث (اختياري)
            name: اسم محرك البحث (اختياري)

        Returns:
            بيانات محرك البحث أو قائمة بمحركات البحث أو None إذا لم يتم العثور على بيانات
        """
        try:
            params = {"entity_type": "search_engine"}
            if engine_id:
                params["entity_id"] = engine_id
            if name:
                params["name"] = name

            response = requests.get(
                f"{self.api_url}/retrieve", params=params, timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                logger.info(
                    "تم استرجاع بيانات محرك البحث من الذاكرة المركزية بنجاح")
                return data
            else:
                logger.error(
                    "فشل استرجاع بيانات محرك البحث من الذاكرة المركزية")
                return None

        except Exception as e:
            logger.error(
                f"خطأ في استرجاع بيانات محرك البحث من الذاكرة المركزية: {str(e)}"
            )
            return None

    def retrieve_similar_searches(
        self, query: str, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        استرجاع عمليات بحث مماثلة من الذاكرة المركزية

        Args:
            query: استعلام البحث
            limit: عدد النتائج المطلوبة

        Returns:
            قائمة بعمليات البحث المماثلة
        """
        try:
            params = {
                "entity_type": "search_result",
                "query": query,
                "limit": limit,
                "similar": True,
            }

            response = requests.get(
                f"{self.api_url}/retrieve", params=params, timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                logger.info(
                    f"تم استرجاع عمليات بحث مماثلة لاستعلام '{query}' بنجاح")
                return data if isinstance(data, list) else []
            else:
                logger.error(
                    f"فشل استرجاع عمليات بحث مماثلة لاستعلام '{query}'")
                return []

        except Exception as e:
            logger.error(
                f"خطأ في استرجاع عمليات بحث مماثلة لاستعلام '{query}': {str(e)}"
            )
            return []

    def update_entity_data(self,
                           entity_type: str,
                           entity_id: int,
                           data: Dict[str,
                                      Any],
                           event_type: str) -> bool:
        """
        تحديث بيانات كيان في الذاكرة المركزية

        Args:
            entity_type: نوع الكيان (keyword, source, search_engine)
            entity_id: معرف الكيان
            data: البيانات المحدثة
            event_type: نوع الحدث

        Returns:
            True إذا تم التحديث بنجاح، False خلاف ذلك
        """
        try:
            memory_data = {
                "entity_type": entity_type,
                "entity_id": entity_id,
                "data": data,
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type,
            }

            response = requests.put(
                f"{self.api_url}/update",
                json=memory_data,
                timeout=self.timeout)

            if response.status_code == 200:
                logger.info(
                    f"تم تحديث بيانات {entity_type} {entity_id} في الذاكرة المركزية بنجاح"
                )
                return True
            else:
                logger.error(
                    f"فشل تحديث بيانات {entity_type} {entity_id} في الذاكرة المركزية: {response.text}"
                )
                return False

        except Exception as e:
            logger.error(
                f"خطأ في تحديث بيانات {entity_type} {entity_id} في الذاكرة المركزية: {str(e)}"
            )
            return False

    def delete_entity_data(self, entity_type: str, entity_id: int) -> bool:
        """
        حذف بيانات كيان من الذاكرة المركزية

        Args:
            entity_type: نوع الكيان (keyword, source, search_engine)
            entity_id: معرف الكيان

        Returns:
            True إذا تم الحذف بنجاح، False خلاف ذلك
        """
        try:
            params = {"entity_type": entity_type, "entity_id": entity_id}

            response = requests.delete(
                f"{self.api_url}/delete", params=params, timeout=self.timeout
            )

            if response.status_code == 200:
                logger.info(
                    f"تم حذف بيانات {entity_type} {entity_id} من الذاكرة المركزية بنجاح"
                )
                return True
            else:
                logger.error(
                    f"فشل حذف بيانات {entity_type} {entity_id} من الذاكرة المركزية: {response.text}"
                )
                return False

        except Exception as e:
            logger.error(
                f"خطأ في حذف بيانات {entity_type} {entity_id} من الذاكرة المركزية: {str(e)}"
            )
            return False

    def check_connection(self) -> bool:
        """
        فحص الاتصال بالذاكرة المركزية

        Returns:
            True إذا كان الاتصال موجود، False خلاف ذلك
        """
        try:
            response = requests.get(
                f"{self.api_url}/health",
                timeout=self.timeout)
            return response.status_code == 200
        except Exception:
            return False


# إنشاء نسخة عامة للاستخدام في التطبيق
memory_integration = MemoryIntegration()
