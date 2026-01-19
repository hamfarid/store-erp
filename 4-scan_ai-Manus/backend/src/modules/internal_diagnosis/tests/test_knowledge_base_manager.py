# /home/ubuntu/ai_web_organized/src/modules/internal_diagnosis/tests/test_knowledge_base_manager.py

"""
اختبارات وحدوية لـ KnowledgeBaseManager في وحدة محرك التشخيص.
"""

import os
import shutil
import unittest
import uuid

import yaml

from ..knowledge_base_manager import KnowledgeBaseManager
from ..models import KnowledgeBaseEntry


class TestKnowledgeBaseManager(unittest.TestCase):
    """مجموعة اختبارات لـ KnowledgeBaseManager."""

    def setUp(self):
        """إعداد بيئة الاختبار لكل اختبار."""
        self.test_kb_dir = "test_kb_temp_dir"
        os.makedirs(self.test_kb_dir, exist_ok=True)
        self.kb_file_path = os.path.join(self.test_kb_dir, "test_kb.yaml")
        self.kb_manager = KnowledgeBaseManager(
            kb_path=self.kb_file_path, create_if_not_exists=True)

        # بيانات اختبار أولية
        self.entry1_data = {
            "disease_name": "الصدأ الأصفر",
            "symptoms": [
                "بقع صفراء على الأوراق",
                "ضعف عام في النبات"],
            "description": "مرض فطري يصيب القمح.",
            "affected_plants": [
                "القمح",
                "الشعير"],
            "treatments": [
                "مبيد فطري متخصص",
                "التخلص من بقايا المحصول المصاب"],
            "prevention": [
                "زراعة أصناف مقاومة",
                "دورة زراعية مناسبة"]}
        self.entry2_data = {
            "disease_name": "تجعد أوراق الخوخ",
            "symptoms": [
                "تجعد وتشوه الأوراق",
                "تلون الأوراق باللون الأحمر أو الأصفر"],
            "description": "مرض فطري يصيب أشجار الخوخ واللوز.",
            "affected_plants": [
                "الخوخ",
                "اللوز",
                "النكتارين"],
            "treatments": ["رش مبيدات فطرية نحاسية في فترة السكون"],
            "prevention": [
                "جمع الأوراق المتساقطة وحرقها",
                "تقليم الأفرع المصابة"]}

    def tearDown(self):
        """تنظيف بيئة الاختبار بعد كل اختبار."""
        if os.path.exists(self.test_kb_dir):
            shutil.rmtree(self.test_kb_dir)

    def test_01_initialization_and_load_empty_kb(self):
        """اختبار تهيئة المدير وتحميل قاعدة معرفة فارغة."""
        self.assertIsNotNone(self.kb_manager)
        self.assertEqual(len(self.kb_manager.get_all_entries()), 0)
        self.assertTrue(os.path.exists(self.kb_file_path))

    def test_02_add_entry(self):
        """اختبار إضافة مدخل جديد إلى قاعدة المعرفة."""
        added_entry = self.kb_manager.add_entry(self.entry1_data)
        self.assertIsNotNone(added_entry)
        self.assertIsInstance(added_entry, KnowledgeBaseEntry)
        self.assertEqual(
            added_entry.disease_name,
            self.entry1_data["disease_name"])
        self.assertIsNotNone(added_entry.entry_id)
        self.assertEqual(len(self.kb_manager.get_all_entries()), 1)

        # التحقق من الحفظ في الملف
        with open(self.kb_file_path, 'r', encoding='utf-8') as f:
            kb_from_file = yaml.safe_load(f)
        self.assertEqual(len(kb_from_file), 1)
        self.assertEqual(
            kb_from_file[0]["disease_name"],
            self.entry1_data["disease_name"])

    def test_03_add_multiple_entries(self):
        """اختبار إضافة عدة مدخلات."""
        self.kb_manager.add_entry(self.entry1_data)
        self.kb_manager.add_entry(self.entry2_data)
        self.assertEqual(len(self.kb_manager.get_all_entries()), 2)

    def test_04_get_entry_by_id(self):
        """اختبار استرجاع مدخل بواسطة المعرف."""
        added_entry = self.kb_manager.add_entry(self.entry1_data)
        self.assertIsNotNone(added_entry)
        retrieved_entry = self.kb_manager.get_entry_by_id(added_entry.entry_id)
        self.assertIsNotNone(retrieved_entry)
        self.assertEqual(
            retrieved_entry.disease_name,
            self.entry1_data["disease_name"])

        non_existent_entry = self.kb_manager.get_entry_by_id(str(uuid.uuid4()))
        self.assertIsNone(non_existent_entry)

    def test_05_update_entry(self):
        """اختبار تحديث مدخل موجود."""
        added_entry = self.kb_manager.add_entry(self.entry1_data)
        self.assertIsNotNone(added_entry)

        update_data = {"description": "وصف محدث لمرض الصدأ الأصفر."}
        updated_entry = self.kb_manager.update_entry(
            added_entry.entry_id, update_data)
        self.assertIsNotNone(updated_entry)
        self.assertEqual(updated_entry.description, update_data["description"])
        self.assertNotEqual(
            updated_entry.last_updated,
            added_entry.last_updated)

        # التحقق من أن المدخل الأصلي تم تحديثه في القائمة الداخلية
        retrieved_after_update = self.kb_manager.get_entry_by_id(
            added_entry.entry_id)
        self.assertEqual(
            retrieved_after_update.description,
            update_data["description"])

        # اختبار تحديث مدخل غير موجود
        failed_update = self.kb_manager.update_entry(
            str(uuid.uuid4()), {"description": "test"})
        self.assertIsNone(failed_update)

    def test_06_delete_entry(self):
        """اختبار حذف مدخل."""
        added_entry1 = self.kb_manager.add_entry(self.entry1_data)
        self.kb_manager.add_entry(self.entry2_data)
        self.assertEqual(len(self.kb_manager.get_all_entries()), 2)

        delete_successful = self.kb_manager.delete_entry(added_entry1.entry_id)
        self.assertTrue(delete_successful)
        self.assertEqual(len(self.kb_manager.get_all_entries()), 1)
        self.assertIsNone(
            self.kb_manager.get_entry_by_id(
                added_entry1.entry_id))

        # اختبار حذف مدخل غير موجود
        delete_failed = self.kb_manager.delete_entry(str(uuid.uuid4()))
        self.assertFalse(delete_failed)

    def test_07_search_entries(self):
        """اختبار البحث في قاعدة المعرفة."""
        self.kb_manager.add_entry(self.entry1_data)  # الصدأ الأصفر (القمح)
        self.kb_manager.add_entry(self.entry2_data)  # تجعد أوراق الخوخ

        # بحث عام
        results_قمح = self.kb_manager.search_entries("القمح")
        self.assertEqual(len(results_قمح), 1)
        self.assertEqual(results_قمح[0].disease_name, "الصدأ الأصفر")

        results_خوخ = self.kb_manager.search_entries("الخوخ")
        self.assertEqual(len(results_خوخ), 1)
        self.assertEqual(results_خوخ[0].disease_name, "تجعد أوراق الخوخ")

        # بحث في حقل محدد (الأعراض)
        results_بقع = self.kb_manager.search_entries(
            "بقع", fields=["symptoms"])
        self.assertEqual(len(results_بقع), 1)
        self.assertEqual(results_بقع[0].disease_name, "الصدأ الأصفر")

        # بحث غير حساس لحالة الأحرف
        results_yellow = self.kb_manager.search_entries(
            "أصفر", fields=["symptoms"])
        # "أصفر" في أعراض الصدأ و "الأصفر" في تجعد الأوراق
        self.assertEqual(len(results_yellow), 2)

        # بحث لا يوجد له نتائج
        results_none = self.kb_manager.search_entries("مرض غير موجود إطلاقا")
        self.assertEqual(len(results_none), 0)

    def test_08_get_all_entries(self):
        """اختبار استرجاع جميع المدخلات."""
        self.assertEqual(len(self.kb_manager.get_all_entries()), 0)
        self.kb_manager.add_entry(self.entry1_data)
        self.assertEqual(len(self.kb_manager.get_all_entries()), 1)
        self.kb_manager.add_entry(self.entry2_data)
        self.assertEqual(len(self.kb_manager.get_all_entries()), 2)

    def test_09_reload_knowledge_base(self):
        """اختبار إعادة تحميل قاعدة المعرفة."""
        self.kb_manager.add_entry(self.entry1_data)
        self.assertEqual(len(self.kb_manager.get_all_entries()), 1)

        # تعديل الملف يدويًا لمحاكاة تغيير خارجي
        with open(self.kb_file_path, 'r', encoding='utf-8') as f:
            current_kb_data = yaml.safe_load(f)

        current_kb_data.append(KnowledgeBaseEntry(
            **self.entry2_data).model_dump(exclude_none=True))
        with open(self.kb_file_path, 'w', encoding='utf-8') as f:
            yaml.dump(current_kb_data, f, allow_unicode=True, sort_keys=False)

        self.kb_manager.reload_knowledge_base()
        self.assertEqual(len(self.kb_manager.get_all_entries()), 2)
        found_entry2 = any(
            e.disease_name == self.entry2_data["disease_name"] for e in self.kb_manager.get_all_entries())
        self.assertTrue(found_entry2)

    def test_10_add_entry_with_invalid_data(self):
        """اختبار إضافة مدخل ببيانات غير صالحة (يجب أن يفشل التحقق من Pydantic)."""
        invalid_data = {"disease_name": "مرض بدون أعراض"}  # الأعراض حقل مطلوب
        added_entry = self.kb_manager.add_entry(invalid_data)
        self.assertIsNone(added_entry)
        self.assertEqual(len(self.kb_manager.get_all_entries()), 0)

    def test_11_load_kb_with_invalid_entries_in_file(self):
        """اختبار تحميل قاعدة معرفة تحتوي على مدخلات صالحة وغير صالحة في الملف."""
        valid_entry_dict = KnowledgeBaseEntry(
            **self.entry1_data).model_dump(exclude_none=True)
        invalid_entry_dict = {"name": "مرض غير صالح", "symptom_list": ["خطأ"]}

        with open(self.kb_file_path, 'w', encoding='utf-8') as f:
            yaml.dump([valid_entry_dict, invalid_entry_dict],
                      f, allow_unicode=True, sort_keys=False)

        # إعادة تهيئة المدير ليقوم بالتحميل من الملف المعدل
        new_kb_manager = KnowledgeBaseManager(kb_path=self.kb_file_path)
        # يجب تحميل المدخل الصالح فقط
        self.assertEqual(len(new_kb_manager.get_all_entries()), 1)
        self.assertEqual(
            new_kb_manager.get_all_entries()[0].disease_name,
            self.entry1_data["disease_name"])

    def test_12_save_and_load_persistence(self):
        """اختبار أن البيانات المحفوظة يتم تحميلها بشكل صحيح عند إعادة التهيئة."""
        self.kb_manager.add_entry(self.entry1_data)
        self.kb_manager.add_entry(self.entry2_data)
        entry_count_before = len(self.kb_manager.get_all_entries())

        # إنشاء مثيل جديد من المدير بنفس مسار الملف
        new_kb_manager = KnowledgeBaseManager(kb_path=self.kb_file_path)
        self.assertEqual(len(new_kb_manager.get_all_entries()),
                         entry_count_before)
        entry1_found = any(
            e.disease_name == self.entry1_data["disease_name"] for e in new_kb_manager.get_all_entries())
        entry2_found = any(
            e.disease_name == self.entry2_data["disease_name"] for e in new_kb_manager.get_all_entries())
        self.assertTrue(entry1_found)
        self.assertTrue(entry2_found)

    def test_13_handle_empty_yaml_file(self):
        """اختبار التعامل مع ملف YAML فارغ."""
        # إنشاء ملف YAML فارغ
        with open(self.kb_file_path, 'w', encoding='utf-8') as f:
            f.write("")

        empty_kb_manager = KnowledgeBaseManager(kb_path=self.kb_file_path)
        self.assertEqual(len(empty_kb_manager.get_all_entries()), 0)

        # إضافة مدخل إلى قاعدة المعرفة الفارغة
        added_entry = empty_kb_manager.add_entry(self.entry1_data)
        self.assertIsNotNone(added_entry)
        self.assertEqual(len(empty_kb_manager.get_all_entries()), 1)

    def test_14_add_entry_without_id_generates_one(self):
        """اختبار أن إضافة مدخل بدون entry_id يؤدي إلى توليد واحد تلقائيًا."""
        entry_data_no_id = self.entry1_data.copy()
        if "entry_id" in entry_data_no_id:
            del entry_data_no_id["entry_id"]

        added_entry = self.kb_manager.add_entry(entry_data_no_id)
        self.assertIsNotNone(added_entry)
        self.assertIsNotNone(added_entry.entry_id)
        self.assertIsInstance(
            uuid.UUID(
                added_entry.entry_id),
            uuid.UUID)  # التحقق من أنه UUID صالح


if __name__ == '__main__':
    unittest.main()
