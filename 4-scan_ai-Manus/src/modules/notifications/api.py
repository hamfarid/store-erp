"""
مسار الملف: /home/ubuntu/implemented_files/v3/src/modules/notifications/api.py
الوصف: واجهة برمجة التطبيقات لمديول الإشعارات
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.modules.notifications import notifications_blueprint
from src.modules.notifications.service import NotificationService
from src.modules.notifications.schemas import (
    NotificationCreateSchema, NotificationTemplateCreateSchema,
    NotificationPreferenceCreateSchema, ScheduledNotificationCreateSchema,
    WebhookSubscriptionCreateSchema, NotificationBulkActionSchema, NotificationFilterSchema,
    NotificationSendTestSchema
)
from src.utils.api_utils import validate_schema, paginate_response, error_response


@notifications_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    """
    الحصول على قائمة الإشعارات للمستخدم الحالي

    المعلمات:
        page: رقم الصفحة (اختياري، افتراضي: 1)
        per_page: عدد العناصر في الصفحة (اختياري، افتراضي: 20)
        type: نوع الإشعار (اختياري)
        priority: أولوية الإشعار (اختياري)
        is_read: حالة القراءة (اختياري)
        is_archived: حالة الأرشفة (اختياري)
        start_date: تاريخ البداية (اختياري)
        end_date: تاريخ النهاية (اختياري)

    العائد:
        قائمة الإشعارات مع معلومات الصفحات
    """
    try:
        user_id = get_jwt_identity()
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        # استخراج معايير التصفية من المعلمات
        filters = NotificationFilterSchema(
            user_id=user_id,
            type=request.args.get('type'),
            priority=request.args.get('priority'),
            is_read=request.args.get('is_read', type=bool, default=None),
            is_archived=request.args.get('is_archived', type=bool, default=None),
            start_date=request.args.get('start_date'),
            end_date=request.args.get('end_date')
        )

        service = NotificationService()
        notifications = service.get_notifications(filters, skip=(page - 1) * per_page, limit=per_page)

        return paginate_response(
            items=[n.dict() for n in notifications],
            page=page,
            per_page=per_page,
            total=len(notifications)  # يجب تحسين هذا لاسترجاع العدد الإجمالي من قاعدة البيانات
        )
    except Exception as e:
        return error_response(str(e), 500)


@notifications_blueprint.route('/<int:notification_id>', methods=['GET'])
@jwt_required()
def get_notification(notification_id: int):
    """
    الحصول على إشعار محدد

    المعلمات:
        notification_id: معرف الإشعار

    العائد:
        تفاصيل الإشعار
    """
    try:
        user_id = get_jwt_identity()
        service = NotificationService()
        notification = service.get_notification_by_id(notification_id)

        if not notification:
            return error_response("الإشعار غير موجود", 404)

        # التحقق من أن الإشعار ينتمي للمستخدم الحالي
        if notification.user_id != user_id:
            return error_response("غير مصرح بالوصول إلى هذا الإشعار", 403)

        return jsonify(notification.dict())
    except Exception as e:
        return error_response(str(e), 500)


@notifications_blueprint.route('/', methods=['POST'])
@jwt_required()
def create_notification():
    """
    إنشاء إشعار جديد

    المعلمات (JSON):
        user_id: معرف المستخدم (اختياري)
        title: عنوان الإشعار
        content: محتوى الإشعار
        type: نوع الإشعار
        priority: أولوية الإشعار
        channels: قنوات الإشعار
        metadata: بيانات وصفية (اختياري)
        expires_at: تاريخ انتهاء الصلاحية (اختياري)

    العائد:
        الإشعار الذي تم إنشاؤه
    """
    try:
        data = validate_schema(NotificationCreateSchema, request.json)
        service = NotificationService()
        notification = service.create_notification(data)
        return jsonify(notification.dict()), 201
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)


@notifications_blueprint.route('/<int:notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_as_read(notification_id: int):
    """
    تحديد إشعار كمقروء

    المعلمات:
        notification_id: معرف الإشعار

    العائد:
        الإشعار المحدث
    """
    try:
        user_id = get_jwt_identity()
        service = NotificationService()
        notification = service.get_notification_by_id(notification_id)

        if not notification:
            return error_response("الإشعار غير موجود", 404)

        # التحقق من أن الإشعار ينتمي للمستخدم الحالي
        if notification.user_id != user_id:
            return error_response("غير مصرح بالوصول إلى هذا الإشعار", 403)

        updated_notification = service.mark_notification_as_read(notification_id)
        return jsonify(updated_notification.dict())
    except Exception as e:
        return error_response(str(e), 500)


@notifications_blueprint.route('/<int:notification_id>/unread', methods=['PUT'])
@jwt_required()
def mark_as_unread(notification_id: int):
    """
    تحديد إشعار كغير مقروء

    المعلمات:
        notification_id: معرف الإشعار

    العائد:
        الإشعار المحدث
    """
    try:
        user_id = get_jwt_identity()
        service = NotificationService()
        notification = service.get_notification_by_id(notification_id)

        if not notification:
            return error_response("الإشعار غير موجود", 404)

        # التحقق من أن الإشعار ينتمي للمستخدم الحالي
        if notification.user_id != user_id:
            return error_response("غير مصرح بالوصول إلى هذا الإشعار", 403)

        updated_notification = service.mark_notification_as_unread(notification_id)
        return jsonify(updated_notification.dict())
    except Exception as e:
        return error_response(str(e), 500)


@notifications_blueprint.route('/<int:notification_id>/archive', methods=['PUT'])
@jwt_required()
def archive_notification(notification_id: int):
    """
    أرشفة إشعار

    المعلمات:
        notification_id: معرف الإشعار

    العائد:
        الإشعار المحدث
    """
    try:
        user_id = get_jwt_identity()
        service = NotificationService()
        notification = service.get_notification_by_id(notification_id)

        if not notification:
            return error_response("الإشعار غير موجود", 404)

        # التحقق من أن الإشعار ينتمي للمستخدم الحالي
        if notification.user_id != user_id:
            return error_response("غير مصرح بالوصول إلى هذا الإشعار", 403)

        updated_notification = service.archive_notification(notification_id)
        return jsonify(updated_notification.dict())
    except Exception as e:
        return error_response(str(e), 500)


@notifications_blueprint.route('/<int:notification_id>/unarchive', methods=['PUT'])
@jwt_required()
def unarchive_notification(notification_id: int):
    """
    إلغاء أرشفة إشعار

    المعلمات:
        notification_id: معرف الإشعار

    العائد:
        الإشعار المحدث
    """
    try:
        user_id = get_jwt_identity()
        service = NotificationService()
        notification = service.get_notification_by_id(notification_id)

        if not notification:
            return error_response("الإشعار غير موجود", 404)

        # التحقق من أن الإشعار ينتمي للمستخدم الحالي
        if notification.user_id != user_id:
            return error_response("غير مصرح بالوصول إلى هذا الإشعار", 403)

        updated_notification = service.unarchive_notification(notification_id)
        return jsonify(updated_notification.dict())
    except Exception as e:
        return error_response(str(e), 500)


@notifications_blueprint.route('/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id: int):
    """
    حذف إشعار

    المعلمات:
        notification_id: معرف الإشعار

    العائد:
        رسالة نجاح
    """
    try:
        user_id = get_jwt_identity()
        service = NotificationService()
        notification = service.get_notification_by_id(notification_id)

        if not notification:
            return error_response("الإشعار غير موجود", 404)

        # التحقق من أن الإشعار ينتمي للمستخدم الحالي
        if notification.user_id != user_id:
            return error_response("غير مصرح بالوصول إلى هذا الإشعار", 403)

        success = service.delete_notification(notification_id)
        if success:
            return jsonify({"message": "تم حذف الإشعار بنجاح"})
        else:
            return error_response("فشل في حذف الإشعار", 500)
    except Exception as e:
        return error_response(str(e), 500)


@notifications_blueprint.route('/bulk-action', methods=['POST'])
@jwt_required()
def bulk_action():
    """
    تنفيذ إجراء جماعي على الإشعارات

    المعلمات (JSON):
        notification_ids: قائمة معرفات الإشعارات
        action: الإجراء المطلوب (mark_read, mark_unread, archive, unarchive, delete)

    العائد:
        عدد الإشعارات المتأثرة
    """
    try:
        user_id = get_jwt_identity()
        data = validate_schema(NotificationBulkActionSchema, request.json)

        # التحقق من أن جميع الإشعارات تنتمي للمستخدم الحالي
        service = NotificationService()
        for notification_id in data.notification_ids:
            notification = service.get_notification_by_id(notification_id)
            if not notification or notification.user_id != user_id:
                return error_response(f"غير مصرح بالوصول إلى الإشعار {notification_id}", 403)

        result = service.bulk_action(data)
        return jsonify(result)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)


# --- إدارة القوالب --- #

@notifications_blueprint.route('/templates', methods=['GET'])
@jwt_required()
def get_templates():
    """
    الحصول على قائمة قوالب الإشعارات

    المعلمات:
        page: رقم الصفحة (اختياري، افتراضي: 1)
        per_page: عدد العناصر في الصفحة (اختياري، افتراضي: 20)

    العائد:
        قائمة القوالب مع معلومات الصفحات
    """
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        service = NotificationService()
        templates = service.get_templates(skip=(page - 1) * per_page, limit=per_page)

        return paginate_response(
            items=[t.dict() for t in templates],
            page=page,
            per_page=per_page,
            total=len(templates)  # يجب تحسين هذا لاسترجاع العدد الإجمالي من قاعدة البيانات
        )
    except Exception as e:
        return error_response(str(e), 500)


@notifications_blueprint.route('/templates/<int:template_id>', methods=['GET'])
@jwt_required()
def get_template(template_id: int):
    """
    الحصول على قالب إشعار محدد

    المعلمات:
        template_id: معرف القالب

    العائد:
        تفاصيل القالب
    """
    try:
        service = NotificationService()
        template = service.get_template_by_id(template_id)

        if not template:
            return error_response("القالب غير موجود", 404)

        return jsonify(template.dict())
    except Exception as e:
        return error_response(str(e), 500)


@notifications_blueprint.route('/templates', methods=['POST'])
@jwt_required()
def create_template():
    """
    إنشاء قالب إشعار جديد

    المعلمات (JSON):
        code: رمز القالب
        name: اسم القالب
        description: وصف القالب (اختياري)
        subject: عنوان القالب (اختياري)
        content_html: محتوى HTML (اختياري)
        content_text: محتوى نصي (اختياري)
        content_sms: محتوى SMS (اختياري)
        content_push: محتوى Push (اختياري)
        variables: متغيرات القالب (اختياري)
        is_active: حالة التفعيل (اختياري، افتراضي: true)

    العائد:
        القالب الذي تم إنشاؤه
    """
    try:
        data = validate_schema(NotificationTemplateCreateSchema, request.json)
        service = NotificationService()
        template = service.create_template(data)
        return jsonify(template.dict()), 201
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)


@notifications_blueprint.route('/templates/<int:template_id>', methods=['PUT'])
@jwt_required()
def update_template(template_id: int):
    """
    تحديث قالب إشعار

    المعلمات:
        template_id: معرف القالب

    المعلمات (JSON):
        code: رمز القالب
        name: اسم القالب
        description: وصف القالب (اختياري)
        subject: عنوان القالب (اختياري)
        content_html: محتوى HTML (اختياري)
        content_text: محتوى نصي (اختياري)
        content_sms: محتوى SMS (اختياري)
        content_push: محتوى Push (اختياري)
        variables: متغيرات القالب (اختياري)
        is_active: حالة التفعيل (اختياري)

    العائد:
        القالب المحدث
    """
    try:
        data = validate_schema(NotificationTemplateCreateSchema, request.json)
        service = NotificationService()
        template = service.update_template(template_id, data)

        if not template:
            return error_response("القالب غير موجود", 404)

        return jsonify(template.dict())
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)


@notifications_blueprint.route('/templates/<int:template_id>', methods=['DELETE'])
@jwt_required()
def delete_template(template_id: int):
    """
    حذف قالب إشعار

    المعلمات:
        template_id: معرف القالب

    العائد:
        رسالة نجاح
    """
    try:
        service = NotificationService()
        success = service.delete_template(template_id)

        if success:
            return jsonify({"message": "تم حذف القالب بنجاح"})
        else:
            return error_response("القالب غير موجود", 404)
    except Exception as e:
        return error_response(str(e), 500)


# --- إدارة التفضيلات --- #

@notifications_blueprint.route('/preferences', methods=['GET'])
@jwt_required()
def get_preferences():
    """
    الحصول على تفضيلات الإشعارات للمستخدم الحالي

    العائد:
        قائمة التفضيلات
    """
    try:
        user_id = get_jwt_identity()
        service = NotificationService()
        preferences = service.get_user_preferences(user_id)

        return jsonify([p.dict() for p in preferences])
    except Exception as e:
        return error_response(str(e), 500)


@notifications_blueprint.route('/preferences', methods=['PUT'])
@jwt_required()
def update_preference():
    """
    تحديث تفضيلات الإشعارات للمستخدم الحالي

    المعلمات (JSON):
        notification_type: نوع الإشعار
        email_enabled: تفعيل البريد الإلكتروني
        in_app_enabled: تفعيل الإشعارات داخل النظام
        sms_enabled: تفعيل الرسائل القصيرة
        push_enabled: تفعيل إشعارات Push

    العائد:
        التفضيلات المحدثة
    """
    try:
        user_id = get_jwt_identity()
        data = validate_schema(NotificationPreferenceCreateSchema, request.json)
        data.user_id = user_id  # تعيين معرف المستخدم الحالي

        service = NotificationService()
        preference = service.update_user_preference(user_id, data)

        return jsonify(preference.dict())
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)


# --- إدارة الإشعارات المجدولة --- #

@notifications_blueprint.route('/scheduled', methods=['POST'])
@jwt_required()
def create_scheduled_notification():
    """
    إنشاء إشعار مجدول

    المعلمات (JSON):
        user_id: معرف المستخدم (اختياري)
        title: عنوان الإشعار
        content: محتوى الإشعار
        type: نوع الإشعار
        priority: أولوية الإشعار
        channels: قنوات الإشعار
        metadata: بيانات وصفية (اختياري)
        scheduled_at: وقت الجدولة

    العائد:
        الإشعار المجدول الذي تم إنشاؤه
    """
    try:
        data = validate_schema(ScheduledNotificationCreateSchema, request.json)
        service = NotificationService()
        scheduled_notification = service.create_scheduled_notification(data)
        return jsonify(scheduled_notification.dict()), 201
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)


@notifications_blueprint.route('/process-scheduled', methods=['POST'])
@jwt_required()
def process_scheduled_notifications():
    """
    معالجة الإشعارات المجدولة التي حان وقتها

    العائد:
        عدد الإشعارات التي تمت معالجتها
    """
    try:
        service = NotificationService()
        processed_count = service.process_scheduled_notifications()
        return jsonify({"processed_count": processed_count})
    except Exception as e:
        return error_response(str(e), 500)


# --- إدارة Webhooks --- #

@notifications_blueprint.route('/webhooks', methods=['GET'])
@jwt_required()
def get_webhook_subscriptions():
    """
    الحصول على قائمة اشتراكات Webhook

    المعلمات:
        page: رقم الصفحة (اختياري، افتراضي: 1)
        per_page: عدد العناصر في الصفحة (اختياري، افتراضي: 20)

    العائد:
        قائمة الاشتراكات مع معلومات الصفحات
    """
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        service = NotificationService()
        subscriptions = service.get_webhook_subscriptions(skip=(page - 1) * per_page, limit=per_page)

        return paginate_response(
            items=[s.dict() for s in subscriptions],
            page=page,
            per_page=per_page,
            total=len(subscriptions)  # يجب تحسين هذا لاسترجاع العدد الإجمالي من قاعدة البيانات
        )
    except Exception as e:
        return error_response(str(e), 500)


@notifications_blueprint.route('/webhooks', methods=['POST'])
@jwt_required()
def create_webhook_subscription():
    """
    إنشاء اشتراك Webhook جديد

    المعلمات (JSON):
        name: اسم الاشتراك
        url: عنوان URL
        secret: كلمة السر (اختياري)
        events: قائمة الأحداث المشترك بها
        is_active: حالة التفعيل (اختياري، افتراضي: true)

    العائد:
        الاشتراك الذي تم إنشاؤه
    """
    try:
        data = validate_schema(WebhookSubscriptionCreateSchema, request.json)
        service = NotificationService()
        subscription = service.create_webhook_subscription(data)
        return jsonify(subscription.dict()), 201
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)


@notifications_blueprint.route('/webhooks/<int:subscription_id>', methods=['PUT'])
@jwt_required()
def update_webhook_subscription(subscription_id: int):
    """
    تحديث اشتراك Webhook

    المعلمات:
        subscription_id: معرف الاشتراك

    المعلمات (JSON):
        name: اسم الاشتراك
        url: عنوان URL
        secret: كلمة السر (اختياري)
        events: قائمة الأحداث المشترك بها
        is_active: حالة التفعيل (اختياري)

    العائد:
        الاشتراك المحدث
    """
    try:
        data = validate_schema(WebhookSubscriptionCreateSchema, request.json)
        service = NotificationService()
        subscription = service.update_webhook_subscription(subscription_id, data)

        if not subscription:
            return error_response("الاشتراك غير موجود", 404)

        return jsonify(subscription.dict())
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)


@notifications_blueprint.route('/webhooks/<int:subscription_id>', methods=['DELETE'])
@jwt_required()
def delete_webhook_subscription(subscription_id: int):
    """
    حذف اشتراك Webhook

    المعلمات:
        subscription_id: معرف الاشتراك

    العائد:
        رسالة نجاح
    """
    try:
        service = NotificationService()
        success = service.delete_webhook_subscription(subscription_id)

        if success:
            return jsonify({"message": "تم حذف الاشتراك بنجاح"})
        else:
            return error_response("الاشتراك غير موجود", 404)
    except Exception as e:
        return error_response(str(e), 500)


@notifications_blueprint.route('/test', methods=['POST'])
@jwt_required()
def send_test_notification():
    """
    إرسال إشعار اختباري

    المعلمات (JSON):
        template_code: رمز القالب
        email: البريد الإلكتروني (اختياري)
        phone: رقم الهاتف (اختياري)
        variables: متغيرات القالب (اختياري)
        channels: قنوات الإشعار

    العائد:
        نتيجة الإرسال لكل قناة
    """
    try:
        data = validate_schema(NotificationSendTestSchema, request.json)
        service = NotificationService()
        results = service.send_test_notification(data)
        return jsonify(results)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)
