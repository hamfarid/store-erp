"""
وحدة التحكم في الموارد البشرية
يحتوي هذا الملف على وحدات التحكم لإدارة الموارد البشرية
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body, status
from fastapi.responses import JSONResponse

from ...core.auth.auth_manager import get_current_user, check_permissions
from ...core.database.db_manager import get_db_manager
from ..services.hr_services import (
    DepartmentService, JobPositionService, EmployeeService,
    SkillService, PayrollService, RecruitmentService
)


# إنشاء موجه API للموارد البشرية
hr_router = APIRouter(prefix="/api/hr", tags=["الموارد البشرية"])


# وحدات التحكم في الأقسام
@hr_router.post("/departments", response_model=Dict[str, Any])
async def create_department(
    department_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء قسم جديد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.departments.create"])
    
    # إنشاء خدمة الأقسام
    department_service = DepartmentService(db_manager)
    
    # إنشاء القسم
    try:
        department = department_service.create_department(department_data)
        return {"status": "success", "data": department.to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء القسم: {str(e)}"
        )


@hr_router.get("/departments", response_model=Dict[str, Any])
async def get_all_departments(
    company_id: Optional[str] = Query(None, description="معرف الشركة"),
    branch_id: Optional[str] = Query(None, description="معرف الفرع"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع الأقسام"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.departments.view"])
    
    # إنشاء خدمة الأقسام
    department_service = DepartmentService(db_manager)
    
    # الحصول على الأقسام
    try:
        departments = department_service.get_all_departments(company_id, branch_id)
        return {
            "status": "success",
            "data": [department.to_dict() for department in departments]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على الأقسام: {str(e)}"
        )


@hr_router.get("/departments/{department_id}", response_model=Dict[str, Any])
async def get_department(
    department_id: str = Path(..., description="معرف القسم"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على قسم بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.departments.view"])
    
    # إنشاء خدمة الأقسام
    department_service = DepartmentService(db_manager)
    
    # الحصول على القسم
    department = department_service.get_department(department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على القسم بالمعرف {department_id}"
        )
    
    return {"status": "success", "data": department.to_dict()}


@hr_router.put("/departments/{department_id}", response_model=Dict[str, Any])
async def update_department(
    department_id: str = Path(..., description="معرف القسم"),
    department_data: Dict[str, Any] = Body(..., description="بيانات القسم المحدثة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث قسم"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.departments.update"])
    
    # إنشاء خدمة الأقسام
    department_service = DepartmentService(db_manager)
    
    # تحديث القسم
    try:
        department = department_service.update_department(department_id, department_data)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على القسم بالمعرف {department_id}"
            )
        
        return {"status": "success", "data": department.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تحديث القسم: {str(e)}"
        )


@hr_router.delete("/departments/{department_id}", response_model=Dict[str, Any])
async def delete_department(
    department_id: str = Path(..., description="معرف القسم"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف قسم"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.departments.delete"])
    
    # إنشاء خدمة الأقسام
    department_service = DepartmentService(db_manager)
    
    # حذف القسم
    success = department_service.delete_department(department_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على القسم بالمعرف {department_id}"
        )
    
    return {"status": "success", "message": "تم حذف القسم بنجاح"}


@hr_router.get("/departments/hierarchy", response_model=Dict[str, Any])
async def get_department_hierarchy(
    company_id: Optional[str] = Query(None, description="معرف الشركة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على التسلسل الهرمي للأقسام"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.departments.view"])
    
    # إنشاء خدمة الأقسام
    department_service = DepartmentService(db_manager)
    
    # الحصول على التسلسل الهرمي للأقسام
    try:
        hierarchy = department_service.get_department_hierarchy(company_id)
        return {"status": "success", "data": hierarchy}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على التسلسل الهرمي للأقسام: {str(e)}"
        )


@hr_router.get("/departments/{department_id}/statistics", response_model=Dict[str, Any])
async def get_department_statistics(
    department_id: str = Path(..., description="معرف القسم"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على إحصائيات القسم"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.departments.view"])
    
    # إنشاء خدمة الأقسام
    department_service = DepartmentService(db_manager)
    
    # الحصول على إحصائيات القسم
    try:
        statistics = department_service.get_department_statistics(department_id)
        if not statistics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على القسم بالمعرف {department_id}"
            )
        
        return {"status": "success", "data": statistics}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على إحصائيات القسم: {str(e)}"
        )


# وحدات التحكم في المناصب الوظيفية
@hr_router.post("/positions", response_model=Dict[str, Any])
async def create_job_position(
    position_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء منصب وظيفي جديد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.positions.create"])
    
    # إنشاء خدمة المناصب الوظيفية
    position_service = JobPositionService(db_manager)
    
    # إنشاء المنصب الوظيفي
    try:
        position = position_service.create_job_position(position_data)
        return {"status": "success", "data": position.to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء المنصب الوظيفي: {str(e)}"
        )


@hr_router.get("/positions", response_model=Dict[str, Any])
async def get_all_job_positions(
    department_id: Optional[str] = Query(None, description="معرف القسم"),
    company_id: Optional[str] = Query(None, description="معرف الشركة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع المناصب الوظيفية"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.positions.view"])
    
    # إنشاء خدمة المناصب الوظيفية
    position_service = JobPositionService(db_manager)
    
    # الحصول على المناصب الوظيفية
    try:
        positions = position_service.get_all_job_positions(department_id, company_id)
        return {
            "status": "success",
            "data": [position.to_dict() for position in positions]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على المناصب الوظيفية: {str(e)}"
        )


@hr_router.get("/positions/{position_id}", response_model=Dict[str, Any])
async def get_job_position(
    position_id: str = Path(..., description="معرف المنصب الوظيفي"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على منصب وظيفي بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.positions.view"])
    
    # إنشاء خدمة المناصب الوظيفية
    position_service = JobPositionService(db_manager)
    
    # الحصول على المنصب الوظيفي
    position = position_service.get_job_position(position_id)
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على المنصب الوظيفي بالمعرف {position_id}"
        )
    
    return {"status": "success", "data": position.to_dict()}


@hr_router.put("/positions/{position_id}", response_model=Dict[str, Any])
async def update_job_position(
    position_id: str = Path(..., description="معرف المنصب الوظيفي"),
    position_data: Dict[str, Any] = Body(..., description="بيانات المنصب الوظيفي المحدثة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث منصب وظيفي"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.positions.update"])
    
    # إنشاء خدمة المناصب الوظيفية
    position_service = JobPositionService(db_manager)
    
    # تحديث المنصب الوظيفي
    try:
        position = position_service.update_job_position(position_id, position_data)
        if not position:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على المنصب الوظيفي بالمعرف {position_id}"
            )
        
        return {"status": "success", "data": position.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تحديث المنصب الوظيفي: {str(e)}"
        )


@hr_router.delete("/positions/{position_id}", response_model=Dict[str, Any])
async def delete_job_position(
    position_id: str = Path(..., description="معرف المنصب الوظيفي"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف منصب وظيفي"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.positions.delete"])
    
    # إنشاء خدمة المناصب الوظيفية
    position_service = JobPositionService(db_manager)
    
    # حذف المنصب الوظيفي
    success = position_service.delete_job_position(position_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على المنصب الوظيفي بالمعرف {position_id}"
        )
    
    return {"status": "success", "message": "تم حذف المنصب الوظيفي بنجاح"}


# وحدات التحكم في الموظفين
@hr_router.post("/employees", response_model=Dict[str, Any])
async def create_employee(
    employee_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء موظف جديد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.employees.create"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # إنشاء الموظف
    try:
        employee = employee_service.create_employee(employee_data)
        return {"status": "success", "data": employee.to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء الموظف: {str(e)}"
        )


@hr_router.get("/employees", response_model=Dict[str, Any])
async def get_all_employees(
    department_id: Optional[str] = Query(None, description="معرف القسم"),
    company_id: Optional[str] = Query(None, description="معرف الشركة"),
    branch_id: Optional[str] = Query(None, description="معرف الفرع"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع الموظفين"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.employees.view"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # الحصول على الموظفين
    try:
        employees = employee_service.get_all_employees(department_id, company_id, branch_id)
        return {
            "status": "success",
            "data": [employee.to_dict() for employee in employees]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على الموظفين: {str(e)}"
        )


@hr_router.get("/employees/search", response_model=Dict[str, Any])
async def search_employees(
    search_term: str = Query(..., description="مصطلح البحث"),
    company_id: Optional[str] = Query(None, description="معرف الشركة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """البحث عن موظفين"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.employees.view"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # البحث عن الموظفين
    try:
        employees = employee_service.search_employees(search_term, company_id)
        return {
            "status": "success",
            "data": [employee.to_dict() for employee in employees]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في البحث عن الموظفين: {str(e)}"
        )


@hr_router.get("/employees/{employee_id}", response_model=Dict[str, Any])
async def get_employee(
    employee_id: str = Path(..., description="معرف الموظف"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على موظف بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.employees.view"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # الحصول على الموظف
    employee = employee_service.get_employee(employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الموظف بالمعرف {employee_id}"
        )
    
    return {"status": "success", "data": employee.to_dict()}


@hr_router.put("/employees/{employee_id}", response_model=Dict[str, Any])
async def update_employee(
    employee_id: str = Path(..., description="معرف الموظف"),
    employee_data: Dict[str, Any] = Body(..., description="بيانات الموظف المحدثة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث موظف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.employees.update"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # تحديث الموظف
    try:
        employee = employee_service.update_employee(employee_id, employee_data)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على الموظف بالمعرف {employee_id}"
            )
        
        return {"status": "success", "data": employee.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تحديث الموظف: {str(e)}"
        )


@hr_router.delete("/employees/{employee_id}", response_model=Dict[str, Any])
async def delete_employee(
    employee_id: str = Path(..., description="معرف الموظف"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف موظف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.employees.delete"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # حذف الموظف
    success = employee_service.delete_employee(employee_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الموظف بالمعرف {employee_id}"
        )
    
    return {"status": "success", "message": "تم حذف الموظف بنجاح"}


@hr_router.get("/employees/{employee_id}/subordinates", response_model=Dict[str, Any])
async def get_subordinates(
    employee_id: str = Path(..., description="معرف الموظف"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على المرؤوسين لموظف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.employees.view"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # الحصول على المرؤوسين
    try:
        subordinates = employee_service.get_subordinates(employee_id)
        return {
            "status": "success",
            "data": [employee.to_dict() for employee in subordinates]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على المرؤوسين: {str(e)}"
        )


# وحدات التحكم في الإجازات
@hr_router.post("/leaves", response_model=Dict[str, Any])
async def add_employee_leave(
    leave_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إضافة إجازة لموظف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.leaves.create"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # إضافة الإجازة
    try:
        leave = employee_service.add_employee_leave(leave_data)
        return {"status": "success", "data": leave.to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إضافة الإجازة: {str(e)}"
        )


@hr_router.put("/leaves/{leave_id}", response_model=Dict[str, Any])
async def update_employee_leave(
    leave_id: str = Path(..., description="معرف الإجازة"),
    leave_data: Dict[str, Any] = Body(..., description="بيانات الإجازة المحدثة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث إجازة موظف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.leaves.update"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # تحديث الإجازة
    try:
        leave = employee_service.update_employee_leave(leave_id, leave_data)
        if not leave:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على الإجازة بالمعرف {leave_id}"
            )
        
        return {"status": "success", "data": leave.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تحديث الإجازة: {str(e)}"
        )


@hr_router.get("/leaves/{leave_id}", response_model=Dict[str, Any])
async def get_employee_leave(
    leave_id: str = Path(..., description="معرف الإجازة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على إجازة بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.leaves.view"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # الحصول على الإجازة
    leave = employee_service.get_employee_leave(leave_id)
    if not leave:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على الإجازة بالمعرف {leave_id}"
        )
    
    return {"status": "success", "data": leave.to_dict()}


@hr_router.post("/leaves/{leave_id}/approve", response_model=Dict[str, Any])
async def approve_leave(
    leave_id: str = Path(..., description="معرف الإجازة"),
    comments: Optional[str] = Body(None, description="تعليقات"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الموافقة على إجازة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.leaves.approve"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # الموافقة على الإجازة
    try:
        leave = employee_service.approve_leave(leave_id, current_user["user_id"], comments)
        if not leave:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على الإجازة بالمعرف {leave_id}"
            )
        
        return {"status": "success", "data": leave.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الموافقة على الإجازة: {str(e)}"
        )


@hr_router.post("/leaves/{leave_id}/reject", response_model=Dict[str, Any])
async def reject_leave(
    leave_id: str = Path(..., description="معرف الإجازة"),
    comments: Optional[str] = Body(None, description="تعليقات"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """رفض إجازة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.leaves.approve"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # رفض الإجازة
    try:
        leave = employee_service.reject_leave(leave_id, current_user["user_id"], comments)
        if not leave:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على الإجازة بالمعرف {leave_id}"
            )
        
        return {"status": "success", "data": leave.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في رفض الإجازة: {str(e)}"
        )


# وحدات التحكم في الحضور
@hr_router.post("/attendance", response_model=Dict[str, Any])
async def add_attendance(
    attendance_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إضافة سجل حضور"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.attendance.create"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # إضافة سجل الحضور
    try:
        attendance = employee_service.add_attendance(attendance_data)
        return {"status": "success", "data": attendance.to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إضافة سجل الحضور: {str(e)}"
        )


@hr_router.put("/attendance/{attendance_id}", response_model=Dict[str, Any])
async def update_attendance(
    attendance_id: str = Path(..., description="معرف سجل الحضور"),
    attendance_data: Dict[str, Any] = Body(..., description="بيانات سجل الحضور المحدثة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث سجل حضور"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.attendance.update"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # تحديث سجل الحضور
    try:
        attendance = employee_service.update_attendance(attendance_id, attendance_data)
        if not attendance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على سجل الحضور بالمعرف {attendance_id}"
            )
        
        return {"status": "success", "data": attendance.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تحديث سجل الحضور: {str(e)}"
        )


@hr_router.get("/attendance/{attendance_id}", response_model=Dict[str, Any])
async def get_attendance(
    attendance_id: str = Path(..., description="معرف سجل الحضور"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على سجل حضور بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.attendance.view"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # الحصول على سجل الحضور
    attendance = employee_service.get_attendance(attendance_id)
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على سجل الحضور بالمعرف {attendance_id}"
        )
    
    return {"status": "success", "data": attendance.to_dict()}


@hr_router.get("/employees/{employee_id}/attendance/report", response_model=Dict[str, Any])
async def get_employee_attendance_report(
    employee_id: str = Path(..., description="معرف الموظف"),
    start_date: date = Query(..., description="تاريخ البداية"),
    end_date: date = Query(..., description="تاريخ النهاية"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على تقرير حضور موظف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.attendance.view"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # الحصول على تقرير الحضور
    try:
        report = employee_service.get_employee_attendance_report(employee_id, start_date, end_date)
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على الموظف بالمعرف {employee_id}"
            )
        
        return {"status": "success", "data": report}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على تقرير الحضور: {str(e)}"
        )


# وحدات التحكم في المستندات
@hr_router.post("/documents", response_model=Dict[str, Any])
async def add_employee_document(
    document_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إضافة مستند لموظف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.documents.create"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # إضافة المستند
    try:
        document = employee_service.add_employee_document(document_data)
        return {"status": "success", "data": document.to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إضافة المستند: {str(e)}"
        )


@hr_router.put("/documents/{document_id}", response_model=Dict[str, Any])
async def update_employee_document(
    document_id: str = Path(..., description="معرف المستند"),
    document_data: Dict[str, Any] = Body(..., description="بيانات المستند المحدثة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث مستند موظف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.documents.update"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # تحديث المستند
    try:
        document = employee_service.update_employee_document(document_id, document_data)
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على المستند بالمعرف {document_id}"
            )
        
        return {"status": "success", "data": document.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تحديث المستند: {str(e)}"
        )


@hr_router.get("/documents/{document_id}", response_model=Dict[str, Any])
async def get_employee_document(
    document_id: str = Path(..., description="معرف المستند"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على مستند بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.documents.view"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # الحصول على المستند
    document = employee_service.get_employee_document(document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على المستند بالمعرف {document_id}"
        )
    
    return {"status": "success", "data": document.to_dict()}


# وحدات التحكم في المهارات
@hr_router.post("/skills", response_model=Dict[str, Any])
async def create_skill(
    skill_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء مهارة جديدة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.skills.create"])
    
    # إنشاء خدمة المهارات
    skill_service = SkillService(db_manager)
    
    # إنشاء المهارة
    try:
        skill = skill_service.create_skill(skill_data)
        return {"status": "success", "data": skill.to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء المهارة: {str(e)}"
        )


@hr_router.get("/skills", response_model=Dict[str, Any])
async def get_all_skills(
    company_id: Optional[str] = Query(None, description="معرف الشركة"),
    category: Optional[str] = Query(None, description="فئة المهارة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع المهارات"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.skills.view"])
    
    # إنشاء خدمة المهارات
    skill_service = SkillService(db_manager)
    
    # الحصول على المهارات
    try:
        skills = skill_service.get_all_skills(company_id, category)
        return {
            "status": "success",
            "data": [skill.to_dict() for skill in skills]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على المهارات: {str(e)}"
        )


@hr_router.get("/skills/categories", response_model=Dict[str, Any])
async def get_skill_categories(
    company_id: Optional[str] = Query(None, description="معرف الشركة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على فئات المهارات"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.skills.view"])
    
    # إنشاء خدمة المهارات
    skill_service = SkillService(db_manager)
    
    # الحصول على فئات المهارات
    try:
        categories = skill_service.get_skill_categories(company_id)
        return {"status": "success", "data": categories}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على فئات المهارات: {str(e)}"
        )


@hr_router.get("/skills/{skill_id}", response_model=Dict[str, Any])
async def get_skill(
    skill_id: str = Path(..., description="معرف المهارة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على مهارة بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.skills.view"])
    
    # إنشاء خدمة المهارات
    skill_service = SkillService(db_manager)
    
    # الحصول على المهارة
    skill = skill_service.get_skill(skill_id)
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على المهارة بالمعرف {skill_id}"
        )
    
    return {"status": "success", "data": skill.to_dict()}


@hr_router.put("/skills/{skill_id}", response_model=Dict[str, Any])
async def update_skill(
    skill_id: str = Path(..., description="معرف المهارة"),
    skill_data: Dict[str, Any] = Body(..., description="بيانات المهارة المحدثة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث مهارة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.skills.update"])
    
    # إنشاء خدمة المهارات
    skill_service = SkillService(db_manager)
    
    # تحديث المهارة
    try:
        skill = skill_service.update_skill(skill_id, skill_data)
        if not skill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على المهارة بالمعرف {skill_id}"
            )
        
        return {"status": "success", "data": skill.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تحديث المهارة: {str(e)}"
        )


@hr_router.delete("/skills/{skill_id}", response_model=Dict[str, Any])
async def delete_skill(
    skill_id: str = Path(..., description="معرف المهارة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف مهارة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.skills.delete"])
    
    # إنشاء خدمة المهارات
    skill_service = SkillService(db_manager)
    
    # حذف المهارة
    success = skill_service.delete_skill(skill_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على المهارة بالمعرف {skill_id}"
        )
    
    return {"status": "success", "message": "تم حذف المهارة بنجاح"}


@hr_router.post("/employees/skills", response_model=Dict[str, Any])
async def add_employee_skill(
    skill_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إضافة مهارة لموظف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.employees.update"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # إضافة المهارة
    try:
        employee_skill = employee_service.add_employee_skill(skill_data)
        return {"status": "success", "data": employee_skill.to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إضافة المهارة للموظف: {str(e)}"
        )


@hr_router.put("/employees/skills/{employee_skill_id}", response_model=Dict[str, Any])
async def update_employee_skill(
    employee_skill_id: str = Path(..., description="معرف مهارة الموظف"),
    skill_data: Dict[str, Any] = Body(..., description="بيانات المهارة المحدثة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث مهارة موظف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.employees.update"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # تحديث المهارة
    try:
        employee_skill = employee_service.update_employee_skill(employee_skill_id, skill_data)
        if not employee_skill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على مهارة الموظف بالمعرف {employee_skill_id}"
            )
        
        return {"status": "success", "data": employee_skill.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تحديث مهارة الموظف: {str(e)}"
        )


@hr_router.get("/employees/skills/{employee_skill_id}", response_model=Dict[str, Any])
async def get_employee_skill(
    employee_skill_id: str = Path(..., description="معرف مهارة الموظف"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على مهارة موظف بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.employees.view"])
    
    # إنشاء خدمة الموظفين
    employee_service = EmployeeService(db_manager)
    
    # الحصول على مهارة الموظف
    employee_skill = employee_service.get_employee_skill(employee_skill_id)
    if not employee_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على مهارة الموظف بالمعرف {employee_skill_id}"
        )
    
    return {"status": "success", "data": employee_skill.to_dict()}


# وحدات التحكم في كشوف الرواتب
@hr_router.post("/payrolls", response_model=Dict[str, Any])
async def create_payroll(
    payroll_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء كشف رواتب جديد"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.payrolls.create"])
    
    # إنشاء خدمة كشوف الرواتب
    payroll_service = PayrollService(db_manager)
    
    # إنشاء كشف الرواتب
    try:
        payroll = payroll_service.create_payroll(payroll_data)
        return {"status": "success", "data": payroll.to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء كشف الرواتب: {str(e)}"
        )


@hr_router.post("/payrolls/generate", response_model=Dict[str, Any])
async def generate_payroll(
    employee_id: str = Body(..., description="معرف الموظف"),
    period_start: date = Body(..., description="تاريخ بداية الفترة"),
    period_end: date = Body(..., description="تاريخ نهاية الفترة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء كشف رواتب لموظف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.payrolls.create"])
    
    # إنشاء خدمة كشوف الرواتب
    payroll_service = PayrollService(db_manager)
    
    # إنشاء كشف الرواتب
    try:
        payroll = payroll_service.generate_payroll(employee_id, period_start, period_end)
        return {"status": "success", "data": payroll.to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء كشف الرواتب: {str(e)}"
        )


@hr_router.post("/payrolls/generate/department", response_model=Dict[str, Any])
async def generate_department_payrolls(
    department_id: str = Body(..., description="معرف القسم"),
    period_start: date = Body(..., description="تاريخ بداية الفترة"),
    period_end: date = Body(..., description="تاريخ نهاية الفترة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء كشوف رواتب لقسم"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.payrolls.create"])
    
    # إنشاء خدمة كشوف الرواتب
    payroll_service = PayrollService(db_manager)
    
    # إنشاء كشوف الرواتب
    try:
        payrolls = payroll_service.generate_department_payrolls(department_id, period_start, period_end)
        return {
            "status": "success",
            "data": [payroll.to_dict() for payroll in payrolls]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء كشوف الرواتب: {str(e)}"
        )


@hr_router.get("/payrolls/{payroll_id}", response_model=Dict[str, Any])
async def get_payroll(
    payroll_id: str = Path(..., description="معرف كشف الرواتب"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على كشف رواتب بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.payrolls.view"])
    
    # إنشاء خدمة كشوف الرواتب
    payroll_service = PayrollService(db_manager)
    
    # الحصول على كشف الرواتب
    payroll = payroll_service.get_payroll(payroll_id)
    if not payroll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على كشف الرواتب بالمعرف {payroll_id}"
        )
    
    return {"status": "success", "data": payroll.to_dict()}


@hr_router.get("/employees/{employee_id}/payrolls", response_model=Dict[str, Any])
async def get_employee_payrolls(
    employee_id: str = Path(..., description="معرف الموظف"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على كشوف رواتب موظف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.payrolls.view"])
    
    # إنشاء خدمة كشوف الرواتب
    payroll_service = PayrollService(db_manager)
    
    # الحصول على كشوف الرواتب
    try:
        payrolls = payroll_service.get_employee_payrolls(employee_id)
        return {
            "status": "success",
            "data": [payroll.to_dict() for payroll in payrolls]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على كشوف الرواتب: {str(e)}"
        )


@hr_router.post("/payrolls/{payroll_id}/approve", response_model=Dict[str, Any])
async def approve_payroll(
    payroll_id: str = Path(..., description="معرف كشف الرواتب"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الموافقة على كشف رواتب"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.payrolls.approve"])
    
    # إنشاء خدمة كشوف الرواتب
    payroll_service = PayrollService(db_manager)
    
    # الموافقة على كشف الرواتب
    try:
        payroll = payroll_service.approve_payroll(payroll_id)
        if not payroll:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على كشف الرواتب بالمعرف {payroll_id}"
            )
        
        return {"status": "success", "data": payroll.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الموافقة على كشف الرواتب: {str(e)}"
        )


@hr_router.post("/payrolls/{payroll_id}/process", response_model=Dict[str, Any])
async def process_payroll(
    payroll_id: str = Path(..., description="معرف كشف الرواتب"),
    payment_method: str = Body(..., description="طريقة الدفع"),
    payment_date: Optional[date] = Body(None, description="تاريخ الدفع"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """معالجة كشف رواتب"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.payrolls.process"])
    
    # إنشاء خدمة كشوف الرواتب
    payroll_service = PayrollService(db_manager)
    
    # معالجة كشف الرواتب
    try:
        payroll = payroll_service.process_payroll(payroll_id, payment_method, payment_date)
        if not payroll:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على كشف الرواتب بالمعرف {payroll_id}"
            )
        
        return {"status": "success", "data": payroll.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في معالجة كشف الرواتب: {str(e)}"
        )


# وحدات التحكم في التوظيف
@hr_router.post("/recruitments", response_model=Dict[str, Any])
async def create_recruitment(
    recruitment_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إنشاء عملية توظيف جديدة"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.recruitments.create"])
    
    # إنشاء خدمة التوظيف
    recruitment_service = RecruitmentService(db_manager)
    
    # إنشاء عملية التوظيف
    try:
        recruitment = recruitment_service.create_recruitment(recruitment_data)
        return {"status": "success", "data": recruitment.to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إنشاء عملية التوظيف: {str(e)}"
        )


@hr_router.get("/recruitments", response_model=Dict[str, Any])
async def get_all_recruitments(
    company_id: Optional[str] = Query(None, description="معرف الشركة"),
    department_id: Optional[str] = Query(None, description="معرف القسم"),
    status: Optional[str] = Query(None, description="حالة عملية التوظيف"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على جميع عمليات التوظيف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.recruitments.view"])
    
    # إنشاء خدمة التوظيف
    recruitment_service = RecruitmentService(db_manager)
    
    # الحصول على عمليات التوظيف
    try:
        recruitments = recruitment_service.get_all_recruitments(company_id, department_id, status)
        return {
            "status": "success",
            "data": [recruitment.to_dict() for recruitment in recruitments]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في الحصول على عمليات التوظيف: {str(e)}"
        )


@hr_router.get("/recruitments/{recruitment_id}", response_model=Dict[str, Any])
async def get_recruitment(
    recruitment_id: str = Path(..., description="معرف عملية التوظيف"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على عملية توظيف بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.recruitments.view"])
    
    # إنشاء خدمة التوظيف
    recruitment_service = RecruitmentService(db_manager)
    
    # الحصول على عملية التوظيف
    recruitment = recruitment_service.get_recruitment(recruitment_id)
    if not recruitment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على عملية التوظيف بالمعرف {recruitment_id}"
        )
    
    return {"status": "success", "data": recruitment.to_dict()}


@hr_router.put("/recruitments/{recruitment_id}", response_model=Dict[str, Any])
async def update_recruitment(
    recruitment_id: str = Path(..., description="معرف عملية التوظيف"),
    recruitment_data: Dict[str, Any] = Body(..., description="بيانات عملية التوظيف المحدثة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث عملية توظيف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.recruitments.update"])
    
    # إنشاء خدمة التوظيف
    recruitment_service = RecruitmentService(db_manager)
    
    # تحديث عملية التوظيف
    try:
        recruitment = recruitment_service.update_recruitment(recruitment_id, recruitment_data)
        if not recruitment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على عملية التوظيف بالمعرف {recruitment_id}"
            )
        
        return {"status": "success", "data": recruitment.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تحديث عملية التوظيف: {str(e)}"
        )


@hr_router.delete("/recruitments/{recruitment_id}", response_model=Dict[str, Any])
async def delete_recruitment(
    recruitment_id: str = Path(..., description="معرف عملية التوظيف"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """حذف عملية توظيف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.recruitments.delete"])
    
    # إنشاء خدمة التوظيف
    recruitment_service = RecruitmentService(db_manager)
    
    # حذف عملية التوظيف
    success = recruitment_service.delete_recruitment(recruitment_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على عملية التوظيف بالمعرف {recruitment_id}"
        )
    
    return {"status": "success", "message": "تم حذف عملية التوظيف بنجاح"}


@hr_router.post("/recruitments/{recruitment_id}/close", response_model=Dict[str, Any])
async def close_recruitment(
    recruitment_id: str = Path(..., description="معرف عملية التوظيف"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إغلاق عملية توظيف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.recruitments.update"])
    
    # إنشاء خدمة التوظيف
    recruitment_service = RecruitmentService(db_manager)
    
    # إغلاق عملية التوظيف
    try:
        recruitment = recruitment_service.close_recruitment(recruitment_id)
        if not recruitment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على عملية التوظيف بالمعرف {recruitment_id}"
            )
        
        return {"status": "success", "data": recruitment.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إغلاق عملية التوظيف: {str(e)}"
        )


@hr_router.post("/candidates", response_model=Dict[str, Any])
async def add_candidate(
    candidate_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """إضافة مرشح لعملية توظيف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.recruitments.update"])
    
    # إنشاء خدمة التوظيف
    recruitment_service = RecruitmentService(db_manager)
    
    # إضافة المرشح
    try:
        candidate = recruitment_service.add_candidate(candidate_data)
        return {"status": "success", "data": candidate.to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في إضافة المرشح: {str(e)}"
        )


@hr_router.get("/candidates/{candidate_id}", response_model=Dict[str, Any])
async def get_candidate(
    candidate_id: str = Path(..., description="معرف المرشح"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """الحصول على مرشح بواسطة المعرف"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.recruitments.view"])
    
    # إنشاء خدمة التوظيف
    recruitment_service = RecruitmentService(db_manager)
    
    # الحصول على المرشح
    candidate = recruitment_service.get_candidate(candidate_id)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"لم يتم العثور على المرشح بالمعرف {candidate_id}"
        )
    
    return {"status": "success", "data": candidate.to_dict()}


@hr_router.put("/candidates/{candidate_id}", response_model=Dict[str, Any])
async def update_candidate(
    candidate_id: str = Path(..., description="معرف المرشح"),
    candidate_data: Dict[str, Any] = Body(..., description="بيانات المرشح المحدثة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تحديث مرشح"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.recruitments.update"])
    
    # إنشاء خدمة التوظيف
    recruitment_service = RecruitmentService(db_manager)
    
    # تحديث المرشح
    try:
        candidate = recruitment_service.update_candidate(candidate_id, candidate_data)
        if not candidate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على المرشح بالمعرف {candidate_id}"
            )
        
        return {"status": "success", "data": candidate.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تحديث المرشح: {str(e)}"
        )


@hr_router.post("/candidates/{candidate_id}/schedule-interview", response_model=Dict[str, Any])
async def schedule_interview(
    candidate_id: str = Path(..., description="معرف المرشح"),
    interview_date: datetime = Body(..., description="تاريخ ووقت المقابلة"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """جدولة مقابلة لمرشح"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.recruitments.update"])
    
    # إنشاء خدمة التوظيف
    recruitment_service = RecruitmentService(db_manager)
    
    # جدولة المقابلة
    try:
        candidate = recruitment_service.schedule_interview(candidate_id, interview_date)
        if not candidate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على المرشح بالمعرف {candidate_id}"
            )
        
        return {"status": "success", "data": candidate.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في جدولة المقابلة: {str(e)}"
        )


@hr_router.post("/candidates/{candidate_id}/evaluate", response_model=Dict[str, Any])
async def evaluate_candidate(
    candidate_id: str = Path(..., description="معرف المرشح"),
    evaluation: str = Body(..., description="تقييم المرشح"),
    rating: int = Body(..., description="تقييم المرشح (1-5)"),
    notes: Optional[str] = Body(None, description="ملاحظات"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """تقييم مرشح"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.recruitments.update"])
    
    # إنشاء خدمة التوظيف
    recruitment_service = RecruitmentService(db_manager)
    
    # تقييم المرشح
    try:
        candidate = recruitment_service.evaluate_candidate(candidate_id, evaluation, rating, notes)
        if not candidate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على المرشح بالمعرف {candidate_id}"
            )
        
        return {"status": "success", "data": candidate.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في تقييم المرشح: {str(e)}"
        )


@hr_router.post("/candidates/{candidate_id}/hire", response_model=Dict[str, Any])
async def hire_candidate(
    candidate_id: str = Path(..., description="معرف المرشح"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """توظيف مرشح"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.recruitments.update", "hr.employees.create"])
    
    # إنشاء خدمة التوظيف
    recruitment_service = RecruitmentService(db_manager)
    
    # توظيف المرشح
    try:
        employee = recruitment_service.hire_candidate(candidate_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على المرشح بالمعرف {candidate_id}"
            )
        
        return {"status": "success", "data": employee.to_dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في توظيف المرشح: {str(e)}"
        )


@hr_router.post("/candidates/{candidate_id}/reject", response_model=Dict[str, Any])
async def reject_candidate(
    candidate_id: str = Path(..., description="معرف المرشح"),
    reason: Optional[str] = Body(None, description="سبب الرفض"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db_manager = Depends(get_db_manager)
):
    """رفض مرشح"""
    # التحقق من الصلاحيات
    check_permissions(current_user, ["hr.recruitments.update"])
    
    # إنشاء خدمة التوظيف
    recruitment_service = RecruitmentService(db_manager)
    
    # رفض المرشح
    try:
        candidate = recruitment_service.reject_candidate(candidate_id, reason)
        if not candidate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"لم يتم العثور على المرشح بالمعرف {candidate_id}"
            )
        
        return {"status": "success", "data": candidate.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل في رفض المرشح: {str(e)}"
        )
