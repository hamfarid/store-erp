# /home/ubuntu/ai_web_organized/src/modules/internal_diagnosis/inference_engine.py
# -*- coding: utf-8 -*-
"""Inference Engine Module for AI Web Organized project."""

import os
from typing import Any, Dict, List, Optional

import yaml

from .models import DiagnosisRequest, DiagnosisResult, KnowledgeBaseEntry

# تم إضافة استيرادات المكتبات المفقودة لإصلاح الأخطاء

# يتطلب تهيئة KnowledgeBaseManager بشكل صحيح
# افتراض وجود ملف knowledge_base.yaml صالح
kb_file_path = os.path.join(
    os.path.dirname(__file__),
    "knowledge_base.yaml")
if not os.path.exists(kb_file_path):
    # إنشاء ملف وهمي إذا لم يكن موجودًا للاختبار
    dummy_kb_data = [{"entry_id": "1",
                      "disease_name": "اللفحة المبكرة",
                      "symptoms": ["بقع داكنة على الأوراق",
                                   "حلقات متحدة المركز"]}]
    with open(kb_file_path, 'w', encoding='utf-8') as file:
        yaml.dump(dummy_kb_data, file, allow_unicode=True)


class InferenceEngine:
    """محرك الاستنتاج للتشخيص الداخلي."""

    def __init__(self, knowledge_base_path=None, knowledge_base_manager=None):
        """تهيئة محرك الاستنتاج.

        Args:
            knowledge_base_path: مسار قاعدة المعرفة (اختياري)
            knowledge_base_manager: مدير قاعدة المعرفة (اختياري)
        """
        if knowledge_base_manager is not None:
            self.kb_manager = knowledge_base_manager
            self.knowledge_base = []
        else:
            if knowledge_base_path is None:
                knowledge_base_path = kb_file_path
            self.kb_path = knowledge_base_path
            self.knowledge_base = self._load_knowledge_base()
            self.kb_manager = None

    def _load_knowledge_base(self):
        """تحميل قاعدة المعرفة من الملف.

        Returns:
            قاعدة المعرفة المحملة
        """
        try:
            with open(self.kb_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"خطأ في تحميل قاعدة المعرفة: {e}")
            return []

    def perform_inference(self,
                          request_data: DiagnosisRequest,
                          ml_model_outputs: Optional[List[Dict[str,
                                                               Any]]] = None) -> List[DiagnosisResult]:
        """تنفيذ الاستدلال بناءً على البيانات المقدمة.

        Args:
            request_data: بيانات طلب التشخيص
            ml_model_outputs: مخرجات نماذج التعلم الآلي (اختياري)

        Returns:
            قائمة بنتائج التشخيص
        """
        results = []

        # الاستدلال من الأعراض
        if hasattr(
                request_data,
                'symptoms_description') and request_data.symptoms_description:
            symptom_results = self._infer_from_symptoms(
                request_data.symptoms_description)
            results.extend(symptom_results)

        # الاستدلال من مخرجات نماذج التعلم الآلي
        if ml_model_outputs:
            ml_results = self._infer_from_ml_outputs(ml_model_outputs)
            results.extend(ml_results)

        # إذا لم توجد نتائج، إرجاع نتيجة افتراضية
        if not results:
            results.append(DiagnosisResult(
                disease_name="غير قادر على التشخيص",
                confidence=0.0,
                description="لا توجد بيانات كافية للتشخيص",
                source="inference_engine",
                evidence=[],
                treatment_suggestions=[],
                prevention_suggestions=[]
            ))

        # إزالة التكرار وترتيب النتائج
        results = self._deduplicate_and_sort_results(results)
        return results

    def _infer_from_symptoms(
            self,
            symptoms_description: str) -> List[DiagnosisResult]:
        """الاستدلال من وصف الأعراض.

        Args:
            symptoms_description: وصف الأعراض

        Returns:
            قائمة بنتائج التشخيص
        """
        results = []

        if self.kb_manager:
            # استخدام مدير قاعدة المعرفة
            entries = self.kb_manager.get_all_entries()
            for entry in entries:
                confidence = self._calculate_symptom_match_confidence(
                    symptoms_description, entry.symptoms)
                if confidence > 0.1:  # حد أدنى للثقة
                    results.append(DiagnosisResult(
                        disease_name=entry.disease_name,
                        confidence=confidence,
                        description=entry.description,
                        source="knowledge_base_symptoms",
                        evidence=[symptoms_description],
                        treatment_suggestions=entry.treatments,
                        prevention_suggestions=entry.prevention
                    ))

        return results

    def _infer_from_ml_outputs(
            self, ml_outputs: List[Dict[str, Any]]) -> List[DiagnosisResult]:
        """الاستدلال من مخرجات نماذج التعلم الآلي.

        Args:
            ml_outputs: مخرجات النماذج

        Returns:
            قائمة بنتائج التشخيص
        """
        results = []

        for output in ml_outputs:
            model_type = output.get("model_type", "unknown")

            if model_type == "classification":
                predictions = output.get("predictions", [])
                for pred in predictions:
                    kb_entry = self._find_kb_entry_for_disease(pred["label"])
                    results.append(
                        DiagnosisResult(
                            disease_name=pred["label"],
                            confidence=pred["confidence"],
                            description=kb_entry.description if kb_entry else "تشخيص من نموذج التصنيف",
                            source=f"ml_model_{model_type}",
                            evidence=[],
                            treatment_suggestions=kb_entry.treatments if kb_entry else [],
                            prevention_suggestions=kb_entry.prevention if kb_entry else []))

            elif model_type == "anomaly_detection":
                predictions = output.get("predictions", {})
                if predictions.get("is_anomalous", False):
                    results.append(
                        DiagnosisResult(
                            disease_name="شذوذ مكتشف (يتطلب مزيدًا من التحليل)",
                            confidence=predictions.get(
                                "confidence",
                                0.5),
                            description=predictions.get(
                                "details",
                                "تم اكتشاف شذوذ"),
                            source=f"ml_model_{model_type}",
                            evidence=[],
                            treatment_suggestions=["يتطلب فحص إضافي"],
                            prevention_suggestions=[]))

        return results

    def _find_kb_entry_for_disease(
            self, disease_name: str) -> Optional[KnowledgeBaseEntry]:
        """البحث عن مدخل في قاعدة المعرفة بناءً على اسم المرض.

        Args:
            disease_name: اسم المرض

        Returns:
            مدخل قاعدة المعرفة أو None
        """
        if self.kb_manager:
            entries = self.kb_manager.get_all_entries()
            for entry in entries:
                if entry.disease_name.lower() == disease_name.lower():
                    return entry

        return None

    def _calculate_symptom_match_confidence(
            self,
            symptoms_description: str,
            known_symptoms: List[str]) -> float:
        """حساب مستوى الثقة في تطابق الأعراض.

        Args:
            symptoms_description: وصف الأعراض
            known_symptoms: الأعراض المعروفة

        Returns:
            مستوى الثقة (0-1)
        """
        if not known_symptoms:
            return 0.0

        symptoms_lower = symptoms_description.lower()
        matches = 0

        for symptom in known_symptoms:
            if any(word in symptoms_lower for word in symptom.lower().split()):
                matches += 1

        return min(matches / len(known_symptoms), 1.0)

    def _deduplicate_and_sort_results(
            self, results: List[DiagnosisResult]) -> List[DiagnosisResult]:
        """إزالة التكرار وترتيب النتائج حسب الثقة.

        Args:
            results: قائمة النتائج

        Returns:
            قائمة النتائج مرتبة ومنظفة
        """
        # إزالة التكرار بناءً على اسم المرض، الاحتفاظ بالأعلى ثقة
        unique_results = {}
        for result in results:
            if result.disease_name not in unique_results or result.confidence > unique_results[
                    result.disease_name].confidence:
                unique_results[result.disease_name] = result

        # ترتيب حسب الثقة
        sorted_results = sorted(
            unique_results.values(),
            key=lambda x: x.confidence,
            reverse=True)
        return sorted_results
