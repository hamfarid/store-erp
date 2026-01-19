# File: /home/ubuntu/clean_project/src/data_seeder.py
"""
مسار الملف: /home/ubuntu/clean_project/src/data_seeder.py

أداة إدخال البيانات الأولية لقاعدة البيانات
تقوم بإنشاء بيانات تجريبية للمحاصيل والأمراض والمستخدمين
"""

from datetime import datetime, timedelta
import logging
import sys
import os

# إضافة مسار src إلى Python path
sys.path.append(os.path.dirname(__file__))

from database_models import (
    get_session, create_database, 
    User, Crop, Disease, Diagnosis, ActivityLog
)
from auth_service import hash_password
import random

logger = logging.getLogger(__name__)

class DataSeeder:
    """فئة إدخال البيانات الأولية"""
    
    def __init__(self):
        self.engine = create_database()
        self.session = get_session(self.engine)
    
    def seed_all(self):
        """إدخال جميع البيانات الأولية"""
        try:
            logger.info("بدء إدخال البيانات الأولية...")
            
            # إدخال المستخدمين
            users = self.seed_users()
            logger.info(f"تم إدخال {len(users)} مستخدم")
            
            # إدخال المحاصيل
            crops = self.seed_crops()
            logger.info(f"تم إدخال {len(crops)} محصول")
            
            # إدخال الأمراض
            diseases = self.seed_diseases(crops)
            logger.info(f"تم إدخال {len(diseases)} مرض")
            
            # إدخال تشخيصات تجريبية
            diagnoses = self.seed_diagnoses(users, crops, diseases)
            logger.info(f"تم إدخال {len(diagnoses)} تشخيص")
            
            # إدخال سجل النشاط
            activities = self.seed_activity_logs(users)
            logger.info(f"تم إدخال {len(activities)} نشاط")
            
            self.session.commit()
            logger.info("تم إدخال جميع البيانات الأولية بنجاح")
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"خطأ في إدخال البيانات: {e}")
            raise
        finally:
            self.session.close()
    
    def seed_users(self):
        """إدخال المستخدمين الأوليين"""
        users_data = [
            {
                "username": "admin",
                "email": "admin@gaara.ai",
                "password": "admin123",
                "full_name": "مدير النظام",
                "role": "admin",
                "is_active": True,
                "permissions": {
                    "admin": True,
                    "diagnosis": True,
                    "ai_management": True,
                    "user_management": True,
                    "system_settings": True
                }
            },
            {
                "username": "farmer1",
                "email": "farmer1@example.com",
                "password": "farmer123",
                "full_name": "أحمد المزارع",
                "role": "farmer",
                "is_active": True,
                "permissions": {
                    "diagnosis": True,
                    "view_reports": True
                }
            },
            {
                "username": "expert1",
                "email": "expert1@gaara.ai",
                "password": "expert123",
                "full_name": "د. سارة الخبيرة",
                "role": "expert",
                "is_active": True,
                "permissions": {
                    "diagnosis": True,
                    "ai_management": True,
                    "view_reports": True,
                    "manage_diseases": True
                }
            },
            {
                "username": "researcher1",
                "email": "researcher1@gaara.ai",
                "password": "research123",
                "full_name": "د. محمد الباحث",
                "role": "researcher",
                "is_active": True,
                "permissions": {
                    "diagnosis": True,
                    "ai_management": True,
                    "view_reports": True,
                    "research_access": True
                }
            }
        ]
        
        users = []
        for user_data in users_data:
            # التحقق من عدم وجود المستخدم
            existing_user = self.session.query(User).filter(
                User.username == user_data["username"]
            ).first()
            
            if not existing_user:
                user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    password_hash=hash_password(user_data["password"]),
                    full_name=user_data["full_name"],
                    is_active=user_data["is_active"],
                    is_admin=(user_data["role"] == "admin"),
                    created_at=datetime.utcnow()
                )
                self.session.add(user)
                users.append(user)
        
        self.session.flush()  # للحصول على IDs
        return users
    
    def seed_crops(self):
        """إدخال المحاصيل الأولية"""
        crops_data = [
            {
                "name": "الطماطم",
                "scientific_name": "Solanum lycopersicum",
                "category": "خضروات",
                "description": "نبات من الفصيلة الباذنجانية، يزرع لثماره الحمراء الغنية بالفيتامينات",
                "image_path": "/static/images/crops/tomato.jpg"
            },
            {
                "name": "البطاطس",
                "scientific_name": "Solanum tuberosum",
                "category": "خضروات",
                "description": "نبات درني من الفصيلة الباذنجانية، مصدر مهم للكربوهيدرات",
                "image_path": "/static/images/crops/potato.jpg"
            },
            {
                "name": "الذرة",
                "scientific_name": "Zea mays",
                "category": "حبوب",
                "description": "نبات عشبي حولي من الفصيلة النجيلية، محصول غذائي مهم",
                "image_path": "/static/images/crops/corn.jpg"
            },
            {
                "name": "القمح",
                "scientific_name": "Triticum aestivum",
                "category": "حبوب",
                "description": "نبات حولي من الفصيلة النجيلية، أساس صناعة الخبز",
                "image_path": "/static/images/crops/wheat.jpg"
            },
            {
                "name": "الأرز",
                "scientific_name": "Oryza sativa",
                "category": "حبوب",
                "description": "نبات عشبي حولي من الفصيلة النجيلية، غذاء أساسي لمليارات البشر",
                "image_path": "/static/images/crops/rice.jpg"
            },
            {
                "name": "القطن",
                "scientific_name": "Gossypium",
                "category": "محاصيل صناعية",
                "description": "نبات ينتج ألياف طبيعية تستخدم في صناعة النسيج",
                "image_path": "/static/images/crops/cotton.jpg"
            },
            {
                "name": "الخيار",
                "scientific_name": "Cucumis sativus",
                "category": "خضروات",
                "description": "نبات متسلق من الفصيلة القرعية، يزرع لثماره الخضراء",
                "image_path": "/static/images/crops/cucumber.jpg"
            },
            {
                "name": "الفلفل",
                "scientific_name": "Capsicum annuum",
                "category": "خضروات",
                "description": "نبات من الفصيلة الباذنجانية، يزرع لثماره الملونة",
                "image_path": "/static/images/crops/pepper.jpg"
            }
        ]
        
        crops = []
        for crop_data in crops_data:
            # التحقق من عدم وجود المحصول
            existing_crop = self.session.query(Crop).filter(
                Crop.name == crop_data["name"]
            ).first()
            
            if not existing_crop:
                crop = Crop(
                    name=crop_data["name"],
                    scientific_name=crop_data["scientific_name"],
                    category=crop_data["category"],
                    description=crop_data["description"],
                    image_path=crop_data["image_path"],
                    is_active=True,
                    created_at=datetime.utcnow()
                )
                self.session.add(crop)
                crops.append(crop)
        
        self.session.flush()
        return crops
    
    def seed_diseases(self, crops):
        """إدخال الأمراض الأولية"""
        diseases_data = [
            # أمراض الطماطم
            {
                "crop_name": "الطماطم",
                "name": "اللفحة المبكرة",
                "severity": "متوسط",
                "symptoms": "بقع بنية دائرية على الأوراق، ذبول الأوراق السفلية، بقع على الثمار",
                "treatment": "استخدام مبيدات فطرية نحاسية، تحسين التهوية، إزالة الأوراق المصابة",
                "prevention": "تجنب الري المفرط، زراعة أصناف مقاومة، تطبيق دورة زراعية"
            },
            {
                "crop_name": "الطماطم",
                "name": "اللفحة المتأخرة",
                "severity": "عالي",
                "symptoms": "بقع مائية على الأوراق، عفن أبيض على السطح السفلي، تعفن الثمار",
                "treatment": "مبيدات فطرية جهازية، إزالة النباتات المصابة فوراً",
                "prevention": "تحسين الصرف، زراعة أصناف مقاومة، مراقبة الرطوبة"
            },
            # أمراض البطاطس
            {
                "crop_name": "البطاطس",
                "name": "العفن البني",
                "severity": "عالي",
                "symptoms": "ذبول النبات، تلون بني في الأوعية الناقلة، تعفن الدرنات",
                "treatment": "لا يوجد علاج كيميائي فعال، إزالة النباتات المصابة",
                "prevention": "استخدام تقاوي معتمدة، تطبيق دورة زراعية، تحسين الصرف"
            },
            {
                "crop_name": "البطاطس",
                "name": "الجرب العادي",
                "severity": "متوسط",
                "symptoms": "بقع خشنة على سطح الدرنات، تشققات في القشرة",
                "treatment": "معاملة التقاوي بمبيدات فطرية، تحسين حموضة التربة",
                "prevention": "تجنب الري المفرط، استخدام تقاوي سليمة"
            },
            # أمراض الذرة
            {
                "crop_name": "الذرة",
                "name": "صدأ الذرة الشائع",
                "severity": "متوسط",
                "symptoms": "بقع صدئية بنية على الأوراق، ضعف النمو",
                "treatment": "مبيدات فطرية، تحسين التغذية بالبوتاسيوم",
                "prevention": "زراعة أصناف مقاومة، تطبيق دورة زراعية"
            },
            {
                "crop_name": "الذرة",
                "name": "تفحم الذرة",
                "severity": "عالي",
                "symptoms": "انتفاخات رمادية على الكيزان والأوراق، إنتاج جراثيم سوداء",
                "treatment": "إزالة الأجزاء المصابة، مبيدات فطرية وقائية",
                "prevention": "تجنب الجروح، زراعة أصناف مقاومة"
            },
            # أمراض القمح
            {
                "crop_name": "القمح",
                "name": "صدأ القمح الأصفر",
                "severity": "عالي",
                "symptoms": "خطوط صفراء على الأوراق، ضعف تكوين الحبوب",
                "treatment": "مبيدات فطرية متخصصة، حصاد مبكر إذا لزم",
                "prevention": "زراعة أصناف مقاومة، مراقبة دورية"
            },
            {
                "crop_name": "القمح",
                "name": "التفحم السائب",
                "severity": "متوسط",
                "symptoms": "تحول السنابل إلى كتلة سوداء من الجراثيم",
                "treatment": "معاملة البذور بمبيدات فطرية",
                "prevention": "استخدام بذور معتمدة، معاملة البذور"
            },
            # أمراض الأرز
            {
                "crop_name": "الأرز",
                "name": "لفحة الأرز",
                "severity": "عالي",
                "symptoms": "بقع رمادية على الأوراق، موت البراعم، تعفن الجذور",
                "treatment": "مبيدات فطرية، تحسين الصرف، تقليل الكثافة النباتية",
                "prevention": "إدارة المياه، زراعة أصناف مقاومة"
            },
            {
                "crop_name": "الأرز",
                "name": "التبقع البني",
                "severity": "متوسط",
                "symptoms": "بقع بنية دائرية على الأوراق، اصفرار الأوراق",
                "treatment": "مبيدات فطرية، تحسين التهوية",
                "prevention": "تجنب الإفراط في التسميد النيتروجيني"
            }
        ]
        
        # إنشاء قاموس للمحاصيل
        crops_dict = {crop.name: crop for crop in crops}
        
        diseases = []
        for disease_data in diseases_data:
            crop = crops_dict.get(disease_data["crop_name"])
            if crop:
                # التحقق من عدم وجود المرض
                existing_disease = self.session.query(Disease).filter(
                    Disease.name == disease_data["name"],
                    Disease.crop_id == crop.id
                ).first()
                
                if not existing_disease:
                    disease = Disease(
                        name=disease_data["name"],
                        crop_id=crop.id,
                        severity=disease_data["severity"],
                        symptoms=disease_data["symptoms"],
                        treatment=disease_data["treatment"],
                        prevention=disease_data["prevention"],
                        is_active=True,
                        created_at=datetime.utcnow()
                    )
                    self.session.add(disease)
                    diseases.append(disease)
        
        self.session.flush()
        return diseases
    
    def seed_diagnoses(self, users, crops, diseases):
        """إدخال تشخيصات تجريبية"""
        diagnoses = []
        
        # إنشاء تشخيصات عشوائية للشهرين الماضيين
        for i in range(50):
            user = random.choice(users)
            crop = random.choice(crops)
            
            # الحصول على الأمراض المرتبطة بالمحصول
            crop_diseases = [d for d in diseases if d.crop_id == crop.id]
            if not crop_diseases:
                continue
            
            disease = random.choice(crop_diseases)
            
            # تاريخ عشوائي في الشهرين الماضيين
            days_ago = random.randint(1, 60)
            created_at = datetime.utcnow() - timedelta(days=days_ago)
            
            diagnosis = Diagnosis(
                user_id=user.id,
                crop_id=crop.id,
                disease_id=disease.id,
                image_path=f"/uploads/images/sample_{i+1}.jpg",
                confidence=round(random.uniform(0.75, 0.98), 2),
                status="completed",
                results={
                    "disease_name": disease.name,
                    "confidence": round(random.uniform(0.75, 0.98), 2),
                    "severity": disease.severity,
                    "processing_time": round(random.uniform(0.5, 3.0), 2),
                    "model_version": "v2.1"
                },
                created_at=created_at,
                processed_at=created_at + timedelta(seconds=random.randint(1, 30))
            )
            
            self.session.add(diagnosis)
            diagnoses.append(diagnosis)
        
        self.session.flush()
        return diagnoses
    
    def seed_activity_logs(self, users):
        """إدخال سجل النشاط التجريبي"""
        activities = []
        
        activity_types = [
            "user_login",
            "diagnosis_created",
            "diagnosis_completed",
            "user_registered",
            "settings_updated",
            "crop_added",
            "disease_added",
            "system_backup",
            "user_logout"
        ]
        
        # إنشاء أنشطة عشوائية للأسبوع الماضي
        for i in range(100):
            user = random.choice(users)
            activity_type = random.choice(activity_types)
            
            # تاريخ عشوائي في الأسبوع الماضي
            hours_ago = random.randint(1, 168)  # 7 أيام
            created_at = datetime.utcnow() - timedelta(hours=hours_ago)
            
            activity = ActivityLog(
                user_id=user.id,
                type=activity_type,
                level="info",
                message=f"المستخدم {user.full_name} قام بـ {activity_type}",
                details={
                    "ip_address": f"192.168.1.{random.randint(1, 254)}",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "session_id": f"sess_{random.randint(1000, 9999)}"
                },
                created_at=created_at
            )
            
            self.session.add(activity)
            activities.append(activity)
        
        self.session.flush()
        return activities

def seed_database():
    """دالة رئيسية لإدخال البيانات"""
    seeder = DataSeeder()
    seeder.seed_all()

if __name__ == "__main__":
    # إعداد التسجيل
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    seed_database()
    print("تم إدخال البيانات الأولية بنجاح!")

