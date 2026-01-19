"""
مسار الملف: /home/ubuntu/gaara_scan_ai_final_4.2/src/modules/import_export/dependencies.py
الوصف: دوال التحقق من صحة البيانات والتبعيات لمديول الاستيراد والتصدير
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import json
import os
import re
from typing import Any, Dict, List

import magic
import pandas as pd
from fastapi import Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from src.database import get_db

from . import schemas, service


async def validate_import_file(file: UploadFile, module: str):
    """
    التحقق من صحة ملف الاستيراد

    Args:
        file (UploadFile): ملف الاستيراد
        module (str): معرف المديول

    Raises:
        HTTPException: في حالة وجود خطأ في الملف
    """
    # التحقق من وجود الملف
    if not file:
        raise HTTPException(status_code=400, detail="لم يتم تحميل أي ملف")

    # التحقق من امتداد الملف
    filename = file.filename
    if not filename:
        raise HTTPException(status_code=400, detail="اسم الملف غير صالح")

    # استخراج امتداد الملف
    file_extension = os.path.splitext(filename)[1].lower()

    # التحقق من نوع الملف
    valid_extensions = {
        ".csv": [
            "text/csv",
            "application/csv"],
        ".xlsx": ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
        ".json": ["application/json"],
        ".xml": [
            "application/xml",
            "text/xml"],
        ".zip": [
            "application/zip",
            "application/x-zip-compressed"]}

    if file_extension not in valid_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"امتداد الملف غير مدعوم. الامتدادات المدعومة هي: {', '.join(valid_extensions.keys())}"
        )

    # قراءة محتوى الملف للتحقق من نوعه
    file_content = await file.read(1024)  # قراءة أول 1024 بايت فقط للتحقق

    # إعادة مؤشر الملف إلى البداية
    await file.seek(0)

    # التحقق من نوع الملف باستخدام مكتبة magic
    mime_type = magic.from_buffer(file_content, mime=True)

    if mime_type not in valid_extensions[file_extension]:
        raise HTTPException(
            status_code=400,
            detail=f"نوع الملف غير متطابق مع الامتداد. نوع الملف المكتشف: {mime_type}")

    # التحقق من حجم الملف
    # الحصول على إعدادات الاستيراد والتصدير
    db = next(get_db())
    settings = await service.get_settings(db)

    # التحقق من حجم الملف
    max_file_size = settings.max_file_size_mb * \
        1024 * 1024  # تحويل من ميجابايت إلى بايت

    # إعادة مؤشر الملف إلى البداية
    await file.seek(0)

    # قراءة محتوى الملف بالكامل
    file_content = await file.read()

    # التحقق من حجم الملف
    if len(file_content) > max_file_size:
        raise HTTPException(
            status_code=400,
            detail=f"حجم الملف يتجاوز الحد الأقصى المسموح به ({settings.max_file_size_mb} ميجابايت)"
        )

    # إعادة مؤشر الملف إلى البداية
    await file.seek(0)

    # التحقق من تنسيق الملف
    if file_extension == ".csv":
        try:
            # قراءة الملف كـ CSV
            df = pd.read_csv(file.file)

            # التحقق من وجود بيانات
            if df.empty:
                raise HTTPException(status_code=400, detail="ملف CSV فارغ")

            # إعادة مؤشر الملف إلى البداية
            await file.seek(0)
        except Exception as e:
            raise HTTPException(status_code=400,
                                detail=f"خطأ في قراءة ملف CSV: {str(e)}")

    elif file_extension == ".xlsx":
        try:
            # قراءة الملف كـ Excel
            df = pd.read_excel(file.file)

            # التحقق من وجود بيانات
            if df.empty:
                raise HTTPException(status_code=400, detail="ملف Excel فارغ")

            # إعادة مؤشر الملف إلى البداية
            await file.seek(0)
        except Exception as e:
            raise HTTPException(status_code=400,
                                detail=f"خطأ في قراءة ملف Excel: {str(e)}")

    elif file_extension == ".json":
        try:
            # قراءة الملف كـ JSON
            data = json.load(file.file)

            # التحقق من وجود بيانات
            if not data:
                raise HTTPException(status_code=400, detail="ملف JSON فارغ")

            # إعادة مؤشر الملف إلى البداية
            await file.seek(0)
        except Exception as e:
            raise HTTPException(status_code=400,
                                detail=f"خطأ في قراءة ملف JSON: {str(e)}")

    # التحقق من دعم المديول للاستيراد
    db = next(get_db())
    modules = await service.get_available_modules(db, {"id": 1, "username": "system"})

    module_found = False
    for m in modules:
        if m.id == module:
            module_found = True
            if not m.supports_import:
                raise HTTPException(
                    status_code=400,
                    detail=f"المديول {module} لا يدعم الاستيراد"
                )
            break

    if not module_found:
        raise HTTPException(
            status_code=400,
            detail=f"المديول {module} غير موجود"
        )


async def validate_export_request(export_request: schemas.ExportRequest):
    """
    التحقق من صحة طلب التصدير

    Args:
        export_request (schemas.ExportRequest): طلب التصدير

    Raises:
        HTTPException: في حالة وجود خطأ في الطلب
    """
    # التحقق من وجود المديول
    db = next(get_db())
    modules = await service.get_available_modules(db, {"id": 1, "username": "system"})

    module_found = False
    for m in modules:
        if m.id == export_request.module:
            module_found = True
            if not m.supports_export:
                raise HTTPException(
                    status_code=400,
                    detail=f"المديول {export_request.module} لا يدعم التصدير"
                )
            break

    if not module_found:
        raise HTTPException(
            status_code=400,
            detail=f"المديول {export_request.module} غير موجود"
        )

    # التحقق من صيغة التصدير
    settings = await service.get_settings(db)

    if export_request.format not in settings.allowed_formats:
        raise HTTPException(
            status_code=400,
            detail=f"صيغة التصدير {export_request.format} غير مدعومة. الصيغ المدعومة هي: {', '.join([f.value for f in settings.allowed_formats])}"
        )

    # التحقق من قالب التصدير إذا تم تحديده
    if export_request.template_id:
        template = await service.get_template(db, export_request.template_id)

        if not template:
            raise HTTPException(
                status_code=400,
                detail=f"قالب التصدير رقم {export_request.template_id} غير موجود")

        if template.module_id != export_request.module:
            raise HTTPException(
                status_code=400,
                detail=f"قالب التصدير رقم {export_request.template_id} غير متوافق مع المديول {export_request.module}"
            )

        if template.type != "export":
            raise HTTPException(
                status_code=400,
                detail=f"قالب رقم {export_request.template_id} ليس قالب تصدير"
            )


async def validate_field_mapping(
    module: str,
    field_mapping: Dict[str, str],
    db: Session = Depends(get_db)
) -> List[str]:
    """
    التحقق من صحة تعيين الحقول

    Args:
        module (str): معرف المديول
        field_mapping (Dict[str, str]): تعيين الحقول
        db (Session): جلسة قاعدة البيانات

    Returns:
        List[str]: قائمة بالأخطاء إن وجدت

    Raises:
        HTTPException: في حالة وجود خطأ في التعيين
    """
    errors = []

    # الحصول على معلومات المديول
    modules = await service.get_available_modules(db, {"id": 1, "username": "system"})

    module_info = None
    for m in modules:
        if m.id == module:
            module_info = m
            break

    if not module_info:
        raise HTTPException(
            status_code=400,
            detail=f"المديول {module} غير موجود"
        )

    # التحقق من وجود جميع الحقول المطلوبة
    for required_field in module_info.required_fields:
        if required_field not in field_mapping.values():
            errors.append(
                f"الحقل المطلوب {required_field} غير موجود في تعيين الحقول")

    # التحقق من صحة أسماء الحقول
    valid_fields = [field["name"] for field in module_info.fields]

    for source_field, target_field in field_mapping.items():
        if target_field not in valid_fields:
            errors.append(
                f"الحقل {target_field} غير موجود في المديول {module}")

    return errors


async def validate_import_data(
    module: str,
    data: List[Dict[str, Any]],
    field_mapping: Dict[str, str],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    التحقق من صحة بيانات الاستيراد

    Args:
        module (str): معرف المديول
        data (List[Dict[str, Any]]): بيانات الاستيراد
        field_mapping (Dict[str, str]): تعيين الحقول
        db (Session): جلسة قاعدة البيانات

    Returns:
        Dict[str, Any]: نتيجة التحقق

    Raises:
        HTTPException: في حالة وجود خطأ في البيانات
    """
    result = {
        "is_valid": True,
        "errors": [],
        "warnings": [],
        "details": {
            "total_records": len(data),
            "valid_records": 0,
            "invalid_records": 0,
            "record_errors": []
        }
    }

    # الحصول على معلومات المديول
    modules = await service.get_available_modules(db, {"id": 1, "username": "system"})

    module_info = None
    for m in modules:
        if m.id == module:
            module_info = m
            break

    if not module_info:
        raise HTTPException(
            status_code=400,
            detail=f"المديول {module} غير موجود"
        )

    # التحقق من صحة البيانات
    for i, record in enumerate(data):
        record_errors = []

        # التحقق من وجود جميع الحقول المطلوبة
        for required_field in module_info.required_fields:
            target_field = None

            # البحث عن الحقل المطلوب في تعيين الحقول
            for source_field, field in field_mapping.items():
                if field == required_field:
                    target_field = source_field
                    break

            if target_field and (
                    target_field not in record or record[target_field] is None or record[target_field] == ""):
                record_errors.append(
                    f"الحقل المطلوب {required_field} غير موجود أو فارغ")

        # التحقق من نوع البيانات
        for field_info in module_info.fields:
            field_name = field_info["name"]
            field_type = field_info.get("type", "string")

            # البحث عن الحقل في تعيين الحقول
            source_field = None
            for src, tgt in field_mapping.items():
                if tgt == field_name:
                    source_field = src
                    break

            if source_field and source_field in record and record[
                    source_field] is not None and record[source_field] != "":
                value = record[source_field]

                # التحقق من نوع البيانات
                if field_type == "integer":
                    try:
                        int(value)
                    except (ValueError, TypeError):
                        record_errors.append(
                            f"قيمة الحقل {field_name} يجب أن تكون رقم صحيح")

                elif field_type == "float" or field_type == "decimal":
                    try:
                        float(value)
                    except (ValueError, TypeError):
                        record_errors.append(
                            f"قيمة الحقل {field_name} يجب أن تكون رقم عشري")

                elif field_type == "boolean":
                    if not isinstance(value, bool) and str(value).lower() not in [
                            "true", "false", "0", "1", "yes", "no", "نعم", "لا"]:
                        record_errors.append(
                            f"قيمة الحقل {field_name} يجب أن تكون قيمة منطقية (true/false)")

                elif field_type == "date":
                    # التحقق من صحة التاريخ
                    if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(value)):
                        record_errors.append(
                            f"قيمة الحقل {field_name} يجب أن تكون تاريخ بصيغة YYYY-MM-DD")

                elif field_type == "datetime":
                    # التحقق من صحة التاريخ والوقت
                    if not re.match(
                        r"^\d{4}-\d{2}-\d{2}(T| )\d{2}:\d{2}(:\d{2})?$",
                            str(value)):
                        record_errors.append(
                            f"قيمة الحقل {field_name} يجب أن تكون تاريخ ووقت بصيغة YYYY-MM-DD HH:MM:SS")

                elif field_type == "email":
                    # التحقق من صحة البريد الإلكتروني
                    if not re.match(
                        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                            str(value)):
                        record_errors.append(
                            f"قيمة الحقل {field_name} يجب أن تكون بريد إلكتروني صحيح")

                elif field_type == "url":
                    # التحقق من صحة الرابط
                    if not re.match(r"^https?://", str(value)):
                        record_errors.append(
                            f"قيمة الحقل {field_name} يجب أن تكون رابط صحيح يبدأ بـ http:// أو https://")

                elif field_type == "phone":
                    # التحقق من صحة رقم الهاتف
                    if not re.match(r"^\+?[0-9\s\-\(\)]{8,20}$", str(value)):
                        record_errors.append(
                            f"قيمة الحقل {field_name} يجب أن تكون رقم هاتف صحيح")

        # إضافة أخطاء السجل إلى النتيجة
        if record_errors:
            result["details"]["invalid_records"] += 1
            result["details"]["record_errors"].append({
                "row": i + 1,
                "errors": record_errors
            })
        else:
            result["details"]["valid_records"] += 1

    # تحديث حالة الصلاحية
    if result["details"]["invalid_records"] > 0:
        result["is_valid"] = False
        result["errors"].append(
            f"يوجد {result['details']['invalid_records']} سجل غير صالح من أصل {result['details']['total_records']}")

    return result
