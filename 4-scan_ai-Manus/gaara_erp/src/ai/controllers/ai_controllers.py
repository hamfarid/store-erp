"""
وحدات التحكم في التكامل مع نظام الذكاء الاصطناعي الزراعي
يحتوي هذا الملف على وحدات التحكم للتكامل مع نظام الذكاء الاصطناعي الزراعي
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, status, UploadFile, File, Form
from fastapi.responses import JSONResponse

from ...core.auth.auth_manager import get_current_user, check_permissions
from ...core.database.db_manager import get_db_manager
from ..services.ai_services import AIIntegrationService
from ..models.ai_models import DiagnosisStatus, BreedingStatus


# إنشاء موجه API للتكامل مع نظام الذكاء الاصطناعي
ai_router = APIRouter(prefix="/api/ai", tags=["الذكاء الاصطناعي"])


# وحدات التحكم في حالة النظام
@ai_router.get("/system/status", response_model=Dict[str, Any])
async def get_system_status(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على حالة نظام الذكاء الاصطناعي"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["ai.system.view"])
    
    # إنشاء خدمة التكامل مع نظام الذكاء الاصطناعي
    ai_service = AIIntegrationService(db_manager)
    
    # الحصول على حالة النظام
    system_status = ai_service.check_system_status()
    
    return {"status": "success", "data": system_status.to_dict()}


@ai_router.get("/models", response_model=Dict[str, Any])
async def get_available_models(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على النماذج المتاحة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["ai.models.view"])
    
    # إنشاء خدمة التكامل مع نظام الذكاء الاصطناعي
    ai_service = AIIntegrationService(db_manager)
    
    # الحصول على النماذج المتاحة
    models = ai_service.get_available_models()
    
    return {
        "status": "success",
        "data": [model.to_dict() for model in models]
    }


# وحدات التحكم في تشخيص الصور
@ai_router.post("/diagnosis", response_model=Dict[str, Any])
async def create_diagnosis_request(
    image: UploadFile = File(...),
    plant_type: str = Form(...),
    description: Optional[str] = Form(None),
    metadata: Optional[str] = Form(None),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء طلب تشخيص جديد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["ai.diagnosis.create"])
    
    # إنشاء خدمة التكامل مع نظام الذكاء الاصطناعي
    ai_service = AIIntegrationService(db_manager)
    
    try:
        # قراءة محتوى الصورة
        image_content = await image.read()
        
        # رفع الصورة
        image_path = ai_service.upload_image(image_content, image.filename)
        
        # إنشاء بيانات الطلب
        request_data = {
            "image_path": image_path,
            "user_id": current_user["user_id"],
            "plant_type": plant_type,
            "description": description
        }
        
        # إضافة البيانات الوصفية إذا تم توفيرها
        if metadata:
            import json
            try:
                request_data["metadata"] = json.loads(metadata)
            except json.JSONDecodeError:
                pass
        
        # إنشاء طلب تشخيص
        diagnosis_request = ai_service.create_diagnosis_request(request_data)
        
        return {"status": "success", "data": diagnosis_request.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء طلب التشخيص: {str(e)}"
        )


@ai_router.post("/diagnosis/{request_id}/submit", response_model=Dict[str, Any])
async def submit_diagnosis_request(
    request_id: str = Path(..., description="معرف طلب التشخيص"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إرسال طلب تشخيص إلى نظام الذكاء الاصطناعي"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["ai.diagnosis.submit"])
    
    # إنشاء خدمة التكامل مع نظام الذكاء الاصطناعي
    ai_service = AIIntegrationService(db_manager)
    
    # التحقق من وجود الطلب
    diagnosis_request = ai_service.get_diagnosis_request(request_id)
    if not diagnosis_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على طلب التشخيص بالمعرف {request_id}"
        )
    
    # التحقق من أن الطلب ينتمي للمستخدم الحالي أو أن المستخدم لديه صلاحيات إدارية
    if diagnosis_request.user_id != current_user["user_id"] and not any(perm in current_user.get("permissions", []) for perm in ["ai.diagnosis.admin", "admin.all"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لإرسال هذا الطلب"
        )
    
    # التحقق من أن الطلب في حالة قيد الانتظار
    if diagnosis_request.status != DiagnosisStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"لا يمكن إرسال الطلب لأنه في حالة {diagnosis_request.status.value}"
        )
    
    # إرسال الطلب
    success = ai_service.submit_diagnosis_request(request_id)
    
    if success:
        return {"status": "success", "message": "تم إرسال طلب التشخيص بنجاح"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="فشل في إرسال طلب التشخيص"
        )


@ai_router.get("/diagnosis/{request_id}", response_model=Dict[str, Any])
async def get_diagnosis_request(
    request_id: str = Path(..., description="معرف طلب التشخيص"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على طلب تشخيص بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["ai.diagnosis.view"])
    
    # إنشاء خدمة التكامل مع نظام الذكاء الاصطناعي
    ai_service = AIIntegrationService(db_manager)
    
    # الحصول على طلب التشخيص
    diagnosis_request = ai_service.get_diagnosis_request(request_id)
    
    if not diagnosis_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على طلب التشخيص بالمعرف {request_id}"
        )
    
    # التحقق من أن الطلب ينتمي للمستخدم الحالي أو أن المستخدم لديه صلاحيات إدارية
    if diagnosis_request.user_id != current_user["user_id"] and not any(perm in current_user.get("permissions", []) for perm in ["ai.diagnosis.admin", "admin.all"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية للوصول إلى هذا الطلب"
        )
    
    return {"status": "success", "data": diagnosis_request.to_dict()}


@ai_router.get("/diagnosis", response_model=Dict[str, Any])
async def get_all_diagnosis_requests(
    user_id: Optional[str] = Query(None, description="معرف المستخدم"),
    status: Optional[str] = Query(None, description="حالة الطلب"),
    plant_type: Optional[str] = Query(None, description="نوع النبات"),
    limit: int = Query(100, description="عدد النتائج"),
    offset: int = Query(0, description="بداية النتائج"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع طلبات التشخيص"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["ai.diagnosis.view"])
    
    # إنشاء خدمة التكامل مع نظام الذكاء الاصطناعي
    ai_service = AIIntegrationService(db_manager)
    
    # التحقق من أن المستخدم يمكنه الوصول إلى طلبات المستخدمين الآخرين
    if user_id and user_id != current_user["user_id"] and not any(perm in current_user.get("permissions", []) for perm in ["ai.diagnosis.admin", "admin.all"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية للوصول إلى طلبات المستخدمين الآخرين"
        )
    
    # إذا لم يتم تحديد معرف المستخدم وليس لدى المستخدم صلاحيات إدارية، استخدم معرف المستخدم الحالي
    if not user_id and not any(perm in current_user.get("permissions", []) for perm in ["ai.diagnosis.admin", "admin.all"]):
        user_id = current_user["user_id"]
    
    # تحويل حالة الطلب إلى نوع DiagnosisStatus إذا تم توفيرها
    diagnosis_status = None
    if status:
        try:
            diagnosis_status = DiagnosisStatus(status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"حالة الطلب غير صالحة: {status}"
            )
    
    # الحصول على طلبات التشخيص
    diagnosis_requests, total = ai_service.get_all_diagnosis_requests(
        user_id=user_id,
        status=diagnosis_status,
        plant_type=plant_type,
        limit=limit,
        offset=offset
    )
    
    return {
        "status": "success",
        "data": {
            "requests": [request.to_dict() for request in diagnosis_requests],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }


@ai_router.get("/diagnosis/results/{result_id}", response_model=Dict[str, Any])
async def get_diagnosis_result(
    result_id: str = Path(..., description="معرف نتيجة التشخيص"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على نتيجة تشخيص بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["ai.diagnosis.view"])
    
    # إنشاء خدمة التكامل مع نظام الذكاء الاصطناعي
    ai_service = AIIntegrationService(db_manager)
    
    # الحصول على نتيجة التشخيص
    diagnosis_result = ai_service.get_diagnosis_result(result_id)
    
    if not diagnosis_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على نتيجة التشخيص بالمعرف {result_id}"
        )
    
    # الحصول على طلب التشخيص للتحقق من الصلاحيات
    diagnosis_request = ai_service.get_diagnosis_request(diagnosis_result.request_id)
    
    if not diagnosis_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على طلب التشخيص المرتبط بالنتيجة"
        )
    
    # التحقق من أن الطلب ينتمي للمستخدم الحالي أو أن المستخدم لديه صلاحيات إدارية
    if diagnosis_request.user_id != current_user["user_id"] and not any(perm in current_user.get("permissions", []) for perm in ["ai.diagnosis.admin", "admin.all"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية للوصول إلى هذه النتيجة"
        )
    
    return {"status": "success", "data": diagnosis_result.to_dict()}


@ai_router.get("/diagnosis/{request_id}/results", response_model=Dict[str, Any])
async def get_diagnosis_results_by_request(
    request_id: str = Path(..., description="معرف طلب التشخيص"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على نتائج التشخيص بواسطة معرف الطلب"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["ai.diagnosis.view"])
    
    # إنشاء خدمة التكامل مع نظام الذكاء الاصطناعي
    ai_service = AIIntegrationService(db_manager)
    
    # الحصول على طلب التشخيص للتحقق من الصلاحيات
    diagnosis_request = ai_service.get_diagnosis_request(request_id)
    
    if not diagnosis_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على طلب التشخيص بالمعرف {request_id}"
        )
    
    # التحقق من أن الطلب ينتمي للمستخدم الحالي أو أن المستخدم لديه صلاحيات إدارية
    if diagnosis_request.user_id != current_user["user_id"] and not any(perm in current_user.get("permissions", []) for perm in ["ai.diagnosis.admin", "admin.all"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية للوصول إلى نتائج هذا الطلب"
        )
    
    # الحصول على نتائج التشخيص
    diagnosis_results = ai_service.get_diagnosis_results_by_request(request_id)
    
    return {
        "status": "success",
        "data": [result.to_dict() for result in diagnosis_results]
    }


# وحدات التحكم في التهجين
@ai_router.post("/breeding", response_model=Dict[str, Any])
async def create_breeding_request(
    breeding_data: Dict[str, Any] = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء طلب تهجين جديد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["ai.breeding.create"])
    
    # إضافة معرف المستخدم
    breeding_data["user_id"] = current_user["user_id"]
    
    # إنشاء خدمة التكامل مع نظام الذكاء الاصطناعي
    ai_service = AIIntegrationService(db_manager)
    
    try:
        # إنشاء طلب تهجين
        breeding_request = ai_service.create_breeding_request(breeding_data)
        
        return {"status": "success", "data": breeding_request.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء طلب التهجين: {str(e)}"
        )


@ai_router.post("/breeding/{request_id}/submit", response_model=Dict[str, Any])
async def submit_breeding_request(
    request_id: str = Path(..., description="معرف طلب التهجين"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إرسال طلب تهجين إلى نظام الذكاء الاصطناعي"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["ai.breeding.submit"])
    
    # إنشاء خدمة التكامل مع نظام الذكاء الاصطناعي
    ai_service = AIIntegrationService(db_manager)
    
    # التحقق من وجود الطلب
    breeding_request = ai_service.get_breeding_request(request_id)
    if not breeding_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على طلب التهجين بالمعرف {request_id}"
        )
    
    # التحقق من أن الطلب ينتمي للمستخدم الحالي أو أن المستخدم لديه صلاحيات إدارية
    if breeding_request.user_id != current_user["user_id"] and not any(perm in current_user.get("permissions", []) for perm in ["ai.breeding.admin", "admin.all"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية لإرسال هذا الطلب"
        )
    
    # التحقق من أن الطلب في حالة قيد الانتظار
    if breeding_request.status != BreedingStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"لا يمكن إرسال الطلب لأنه في حالة {breeding_request.status.value}"
        )
    
    # إرسال الطلب
    success = ai_service.submit_breeding_request(request_id)
    
    if success:
        return {"status": "success", "message": "تم إرسال طلب التهجين بنجاح"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="فشل في إرسال طلب التهجين"
        )


@ai_router.get("/breeding/{request_id}", response_model=Dict[str, Any])
async def get_breeding_request(
    request_id: str = Path(..., description="معرف طلب التهجين"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على طلب تهجين بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["ai.breeding.view"])
    
    # إنشاء خدمة التكامل مع نظام الذكاء الاصطناعي
    ai_service = AIIntegrationService(db_manager)
    
    # الحصول على طلب التهجين
    breeding_request = ai_service.get_breeding_request(request_id)
    
    if not breeding_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على طلب التهجين بالمعرف {request_id}"
        )
    
    # التحقق من أن الطلب ينتمي للمستخدم الحالي أو أن المستخدم لديه صلاحيات إدارية
    if breeding_request.user_id != current_user["user_id"] and not any(perm in current_user.get("permissions", []) for perm in ["ai.breeding.admin", "admin.all"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية للوصول إلى هذا الطلب"
        )
    
    return {"status": "success", "data": breeding_request.to_dict()}


@ai_router.get("/breeding", response_model=Dict[str, Any])
async def get_all_breeding_requests(
    user_id: Optional[str] = Query(None, description="معرف المستخدم"),
    status: Optional[str] = Query(None, description="حالة الطلب"),
    limit: int = Query(100, description="عدد النتائج"),
    offset: int = Query(0, description="بداية النتائج"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع طلبات التهجين"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["ai.breeding.view"])
    
    # إنشاء خدمة التكامل مع نظام الذكاء الاصطناعي
    ai_service = AIIntegrationService(db_manager)
    
    # التحقق من أن المستخدم يمكنه الوصول إلى طلبات المستخدمين الآخرين
    if user_id and user_id != current_user["user_id"] and not any(perm in current_user.get("permissions", []) for perm in ["ai.breeding.admin", "admin.all"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية للوصول إلى طلبات المستخدمين الآخرين"
        )
    
    # إذا لم يتم تحديد معرف المستخدم وليس لدى المستخدم صلاحيات إدارية، استخدم معرف المستخدم الحالي
    if not user_id and not any(perm in current_user.get("permissions", []) for perm in ["ai.breeding.admin", "admin.all"]):
        user_id = current_user["user_id"]
    
    # تحويل حالة الطلب إلى نوع BreedingStatus إذا تم توفيرها
    breeding_status = None
    if status:
        try:
            breeding_status = BreedingStatus(status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"حالة الطلب غير صالحة: {status}"
            )
    
    # الحصول على طلبات التهجين
    breeding_requests, total = ai_service.get_all_breeding_requests(
        user_id=user_id,
        status=breeding_status,
        limit=limit,
        offset=offset
    )
    
    return {
        "status": "success",
        "data": {
            "requests": [request.to_dict() for request in breeding_requests],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }


@ai_router.get("/breeding/{request_id}/status", response_model=Dict[str, Any])
async def check_breeding_status(
    request_id: str = Path(..., description="معرف طلب التهجين"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """التحقق من حالة طلب تهجين"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["ai.breeding.view"])
    
    # إنشاء خدمة التكامل مع نظام الذكاء الاصطناعي
    ai_service = AIIntegrationService(db_manager)
    
    # التحقق من وجود الطلب
    breeding_request = ai_service.get_breeding_request(request_id)
    if not breeding_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على طلب التهجين بالمعرف {request_id}"
        )
    
    # التحقق من أن الطلب ينتمي للمستخدم الحالي أو أن المستخدم لديه صلاحيات إدارية
    if breeding_request.user_id != current_user["user_id"] and not any(perm in current_user.get("permissions", []) for perm in ["ai.breeding.admin", "admin.all"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية للوصول إلى هذا الطلب"
        )
    
    # التحقق من حالة الطلب
    status_result = ai_service.check_breeding_status(request_id)
    
    if not status_result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=status_result.get("error", "فشل في التحقق من حالة الطلب")
        )
    
    return {"status": "success", "data": status_result}


@ai_router.get("/breeding/results/{result_id}", response_model=Dict[str, Any])
async def get_breeding_result(
    result_id: str = Path(..., description="معرف نتيجة التهجين"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على نتيجة تهجين بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["ai.breeding.view"])
    
    # إنشاء خدمة التكامل مع نظام الذكاء الاصطناعي
    ai_service = AIIntegrationService(db_manager)
    
    # الحصول على نتيجة التهجين
    breeding_result = ai_service.get_breeding_result(result_id)
    
    if not breeding_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على نتيجة التهجين بالمعرف {result_id}"
        )
    
    # الحصول على طلب التهجين للتحقق من الصلاحيات
    breeding_request = ai_service.get_breeding_request(breeding_result.request_id)
    
    if not breeding_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على طلب التهجين المرتبط بالنتيجة"
        )
    
    # التحقق من أن الطلب ينتمي للمستخدم الحالي أو أن المستخدم لديه صلاحيات إدارية
    if breeding_request.user_id != current_user["user_id"] and not any(perm in current_user.get("permissions", []) for perm in ["ai.breeding.admin", "admin.all"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية للوصول إلى هذه النتيجة"
        )
    
    return {"status": "success", "data": breeding_result.to_dict()}


@ai_router.get("/breeding/{request_id}/results", response_model=Dict[str, Any])
async def get_breeding_results_by_request(
    request_id: str = Path(..., description="معرف طلب التهجين"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على نتائج التهجين بواسطة معرف الطلب"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["ai.breeding.view"])
    
    # إنشاء خدمة التكامل مع نظام الذكاء الاصطناعي
    ai_service = AIIntegrationService(db_manager)
    
    # الحصول على طلب التهجين للتحقق من الصلاحيات
    breeding_request = ai_service.get_breeding_request(request_id)
    
    if not breeding_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على طلب التهجين بالمعرف {request_id}"
        )
    
    # التحقق من أن الطلب ينتمي للمستخدم الحالي أو أن المستخدم لديه صلاحيات إدارية
    if breeding_request.user_id != current_user["user_id"] and not any(perm in current_user.get("permissions", []) for perm in ["ai.breeding.admin", "admin.all"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ليس لديك صلاحية للوصول إلى نتائج هذا الطلب"
        )
    
    # الحصول على نتائج التهجين
    breeding_results = ai_service.get_breeding_results_by_request(request_id)
    
    return {
        "status": "success",
        "data": [result.to_dict() for result in breeding_results]
    }


# وحدات التحكم في مزامنة البيانات
@ai_router.post("/data/sync/{data_type}", response_model=Dict[str, Any])
async def sync_data_to_ai_system(
    data_type: str = Path(..., description="نوع البيانات"),
    data: List[Dict[str, Any]] = Body(..., description="البيانات المراد مزامنتها"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """مزامنة البيانات إلى نظام الذكاء الاصطناعي"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["ai.data.sync"])
    
    # التحقق من نوع البيانات
    valid_data_types = ["plants", "diseases", "varieties", "treatments", "soil_types", "nutrients"]
    if data_type not in valid_data_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"نوع البيانات غير صالح. الأنواع الصالحة هي: {', '.join(valid_data_types)}"
        )
    
    # إنشاء خدمة التكامل مع نظام الذكاء الاصطناعي
    ai_service = AIIntegrationService(db_manager)
    
    # مزامنة البيانات
    sync_job = ai_service.sync_data_to_ai_system(data_type, data)
    
    return {"status": "success", "data": sync_job.to_dict()}


@ai_router.get("/data/sync/jobs", response_model=Dict[str, Any])
async def get_all_data_sync_jobs(
    data_type: Optional[str] = Query(None, description="نوع البيانات"),
    status: Optional[str] = Query(None, description="حالة المهمة"),
    limit: int = Query(100, description="عدد النتائج"),
    offset: int = Query(0, description="بداية النتائج"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع مهام مزامنة البيانات"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["ai.data.view"])
    
    # إنشاء خدمة التكامل مع نظام الذكاء الاصطناعي
    ai_service = AIIntegrationService(db_manager)
    
    # الحصول على مهام مزامنة البيانات
    sync_jobs, total = ai_service.get_all_data_sync_jobs(
        data_type=data_type,
        status=status,
        limit=limit,
        offset=offset
    )
    
    return {
        "status": "success",
        "data": {
            "jobs": [job.to_dict() for job in sync_jobs],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }


@ai_router.get("/data/sync/jobs/{job_id}", response_model=Dict[str, Any])
async def get_data_sync_job(
    job_id: str = Path(..., description="معرف مهمة المزامنة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على مهمة مزامنة البيانات بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["ai.data.view"])
    
    # إنشاء خدمة التكامل مع نظام الذكاء الاصطناعي
    ai_service = AIIntegrationService(db_manager)
    
    # الحصول على مهمة مزامنة البيانات
    sync_job = ai_service.get_data_sync_job(job_id)
    
    if not sync_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على مهمة المزامنة بالمعرف {job_id}"
        )
    
    return {"status": "success", "data": sync_job.to_dict()}
