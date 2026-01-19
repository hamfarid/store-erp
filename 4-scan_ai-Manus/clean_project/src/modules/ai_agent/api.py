# File: /home/ubuntu/clean_project/src/modules/ai_agent/api.py
"""
مسار الملف: /home/ubuntu/clean_project/src/modules/ai_agent/api.py

واجهة برمجة تطبيقات الوكلاء الذكيين
توفر نقاط نهاية لإدارة الوكلاء الذكيين والتفاعل معهم
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Any, Optional
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/agents")
async def get_all_agents():
    """الحصول على جميع الوكلاء الذكيين"""
    try:
        return {
            "agents": [
                {
                    "id": "agent_main",
                    "name": "الوكيل الرئيسي",
                    "type": "main_coordinator",
                    "status": "active",
                    "capabilities": [
                        "task_coordination",
                        "resource_management", 
                        "decision_making"
                    ],
                    "performance": {
                        "tasks_completed": 1250,
                        "success_rate": 98.5,
                        "average_response_time": 0.3
                    },
                    "last_activity": "2025-06-14T10:55:00Z"
                },
                {
                    "id": "agent_diagnosis",
                    "name": "وكيل التشخيص",
                    "type": "specialist",
                    "status": "active",
                    "capabilities": [
                        "disease_detection",
                        "image_analysis",
                        "treatment_recommendation"
                    ],
                    "performance": {
                        "tasks_completed": 856,
                        "success_rate": 94.2,
                        "average_response_time": 0.8
                    },
                    "last_activity": "2025-06-14T10:52:00Z"
                },
                {
                    "id": "agent_monitor",
                    "name": "وكيل المراقبة",
                    "type": "monitoring",
                    "status": "active",
                    "capabilities": [
                        "system_monitoring",
                        "error_detection",
                        "performance_analysis"
                    ],
                    "performance": {
                        "tasks_completed": 2340,
                        "success_rate": 99.1,
                        "average_response_time": 0.1
                    },
                    "last_activity": "2025-06-14T10:56:00Z"
                }
            ],
            "total": 3,
            "active": 3,
            "inactive": 0
        }
    except Exception as e:
        logger.error(f"خطأ في الحصول على الوكلاء: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الخادم")

@router.get("/agents/{agent_id}")
async def get_agent_details(agent_id: str):
    """الحصول على تفاصيل وكيل محدد"""
    try:
        # محاكاة البحث عن الوكيل
        agent = {
            "id": agent_id,
            "name": "وكيل التشخيص",
            "type": "specialist",
            "status": "active",
            "description": "وكيل متخصص في تشخيص الأمراض النباتية",
            "capabilities": [
                "disease_detection",
                "image_analysis", 
                "treatment_recommendation",
                "crop_identification"
            ],
            "configuration": {
                "model_version": "v2.1",
                "confidence_threshold": 0.85,
                "max_concurrent_tasks": 5,
                "timeout_seconds": 30
            },
            "performance_metrics": {
                "total_tasks": 856,
                "completed_tasks": 806,
                "failed_tasks": 12,
                "pending_tasks": 38,
                "success_rate": 94.2,
                "average_response_time": 0.8,
                "peak_response_time": 2.1,
                "uptime_percentage": 99.7
            },
            "recent_activities": [
                {
                    "task_id": "task_001",
                    "type": "diagnosis",
                    "status": "completed",
                    "timestamp": "2025-06-14T10:52:00Z",
                    "duration": 0.7
                },
                {
                    "task_id": "task_002",
                    "type": "analysis",
                    "status": "completed", 
                    "timestamp": "2025-06-14T10:50:00Z",
                    "duration": 1.2
                }
            ],
            "created_at": "2025-05-01T08:00:00Z",
            "last_updated": "2025-06-14T10:52:00Z"
        }
        
        return agent
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على تفاصيل الوكيل: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الخادم")

@router.post("/agents")
async def create_agent(agent_data: Dict[str, Any]):
    """إنشاء وكيل ذكي جديد"""
    try:
        # التحقق من البيانات المطلوبة
        required_fields = ["name", "type", "capabilities"]
        for field in required_fields:
            if field not in agent_data:
                raise HTTPException(status_code=400, detail=f"الحقل {field} مطلوب")
        
        # إنشاء الوكيل الجديد
        new_agent = {
            "id": f"agent_{agent_data['name'].lower().replace(' ', '_')}",
            "name": agent_data["name"],
            "type": agent_data["type"],
            "status": "initializing",
            "capabilities": agent_data["capabilities"],
            "configuration": agent_data.get("configuration", {}),
            "created_at": "2025-06-14T11:00:00Z"
        }
        
        return {
            "message": "تم إنشاء الوكيل بنجاح",
            "agent": new_agent
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في إنشاء الوكيل: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الخادم")

@router.put("/agents/{agent_id}")
async def update_agent(agent_id: str, update_data: Dict[str, Any]):
    """تحديث إعدادات وكيل"""
    try:
        # محاكاة التحديث
        updated_agent = {
            "id": agent_id,
            "name": update_data.get("name", "وكيل محدث"),
            "status": update_data.get("status", "active"),
            "configuration": update_data.get("configuration", {}),
            "updated_at": "2025-06-14T11:05:00Z"
        }
        
        return {
            "message": "تم تحديث الوكيل بنجاح",
            "agent": updated_agent
        }
        
    except Exception as e:
        logger.error(f"خطأ في تحديث الوكيل: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الخادم")

@router.post("/agents/{agent_id}/tasks")
async def assign_task_to_agent(agent_id: str, task_data: Dict[str, Any]):
    """تعيين مهمة لوكيل محدد"""
    try:
        # التحقق من البيانات المطلوبة
        if "task_type" not in task_data:
            raise HTTPException(status_code=400, detail="نوع المهمة مطلوب")
        
        # إنشاء المهمة
        task = {
            "task_id": f"task_{agent_id}_{len(task_data)}",
            "agent_id": agent_id,
            "task_type": task_data["task_type"],
            "parameters": task_data.get("parameters", {}),
            "status": "assigned",
            "priority": task_data.get("priority", "normal"),
            "created_at": "2025-06-14T11:10:00Z",
            "estimated_duration": task_data.get("estimated_duration", "unknown")
        }
        
        return {
            "message": "تم تعيين المهمة بنجاح",
            "task": task
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في تعيين المهمة: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الخادم")

@router.get("/agents/{agent_id}/tasks")
async def get_agent_tasks(agent_id: str, status: Optional[str] = None):
    """الحصول على مهام وكيل محدد"""
    try:
        # محاكاة المهام
        tasks = [
            {
                "task_id": "task_001",
                "task_type": "diagnosis",
                "status": "completed",
                "priority": "high",
                "created_at": "2025-06-14T10:45:00Z",
                "completed_at": "2025-06-14T10:46:00Z",
                "duration": 1.2
            },
            {
                "task_id": "task_002", 
                "task_type": "analysis",
                "status": "in_progress",
                "priority": "normal",
                "created_at": "2025-06-14T10:50:00Z",
                "estimated_completion": "2025-06-14T10:52:00Z"
            },
            {
                "task_id": "task_003",
                "task_type": "monitoring",
                "status": "pending",
                "priority": "low",
                "created_at": "2025-06-14T10:55:00Z"
            }
        ]
        
        if status:
            tasks = [task for task in tasks if task["status"] == status]
        
        return {
            "agent_id": agent_id,
            "tasks": tasks,
            "total": len(tasks)
        }
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على مهام الوكيل: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الخادم")

@router.post("/agents/{agent_id}/communicate")
async def communicate_with_agent(agent_id: str, message_data: Dict[str, Any]):
    """التواصل مع وكيل محدد"""
    try:
        # التحقق من الرسالة
        if "message" not in message_data:
            raise HTTPException(status_code=400, detail="الرسالة مطلوبة")
        
        # محاكاة الاستجابة
        response = {
            "agent_id": agent_id,
            "message_id": f"msg_{agent_id}_{len(message_data)}",
            "user_message": message_data["message"],
            "agent_response": f"تم استلام رسالتك: {message_data['message']}. كيف يمكنني مساعدتك؟",
            "response_time": 0.5,
            "timestamp": "2025-06-14T11:15:00Z"
        }
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"خطأ في التواصل مع الوكيل: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الخادم")

@router.get("/statistics")
async def get_agents_statistics():
    """الحصول على إحصائيات الوكلاء"""
    try:
        return {
            "total_agents": 3,
            "active_agents": 3,
            "inactive_agents": 0,
            "total_tasks_today": 156,
            "completed_tasks_today": 142,
            "failed_tasks_today": 3,
            "pending_tasks": 11,
            "average_response_time": 0.6,
            "system_load": 45.2,
            "agent_types": [
                {
                    "type": "main_coordinator",
                    "count": 1,
                    "active": 1
                },
                {
                    "type": "specialist",
                    "count": 1,
                    "active": 1
                },
                {
                    "type": "monitoring",
                    "count": 1,
                    "active": 1
                }
            ]
        }
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على إحصائيات الوكلاء: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الخادم")

