#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نظام إدارة المهام
===============

يوفر هذا المديول نظامًا لإدارة المهام الرئيسية والفرعية في نظام الذكاء الاصطناعي الزراعي،
مع إمكانية تتبع التقدم وإعداد التقارير وإدارة الإشعارات.

المؤلف: فريق Manus للذكاء الاصطناعي
الإصدار: 1.0.0
التاريخ: أبريل 2025
"""

import os
import logging
import json
import uuid
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime, timedelta
import threading
import time

# إعداد السجل
logger = logging.getLogger("agricultural_ai.task_manager")

class Task:
    """فئة تمثل مهمة فردية"""
    
    def __init__(self, 
                title: str, 
                description: str = "", 
                parent_id: str = None, 
                priority: int = 2, 
                due_date: datetime = None,
                tags: List[str] = None,
                assignee: str = None):
        """تهيئة مهمة جديدة
        
        المعاملات:
            title (str): عنوان المهمة
            description (str): وصف المهمة
            parent_id (str): معرف المهمة الأم (إذا كانت مهمة فرعية)
            priority (int): أولوية المهمة (1: منخفضة، 2: متوسطة، 3: عالية)
            due_date (datetime): تاريخ استحقاق المهمة
            tags (List[str]): وسوم المهمة
            assignee (str): الشخص المسؤول عن المهمة
        """
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.parent_id = parent_id
        self.priority = priority
        self.due_date = due_date
        self.tags = tags or []
        self.assignee = assignee
        self.status = "pending"  # pending, in_progress, completed, cancelled
        self.progress = 0  # 0-100
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.completed_at = None
        self.subtasks = []  # قائمة بمعرفات المهام الفرعية
        self.notes = []  # ملاحظات إضافية
        self.attachments = []  # مرفقات
        
    def to_dict(self) -> Dict:
        """تحويل المهمة إلى قاموس
        
        الإرجاع:
            Dict: تمثيل المهمة كقاموس
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "parent_id": self.parent_id,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "tags": self.tags,
            "assignee": self.assignee,
            "status": self.status,
            "progress": self.progress,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "subtasks": self.subtasks,
            "notes": self.notes,
            "attachments": self.attachments
        }
        
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """إنشاء مهمة من قاموس
        
        المعاملات:
            data (Dict): قاموس يحتوي على بيانات المهمة
            
        الإرجاع:
            Task: كائن المهمة
        """
        task = cls(
            title=data.get("title", ""),
            description=data.get("description", ""),
            parent_id=data.get("parent_id"),
            priority=data.get("priority", 2),
            tags=data.get("tags", []),
            assignee=data.get("assignee")
        )
        
        task.id = data.get("id", task.id)
        task.status = data.get("status", "pending")
        task.progress = data.get("progress", 0)
        
        # تحويل التواريخ من سلاسل نصية إلى كائنات datetime
        if "created_at" in data:
            task.created_at = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data:
            task.updated_at = datetime.fromisoformat(data["updated_at"])
        if "completed_at" in data and data["completed_at"]:
            task.completed_at = datetime.fromisoformat(data["completed_at"])
        if "due_date" in data and data["due_date"]:
            task.due_date = datetime.fromisoformat(data["due_date"])
            
        task.subtasks = data.get("subtasks", [])
        task.notes = data.get("notes", [])
        task.attachments = data.get("attachments", [])
        
        return task

class TaskManager:
    """فئة لإدارة المهام"""
    
    def __init__(self, config: Dict):
        """تهيئة مدير المهام
        
        المعاملات:
            config (Dict): تكوين مدير المهام
        """
        self.config = config.get("task_manager", {})
        self.tasks = {}  # قاموس المهام (المفتاح: معرف المهمة، القيمة: كائن المهمة)
        self.data_file = self.config.get("data_file", "data/tasks.json")
        self.auto_save = self.config.get("auto_save", True)
        self.notification_handlers = []  # معالجات الإشعارات
        self.reminder_thread = None  # خيط التذكير
        self.stop_reminder_thread = False  # علامة لإيقاف خيط التذكير
        
        # إنشاء مجلد البيانات إذا لم يكن موجودًا
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        # محاولة تحميل المهام من الملف
        self._load_tasks()
        
        # بدء خيط التذكير إذا كان مطلوبًا
        if self.config.get("enable_reminders", True):
            self._start_reminder_thread()
            
        logger.info("تم تهيئة مدير المهام")

    def add_task(self, task_data: Dict) -> str:
        """إضافة مهمة جديدة
        
        المعاملات:
            task_data (Dict): بيانات المهمة
            
        الإرجاع:
            str: معرف المهمة الجديدة
        """
        # إنشاء كائن المهمة
        task = Task(
            title=task_data.get("title", "مهمة جديدة"),
            description=task_data.get("description", ""),
            parent_id=task_data.get("parent_id"),
            priority=task_data.get("priority", 2),
            due_date=task_data.get("due_date"),
            tags=task_data.get("tags", []),
            assignee=task_data.get("assignee")
        )
        
        # إضافة المهمة إلى القاموس
        self.tasks[task.id] = task
        
        # إذا كانت مهمة فرعية، إضافتها إلى المهمة الأم
        if task.parent_id and task.parent_id in self.tasks:
            parent_task = self.tasks[task.parent_id]
            parent_task.subtasks.append(task.id)
            parent_task.updated_at = datetime.now()
            
        # حفظ المهام إذا كان الحفظ التلقائي مفعلاً
        if self.auto_save:
            self._save_tasks()
            
        # إرسال إشعار بإضافة مهمة جديدة
        self._notify("task_added", task.id)
            
        logger.info(f"تمت إضافة مهمة جديدة: {task.title} (المعرف: {task.id})")
        return task.id

    def update_task(self, task_id: str, update_data: Dict) -> bool:
        """تحديث مهمة موجودة
        
        المعاملات:
            task_id (str): معرف المهمة
            update_data (Dict): بيانات التحديث
            
        الإرجاع:
            bool: True إذا تم التحديث بنجاح، وإلا False
        """
        # التحقق من وجود المهمة
        if task_id not in self.tasks:
            logger.warning(f"محاولة تحديث مهمة غير موجودة: {task_id}")
            return False
            
        task = self.tasks[task_id]
        old_status = task.status
        
        # تحديث الحقول
        for key, value in update_data.items():
            if key == "title":
                task.title = value
            elif key == "description":
                task.description = value
            elif key == "priority":
                task.priority = value
            elif key == "due_date":
                task.due_date = value
            elif key == "tags":
                task.tags = value
            elif key == "assignee":
                task.assignee = value
            elif key == "status":
                task.status = value
                # إذا تم تغيير الحالة إلى "مكتملة"، تحديث تاريخ الإكمال والتقدم
                if value == "completed" and old_status != "completed":
                    task.completed_at = datetime.now()
                    task.progress = 100
                elif value != "completed" and old_status == "completed":
                    task.completed_at = None
            elif key == "progress":
                task.progress = value
                # تحديث الحالة بناءً على التقدم
                if value == 100 and task.status != "completed":
                    task.status = "completed"
                    task.completed_at = datetime.now()
                elif value > 0 and value < 100 and task.status == "pending":
                    task.status = "in_progress"
            elif key == "notes":
                task.notes = value
            elif key == "attachments":
                task.attachments = value
                
        # تحديث وقت التحديث
        task.updated_at = datetime.now()
        
        # حفظ المهام إذا كان الحفظ التلقائي مفعلاً
        if self.auto_save:
            self._save_tasks()
            
        # إرسال إشعار بتحديث المهمة
        self._notify("task_updated", task_id)
            
        logger.info(f"تم تحديث المهمة: {task.title} (المعرف: {task.id})")
        return True

    def delete_task(self, task_id: str, delete_subtasks: bool = True) -> bool:
        """حذف مهمة
        
        المعاملات:
            task_id (str): معرف المهمة
            delete_subtasks (bool): ما إذا كان يجب حذف المهام الفرعية أيضًا
            
        الإرجاع:
            bool: True إذا تم الحذف بنجاح، وإلا False
        """
        # التحقق من وجود المهمة
        if task_id not in self.tasks:
            logger.warning(f"محاولة حذف مهمة غير موجودة: {task_id}")
            return False
            
        task = self.tasks[task_id]
        
        # حذف المهام الفرعية إذا كان مطلوبًا
        if delete_subtasks:
            for subtask_id in task.subtasks[:]:  # نسخة من القائمة لتجنب التعديل أثناء التكرار
                self.delete_task(subtask_id, delete_subtasks=True)
        else:
            # تحديث المهام الفرعية لتكون مهام رئيسية
            for subtask_id in task.subtasks:
                if subtask_id in self.tasks:
                    subtask = self.tasks[subtask_id]
                    subtask.parent_id = None
                    subtask.updated_at = datetime.now()
        
        # إذا كانت مهمة فرعية، إزالتها من المهمة الأم
        if task.parent_id and task.parent_id in self.tasks:
            parent_task = self.tasks[task.parent_id]
            if task_id in parent_task.subtasks:
                parent_task.subtasks.remove(task_id)
                parent_task.updated_at = datetime.now()
        
        # حذف المهمة من القاموس
        deleted_task = self.tasks.pop(task_id)
        
        # حفظ المهام إذا كان الحفظ التلقائي مفعلاً
        if self.auto_save:
            self._save_tasks()
            
        # إرسال إشعار بحذف المهمة
        self._notify("task_deleted", task_id)
            
        logger.info(f"تم حذف المهمة: {deleted_task.title} (المعرف: {task_id})")
        return True

    def get_task(self, task_id: str) -> Optional[Dict]:
        """الحصول على مهمة بمعرفها
        
        المعاملات:
            task_id (str): معرف المهمة
            
        الإرجاع:
            Optional[Dict]: بيانات المهمة، أو None إذا لم تكن موجودة
        """
        if task_id in self.tasks:
            return self.tasks[task_id].to_dict()
        return None

    def get_all_tasks(self, include_completed: bool = True) -> List[Dict]:
        """الحصول على جميع المهام
        
        المعاملات:
            include_completed (bool): ما إذا كان يجب تضمين المهام المكتملة
            
        الإرجاع:
            List[Dict]: قائمة بجميع المهام
        """
        tasks = []
        for task in self.tasks.values():
            if include_completed or task.status != "completed":
                tasks.append(task.to_dict())
        return tasks

    def get_root_tasks(self, include_completed: bool = True) -> List[Dict]:
        """الحصول على المهام الرئيسية (غير الفرعية)
        
        المعاملات:
            include_completed (bool): ما إذا كان يجب تضمين المهام المكتملة
            
        الإرجاع:
            List[Dict]: قائمة بالمهام الرئيسية
        """
        root_tasks = []
        for task in self.tasks.values():
            if task.parent_id is None and (include_completed or task.status != "completed"):
                root_tasks.append(task.to_dict())
        return root_tasks

    def get_subtasks(self, task_id: str, include_completed: bool = True) -> List[Dict]:
        """الحصول على المهام الفرعية لمهمة معينة
        
        المعاملات:
            task_id (str): معرف المهمة الأم
            include_completed (bool): ما إذا كان يجب تضمين المهام المكتملة
            
        الإرجاع:
            List[Dict]: قائمة بالمهام الفرعية
        """
        if task_id not in self.tasks:
            return []
            
        task = self.tasks[task_id]
        subtasks = []
        
        for subtask_id in task.subtasks:
            if subtask_id in self.tasks:
                subtask = self.tasks[subtask_id]
                if include_completed or subtask.status != "completed":
                    subtasks.append(subtask.to_dict())
                    
        return subtasks

    def search_tasks(self, query: Dict) -> List[Dict]:
        """البحث عن المهام
        
        المعاملات:
            query (Dict): معايير البحث
            
        الإرجاع:
            List[Dict]: قائمة بالمهام المطابقة
        """
        results = []
        
        for task in self.tasks.values():
            match = True
            
            # البحث في العنوان والوصف
            if "text" in query:
                text = query["text"].lower()
                if text not in task.title.lower() and text not in task.description.lower():
                    match = False
                    
            # البحث حسب الحالة
            if "status" in query and task.status != query["status"]:
                match = False
                
            # البحث حسب الأولوية
            if "priority" in query and task.priority != query["priority"]:
                match = False
                
            # البحث حسب الوسوم
            if "tag" in query and query["tag"] not in task.tags:
                match = False
                
            # البحث حسب المسؤول
            if "assignee" in query and task.assignee != query["assignee"]:
                match = False
                
            # البحث حسب تاريخ الاستحقاق
            if "due_before" in query and (not task.due_date or task.due_date > query["due_before"]):
                match = False
            if "due_after" in query and (not task.due_date or task.due_date < query["due_after"]):
                match = False
                
            # إذا كانت المهمة مطابقة، إضافتها إلى النتائج
            if match:
                results.append(task.to_dict())
                
        return results

    def get_task_hierarchy(self, root_task_id: str = None, include_completed: bool = True) -> List[Dict]:
        """الحصول على التسلسل الهرمي للمهام
        
        المعاملات:
            root_task_id (str): معرف المهمة الجذرية (اختياري)
            include_completed (bool): ما إذا كان يجب تضمين المهام المكتملة
            
        الإرجاع:
            List[Dict]: قائمة بالمهام مع المهام الفرعية المضمنة
        """
        if root_task_id:
            # الحصول على التسلسل الهرمي لمهمة معينة
            if root_task_id not in self.tasks:
                return []
                
            root_task = self.tasks[root_task_id]
            if not include_completed and root_task.status == "completed":
                return []
                
            return [self._build_task_hierarchy(root_task, include_completed)]
        else:
            # الحصول على التسلسل الهرمي لجميع المهام الرئيسية
            hierarchy = []
            
            for task in self.tasks.values():
                if task.parent_id is None and (include_completed or task.status != "completed"):
                    hierarchy.append(self._build_task_hierarchy(task, include_completed))
                    
            return hierarchy

    def _build_task_hierarchy(self, task: Task, include_completed: bool) -> Dict:
        """بناء التسلسل الهرمي لمهمة
        
        المعاملات:
            task (Task): المهمة
            include_completed (bool): ما إذا كان يجب تضمين المهام المكتملة
            
        الإرجاع:
            Dict: المهمة مع المهام الفرعية المضمنة
        """
        task_dict = task.to_dict()
        task_dict["children"] = []
        
        for subtask_id in task.subtasks:
            if subtask_id in self.tasks:
                subtask = self.tasks[subtask_id]
                if include_completed or subtask.status != "completed":
                    task_dict["children"].append(self._build_task_hierarchy(subtask, include_completed))
                    
        return task_dict

    def calculate_progress(self, task_id: str) -> int:
        """حساب تقدم المهمة بناءً على المهام الفرعية
        
        المعاملات:
            task_id (str): معرف المهمة
            
        الإرجاع:
            int: نسبة التقدم (0-100)
        """
        if task_id not in self.tasks:
            return 0
            
        task = self.tasks[task_id]
        
        # إذا لم تكن هناك مهام فرعية، إرجاع التقدم المخزن
        if not task.subtasks:
            return task.progress
            
        # حساب متوسط تقدم المهام الفرعية
        total_progress = 0
        count = 0
        
        for subtask_id in task.subtasks:
            if subtask_id in self.tasks:
                # حساب تقدم المهمة الفرعية بشكل متكرر
                subtask_progress = self.calculate_progress(subtask_id)
                total_progress += subtask_progress
                count += 1
                
        # حساب المتوسط
        if count > 0:
            avg_progress = total_progress / count
            
            # تحديث تقدم المهمة
            task.progress = int(avg_progress)
            
            # تحديث حالة المهمة بناءً على التقدم
            if task.progress == 100 and task.status != "completed":
                task.status = "completed"
                task.completed_at = datetime.now()
            elif task.progress > 0 and task.progress < 100 and task.status == "pending":
                task.status = "in_progress"
                
            # تحديث وقت التحديث
            task.updated_at = datetime.now()
            
            # حفظ المهام إذا كان الحفظ التلقائي مفعلاً
            if self.auto_save:
                self._save_tasks()
                
            return task.progress
        else:
            return task.progress

    def update_all_progress(self) -> None:
        """تحديث تقدم جميع المهام"""
        # تحديث المهام الرئيسية أولاً
        for task in self.tasks.values():
            if task.parent_id is None:
                self.calculate_progress(task.id)

    def add_notification_handler(self, handler) -> None:
        """إضافة معالج إشعارات
        
        المعاملات:
            handler: دالة تستقبل نوع الإشعار ومعرف المهمة
        """
        self.notification_handlers.append(handler)

    def _notify(self, notification_type: str, task_id: str) -> None:
        """إرسال إشعار
        
        المعاملات:
            notification_type (str): نوع الإشعار
            task_id (str): معرف المهمة
        """
        for handler in self.notification_handlers:
            try:
                handler(notification_type, task_id)
            except Exception as e:
                logger.error(f"خطأ في معالج الإشعارات: {e}")

    def _start_reminder_thread(self) -> None:
        """بدء خيط التذكير"""
        self.stop_reminder_thread = False
        self.reminder_thread = threading.Thread(target=self._reminder_loop)
        self.reminder_thread.daemon = True
        self.reminder_thread.start()
        logger.debug("تم بدء خيط التذكير")

    def _stop_reminder_thread(self) -> None:
        """إيقاف خيط التذكير"""
        if self.reminder_thread:
            self.stop_reminder_thread = True
            self.reminder_thread.join(timeout=1)
            self.reminder_thread = None
            logger.debug("تم إيقاف خيط التذكير")

    def _reminder_loop(self) -> None:
        """حلقة التذكير"""
        while not self.stop_reminder_thread:
            try:
                self._check_due_tasks()
            except Exception as e:
                logger.error(f"خطأ في حلقة التذكير: {e}")
                
            # انتظار قبل التحقق التالي
            for _ in range(60):  # التحقق كل دقيقة
                if self.stop_reminder_thread:
                    break
                time.sleep(1)

    def _check_due_tasks(self) -> None:
        """التحقق من المهام المستحقة"""
        now = datetime.now()
        
        for task in self.tasks.values():
            # التحقق فقط من المهام غير المكتملة وغير الملغاة
            if task.status not in ["completed", "cancelled"] and task.due_date:
                # التحقق من المهام المستحقة خلال الساعة القادمة
                if now <= task.due_date <= now + timedelta(hours=1):
                    # إرسال إشعار بالمهمة المستحقة
                    self._notify("task_due_soon", task.id)
                    logger.debug(f"المهمة ستستحق قريبًا: {task.title} (المعرف: {task.id})")
                # التحقق من المهام المتأخرة
                elif task.due_date < now:
                    # إرسال إشعار بالمهمة المتأخرة
                    self._notify("task_overdue", task.id)
                    logger.debug(f"المهمة متأخرة: {task.title} (المعرف: {task.id})")

    def generate_report(self, report_type: str = "summary") -> Dict:
        """إنشاء تقرير عن المهام
        
        المعاملات:
            report_type (str): نوع التقرير ("summary", "detailed", "progress")
            
        الإرجاع:
            Dict: بيانات التقرير
        """
        if report_type == "summary":
            return self._generate_summary_report()
        elif report_type == "detailed":
            return self._generate_detailed_report()
        elif report_type == "progress":
            return self._generate_progress_report()
        else:
            logger.warning(f"نوع تقرير غير معروف: {report_type}")
            return {"error": f"نوع تقرير غير معروف: {report_type}"}

    def _generate_summary_report(self) -> Dict:
        """إنشاء تقرير ملخص
        
        الإرجاع:
            Dict: بيانات التقرير
        """
        # تحديث تقدم جميع المهام
        self.update_all_progress()
        
        # إحصاءات المهام
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks.values() if task.status == "completed")
        in_progress_tasks = sum(1 for task in self.tasks.values() if task.status == "in_progress")
        pending_tasks = sum(1 for task in self.tasks.values() if task.status == "pending")
        cancelled_tasks = sum(1 for task in self.tasks.values() if task.status == "cancelled")
        
        # المهام المستحقة قريبًا
        now = datetime.now()
        due_soon = []
        
        for task in self.tasks.values():
            if task.status not in ["completed", "cancelled"] and task.due_date:
                if now <= task.due_date <= now + timedelta(days=3):
                    due_soon.append(task.to_dict())
                    
        # المهام المتأخرة
        overdue = []
        
        for task in self.tasks.values():
            if task.status not in ["completed", "cancelled"] and task.due_date:
                if task.due_date < now:
                    overdue.append(task.to_dict())
                    
        # المهام ذات الأولوية العالية
        high_priority = []
        
        for task in self.tasks.values():
            if task.status not in ["completed", "cancelled"] and task.priority == 3:
                high_priority.append(task.to_dict())
                
        # التقدم الإجمالي
        overall_progress = 0
        if total_tasks > 0:
            overall_progress = sum(task.progress for task in self.tasks.values()) / total_tasks
            
        return {
            "report_type": "summary",
            "generated_at": datetime.now().isoformat(),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "pending_tasks": pending_tasks,
            "cancelled_tasks": cancelled_tasks,
            "overall_progress": overall_progress,
            "due_soon": due_soon,
            "overdue": overdue,
            "high_priority": high_priority
        }

    def _generate_detailed_report(self) -> Dict:
        """إنشاء تقرير مفصل
        
        الإرجاع:
            Dict: بيانات التقرير
        """
        # تحديث تقدم جميع المهام
        self.update_all_progress()
        
        # الحصول على التسلسل الهرمي للمهام
        task_hierarchy = self.get_task_hierarchy(include_completed=True)
        
        # إحصاءات حسب الوسوم
        tag_stats = {}
        
        for task in self.tasks.values():
            for tag in task.tags:
                if tag not in tag_stats:
                    tag_stats[tag] = {
                        "total": 0,
                        "completed": 0,
                        "in_progress": 0,
                        "pending": 0,
                        "cancelled": 0
                    }
                    
                tag_stats[tag]["total"] += 1
                tag_stats[tag][task.status] += 1
                
        # إحصاءات حسب المسؤولين
        assignee_stats = {}
        
        for task in self.tasks.values():
            if task.assignee:
                if task.assignee not in assignee_stats:
                    assignee_stats[task.assignee] = {
                        "total": 0,
                        "completed": 0,
                        "in_progress": 0,
                        "pending": 0,
                        "cancelled": 0
                    }
                    
                assignee_stats[task.assignee]["total"] += 1
                assignee_stats[task.assignee][task.status] += 1
                
        return {
            "report_type": "detailed",
            "generated_at": datetime.now().isoformat(),
            "task_hierarchy": task_hierarchy,
            "tag_stats": tag_stats,
            "assignee_stats": assignee_stats
        }

    def _generate_progress_report(self) -> Dict:
        """إنشاء تقرير التقدم
        
        الإرجاع:
            Dict: بيانات التقرير
        """
        # تحديث تقدم جميع المهام
        self.update_all_progress()
        
        # تقدم المهام الرئيسية
        root_tasks_progress = []
        
        for task in self.tasks.values():
            if task.parent_id is None:
                root_tasks_progress.append({
                    "id": task.id,
                    "title": task.title,
                    "progress": task.progress,
                    "status": task.status,
                    "subtasks_count": len(task.subtasks)
                })
                
        # تقدم المهام حسب الوسوم
        tag_progress = {}
        
        for task in self.tasks.values():
            for tag in task.tags:
                if tag not in tag_progress:
                    tag_progress[tag] = {
                        "total_tasks": 0,
                        "total_progress": 0
                    }
                    
                tag_progress[tag]["total_tasks"] += 1
                tag_progress[tag]["total_progress"] += task.progress
                
        # حساب متوسط التقدم لكل وسم
        for tag, stats in tag_progress.items():
            if stats["total_tasks"] > 0:
                stats["average_progress"] = stats["total_progress"] / stats["total_tasks"]
            else:
                stats["average_progress"] = 0
                
        # تقدم المهام حسب المسؤولين
        assignee_progress = {}
        
        for task in self.tasks.values():
            if task.assignee:
                if task.assignee not in assignee_progress:
                    assignee_progress[task.assignee] = {
                        "total_tasks": 0,
                        "total_progress": 0
                    }
                    
                assignee_progress[task.assignee]["total_tasks"] += 1
                assignee_progress[task.assignee]["total_progress"] += task.progress
                
        # حساب متوسط التقدم لكل مسؤول
        for assignee, stats in assignee_progress.items():
            if stats["total_tasks"] > 0:
                stats["average_progress"] = stats["total_progress"] / stats["total_tasks"]
            else:
                stats["average_progress"] = 0
                
        return {
            "report_type": "progress",
            "generated_at": datetime.now().isoformat(),
            "root_tasks_progress": root_tasks_progress,
            "tag_progress": tag_progress,
            "assignee_progress": assignee_progress
        }

    def _load_tasks(self) -> None:
        """تحميل المهام من الملف"""
        if not os.path.exists(self.data_file):
            logger.info(f"ملف المهام غير موجود: {self.data_file}")
            return
            
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
                
            self.tasks = {}
            for task_data in tasks_data:
                task = Task.from_dict(task_data)
                self.tasks[task.id] = task
                
            logger.info(f"تم تحميل {len(self.tasks)} مهمة من الملف")
        except Exception as e:
            logger.error(f"فشل في تحميل المهام من الملف: {e}")

    def _save_tasks(self) -> None:
        """حفظ المهام في الملف"""
        try:
            tasks_data = [task.to_dict() for task in self.tasks.values()]
            
            # إنشاء مجلد البيانات إذا لم يكن موجودًا
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, ensure_ascii=False, indent=2)
                
            logger.debug(f"تم حفظ {len(self.tasks)} مهمة في الملف")
        except Exception as e:
            logger.error(f"فشل في حفظ المهام في الملف: {e}")

    def __del__(self):
        """المنظف"""
        # إيقاف خيط التذكير
        self._stop_reminder_thread()
        
        # حفظ المهام
        if self.auto_save:
            self._save_tasks()

# مثال للاستخدام (للتجربة)
if __name__ == "__main__":
    # إعداد سجل بسيط للعرض
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # تكوين وهمي
    dummy_config = {
        "task_manager": {
            "data_file": "/tmp/tasks.json",
            "auto_save": True,
            "enable_reminders": False
        }
    }
    
    # تهيئة مدير المهام
    task_manager = TaskManager(dummy_config)
    
    # إضافة بعض المهام للتجربة
    print("\n--- إضافة مهام للتجربة ---")
    
    # مهمة رئيسية 1
    task1_id = task_manager.add_task({
        "title": "تطوير نظام تحليل الصور",
        "description": "تطوير نظام متكامل لتحليل الصور الزراعية",
        "priority": 3,
        "tags": ["تطوير", "صور"]
    })
    print(f"تمت إضافة المهمة الرئيسية 1: {task1_id}")
    
    # مهام فرعية للمهمة 1
    subtask1_id = task_manager.add_task({
        "title": "تطوير وحدة التقسيم",
        "description": "تطوير وحدة لتقسيم الصور إلى مناطق",
        "parent_id": task1_id,
        "priority": 2,
        "tags": ["تطوير", "صور", "تقسيم"]
    })
    print(f"تمت إضافة المهمة الفرعية 1: {subtask1_id}")
    
    subtask2_id = task_manager.add_task({
        "title": "تطوير وحدة استخراج الميزات",
        "description": "تطوير وحدة لاستخراج الميزات من الصور المقسمة",
        "parent_id": task1_id,
        "priority": 2,
        "tags": ["تطوير", "صور", "ميزات"]
    })
    print(f"تمت إضافة المهمة الفرعية 2: {subtask2_id}")
    
    # مهمة رئيسية 2
    task2_id = task_manager.add_task({
        "title": "تطوير نظام البحث",
        "description": "تطوير نظام للبحث عن المعلومات الزراعية",
        "priority": 2,
        "tags": ["تطوير", "بحث"]
    })
    print(f"تمت إضافة المهمة الرئيسية 2: {task2_id}")
    
    # تحديث حالة بعض المهام
    print("\n--- تحديث حالة المهام ---")
    
    task_manager.update_task(subtask1_id, {"status": "completed"})
    print(f"تم تحديث حالة المهمة {subtask1_id} إلى 'مكتملة'")
    
    task_manager.update_task(subtask2_id, {"progress": 50})
    print(f"تم تحديث تقدم المهمة {subtask2_id} إلى 50%")
    
    # حساب تقدم المهام الرئيسية
    print("\n--- حساب تقدم المهام الرئيسية ---")
    
    task1_progress = task_manager.calculate_progress(task1_id)
    print(f"تقدم المهمة {task1_id}: {task1_progress}%")
    
    task2_progress = task_manager.calculate_progress(task2_id)
    print(f"تقدم المهمة {task2_id}: {task2_progress}%")
    
    # البحث عن المهام
    print("\n--- البحث عن المهام ---")
    
    image_tasks = task_manager.search_tasks({"tag": "صور"})
    print(f"تم العثور على {len(image_tasks)} مهمة بوسم 'صور'")
    
    # إنشاء تقرير ملخص
    print("\n--- إنشاء تقرير ملخص ---")
    
    summary_report = task_manager.generate_report("summary")
    print(f"إجمالي المهام: {summary_report['total_tasks']}")
    print(f"المهام المكتملة: {summary_report['completed_tasks']}")
    print(f"المهام قيد التقدم: {summary_report['in_progress_tasks']}")
    print(f"المهام المعلقة: {summary_report['pending_tasks']}")
    print(f"التقدم الإجمالي: {summary_report['overall_progress']:.2f}%")
    
    # الحصول على التسلسل الهرمي للمهام
    print("\n--- الحصول على التسلسل الهرمي للمهام ---")
    
    hierarchy = task_manager.get_task_hierarchy()
    print(f"عدد المهام الرئيسية: {len(hierarchy)}")
    for root_task in hierarchy:
        print(f"المهمة الرئيسية: {root_task['title']}")
        print(f"  عدد المهام الفرعية: {len(root_task['children'])}")
        for child in root_task['children']:
            print(f"  - {child['title']} (الحالة: {child['status']}, التقدم: {child['progress']}%)")
