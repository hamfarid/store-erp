# File: /home/ubuntu/ai_web_organized/src/modules/disease_diagnosis/db_service.py
"""
from flask import g
خدمة قاعدة البيانات لتشخيص الأمراض النباتية
توفر هذه الوحدة خدمات للتعامل مع قاعدة بيانات المحاصيل والأمراض النباتية وأعراضها وطرق علاجها
"""

import os
import logging
from datetime import datetime

import yaml
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError

from .db_models import (
    Base, Crop, Disease, DiseaseImage, Symptom, Treatment,
    Prevention, Condition, Diagnosis
)

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# إعداد اتصال قاعدة البيانات
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///disease_diagnosis.db')

engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

# إنشاء الجداول إذا لم تكن موجودة


def init_db():
    """تهيئة قاعدة البيانات وإنشاء الجداول"""
    try:
        Base.metadata.create_all(engine)
        logger.info("تم إنشاء جداول قاعدة البيانات بنجاح")

        # التحقق من وجود بيانات أولية وإضافتها إذا لم تكن موجودة
        session = Session()
        try:
            if session.query(Crop).count() == 0:
                init_default_data(session)
                logger.info("تم إضافة البيانات الافتراضية بنجاح")
        except Exception as e:
            logger.error("خطأ أثناء إضافة البيانات الافتراضية: %s", str(e))
            session.rollback()
        finally:
            session.close()

    except Exception as e:
        logger.error("خطأ أثناء إنشاء قاعدة البيانات: %s", str(e))

# إضافة بيانات افتراضية


def init_default_data(session):
    """إضافة بيانات افتراضية إلى قاعدة البيانات"""

    # تحميل البيانات الافتراضية من ملف YAML إذا كان موجوداً
    default_path = os.path.join(os.path.dirname(__file__), 'data', 'disease_knowledge.yaml')
    if os.path.exists(default_path):
        try:
            with open(default_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            # إضافة المحاصيل والأمراض من الملف
            import_from_knowledge_base(data, session)
            return
        except Exception as e:
            logger.error("خطأ في تحميل البيانات الافتراضية من الملف: %s", str(e))

    # إضافة بيانات افتراضية إذا لم يتم تحميلها من ملف

    # إضافة المحاصيل
    tomato = Crop(
        name="طماطم",
        name_en="Tomato",
        scientific_name="Solanum lycopersicum",
        description="محصول من الخضروات الشائعة ينتمي إلى العائلة الباذنجانية"
    )

    cucumber = Crop(
        name="خيار",
        name_en="Cucumber",
        scientific_name="Cucumis sativus",
        description="محصول من الخضروات ينتمي إلى العائلة القرعية"
    )

    wheat = Crop(
        name="قمح",
        name_en="Wheat",
        scientific_name="Triticum aestivum",
        description="محصول حبوب أساسي ينتمي إلى العائلة النجيلية"
    )

    session.add_all([tomato, cucumber, wheat])
    session.flush()

    # إضافة الأعراض
    symptoms = {
        "brown_spots": Symptom(description="بقع بنية داكنة على الأوراق"),
        "water_spots": Symptom(description="بقع خضراء مائية على الثمار"),
        "fruit_rot": Symptom(description="تعفن الثمار"),
        "white_growth": Symptom(description="ظهور نمو أبيض على السطح السفلي للأوراق في الظروف الرطبة"),
        "yellow_spots": Symptom(description="بقع صفراء على الجانب العلوي للأوراق"),
        "powdery_growth": Symptom(description="نمو أبيض دقيقي على السطح السفلي للأوراق"),
        "leaf_death": Symptom(description="جفاف وموت الأوراق المصابة"),
        "angular_spots": Symptom(description="بقع صفراء زاوية على الأوراق"),
        "gray_growth": Symptom(description="نمو رمادي-بنفسجي على السطح السفلي للأوراق"),
        "circular_spots": Symptom(description="بقع دائرية غائرة على الثمار"),
        "stem_lesions": Symptom(description="تقرحات على السيقان"),
        "red_pustules": Symptom(description="بثرات بنية محمرة على السيقان والأوراق"),
        "tissue_damage": Symptom(description="تمزق الأنسجة النباتية"),
        "weak_plant": Symptom(description="ضعف النبات وقلة المحصول"),
        "black_spores": Symptom(description="استبدال حبوب القمح بكتل سوداء من الجراثيم"),
        "bad_smell": Symptom(description="رائحة كريهة تشبه رائحة السمك الفاسد")
    }

    session.add_all(symptoms.values())
    session.flush()

    # إضافة الظروف
    conditions = {
        "high_humidity": Condition(description="رطوبة عالية"),
        "moderate_temp": Condition(description="درجات حرارة معتدلة (15-25 درجة مئوية)"),
        "dry_warm": Condition(description="طقس جاف ودافئ"),
        "warm_temp": Condition(description="درجات حرارة معتدلة إلى مرتفعة (20-30 درجة مئوية)"),
        "dew": Condition(description="رطوبة عالية أو ندى"),
        "seed_contamination": Condition(description="تلوث البذور بالجراثيم"),
        "cold_wet": Condition(description="ظروف باردة ورطبة أثناء الإنبات")
    }

    session.add_all(conditions.values())
    session.flush()

    # إضافة العلاجات
    treatments = {
        "copper_fungicide": Treatment(description="استخدام مبيدات فطرية نحاسية"),
        "avoid_overhead": Treatment(description="تجنب الري العلوي"),
        "improve_ventilation": Treatment(description="تحسين تهوية النباتات"),
        "remove_infected": Treatment(description="إزالة وتدمير النباتات المصابة"),
        "sulfur_fungicide": Treatment(description="استخدام مبيدات فطرية مثل الكبريت"),
        "plant_oils": Treatment(description="استخدام زيوت نباتية"),
        "remove_leaves": Treatment(description="إزالة الأوراق المصابة بشدة"),
        "reduce_humidity": Treatment(description="تقليل الرطوبة حول النباتات"),
        "fungicides": Treatment(description="استخدام مبيدات فطرية"),
        "early_harvest": Treatment(description="حصاد مبكر إذا كانت الإصابة شديدة"),
        "no_treatment": Treatment(description="لا يوجد علاج بعد ظهور المرض")
    }

    session.add_all(treatments.values())
    session.flush()

    # إضافة طرق الوقاية
    preventions = {
        "resistant_varieties": Prevention(description="استخدام أصناف مقاومة"),
        "crop_rotation": Prevention(description="تناوب المحاصيل"),
        "avoid_wet_areas": Prevention(description="تجنب الزراعة في المناطق المنخفضة الرطبة"),
        "avoid_nitrogen": Prevention(description="تجنب الإفراط في التسميد النيتروجيني"),
        "certified_seeds": Prevention(description="استخدام بذور معتمدة خالية من المرض"),
        "remove_hosts": Prevention(description="التخلص من العوائل البديلة مثل نبات البربري"),
        "early_planting": Prevention(description="زراعة مبكرة"),
        "seed_treatment": Prevention(description="معالجة البذور بمبيدات فطرية")
    }

    session.add_all(preventions.values())
    session.flush()

    # إضافة الأمراض
    late_blight = Disease(
        name="اللفحة المتأخرة",
        name_en="Late Blight",
        scientific_name="Phytophthora infestans",
        description="مرض فطري خطير يصيب الطماطم والبطاطس ويمكن أن يدمر المحصول بالكامل في ظروف مناسبة",
        crop_id=tomato.id
    )

    late_blight.symptoms.extend([
        symptoms["brown_spots"], symptoms["water_spots"],
        symptoms["fruit_rot"], symptoms["white_growth"]
    ])

    late_blight.conditions.extend([
        conditions["high_humidity"], conditions["moderate_temp"]
    ])

    late_blight.treatments.extend([
        treatments["copper_fungicide"], treatments["avoid_overhead"],
        treatments["improve_ventilation"], treatments["remove_infected"]
    ])

    late_blight.preventions.extend([
        preventions["resistant_varieties"], preventions["crop_rotation"],
        preventions["avoid_wet_areas"]
    ])

    powdery_mildew = Disease(
        name="البياض الدقيقي",
        name_en="Powdery Mildew",
        scientific_name="Leveillula taurica",
        description="مرض فطري شائع يصيب العديد من النباتات ويظهر كطبقة بيضاء دقيقية على الأوراق",
        crop_id=tomato.id
    )

    powdery_mildew.symptoms.extend([
        symptoms["yellow_spots"], symptoms["powdery_growth"],
        symptoms["leaf_death"]
    ])

    powdery_mildew.conditions.extend([
        conditions["dry_warm"], conditions["warm_temp"]
    ])

    powdery_mildew.treatments.extend([
        treatments["sulfur_fungicide"], treatments["plant_oils"],
        treatments["remove_leaves"]
    ])

    powdery_mildew.preventions.extend([
        preventions["resistant_varieties"], preventions["improve_ventilation"],
        preventions["avoid_nitrogen"]
    ])

    downy_mildew = Disease(
        name="البياض الزغبي",
        name_en="Downy Mildew",
        scientific_name="Pseudoperonospora cubensis",
        description="مرض فطري يصيب النباتات من العائلة القرعية ويظهر كبقع صفراء على الأوراق",
        crop_id=cucumber.id
    )

    downy_mildew.symptoms.extend([
        symptoms["angular_spots"], symptoms["gray_growth"],
        symptoms["leaf_death"]
    ])

    downy_mildew.conditions.extend([
        conditions["high_humidity"], conditions["moderate_temp"]
    ])

    downy_mildew.treatments.extend([
        treatments["copper_fungicide"], treatments["improve_ventilation"],
        treatments["reduce_humidity"]
    ])

    downy_mildew.preventions.extend([
        preventions["resistant_varieties"], preventions["crop_rotation"],
        preventions["avoid_overhead"]
    ])

    session.add_all([late_blight, powdery_mildew, downy_mildew])
    session.commit()


def import_from_knowledge_base(data, session):
    """استيراد البيانات من قاعدة المعرفة"""
    try:
        # إضافة المحاصيل
        crops = {}
        for crop_data in data.get('crops', []):
            crop = Crop(
                name=crop_data['name'],
                name_en=crop_data.get('name_en', ''),
                scientific_name=crop_data.get('scientific_name', ''),
                description=crop_data.get('description', '')
            )
            session.add(crop)
            session.flush()
            crops[crop.name] = crop

        # قواميس لتخزين الكائنات المشتركة
        symptoms_dict = {}
        conditions_dict = {}
        treatments_dict = {}
        preventions_dict = {}

        # إضافة الأمراض لكل محصول
        for crop_data in data.get('crops', []):
            crop = crops.get(crop_data['name'])
            if not crop:
                continue

            for disease_data in crop_data.get('diseases', []):
                # إنشاء المرض
                disease = Disease(
                    name=disease_data['name'],
                    name_en=disease_data.get('name_en', ''),
                    scientific_name=disease_data.get('scientific_name', ''),
                    description=disease_data.get('description', ''),
                    crop_id=crop.id
                )
                session.add(disease)
                session.flush()

                # إضافة الأعراض
                for symptom_text in disease_data.get('symptoms', []):
                    if symptom_text not in symptoms_dict:
                        symptom = Symptom(description=symptom_text)
                        session.add(symptom)
                        session.flush()
                        symptoms_dict[symptom_text] = symptom
                    disease.symptoms.append(symptoms_dict[symptom_text])

                # إضافة الظروف
                for condition_text in disease_data.get('conditions', []):
                    if condition_text not in conditions_dict:
                        condition = Condition(description=condition_text)
                        session.add(condition)
                        session.flush()
                        conditions_dict[condition_text] = condition
                    disease.conditions.append(conditions_dict[condition_text])

                # إضافة العلاجات
                for treatment_text in disease_data.get('treatments', []):
                    if treatment_text not in treatments_dict:
                        treatment = Treatment(description=treatment_text)
                        session.add(treatment)
                        session.flush()
                        treatments_dict[treatment_text] = treatment
                    disease.treatments.append(treatments_dict[treatment_text])

                # إضافة طرق الوقاية
                for prevention_text in disease_data.get('prevention', []):
                    if prevention_text not in preventions_dict:
                        prevention = Prevention(description=prevention_text)
                        session.add(prevention)
                        session.flush()
                        preventions_dict[prevention_text] = prevention
                    disease.preventions.append(preventions_dict[prevention_text])

                # إضافة الصور
                for image_path in disease_data.get('images', []):
                    image = DiseaseImage(
                        disease_id=disease.id,
                        file_path=image_path,
                        caption=disease_data['name']
                    )
                    session.add(image)

        session.commit()
        logger.info("تم استيراد البيانات من قاعدة المعرفة بنجاح")
        return True
    except Exception as e:
        session.rollback()
        logger.error("خطأ أثناء استيراد البيانات من قاعدة المعرفة: %s", str(e))
        return False

# خدمات المحاصيل


def get_all_crops():
    """الحصول على جميع المحاصيل"""
    session = Session()
    try:
        crops = session.query(Crop).all()
        return [crop.to_dict() for crop in crops]
    except SQLAlchemyError as e:
        logger.error("خطأ أثناء استرجاع المحاصيل: %s", str(e))
        return []
    finally:
        session.close()


def get_crop_by_id(crop_id):
    """الحصول على محصول بواسطة المعرف"""
    session = Session()
    try:
        crop = session.query(Crop).filter(Crop.id == crop_id).first()
        return crop.to_dict() if crop else None
    except SQLAlchemyError as e:
        logger.error("خطأ أثناء استرجاع المحصول {crop_id}: %s", str(e))
        return None
    finally:
        session.close()


def get_crop_by_name(crop_name):
    """الحصول على محصول بواسطة الاسم"""
    session = Session()
    try:
        crop = session.query(Crop).filter(Crop.name == crop_name).first()
        return crop.to_dict() if crop else None
    except SQLAlchemyError as e:
        logger.error("خطأ أثناء استرجاع المحصول {crop_name}: %s", str(e))
        return None
    finally:
        session.close()


def create_crop(crop_data):
    """إنشاء محصول جديد"""
    session = Session()
    try:
        # التحقق من عدم وجود المحصول مسبقاً
        existing_crop = session.query(Crop).filter(Crop.name == crop_data['name']).first()
        if existing_crop:
            logger.warning("المحصول %s موجود بالفعل", crop_data['name'])
            return None

        crop = Crop(
            name=crop_data['name'],
            name_en=crop_data.get('nameEn', ''),
            scientific_name=crop_data.get('scientificName', ''),
            description=crop_data.get('description', ''),
            image_path=crop_data.get('imagePath', '')
        )

        session.add(crop)
        session.commit()

        return crop.to_dict()
    except SQLAlchemyError as e:
        session.rollback()
        logger.error("خطأ أثناء إنشاء محصول جديد: %s", str(e))
        return None
    finally:
        session.close()


def update_crop(crop_id, crop_data):
    """تحديث محصول موجود"""
    session = Session()
    try:
        crop = session.query(Crop).filter(Crop.id == crop_id).first()
        if not crop:
            return None

        # تحديث البيانات
        if 'name' in crop_data:
            crop.name = crop_data['name']
        if 'nameEn' in crop_data:
            crop.name_en = crop_data['nameEn']
        if 'scientificName' in crop_data:
            crop.scientific_name = crop_data['scientificName']
        if 'description' in crop_data:
            crop.description = crop_data['description']
        if 'imagePath' in crop_data:
            crop.image_path = crop_data['imagePath']

        crop.updated_at = datetime.now()

        session.commit()

        return crop.to_dict()
    except SQLAlchemyError as e:
        session.rollback()
        logger.error("خطأ أثناء تحديث المحصول {crop_id}: %s", str(e))
        return None
    finally:
        session.close()


def delete_crop(crop_id):
    """حذف محصول"""
    session = Session()
    try:
        crop = session.query(Crop).filter(Crop.id == crop_id).first()
        if not crop:
            return None

        # التحقق من عدم وجود أمراض مرتبطة بالمحصول
        diseases_count = session.query(Disease).filter(Disease.crop_id == crop_id).count()
        if diseases_count > 0:
            logger.warning("لا يمكن حذف المحصول {crop_id} لأنه مرتبط بـ %s مرض", diseases_count)
            return False

        crop_dict = crop.to_dict()
        session.delete(crop)
        session.commit()

        return crop_dict
    except SQLAlchemyError as e:
        session.rollback()
        logger.error("خطأ أثناء حذف المحصول {crop_id}: %s", str(e))
        return None
    finally:
        session.close()

# خدمات الأمراض


def get_all_diseases():
    """الحصول على جميع الأمراض"""
    session = Session()
    try:
        diseases = session.query(Disease).all()
        return [disease.to_dict() for disease in diseases]
    except SQLAlchemyError as e:
        logger.error("خطأ أثناء استرجاع الأمراض: %s", str(e))
        return []
    finally:
        session.close()


def get_diseases_by_crop(crop_id):
    """الحصول على الأمراض بواسطة معرف المحصول"""
    session = Session()
    try:
        diseases = session.query(Disease).filter(Disease.crop_id == crop_id).all()
        return [disease.to_dict() for disease in diseases]
    except SQLAlchemyError as e:
        logger.error("خطأ أثناء استرجاع أمراض المحصول {crop_id}: %s", str(e))
        return []
    finally:
        session.close()


def get_disease_by_id(disease_id):
    """الحصول على مرض بواسطة المعرف"""
    session = Session()
    try:
        disease = session.query(Disease).filter(Disease.id == disease_id).first()
        return disease.to_dict() if disease else None
    except SQLAlchemyError as e:
        logger.error("خطأ أثناء استرجاع المرض {disease_id}: %s", str(e))
        return None
    finally:
        session.close()


def get_disease_by_name(disease_name, crop_id=None):
    """الحصول على مرض بواسطة الاسم"""
    session = Session()
    try:
        query = session.query(Disease).filter(Disease.name == disease_name)
        if crop_id:
            query = query.filter(Disease.crop_id == crop_id)

        disease = query.first()
        return disease.to_dict() if disease else None
    except SQLAlchemyError as e:
        logger.error("خطأ أثناء استرجاع المرض {disease_name}: %s", str(e))
        return None
    finally:
        session.close()


def create_disease(disease_data):
    """إنشاء مرض جديد"""
    session = Session()
    try:
        # التحقق من وجود المحصول
        crop_id = disease_data.get('cropId')
        crop = session.query(Crop).filter(Crop.id == crop_id).first()
        if not crop:
            logger.warning("المحصول %s غير موجود", crop_id)
            return None

        # التحقق من عدم وجود المرض مسبقاً لنفس المحصول
        existing_disease = session.query(Disease).filter(
            Disease.name == disease_data['name'],
            Disease.crop_id == crop_id
        ).first()

        if existing_disease:
            logger.warning("المرض {disease_data['name']} موجود بالفعل للمحصول %s", crop_id)
            return None

        # إنشاء المرض
        disease = Disease(
            name=disease_data['name'],
            name_en=disease_data.get('nameEn', ''),
            scientific_name=disease_data.get('scientificName', ''),
            description=disease_data.get('description', ''),
            crop_id=crop_id
        )

        session.add(disease)
        session.flush()

        # إضافة الأعراض
        if 'symptoms' in disease_data:
            for symptom_text in disease_data['symptoms']:
                symptom = session.query(Symptom).filter(Symptom.description == symptom_text).first()
                if not symptom:
                    symptom = Symptom(description=symptom_text)
                    session.add(symptom)
                    session.flush()
                disease.symptoms.append(symptom)

        # إضافة الظروف
        if 'conditions' in disease_data:
            for condition_text in disease_data['conditions']:
                condition = session.query(Condition).filter(Condition.description == condition_text).first()
                if not condition:
                    condition = Condition(description=condition_text)
                    session.add(condition)
                    session.flush()
                disease.conditions.append(condition)

        # إضافة العلاجات
        if 'treatments' in disease_data:
            for treatment_text in disease_data['treatments']:
                treatment = session.query(Treatment).filter(Treatment.description == treatment_text).first()
                if not treatment:
                    treatment = Treatment(description=treatment_text)
                    session.add(treatment)
                    session.flush()
                disease.treatments.append(treatment)

        # إضافة طرق الوقاية
        if 'preventions' in disease_data:
            for prevention_text in disease_data['preventions']:
                prevention = session.query(Prevention).filter(Prevention.description == prevention_text).first()
                if not prevention:
                    prevention = Prevention(description=prevention_text)
                    session.add(prevention)
                    session.flush()
                disease.preventions.append(prevention)

        # إضافة الصور
        if 'images' in disease_data:
            for image_data in disease_data['images']:
                image = DiseaseImage(
                    disease_id=disease.id,
                    file_path=image_data.get('filePath', ''),
                    caption=image_data.get('caption', '')
                )
                session.add(image)

        session.commit()

        return disease.to_dict()
    except SQLAlchemyError as e:
        session.rollback()
        logger.error("خطأ أثناء إنشاء مرض جديد: %s", str(e))
        return None
    finally:
        session.close()


def update_disease(disease_id, disease_data):
    """تحديث مرض موجود"""
    session = Session()
    try:
        disease = session.query(Disease).filter(Disease.id == disease_id).first()
        if not disease:
            return None

        # تحديث البيانات الأساسية
        if 'name' in disease_data:
            disease.name = disease_data['name']
        if 'nameEn' in disease_data:
            disease.name_en = disease_data['nameEn']
        if 'scientificName' in disease_data:
            disease.scientific_name = disease_data['scientificName']
        if 'description' in disease_data:
            disease.description = disease_data['description']
        if 'cropId' in disease_data:
            # التحقق من وجود المحصول
            crop = session.query(Crop).filter(Crop.id == disease_data['cropId']).first()
            if crop:
                disease.crop_id = disease_data['cropId']

        disease.updated_at = datetime.now()

        # تحديث الأعراض
        if 'symptoms' in disease_data:
            # إزالة جميع الأعراض الحالية
            disease.symptoms = []

            # إضافة الأعراض الجديدة
            for symptom_text in disease_data['symptoms']:
                symptom = session.query(Symptom).filter(Symptom.description == symptom_text).first()
                if not symptom:
                    symptom = Symptom(description=symptom_text)
                    session.add(symptom)
                    session.flush()
                disease.symptoms.append(symptom)

        # تحديث الظروف
        if 'conditions' in disease_data:
            # إزالة جميع الظروف الحالية
            disease.conditions = []

            # إضافة الظروف الجديدة
            for condition_text in disease_data['conditions']:
                condition = session.query(Condition).filter(Condition.description == condition_text).first()
                if not condition:
                    condition = Condition(description=condition_text)
                    session.add(condition)
                    session.flush()
                disease.conditions.append(condition)

        # تحديث العلاجات
        if 'treatments' in disease_data:
            # إزالة جميع العلاجات الحالية
            disease.treatments = []

            # إضافة العلاجات الجديدة
            for treatment_text in disease_data['treatments']:
                treatment = session.query(Treatment).filter(Treatment.description == treatment_text).first()
                if not treatment:
                    treatment = Treatment(description=treatment_text)
                    session.add(treatment)
                    session.flush()
                disease.treatments.append(treatment)

        # تحديث طرق الوقاية
        if 'preventions' in disease_data:
            # إزالة جميع طرق الوقاية الحالية
            disease.preventions = []

            # إضافة طرق الوقاية الجديدة
            for prevention_text in disease_data['preventions']:
                prevention = session.query(Prevention).filter(Prevention.description == prevention_text).first()
                if not prevention:
                    prevention = Prevention(description=prevention_text)
                    session.add(prevention)
                    session.flush()
                disease.preventions.append(prevention)

        # تحديث الصور
        if 'images' in disease_data:
            # حذف جميع الصور الحالية
            session.query(DiseaseImage).filter(DiseaseImage.disease_id == disease_id).delete()

            # إضافة الصور الجديدة
            for image_data in disease_data['images']:
                image = DiseaseImage(
                    disease_id=disease.id,
                    file_path=image_data.get('filePath', ''),
                    caption=image_data.get('caption', '')
                )
                session.add(image)

        session.commit()

        return disease.to_dict()
    except SQLAlchemyError as e:
        session.rollback()
        logger.error("خطأ أثناء تحديث المرض {disease_id}: %s", str(e))
        return None
    finally:
        session.close()


def delete_disease(disease_id):
    """حذف مرض"""
    session = Session()
    try:
        disease = session.query(Disease).filter(Disease.id == disease_id).first()
        if not disease:
            return None

        # التحقق من عدم وجود تشخيصات مرتبطة بالمرض
        diagnoses_count = session.query(Diagnosis).filter(Diagnosis.disease_id == disease_id).count()
        if diagnoses_count > 0:
            logger.warning("لا يمكن حذف المرض {disease_id} لأنه مرتبط بـ %s تشخيص", diagnoses_count)
            return False

        disease_dict = disease.to_dict()

        # حذف الصور المرتبطة بالمرض
        session.query(DiseaseImage).filter(DiseaseImage.disease_id == disease_id).delete()

        # حذف المرض
        session.delete(disease)
        session.commit()

        return disease_dict
    except SQLAlchemyError as e:
        session.rollback()
        logger.error("خطأ أثناء حذف المرض {disease_id}: %s", str(e))
        return None
    finally:
        session.close()

# خدمات التشخيص


def create_diagnosis(diagnosis_data):
    """إنشاء تشخيص جديد"""
    session = Session()
    try:
        # التحقق من وجود المرض
        disease_id = diagnosis_data.get('diseaseId')
        disease = session.query(Disease).filter(Disease.id == disease_id).first()
        if not disease:
            logger.warning("المرض %s غير موجود", disease_id)
            return None

        diagnosis = Diagnosis(
            user_id=diagnosis_data.get('userId'),
            disease_id=disease_id,
            confidence=diagnosis_data.get('confidence', 0.0),
            symptoms_text=diagnosis_data.get('symptomsText', ''),
            image_path=diagnosis_data.get('imagePath', ''),
            notes=diagnosis_data.get('notes', '')
        )

        session.add(diagnosis)
        session.commit()

        return diagnosis.to_dict()
    except SQLAlchemyError as e:
        session.rollback()
        logger.error("خطأ أثناء إنشاء تشخيص جديد: %s", str(e))
        return None
    finally:
        session.close()


def get_diagnosis_by_id(diagnosis_id):
    """الحصول على تشخيص بواسطة المعرف"""
    session = Session()
    try:
        diagnosis = session.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()
        return diagnosis.to_dict() if diagnosis else None
    except SQLAlchemyError as e:
        logger.error("خطأ أثناء استرجاع التشخيص {diagnosis_id}: %s", str(e))
        return None
    finally:
        session.close()


def get_diagnoses_by_user(user_id):
    """الحصول على تشخيصات المستخدم"""
    session = Session()
    try:
        diagnoses = session.query(Diagnosis).filter(Diagnosis.user_id == user_id).order_by(desc(Diagnosis.created_at)).all()
        return [diagnosis.to_dict() for diagnosis in diagnoses]
    except SQLAlchemyError as e:
        logger.error("خطأ أثناء استرجاع تشخيصات المستخدم {user_id}: %s", str(e))
        return []
    finally:
        session.close()


def get_all_diagnoses():
    """الحصول على جميع التشخيصات"""
    session = Session()
    try:
        diagnoses = session.query(Diagnosis).order_by(desc(Diagnosis.created_at)).all()
        return [diagnosis.to_dict() for diagnosis in diagnoses]
    except SQLAlchemyError as e:
        logger.error("خطأ أثناء استرجاع جميع التشخيصات: %s", str(e))
        return []
    finally:
        session.close()


def update_diagnosis(diagnosis_id, diagnosis_data):
    """تحديث تشخيص موجود"""
    session = Session()
    try:
        diagnosis = session.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()
        if not diagnosis:
            return None

        # تحديث البيانات
        if 'diseaseId' in diagnosis_data:
            # التحقق من وجود المرض
            disease = session.query(Disease).filter(Disease.id == diagnosis_data['diseaseId']).first()
            if disease:
                diagnosis.disease_id = diagnosis_data['diseaseId']

        if 'confidence' in diagnosis_data:
            diagnosis.confidence = diagnosis_data['confidence']
        if 'symptomsText' in diagnosis_data:
            diagnosis.symptoms_text = diagnosis_data['symptomsText']
        if 'imagePath' in diagnosis_data:
            diagnosis.image_path = diagnosis_data['imagePath']
        if 'notes' in diagnosis_data:
            diagnosis.notes = diagnosis_data['notes']

        session.commit()

        return diagnosis.to_dict()
    except SQLAlchemyError as e:
        session.rollback()
        logger.error("خطأ أثناء تحديث التشخيص {diagnosis_id}: %s", str(e))
        return None
    finally:
        session.close()


def delete_diagnosis(diagnosis_id):
    """حذف تشخيص"""
    session = Session()
    try:
        diagnosis = session.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()
        if not diagnosis:
            return None

        diagnosis_dict = diagnosis.to_dict()
        session.delete(diagnosis)
        session.commit()

        return diagnosis_dict
    except SQLAlchemyError as e:
        session.rollback()
        logger.error("خطأ أثناء حذف التشخيص {diagnosis_id}: %s", str(e))
        return None
    finally:
        session.close()

# خدمات البحث


def search_diseases(query, crop_id=None):
    """البحث عن الأمراض"""
    session = Session()
    try:
        search_query = f"%{query}%"
        base_query = session.query(Disease).filter(
            (Disease.name.like(search_query))
            | (Disease.name_en.like(search_query))
            | (Disease.scientific_name.like(search_query))
            | (Disease.description.like(search_query))
        )

        if crop_id:
            base_query = base_query.filter(Disease.crop_id == crop_id)

        diseases = base_query.all()
        return [disease.to_dict() for disease in diseases]
    except SQLAlchemyError as e:
        logger.error("خطأ أثناء البحث عن الأمراض: %s", str(e))
        return []
    finally:
        session.close()


def search_by_symptoms(symptoms_list, crop_id=None):
    """البحث عن الأمراض بواسطة الأعراض"""
    session = Session()
    try:
        # البحث عن الأمراض التي تطابق الأعراض
        diseases_with_scores = []

        # الحصول على جميع الأمراض
        query = session.query(Disease)
        if crop_id:
            query = query.filter(Disease.crop_id == crop_id)

        diseases = query.all()

        for disease in diseases:
            # حساب درجة التطابق
            disease_symptoms = [symptom.description.lower() for symptom in disease.symptoms]
            match_count = 0

            for symptom in symptoms_list:
                symptom_lower = symptom.lower()
                for disease_symptom in disease_symptoms:
                    if symptom_lower in disease_symptom or disease_symptom in symptom_lower:
                        match_count += 1
                        break

            if match_count > 0:
                # حساب نسبة التطابق
                match_score = match_count / len(symptoms_list) if symptoms_list else 0
                diseases_with_scores.append({
                    "disease": disease.to_dict(),
                    "matchScore": match_score
                })

        # ترتيب النتائج حسب درجة التطابق
        diseases_with_scores.sort(key=lambda x: x["matchScore"], reverse=True)

        return diseases_with_scores
    except SQLAlchemyError as e:
        logger.error("خطأ أثناء البحث عن الأمراض بواسطة الأعراض: %s", str(e))
        return []
    finally:
        session.close()


# تهيئة قاعدة البيانات
# Note: init_db() should be called explicitly when needed, not on import
# This prevents connection errors when running outside Docker
