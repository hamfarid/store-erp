"""
نماذج بيانات المشاتل
يحتوي هذا الملف على تعريفات نماذج البيانات المتعلقة بإدارة المشاتل
"""

from datetime import datetime
from typing import List, Optional, Dict, Any

class Nursery:
    """نموذج بيانات المشتل الرئيسي"""
    
    def __init__(self, 
                 nursery_id: str, 
                 name: str, 
                 location: str, 
                 area: float, 
                 capacity: int,
                 manager_id: str,
                 company_id: str,
                 branch_id: str,
                 creation_date: datetime = None,
                 status: str = "نشط",
                 description: str = "",
                 coordinates: Dict[str, float] = None):
        """
        تهيئة كائن المشتل
        
        المعاملات:
            nursery_id: معرف المشتل الفريد
            name: اسم المشتل
            location: موقع المشتل
            area: مساحة المشتل بالمتر المربع
            capacity: السعة الإنتاجية للمشتل (عدد الشتلات)
            manager_id: معرف مدير المشتل
            company_id: معرف الشركة التابع لها المشتل
            branch_id: معرف الفرع التابع له المشتل
            creation_date: تاريخ إنشاء المشتل
            status: حالة المشتل (نشط، متوقف، تحت الصيانة)
            description: وصف المشتل
            coordinates: إحداثيات المشتل (خط الطول، خط العرض)
        """
        self.nursery_id = nursery_id
        self.name = name
        self.location = location
        self.area = area
        self.capacity = capacity
        self.manager_id = manager_id
        self.company_id = company_id
        self.branch_id = branch_id
        self.creation_date = creation_date or datetime.now()
        self.status = status
        self.description = description
        self.coordinates = coordinates or {}
        self.sections: List[NurserySection] = []
        self.equipment: List[NurseryEquipment] = []
        
    def to_dict(self) -> Dict[str, Any]:
        """تحويل كائن المشتل إلى قاموس"""
        return {
            "nursery_id": self.nursery_id,
            "name": self.name,
            "location": self.location,
            "area": self.area,
            "capacity": self.capacity,
            "manager_id": self.manager_id,
            "company_id": self.company_id,
            "branch_id": self.branch_id,
            "creation_date": self.creation_date.isoformat(),
            "status": self.status,
            "description": self.description,
            "coordinates": self.coordinates,
            "sections": [section.to_dict() for section in self.sections],
            "equipment": [equipment.to_dict() for equipment in self.equipment]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Nursery':
        """إنشاء كائن المشتل من قاموس"""
        nursery = cls(
            nursery_id=data["nursery_id"],
            name=data["name"],
            location=data["location"],
            area=data["area"],
            capacity=data["capacity"],
            manager_id=data["manager_id"],
            company_id=data["company_id"],
            branch_id=data["branch_id"],
            creation_date=datetime.fromisoformat(data["creation_date"]) if isinstance(data["creation_date"], str) else data["creation_date"],
            status=data["status"],
            description=data["description"],
            coordinates=data["coordinates"]
        )
        
        # إضافة الأقسام إذا كانت موجودة
        if "sections" in data:
            for section_data in data["sections"]:
                nursery.sections.append(NurserySection.from_dict(section_data))
                
        # إضافة المعدات إذا كانت موجودة
        if "equipment" in data:
            for equipment_data in data["equipment"]:
                nursery.equipment.append(NurseryEquipment.from_dict(equipment_data))
                
        return nursery


class NurserySection:
    """نموذج بيانات قسم المشتل"""
    
    def __init__(self,
                 section_id: str,
                 nursery_id: str,
                 name: str,
                 area: float,
                 capacity: int,
                 section_type: str,
                 climate_controlled: bool = False,
                 temperature_range: Dict[str, float] = None,
                 humidity_range: Dict[str, float] = None,
                 description: str = ""):
        """
        تهيئة كائن قسم المشتل
        
        المعاملات:
            section_id: معرف القسم الفريد
            nursery_id: معرف المشتل التابع له القسم
            name: اسم القسم
            area: مساحة القسم بالمتر المربع
            capacity: السعة الإنتاجية للقسم (عدد الشتلات)
            section_type: نوع القسم (بذور، شتلات، أمهات)
            climate_controlled: هل القسم متحكم بالمناخ
            temperature_range: نطاق درجة الحرارة (الحد الأدنى، الحد الأقصى)
            humidity_range: نطاق الرطوبة (الحد الأدنى، الحد الأقصى)
            description: وصف القسم
        """
        self.section_id = section_id
        self.nursery_id = nursery_id
        self.name = name
        self.area = area
        self.capacity = capacity
        self.section_type = section_type
        self.climate_controlled = climate_controlled
        self.temperature_range = temperature_range or {"min": 18.0, "max": 30.0}
        self.humidity_range = humidity_range or {"min": 40.0, "max": 80.0}
        self.description = description
        self.plants: List[Plant] = []
        
    def to_dict(self) -> Dict[str, Any]:
        """تحويل كائن قسم المشتل إلى قاموس"""
        return {
            "section_id": self.section_id,
            "nursery_id": self.nursery_id,
            "name": self.name,
            "area": self.area,
            "capacity": self.capacity,
            "section_type": self.section_type,
            "climate_controlled": self.climate_controlled,
            "temperature_range": self.temperature_range,
            "humidity_range": self.humidity_range,
            "description": self.description,
            "plants": [plant.to_dict() for plant in self.plants]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NurserySection':
        """إنشاء كائن قسم المشتل من قاموس"""
        section = cls(
            section_id=data["section_id"],
            nursery_id=data["nursery_id"],
            name=data["name"],
            area=data["area"],
            capacity=data["capacity"],
            section_type=data["section_type"],
            climate_controlled=data["climate_controlled"],
            temperature_range=data["temperature_range"],
            humidity_range=data["humidity_range"],
            description=data["description"]
        )
        
        # إضافة النباتات إذا كانت موجودة
        if "plants" in data:
            for plant_data in data["plants"]:
                section.plants.append(Plant.from_dict(plant_data))
                
        return section


class Plant:
    """نموذج بيانات النبات"""
    
    def __init__(self,
                 plant_id: str,
                 section_id: str,
                 nursery_id: str,
                 name: str,
                 variety: str,
                 quantity: int,
                 planting_date: datetime,
                 expected_harvest_date: Optional[datetime] = None,
                 status: str = "نمو",
                 growth_stage: str = "بذرة",
                 health_status: str = "سليم",
                 notes: str = ""):
        """
        تهيئة كائن النبات
        
        المعاملات:
            plant_id: معرف النبات الفريد
            section_id: معرف القسم التابع له النبات
            nursery_id: معرف المشتل التابع له النبات
            name: اسم النبات
            variety: صنف النبات
            quantity: كمية النباتات
            planting_date: تاريخ الزراعة
            expected_harvest_date: تاريخ الحصاد المتوقع
            status: حالة النبات (نمو، جاهز للنقل، تم نقله)
            growth_stage: مرحلة النمو (بذرة، شتلة، نبات بالغ)
            health_status: الحالة الصحية (سليم، مريض، معالج)
            notes: ملاحظات إضافية
        """
        self.plant_id = plant_id
        self.section_id = section_id
        self.nursery_id = nursery_id
        self.name = name
        self.variety = variety
        self.quantity = quantity
        self.planting_date = planting_date
        self.expected_harvest_date = expected_harvest_date
        self.status = status
        self.growth_stage = growth_stage
        self.health_status = health_status
        self.notes = notes
        self.activities: List[PlantActivity] = []
        
    def to_dict(self) -> Dict[str, Any]:
        """تحويل كائن النبات إلى قاموس"""
        return {
            "plant_id": self.plant_id,
            "section_id": self.section_id,
            "nursery_id": self.nursery_id,
            "name": self.name,
            "variety": self.variety,
            "quantity": self.quantity,
            "planting_date": self.planting_date.isoformat(),
            "expected_harvest_date": self.expected_harvest_date.isoformat() if self.expected_harvest_date else None,
            "status": self.status,
            "growth_stage": self.growth_stage,
            "health_status": self.health_status,
            "notes": self.notes,
            "activities": [activity.to_dict() for activity in self.activities]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Plant':
        """إنشاء كائن النبات من قاموس"""
        plant = cls(
            plant_id=data["plant_id"],
            section_id=data["section_id"],
            nursery_id=data["nursery_id"],
            name=data["name"],
            variety=data["variety"],
            quantity=data["quantity"],
            planting_date=datetime.fromisoformat(data["planting_date"]) if isinstance(data["planting_date"], str) else data["planting_date"],
            expected_harvest_date=datetime.fromisoformat(data["expected_harvest_date"]) if data.get("expected_harvest_date") and isinstance(data["expected_harvest_date"], str) else data.get("expected_harvest_date"),
            status=data["status"],
            growth_stage=data["growth_stage"],
            health_status=data["health_status"],
            notes=data["notes"]
        )
        
        # إضافة الأنشطة إذا كانت موجودة
        if "activities" in data:
            for activity_data in data["activities"]:
                plant.activities.append(PlantActivity.from_dict(activity_data))
                
        return plant


class PlantActivity:
    """نموذج بيانات نشاط النبات"""
    
    def __init__(self,
                 activity_id: str,
                 plant_id: str,
                 activity_type: str,
                 date: datetime,
                 performed_by: str,
                 description: str,
                 quantity_affected: int = 0,
                 resources_used: List[Dict[str, Any]] = None,
                 notes: str = ""):
        """
        تهيئة كائن نشاط النبات
        
        المعاملات:
            activity_id: معرف النشاط الفريد
            plant_id: معرف النبات المرتبط بالنشاط
            activity_type: نوع النشاط (ري، تسميد، مكافحة، تقليم)
            date: تاريخ النشاط
            performed_by: الشخص الذي قام بالنشاط
            description: وصف النشاط
            quantity_affected: الكمية المتأثرة
            resources_used: الموارد المستخدمة
            notes: ملاحظات إضافية
        """
        self.activity_id = activity_id
        self.plant_id = plant_id
        self.activity_type = activity_type
        self.date = date
        self.performed_by = performed_by
        self.description = description
        self.quantity_affected = quantity_affected
        self.resources_used = resources_used or []
        self.notes = notes
        
    def to_dict(self) -> Dict[str, Any]:
        """تحويل كائن نشاط النبات إلى قاموس"""
        return {
            "activity_id": self.activity_id,
            "plant_id": self.plant_id,
            "activity_type": self.activity_type,
            "date": self.date.isoformat(),
            "performed_by": self.performed_by,
            "description": self.description,
            "quantity_affected": self.quantity_affected,
            "resources_used": self.resources_used,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PlantActivity':
        """إنشاء كائن نشاط النبات من قاموس"""
        return cls(
            activity_id=data["activity_id"],
            plant_id=data["plant_id"],
            activity_type=data["activity_type"],
            date=datetime.fromisoformat(data["date"]) if isinstance(data["date"], str) else data["date"],
            performed_by=data["performed_by"],
            description=data["description"],
            quantity_affected=data["quantity_affected"],
            resources_used=data["resources_used"],
            notes=data["notes"]
        )


class NurseryEquipment:
    """نموذج بيانات معدات المشتل"""
    
    def __init__(self,
                 equipment_id: str,
                 nursery_id: str,
                 name: str,
                 equipment_type: str,
                 acquisition_date: datetime,
                 status: str = "صالح للاستخدام",
                 last_maintenance_date: Optional[datetime] = None,
                 next_maintenance_date: Optional[datetime] = None,
                 specifications: Dict[str, Any] = None,
                 notes: str = ""):
        """
        تهيئة كائن معدات المشتل
        
        المعاملات:
            equipment_id: معرف المعدة الفريد
            nursery_id: معرف المشتل التابعة له المعدة
            name: اسم المعدة
            equipment_type: نوع المعدة
            acquisition_date: تاريخ الاقتناء
            status: حالة المعدة
            last_maintenance_date: تاريخ آخر صيانة
            next_maintenance_date: تاريخ الصيانة القادمة
            specifications: مواصفات المعدة
            notes: ملاحظات إضافية
        """
        self.equipment_id = equipment_id
        self.nursery_id = nursery_id
        self.name = name
        self.equipment_type = equipment_type
        self.acquisition_date = acquisition_date
        self.status = status
        self.last_maintenance_date = last_maintenance_date
        self.next_maintenance_date = next_maintenance_date
        self.specifications = specifications or {}
        self.notes = notes
        
    def to_dict(self) -> Dict[str, Any]:
        """تحويل كائن معدات المشتل إلى قاموس"""
        return {
            "equipment_id": self.equipment_id,
            "nursery_id": self.nursery_id,
            "name": self.name,
            "equipment_type": self.equipment_type,
            "acquisition_date": self.acquisition_date.isoformat(),
            "status": self.status,
            "last_maintenance_date": self.last_maintenance_date.isoformat() if self.last_maintenance_date else None,
            "next_maintenance_date": self.next_maintenance_date.isoformat() if self.next_maintenance_date else None,
            "specifications": self.specifications,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NurseryEquipment':
        """إنشاء كائن معدات المشتل من قاموس"""
        return cls(
            equipment_id=data["equipment_id"],
            nursery_id=data["nursery_id"],
            name=data["name"],
            equipment_type=data["equipment_type"],
            acquisition_date=datetime.fromisoformat(data["acquisition_date"]) if isinstance(data["acquisition_date"], str) else data["acquisition_date"],
            status=data["status"],
            last_maintenance_date=datetime.fromisoformat(data["last_maintenance_date"]) if data.get("last_maintenance_date") and isinstance(data["last_maintenance_date"], str) else data.get("last_maintenance_date"),
            next_maintenance_date=datetime.fromisoformat(data["next_maintenance_date"]) if data.get("next_maintenance_date") and isinstance(data["next_maintenance_date"], str) else data.get("next_maintenance_date"),
            specifications=data["specifications"],
            notes=data["notes"]
        )


class Farm:
    """نموذج بيانات المزرعة"""
    
    def __init__(self,
                 farm_id: str,
                 name: str,
                 location: str,
                 area: float,
                 manager_id: str,
                 company_id: str,
                 branch_id: str,
                 creation_date: datetime = None,
                 status: str = "نشط",
                 description: str = "",
                 coordinates: Dict[str, float] = None,
                 soil_type: str = "",
                 water_source: str = ""):
        """
        تهيئة كائن المزرعة
        
        المعاملات:
            farm_id: معرف المزرعة الفريد
            name: اسم المزرعة
            location: موقع المزرعة
            area: مساحة المزرعة بالهكتار
            manager_id: معرف مدير المزرعة
            company_id: معرف الشركة التابعة لها المزرعة
            branch_id: معرف الفرع التابع له المزرعة
            creation_date: تاريخ إنشاء المزرعة
            status: حالة المزرعة (نشط، متوقف، تحت الصيانة)
            description: وصف المزرعة
            coordinates: إحداثيات المزرعة (خط الطول، خط العرض)
            soil_type: نوع التربة
            water_source: مصدر المياه
        """
        self.farm_id = farm_id
        self.name = name
        self.location = location
        self.area = area
        self.manager_id = manager_id
        self.company_id = company_id
        self.branch_id = branch_id
        self.creation_date = creation_date or datetime.now()
        self.status = status
        self.description = description
        self.coordinates = coordinates or {}
        self.soil_type = soil_type
        self.water_source = water_source
        self.plots: List[FarmPlot] = []
        self.equipment: List[FarmEquipment] = []
        
    def to_dict(self) -> Dict[str, Any]:
        """تحويل كائن المزرعة إلى قاموس"""
        return {
            "farm_id": self.farm_id,
            "name": self.name,
            "location": self.location,
            "area": self.area,
            "manager_id": self.manager_id,
            "company_id": self.company_id,
            "branch_id": self.branch_id,
            "creation_date": self.creation_date.isoformat(),
            "status": self.status,
            "description": self.description,
            "coordinates": self.coordinates,
            "soil_type": self.soil_type,
            "water_source": self.water_source,
            "plots": [plot.to_dict() for plot in self.plots],
            "equipment": [equipment.to_dict() for equipment in self.equipment]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Farm':
        """إنشاء كائن المزرعة من قاموس"""
        farm = cls(
            farm_id=data["farm_id"],
            name=data["name"],
            location=data["location"],
            area=data["area"],
            manager_id=data["manager_id"],
            company_id=data["company_id"],
            branch_id=data["branch_id"],
            creation_date=datetime.fromisoformat(data["creation_date"]) if isinstance(data["creation_date"], str) else data["creation_date"],
            status=data["status"],
            description=data["description"],
            coordinates=data["coordinates"],
            soil_type=data["soil_type"],
            water_source=data["water_source"]
        )
        
        # إضافة القطع إذا كانت موجودة
        if "plots" in data:
            for plot_data in data["plots"]:
                farm.plots.append(FarmPlot.from_dict(plot_data))
                
        # إضافة المعدات إذا كانت موجودة
        if "equipment" in data:
            for equipment_data in data["equipment"]:
                farm.equipment.append(FarmEquipment.from_dict(equipment_data))
                
        return farm


class FarmPlot:
    """نموذج بيانات قطعة المزرعة"""
    
    def __init__(self,
                 plot_id: str,
                 farm_id: str,
                 name: str,
                 area: float,
                 plot_type: str,
                 soil_type: str = "",
                 irrigation_type: str = "",
                 status: str = "متاح",
                 description: str = "",
                 coordinates: List[Dict[str, float]] = None):
        """
        تهيئة كائن قطعة المزرعة
        
        المعاملات:
            plot_id: معرف القطعة الفريد
            farm_id: معرف المزرعة التابعة لها القطعة
            name: اسم القطعة
            area: مساحة القطعة بالهكتار
            plot_type: نوع القطعة (مفتوحة، محمية، مختلطة)
            soil_type: نوع التربة
            irrigation_type: نوع الري
            status: حالة القطعة (متاح، مزروع، تحت الصيانة)
            description: وصف القطعة
            coordinates: إحداثيات حدود القطعة
        """
        self.plot_id = plot_id
        self.farm_id = farm_id
        self.name = name
        self.area = area
        self.plot_type = plot_type
        self.soil_type = soil_type
        self.irrigation_type = irrigation_type
        self.status = status
        self.description = description
        self.coordinates = coordinates or []
        self.crops: List[Crop] = []
        
    def to_dict(self) -> Dict[str, Any]:
        """تحويل كائن قطعة المزرعة إلى قاموس"""
        return {
            "plot_id": self.plot_id,
            "farm_id": self.farm_id,
            "name": self.name,
            "area": self.area,
            "plot_type": self.plot_type,
            "soil_type": self.soil_type,
            "irrigation_type": self.irrigation_type,
            "status": self.status,
            "description": self.description,
            "coordinates": self.coordinates,
            "crops": [crop.to_dict() for crop in self.crops]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FarmPlot':
        """إنشاء كائن قطعة المزرعة من قاموس"""
        plot = cls(
            plot_id=data["plot_id"],
            farm_id=data["farm_id"],
            name=data["name"],
            area=data["area"],
            plot_type=data["plot_type"],
            soil_type=data["soil_type"],
            irrigation_type=data["irrigation_type"],
            status=data["status"],
            description=data["description"],
            coordinates=data["coordinates"]
        )
        
        # إضافة المحاصيل إذا كانت موجودة
        if "crops" in data:
            for crop_data in data["crops"]:
                plot.crops.append(Crop.from_dict(crop_data))
                
        return plot


class Crop:
    """نموذج بيانات المحصول"""
    
    def __init__(self,
                 crop_id: str,
                 plot_id: str,
                 farm_id: str,
                 name: str,
                 variety: str,
                 planting_date: datetime,
                 expected_harvest_date: Optional[datetime] = None,
                 actual_harvest_date: Optional[datetime] = None,
                 status: str = "نمو",
                 area: float = 0.0,
                 quantity_planted: int = 0,
                 expected_yield: float = 0.0,
                 actual_yield: float = 0.0,
                 notes: str = ""):
        """
        تهيئة كائن المحصول
        
        المعاملات:
            crop_id: معرف المحصول الفريد
            plot_id: معرف القطعة التابع لها المحصول
            farm_id: معرف المزرعة التابعة لها المحصول
            name: اسم المحصول
            variety: صنف المحصول
            planting_date: تاريخ الزراعة
            expected_harvest_date: تاريخ الحصاد المتوقع
            actual_harvest_date: تاريخ الحصاد الفعلي
            status: حالة المحصول (نمو، جاهز للحصاد، تم حصاده)
            area: المساحة المزروعة بالهكتار
            quantity_planted: الكمية المزروعة
            expected_yield: الإنتاجية المتوقعة
            actual_yield: الإنتاجية الفعلية
            notes: ملاحظات إضافية
        """
        self.crop_id = crop_id
        self.plot_id = plot_id
        self.farm_id = farm_id
        self.name = name
        self.variety = variety
        self.planting_date = planting_date
        self.expected_harvest_date = expected_harvest_date
        self.actual_harvest_date = actual_harvest_date
        self.status = status
        self.area = area
        self.quantity_planted = quantity_planted
        self.expected_yield = expected_yield
        self.actual_yield = actual_yield
        self.notes = notes
        self.activities: List[CropActivity] = []
        
    def to_dict(self) -> Dict[str, Any]:
        """تحويل كائن المحصول إلى قاموس"""
        return {
            "crop_id": self.crop_id,
            "plot_id": self.plot_id,
            "farm_id": self.farm_id,
            "name": self.name,
            "variety": self.variety,
            "planting_date": self.planting_date.isoformat(),
            "expected_harvest_date": self.expected_harvest_date.isoformat() if self.expected_harvest_date else None,
            "actual_harvest_date": self.actual_harvest_date.isoformat() if self.actual_harvest_date else None,
            "status": self.status,
            "area": self.area,
            "quantity_planted": self.quantity_planted,
            "expected_yield": self.expected_yield,
            "actual_yield": self.actual_yield,
            "notes": self.notes,
            "activities": [activity.to_dict() for activity in self.activities]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Crop':
        """إنشاء كائن المحصول من قاموس"""
        crop = cls(
            crop_id=data["crop_id"],
            plot_id=data["plot_id"],
            farm_id=data["farm_id"],
            name=data["name"],
            variety=data["variety"],
            planting_date=datetime.fromisoformat(data["planting_date"]) if isinstance(data["planting_date"], str) else data["planting_date"],
            expected_harvest_date=datetime.fromisoformat(data["expected_harvest_date"]) if data.get("expected_harvest_date") and isinstance(data["expected_harvest_date"], str) else data.get("expected_harvest_date"),
            actual_harvest_date=datetime.fromisoformat(data["actual_harvest_date"]) if data.get("actual_harvest_date") and isinstance(data["actual_harvest_date"], str) else data.get("actual_harvest_date"),
            status=data["status"],
            area=data["area"],
            quantity_planted=data["quantity_planted"],
            expected_yield=data["expected_yield"],
            actual_yield=data["actual_yield"],
            notes=data["notes"]
        )
        
        # إضافة الأنشطة إذا كانت موجودة
        if "activities" in data:
            for activity_data in data["activities"]:
                crop.activities.append(CropActivity.from_dict(activity_data))
                
        return crop


class CropActivity:
    """نموذج بيانات نشاط المحصول"""
    
    def __init__(self,
                 activity_id: str,
                 crop_id: str,
                 activity_type: str,
                 date: datetime,
                 performed_by: str,
                 description: str,
                 area_affected: float = 0.0,
                 resources_used: List[Dict[str, Any]] = None,
                 cost: float = 0.0,
                 notes: str = ""):
        """
        تهيئة كائن نشاط المحصول
        
        المعاملات:
            activity_id: معرف النشاط الفريد
            crop_id: معرف المحصول المرتبط بالنشاط
            activity_type: نوع النشاط (ري، تسميد، مكافحة، حصاد)
            date: تاريخ النشاط
            performed_by: الشخص الذي قام بالنشاط
            description: وصف النشاط
            area_affected: المساحة المتأثرة
            resources_used: الموارد المستخدمة
            cost: تكلفة النشاط
            notes: ملاحظات إضافية
        """
        self.activity_id = activity_id
        self.crop_id = crop_id
        self.activity_type = activity_type
        self.date = date
        self.performed_by = performed_by
        self.description = description
        self.area_affected = area_affected
        self.resources_used = resources_used or []
        self.cost = cost
        self.notes = notes
        
    def to_dict(self) -> Dict[str, Any]:
        """تحويل كائن نشاط المحصول إلى قاموس"""
        return {
            "activity_id": self.activity_id,
            "crop_id": self.crop_id,
            "activity_type": self.activity_type,
            "date": self.date.isoformat(),
            "performed_by": self.performed_by,
            "description": self.description,
            "area_affected": self.area_affected,
            "resources_used": self.resources_used,
            "cost": self.cost,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CropActivity':
        """إنشاء كائن نشاط المحصول من قاموس"""
        return cls(
            activity_id=data["activity_id"],
            crop_id=data["crop_id"],
            activity_type=data["activity_type"],
            date=datetime.fromisoformat(data["date"]) if isinstance(data["date"], str) else data["date"],
            performed_by=data["performed_by"],
            description=data["description"],
            area_affected=data["area_affected"],
            resources_used=data["resources_used"],
            cost=data["cost"],
            notes=data["notes"]
        )


class FarmEquipment:
    """نموذج بيانات معدات المزرعة"""
    
    def __init__(self,
                 equipment_id: str,
                 farm_id: str,
                 name: str,
                 equipment_type: str,
                 acquisition_date: datetime,
                 status: str = "صالح للاستخدام",
                 last_maintenance_date: Optional[datetime] = None,
                 next_maintenance_date: Optional[datetime] = None,
                 specifications: Dict[str, Any] = None,
                 notes: str = ""):
        """
        تهيئة كائن معدات المزرعة
        
        المعاملات:
            equipment_id: معرف المعدة الفريد
            farm_id: معرف المزرعة التابعة لها المعدة
            name: اسم المعدة
            equipment_type: نوع المعدة
            acquisition_date: تاريخ الاقتناء
            status: حالة المعدة
            last_maintenance_date: تاريخ آخر صيانة
            next_maintenance_date: تاريخ الصيانة القادمة
            specifications: مواصفات المعدة
            notes: ملاحظات إضافية
        """
        self.equipment_id = equipment_id
        self.farm_id = farm_id
        self.name = name
        self.equipment_type = equipment_type
        self.acquisition_date = acquisition_date
        self.status = status
        self.last_maintenance_date = last_maintenance_date
        self.next_maintenance_date = next_maintenance_date
        self.specifications = specifications or {}
        self.notes = notes
        
    def to_dict(self) -> Dict[str, Any]:
        """تحويل كائن معدات المزرعة إلى قاموس"""
        return {
            "equipment_id": self.equipment_id,
            "farm_id": self.farm_id,
            "name": self.name,
            "equipment_type": self.equipment_type,
            "acquisition_date": self.acquisition_date.isoformat(),
            "status": self.status,
            "last_maintenance_date": self.last_maintenance_date.isoformat() if self.last_maintenance_date else None,
            "next_maintenance_date": self.next_maintenance_date.isoformat() if self.next_maintenance_date else None,
            "specifications": self.specifications,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FarmEquipment':
        """إنشاء كائن معدات المزرعة من قاموس"""
        return cls(
            equipment_id=data["equipment_id"],
            farm_id=data["farm_id"],
            name=data["name"],
            equipment_type=data["equipment_type"],
            acquisition_date=datetime.fromisoformat(data["acquisition_date"]) if isinstance(data["acquisition_date"], str) else data["acquisition_date"],
            status=data["status"],
            last_maintenance_date=datetime.fromisoformat(data["last_maintenance_date"]) if data.get("last_maintenance_date") and isinstance(data["last_maintenance_date"], str) else data.get("last_maintenance_date"),
            next_maintenance_date=datetime.fromisoformat(data["next_maintenance_date"]) if data.get("next_maintenance_date") and isinstance(data["next_maintenance_date"], str) else data.get("next_maintenance_date"),
            specifications=data["specifications"],
            notes=data["notes"]
        )
