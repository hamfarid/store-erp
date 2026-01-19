"""
/home/ubuntu/implemented_files/v3/src/modules/memory/memory_integration.py

ملف تكامل الذاكرة المركزية مع المديولات الأخرى

يوفر هذا الملف وظائف التكامل بين مديول الذاكرة المركزية والمديولات الأخرى، بما في ذلك:
- تكامل مع مديول البحث عن الصور
- تكامل مع مديول تشخيص النباتات
- تكامل مع مديول وكلاء الذكاء الاصطناعي
- تكامل مع مديول الصلاحيات
"""

from typing import Dict, List, Optional
import logging
from datetime import datetime

from sqlalchemy.orm import Session

from .service import MemoryService
from .schemas import MemoryCreate, MemorySearch
from .models import MemoryType, MemoryCategory, MemoryAccess
from .config import default_config as config

# إعداد التسجيل
logger = logging.getLogger(__name__)


class MemoryIntegration:
    """فئة تكامل الذاكرة المركزية مع المديولات الأخرى"""

    def __init__(self, db: Session):
        """
        تهيئة فئة تكامل الذاكرة

        المعلمات:
            db (Session): جلسة قاعدة البيانات
        """
        self.db = db
        self.memory_service = MemoryService(db)
        self.config = config

    # ==================== تكامل مع مديول البحث عن الصور ====================

    def store_image_search_result(self, query: str, results: List[Dict], user_id: Optional[str] = None) -> str:
        """
        تخزين نتائج البحث عن الصور في الذاكرة

        المعلمات:
            query (str): استعلام البحث
            results (List[Dict]): نتائج البحث
            user_id (Optional[str]): معرف المستخدم

        العوائد:
            str: معرف الذاكرة المنشأة
        """
        try:
            # إنشاء محتوى الذاكرة
            content = f"نتائج البحث عن الصور للاستعلام: {query}\n\n"

            for i, result in enumerate(results, 1):
                content += f"{i}. {result.get('title', 'بدون عنوان')}\n"
                content += f"   المصدر: {result.get('source', 'غير معروف')}\n"
                content += f"   الرابط: {result.get('url', 'غير متوفر')}\n"
                content += f"   الوصف: {result.get('description', 'بدون وصف')}\n\n"

            # إنشاء ملخص
            summary = f"نتائج البحث عن الصور ({len(results)} نتيجة) للاستعلام: {query}"

            # إنشاء بيانات الذاكرة
            memory_data = MemoryCreate(
                title=f"نتائج البحث عن الصور: {query}",
                content=content,
                summary=summary,
                memory_type=MemoryType.EPISODIC.value,
                category=MemoryCategory.SEARCH_HISTORY.value,
                access_level=MemoryAccess.PRIVATE.value if user_id else MemoryAccess.SYSTEM.value,
                source_module="image_search",
                source_id=None,
                importance_score=0.5,
                retention_days=30,
                created_by=user_id,
                tags=["image_search", "search_result"]
            )

            # تخزين الذاكرة
            memory = self.memory_service.create_memory(memory_data)

            logger.info("تم تخزين نتائج البحث عن الصور في الذاكرة: %s", memory.id)
            return memory.id

        except Exception as e:
            logger.error("فشل تخزين نتائج البحث عن الصور في الذاكرة: %s", str(e))
            return ""

    def get_related_image_searches(self, query: str, limit: int = 5, user_id: Optional[str] = None) -> List[Dict]:
        """
        استرجاع عمليات البحث عن الصور ذات الصلة

        المعلمات:
            query (str): استعلام البحث
            limit (int): الحد الأقصى لعدد النتائج
            user_id (Optional[str]): معرف المستخدم

        العوائد:
            List[Dict]: قائمة عمليات البحث ذات الصلة
        """
        try:
            # إنشاء معلمات البحث
            search_params = MemorySearch(
                query=query,
                category=MemoryCategory.SEARCH_HISTORY.value,
                source_module="image_search",
                page=1,
                page_size=limit,
                sort_by="created_at",
                sort_order="desc"
            )

            # البحث في الذاكرة
            results = self.memory_service.search_memories(search_params, user_id)

            # تحويل النتائج إلى قائمة
            related_searches = []
            for memory in results.items:
                related_searches.append({
                    "id": memory.id,
                    "title": memory.title,
                    "summary": memory.summary,
                    "created_at": memory.created_at.isoformat(),
                    "importance_score": memory.importance_score
                })

            return related_searches

        except Exception as e:
            logger.error("فشل استرجاع عمليات البحث عن الصور ذات الصلة: %s", str(e))
            return []

    # ==================== تكامل مع مديول تشخيص النباتات ====================

    def store_plant_diagnosis(self, plant_name: str, diagnosis_data: Dict, images: List[str], user_id: Optional[str] = None) -> str:
        """
        تخزين نتائج تشخيص النباتات في الذاكرة

        المعلمات:
            plant_name (str): اسم النبات
            diagnosis_data (Dict): بيانات التشخيص
            images (List[str]): قائمة مسارات الصور
            user_id (Optional[str]): معرف المستخدم

        العوائد:
            str: معرف الذاكرة المنشأة
        """
        try:
            # إنشاء محتوى الذاكرة
            content = f"تشخيص نبات: {plant_name}\n\n"

            # إضافة معلومات التشخيص
            if "diseases" in diagnosis_data:
                content += "الأمراض المحتملة:\n"
                for disease in diagnosis_data["diseases"]:
                    content += f"- {disease.get('name', 'غير معروف')}: {disease.get('confidence', 0):.2f}%\n"
                    if "symptoms" in disease:
                        content += "  الأعراض:\n"
                        for symptom in disease["symptoms"]:
                            content += f"  - {symptom}\n"
                    if "treatments" in disease:
                        content += "  العلاجات المقترحة:\n"
                        for treatment in disease["treatments"]:
                            content += f"  - {treatment}\n"
                content += "\n"

            if "health_status" in diagnosis_data:
                content += f"الحالة الصحية: {diagnosis_data['health_status']}\n\n"

            if "recommendations" in diagnosis_data:
                content += "التوصيات:\n"
                for recommendation in diagnosis_data["recommendations"]:
                    content += f"- {recommendation}\n"
                content += "\n"

            # إضافة معلومات الصور
            content += f"عدد الصور المرفقة: {len(images)}\n"
            for i, image_path in enumerate(images, 1):
                content += f"صورة {i}: {image_path}\n"

            # إنشاء ملخص
            summary = f"تشخيص نبات {plant_name}"
            if "diseases" in diagnosis_data and diagnosis_data["diseases"]:
                top_disease = diagnosis_data["diseases"][0]
                summary += f" - {top_disease.get('name', 'غير معروف')} ({top_disease.get('confidence', 0):.2f}%)"

            # إنشاء بيانات الذاكرة
            memory_data = MemoryCreate(
                title=f"تشخيص نبات: {plant_name}",
                content=content,
                summary=summary,
                memory_type=MemoryType.EPISODIC.value,
                category=MemoryCategory.DIAGNOSIS_RESULT.value,
                access_level=MemoryAccess.PRIVATE.value if user_id else MemoryAccess.SYSTEM.value,
                source_module="plant_diagnosis",
                source_id=None,
                importance_score=0.7,
                retention_days=90,
                created_by=user_id,
                tags=["plant_diagnosis", plant_name]
            )

            # إضافة علامات الأمراض
            if "diseases" in diagnosis_data:
                for disease in diagnosis_data["diseases"]:
                    disease_name = disease.get("name", "").lower().replace(" ", "_")
                    if disease_name:
                        memory_data.tags.append(f"disease_{disease_name}")

            # تخزين الذاكرة
            memory = self.memory_service.create_memory(memory_data)

            logger.info("تم تخزين نتائج تشخيص النباتات في الذاكرة: %s", memory.id)
            return memory.id

        except Exception as e:
            logger.error("فشل تخزين نتائج تشخيص النباتات في الذاكرة: %s", str(e))
            return ""

    def get_plant_diagnosis_history(self, plant_name: Optional[str] = None, limit: int = 10, user_id: Optional[str] = None) -> List[Dict]:
        """
        استرجاع سجل تشخيص النباتات

        المعلمات:
            plant_name (Optional[str]): اسم النبات (اختياري)
            limit (int): الحد الأقصى لعدد النتائج
            user_id (Optional[str]): معرف المستخدم

        العوائد:
            List[Dict]: قائمة سجلات التشخيص
        """
        try:
            # إنشاء معلمات البحث
            search_params = MemorySearch(
                category=MemoryCategory.DIAGNOSIS_RESULT.value,
                source_module="plant_diagnosis",
                page=1,
                page_size=limit,
                sort_by="created_at",
                sort_order="desc"
            )

            # إضافة اسم النبات إذا تم توفيره
            if plant_name:
                search_params.query = plant_name
                search_params.tags = [plant_name]

            # البحث في الذاكرة
            results = self.memory_service.search_memories(search_params, user_id)

            # تحويل النتائج إلى قائمة
            diagnosis_history = []
            for memory in results.items:
                diagnosis_history.append({
                    "id": memory.id,
                    "title": memory.title,
                    "summary": memory.summary,
                    "created_at": memory.created_at.isoformat(),
                    "importance_score": memory.importance_score
                })

            return diagnosis_history

        except Exception as e:
            logger.error("فشل استرجاع سجل تشخيص النباتات: %s", str(e))
            return []

    # ==================== تكامل مع مديول وكلاء الذكاء الاصطناعي ====================

    def store_ai_agent_interaction(self, agent_id: str, conversation: List[Dict], user_id: Optional[str] = None) -> str:
        """
        تخزين تفاعل وكيل الذكاء الاصطناعي في الذاكرة

        المعلمات:
            agent_id (str): معرف الوكيل
            conversation (List[Dict]): محادثة الوكيل
            user_id (Optional[str]): معرف المستخدم

        العوائد:
            str: معرف الذاكرة المنشأة
        """
        try:
            # استخراج معلومات المحادثة
            messages = []
            for msg in conversation:
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                timestamp = msg.get("timestamp", datetime.utcnow().isoformat())
                messages.append({"role": role, "content": content, "timestamp": timestamp})

            # إنشاء محتوى الذاكرة
            content = f"تفاعل مع وكيل الذكاء الاصطناعي: {agent_id}\n\n"

            for i, msg in enumerate(messages, 1):
                content += f"[{msg['timestamp']}] {msg['role']}: {msg['content']}\n\n"

            # إنشاء ملخص
            first_user_msg = next((msg["content"] for msg in messages if msg["role"] == "user"), "")
            summary = f"تفاعل مع وكيل {agent_id}"
            if first_user_msg:
                # اقتصار الملخص على 100 حرف
                if len(first_user_msg) > 100:
                    first_user_msg = first_user_msg[:97] + "..."
                summary += f": {first_user_msg}"

            # إنشاء بيانات الذاكرة
            memory_data = MemoryCreate(
                title=f"تفاعل مع وكيل {agent_id}",
                content=content,
                summary=summary,
                memory_type=MemoryType.EPISODIC.value,
                category=MemoryCategory.AI_AGENT_INTERACTION.value,
                access_level=MemoryAccess.PRIVATE.value if user_id else MemoryAccess.SYSTEM.value,
                source_module="ai_agent_module",
                source_id=agent_id,
                importance_score=0.6,
                retention_days=60,
                created_by=user_id,
                tags=["ai_agent", f"agent_{agent_id}"],
                metadata={"conversation_length": len(messages)}
            )

            # تخزين الذاكرة
            memory = self.memory_service.create_memory(memory_data)

            logger.info("تم تخزين تفاعل وكيل الذكاء الاصطناعي في الذاكرة: %s", memory.id)
            return memory.id

        except Exception as e:
            logger.error("فشل تخزين تفاعل وكيل الذكاء الاصطناعي في الذاكرة: %s", str(e))
            return ""

    def get_ai_agent_history(self, agent_id: Optional[str] = None, query: Optional[str] = None, limit: int = 10, user_id: Optional[str] = None) -> List[Dict]:
        """
        استرجاع سجل تفاعلات وكيل الذكاء الاصطناعي

        المعلمات:
            agent_id (Optional[str]): معرف الوكيل (اختياري)
            query (Optional[str]): نص البحث (اختياري)
            limit (int): الحد الأقصى لعدد النتائج
            user_id (Optional[str]): معرف المستخدم

        العوائد:
            List[Dict]: قائمة سجلات التفاعل
        """
        try:
            # إنشاء معلمات البحث
            search_params = MemorySearch(
                category=MemoryCategory.AI_AGENT_INTERACTION.value,
                source_module="ai_agent_module",
                page=1,
                page_size=limit,
                sort_by="created_at",
                sort_order="desc"
            )

            # إضافة معرف الوكيل إذا تم توفيره
            if agent_id:
                search_params.source_id = agent_id
                search_params.tags = [f"agent_{agent_id}"]

            # إضافة نص البحث إذا تم توفيره
            if query:
                search_params.query = query

            # البحث في الذاكرة
            results = self.memory_service.search_memories(search_params, user_id)

            # تحويل النتائج إلى قائمة
            agent_history = []
            for memory in results.items:
                agent_history.append({
                    "id": memory.id,
                    "title": memory.title,
                    "summary": memory.summary,
                    "created_at": memory.created_at.isoformat(),
                    "importance_score": memory.importance_score,
                    "metadata": memory.metadata
                })

            return agent_history

        except Exception as e:
            logger.error("فشل استرجاع سجل تفاعلات وكيل الذكاء الاصطناعي: %s", str(e))
            return []

    # ==================== وظائف عامة ====================

    def semantic_search_across_modules(self, query: str, top_k: int = 5, user_id: Optional[str] = None) -> List[Dict]:
        """
        البحث الدلالي عبر جميع المديولات

        المعلمات:
            query (str): نص البحث
            top_k (int): عدد النتائج المطلوبة
            user_id (Optional[str]): معرف المستخدم

        العوائد:
            List[Dict]: قائمة النتائج
        """
        try:
            # البحث الدلالي في الذاكرة
            results = self.memory_service.semantic_search(query, top_k, user_id)

            # تحويل النتائج إلى قائمة
            search_results = []
            for result in results.items:
                search_results.append({
                    "id": result.memory.id,
                    "title": result.memory.title,
                    "summary": result.memory.summary,
                    "content": result.memory.content,
                    "category": result.memory.category.value if result.memory.category else None,
                    "source_module": result.memory.source_module,
                    "created_at": result.memory.created_at.isoformat(),
                    "similarity_score": result.similarity_score
                })

            return search_results

        except Exception as e:
            logger.error("فشل البحث الدلالي عبر جميع المديولات: %s", str(e))
            return []

    def store_external_data(self, title: str, content: str, source: str, source_url: Optional[str] = None, tags: List[str] = None, user_id: Optional[str] = None) -> str:
        """
        تخزين بيانات خارجية في الذاكرة

        المعلمات:
            title (str): عنوان البيانات
            content (str): محتوى البيانات
            source (str): مصدر البيانات
            source_url (Optional[str]): رابط المصدر
            tags (List[str]): قائمة العلامات
            user_id (Optional[str]): معرف المستخدم

        العوائد:
            str: معرف الذاكرة المنشأة
        """
        try:
            # إنشاء ملخص
            summary = title

            # إنشاء بيانات الذاكرة
            memory_data = MemoryCreate(
                title=title,
                content=content,
                summary=summary,
                memory_type=MemoryType.SEMANTIC.value,
                category=MemoryCategory.EXTERNAL_SOURCE.value,
                access_level=MemoryAccess.PRIVATE.value if user_id else MemoryAccess.SYSTEM.value,
                source_module="external",
                source_id=None,
                source_url=source_url,
                importance_score=0.5,
                retention_days=180,
                created_by=user_id,
                tags=tags or ["external_data", source]
            )

            # تخزين الذاكرة
            memory = self.memory_service.create_memory(memory_data)

            logger.info("تم تخزين البيانات الخارجية في الذاكرة: %s", memory.id)
            return memory.id

        except Exception as e:
            logger.error("فشل تخزين البيانات الخارجية في الذاكرة: %s", str(e))
            return ""


# تصدير الدوال والكائنات
__all__ = ['MemoryIntegration']
