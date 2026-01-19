"""
نظام تحديث قواعد البيانات للأمراض والإصابات
Database Update System for Plant Diseases
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..models.disease import Disease
from .data_sources import COMMON_PLANT_DISEASES, MAJOR_CROPS, DataSourceManager

logger = logging.getLogger(__name__)


class DatabaseUpdater:
    """مدير تحديث قواعد البيانات"""

    def __init__(self, db: Session):
        self.db = db
        self.data_source_manager = DataSourceManager()
        self.update_log = []

    async def update_disease_database(
        self,
        force_update: bool = False,
        update_images: bool = True
    ) -> Dict:
        """تحديث قاعدة بيانات الأمراض"""
        logger.info("Starting database update...")

        stats = {
            "started_at": datetime.utcnow().isoformat(),
            "diseases_checked": 0,
            "diseases_updated": 0,
            "diseases_added": 0,
            "images_updated": 0,
            "errors": []
        }

        try:
            async with self.data_source_manager as dsm:
                # الحصول على المصادر الموثوقة
                sources = dsm.get_high_reliability_sources(min_reliability=0.9)

                # تحديث كل مرض
                for disease_name in COMMON_PLANT_DISEASES:
                    try:
                        stats["diseases_checked"] += 1

                        # البحث عن المرض في قاعدة البيانات
                        disease = self.db.query(Disease).filter(
                            or_(
                                Disease.name_en == disease_name,
                                Disease.name_ar == disease_name
                            )
                        ).first()

                        if disease:
                            # تحديث المرض الموجود
                            if force_update or self._needs_update(disease):
                                updated = await self._update_disease_info(
                                    disease, sources, dsm
                                )
                                if updated:
                                    stats["diseases_updated"] += 1
                        else:
                            # إضافة مرض جديد
                            new_disease = await self._create_disease_entry(
                                disease_name, sources, dsm
                            )
                            if new_disease:
                                stats["diseases_added"] += 1

                        # تحديث الصور إذا لزم الأمر
                        if update_images and disease:
                            images_count = await self._update_disease_images(
                                disease, dsm
                            )
                            stats["images_updated"] += images_count

                    except Exception as e:
                        error_msg = f"Error updating {disease_name}: {str(e)}"
                        logger.error(error_msg)
                        stats["errors"].append(error_msg)

                self.db.commit()

        except Exception as e:
            error_msg = f"Database update failed: {str(e)}"
            logger.error(error_msg)
            stats["errors"].append(error_msg)
            self.db.rollback()

        stats["completed_at"] = datetime.utcnow().isoformat()
        stats["duration_seconds"] = (
            datetime.fromisoformat(stats["completed_at"]) -
            datetime.fromisoformat(stats["started_at"])
        ).total_seconds()

        logger.info(f"Database update completed: {stats}")
        return stats

    def _needs_update(self, disease: Disease, days: int = 30) -> bool:
        """التحقق من حاجة المرض للتحديث"""
        if not disease.updated_at:
            return True

        last_update = disease.updated_at
        if isinstance(last_update, str):
            last_update = datetime.fromisoformat(last_update)

        return (datetime.utcnow() - last_update) > timedelta(days=days)

    async def _update_disease_info(
        self,
        disease: Disease,
        sources: List,
        dsm: DataSourceManager
    ) -> bool:
        """تحديث معلومات المرض"""
        try:
            # جلب معلومات من المصادر
            for source in sources[:3]:  # أول 3 مصادر
                info = await dsm.fetch_disease_info(disease.name_en, source)
                if info:
                    # تحديث المعلومات
                    disease.updated_at = datetime.utcnow()
                    disease.data_sources = disease.data_sources or []

                    # إضافة المصدر إذا لم يكن موجوداً
                    if source.name not in disease.data_sources:
                        disease.data_sources.append(source.name)

                    logger.info(f"Updated {disease.name_en} from {source.name}")
                    return True

            return False

        except Exception as e:
            logger.error(f"Error updating disease info: {e}")
            return False

    async def _create_disease_entry(
        self,
        disease_name: str,
        sources: List,
        dsm: DataSourceManager
    ) -> Optional[Disease]:
        """إنشاء إدخال مرض جديد"""
        try:
            # تحديد اللغة
            is_arabic = any(ord(c) > 127 for c in disease_name)

            # جلب معلومات من المصادر
            info = None
            for source in sources[:3]:
                info = await dsm.fetch_disease_info(disease_name, source)
                if info:
                    break

            if not info:
                logger.warning(f"No info found for {disease_name}")
                return None

            # إنشاء المرض
            new_disease = Disease(
                name_en=disease_name if not is_arabic else "",
                name_ar=disease_name if is_arabic else "",
                description_en=f"Information about {disease_name}",
                description_ar=f"معلومات عن {disease_name}" if is_arabic else "",
                symptoms_en=[],
                symptoms_ar=[],
                treatment_en=[],
                treatment_ar=[],
                prevention_en=[],
                prevention_ar=[],
                severity="medium",
                affected_crops=[],
                data_sources=[info["source"]],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            self.db.add(new_disease)
            logger.info(f"Created new disease entry: {disease_name}")
            return new_disease

        except Exception as e:
            logger.error(f"Error creating disease entry: {e}")
            return None

    async def _update_disease_images(
        self,
        disease: Disease,
        dsm: DataSourceManager
    ) -> int:
        """تحديث صور المرض"""
        try:
            # الحصول على مصادر الصور
            image_sources = dsm.get_image_sources()

            # هنا يمكن إضافة منطق تحميل الصور
            # سيتم ربطه مع Image Crawler

            logger.info(f"Image sources available for {disease.name_en}")
            return 0

        except Exception as e:
            logger.error(f"Error updating images: {e}")
            return 0

    async def update_nutrient_deficiencies(self) -> Dict:
        """تحديث معلومات نقص العناصر"""
        logger.info("Updating nutrient deficiencies...")

        stats = {
            "started_at": datetime.utcnow().isoformat(),
            "deficiencies_updated": 0,
            "errors": []
        }

        nutrient_deficiencies = [
            {
                "name_en": "Nitrogen Deficiency",
                "name_ar": "نقص النيتروجين",
                "symptoms_en": [
                    "Yellowing of older leaves",
                    "Stunted growth",
                    "Pale green color"
                ],
                "symptoms_ar": [
                    "اصفرار الأوراق القديمة",
                    "تقزم النمو",
                    "لون أخضر شاحب"
                ],
                "treatment_en": [
                    "Apply nitrogen fertilizer",
                    "Use compost or manure",
                    "Plant nitrogen-fixing cover crops"
                ],
                "treatment_ar": [
                    "إضافة سماد نيتروجيني",
                    "استخدام السماد العضوي",
                    "زراعة محاصيل مثبتة للنيتروجين"
                ]
            },
            {
                "name_en": "Phosphorus Deficiency",
                "name_ar": "نقص الفوسفور",
                "symptoms_en": [
                    "Purple or reddish leaves",
                    "Slow growth",
                    "Dark green leaves"
                ],
                "symptoms_ar": [
                    "أوراق أرجوانية أو محمرة",
                    "نمو بطيء",
                    "أوراق خضراء داكنة"
                ],
                "treatment_en": [
                    "Apply phosphorus fertilizer",
                    "Use bone meal",
                    "Adjust soil pH"
                ],
                "treatment_ar": [
                    "إضافة سماد فوسفوري",
                    "استخدام مسحوق العظام",
                    "تعديل حموضة التربة"
                ]
            },
            {
                "name_en": "Potassium Deficiency",
                "name_ar": "نقص البوتاسيوم",
                "symptoms_en": [
                    "Brown leaf edges",
                    "Weak stems",
                    "Poor fruit quality"
                ],
                "symptoms_ar": [
                    "حواف الأوراق بنية",
                    "سيقان ضعيفة",
                    "جودة ثمار ضعيفة"
                ],
                "treatment_en": [
                    "Apply potassium fertilizer",
                    "Use wood ash",
                    "Apply compost"
                ],
                "treatment_ar": [
                    "إضافة سماد بوتاسي",
                    "استخدام رماد الخشب",
                    "إضافة السماد العضوي"
                ]
            },
            # يمكن إضافة المزيد من العناصر
        ]

        try:
            for deficiency in nutrient_deficiencies:
                # البحث عن النقص في قاعدة البيانات
                disease = self.db.query(Disease).filter(
                    or_(
                        Disease.name_en == deficiency["name_en"],
                        Disease.name_ar == deficiency["name_ar"]
                    )
                ).first()

                if disease:
                    # تحديث المعلومات
                    disease.symptoms_en = deficiency["symptoms_en"]
                    disease.symptoms_ar = deficiency["symptoms_ar"]
                    disease.treatment_en = deficiency["treatment_en"]
                    disease.treatment_ar = deficiency["treatment_ar"]
                    disease.updated_at = datetime.utcnow()
                else:
                    # إنشاء إدخال جديد
                    new_disease = Disease(
                        name_en=deficiency["name_en"],
                        name_ar=deficiency["name_ar"],
                        description_en=f"Nutrient deficiency: {deficiency['name_en']}",
                        description_ar=f"نقص عنصر: {deficiency['name_ar']}",
                        symptoms_en=deficiency["symptoms_en"],
                        symptoms_ar=deficiency["symptoms_ar"],
                        treatment_en=deficiency["treatment_en"],
                        treatment_ar=deficiency["treatment_ar"],
                        prevention_en=[],
                        prevention_ar=[],
                        severity="medium",
                        affected_crops=MAJOR_CROPS,
                        data_sources=["Internal Database"],
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    self.db.add(new_disease)

                stats["deficiencies_updated"] += 1

            self.db.commit()

        except Exception as e:
            error_msg = f"Error updating nutrient deficiencies: {str(e)}"
            logger.error(error_msg)
            stats["errors"].append(error_msg)
            self.db.rollback()

        stats["completed_at"] = datetime.utcnow().isoformat()
        logger.info(f"Nutrient deficiencies update completed: {stats}")
        return stats

    def get_update_statistics(self) -> Dict:
        """الحصول على إحصائيات التحديث"""
        try:
            total_diseases = self.db.query(Disease).count()

            # الأمراض المحدثة مؤخراً (آخر 30 يوم)
            recent_cutoff = datetime.utcnow() - timedelta(days=30)
            recently_updated = self.db.query(Disease).filter(
                Disease.updated_at >= recent_cutoff
            ).count()

            # الأمراض التي تحتاج تحديث
            needs_update = self.db.query(Disease).filter(
                or_(
                    Disease.updated_at < recent_cutoff,
                    Disease.updated_at.is_(None)
                )
            ).count()

            return {
                "total_diseases": total_diseases,
                "recently_updated": recently_updated,
                "needs_update": needs_update,
                "last_check": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}


# دالة مساعدة
def get_database_updater(db: Session) -> DatabaseUpdater:
    """الحصول على مدير التحديث"""
    return DatabaseUpdater(db)
