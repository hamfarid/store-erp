# File: /home/ubuntu/clean_project/src/integration/api_integration.py

"""
تكامل APIs - ربط الواجهة الأمامية بالخلفية
API Integration - Connect frontend with backend
"""

import logging
from typing import Dict, Any, List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from ..database_models import (
    User, DiagnosisResult, AIModel, ActivityLog, 
    SystemSettings, Report, MemoryEntry
)
from ..services.memory_service import MemoryService
from ..core.config import Settings

logger = logging.getLogger(__name__)

class APIIntegrationService:
    """خدمة تكامل APIs لربط الواجهات"""
    
    def __init__(self, db: Session, settings: Settings):
        self.db = db
        self.settings = settings
        self.memory_service = MemoryService(db)
    
    async def get_dashboard_data(self, user_id: int) -> Dict[str, Any]:
        """
        جلب بيانات لوحة التحكم
        Get dashboard data
        """
        try:
            # إحصائيات عامة
            total_diagnoses = self.db.query(DiagnosisResult).count()
            total_users = self.db.query(User).count()
            total_models = self.db.query(AIModel).count()
            
            # إحصائيات اليوم
            today = datetime.now().date()
            today_diagnoses = self.db.query(DiagnosisResult).filter(
                DiagnosisResult.created_at >= today
            ).count()
            
            # آخر التشخيصات
            recent_diagnoses = self.db.query(DiagnosisResult).order_by(
                DiagnosisResult.created_at.desc()
            ).limit(5).all()
            
            # نشاط المستخدم
            user_activity = self.db.query(ActivityLog).filter(
                ActivityLog.user_id == user_id
            ).order_by(ActivityLog.timestamp.desc()).limit(10).all()
            
            return {
                "statistics": {
                    "total_diagnoses": total_diagnoses,
                    "total_users": total_users,
                    "total_models": total_models,
                    "today_diagnoses": today_diagnoses
                },
                "recent_diagnoses": [
                    {
                        "id": d.id,
                        "disease_name": d.disease_name,
                        "confidence": d.confidence_score,
                        "created_at": d.created_at.isoformat()
                    } for d in recent_diagnoses
                ],
                "user_activity": [
                    {
                        "id": a.id,
                        "action": a.action,
                        "description": a.description,
                        "timestamp": a.timestamp.isoformat()
                    } for a in user_activity
                ]
            }
        except Exception as e:
            logger.error(f"خطأ في جلب بيانات لوحة التحكم: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="فشل في جلب بيانات لوحة التحكم"
            )
    
    async def get_user_management_data(self) -> Dict[str, Any]:
        """
        جلب بيانات إدارة المستخدمين
        Get user management data
        """
        try:
            users = self.db.query(User).all()
            
            # إحصائيات المستخدمين
            active_users = len([u for u in users if u.is_active])
            admin_users = len([u for u in users if u.role == 'admin'])
            expert_users = len([u for u in users if u.role == 'expert'])
            regular_users = len([u for u in users if u.role == 'user'])
            
            return {
                "users": [
                    {
                        "id": u.id,
                        "username": u.username,
                        "email": u.email,
                        "full_name": u.full_name,
                        "role": u.role,
                        "is_active": u.is_active,
                        "created_at": u.created_at.isoformat() if u.created_at else None,
                        "last_login": u.last_login.isoformat() if u.last_login else None
                    } for u in users
                ],
                "statistics": {
                    "total": len(users),
                    "active": active_users,
                    "admin": admin_users,
                    "expert": expert_users,
                    "regular": regular_users
                }
            }
        except Exception as e:
            logger.error(f"خطأ في جلب بيانات المستخدمين: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="فشل في جلب بيانات المستخدمين"
            )
    
    async def get_system_monitoring_data(self) -> Dict[str, Any]:
        """
        جلب بيانات مراقبة النظام
        Get system monitoring data
        """
        try:
            # محاكاة بيانات مراقبة النظام
            # في التطبيق الحقيقي، ستأتي هذه البيانات من خدمات المراقبة
            
            return {
                "system_status": {
                    "overall": "healthy",
                    "last_update": datetime.now().isoformat()
                },
                "metrics": {
                    "cpu": 45,
                    "memory": 62,
                    "disk": 78,
                    "network": 12.5,
                    "network_status": "مستقر"
                },
                "services": [
                    {
                        "name": "api_server",
                        "display_name": "خادم API",
                        "status": "running",
                        "uptime": "5 أيام 12 ساعة",
                        "memory_usage": 256,
                        "cpu_usage": 15
                    },
                    {
                        "name": "database",
                        "display_name": "قاعدة البيانات",
                        "status": "running",
                        "uptime": "5 أيام 12 ساعة",
                        "memory_usage": 512,
                        "cpu_usage": 8
                    },
                    {
                        "name": "ai_service",
                        "display_name": "خدمة الذكاء الاصطناعي",
                        "status": "running",
                        "uptime": "2 أيام 8 ساعات",
                        "memory_usage": 1024,
                        "cpu_usage": 35
                    }
                ]
            }
        except Exception as e:
            logger.error(f"خطأ في جلب بيانات مراقبة النظام: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="فشل في جلب بيانات مراقبة النظام"
            )
    
    async def get_activity_logs(
        self, 
        page: int = 1, 
        limit: int = 20,
        level: Optional[str] = None,
        action: Optional[str] = None,
        user_id: Optional[int] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        جلب سجل الأنشطة مع الفلترة والترقيم
        Get activity logs with filtering and pagination
        """
        try:
            query = self.db.query(ActivityLog)
            
            # تطبيق الفلاتر
            if level:
                query = query.filter(ActivityLog.level == level)
            if action:
                query = query.filter(ActivityLog.action == action)
            if user_id:
                query = query.filter(ActivityLog.user_id == user_id)
            if date_from:
                query = query.filter(ActivityLog.timestamp >= date_from)
            if date_to:
                query = query.filter(ActivityLog.timestamp <= date_to)
            
            # العدد الإجمالي
            total = query.count()
            
            # الترقيم
            offset = (page - 1) * limit
            logs = query.order_by(ActivityLog.timestamp.desc()).offset(offset).limit(limit).all()
            
            return {
                "logs": [
                    {
                        "id": log.id,
                        "timestamp": log.timestamp.isoformat(),
                        "level": log.level,
                        "action": log.action,
                        "user_id": log.user_id,
                        "description": log.description,
                        "ip_address": log.ip_address,
                        "user_agent": log.user_agent,
                        "details": log.details
                    } for log in logs
                ],
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "pages": (total + limit - 1) // limit
                }
            }
        except Exception as e:
            logger.error(f"خطأ في جلب سجل الأنشطة: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="فشل في جلب سجل الأنشطة"
            )
    
    async def create_activity_log(
        self,
        user_id: int,
        action: str,
        description: str,
        level: str = "info",
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> ActivityLog:
        """
        إنشاء سجل نشاط جديد
        Create new activity log
        """
        try:
            log = ActivityLog(
                user_id=user_id,
                action=action,
                description=description,
                level=level,
                ip_address=ip_address,
                user_agent=user_agent,
                details=details,
                timestamp=datetime.now()
            )
            
            self.db.add(log)
            self.db.commit()
            self.db.refresh(log)
            
            return log
        except Exception as e:
            logger.error(f"خطأ في إنشاء سجل النشاط: {e}")
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="فشل في إنشاء سجل النشاط"
            )
    
    async def get_system_settings(self) -> Dict[str, Any]:
        """
        جلب إعدادات النظام
        Get system settings
        """
        try:
            settings = self.db.query(SystemSettings).all()
            
            settings_dict = {}
            for setting in settings:
                settings_dict[setting.key] = {
                    "value": setting.value,
                    "description": setting.description,
                    "category": setting.category,
                    "is_public": setting.is_public
                }
            
            return settings_dict
        except Exception as e:
            logger.error(f"خطأ في جلب إعدادات النظام: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="فشل في جلب إعدادات النظام"
            )
    
    async def update_system_setting(
        self,
        key: str,
        value: str,
        user_id: int
    ) -> SystemSettings:
        """
        تحديث إعداد النظام
        Update system setting
        """
        try:
            setting = self.db.query(SystemSettings).filter(
                SystemSettings.key == key
            ).first()
            
            if not setting:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="الإعداد غير موجود"
                )
            
            old_value = setting.value
            setting.value = value
            setting.updated_at = datetime.now()
            
            self.db.commit()
            self.db.refresh(setting)
            
            # تسجيل النشاط
            await self.create_activity_log(
                user_id=user_id,
                action="settings",
                description=f"تم تحديث الإعداد {key} من {old_value} إلى {value}",
                level="info"
            )
            
            return setting
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"خطأ في تحديث إعداد النظام: {e}")
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="فشل في تحديث إعداد النظام"
            )
    
    async def get_ai_models_data(self) -> Dict[str, Any]:
        """
        جلب بيانات نماذج الذكاء الاصطناعي
        Get AI models data
        """
        try:
            models = self.db.query(AIModel).all()
            
            return {
                "models": [
                    {
                        "id": m.id,
                        "name": m.name,
                        "version": m.version,
                        "status": m.status,
                        "accuracy": m.accuracy,
                        "created_at": m.created_at.isoformat() if m.created_at else None,
                        "last_trained": m.last_trained.isoformat() if m.last_trained else None,
                        "description": m.description
                    } for m in models
                ],
                "statistics": {
                    "total": len(models),
                    "active": len([m for m in models if m.status == 'active']),
                    "training": len([m for m in models if m.status == 'training']),
                    "inactive": len([m for m in models if m.status == 'inactive'])
                }
            }
        except Exception as e:
            logger.error(f"خطأ في جلب بيانات النماذج: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="فشل في جلب بيانات النماذج"
            )
    
    async def validate_api_connection(self) -> Dict[str, Any]:
        """
        التحقق من اتصال APIs
        Validate API connections
        """
        try:
            # اختبار الاتصال بقاعدة البيانات
            db_status = "connected"
            try:
                self.db.execute("SELECT 1")
            except Exception:
                db_status = "disconnected"
            
            # اختبار خدمة الذاكرة
            memory_status = "connected"
            try:
                await self.memory_service.get_memory_stats()
            except Exception:
                memory_status = "disconnected"
            
            # اختبار APIs الأساسية
            api_endpoints = [
                "/api/v1/health",
                "/api/v1/auth/login",
                "/api/v1/diagnosis/analyze",
                "/api/v1/reports/generate",
                "/api/v1/models/list"
            ]
            
            return {
                "database": db_status,
                "memory_service": memory_status,
                "api_endpoints": api_endpoints,
                "status": "healthy" if db_status == "connected" and memory_status == "connected" else "unhealthy",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"خطأ في التحقق من اتصال APIs: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

class FrontendIntegrationHelper:
    """مساعد تكامل الواجهة الأمامية"""
    
    @staticmethod
    def format_api_response(data: Any, success: bool = True, message: str = "") -> Dict[str, Any]:
        """
        تنسيق استجابة API للواجهة الأمامية
        Format API response for frontend
        """
        return {
            "success": success,
            "message": message,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def handle_api_error(error: Exception) -> Dict[str, Any]:
        """
        معالجة أخطاء API
        Handle API errors
        """
        if isinstance(error, HTTPException):
            return {
                "success": False,
                "error": {
                    "code": error.status_code,
                    "message": error.detail
                },
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "error": {
                    "code": 500,
                    "message": "خطأ داخلي في الخادم"
                },
                "timestamp": datetime.now().isoformat()
            }
    
    @staticmethod
    def validate_frontend_request(data: Dict[str, Any], required_fields: List[str]) -> bool:
        """
        التحقق من صحة طلب الواجهة الأمامية
        Validate frontend request
        """
        for field in required_fields:
            if field not in data or data[field] is None:
                return False
        return True

