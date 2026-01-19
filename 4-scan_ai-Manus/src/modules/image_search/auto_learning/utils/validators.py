# /home/ubuntu/image_search_integration/auto_learning/utils/validators.py
"""
أدوات التحقق من صحة البيانات لمديول البحث الذاتي الذكي

يحتوي هذا الملف على دوال للتحقق من صحة البيانات المدخلة في مديول البحث الذاتي الذكي،
مثل التحقق من صحة الكلمات المفتاحية والمصادر ومحركات البحث.
"""

import re
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

from ..config import (
    CATEGORIES, PLANT_PARTS, RELATION_TYPES, TRUST_LEVEL_MIN,
    TRUST_LEVEL_MAX, LOAD_BALANCING_STRATEGIES
)


def validate_keyword(keyword_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    التحقق من صحة بيانات الكلمة المفتاحية

    Args:
        keyword_data: بيانات الكلمة المفتاحية للتحقق منها

    Returns:
        قائمة بالأخطاء إن وجدت، أو قائمة فارغة إذا كانت البيانات صحيحة
    """
    errors = {}

    # التحقق من النص
    if 'text' not in keyword_data or not keyword_data['text']:
        errors['text'] = ["نص الكلمة المفتاحية مطلوب"]
    elif len(keyword_data['text']) < 2:
        errors['text'] = ["نص الكلمة المفتاحية يجب أن يكون أكثر من حرف واحد"]
    elif len(keyword_data['text']) > 100:
        errors['text'] = ["نص الكلمة المفتاحية يجب أن يكون أقل من 100 حرف"]

    # التحقق من التصنيف
    if 'category' not in keyword_data or not keyword_data['category']:
        errors['category'] = ["تصنيف الكلمة المفتاحية مطلوب"]
    elif keyword_data['category'] not in CATEGORIES:
        errors['category'] = [f"تصنيف الكلمة المفتاحية غير صالح. القيم المسموح بها: {', '.join(CATEGORIES)}"]

    # التحقق من المرادفات
    if 'synonyms' in keyword_data and keyword_data['synonyms']:
        if not isinstance(keyword_data['synonyms'], list):
            errors['synonyms'] = ["المرادفات يجب أن تكون قائمة"]
        elif any(not isinstance(syn, str) for syn in keyword_data['synonyms']):
            errors['synonyms'] = ["جميع المرادفات يجب أن تكون نصوص"]

    # التحقق من أجزاء النبات
    if 'plant_parts' in keyword_data and keyword_data['plant_parts']:
        if not isinstance(keyword_data['plant_parts'], list):
            errors['plant_parts'] = ["أجزاء النبات يجب أن تكون قائمة"]
        elif any(part not in PLANT_PARTS for part in keyword_data['plant_parts']):
            errors['plant_parts'] = [f"أجزاء النبات غير صالحة. القيم المسموح بها: {', '.join(PLANT_PARTS)}"]

    return errors


def validate_source(source_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    التحقق من صحة بيانات المصدر

    Args:
        source_data: بيانات المصدر للتحقق منها

    Returns:
        قائمة بالأخطاء إن وجدت، أو قائمة فارغة إذا كانت البيانات صحيحة
    """
    errors = {}

    # التحقق من النطاق
    if 'domain' not in source_data or not source_data['domain']:
        errors['domain'] = ["نطاق المصدر مطلوب"]
    else:
        # التحقق من صحة تنسيق النطاق
        try:
            result = urlparse(source_data['domain'])
            if not all([result.scheme, result.netloc]):
                errors['domain'] = ["نطاق المصدر غير صالح"]
        except (ValueError, AttributeError):
            errors['domain'] = ["نطاق المصدر غير صالح"]

    # التحقق من التصنيف
    if 'category' not in source_data or not source_data['category']:
        errors['category'] = ["تصنيف المصدر مطلوب"]

    # التحقق من مستوى الثقة
    if 'trust_level' not in source_data:
        errors['trust_level'] = ["مستوى الثقة مطلوب"]
    elif not isinstance(source_data['trust_level'], int):
        errors['trust_level'] = ["مستوى الثقة يجب أن يكون رقماً صحيحاً"]
    elif source_data['trust_level'] < TRUST_LEVEL_MIN or source_data['trust_level'] > TRUST_LEVEL_MAX:
        errors['trust_level'] = [f"مستوى الثقة يجب أن يكون بين {TRUST_LEVEL_MIN} و {TRUST_LEVEL_MAX}"]

    # التحقق من النطاقات الفرعية
    if 'subdomains' in source_data and source_data['subdomains']:
        if not isinstance(source_data['subdomains'], list):
            errors['subdomains'] = ["النطاقات الفرعية يجب أن تكون قائمة"]
        elif any(not isinstance(subdomain, str) for subdomain in source_data['subdomains']):
            errors['subdomains'] = ["جميع النطاقات الفرعية يجب أن تكون نصوص"]

    return errors


def validate_search_engine(engine_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    التحقق من صحة بيانات محرك البحث

    Args:
        engine_data: بيانات محرك البحث للتحقق منها

    Returns:
        قائمة بالأخطاء إن وجدت، أو قائمة فارغة إذا كانت البيانات صحيحة
    """
    errors = {}

    # التحقق من الاسم
    if 'name' not in engine_data or not engine_data['name']:
        errors['name'] = ["اسم محرك البحث مطلوب"]
    elif len(engine_data['name']) < 2:
        errors['name'] = ["اسم محرك البحث يجب أن يكون أكثر من حرف واحد"]
    elif len(engine_data['name']) > 100:
        errors['name'] = ["اسم محرك البحث يجب أن يكون أقل من 100 حرف"]

    # التحقق من النوع
    if 'type' not in engine_data or not engine_data['type']:
        errors['type'] = ["نوع محرك البحث مطلوب"]

    # التحقق من عنوان URL الأساسي
    if 'base_url' not in engine_data or not engine_data['base_url']:
        errors['base_url'] = ["عنوان URL الأساسي مطلوب"]
    else:
        # التحقق من صحة تنسيق عنوان URL
        try:
            result = urlparse(engine_data['base_url'])
            if not all([result.scheme, result.netloc]):
                errors['base_url'] = ["عنوان URL الأساسي غير صالح"]
        except (ValueError, AttributeError):
            errors['base_url'] = ["عنوان URL الأساسي غير صالح"]

    # التحقق من معلمة الاستعلام
    if 'query_param' not in engine_data or not engine_data['query_param']:
        errors['query_param'] = ["معلمة الاستعلام مطلوبة"]

    # التحقق من الأولوية
    if 'priority' in engine_data:
        if not isinstance(engine_data['priority'], int):
            errors['priority'] = ["الأولوية يجب أن تكون رقماً صحيحاً"]
        elif engine_data['priority'] < 0:
            errors['priority'] = ["الأولوية يجب أن تكون رقماً موجباً"]

    return errors


def validate_keyword_relation(relation_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    التحقق من صحة بيانات العلاقة بين الكلمات المفتاحية

    Args:
        relation_data: بيانات العلاقة للتحقق منها

    Returns:
        قائمة بالأخطاء إن وجدت، أو قائمة فارغة إذا كانت البيانات صحيحة
    """
    errors = {}

    # التحقق من معرف الكلمة المفتاحية المصدر
    if 'source_id' not in relation_data:
        errors['source_id'] = ["معرف الكلمة المفتاحية المصدر مطلوب"]
    elif not isinstance(relation_data['source_id'], int):
        errors['source_id'] = ["معرف الكلمة المفتاحية المصدر يجب أن يكون رقماً صحيحاً"]

    # التحقق من معرف الكلمة المفتاحية المرتبطة
    if 'related_id' not in relation_data:
        errors['related_id'] = ["معرف الكلمة المفتاحية المرتبطة مطلوب"]
    elif not isinstance(relation_data['related_id'], int):
        errors['related_id'] = ["معرف الكلمة المفتاحية المرتبطة يجب أن يكون رقماً صحيحاً"]

    # التحقق من نوع العلاقة
    if 'relation_type' not in relation_data or not relation_data['relation_type']:
        errors['relation_type'] = ["نوع العلاقة مطلوب"]
    elif relation_data['relation_type'] not in RELATION_TYPES:
        errors['relation_type'] = [f"نوع العلاقة غير صالح. القيم المسموح بها: {', '.join(RELATION_TYPES)}"]

    # التحقق من أن الكلمتين المفتاحيتين مختلفتان
    if 'source_id' in relation_data and 'related_id' in relation_data:
        if relation_data['source_id'] == relation_data['related_id']:
            errors['related_id'] = ["لا يمكن إنشاء علاقة بين الكلمة المفتاحية ونفسها"]

    return errors


def validate_load_balancing_strategy(strategy: str) -> bool:
    """
    التحقق من صحة استراتيجية توزيع الحمل

    Args:
        strategy: استراتيجية توزيع الحمل للتحقق منها

    Returns:
        True إذا كانت الاستراتيجية صالحة، False خلاف ذلك
    """
    return strategy in LOAD_BALANCING_STRATEGIES
