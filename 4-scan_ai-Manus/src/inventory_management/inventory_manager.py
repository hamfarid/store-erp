#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مدير المخزون والإمدادات الزراعية

هذا الملف يتضمن وظائف إدارة المخزون من الأسمدة والمبيدات والمستلزمات الزراعية الأخرى،
مع تتبع الكميات المتوفرة والمستخدمة وتنبيهات انخفاض المخزون.
"""

import os
import json
import datetime
import logging
from typing import Dict, List, Optional, Tuple, Union
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from ..cost_management.cost_calculator import CostCalculator
from ..audit.audit_manager import AuditManager
from ..utils.config_loader import ConfigLoader

# إعداد قاعدة البيانات
Base = declarative_base()

class InventoryItem(Base):
    """نموذج عنصر المخزون في قاعدة البيانات"""
    __tablename__ = 'inventory_items'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)  # سماد، مبيد، أدوات، إلخ
    quantity = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)  # كجم، لتر، قطعة، إلخ
    unit_cost = Column(Float, nullable=False)
    min_threshold = Column(Float, nullable=False)  # الحد الأدنى للمخزون قبل التنبيه
    expiry_date = Column(DateTime, nullable=True)
    supplier = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    last_updated = Column(DateTime, default=datetime.datetime.now)
    notes = Column(String(500), nullable=True)
    
    # العلاقات
    transactions = relationship("InventoryTransaction", back_populates="item")

class InventoryTransaction(Base):
    """نموذج معاملات المخزون في قاعدة البيانات"""
    __tablename__ = 'inventory_transactions'
    
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('inventory_items.id'))
    transaction_type = Column(String(20), nullable=False)  # إضافة، استخدام، تعديل
    quantity = Column(Float, nullable=False)
    transaction_date = Column(DateTime, default=datetime.datetime.now)
    farm_id = Column(Integer, nullable=True)  # المزرعة المستخدمة (إذا كان استخدامًا)
    crop_id = Column(Integer, nullable=True)  # المحصول المستخدم له (إذا كان استخدامًا)
    user_id = Column(Integer, nullable=False)  # المستخدم الذي قام بالمعاملة
    notes = Column(String(500), nullable=True)
    
    # العلاقات
    item = relationship("InventoryItem", back_populates="transactions")

class InventoryManager:
    """مدير المخزون والإمدادات الزراعية"""
    
    def __init__(self, db_uri: str, config_path: str = None):
        """
        تهيئة مدير المخزون
        
        المعلمات:
            db_uri (str): رابط قاعدة البيانات
            config_path (str): مسار ملف التكوين
        """
        self.engine = create_engine(db_uri)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        
        # تحميل التكوين
        self.config = ConfigLoader(config_path).load_config() if config_path else {}
        
        # إعداد السجل
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # مدير التدقيق
        self.audit_manager = AuditManager(db_uri)
        
        # حاسبة التكلفة
        self.cost_calculator = CostCalculator(db_uri)
    
    def add_item(self, name: str, category: str, quantity: float, unit: str, 
                 unit_cost: float, min_threshold: float, expiry_date: Optional[datetime.datetime] = None,
                 supplier: Optional[str] = None, location: Optional[str] = None, 
                 notes: Optional[str] = None, user_id: int = 1) -> int:
        """
        إضافة عنصر جديد إلى المخزون
        
        المعلمات:
            name (str): اسم العنصر
            category (str): فئة العنصر (سماد، مبيد، أدوات، إلخ)
            quantity (float): الكمية
            unit (str): وحدة القياس
            unit_cost (float): تكلفة الوحدة
            min_threshold (float): الحد الأدنى للمخزون قبل التنبيه
            expiry_date (datetime): تاريخ انتهاء الصلاحية (اختياري)
            supplier (str): المورد (اختياري)
            location (str): موقع التخزين (اختياري)
            notes (str): ملاحظات (اختياري)
            user_id (int): معرف المستخدم الذي يقوم بالإضافة
            
        العائد:
            int: معرف العنصر المضاف
        """
        session = self.Session()
        try:
            # التحقق من وجود العنصر بنفس الاسم والفئة
            existing_item = session.query(InventoryItem).filter_by(name=name, category=category).first()
            
            if existing_item:
                # تحديث الكمية والتكلفة للعنصر الموجود
                old_quantity = existing_item.quantity
                old_cost = existing_item.unit_cost
                
                # حساب متوسط التكلفة الجديد (متوسط مرجح)
                total_old_value = old_quantity * old_cost
                total_new_value = quantity * unit_cost
                total_quantity = old_quantity + quantity
                new_avg_cost = (total_old_value + total_new_value) / total_quantity if total_quantity > 0 else unit_cost
                
                existing_item.quantity += quantity
                existing_item.unit_cost = new_avg_cost
                existing_item.last_updated = datetime.datetime.now()
                
                if expiry_date and (not existing_item.expiry_date or expiry_date > existing_item.expiry_date):
                    existing_item.expiry_date = expiry_date
                
                if supplier:
                    existing_item.supplier = supplier
                
                if location:
                    existing_item.location = location
                
                if notes:
                    existing_item.notes = notes if not existing_item.notes else f"{existing_item.notes}; {notes}"
                
                # إضافة معاملة
                transaction = InventoryTransaction(
                    item_id=existing_item.id,
                    transaction_type="إضافة",
                    quantity=quantity,
                    user_id=user_id,
                    notes=f"إضافة كمية {quantity} {unit} بتكلفة {unit_cost} للوحدة"
                )
                session.add(transaction)
                
                item_id = existing_item.id
            else:
                # إنشاء عنصر جديد
                new_item = InventoryItem(
                    name=name,
                    category=category,
                    quantity=quantity,
                    unit=unit,
                    unit_cost=unit_cost,
                    min_threshold=min_threshold,
                    expiry_date=expiry_date,
                    supplier=supplier,
                    location=location,
                    notes=notes
                )
                session.add(new_item)
                session.flush()  # للحصول على معرف العنصر الجديد
                
                # إضافة معاملة
                transaction = InventoryTransaction(
                    item_id=new_item.id,
                    transaction_type="إضافة",
                    quantity=quantity,
                    user_id=user_id,
                    notes=f"إضافة عنصر جديد بكمية {quantity} {unit}"
                )
                session.add(transaction)
                
                item_id = new_item.id
            
            # تسجيل في التدقيق
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="إضافة_مخزون",
                entity_type="inventory_item",
                entity_id=item_id,
                details=f"إضافة/تحديث عنصر المخزون: {name} ({category}) - الكمية: {quantity} {unit}"
            )
            
            session.commit()
            return item_id
        
        except Exception as e:
            session.rollback()
            self.logger.error(f"خطأ في إضافة عنصر المخزون: {str(e)}")
            raise
        finally:
            session.close()
    
    def use_item(self, item_id: int, quantity: float, farm_id: Optional[int] = None, 
                 crop_id: Optional[int] = None, notes: Optional[str] = None, 
                 user_id: int = 1) -> bool:
        """
        استخدام كمية من عنصر المخزون
        
        المعلمات:
            item_id (int): معرف العنصر
            quantity (float): الكمية المستخدمة
            farm_id (int): معرف المزرعة (اختياري)
            crop_id (int): معرف المحصول (اختياري)
            notes (str): ملاحظات (اختياري)
            user_id (int): معرف المستخدم
            
        العائد:
            bool: نجاح العملية
        """
        session = self.Session()
        try:
            item = session.query(InventoryItem).filter_by(id=item_id).first()
            
            if not item:
                raise ValueError(f"العنصر بالمعرف {item_id} غير موجود")
            
            if item.quantity < quantity:
                raise ValueError(f"الكمية المتوفرة ({item.quantity} {item.unit}) أقل من الكمية المطلوبة ({quantity} {item.unit})")
            
            # تحديث الكمية
            item.quantity -= quantity
            item.last_updated = datetime.datetime.now()
            
            # إضافة معاملة
            transaction = InventoryTransaction(
                item_id=item_id,
                transaction_type="استخدام",
                quantity=quantity,
                farm_id=farm_id,
                crop_id=crop_id,
                user_id=user_id,
                notes=notes
            )
            session.add(transaction)
            
            # تسجيل في التدقيق
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="استخدام_مخزون",
                entity_type="inventory_item",
                entity_id=item_id,
                details=f"استخدام {quantity} {item.unit} من {item.name} ({item.category})"
            )
            
            # التحقق من الحد الأدنى للمخزون
            if item.quantity <= item.min_threshold:
                self.logger.warning(f"تنبيه: مستوى المخزون منخفض لـ {item.name} ({item.quantity} {item.unit})")
                # يمكن إضافة إرسال إشعار هنا
            
            # حساب تكلفة الاستخدام
            usage_cost = quantity * item.unit_cost
            
            # إذا كان هناك معرف مزرعة، أضف التكلفة إلى سجل تكاليف المزرعة
            if farm_id:
                self.cost_calculator.add_farm_cost(
                    farm_id=farm_id,
                    cost_type=f"{item.category}",
                    amount=usage_cost,
                    description=f"استخدام {quantity} {item.unit} من {item.name}",
                    crop_id=crop_id,
                    user_id=user_id
                )
            
            session.commit()
            return True
        
        except Exception as e:
            session.rollback()
            self.logger.error(f"خطأ في استخدام عنصر المخزون: {str(e)}")
            raise
        finally:
            session.close()
    
    def adjust_item(self, item_id: int, new_quantity: float, reason: str, user_id: int = 1) -> bool:
        """
        تعديل كمية عنصر المخزون (للجرد أو التصحيح)
        
        المعلمات:
            item_id (int): معرف العنصر
            new_quantity (float): الكمية الجديدة
            reason (str): سبب التعديل
            user_id (int): معرف المستخدم
            
        العائد:
            bool: نجاح العملية
        """
        session = self.Session()
        try:
            item = session.query(InventoryItem).filter_by(id=item_id).first()
            
            if not item:
                raise ValueError(f"العنصر بالمعرف {item_id} غير موجود")
            
            old_quantity = item.quantity
            quantity_diff = new_quantity - old_quantity
            
            # إضافة معاملة
            transaction = InventoryTransaction(
                item_id=item_id,
                transaction_type="تعديل",
                quantity=quantity_diff,
                user_id=user_id,
                notes=f"تعديل الكمية من {old_quantity} إلى {new_quantity}: {reason}"
            )
            session.add(transaction)
            
            # تحديث الكمية
            item.quantity = new_quantity
            item.last_updated = datetime.datetime.now()
            
            # تسجيل في التدقيق
            self.audit_manager.log_action(
                user_id=user_id,
                action_type="تعديل_مخزون",
                entity_type="inventory_item",
                entity_id=item_id,
                details=f"تعديل كمية {item.name} من {old_quantity} إلى {new_quantity} {item.unit}: {reason}"
            )
            
            session.commit()
            return True
        
        except Exception as e:
            session.rollback()
            self.logger.error(f"خطأ في تعديل عنصر المخزون: {str(e)}")
            raise
        finally:
            session.close()
    
    def get_item(self, item_id: int) -> Dict:
        """
        الحصول على معلومات عنصر المخزون
        
        المعلمات:
            item_id (int): معرف العنصر
            
        العائد:
            Dict: معلومات العنصر
        """
        session = self.Session()
        try:
            item = session.query(InventoryItem).filter_by(id=item_id).first()
            
            if not item:
                raise ValueError(f"العنصر بالمعرف {item_id} غير موجود")
            
            return {
                'id': item.id,
                'name': item.name,
                'category': item.category,
                'quantity': item.quantity,
                'unit': item.unit,
                'unit_cost': item.unit_cost,
                'min_threshold': item.min_threshold,
                'expiry_date': item.expiry_date.isoformat() if item.expiry_date else None,
                'supplier': item.supplier,
                'location': item.location,
                'last_updated': item.last_updated.isoformat(),
                'notes': item.notes,
                'total_value': item.quantity * item.unit_cost
            }
        
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على معلومات عنصر المخزون: {str(e)}")
            raise
        finally:
            session.close()
    
    def get_all_items(self, category: Optional[str] = None, 
                      low_stock_only: bool = False) -> List[Dict]:
        """
        الحصول على قائمة عناصر المخزون
        
        المعلمات:
            category (str): تصفية حسب الفئة (اختياري)
            low_stock_only (bool): عرض العناصر ذات المخزون المنخفض فقط
            
        العائد:
            List[Dict]: قائمة عناصر المخزون
        """
        session = self.Session()
        try:
            query = session.query(InventoryItem)
            
            if category:
                query = query.filter(InventoryItem.category == category)
            
            if low_stock_only:
                query = query.filter(InventoryItem.quantity <= InventoryItem.min_threshold)
            
            items = query.all()
            
            result = []
            for item in items:
                result.append({
                    'id': item.id,
                    'name': item.name,
                    'category': item.category,
                    'quantity': item.quantity,
                    'unit': item.unit,
                    'unit_cost': item.unit_cost,
                    'min_threshold': item.min_threshold,
                    'expiry_date': item.expiry_date.isoformat() if item.expiry_date else None,
                    'supplier': item.supplier,
                    'location': item.location,
                    'last_updated': item.last_updated.isoformat(),
                    'notes': item.notes,
                    'total_value': item.quantity * item.unit_cost,
                    'is_low_stock': item.quantity <= item.min_threshold
                })
            
            return result
        
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على قائمة عناصر المخزون: {str(e)}")
            raise
        finally:
            session.close()
    
    def get_item_transactions(self, item_id: int, 
                              start_date: Optional[datetime.datetime] = None,
                              end_date: Optional[datetime.datetime] = None) -> List[Dict]:
        """
        الحصول على سجل معاملات عنصر المخزون
        
        المعلمات:
            item_id (int): معرف العنصر
            start_date (datetime): تاريخ البداية (اختياري)
            end_date (datetime): تاريخ النهاية (اختياري)
            
        العائد:
            List[Dict]: قائمة المعاملات
        """
        session = self.Session()
        try:
            query = session.query(InventoryTransaction).filter(InventoryTransaction.item_id == item_id)
            
            if start_date:
                query = query.filter(InventoryTransaction.transaction_date >= start_date)
            
            if end_date:
                query = query.filter(InventoryTransaction.transaction_date <= end_date)
            
            transactions = query.order_by(InventoryTransaction.transaction_date.desc()).all()
            
            result = []
            for transaction in transactions:
                result.append({
                    'id': transaction.id,
                    'transaction_type': transaction.transaction_type,
                    'quantity': transaction.quantity,
                    'transaction_date': transaction.transaction_date.isoformat(),
                    'farm_id': transaction.farm_id,
                    'crop_id': transaction.crop_id,
                    'user_id': transaction.user_id,
                    'notes': transaction.notes
                })
            
            return result
        
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على سجل معاملات عنصر المخزون: {str(e)}")
            raise
        finally:
            session.close()
    
    def get_expiring_items(self, days: int = 30) -> List[Dict]:
        """
        الحصول على قائمة العناصر التي ستنتهي صلاحيتها قريبًا
        
        المعلمات:
            days (int): عدد الأيام للتحقق (افتراضيًا 30 يومًا)
            
        العائد:
            List[Dict]: قائمة العناصر
        """
        session = self.Session()
        try:
            today = datetime.datetime.now().date()
            expiry_date = today + datetime.timedelta(days=days)
            
            items = session.query(InventoryItem).filter(
                InventoryItem.expiry_date.isnot(None),
                InventoryItem.expiry_date <= expiry_date,
                InventoryItem.expiry_date >= today,
                InventoryItem.quantity > 0
            ).all()
            
            result = []
            for item in items:
                days_remaining = (item.expiry_date.date() - today).days
                result.append({
                    'id': item.id,
                    'name': item.name,
                    'category': item.category,
                    'quantity': item.quantity,
                    'unit': item.unit,
                    'expiry_date': item.expiry_date.isoformat(),
                    'days_remaining': days_remaining,
                    'total_value': item.quantity * item.unit_cost
                })
            
            return result
        
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على قائمة العناصر التي ستنتهي صلاحيتها: {str(e)}")
            raise
        finally:
            session.close()
    
    def get_inventory_value(self, category: Optional[str] = None) -> Dict:
        """
        حساب إجمالي قيمة المخزون
        
        المعلمات:
            category (str): تصفية حسب الفئة (اختياري)
            
        العائد:
            Dict: إجمالي قيمة المخزون وتفاصيل حسب الفئة
        """
        session = self.Session()
        try:
            query = session.query(InventoryItem)
            
            if category:
                query = query.filter(InventoryItem.category == category)
            
            items = query.all()
            
            total_value = 0
            category_values = {}
            
            for item in items:
                item_value = item.quantity * item.unit_cost
                total_value += item_value
                
                if item.category not in category_values:
                    category_values[item.category] = 0
                
                category_values[item.category] += item_value
            
            return {
                'total_value': total_value,
                'category_breakdown': category_values
            }
        
        except Exception as e:
            self.logger.error(f"خطأ في حساب إجمالي قيمة المخزون: {str(e)}")
            raise
        finally:
            session.close()
    
    def generate_inventory_report(self, output_dir: str, 
                                  format: str = 'csv') -> str:
        """
        إنشاء تقرير المخزون
        
        المعلمات:
            output_dir (str): مجلد الإخراج
            format (str): تنسيق التقرير (csv، excel، json)
            
        العائد:
            str: مسار ملف التقرير
        """
        session = self.Session()
        try:
            items = session.query(InventoryItem).all()
            
            data = []
            for item in items:
                data.append({
                    'id': item.id,
                    'name': item.name,
                    'category': item.category,
                    'quantity': item.quantity,
                    'unit': item.unit,
                    'unit_cost': item.unit_cost,
                    'total_value': item.quantity * item.unit_cost,
                    'min_threshold': item.min_threshold,
                    'is_low_stock': item.quantity <= item.min_threshold,
                    'expiry_date': item.expiry_date.isoformat() if item.expiry_date else None,
                    'supplier': item.supplier,
                    'location': item.location,
                    'last_updated': item.last_updated.isoformat()
                })
            
            df = pd.DataFrame(data)
            
            # إنشاء اسم الملف بالتاريخ والوقت
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"inventory_report_{timestamp}"
            
            # التأكد من وجود المجلد
            os.makedirs(output_dir, exist_ok=True)
            
            # حفظ التقرير بالتنسيق المطلوب
            file_path = ""
            if format.lower() == 'csv':
                file_path = os.path.join(output_dir, f"{filename}.csv")
                df.to_csv(file_path, index=False, encoding='utf-8-sig')
            elif format.lower() == 'excel':
                file_path = os.path.join(output_dir, f"{filename}.xlsx")
                df.to_excel(file_path, index=False)
            elif format.lower() == 'json':
                file_path = os.path.join(output_dir, f"{filename}.json")
                df.to_json(file_path, orient='records', force_ascii=False)
            else:
                raise ValueError(f"تنسيق غير مدعوم: {format}")
            
            return file_path
        
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء تقرير المخزون: {str(e)}")
            raise
        finally:
            session.close()
    
    def generate_inventory_charts(self, output_dir: str) -> List[str]:
        """
        إنشاء رسوم بيانية للمخزون
        
        المعلمات:
            output_dir (str): مجلد الإخراج
            
        العائد:
            List[str]: قائمة مسارات ملفات الرسوم البيانية
        """
        session = self.Session()
        try:
            # التأكد من وجود المجلد
            os.makedirs(output_dir, exist_ok=True)
            
            # الحصول على البيانات
            items = session.query(InventoryItem).all()
            
            # إنشاء DataFrame
            data = []
            for item in items:
                data.append({
                    'id': item.id,
                    'name': item.name,
                    'category': item.category,
                    'quantity': item.quantity,
                    'unit': item.unit,
                    'unit_cost': item.unit_cost,
                    'total_value': item.quantity * item.unit_cost
                })
            
            df = pd.DataFrame(data)
            
            # قائمة مسارات الملفات
            file_paths = []
            
            # 1. رسم بياني للقيمة حسب الفئة
            if not df.empty and 'category' in df.columns and 'total_value' in df.columns:
                plt.figure(figsize=(12, 8))
                category_values = df.groupby('category')['total_value'].sum()
                category_values.plot(kind='pie', autopct='%1.1f%%')
                plt.title('توزيع قيمة المخزون حسب الفئة')
                plt.ylabel('')
                
                file_path = os.path.join(output_dir, "inventory_value_by_category.png")
                plt.savefig(file_path, bbox_inches='tight')
                plt.close()
                file_paths.append(file_path)
            
            # 2. رسم بياني للعناصر ذات المخزون المنخفض
            if not df.empty:
                low_stock_items = []
                for item in items:
                    if item.quantity <= item.min_threshold:
                        low_stock_items.append({
                            'name': item.name,
                            'current': item.quantity,
                            'threshold': item.min_threshold
                        })
                
                if low_stock_items:
                    low_stock_df = pd.DataFrame(low_stock_items)
                    plt.figure(figsize=(12, 8))
                    
                    # إنشاء رسم بياني شريطي مزدوج
                    ax = low_stock_df.plot(kind='bar', x='name', y=['current', 'threshold'], 
                                          color=['red', 'green'])
                    
                    plt.title('العناصر ذات المخزون المنخفض')
                    plt.xlabel('العنصر')
                    plt.ylabel('الكمية')
                    plt.legend(['المستوى الحالي', 'الحد الأدنى'])
                    plt.xticks(rotation=45, ha='right')
                    
                    file_path = os.path.join(output_dir, "low_stock_items.png")
                    plt.savefig(file_path, bbox_inches='tight')
                    plt.close()
                    file_paths.append(file_path)
            
            # 3. رسم بياني للعناصر الأعلى قيمة
            if not df.empty and 'name' in df.columns and 'total_value' in df.columns:
                plt.figure(figsize=(12, 8))
                top_items = df.nlargest(10, 'total_value')
                ax = top_items.plot(kind='barh', x='name', y='total_value', color='blue')
                
                plt.title('العناصر الأعلى قيمة في المخزون')
                plt.xlabel('القيمة الإجمالية')
                plt.ylabel('العنصر')
                
                # إضافة قيم على الرسم البياني
                for i, v in enumerate(top_items['total_value']):
                    ax.text(v, i, f" {v:.2f}", va='center')
                
                file_path = os.path.join(output_dir, "top_value_items.png")
                plt.savefig(file_path, bbox_inches='tight')
                plt.close()
                file_paths.append(file_path)
            
            return file_paths
        
        except Exception as e:
            self.logger.error(f"خطأ في إنشاء رسوم بيانية للمخزون: {str(e)}")
            raise
        finally:
            session.close()
    
    def get_farm_usage_history(self, farm_id: int, 
                               start_date: Optional[datetime.datetime] = None,
                               end_date: Optional[datetime.datetime] = None) -> Dict:
        """
        الحصول على سجل استخدام المزرعة للمخزون
        
        المعلمات:
            farm_id (int): معرف المزرعة
            start_date (datetime): تاريخ البداية (اختياري)
            end_date (datetime): تاريخ النهاية (اختياري)
            
        العائد:
            Dict: سجل الاستخدام وإجمالي التكلفة
        """
        session = self.Session()
        try:
            query = session.query(
                InventoryTransaction, InventoryItem
            ).join(
                InventoryItem, InventoryTransaction.item_id == InventoryItem.id
            ).filter(
                InventoryTransaction.farm_id == farm_id,
                InventoryTransaction.transaction_type == "استخدام"
            )
            
            if start_date:
                query = query.filter(InventoryTransaction.transaction_date >= start_date)
            
            if end_date:
                query = query.filter(InventoryTransaction.transaction_date <= end_date)
            
            results = query.order_by(InventoryTransaction.transaction_date.desc()).all()
            
            usage_records = []
            total_cost = 0
            category_costs = {}
            
            for transaction, item in results:
                cost = transaction.quantity * item.unit_cost
                total_cost += cost
                
                if item.category not in category_costs:
                    category_costs[item.category] = 0
                
                category_costs[item.category] += cost
                
                usage_records.append({
                    'transaction_id': transaction.id,
                    'item_id': item.id,
                    'item_name': item.name,
                    'category': item.category,
                    'quantity': transaction.quantity,
                    'unit': item.unit,
                    'unit_cost': item.unit_cost,
                    'total_cost': cost,
                    'transaction_date': transaction.transaction_date.isoformat(),
                    'crop_id': transaction.crop_id,
                    'notes': transaction.notes
                })
            
            return {
                'farm_id': farm_id,
                'total_cost': total_cost,
                'category_costs': category_costs,
                'usage_records': usage_records
            }
        
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على سجل استخدام المزرعة للمخزون: {str(e)}")
            raise
        finally:
            session.close()
    
    def get_crop_usage_history(self, crop_id: int,
                               start_date: Optional[datetime.datetime] = None,
                               end_date: Optional[datetime.datetime] = None) -> Dict:
        """
        الحصول على سجل استخدام المحصول للمخزون
        
        المعلمات:
            crop_id (int): معرف المحصول
            start_date (datetime): تاريخ البداية (اختياري)
            end_date (datetime): تاريخ النهاية (اختياري)
            
        العائد:
            Dict: سجل الاستخدام وإجمالي التكلفة
        """
        session = self.Session()
        try:
            query = session.query(
                InventoryTransaction, InventoryItem
            ).join(
                InventoryItem, InventoryTransaction.item_id == InventoryItem.id
            ).filter(
                InventoryTransaction.crop_id == crop_id,
                InventoryTransaction.transaction_type == "استخدام"
            )
            
            if start_date:
                query = query.filter(InventoryTransaction.transaction_date >= start_date)
            
            if end_date:
                query = query.filter(InventoryTransaction.transaction_date <= end_date)
            
            results = query.order_by(InventoryTransaction.transaction_date.desc()).all()
            
            usage_records = []
            total_cost = 0
            category_costs = {}
            
            for transaction, item in results:
                cost = transaction.quantity * item.unit_cost
                total_cost += cost
                
                if item.category not in category_costs:
                    category_costs[item.category] = 0
                
                category_costs[item.category] += cost
                
                usage_records.append({
                    'transaction_id': transaction.id,
                    'item_id': item.id,
                    'item_name': item.name,
                    'category': item.category,
                    'quantity': transaction.quantity,
                    'unit': item.unit,
                    'unit_cost': item.unit_cost,
                    'total_cost': cost,
                    'transaction_date': transaction.transaction_date.isoformat(),
                    'farm_id': transaction.farm_id,
                    'notes': transaction.notes
                })
            
            return {
                'crop_id': crop_id,
                'total_cost': total_cost,
                'category_costs': category_costs,
                'usage_records': usage_records
            }
        
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على سجل استخدام المحصول للمخزون: {str(e)}")
            raise
        finally:
            session.close()
    
    def calculate_per_area_usage(self, farm_id: int, area: float, 
                                 area_unit: str = 'فدان',
                                 start_date: Optional[datetime.datetime] = None,
                                 end_date: Optional[datetime.datetime] = None) -> Dict:
        """
        حساب استخدام المخزون لكل وحدة مساحة
        
        المعلمات:
            farm_id (int): معرف المزرعة
            area (float): المساحة
            area_unit (str): وحدة المساحة (فدان، هكتار، إلخ)
            start_date (datetime): تاريخ البداية (اختياري)
            end_date (datetime): تاريخ النهاية (اختياري)
            
        العائد:
            Dict: استخدام المخزون لكل وحدة مساحة
        """
        # الحصول على سجل استخدام المزرعة
        farm_usage = self.get_farm_usage_history(farm_id, start_date, end_date)
        
        # حساب التكلفة لكل وحدة مساحة
        cost_per_area = farm_usage['total_cost'] / area if area > 0 else 0
        
        # حساب التكلفة لكل فئة لكل وحدة مساحة
        category_costs_per_area = {}
        for category, cost in farm_usage['category_costs'].items():
            category_costs_per_area[category] = cost / area if area > 0 else 0
        
        # حساب الكمية لكل عنصر لكل وحدة مساحة
        item_usage_per_area = {}
        for record in farm_usage['usage_records']:
            item_id = record['item_id']
            item_name = record['item_name']
            key = f"{item_id}_{item_name}"
            
            if key not in item_usage_per_area:
                item_usage_per_area[key] = {
                    'item_id': item_id,
                    'item_name': item_name,
                    'category': record['category'],
                    'unit': record['unit'],
                    'total_quantity': 0,
                    'total_cost': 0
                }
            
            item_usage_per_area[key]['total_quantity'] += record['quantity']
            item_usage_per_area[key]['total_cost'] += record['total_cost']
        
        # حساب الكمية والتكلفة لكل وحدة مساحة
        for key in item_usage_per_area:
            item_usage_per_area[key]['quantity_per_area'] = item_usage_per_area[key]['total_quantity'] / area if area > 0 else 0
            item_usage_per_area[key]['cost_per_area'] = item_usage_per_area[key]['total_cost'] / area if area > 0 else 0
        
        return {
            'farm_id': farm_id,
            'area': area,
            'area_unit': area_unit,
            'total_cost': farm_usage['total_cost'],
            'cost_per_area': cost_per_area,
            'category_costs': farm_usage['category_costs'],
            'category_costs_per_area': category_costs_per_area,
            'item_usage_per_area': list(item_usage_per_area.values())
        }
    
    def forecast_inventory_needs(self, days: int = 90) -> Dict:
        """
        التنبؤ باحتياجات المخزون المستقبلية
        
        المعلمات:
            days (int): عدد الأيام للتنبؤ (افتراضيًا 90 يومًا)
            
        العائد:
            Dict: التنبؤ باحتياجات المخزون
        """
        session = self.Session()
        try:
            # تحديد تاريخ البداية والنهاية للتحليل التاريخي
            end_date = datetime.datetime.now()
            start_date = end_date - datetime.timedelta(days=days)
            
            # الحصول على جميع المعاملات في الفترة المحددة
            transactions = session.query(
                InventoryTransaction, InventoryItem
            ).join(
                InventoryItem, InventoryTransaction.item_id == InventoryItem.id
            ).filter(
                InventoryTransaction.transaction_type == "استخدام",
                InventoryTransaction.transaction_date >= start_date,
                InventoryTransaction.transaction_date <= end_date
            ).all()
            
            # تحليل معدل الاستهلاك لكل عنصر
            item_usage = {}
            for transaction, item in transactions:
                if item.id not in item_usage:
                    item_usage[item.id] = {
                        'item_id': item.id,
                        'name': item.name,
                        'category': item.category,
                        'unit': item.unit,
                        'current_quantity': item.quantity,
                        'min_threshold': item.min_threshold,
                        'total_usage': 0,
                        'usage_count': 0
                    }
                
                item_usage[item.id]['total_usage'] += transaction.quantity
                item_usage[item.id]['usage_count'] += 1
            
            # حساب متوسط الاستهلاك اليومي والتنبؤ بالاحتياجات المستقبلية
            forecast_results = []
            for item_id, data in item_usage.items():
                # حساب متوسط الاستهلاك اليومي
                daily_usage = data['total_usage'] / days if days > 0 else 0
                
                # حساب الأيام المتبقية قبل الوصول إلى الحد الأدنى
                days_until_threshold = (data['current_quantity'] - data['min_threshold']) / daily_usage if daily_usage > 0 else float('inf')
                
                # حساب الكمية المتوقع استهلاكها في الفترة المقبلة
                forecast_usage = daily_usage * days
                
                # حساب الكمية المطلوب شراؤها
                quantity_to_order = max(0, forecast_usage - data['current_quantity'] + data['min_threshold'])
                
                forecast_results.append({
                    'item_id': data['item_id'],
                    'name': data['name'],
                    'category': data['category'],
                    'unit': data['unit'],
                    'current_quantity': data['current_quantity'],
                    'min_threshold': data['min_threshold'],
                    'daily_usage': daily_usage,
                    'days_until_threshold': days_until_threshold,
                    'forecast_usage': forecast_usage,
                    'quantity_to_order': quantity_to_order,
                    'order_priority': 'عالي' if days_until_threshold < 30 else ('متوسط' if days_until_threshold < 60 else 'منخفض')
                })
            
            # ترتيب النتائج حسب الأولوية
            forecast_results.sort(key=lambda x: x['days_until_threshold'])
            
            return {
                'forecast_period_days': days,
                'forecast_date': end_date.isoformat(),
                'items': forecast_results
            }
        
        except Exception as e:
            self.logger.error(f"خطأ في التنبؤ باحتياجات المخزون: {str(e)}")
            raise
        finally:
            session.close()
