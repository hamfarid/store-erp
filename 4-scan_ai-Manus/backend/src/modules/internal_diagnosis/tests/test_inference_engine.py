# /home/ubuntu/ai_web_organized/src/modules/internal_diagnosis/tests/test_inference_engine.py

"""
اختبارات وحدوية لـ InferenceEngine في وحدة محرك التشخيص.
"""

import os
import shutil
import unittest

from ..inference_engine import InferenceEngine
from ..knowledge_base_manager import KnowledgeBaseManager

# استيراد النماذج والمديرين اللازمين للاختبار
from ..models import DiagnosisRequest, KnowledgeBaseEntry


class TestInferenceEngine(unittest.TestCase):
    """مجموعة اختبارات لـ InferenceEngine."""

    def setUp(self):
        """إعداد بيئة الاختبار لكل اختبار."""
        # إعداد KnowledgeBaseManager وهمي أو حقيقي ببيانات اختبار
        self.test_kb_dir = "test_inference_kb_temp_dir"
        os.makedirs(self.test_kb_dir, exist_ok=True)
        self.kb_file_path = os.path.join(
            self.test_kb_dir, "test_inference_kb.yaml")

        # بيانات اختبار لقاعدة المعرفة
        self.kb_entry1 = KnowledgeBaseEntry(
            entry_id="kb1",
            disease_name="اللفحة المبكرة",
            symptoms=["بقع داكنة على الأوراق", "حلقات متحدة المركز"],
            description="مرض فطري يصيب الطماطم.",
            affected_plants=["الطماطم"],
            treatments=["مبيد فطري أ", "إزالة الأوراق المصابة"],
            prevention=["تناوب المحاصيل"]
        )
        self.kb_entry2 = KnowledgeBaseEntry(
            entry_id="kb2",
            disease_name="البياض الدقيقي",
            symptoms=["طبقة بيضاء تشبه الدقيق", "تشوه الأوراق"],
            description="مرض فطري شائع.",
            affected_plants=["الخيار", "العنب"],
            treatments=["مبيد فطري ب"],
            prevention=["تهوية جيدة"]
        )
        self.kb_entry3 = KnowledgeBaseEntry(
            entry_id="kb3",
            disease_name="نقص المغنيسيوم",
            symptoms=["اصفرار بين عروق الأوراق القديمة", "سقوط مبكر للأوراق"],
            description="نقص عنصر غذائي.",
            affected_plants=["الطماطم", "الفلفل"],
            treatments=["رش سماد ورقي يحتوي على المغنيسيوم"],
            prevention=["تسميد متوازن"]
        )

        # استخدام KnowledgeBaseManager حقيقي مع ملف مؤقت
        self.kb_manager_instance = KnowledgeBaseManager(
            kb_path=self.kb_file_path, create_if_not_exists=True)
        self.kb_manager_instance.add_entry(self.kb_entry1)
        self.kb_manager_instance.add_entry(self.kb_entry2)
        self.kb_manager_instance.add_entry(self.kb_entry3)

        # تهيئة InferenceEngine مع المدير الحقيقي
        self.inference_engine = InferenceEngine(
            knowledge_base_manager=self.kb_manager_instance)

    def tearDown(self):
        """تنظيف بيئة الاختبار بعد كل اختبار."""
        if os.path.exists(self.test_kb_dir):
            shutil.rmtree(self.test_kb_dir)

    def test_01_infer_from_symptoms_direct_match(self):
        """اختبار الاستدلال من الأعراض مع تطابق مباشر لكلمة مفتاحية."""
        request = DiagnosisRequest(
            symptoms_description="الأوراق بها بقع داكنة")
        results = self.inference_engine.perform_inference(request_data=request)

        self.assertGreater(len(results), 0)
        # نتوقع أن يكون "اللفحة المبكرة" هو الأعلى ثقة أو الوحيد
        found_early_blight = any(
            r.disease_name == "اللفحة المبكرة" for r in results)
        self.assertTrue(
            found_early_blight,
            "لم يتم تشخيص اللفحة المبكرة بناءً على الأعراض")
        if found_early_blight:
            early_blight_res = next(
                r for r in results if r.disease_name == "اللفحة المبكرة")
            self.assertIn(
                "بقع داكنة",
                early_blight_res.evidence[0].lower() if early_blight_res.evidence else "")

    def test_02_infer_from_symptoms_multiple_keywords(self):
        """اختبار الاستدلال من الأعراض مع عدة كلمات مفتاحية."""
        request = DiagnosisRequest(
            symptoms_description="الطماطم تعاني من اصفرار الأوراق القديمة وسقوطها")
        results = self.inference_engine.perform_inference(request_data=request)

        self.assertGreater(len(results), 0)
        found_magnesium_deficiency = any(
            r.disease_name == "نقص المغنيسيوم" for r in results)
        self.assertTrue(
            found_magnesium_deficiency,
            "لم يتم تشخيص نقص المغنيسيوم")
        if found_magnesium_deficiency:
            mag_def_res = next(
                r for r in results if r.disease_name == "نقص المغنيسيوم")
            self.assertGreaterEqual(
                mag_def_res.confidence,
                0.2)  # يجب أن تكون الثقة معقولة

    def test_03_infer_from_ml_outputs(self):
        """اختبار الاستدلال من مخرجات نماذج التعلم الآلي."""
        ml_outputs = [
            {
                "model_type": "classification",
                "predictions": [
                    {"label": "اللفحة المبكرة", "confidence": 0.95},
                    {"label": "البياض الدقيقي", "confidence": 0.15}
                ]
            }
        ]
        # لا توجد أعراض، فقط مخرجات نموذج
        request = DiagnosisRequest(plant_type="طماطم")
        results = self.inference_engine.perform_inference(
            request_data=request, ml_model_outputs=ml_outputs)

        self.assertEqual(len(results), 2)  # نتوقع نتيجتين من النموذج
        results.sort(key=lambda r: r.confidence, reverse=True)
        self.assertEqual(results[0].disease_name, "اللفحة المبكرة")
        self.assertAlmostEqual(results[0].confidence, 0.95)
        self.assertEqual(results[0].source, "ml_model_classification")
        self.assertIn("مبيد فطري أ", results[0].treatment_suggestions)

        self.assertEqual(results[1].disease_name, "البياض الدقيقي")
        self.assertAlmostEqual(results[1].confidence, 0.15)

    def test_04_infer_with_both_symptoms_and_ml(self):
        """اختبار الاستدلال مع وجود أعراض ومخرجات نماذج معًا."""
        ml_outputs = [{"model_type": "classification", "predictions": [
            {"label": "البياض الدقيقي", "confidence": 0.88}]}]
        # الأعراض تشير إلى اللفحة المبكرة، النموذج يشير إلى البياض الدقيقي
        request = DiagnosisRequest(
            symptoms_description="بقع داكنة وحلقات على أوراق الطماطم")
        results = self.inference_engine.perform_inference(
            request_data=request, ml_model_outputs=ml_outputs)

        # نتوقع أن يتم دمج النتائج أو إعطاء الأولوية للنموذج إذا كانت ثقته عالية
        # في التنفيذ الحالي، يتم تجميع النتائج ثم إزالة التكرار مع اختيار
        # الأعلى ثقة
        self.assertGreaterEqual(len(results), 1)

        found_powdery_mildew = any(
            r.disease_name == "البياض الدقيقي" for r in results)
        found_early_blight_from_symptoms = any(
            r.disease_name == "اللفحة المبكرة" and r.source == "knowledge_base_symptoms" for r in results)

        self.assertTrue(
            found_powdery_mildew,
            "البياض الدقيقي من النموذج يجب أن يكون موجودًا")
        self.assertTrue(
            found_early_blight_from_symptoms,
            "اللفحة المبكرة من الأعراض يجب أن تكون موجودة")

        # التحقق من أن نتيجة البياض الدقيقي لها الثقة الأعلى
        results.sort(key=lambda r: r.confidence, reverse=True)
        if results:
            self.assertEqual(results[0].disease_name, "البياض الدقيقي")
            self.assertAlmostEqual(results[0].confidence, 0.88)

    def test_05_infer_no_sufficient_data(self):
        """اختبار الاستدلال عند عدم وجود بيانات كافية."""
        request = DiagnosisRequest()  # لا أعراض ولا مخرجات نماذج
        results = self.inference_engine.perform_inference(request_data=request)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].disease_name, "غير قادر على التشخيص")
        self.assertEqual(results[0].confidence, 0.0)
        self.assertIn("لا توجد بيانات كافية", results[0].description)

    def test_06_infer_from_ml_anomaly_detection(self):
        """اختبار الاستدلال من مخرجات نموذج كشف الشذوذ."""
        ml_outputs = [{"model_type": "anomaly_detection", "predictions": {
            "is_anomalous": True, "details": "تم اكتشاف بقع غير منتظمة", "confidence": 0.75}}]
        request = DiagnosisRequest(plant_type="خيار")
        results = self.inference_engine.perform_inference(
            request_data=request, ml_model_outputs=ml_outputs)

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].disease_name,
            "شذوذ مكتشف (يتطلب مزيدًا من التحليل)")
        self.assertAlmostEqual(results[0].confidence, 0.75)
        self.assertIn("بقع غير منتظمة", results[0].description)
        self.assertEqual(results[0].source, "ml_model_anomaly_detection")

    def test_07_find_kb_entry_for_disease_exact_match(self):
        """اختبار العثور على مدخل في قاعدة المعرفة بتطابق تام لاسم المرض."""
        entry = self.inference_engine._find_kb_entry_for_disease(
            "اللفحة المبكرة")
        self.assertIsNotNone(entry)
        self.assertEqual(entry.disease_name, "اللفحة المبكرة")

    def test_08_find_kb_entry_for_disease_case_insensitive(self):
        """اختبار العثور على مدخل في قاعدة المعرفة بتطابق غير حساس لحالة الأحرف."""
        entry = self.inference_engine._find_kb_entry_for_disease(
            "البياض الدقيقي")  # الاسم في القاعدة "البياض الدقيقي"
        self.assertIsNotNone(entry)
        self.assertEqual(entry.disease_name, "البياض الدقيقي")

    def test_09_find_kb_entry_for_disease_no_match(self):
        """اختبار عدم العثور على مدخل لاسم مرض غير موجود."""
        entry = self.inference_engine._find_kb_entry_for_disease(
            "مرض خيالي غير موجود")
        self.assertIsNone(entry)

    def test_10_symptom_inference_confidence_scaling(self):
        """اختبار كيفية تأثير عدد الكلمات المفتاحية المطابقة على الثقة."""
        # كلمة مفتاحية واحدة مطابقة لـ "اللفحة المبكرة"
        request1 = DiagnosisRequest(symptoms_description="بقع")
        results1 = self.inference_engine.perform_inference(
            request_data=request1)
        early_blight_res1 = next(
            (r for r in results1 if r.disease_name == "اللفحة المبكرة"), None)
        self.assertIsNotNone(early_blight_res1)
        confidence1 = early_blight_res1.confidence

        # كلمتان مفتاحيتان مطابقتان لـ "اللفحة المبكرة"
        request2 = DiagnosisRequest(symptoms_description="بقع داكنة وحلقات")
        results2 = self.inference_engine.perform_inference(
            request_data=request2)
        early_blight_res2 = next(
            (r for r in results2 if r.disease_name == "اللفحة المبكرة"), None)
        self.assertIsNotNone(early_blight_res2)
        confidence2 = early_blight_res2.confidence

        # نتوقع أن تكون الثقة أعلى مع المزيد من الكلمات المفتاحية المطابقة (حتى حد معين)
        # هذا يعتمد على منطق حساب الثقة في _infer_from_symptoms
        self.assertGreater(confidence2, confidence1)


if __name__ == '__main__':
    unittest.main()
