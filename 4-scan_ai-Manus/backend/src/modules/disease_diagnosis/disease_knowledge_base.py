# File:
# /home/ubuntu/ai_web_organized/src/modules/disease_diagnosis/disease_knowledge_base.py
"""
from flask import g
قاعدة معرفية للأمراض النباتية
توفر هذه الوحدة قاعدة معرفية للأمراض النباتية وأعراضها وطرق علاجها
"""

import json
import os
from typing import Any, Dict, List, Optional

import yaml


class DiseaseKnowledgeBase:
    """قاعدة معرفية للأمراض النباتية"""

    def __init__(self, knowledge_file: str = None):
        """
        تهيئة قاعدة المعرفة

        Args:
            knowledge_file: مسار ملف قاعدة المعرفة (YAML أو JSON)
        """
        self.knowledge_base = {}
        self.crops = set()
        self.diseases = set()

        # تحميل قاعدة المعرفة الافتراضية إذا لم يتم تحديد ملف
        if knowledge_file is None:
            default_path = os.path.join(
                os.path.dirname(__file__),
                'data',
                'disease_knowledge.yaml')
            if os.path.exists(default_path):
                knowledge_file = default_path

        # تحميل قاعدة المعرفة من الملف إذا كان موجوداً
        if knowledge_file and os.path.exists(knowledge_file):
            self.load_knowledge_base(knowledge_file)
        else:
            # تهيئة قاعدة معرفة افتراضية
            self._init_default_knowledge_base()

    def load_knowledge_base(self, file_path: str) -> None:
        """
        تحميل قاعدة المعرفة من ملف

        Args:
            file_path: مسار الملف (YAML أو JSON)
        """
        try:
            ext = os.path.splitext(file_path)[1].lower()

            if ext in ['.yaml', '.yml']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.knowledge_base = yaml.safe_load(f)
            elif ext == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.knowledge_base = json.load(f)
            else:
                raise ValueError(f"صيغة الملف غير مدعومة: {ext}")

            # استخراج قوائم المحاصيل والأمراض
            self._extract_crops_and_diseases()

            print(f"تم تحميل قاعدة المعرفة بنجاح من {file_path}")
            print(f"عدد المحاصيل: {len(self.crops)}")
            print(f"عدد الأمراض: {len(self.diseases)}")

        except Exception as e:
            print(f"خطأ في تحميل قاعدة المعرفة: {str(e)}")
            # تهيئة قاعدة معرفة افتراضية في حالة الخطأ
            self._init_default_knowledge_base()

    def save_knowledge_base(self, file_path: str) -> None:
        """
        حفظ قاعدة المعرفة إلى ملف

        Args:
            file_path: مسار الملف (YAML أو JSON)
        """
        try:
            # التأكد من وجود المجلد
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            ext = os.path.splitext(file_path)[1].lower()

            if ext in ['.yaml', '.yml']:
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(
                        self.knowledge_base,
                        f,
                        allow_unicode=True,
                        sort_keys=False)
            elif ext == '.json':
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(
                        self.knowledge_base,
                        f,
                        ensure_ascii=False,
                        indent=2)
            else:
                raise ValueError(f"صيغة الملف غير مدعومة: {ext}")

            print(f"تم حفظ قاعدة المعرفة بنجاح إلى {file_path}")

        except Exception as e:
            print(f"خطأ في حفظ قاعدة المعرفة: {str(e)}")

    def _extract_crops_and_diseases(self) -> None:
        """استخراج قوائم المحاصيل والأمراض من قاعدة المعرفة"""
        self.crops = set()
        self.diseases = set()

        for crop in self.knowledge_base.get('crops', []):
            self.crops.add(crop['name'])
            for disease in crop.get('diseases', []):
                self.diseases.add(disease['name'])

    def _init_default_knowledge_base(self) -> None:
        """تهيئة قاعدة معرفة افتراضية"""
        self.knowledge_base = {'crops': [{'name': 'طماطم',
                                          'scientific_name': 'Solanum lycopersicum',
                                          'diseases': [{'name': 'اللفحة المتأخرة',
                                                        'scientific_name': 'Phytophthora infestans',
                                                        'symptoms': ['بقع بنية داكنة على الأوراق',
                                                                     'بقع خضراء مائية على الثمار',
                                                                     'تعفن الثمار',
                                                                     'ظهور نمو أبيض على السطح السفلي للأوراق في الظروف الرطبة'],
                                                        'conditions': ['رطوبة عالية',
                                                                       'درجات حرارة معتدلة (15-25 درجة مئوية)'],
                                                        'treatments': ['استخدام مبيدات فطرية نحاسية',
                                                                       'تجنب الري العلوي',
                                                                       'تحسين تهوية النباتات',
                                                                       'إزالة وتدمير النباتات المصابة'],
                                                        'prevention': ['استخدام أصناف مقاومة',
                                                                       'تناوب المحاصيل',
                                                                       'تجنب الزراعة في المناطق المنخفضة الرطبة'],
                                                        'images': ['late_blight_leaf.jpg',
                                                                   'late_blight_fruit.jpg']},
                                                       {'name': 'البياض الدقيقي',
                                                        'scientific_name': 'Leveillula taurica',
                                                        'symptoms': ['بقع صفراء على الجانب العلوي للأوراق',
                                                                     'نمو أبيض دقيقي على السطح السفلي للأوراق',
                                                                     'جفاف وموت الأوراق المصابة'],
                                                        'conditions': ['طقس جاف ودافئ',
                                                                       'درجات حرارة معتدلة إلى مرتفعة (20-30 درجة مئوية)'],
                                                        'treatments': ['استخدام مبيدات فطرية مثل الكبريت',
                                                                       'استخدام زيوت نباتية',
                                                                       'إزالة الأوراق المصابة بشدة'],
                                                        'prevention': ['استخدام أصناف مقاومة',
                                                                       'تحسين تهوية النباتات',
                                                                       'تجنب الإفراط في التسميد النيتروجيني'],
                                                        'images': ['powdery_mildew_tomato.jpg']}]},
                                         {'name': 'خيار',
                                          'scientific_name': 'Cucumis sativus',
                                          'diseases': [{'name': 'البياض الزغبي',
                                                        'scientific_name': 'Pseudoperonospora cubensis',
                                                        'symptoms': ['بقع صفراء زاوية على الأوراق',
                                                                     'نمو رمادي-بنفسجي على السطح السفلي للأوراق',
                                                                     'جفاف وموت الأوراق المصابة'],
                                                        'conditions': ['رطوبة عالية',
                                                                       'درجات حرارة معتدلة (15-25 درجة مئوية)'],
                                                        'treatments': ['استخدام مبيدات فطرية نحاسية',
                                                                       'تحسين تهوية النباتات',
                                                                       'تقليل الرطوبة حول النباتات'],
                                                        'prevention': ['استخدام أصناف مقاومة',
                                                                       'تناوب المحاصيل',
                                                                       'تجنب الري العلوي'],
                                                        'images': ['downy_mildew_cucumber.jpg']},
                                                       {'name': 'الأنثراكنوز',
                                                        'scientific_name': 'Colletotrichum orbiculare',
                                                        'symptoms': ['بقع دائرية غائرة على الثمار',
                                                                     'بقع بنية على الأوراق',
                                                                     'تقرحات على السيقان'],
                                                        'conditions': ['رطوبة عالية',
                                                                       'درجات حرارة دافئة (20-30 درجة مئوية)'],
                                                        'treatments': ['استخدام مبيدات فطرية',
                                                                       'إزالة وتدمير النباتات المصابة',
                                                                       'تجنب الري العلوي'],
                                                        'prevention': ['استخدام بذور معتمدة خالية من المرض',
                                                                       'تناوب المحاصيل',
                                                                       'تحسين تهوية النباتات'],
                                                        'images': ['anthracnose_cucumber.jpg']}]},
                                         {'name': 'قمح',
                                          'scientific_name': 'Triticum aestivum',
                                          'diseases': [{'name': 'صدأ الساق',
                                                        'scientific_name': 'Puccinia graminis',
                                                        'symptoms': ['بثرات بنية محمرة على السيقان والأوراق',
                                                                     'تمزق الأنسجة النباتية',
                                                                     'ضعف النبات وقلة المحصول'],
                                                        'conditions': ['درجات حرارة دافئة (15-30 درجة مئوية)',
                                                                       'رطوبة عالية أو ندى'],
                                                        'treatments': ['استخدام مبيدات فطرية',
                                                                       'حصاد مبكر إذا كانت الإصابة شديدة'],
                                                        'prevention': ['استخدام أصناف مقاومة',
                                                                       'التخلص من العوائل البديلة مثل نبات البربري',
                                                                       'زراعة مبكرة'],
                                                        'images': ['stem_rust_wheat.jpg']},
                                                       {'name': 'التفحم المغطى',
                                                        'scientific_name': 'Tilletia caries',
                                                        'symptoms': ['استبدال حبوب القمح بكتل سوداء من الجراثيم',
                                                                     'رائحة كريهة تشبه رائحة السمك الفاسد',
                                                                     'سنابل ذات مظهر طبيعي حتى النضج'],
                                                        'conditions': ['تلوث البذور بالجراثيم',
                                                                       'ظروف باردة ورطبة أثناء الإنبات'],
                                                        'treatments': ['لا يوجد علاج بعد ظهور المرض'],
                                                        'prevention': ['معالجة البذور بمبيدات فطرية',
                                                                       'استخدام بذور معتمدة خالية من المرض',
                                                                       'تناوب المحاصيل'],
                                                        'images': ['covered_smut_wheat.jpg']}]}]}

        # استخراج قوائم المحاصيل والأمراض
        self._extract_crops_and_diseases()

        print("تم تهيئة قاعدة معرفة افتراضية")
        print(f"عدد المحاصيل: {len(self.crops)}")
        print(f"عدد الأمراض: {len(self.diseases)}")

    def get_all_crops(self) -> List[Dict[str, Any]]:
        """
        الحصول على قائمة جميع المحاصيل

        Returns:
            قائمة بجميع المحاصيل
        """
        return self.knowledge_base.get('crops', [])

    def get_crop_by_name(self, crop_name: str) -> Optional[Dict[str, Any]]:
        """
        البحث عن محصول باسمه

        Args:
            crop_name: اسم المحصول

        Returns:
            معلومات المحصول أو None إذا لم يتم العثور عليه
        """
        for crop in self.knowledge_base.get('crops', []):
            if crop['name'] == crop_name:
                return crop
        return None

    def get_all_diseases(self) -> List[Dict[str, Any]]:
        """
        الحصول على قائمة جميع الأمراض

        Returns:
            قائمة بجميع الأمراض
        """
        diseases = []
        for crop in self.knowledge_base.get('crops', []):
            for disease in crop.get('diseases', []):
                disease_info = disease.copy()
                disease_info['crop'] = crop['name']
                diseases.append(disease_info)
        return diseases

    def get_diseases_by_crop(self, crop_name: str) -> List[Dict[str, Any]]:
        """
        الحصول على قائمة الأمراض لمحصول معين

        Args:
            crop_name: اسم المحصول

        Returns:
            قائمة بأمراض المحصول
        """
        crop = self.get_crop_by_name(crop_name)
        if crop:
            return crop.get('diseases', [])
        return []

    def get_disease_by_name(self, disease_name: str,
                            crop_name: str = None) -> Optional[Dict[str, Any]]:
        """
        البحث عن مرض باسمه

        Args:
            disease_name: اسم المرض
            crop_name: اسم المحصول (اختياري)

        Returns:
            معلومات المرض أو None إذا لم يتم العثور عليه
        """
        if crop_name:
            # البحث في محصول محدد
            diseases = self.get_diseases_by_crop(crop_name)
            for disease in diseases:
                if disease['name'] == disease_name:
                    return disease
        else:
            # البحث في جميع المحاصيل
            for crop in self.knowledge_base.get('crops', []):
                for disease in crop.get('diseases', []):
                    if disease['name'] == disease_name:
                        disease_info = disease.copy()
                        disease_info['crop'] = crop['name']
                        return disease_info
        return None

    def add_crop(self, crop_data: Dict[str, Any]) -> bool:
        """
        إضافة محصول جديد

        Args:
            crop_data: بيانات المحصول

        Returns:
            True إذا تمت الإضافة بنجاح، False خلاف ذلك
        """
        if 'name' not in crop_data:
            print("خطأ: يجب تحديد اسم المحصول")
            return False

        # التحقق من عدم وجود المحصول مسبقاً
        if crop_data['name'] in self.crops:
            print(f"خطأ: المحصول {crop_data['name']} موجود بالفعل")
            return False

        # إضافة المحصول
        if 'crops' not in self.knowledge_base:
            self.knowledge_base['crops'] = []

        self.knowledge_base['crops'].append(crop_data)
        self.crops.add(crop_data['name'])

        print(f"تمت إضافة المحصول {crop_data['name']} بنجاح")
        return True

    def add_disease(self, crop_name: str,
                    disease_data: Dict[str, Any]) -> bool:
        """
        إضافة مرض جديد لمحصول

        Args:
            crop_name: اسم المحصول
            disease_data: بيانات المرض

        Returns:
            True إذا تمت الإضافة بنجاح، False خلاف ذلك
        """
        if 'name' not in disease_data:
            print("خطأ: يجب تحديد اسم المرض")
            return False

        # البحث عن المحصول
        crop = self.get_crop_by_name(crop_name)
        if not crop:
            print(f"خطأ: المحصول {crop_name} غير موجود")
            return False

        # التحقق من عدم وجود المرض مسبقاً
        for disease in crop.get('diseases', []):
            if disease['name'] == disease_data['name']:
                print(
                    f"خطأ: المرض {disease_data['name']} موجود بالفعل للمحصول {crop_name}")
                return False

        # إضافة المرض
        if 'diseases' not in crop:
            crop['diseases'] = []

        crop['diseases'].append(disease_data)
        self.diseases.add(disease_data['name'])

        print(
            f"تمت إضافة المرض {disease_data['name']} للمحصول {crop_name} بنجاح")
        return True

    def update_crop(self, crop_name: str, crop_data: Dict[str, Any]) -> bool:
        """
        تحديث بيانات محصول

        Args:
            crop_name: اسم المحصول
            crop_data: بيانات المحصول المحدثة

        Returns:
            True إذا تم التحديث بنجاح، False خلاف ذلك
        """
        # البحث عن المحصول
        for i, crop in enumerate(self.knowledge_base.get('crops', [])):
            if crop['name'] == crop_name:
                # الاحتفاظ بقائمة الأمراض إذا لم تكن موجودة في البيانات المحدثة
                if 'diseases' not in crop_data and 'diseases' in crop:
                    crop_data['diseases'] = crop['diseases']

                # تحديث بيانات المحصول
                self.knowledge_base['crops'][i] = crop_data

                # تحديث قائمة المحاصيل إذا تغير الاسم
                if crop_data['name'] != crop_name:
                    self.crops.remove(crop_name)
                    self.crops.add(crop_data['name'])

                print(f"تم تحديث بيانات المحصول {crop_name} بنجاح")
                return True

        print(f"خطأ: المحصول {crop_name} غير موجود")
        return False

    def update_disease(self, disease_name: str, crop_name: str,
                       disease_data: Dict[str, Any]) -> bool:
        """
        تحديث بيانات مرض

        Args:
            disease_name: اسم المرض
            crop_name: اسم المحصول
            disease_data: بيانات المرض المحدثة

        Returns:
            True إذا تم التحديث بنجاح، False خلاف ذلك
        """
        # البحث عن المحصول
        crop = self.get_crop_by_name(crop_name)
        if not crop:
            print(f"خطأ: المحصول {crop_name} غير موجود")
            return False

        # البحث عن المرض
        for i, disease in enumerate(crop.get('diseases', [])):
            if disease['name'] == disease_name:
                # تحديث بيانات المرض
                crop['diseases'][i] = disease_data

                # تحديث قائمة الأمراض إذا تغير الاسم
                if disease_data['name'] != disease_name:
                    self.diseases.remove(disease_name)
                    self.diseases.add(disease_data['name'])

                print(
                    f"تم تحديث بيانات المرض {disease_name} للمحصول {crop_name} بنجاح")
                return True

        print(f"خطأ: المرض {disease_name} غير موجود للمحصول {crop_name}")
        return False

    def delete_crop(self, crop_name: str) -> bool:
        """
        حذف محصول

        Args:
            crop_name: اسم المحصول

        Returns:
            True إذا تم الحذف بنجاح، False خلاف ذلك
        """
        # البحث عن المحصول
        for i, crop in enumerate(self.knowledge_base.get('crops', [])):
            if crop['name'] == crop_name:
                # حذف المحصول
                del self.knowledge_base['crops'][i]
                self.crops.remove(crop_name)

                # تحديث قائمة الأمراض
                self._extract_crops_and_diseases()

                print(f"تم حذف المحصول {crop_name} بنجاح")
                return True

        print(f"خطأ: المحصول {crop_name} غير موجود")
        return False

    def delete_disease(self, disease_name: str, crop_name: str) -> bool:
        """
        حذف مرض

        Args:
            disease_name: اسم المرض
            crop_name: اسم المحصول

        Returns:
            True إذا تم الحذف بنجاح، False خلاف ذلك
        """
        # البحث عن المحصول
        crop = self.get_crop_by_name(crop_name)
        if not crop:
            print(f"خطأ: المحصول {crop_name} غير موجود")
            return False

        # البحث عن المرض
        for i, disease in enumerate(crop.get('diseases', [])):
            if disease['name'] == disease_name:
                # حذف المرض
                del crop['diseases'][i]

                # تحديث قائمة الأمراض
                self._extract_crops_and_diseases()

                print(
                    f"تم حذف المرض {disease_name} من المحصول {crop_name} بنجاح")
                return True

        print(f"خطأ: المرض {disease_name} غير موجود للمحصول {crop_name}")
        return False

    def search_diseases_by_symptoms(
            self, symptoms: List[str]) -> List[Dict[str, Any]]:
        """
        البحث عن الأمراض بناءً على الأعراض

        Args:
            symptoms: قائمة الأعراض

        Returns:
            قائمة بالأمراض المطابقة مع درجة التطابق
        """
        matching_diseases = []

        for crop in self.knowledge_base.get('crops', []):
            for disease in crop.get('diseases', []):
                if 'symptoms' in disease:
                    # حساب عدد الأعراض المتطابقة
                    matching_symptoms = [
                        s for s in symptoms if any(
                            s.lower() in ds.lower() for ds in disease['symptoms'])]
                    match_count = len(matching_symptoms)

                    if match_count > 0:
                        # حساب درجة التطابق
                        match_score = match_count / len(disease['symptoms'])

                        # إضافة المرض إلى القائمة
                        result = {
                            'disease': disease['name'],
                            'crop': crop['name'],
                            'match_score': match_score,
                            'matching_symptoms': matching_symptoms,
                            'disease_info': disease
                        }
                        matching_diseases.append(result)

        # ترتيب النتائج حسب درجة التطابق
        matching_diseases.sort(key=lambda x: x['match_score'], reverse=True)

        return matching_diseases


# اختبار الوحدة إذا تم تشغيل الملف مباشرة
if __name__ == "__main__":
    # إنشاء مجلد البيانات إذا لم يكن موجوداً
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)

    # إنشاء قاعدة المعرفة
    kb = DiseaseKnowledgeBase()

    # حفظ قاعدة المعرفة
    kb.save_knowledge_base(os.path.join(data_dir, 'disease_knowledge.yaml'))

    # اختبار البحث عن الأمراض بناءً على الأعراض
    symptoms = ['بقع بنية على الأوراق', 'تعفن الثمار']
    results = kb.search_diseases_by_symptoms(symptoms)

    print("\nنتائج البحث عن الأمراض:")
    for result in results:
        print(f"المرض: {result['disease']}")
        print(f"المحصول: {result['crop']}")
        print(f"درجة التطابق: {result['match_score']:.2f}")
        print(f"الأعراض المتطابقة: {', '.join(result['matching_symptoms'])}")
        print("---")
