# File: /home/ubuntu/ai_web_organized/src/modules/integration_tests/test_agricultural_modules.py
"""
اختبارات تكامل المديولات الزراعية
هذا الملف يحتوي على اختبارات للتحقق من تكامل المديولات الزراعية مع بعضها البعض
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch

from modules.plant_hybridization.hybridization_simulator import HybridizationSimulator
from modules.image_processing.image_processor import ImageProcessor
from modules.disease_diagnosis.disease_knowledge_base import DiseaseKnowledgeBase
from modules.disease_diagnosis.diagnosis_engine import DiagnosisEngine

# إضافة مسار المشروع إلى مسارات البحث
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# استيراد المديولات المطلوبة للاختبار


class TestAgriculturalModulesIntegration(unittest.TestCase):
    """اختبارات تكامل المديولات الزراعية"""

    @classmethod
    def setUpClass(cls):
        """إعداد بيئة الاختبار"""
        # تهيئة قاعدة المعرفة للأمراض
        cls.knowledge_base = DiseaseKnowledgeBase()
        cls.knowledge_base.add_crop('طماطم')
        cls.knowledge_base.add_disease('طماطم', 'اللفحة المتأخرة', {
            'scientific_name': 'Phytophthora infestans',
            'symptoms': ['بقع بنية على الأوراق', 'تعفن الثمار', 'ذبول الأوراق'],
            'visual_symptoms': ['بقع بنية', 'عفن أبيض'],
            'severity': 'high',
            'treatments': ['رش مبيدات فطرية', 'إزالة النباتات المصابة'],
            'prevention': ['تجنب الري العلوي', 'استخدام أصناف مقاومة']
        })

        # تهيئة محرك التشخيص
        cls.diagnosis_engine = DiagnosisEngine(cls.knowledge_base)

        # تهيئة معالج الصور
        cls.image_processor = ImageProcessor()

        # تهيئة محاكي التهجين
        cls.hybridization_simulator = HybridizationSimulator()

        # إنشاء بيانات تجريبية للأصناف
        cls.test_varieties = [
            {
                'id': 'var1',
                'name': 'صنف 1',
                'yield': 5.2,
                'height': 120,
                'maturity_days': 90,
                'disease_resistance': 'high',
                'drought_tolerance': 'medium'
            },
            {
                'id': 'var2',
                'name': 'صنف 2',
                'yield': 4.8,
                'height': 100,
                'maturity_days': 85,
                'disease_resistance': 'medium',
                'drought_tolerance': 'high'
            }
        ]

        # تعيين البيانات التجريبية
        cls.hybridization_simulator.varieties_data = cls.test_varieties

        # إنشاء بيانات تجريبية للصفات
        cls.test_traits = {
            'yield': {
                'type': 'quantitative',
                'inheritance': 'polygenic',
                'importance': 10,
                'target': 7.0
            },
            'disease_resistance': {
                'type': 'qualitative',
                'inheritance': 'dominant',
                'importance': 8,
                'target': 'high',
                'dominant_value': 'high',
                'recessive_value': 'low'
            }
        }

        # تعيين بيانات الصفات
        cls.hybridization_simulator.traits_data = cls.test_traits

    def setUp(self):
        """إعداد قبل كل اختبار"""
        # إنشاء ملف صورة تجريبي
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            self.temp_image = temp_file
            self.temp_image_name = temp_file.name

    def tearDown(self):
        """تنظيف بعد كل اختبار"""
        # حذف ملف الصورة التجريبي
        if os.path.exists(self.temp_image_name):
            os.unlink(self.temp_image_name)

    def test_image_processing_to_diagnosis_integration(self):
        """اختبار تكامل معالجة الصور مع تشخيص الأمراض"""
        # محاكاة تحليل الصورة
        with patch.object(self.image_processor, 'detect_disease_regions') as mock_detect:
            # تكوين المحاكاة للاستجابة بنجاح
            mock_detect.return_value = {
                'success': True,
                'disease_regions': {
                    'all': {
                        'path': self.temp_image_name,
                        'percentage': 25.5
                    },
                    'yellow_spots': {
                        'percentage': 5.2
                    },
                    'brown_spots': {
                        'percentage': 15.8
                    },
                    'white_mold': {
                        'percentage': 4.5
                    }
                },
                'severity': 'medium',
                'image_path': self.temp_image_name
            }

            # تحليل الصورة
            image_analysis = self.image_processor.detect_disease_regions(self.temp_image_name)

            # التحقق من نجاح التحليل
            self.assertTrue(image_analysis['success'])

            # استخدام نتائج تحليل الصورة في التشخيص
            diagnosis_result = self.diagnosis_engine.diagnose_by_image('طماطم', image_analysis)

            # التحقق من نجاح التشخيص
            self.assertTrue(diagnosis_result['success'])
            self.assertEqual(diagnosis_result['crop_type'], 'طماطم')
            self.assertIn('visual_symptoms', diagnosis_result)
            self.assertIn('بقع بنية', diagnosis_result['visual_symptoms'])
            self.assertEqual(diagnosis_result['severity'], 'medium')

    def test_combined_diagnosis_integration(self):
        """اختبار تكامل التشخيص المدمج (الأعراض والصور)"""
        # محاكاة تحليل الصورة
        with patch.object(self.image_processor, 'detect_disease_regions') as mock_detect:
            # تكوين المحاكاة للاستجابة بنجاح
            mock_detect.return_value = {
                'success': True,
                'disease_regions': {
                    'all': {
                        'path': self.temp_image_name,
                        'percentage': 25.5
                    },
                    'brown_spots': {
                        'percentage': 15.8
                    },
                    'white_mold': {
                        'percentage': 9.7
                    }
                },
                'severity': 'medium',
                'image_path': self.temp_image_name
            }

            # تحليل الصورة
            image_analysis = self.image_processor.detect_disease_regions(self.temp_image_name)

            # قائمة الأعراض المدخلة من المستخدم
            symptoms = ['بقع بنية على الأوراق', 'تعفن الثمار']

            # التشخيص المدمج
            diagnosis_result = self.diagnosis_engine.diagnose_combined('طماطم', symptoms, image_analysis)

            # التحقق من نجاح التشخيص
            self.assertTrue(diagnosis_result['success'])
            self.assertEqual(diagnosis_result['crop_type'], 'طماطم')
            self.assertEqual(diagnosis_result['symptoms'], symptoms)
            self.assertIn('visual_symptoms', diagnosis_result)
            self.assertIn('بقع بنية', diagnosis_result['visual_symptoms'])
            self.assertIn('عفن أبيض', diagnosis_result['visual_symptoms'])
            self.assertEqual(diagnosis_result['severity'], 'medium')

            # التحقق من وجود نتائج التشخيص بالأعراض والصورة
            self.assertIn('symptoms_diagnosis', diagnosis_result)
            self.assertIn('image_diagnosis', diagnosis_result)

            # التحقق من المرض الأكثر احتمالاً
            if diagnosis_result['most_likely_disease']:
                self.assertEqual(diagnosis_result['most_likely_disease']['disease'], 'اللفحة المتأخرة')

    def test_hybridization_with_disease_resistance_integration(self):
        """اختبار تكامل محاكاة التهجين مع مقاومة الأمراض"""
        # تشغيل محاكاة التهجين
        simulation_result = self.hybridization_simulator.run_simulation()

        # التحقق من نجاح المحاكاة
        self.assertTrue(simulation_result['success'])

        # الحصول على التوصيات
        recommendations = self.hybridization_simulator.get_recommendations(3)

        # التحقق من نجاح الحصول على التوصيات
        self.assertTrue(recommendations['success'])
        self.assertIn('recommendations', recommendations)
        self.assertGreater(len(recommendations['recommendations']), 0)

        # التحقق من وجود صفة مقاومة الأمراض في التوصيات
        top_recommendation = recommendations['recommendations'][0]
        self.assertIn('traits', top_recommendation)
        self.assertIn('disease_resistance', top_recommendation['traits'])

        # التحقق من قيمة مقاومة الأمراض
        disease_resistance = top_recommendation['traits']['disease_resistance']['value']
        self.assertIn(disease_resistance, ['high', 'medium', 'low'])

    def test_full_agricultural_workflow_integration(self):
        """اختبار تكامل سير العمل الزراعي الكامل"""
        # 1. تحليل صورة للكشف عن الأمراض
        with patch.object(self.image_processor, 'analyze_image') as mock_analyze:
            # تكوين المحاكاة للاستجابة بنجاح
            mock_analyze.return_value = {
                'success': True,
                'results': [
                    {'class': 'مرض_1', 'probability': 0.85},
                    {'class': 'سليم', 'probability': 0.10},
                    {'class': 'مرض_2', 'probability': 0.05}
                ],
                'top_result': {'class': 'مرض_1', 'probability': 0.85},
                'is_disease': True,
                'image_path': self.temp_image_name
            }

            # تحليل الصورة
            image_analysis = self.image_processor.analyze_image(self.temp_image_name)

            # التحقق من نجاح التحليل
            self.assertTrue(image_analysis['success'])
            self.assertTrue(image_analysis['is_disease'])

        # 2. استخراج مناطق المرض من الصورة
        with patch.object(self.image_processor, 'detect_disease_regions') as mock_detect:
            # تكوين المحاكاة للاستجابة بنجاح
            mock_detect.return_value = {
                'success': True,
                'disease_regions': {
                    'all': {
                        'path': self.temp_image_name,
                        'percentage': 25.5
                    },
                    'brown_spots': {
                        'percentage': 15.8
                    },
                    'white_mold': {
                        'percentage': 9.7
                    }
                },
                'severity': 'medium',
                'image_path': self.temp_image_name
            }

            # تحليل مناطق المرض
            regions_analysis = self.image_processor.detect_disease_regions(self.temp_image_name)

            # التحقق من نجاح التحليل
            self.assertTrue(regions_analysis['success'])
            self.assertEqual(regions_analysis['severity'], 'medium')

        # 3. تشخيص المرض بناءً على تحليل الصورة
        diagnosis_result = self.diagnosis_engine.diagnose_by_image('طماطم', regions_analysis)

        # التحقق من نجاح التشخيص
        self.assertTrue(diagnosis_result['success'])

        # 4. الحصول على توصيات العلاج
        if diagnosis_result['most_likely_disease']:
            disease_name = diagnosis_result['most_likely_disease']['disease']
            treatment_result = self.diagnosis_engine.get_treatment_recommendations(disease_name)

            # التحقق من نجاح الحصول على التوصيات
            self.assertTrue(treatment_result['success'])
            self.assertIn('treatments', treatment_result)
            self.assertIn('prevention', treatment_result)

        # 5. محاكاة التهجين لتحسين مقاومة الأمراض
        # تحديث أهداف التهجين بناءً على المرض المكتشف
        self.hybridization_simulator.set_breeding_objectives({
            'disease_resistance': 'high',
            'disease_resistance_importance': 10  # أهمية قصوى
        })

        # تشغيل محاكاة التهجين
        simulation_result = self.hybridization_simulator.run_simulation()

        # التحقق من نجاح المحاكاة
        self.assertTrue(simulation_result['success'])

        # الحصول على التوصيات
        recommendations = self.hybridization_simulator.get_recommendations(1)

        # التحقق من نجاح الحصول على التوصيات
        self.assertTrue(recommendations['success'])
        self.assertGreater(len(recommendations['recommendations']), 0)

        # التحقق من أن الهجين الموصى به له مقاومة عالية للأمراض
        top_recommendation = recommendations['recommendations'][0]
        disease_resistance = top_recommendation['traits']['disease_resistance']['value']
        self.assertEqual(disease_resistance, 'high')


if __name__ == '__main__':
    unittest.main()
