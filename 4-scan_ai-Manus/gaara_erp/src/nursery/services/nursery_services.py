"""
خدمات إدارة المشاتل
يحتوي هذا الملف على تنفيذ خدمات إدارة المشاتل والمزارع
"""

import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

from ..models.nursery_models import (
    Nursery, NurserySection, Plant, PlantActivity, NurseryEquipment,
    Farm, FarmPlot, Crop, CropActivity, FarmEquipment
)


class NurseryService:
    """خدمة إدارة المشاتل"""
    
    def __init__(self, db_manager):
        """
        تهيئة خدمة إدارة المشاتل
        
        المعاملات:
            db_manager: مدير قاعدة البيانات
        """
        self.db_manager = db_manager
        
    def create_nursery(self, nursery_data: Dict[str, Any]) -> Nursery:
        """
        إنشاء مشتل جديد
        
        المعاملات:
            nursery_data: بيانات المشتل
            
        العائد:
            كائن المشتل الجديد
        """
        # إنشاء معرف فريد للمشتل
        nursery_id = str(uuid.uuid4())
        nursery_data['nursery_id'] = nursery_id
        
        # إنشاء كائن المشتل
        nursery = Nursery.from_dict(nursery_data)
        
        # حفظ المشتل في قاعدة البيانات
        self._save_nursery(nursery)
        
        return nursery
    
    def update_nursery(self, nursery_id: str, nursery_data: Dict[str, Any]) -> Optional[Nursery]:
        """
        تحديث بيانات مشتل
        
        المعاملات:
            nursery_id: معرف المشتل
            nursery_data: بيانات المشتل المحدثة
            
        العائد:
            كائن المشتل المحدث أو None إذا لم يتم العثور على المشتل
        """
        # البحث عن المشتل
        nursery = self.get_nursery(nursery_id)
        if not nursery:
            return None
        
        # تحديث بيانات المشتل
        nursery_data['nursery_id'] = nursery_id
        updated_nursery = Nursery.from_dict(nursery_data)
        
        # الحفاظ على الأقسام والمعدات الحالية
        updated_nursery.sections = nursery.sections
        updated_nursery.equipment = nursery.equipment
        
        # حفظ المشتل المحدث في قاعدة البيانات
        self._save_nursery(updated_nursery)
        
        return updated_nursery
    
    def delete_nursery(self, nursery_id: str) -> bool:
        """
        حذف مشتل
        
        المعاملات:
            nursery_id: معرف المشتل
            
        العائد:
            True إذا تم الحذف بنجاح، False إذا لم يتم العثور على المشتل
        """
        # البحث عن المشتل
        nursery = self.get_nursery(nursery_id)
        if not nursery:
            return False
        
        # حذف المشتل من قاعدة البيانات
        query = "DELETE FROM nurseries WHERE nursery_id = %s"
        self.db_manager.execute_query(query, (nursery_id,))
        
        # حذف الأقسام والنباتات والمعدات المرتبطة بالمشتل
        self._delete_nursery_sections(nursery_id)
        self._delete_nursery_equipment(nursery_id)
        
        return True
    
    def get_nursery(self, nursery_id: str) -> Optional[Nursery]:
        """
        الحصول على مشتل بواسطة المعرف
        
        المعاملات:
            nursery_id: معرف المشتل
            
        العائد:
            كائن المشتل أو None إذا لم يتم العثور على المشتل
        """
        # استعلام قاعدة البيانات للحصول على المشتل
        query = "SELECT * FROM nurseries WHERE nursery_id = %s"
        result = self.db_manager.execute_query(query, (nursery_id,))
        
        if not result:
            return None
        
        # إنشاء كائن المشتل
        nursery_data = result[0]
        nursery = Nursery.from_dict(nursery_data)
        
        # إضافة الأقسام والمعدات
        nursery.sections = self._get_nursery_sections(nursery_id)
        nursery.equipment = self._get_nursery_equipment(nursery_id)
        
        return nursery
    
    def get_all_nurseries(self, company_id: Optional[str] = None, branch_id: Optional[str] = None) -> List[Nursery]:
        """
        الحصول على جميع المشاتل
        
        المعاملات:
            company_id: معرف الشركة (اختياري)
            branch_id: معرف الفرع (اختياري)
            
        العائد:
            قائمة بكائنات المشاتل
        """
        # بناء استعلام قاعدة البيانات
        query = "SELECT * FROM nurseries"
        params = []
        
        if company_id and branch_id:
            query += " WHERE company_id = %s AND branch_id = %s"
            params = [company_id, branch_id]
        elif company_id:
            query += " WHERE company_id = %s"
            params = [company_id]
        elif branch_id:
            query += " WHERE branch_id = %s"
            params = [branch_id]
        
        # تنفيذ الاستعلام
        results = self.db_manager.execute_query(query, tuple(params))
        
        # إنشاء قائمة المشاتل
        nurseries = []
        for nursery_data in results:
            nursery = Nursery.from_dict(nursery_data)
            nursery.sections = self._get_nursery_sections(nursery.nursery_id)
            nursery.equipment = self._get_nursery_equipment(nursery.nursery_id)
            nurseries.append(nursery)
        
        return nurseries
    
    def create_nursery_section(self, section_data: Dict[str, Any]) -> NurserySection:
        """
        إنشاء قسم مشتل جديد
        
        المعاملات:
            section_data: بيانات القسم
            
        العائد:
            كائن قسم المشتل الجديد
        """
        # إنشاء معرف فريد للقسم
        section_id = str(uuid.uuid4())
        section_data['section_id'] = section_id
        
        # إنشاء كائن قسم المشتل
        section = NurserySection.from_dict(section_data)
        
        # حفظ قسم المشتل في قاعدة البيانات
        self._save_nursery_section(section)
        
        return section
    
    def update_nursery_section(self, section_id: str, section_data: Dict[str, Any]) -> Optional[NurserySection]:
        """
        تحديث بيانات قسم مشتل
        
        المعاملات:
            section_id: معرف القسم
            section_data: بيانات القسم المحدثة
            
        العائد:
            كائن قسم المشتل المحدث أو None إذا لم يتم العثور على القسم
        """
        # البحث عن القسم
        section = self.get_nursery_section(section_id)
        if not section:
            return None
        
        # تحديث بيانات القسم
        section_data['section_id'] = section_id
        section_data['nursery_id'] = section.nursery_id
        updated_section = NurserySection.from_dict(section_data)
        
        # الحفاظ على النباتات الحالية
        updated_section.plants = section.plants
        
        # حفظ القسم المحدث في قاعدة البيانات
        self._save_nursery_section(updated_section)
        
        return updated_section
    
    def delete_nursery_section(self, section_id: str) -> bool:
        """
        حذف قسم مشتل
        
        المعاملات:
            section_id: معرف القسم
            
        العائد:
            True إذا تم الحذف بنجاح، False إذا لم يتم العثور على القسم
        """
        # البحث عن القسم
        section = self.get_nursery_section(section_id)
        if not section:
            return False
        
        # حذف القسم من قاعدة البيانات
        query = "DELETE FROM nursery_sections WHERE section_id = %s"
        self.db_manager.execute_query(query, (section_id,))
        
        # حذف النباتات المرتبطة بالقسم
        self._delete_section_plants(section_id)
        
        return True
    
    def get_nursery_section(self, section_id: str) -> Optional[NurserySection]:
        """
        الحصول على قسم مشتل بواسطة المعرف
        
        المعاملات:
            section_id: معرف القسم
            
        العائد:
            كائن قسم المشتل أو None إذا لم يتم العثور على القسم
        """
        # استعلام قاعدة البيانات للحصول على القسم
        query = "SELECT * FROM nursery_sections WHERE section_id = %s"
        result = self.db_manager.execute_query(query, (section_id,))
        
        if not result:
            return None
        
        # إنشاء كائن قسم المشتل
        section_data = result[0]
        section = NurserySection.from_dict(section_data)
        
        # إضافة النباتات
        section.plants = self._get_section_plants(section_id)
        
        return section
    
    def _get_nursery_sections(self, nursery_id: str) -> List[NurserySection]:
        """
        الحصول على أقسام المشتل
        
        المعاملات:
            nursery_id: معرف المشتل
            
        العائد:
            قائمة بكائنات أقسام المشتل
        """
        # استعلام قاعدة البيانات للحصول على أقسام المشتل
        query = "SELECT * FROM nursery_sections WHERE nursery_id = %s"
        results = self.db_manager.execute_query(query, (nursery_id,))
        
        # إنشاء قائمة أقسام المشتل
        sections = []
        for section_data in results:
            section = NurserySection.from_dict(section_data)
            section.plants = self._get_section_plants(section.section_id)
            sections.append(section)
        
        return sections
    
    def _save_nursery(self, nursery: Nursery) -> None:
        """
        حفظ المشتل في قاعدة البيانات
        
        المعاملات:
            nursery: كائن المشتل
        """
        # تحويل كائن المشتل إلى قاموس
        nursery_dict = nursery.to_dict()
        
        # حذف الأقسام والمعدات من القاموس
        nursery_dict.pop('sections', None)
        nursery_dict.pop('equipment', None)
        
        # بناء استعلام الإدراج أو التحديث
        columns = ', '.join(nursery_dict.keys())
        placeholders = ', '.join(['%s'] * len(nursery_dict))
        values = tuple(nursery_dict.values())
        
        # تنفيذ استعلام الإدراج أو التحديث
        query = f"""
        INSERT INTO nurseries ({columns})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE
        {', '.join([f'{col} = VALUES({col})' for col in nursery_dict.keys() if col != 'nursery_id'])}
        """
        
        self.db_manager.execute_query(query, values)
    
    def _save_nursery_section(self, section: NurserySection) -> None:
        """
        حفظ قسم المشتل في قاعدة البيانات
        
        المعاملات:
            section: كائن قسم المشتل
        """
        # تحويل كائن قسم المشتل إلى قاموس
        section_dict = section.to_dict()
        
        # حذف النباتات من القاموس
        section_dict.pop('plants', None)
        
        # بناء استعلام الإدراج أو التحديث
        columns = ', '.join(section_dict.keys())
        placeholders = ', '.join(['%s'] * len(section_dict))
        values = tuple(section_dict.values())
        
        # تنفيذ استعلام الإدراج أو التحديث
        query = f"""
        INSERT INTO nursery_sections ({columns})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE
        {', '.join([f'{col} = VALUES({col})' for col in section_dict.keys() if col != 'section_id'])}
        """
        
        self.db_manager.execute_query(query, values)
    
    def _delete_nursery_sections(self, nursery_id: str) -> None:
        """
        حذف أقسام المشتل
        
        المعاملات:
            nursery_id: معرف المشتل
        """
        # الحصول على أقسام المشتل
        sections = self._get_nursery_sections(nursery_id)
        
        # حذف النباتات المرتبطة بكل قسم
        for section in sections:
            self._delete_section_plants(section.section_id)
        
        # حذف أقسام المشتل
        query = "DELETE FROM nursery_sections WHERE nursery_id = %s"
        self.db_manager.execute_query(query, (nursery_id,))
    
    def _get_nursery_equipment(self, nursery_id: str) -> List[NurseryEquipment]:
        """
        الحصول على معدات المشتل
        
        المعاملات:
            nursery_id: معرف المشتل
            
        العائد:
            قائمة بكائنات معدات المشتل
        """
        # استعلام قاعدة البيانات للحصول على معدات المشتل
        query = "SELECT * FROM nursery_equipment WHERE nursery_id = %s"
        results = self.db_manager.execute_query(query, (nursery_id,))
        
        # إنشاء قائمة معدات المشتل
        equipment_list = []
        for equipment_data in results:
            equipment = NurseryEquipment.from_dict(equipment_data)
            equipment_list.append(equipment)
        
        return equipment_list
    
    def _delete_nursery_equipment(self, nursery_id: str) -> None:
        """
        حذف معدات المشتل
        
        المعاملات:
            nursery_id: معرف المشتل
        """
        # حذف معدات المشتل
        query = "DELETE FROM nursery_equipment WHERE nursery_id = %s"
        self.db_manager.execute_query(query, (nursery_id,))
    
    def _get_section_plants(self, section_id: str) -> List[Plant]:
        """
        الحصول على نباتات القسم
        
        المعاملات:
            section_id: معرف القسم
            
        العائد:
            قائمة بكائنات النباتات
        """
        # استعلام قاعدة البيانات للحصول على نباتات القسم
        query = "SELECT * FROM plants WHERE section_id = %s"
        results = self.db_manager.execute_query(query, (section_id,))
        
        # إنشاء قائمة النباتات
        plants = []
        for plant_data in results:
            plant = Plant.from_dict(plant_data)
            plant.activities = self._get_plant_activities(plant.plant_id)
            plants.append(plant)
        
        return plants
    
    def _delete_section_plants(self, section_id: str) -> None:
        """
        حذف نباتات القسم
        
        المعاملات:
            section_id: معرف القسم
        """
        # الحصول على نباتات القسم
        plants = self._get_section_plants(section_id)
        
        # حذف أنشطة النباتات
        for plant in plants:
            self._delete_plant_activities(plant.plant_id)
        
        # حذف نباتات القسم
        query = "DELETE FROM plants WHERE section_id = %s"
        self.db_manager.execute_query(query, (section_id,))
    
    def _get_plant_activities(self, plant_id: str) -> List[PlantActivity]:
        """
        الحصول على أنشطة النبات
        
        المعاملات:
            plant_id: معرف النبات
            
        العائد:
            قائمة بكائنات أنشطة النبات
        """
        # استعلام قاعدة البيانات للحصول على أنشطة النبات
        query = "SELECT * FROM plant_activities WHERE plant_id = %s"
        results = self.db_manager.execute_query(query, (plant_id,))
        
        # إنشاء قائمة أنشطة النبات
        activities = []
        for activity_data in results:
            activity = PlantActivity.from_dict(activity_data)
            activities.append(activity)
        
        return activities
    
    def _delete_plant_activities(self, plant_id: str) -> None:
        """
        حذف أنشطة النبات
        
        المعاملات:
            plant_id: معرف النبات
        """
        # حذف أنشطة النبات
        query = "DELETE FROM plant_activities WHERE plant_id = %s"
        self.db_manager.execute_query(query, (plant_id,))
    
    def get_nursery_statistics(self, nursery_id: str) -> Dict[str, Any]:
        """
        الحصول على إحصائيات المشتل
        
        المعاملات:
            nursery_id: معرف المشتل
            
        العائد:
            قاموس يحتوي على إحصائيات المشتل
        """
        # الحصول على المشتل
        nursery = self.get_nursery(nursery_id)
        if not nursery:
            return {}
        
        # حساب إجمالي عدد الأقسام
        total_sections = len(nursery.sections)
        
        # حساب إجمالي عدد النباتات
        total_plants = 0
        plants_by_status = {}
        plants_by_growth_stage = {}
        
        for section in nursery.sections:
            total_plants += len(section.plants)
            
            for plant in section.plants:
                # حساب النباتات حسب الحالة
                if plant.status in plants_by_status:
                    plants_by_status[plant.status] += 1
                else:
                    plants_by_status[plant.status] = 1
                
                # حساب النباتات حسب مرحلة النمو
                if plant.growth_stage in plants_by_growth_stage:
                    plants_by_growth_stage[plant.growth_stage] += 1
                else:
                    plants_by_growth_stage[plant.growth_stage] = 1
        
        # حساب نسبة الإشغال
        occupancy_rate = (total_plants / nursery.capacity) * 100 if nursery.capacity > 0 else 0
        
        # إنشاء قاموس الإحصائيات
        statistics = {
            "nursery_id": nursery_id,
            "nursery_name": nursery.name,
            "total_sections": total_sections,
            "total_plants": total_plants,
            "capacity": nursery.capacity,
            "occupancy_rate": occupancy_rate,
            "plants_by_status": plants_by_status,
            "plants_by_growth_stage": plants_by_growth_stage
        }
        
        return statistics
    
    def generate_nursery_report(self, nursery_id: str, report_type: str = "summary") -> Dict[str, Any]:
        """
        إنشاء تقرير عن المشتل
        
        المعاملات:
            nursery_id: معرف المشتل
            report_type: نوع التقرير (summary, detailed, financial)
            
        العائد:
            قاموس يحتوي على بيانات التقرير
        """
        # الحصول على المشتل
        nursery = self.get_nursery(nursery_id)
        if not nursery:
            return {}
        
        # الحصول على إحصائيات المشتل
        statistics = self.get_nursery_statistics(nursery_id)
        
        # إنشاء التقرير حسب النوع
        if report_type == "summary":
            report = {
                "report_type": "summary",
                "nursery_id": nursery_id,
                "nursery_name": nursery.name,
                "location": nursery.location,
                "manager_id": nursery.manager_id,
                "statistics": statistics
            }
        elif report_type == "detailed":
            # إنشاء تقرير مفصل يتضمن معلومات عن الأقسام والنباتات
            sections_data = []
            for section in nursery.sections:
                section_data = {
                    "section_id": section.section_id,
                    "name": section.name,
                    "area": section.area,
                    "capacity": section.capacity,
                    "section_type": section.section_type,
                    "total_plants": len(section.plants),
                    "plants": [
                        {
                            "plant_id": plant.plant_id,
                            "name": plant.name,
                            "variety": plant.variety,
                            "quantity": plant.quantity,
                            "status": plant.status,
                            "growth_stage": plant.growth_stage,
                            "health_status": plant.health_status
                        }
                        for plant in section.plants
                    ]
                }
                sections_data.append(section_data)
            
            report = {
                "report_type": "detailed",
                "nursery_id": nursery_id,
                "nursery_name": nursery.name,
                "location": nursery.location,
                "area": nursery.area,
                "capacity": nursery.capacity,
                "manager_id": nursery.manager_id,
                "company_id": nursery.company_id,
                "branch_id": nursery.branch_id,
                "creation_date": nursery.creation_date.isoformat(),
                "status": nursery.status,
                "description": nursery.description,
                "statistics": statistics,
                "sections": sections_data,
                "equipment": [
                    {
                        "equipment_id": equipment.equipment_id,
                        "name": equipment.name,
                        "equipment_type": equipment.equipment_type,
                        "status": equipment.status
                    }
                    for equipment in nursery.equipment
                ]
            }
        elif report_type == "financial":
            # إنشاء تقرير مالي (يتطلب بيانات إضافية من نظام المحاسبة)
            # هذا مجرد مثال بسيط
            report = {
                "report_type": "financial",
                "nursery_id": nursery_id,
                "nursery_name": nursery.name,
                "total_plants": statistics["total_plants"],
                "estimated_value": statistics["total_plants"] * 10,  # قيمة تقديرية بسيطة
                "expenses": {
                    "maintenance": 1000,
                    "labor": 2000,
                    "supplies": 1500
                },
                "revenue": {
                    "plant_sales": 5000
                }
            }
        else:
            report = {
                "error": "نوع التقرير غير معروف"
            }
        
        return report


class FarmService:
    """خدمة إدارة المزارع"""
    
    def __init__(self, db_manager):
        """
        تهيئة خدمة إدارة المزارع
        
        المعاملات:
            db_manager: مدير قاعدة البيانات
        """
        self.db_manager = db_manager
        
    def create_farm(self, farm_data: Dict[str, Any]) -> Farm:
        """
        إنشاء مزرعة جديدة
        
        المعاملات:
            farm_data: بيانات المزرعة
            
        العائد:
            كائن المزرعة الجديدة
        """
        # إنشاء معرف فريد للمزرعة
        farm_id = str(uuid.uuid4())
        farm_data['farm_id'] = farm_id
        
        # إنشاء كائن المزرعة
        farm = Farm.from_dict(farm_data)
        
        # حفظ المزرعة في قاعدة البيانات
        self._save_farm(farm)
        
        return farm
    
    def update_farm(self, farm_id: str, farm_data: Dict[str, Any]) -> Optional[Farm]:
        """
        تحديث بيانات مزرعة
        
        المعاملات:
            farm_id: معرف المزرعة
            farm_data: بيانات المزرعة المحدثة
            
        العائد:
            كائن المزرعة المحدثة أو None إذا لم يتم العثور على المزرعة
        """
        # البحث عن المزرعة
        farm = self.get_farm(farm_id)
        if not farm:
            return None
        
        # تحديث بيانات المزرعة
        farm_data['farm_id'] = farm_id
        updated_farm = Farm.from_dict(farm_data)
        
        # الحفاظ على القطع والمعدات الحالية
        updated_farm.plots = farm.plots
        updated_farm.equipment = farm.equipment
        
        # حفظ المزرعة المحدثة في قاعدة البيانات
        self._save_farm(updated_farm)
        
        return updated_farm
    
    def delete_farm(self, farm_id: str) -> bool:
        """
        حذف مزرعة
        
        المعاملات:
            farm_id: معرف المزرعة
            
        العائد:
            True إذا تم الحذف بنجاح، False إذا لم يتم العثور على المزرعة
        """
        # البحث عن المزرعة
        farm = self.get_farm(farm_id)
        if not farm:
            return False
        
        # حذف المزرعة من قاعدة البيانات
        query = "DELETE FROM farms WHERE farm_id = %s"
        self.db_manager.execute_query(query, (farm_id,))
        
        # حذف القطع والمعدات المرتبطة بالمزرعة
        self._delete_farm_plots(farm_id)
        self._delete_farm_equipment(farm_id)
        
        return True
    
    def get_farm(self, farm_id: str) -> Optional[Farm]:
        """
        الحصول على مزرعة بواسطة المعرف
        
        المعاملات:
            farm_id: معرف المزرعة
            
        العائد:
            كائن المزرعة أو None إذا لم يتم العثور على المزرعة
        """
        # استعلام قاعدة البيانات للحصول على المزرعة
        query = "SELECT * FROM farms WHERE farm_id = %s"
        result = self.db_manager.execute_query(query, (farm_id,))
        
        if not result:
            return None
        
        # إنشاء كائن المزرعة
        farm_data = result[0]
        farm = Farm.from_dict(farm_data)
        
        # إضافة القطع والمعدات
        farm.plots = self._get_farm_plots(farm_id)
        farm.equipment = self._get_farm_equipment(farm_id)
        
        return farm
    
    def get_all_farms(self, company_id: Optional[str] = None, branch_id: Optional[str] = None) -> List[Farm]:
        """
        الحصول على جميع المزارع
        
        المعاملات:
            company_id: معرف الشركة (اختياري)
            branch_id: معرف الفرع (اختياري)
            
        العائد:
            قائمة بكائنات المزارع
        """
        # بناء استعلام قاعدة البيانات
        query = "SELECT * FROM farms"
        params = []
        
        if company_id and branch_id:
            query += " WHERE company_id = %s AND branch_id = %s"
            params = [company_id, branch_id]
        elif company_id:
            query += " WHERE company_id = %s"
            params = [company_id]
        elif branch_id:
            query += " WHERE branch_id = %s"
            params = [branch_id]
        
        # تنفيذ الاستعلام
        results = self.db_manager.execute_query(query, tuple(params))
        
        # إنشاء قائمة المزارع
        farms = []
        for farm_data in results:
            farm = Farm.from_dict(farm_data)
            farm.plots = self._get_farm_plots(farm.farm_id)
            farm.equipment = self._get_farm_equipment(farm.farm_id)
            farms.append(farm)
        
        return farms
    
    def create_farm_plot(self, plot_data: Dict[str, Any]) -> FarmPlot:
        """
        إنشاء قطعة مزرعة جديدة
        
        المعاملات:
            plot_data: بيانات القطعة
            
        العائد:
            كائن قطعة المزرعة الجديدة
        """
        # إنشاء معرف فريد للقطعة
        plot_id = str(uuid.uuid4())
        plot_data['plot_id'] = plot_id
        
        # إنشاء كائن قطعة المزرعة
        plot = FarmPlot.from_dict(plot_data)
        
        # حفظ قطعة المزرعة في قاعدة البيانات
        self._save_farm_plot(plot)
        
        return plot
    
    def update_farm_plot(self, plot_id: str, plot_data: Dict[str, Any]) -> Optional[FarmPlot]:
        """
        تحديث بيانات قطعة مزرعة
        
        المعاملات:
            plot_id: معرف القطعة
            plot_data: بيانات القطعة المحدثة
            
        العائد:
            كائن قطعة المزرعة المحدثة أو None إذا لم يتم العثور على القطعة
        """
        # البحث عن القطعة
        plot = self.get_farm_plot(plot_id)
        if not plot:
            return None
        
        # تحديث بيانات القطعة
        plot_data['plot_id'] = plot_id
        plot_data['farm_id'] = plot.farm_id
        updated_plot = FarmPlot.from_dict(plot_data)
        
        # الحفاظ على المحاصيل الحالية
        updated_plot.crops = plot.crops
        
        # حفظ القطعة المحدثة في قاعدة البيانات
        self._save_farm_plot(updated_plot)
        
        return updated_plot
    
    def delete_farm_plot(self, plot_id: str) -> bool:
        """
        حذف قطعة مزرعة
        
        المعاملات:
            plot_id: معرف القطعة
            
        العائد:
            True إذا تم الحذف بنجاح، False إذا لم يتم العثور على القطعة
        """
        # البحث عن القطعة
        plot = self.get_farm_plot(plot_id)
        if not plot:
            return False
        
        # حذف القطعة من قاعدة البيانات
        query = "DELETE FROM farm_plots WHERE plot_id = %s"
        self.db_manager.execute_query(query, (plot_id,))
        
        # حذف المحاصيل المرتبطة بالقطعة
        self._delete_plot_crops(plot_id)
        
        return True
    
    def get_farm_plot(self, plot_id: str) -> Optional[FarmPlot]:
        """
        الحصول على قطعة مزرعة بواسطة المعرف
        
        المعاملات:
            plot_id: معرف القطعة
            
        العائد:
            كائن قطعة المزرعة أو None إذا لم يتم العثور على القطعة
        """
        # استعلام قاعدة البيانات للحصول على القطعة
        query = "SELECT * FROM farm_plots WHERE plot_id = %s"
        result = self.db_manager.execute_query(query, (plot_id,))
        
        if not result:
            return None
        
        # إنشاء كائن قطعة المزرعة
        plot_data = result[0]
        plot = FarmPlot.from_dict(plot_data)
        
        # إضافة المحاصيل
        plot.crops = self._get_plot_crops(plot_id)
        
        return plot
    
    def _get_farm_plots(self, farm_id: str) -> List[FarmPlot]:
        """
        الحصول على قطع المزرعة
        
        المعاملات:
            farm_id: معرف المزرعة
            
        العائد:
            قائمة بكائنات قطع المزرعة
        """
        # استعلام قاعدة البيانات للحصول على قطع المزرعة
        query = "SELECT * FROM farm_plots WHERE farm_id = %s"
        results = self.db_manager.execute_query(query, (farm_id,))
        
        # إنشاء قائمة قطع المزرعة
        plots = []
        for plot_data in results:
            plot = FarmPlot.from_dict(plot_data)
            plot.crops = self._get_plot_crops(plot.plot_id)
            plots.append(plot)
        
        return plots
    
    def _save_farm(self, farm: Farm) -> None:
        """
        حفظ المزرعة في قاعدة البيانات
        
        المعاملات:
            farm: كائن المزرعة
        """
        # تحويل كائن المزرعة إلى قاموس
        farm_dict = farm.to_dict()
        
        # حذف القطع والمعدات من القاموس
        farm_dict.pop('plots', None)
        farm_dict.pop('equipment', None)
        
        # بناء استعلام الإدراج أو التحديث
        columns = ', '.join(farm_dict.keys())
        placeholders = ', '.join(['%s'] * len(farm_dict))
        values = tuple(farm_dict.values())
        
        # تنفيذ استعلام الإدراج أو التحديث
        query = f"""
        INSERT INTO farms ({columns})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE
        {', '.join([f'{col} = VALUES({col})' for col in farm_dict.keys() if col != 'farm_id'])}
        """
        
        self.db_manager.execute_query(query, values)
    
    def _save_farm_plot(self, plot: FarmPlot) -> None:
        """
        حفظ قطعة المزرعة في قاعدة البيانات
        
        المعاملات:
            plot: كائن قطعة المزرعة
        """
        # تحويل كائن قطعة المزرعة إلى قاموس
        plot_dict = plot.to_dict()
        
        # حذف المحاصيل من القاموس
        plot_dict.pop('crops', None)
        
        # بناء استعلام الإدراج أو التحديث
        columns = ', '.join(plot_dict.keys())
        placeholders = ', '.join(['%s'] * len(plot_dict))
        values = tuple(plot_dict.values())
        
        # تنفيذ استعلام الإدراج أو التحديث
        query = f"""
        INSERT INTO farm_plots ({columns})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE
        {', '.join([f'{col} = VALUES({col})' for col in plot_dict.keys() if col != 'plot_id'])}
        """
        
        self.db_manager.execute_query(query, values)
    
    def _delete_farm_plots(self, farm_id: str) -> None:
        """
        حذف قطع المزرعة
        
        المعاملات:
            farm_id: معرف المزرعة
        """
        # الحصول على قطع المزرعة
        plots = self._get_farm_plots(farm_id)
        
        # حذف المحاصيل المرتبطة بكل قطعة
        for plot in plots:
            self._delete_plot_crops(plot.plot_id)
        
        # حذف قطع المزرعة
        query = "DELETE FROM farm_plots WHERE farm_id = %s"
        self.db_manager.execute_query(query, (farm_id,))
    
    def _get_farm_equipment(self, farm_id: str) -> List[FarmEquipment]:
        """
        الحصول على معدات المزرعة
        
        المعاملات:
            farm_id: معرف المزرعة
            
        العائد:
            قائمة بكائنات معدات المزرعة
        """
        # استعلام قاعدة البيانات للحصول على معدات المزرعة
        query = "SELECT * FROM farm_equipment WHERE farm_id = %s"
        results = self.db_manager.execute_query(query, (farm_id,))
        
        # إنشاء قائمة معدات المزرعة
        equipment_list = []
        for equipment_data in results:
            equipment = FarmEquipment.from_dict(equipment_data)
            equipment_list.append(equipment)
        
        return equipment_list
    
    def _delete_farm_equipment(self, farm_id: str) -> None:
        """
        حذف معدات المزرعة
        
        المعاملات:
            farm_id: معرف المزرعة
        """
        # حذف معدات المزرعة
        query = "DELETE FROM farm_equipment WHERE farm_id = %s"
        self.db_manager.execute_query(query, (farm_id,))
    
    def _get_plot_crops(self, plot_id: str) -> List[Crop]:
        """
        الحصول على محاصيل القطعة
        
        المعاملات:
            plot_id: معرف القطعة
            
        العائد:
            قائمة بكائنات المحاصيل
        """
        # استعلام قاعدة البيانات للحصول على محاصيل القطعة
        query = "SELECT * FROM crops WHERE plot_id = %s"
        results = self.db_manager.execute_query(query, (plot_id,))
        
        # إنشاء قائمة المحاصيل
        crops = []
        for crop_data in results:
            crop = Crop.from_dict(crop_data)
            crop.activities = self._get_crop_activities(crop.crop_id)
            crops.append(crop)
        
        return crops
    
    def _delete_plot_crops(self, plot_id: str) -> None:
        """
        حذف محاصيل القطعة
        
        المعاملات:
            plot_id: معرف القطعة
        """
        # الحصول على محاصيل القطعة
        crops = self._get_plot_crops(plot_id)
        
        # حذف أنشطة المحاصيل
        for crop in crops:
            self._delete_crop_activities(crop.crop_id)
        
        # حذف محاصيل القطعة
        query = "DELETE FROM crops WHERE plot_id = %s"
        self.db_manager.execute_query(query, (plot_id,))
    
    def _get_crop_activities(self, crop_id: str) -> List[CropActivity]:
        """
        الحصول على أنشطة المحصول
        
        المعاملات:
            crop_id: معرف المحصول
            
        العائد:
            قائمة بكائنات أنشطة المحصول
        """
        # استعلام قاعدة البيانات للحصول على أنشطة المحصول
        query = "SELECT * FROM crop_activities WHERE crop_id = %s"
        results = self.db_manager.execute_query(query, (crop_id,))
        
        # إنشاء قائمة أنشطة المحصول
        activities = []
        for activity_data in results:
            activity = CropActivity.from_dict(activity_data)
            activities.append(activity)
        
        return activities
    
    def _delete_crop_activities(self, crop_id: str) -> None:
        """
        حذف أنشطة المحصول
        
        المعاملات:
            crop_id: معرف المحصول
        """
        # حذف أنشطة المحصول
        query = "DELETE FROM crop_activities WHERE crop_id = %s"
        self.db_manager.execute_query(query, (crop_id,))
    
    def get_farm_statistics(self, farm_id: str) -> Dict[str, Any]:
        """
        الحصول على إحصائيات المزرعة
        
        المعاملات:
            farm_id: معرف المزرعة
            
        العائد:
            قاموس يحتوي على إحصائيات المزرعة
        """
        # الحصول على المزرعة
        farm = self.get_farm(farm_id)
        if not farm:
            return {}
        
        # حساب إجمالي عدد القطع
        total_plots = len(farm.plots)
        
        # حساب إجمالي المساحة المزروعة
        total_planted_area = 0
        
        # حساب إجمالي عدد المحاصيل
        total_crops = 0
        crops_by_status = {}
        
        for plot in farm.plots:
            total_crops += len(plot.crops)
            
            for crop in plot.crops:
                # حساب المساحة المزروعة
                total_planted_area += crop.area
                
                # حساب المحاصيل حسب الحالة
                if crop.status in crops_by_status:
                    crops_by_status[crop.status] += 1
                else:
                    crops_by_status[crop.status] = 1
        
        # حساب نسبة الاستغلال
        utilization_rate = (total_planted_area / farm.area) * 100 if farm.area > 0 else 0
        
        # إنشاء قاموس الإحصائيات
        statistics = {
            "farm_id": farm_id,
            "farm_name": farm.name,
            "total_plots": total_plots,
            "total_crops": total_crops,
            "total_area": farm.area,
            "planted_area": total_planted_area,
            "utilization_rate": utilization_rate,
            "crops_by_status": crops_by_status
        }
        
        return statistics
    
    def generate_farm_report(self, farm_id: str, report_type: str = "summary") -> Dict[str, Any]:
        """
        إنشاء تقرير عن المزرعة
        
        المعاملات:
            farm_id: معرف المزرعة
            report_type: نوع التقرير (summary, detailed, financial)
            
        العائد:
            قاموس يحتوي على بيانات التقرير
        """
        # الحصول على المزرعة
        farm = self.get_farm(farm_id)
        if not farm:
            return {}
        
        # الحصول على إحصائيات المزرعة
        statistics = self.get_farm_statistics(farm_id)
        
        # إنشاء التقرير حسب النوع
        if report_type == "summary":
            report = {
                "report_type": "summary",
                "farm_id": farm_id,
                "farm_name": farm.name,
                "location": farm.location,
                "manager_id": farm.manager_id,
                "statistics": statistics
            }
        elif report_type == "detailed":
            # إنشاء تقرير مفصل يتضمن معلومات عن القطع والمحاصيل
            plots_data = []
            for plot in farm.plots:
                plot_data = {
                    "plot_id": plot.plot_id,
                    "name": plot.name,
                    "area": plot.area,
                    "plot_type": plot.plot_type,
                    "soil_type": plot.soil_type,
                    "irrigation_type": plot.irrigation_type,
                    "status": plot.status,
                    "crops": [
                        {
                            "crop_id": crop.crop_id,
                            "name": crop.name,
                            "variety": crop.variety,
                            "area": crop.area,
                            "status": crop.status,
                            "planting_date": crop.planting_date.isoformat(),
                            "expected_harvest_date": crop.expected_harvest_date.isoformat() if crop.expected_harvest_date else None
                        }
                        for crop in plot.crops
                    ]
                }
                plots_data.append(plot_data)
            
            report = {
                "report_type": "detailed",
                "farm_id": farm_id,
                "farm_name": farm.name,
                "location": farm.location,
                "area": farm.area,
                "manager_id": farm.manager_id,
                "company_id": farm.company_id,
                "branch_id": farm.branch_id,
                "creation_date": farm.creation_date.isoformat(),
                "status": farm.status,
                "description": farm.description,
                "soil_type": farm.soil_type,
                "water_source": farm.water_source,
                "statistics": statistics,
                "plots": plots_data,
                "equipment": [
                    {
                        "equipment_id": equipment.equipment_id,
                        "name": equipment.name,
                        "equipment_type": equipment.equipment_type,
                        "status": equipment.status
                    }
                    for equipment in farm.equipment
                ]
            }
        elif report_type == "financial":
            # إنشاء تقرير مالي (يتطلب بيانات إضافية من نظام المحاسبة)
            # هذا مجرد مثال بسيط
            report = {
                "report_type": "financial",
                "farm_id": farm_id,
                "farm_name": farm.name,
                "total_area": farm.area,
                "planted_area": statistics["planted_area"],
                "estimated_value": statistics["planted_area"] * 1000,  # قيمة تقديرية بسيطة
                "expenses": {
                    "maintenance": 5000,
                    "labor": 10000,
                    "supplies": 7500,
                    "irrigation": 3000
                },
                "revenue": {
                    "crop_sales": 30000
                }
            }
        else:
            report = {
                "error": "نوع التقرير غير معروف"
            }
        
        return report
