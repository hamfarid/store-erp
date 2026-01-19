# /home/ubuntu/ai_web_organized/src/modules/internal_diagnosis/knowledge_base_manager.py

"""
مدير قاعدة المعرفة (KnowledgeBaseManager) لوحدة محرك التشخيص (internal_diagnosis).

هذا الملف مسؤول عن إدارة جميع عمليات القراءة، الكتابة، التحديث، والبحث
في قاعدة المعرفة الخاصة بالأمراض النباتية وعلاجاتها.
"""

import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import yaml
from pydantic import ValidationError

# افتراض أن النماذج موجودة في نفس الدليل أو يمكن الوصول إليها
from .models import KnowledgeBaseEntry  # استخدام نسبي للاستيراد

# إعداد المسجل (Logger)
# في بيئة إنتاجية، سيتم استخدام مسجل أكثر تطوراً من وحدة log_activity
import logging
logger = logging.getLogger(__name__)
# للتبسيط في هذه المرحلة، سنستخدم المسجل الأساسي
logging.basicConfig(level=logging.INFO)


class KnowledgeBaseManager:
    """إدارة قاعدة المعرفة للأمراض النباتية."""

    def __init__(
            self,
            kb_path: Optional[str] = None,
            create_if_not_exists: bool = True):
        """تهيئة مدير قاعدة المعرفة.

        Args:
            kb_path: المسار إلى ملف قاعدة المعرفة (YAML). إذا لم يتم توفيره،
                     سيتم استخدام مسار افتراضي بجوار هذا الملف.
            create_if_not_exists: إذا كان صحيحًا، سيتم إنشاء ملف قاعدة معرفة فارغ
                                  إذا لم يكن الملف المحدد موجودًا.
        """
        if kb_path:
            self.kb_path = kb_path
        else:
            self.kb_path = os.path.join(
                os.path.dirname(__file__),
                "knowledge_base.yaml")

        self.knowledge_base: List[KnowledgeBaseEntry] = []
        self._load_knowledge_base(create_if_not_exists=create_if_not_exists)

    def _load_knowledge_base(self, create_if_not_exists: bool = True) -> None:
        """تحميل قاعدة المعرفة من ملف YAML."""
        if not os.path.exists(self.kb_path):
            logger.warning(f"ملف قاعدة المعرفة غير موجود: {self.kb_path}")
            if create_if_not_exists:
                logger.info(f"إنشاء ملف قاعدة معرفة فارغ في: {self.kb_path}")
                self.knowledge_base = []
                self._save_knowledge_base()  # حفظ قائمة فارغة لإنشاء الملف
            else:
                self.knowledge_base = []  # أو إثارة خطأ إذا كان السلوك المطلوب مختلفًا
            return

        if not os.path.isfile(self.kb_path):
            logger.error(f"مسار قاعدة المعرفة ليس ملفًا: {self.kb_path}")
            self.knowledge_base = []
            return

        try:
            with open(self.kb_path, 'r', encoding='utf-8') as f:
                kb_data = yaml.safe_load(f)

            if kb_data is None:  # الملف فارغ
                self.knowledge_base = []
                logger.info(
                    f"تم تحميل قاعدة معرفة فارغة من {self.kb_path} (الملف كان فارغًا أو لا يحتوي على بيانات YAML صالحة).")
                return

            if not isinstance(kb_data, list):
                logger.error(
                    f"تنسيق ملف قاعدة المعرفة غير صحيح (يجب أن يكون قائمة): {self.kb_path}. تم تحميل قاعدة فارغة.")
                self.knowledge_base = []
                return

            valid_entries = []
            for i, entry_data in enumerate(kb_data):
                try:
                    entry = KnowledgeBaseEntry(**entry_data)
                    if not entry.entry_id:
                        entry.entry_id = str(
                            uuid.uuid4())  # تعيين ID إذا لم يكن موجودًا
                    valid_entries.append(entry)
                except ValidationError as ve:
                    logger.warning(
                        f"خطأ في التحقق من صحة المدخل رقم {i+1} في {self.kb_path}: {ve}. سيتم تجاهل هذا المدخل.")

            self.knowledge_base = valid_entries
            logger.info(
                f"تم تحميل قاعدة المعرفة بنجاح من {self.kb_path} ({len(self.knowledge_base)} مدخل صالح).")

        except yaml.YAMLError as e:
            logger.error(
                f"خطأ في تحليل ملف قاعدة المعرفة {self.kb_path}: {e}",
                exc_info=True)
            self.knowledge_base = []
        except Exception as e:
            logger.error(
                f"خطأ غير متوقع أثناء تحميل قاعدة المعرفة {self.kb_path}: {e}",
                exc_info=True)
            self.knowledge_base = []

    def _save_knowledge_base(self) -> bool:
        """حفظ الحالة الحالية لقاعدة المعرفة في ملف YAML."""
        try:
            # تحويل كائنات Pydantic إلى قواميس قبل الحفظ
            kb_data_to_save = [
                entry.model_dump(
                    exclude_none=True) for entry in self.knowledge_base]
            with open(self.kb_path, 'w', encoding='utf-8') as f:
                yaml.dump(
                    kb_data_to_save,
                    f,
                    allow_unicode=True,
                    sort_keys=False)
            logger.info(f"تم حفظ قاعدة المعرفة بنجاح في {self.kb_path}")
            return True
        except Exception as e:
            logger.error(
                f"فشل حفظ قاعدة المعرفة في {self.kb_path}: {e}",
                exc_info=True)
            return False

    def add_entry(self,
                  entry_data: Union[Dict[str,
                                         Any],
                                    KnowledgeBaseEntry]) -> Optional[KnowledgeBaseEntry]:
        """إضافة مدخل جديد إلى قاعدة المعرفة.

        Args:
            entry_data: بيانات المدخل كقاموس أو كائن KnowledgeBaseEntry.

        Returns:
            المدخل المضاف مع entry_id (إذا نجحت الإضافة)، أو None إذا فشلت.
        """
        try:
            if isinstance(entry_data, dict):
                new_entry = KnowledgeBaseEntry(**entry_data)
            elif isinstance(entry_data, KnowledgeBaseEntry):
                new_entry = entry_data
            else:
                logger.error(
                    "نوع بيانات المدخل غير صالح. يجب أن يكون قاموسًا أو KnowledgeBaseEntry.")
                return None

            if not new_entry.entry_id:
                new_entry.entry_id = str(uuid.uuid4())

            # التحقق من عدم وجود entry_id مكرر (نادر الحدوث مع UUIDs ولكن جيد
            # للتحقق)
            if any(e.entry_id == new_entry.entry_id for e in self.knowledge_base):
                logger.warning(
                    f"المدخل بالمعرف {new_entry.entry_id} موجود بالفعل. سيتم إنشاء معرف جديد.")
                new_entry.entry_id = str(uuid.uuid4())

            new_entry.last_updated = datetime.utcnow()
            self.knowledge_base.append(new_entry)
            if self._save_knowledge_base():
                logger.info(
                    f"تمت إضافة مدخل جديد بنجاح بالمعرف: {new_entry.entry_id}")
                return new_entry
            else:
                # محاولة التراجع عن الإضافة إذا فشل الحفظ
                self.knowledge_base.pop()
                logger.error("فشلت إضافة المدخل بسبب خطأ في الحفظ.")
                return None
        except ValidationError as ve:
            logger.error(f"خطأ في التحقق من صحة بيانات المدخل الجديد: {ve}")
            return None
        except Exception as e:
            logger.error(
                f"خطأ غير متوقع أثناء إضافة مدخل جديد: {e}",
                exc_info=True)
            return None

    def get_entry_by_id(self, entry_id: str) -> Optional[KnowledgeBaseEntry]:
        """استرجاع مدخل من قاعدة المعرفة بواسطة المعرف الخاص به."""
        for entry in self.knowledge_base:
            if entry.entry_id == entry_id:
                return entry
        logger.debug(f"لم يتم العثور على مدخل بالمعرف: {entry_id}")
        return None

    def update_entry(self,
                     entry_id: str,
                     update_data: Dict[str,
                                       Any]) -> Optional[KnowledgeBaseEntry]:
        """تحديث مدخل موجود في قاعدة المعرفة.

        Args:
            entry_id: معرف المدخل المراد تحديثه.
            update_data: قاموس يحتوي على الحقول المراد تحديثها وقيمها الجديدة.

        Returns:
            المدخل المحدث إذا نجحت العملية، أو None إذا فشلت.
        """
        entry_to_update = self.get_entry_by_id(entry_id)
        if not entry_to_update:
            logger.error(f"لم يتم العثور على مدخل للتحديث بالمعرف: {entry_id}")
            return None

        try:
            # إنشاء نسخة من بيانات المدخل الحالي وتحديثها
            updated_entry_data = entry_to_update.model_copy(
                update=update_data).model_dump()
            # تحديث وقت التعديل
            updated_entry_data['last_updated'] = datetime.utcnow()

            # التحقق من صحة البيانات المحدثة
            validated_updated_entry = KnowledgeBaseEntry(**updated_entry_data)

            # استبدال المدخل القديم بالمدخل المحدث
            for i, entry in enumerate(self.knowledge_base):
                if entry.entry_id == entry_id:
                    self.knowledge_base[i] = validated_updated_entry
                    break

            if self._save_knowledge_base():
                logger.info(f"تم تحديث المدخل بنجاح بالمعرف: {entry_id}")
                return validated_updated_entry
            else:
                # محاولة التراجع عن التحديث إذا فشل الحفظ (قد يكون معقدًا، أبسط
                # طريقة هي إعادة تحميل القاعدة)
                logger.error(
                    "فشل تحديث المدخل بسبب خطأ في الحفظ. قد تحتاج القاعدة إلى إعادة تحميل.")
                # إعادة تحميل للحفاظ على الاتساق
                self._load_knowledge_base(create_if_not_exists=False)
                return None
        except ValidationError as ve:
            logger.error(
                f"خطأ في التحقق من صحة بيانات التحديث للمدخل {entry_id}: {ve}")
            return None
        except Exception as e:
            logger.error(
                f"خطأ غير متوقع أثناء تحديث المدخل {entry_id}: {e}",
                exc_info=True)
            return None

    def delete_entry(self, entry_id: str) -> bool:
        """حذف مدخل من قاعدة المعرفة."""
        entry_to_delete = self.get_entry_by_id(entry_id)
        if not entry_to_delete:
            logger.error(f"لم يتم العثور على مدخل للحذف بالمعرف: {entry_id}")
            return False

        self.knowledge_base = [
            entry for entry in self.knowledge_base if entry.entry_id != entry_id]
        if self._save_knowledge_base():
            logger.info(f"تم حذف المدخل بنجاح بالمعرف: {entry_id}")
            return True
        else:
            # محاولة التراجع عن الحذف إذا فشل الحفظ
            self.knowledge_base.append(entry_to_delete)  # إعادة الإضافة محليًا
            logger.error("فشل حذف المدخل بسبب خطأ في الحفظ.")
            return False

    def search_entries(
            self, query: str, fields: Optional[List[str]] = None) -> List[KnowledgeBaseEntry]:
        """البحث في قاعدة المعرفة عن مدخلات تطابق استعلامًا معينًا في حقول محددة.

        Args:
            query: نص الاستعلام للبحث عنه (غير حساس لحالة الأحرف).
            fields: قائمة اختيارية بالحقول التي سيتم البحث فيها (مثل ['disease_name', 'symptoms']).
                    إذا لم يتم توفيرها، سيتم البحث في حقول افتراضية (مثل disease_name, symptoms, description).

        Returns:
            قائمة بالمدخلات المطابقة.
        """
        results: List[KnowledgeBaseEntry] = []
        search_query = query.lower()

        if fields is None:
            search_fields = [
                'disease_name',
                'symptoms',
                'description',
                'affected_plants']
        else:
            search_fields = fields

        for entry in self.knowledge_base:
            match_found = False
            for field_name in search_fields:
                if hasattr(entry, field_name):
                    field_value = getattr(entry, field_name)
                    if isinstance(field_value,
                                  str) and search_query in field_value.lower():
                        match_found = True
                        break
                    elif isinstance(field_value, list):
                        for item in field_value:
                            if isinstance(
                                    item, str) and search_query in item.lower():
                                match_found = True
                                break
                if match_found:
                    break

            if match_found:
                results.append(entry)

        logger.info(
            f"تم العثور على {len(results)} مدخل(ات) تطابق الاستعلام: '{query}'")
        return results

    def get_all_entries(self) -> List[KnowledgeBaseEntry]:
        """استرجاع جميع المدخلات في قاعدة المعرفة."""
        return self.knowledge_base

    def reload_knowledge_base(self) -> None:
        """إعادة تحميل قاعدة المعرفة من الملف."""
        logger.info("إعادة تحميل قاعدة المعرفة...")
        self._load_knowledge_base(create_if_not_exists=False)


# مثال للاستخدام (يمكن إزالته أو وضعه في قسم __main__)
if __name__ == '__main__':
    # إنشاء مدير مع مسار افتراضي (سيتم إنشاء knowledge_base.yaml إذا لم يكن
    # موجودًا)
    kb_manager = KnowledgeBaseManager()

    # إضافة مدخل جديد
    new_disease_data = {
        "disease_name": "اللفحة المبكرة في الطماطم",
        "scientific_name": "Alternaria solani",
        "symptoms": [
            "بقع داكنة على الأوراق السفلية",
            "حلقات متحدة المركز داخل البقع",
            "تساقط الأوراق"],
        "description": "مرض فطري شائع يصيب الطماطم والبطاطس.",
        "affected_plants": [
            "الطماطم",
            "البطاطس",
            "الباذنجان"],
        "treatments": [
            "استخدام مبيدات فطرية تحتوي على مانكوزيب أو كلوروثالونيل",
            "إزالة الأجزاء المصابة"],
        "prevention": [
            "تناوب المحاصيل",
            "الري بالتنقيط لتجنب ترطيب الأوراق",
            "زراعة أصناف مقاومة"]}
    added_entry = kb_manager.add_entry(new_disease_data)
    if added_entry:
        print(
            f"تمت إضافة مدخل: {added_entry.disease_name} (ID: {added_entry.entry_id})")

    # البحث عن مدخل
    search_results = kb_manager.search_entries("طماطم")
    print(f"نتائج البحث عن 'طماطم': {len(search_results)} مدخل")
    for res in search_results:
        print(f"- {res.disease_name}")

    # الحصول على جميع المدخلات
    all_entries = kb_manager.get_all_entries()
    print(f"إجمالي عدد المدخلات في قاعدة المعرفة: {len(all_entries)}")

    if added_entry:
        # تحديث مدخل
        update_info = {
            "description": "مرض فطري شائع جدًا يصيب الطماطم والبطاطس في الظروف الرطبة."}
        updated = kb_manager.update_entry(added_entry.entry_id, update_info)
        if updated:
            print(f"تم تحديث وصف المرض: {updated.description}")

        # حذف مدخل
        # deleted = kb_manager.delete_entry(added_entry.entry_id)
        # print(f"هل تم حذف المدخل؟ {deleted}")

    # طباعة محتوى الملف للتحقق (اختياري)
    # with open(kb_manager.kb_path, 'r', encoding='utf-8') as f:
    #     print("\nمحتوى ملف knowledge_base.yaml:")
    #     print(f.read())
