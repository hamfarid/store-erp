# /home/ubuntu/image_search_integration/auto_learning/utils/helpers.py
"""
دوال مساعدة لمديول البحث الذاتي الذكي

يحتوي هذا الملف على دوال مساعدة متنوعة تستخدم في مديول البحث الذاتي الذكي،
مثل دوال معالجة النصوص وتحويل البيانات وتنسيق النتائج.
"""

import datetime
import hashlib
import re
from typing import Any, Dict, List, Optional, Union
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


def normalize_text(text: str) -> str:
    """
    تطبيع النص بإزالة الأحرف الخاصة والمسافات الزائدة

    Args:
        text: النص المراد تطبيعه

    Returns:
        النص بعد التطبيع
    """
    # إزالة الأحرف الخاصة
    text = re.sub(r'[^\w\s]', ' ', text)
    # إزالة المسافات الزائدة
    text = re.sub(r'\s+', ' ', text)
    # تحويل إلى أحرف صغيرة وإزالة المسافات في البداية والنهاية
    return text.lower().strip()


def generate_hash(text: str) -> str:
    """
    توليد قيمة تجزئة (hash) للنص

    Args:
        text: النص المراد توليد قيمة تجزئة له

    Returns:
        قيمة التجزئة كسلسلة نصية
    """
    return hashlib.md5(text.encode('utf-8'), usedforsecurity=False).hexdigest()


def build_search_url(base_url: str, query_param: str, query: str,
                     additional_params: Optional[Dict[str, str]] = None) -> str:
    """
    بناء عنوان URL للبحث

    Args:
        base_url: عنوان URL الأساسي
        query_param: اسم معلمة الاستعلام
        query: نص الاستعلام
        additional_params: معلمات إضافية (اختياري)

    Returns:
        عنوان URL كامل للبحث
    """
    # تحليل عنوان URL الأساسي
    parsed_url = urlparse(base_url)

    # الحصول على المعلمات الحالية
    query_dict = dict(parse_qsl(parsed_url.query))

    # إضافة معلمة الاستعلام
    query_dict[query_param] = query

    # إضافة المعلمات الإضافية إن وجدت
    if additional_params:
        query_dict.update(additional_params)

    # إعادة بناء عنوان URL
    new_query = urlencode(query_dict)
    return urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        new_query,
        parsed_url.fragment
    ))


def format_date(date: Union[datetime.datetime, str]) -> str:
    """
    تنسيق التاريخ إلى سلسلة نصية

    Args:
        date: كائن تاريخ أو سلسلة نصية تمثل تاريخ

    Returns:
        التاريخ منسقاً كسلسلة نصية
    """
    if isinstance(date, str):
        try:
            date = datetime.datetime.fromisoformat(date)
        except ValueError:
            return date

    return date.strftime("%Y-%m-%d %H:%M:%S")


def get_category_label(category: str) -> str:
    """
    الحصول على تسمية التصنيف بالعربية

    Args:
        category: رمز التصنيف

    Returns:
        تسمية التصنيف بالعربية
    """
    category_labels = {
        "PLANT": "نبات",
        "DISEASE": "مرض",
        "PEST": "آفة",
        "TECHNIQUE": "تقنية",
        "FERTILIZER": "سماد",
        "EQUIPMENT": "معدات",
        "SYMPTOM": "عرض",
        "OTHER": "أخرى"
    }
    return category_labels.get(category, category)


def get_plant_part_label(part: str) -> str:
    """
    الحصول على تسمية جزء النبات بالعربية

    Args:
        part: رمز جزء النبات

    Returns:
        تسمية جزء النبات بالعربية
    """
    part_labels = {
        "LEAF": "ورقة",
        "STEM": "ساق",
        "ROOT": "جذر",
        "FLOWER": "زهرة",
        "FRUIT": "ثمرة",
        "SEED": "بذرة"
    }
    return part_labels.get(part, part)


def get_relation_type_label(relation_type: str) -> str:
    """
    الحصول على تسمية نوع العلاقة بالعربية

    Args:
        relation_type: رمز نوع العلاقة

    Returns:
        تسمية نوع العلاقة بالعربية
    """
    relation_labels = {
        "SYNONYM": "مرادف",
        "BROADER": "أوسع",
        "NARROWER": "أضيق",
        "RELATED": "ذو صلة",
        "CAUSE": "سبب",
        "EFFECT": "نتيجة",
        "PART_OF": "جزء من",
        "HAS_PART": "يحتوي على"
    }
    return relation_labels.get(relation_type, relation_type)


def extract_domain_from_url(url: str) -> str:
    """
    استخراج النطاق من عنوان URL

    Args:
        url: عنوان URL

    Returns:
        النطاق المستخرج
    """
    try:
        parsed_url = urlparse(url)
        return parsed_url.netloc
    except (ValueError, AttributeError):
        return ""


def is_valid_url(url: str) -> bool:
    """
    التحقق من صحة عنوان URL

    Args:
        url: عنوان URL للتحقق منه

    Returns:
        True إذا كان العنوان صالحاً، False خلاف ذلك
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except (ValueError, AttributeError):
        return False


def paginate_results(items: List[Any], page: int,
                     page_size: int) -> Dict[str, Any]:
    """
    تقسيم النتائج إلى صفحات

    Args:
        items: قائمة العناصر
        page: رقم الصفحة (يبدأ من 1)
        page_size: عدد العناصر في الصفحة

    Returns:
        قاموس يحتوي على العناصر المقسمة والبيانات الوصفية للصفحات
    """
    # التأكد من أن رقم الصفحة وحجم الصفحة صالحان
    page = max(1, page)
    page_size = max(1, page_size)

    # حساب إجمالي عدد الصفحات
    total_items = len(items)
    total_pages = (total_items + page_size - 1) // page_size

    # حساب مؤشرات البداية والنهاية
    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, total_items)

    # الحصول على العناصر في الصفحة الحالية
    page_items = items[start_idx:end_idx]

    return {
        "items": page_items,
        "metadata": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }


def serialize_model(model: Any) -> Dict[str, Any]:
    """
    تحويل نموذج قاعدة البيانات إلى قاموس

    Args:
        model: نموذج قاعدة البيانات

    Returns:
        قاموس يمثل النموذج
    """
    result = {}
    for column in model.__table__.columns:
        value = getattr(model, column.name)
        if isinstance(value, datetime.datetime):
            value = format_date(value)
        result[column.name] = value
    return result
