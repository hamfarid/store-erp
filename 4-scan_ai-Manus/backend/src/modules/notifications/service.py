"""
مسار الملف: /home/ubuntu/implemented_files/v3/src/modules/notifications/service.py
الوصف: خدمة مديول الإشعارات
المؤلف: فريق Gaara ERP
تاريخ الإنشاء: 29 مايو 2025
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.database import db_session
from src.modules.notifications.config import (
    NOTIFICATION_CHANNELS,
    NOTIFICATION_PRIORITIES,
    NOTIFICATION_TYPES,
    NOTIFICATIONS_CONFIG,
)
from src.modules.notifications.models import (
    Notification,
    NotificationChannel,
    NotificationPreference,
    NotificationTemplate,
    ScheduledNotification,
    WebhookSubscription,
)
from src.modules.notifications.schemas import (
    NotificationBulkActionSchema,
    NotificationCreateSchema,
    NotificationFilterSchema,
    NotificationPreferenceCreateSchema,
    NotificationPreferenceSchema,
    NotificationSchema,
    NotificationSendTestSchema,
    NotificationTemplateCreateSchema,
    NotificationTemplateSchema,
    ScheduledNotificationCreateSchema,
    ScheduledNotificationSchema,
    WebhookSubscriptionCreateSchema,
    WebhookSubscriptionSchema,
)
from src.modules.user_management.models import User

# إعداد المسجل
logger = logging.getLogger(__name__)

# إعداد Jinja2
jinja_env = Environment(
    loader=FileSystemLoader(NOTIFICATIONS_CONFIG["EMAIL_TEMPLATE_DIR"]),
    autoescape=select_autoescape(["html", "xml"])
)


class NotificationService:
    """خدمة الإشعارات"""

    def __init__(self, db: Session = None):
        """
        تهيئة خدمة الإشعارات

        المعلمات:
            db: جلسة قاعدة البيانات (اختياري)
        """
        self.db = db or db_session

    def create_notification(
            self,
            data: NotificationCreateSchema) -> NotificationSchema:
        """
        إنشاء إشعار جديد

        المعلمات:
            data: بيانات الإشعار

        العائد:
            NotificationSchema: الإشعار الذي تم إنشاؤه

        يثير:
            ValueError: إذا كان المستخدم غير موجود
            SQLAlchemyError: إذا حدث خطأ في قاعدة البيانات
        """
        try:
            # التحقق من وجود المستخدم إذا تم تحديده
            if data.user_id:
                user = self.db.query(User).filter(
                    User.id == data.user_id).first()
                if not user:
                    raise ValueError(
                        f"المستخدم بالمعرف {data.user_id} غير موجود")

            # إنشاء الإشعار
            notification = Notification(
                user_id=data.user_id,
                title=data.title,
                content=data.content,
                type=data.type,
                priority=data.priority,
                metadata=data.metadata,
                expires_at=data.expires_at
            )
            self.db.add(notification)
            self.db.flush()  # للحصول على معرف الإشعار

            # إنشاء قنوات الإشعار
            for channel_code in data.channels:
                channel = NotificationChannel(
                    notification_id=notification.id,
                    channel=channel_code,
                    status="pending"
                )
                self.db.add(channel)

            self.db.commit()
            self.db.refresh(notification)

            # إرسال الإشعار عبر القنوات المطلوبة (يمكن تشغيله في مهمة خلفية)
            self.send_notification(notification.id)

            return NotificationSchema.from_orm(notification)
        except SQLAlchemyError as e:
            logger.error(f"خطأ في إنشاء الإشعار: {str(e)}")
            self.db.rollback()
            raise
        except ValueError as e:
            logger.error(f"خطأ في إنشاء الإشعار: {str(e)}")
            self.db.rollback()
            raise

    def get_notifications(
            self,
            filters: NotificationFilterSchema,
            skip: int = 0,
            limit: int = 100) -> List[NotificationSchema]:
        """
        الحصول على قائمة الإشعارات مع التصفية

        المعلمات:
            filters: معايير التصفية
            skip: عدد السجلات لتخطيها
            limit: الحد الأقصى لعدد السجلات

        العائد:
            List[NotificationSchema]: قائمة الإشعارات
        """
        try:
            query = self.db.query(Notification)

            if filters.user_id is not None:
                query = query.filter(Notification.user_id == filters.user_id)
            if filters.type is not None:
                query = query.filter(Notification.type == filters.type)
            if filters.priority is not None:
                query = query.filter(Notification.priority == filters.priority)
            if filters.is_read is not None:
                query = query.filter(Notification.is_read == filters.is_read)
            if filters.is_archived is not None:
                query = query.filter(
                    Notification.is_archived == filters.is_archived)
            if filters.start_date is not None:
                query = query.filter(
                    Notification.created_at >= filters.start_date)
            if filters.end_date is not None:
                query = query.filter(
                    Notification.created_at <= filters.end_date)

            notifications = query.order_by(
                Notification.created_at.desc()).offset(skip).limit(limit).all()
            return [NotificationSchema.from_orm(n) for n in notifications]
        except SQLAlchemyError as e:
            logger.error(f"خطأ في الحصول على الإشعارات: {str(e)}")
            raise

    def get_notification_by_id(
            self,
            notification_id: int) -> Optional[NotificationSchema]:
        """
        الحصول على إشعار بواسطة المعرف

        المعلمات:
            notification_id: معرف الإشعار

        العائد:
            Optional[NotificationSchema]: الإشعار أو None إذا لم يتم العثور عليه
        """
        try:
            notification = self.db.query(Notification).filter(
                Notification.id == notification_id).first()
            return NotificationSchema.from_orm(
                notification) if notification else None
        except SQLAlchemyError as e:
            logger.error(
                f"خطأ في الحصول على الإشعار بالمعرف {notification_id}: {str(e)}")
            raise

    def mark_notification_as_read(
            self, notification_id: int) -> Optional[NotificationSchema]:
        """
        تحديد إشعار كمقروء

        المعلمات:
            notification_id: معرف الإشعار

        العائد:
            Optional[NotificationSchema]: الإشعار المحدث أو None إذا لم يتم العثور عليه
        """
        try:
            notification = self.db.query(Notification).filter(
                Notification.id == notification_id).first()
            if notification:
                notification.is_read = True
                notification.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(notification)
                return NotificationSchema.from_orm(notification)
            return None
        except SQLAlchemyError as e:
            logger.error(
                f"خطأ في تحديد الإشعار {notification_id} كمقروء: {str(e)}")
            self.db.rollback()
            raise

    def mark_notification_as_unread(
            self, notification_id: int) -> Optional[NotificationSchema]:
        """
        تحديد إشعار كغير مقروء

        المعلمات:
            notification_id: معرف الإشعار

        العائد:
            Optional[NotificationSchema]: الإشعار المحدث أو None إذا لم يتم العثور عليه
        """
        try:
            notification = self.db.query(Notification).filter(
                Notification.id == notification_id).first()
            if notification:
                notification.is_read = False
                notification.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(notification)
                return NotificationSchema.from_orm(notification)
            return None
        except SQLAlchemyError as e:
            logger.error(
                f"خطأ في تحديد الإشعار {notification_id} كغير مقروء: {str(e)}")
            self.db.rollback()
            raise

    def archive_notification(
            self,
            notification_id: int) -> Optional[NotificationSchema]:
        """
        أرشفة إشعار

        المعلمات:
            notification_id: معرف الإشعار

        العائد:
            Optional[NotificationSchema]: الإشعار المحدث أو None إذا لم يتم العثور عليه
        """
        try:
            notification = self.db.query(Notification).filter(
                Notification.id == notification_id).first()
            if notification:
                notification.is_archived = True
                notification.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(notification)
                return NotificationSchema.from_orm(notification)
            return None
        except SQLAlchemyError as e:
            logger.error(f"خطأ في أرشفة الإشعار {notification_id}: {str(e)}")
            self.db.rollback()
            raise

    def unarchive_notification(
            self,
            notification_id: int) -> Optional[NotificationSchema]:
        """
        إلغاء أرشفة إشعار

        المعلمات:
            notification_id: معرف الإشعار

        العائد:
            Optional[NotificationSchema]: الإشعار المحدث أو None إذا لم يتم العثور عليه
        """
        try:
            notification = self.db.query(Notification).filter(
                Notification.id == notification_id).first()
            if notification:
                notification.is_archived = False
                notification.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(notification)
                return NotificationSchema.from_orm(notification)
            return None
        except SQLAlchemyError as e:
            logger.error(
                f"خطأ في إلغاء أرشفة الإشعار {notification_id}: {str(e)}")
            self.db.rollback()
            raise

    def delete_notification(self, notification_id: int) -> bool:
        """
        حذف إشعار

        المعلمات:
            notification_id: معرف الإشعار

        العائد:
            bool: صحيح إذا تم الحذف بنجاح
        """
        try:
            notification = self.db.query(Notification).filter(
                Notification.id == notification_id).first()
            if notification:
                self.db.delete(notification)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            logger.error(f"خطأ في حذف الإشعار {notification_id}: {str(e)}")
            self.db.rollback()
            raise

    def bulk_action(
            self, data: NotificationBulkActionSchema) -> Dict[str, int]:
        """
        تنفيذ إجراء جماعي على الإشعارات

        المعلمات:
            data: بيانات الإجراء الجماعي

        العائد:
            Dict[str, int]: قاموس يحتوي على عدد الإشعارات المتأثرة
        """
        try:
            affected_count = 0
            query = self.db.query(Notification).filter(
                Notification.id.in_(data.notification_ids))

            if data.action == "mark_read":
                affected_count = query.update(
                    {"is_read": True, "updated_at": datetime.utcnow()}, synchronize_session=False)
            elif data.action == "mark_unread":
                affected_count = query.update(
                    {"is_read": False, "updated_at": datetime.utcnow()}, synchronize_session=False)
            elif data.action == "archive":
                affected_count = query.update(
                    {"is_archived": True, "updated_at": datetime.utcnow()}, synchronize_session=False)
            elif data.action == "unarchive":
                affected_count = query.update(
                    {"is_archived": False, "updated_at": datetime.utcnow()}, synchronize_session=False)
            elif data.action == "delete":
                affected_count = query.delete(synchronize_session=False)

            self.db.commit()
            return {"affected_count": affected_count}
        except SQLAlchemyError as e:
            logger.error(
                f"خطأ في تنفيذ الإجراء الجماعي ({data.action}): {str(e)}")
            self.db.rollback()
            raise

    def send_notification(self, notification_id: int) -> None:
        """
        إرسال إشعار عبر القنوات المطلوبة (يمكن تشغيله في مهمة خلفية)

        المعلمات:
            notification_id: معرف الإشعار
        """
        try:
            notification = self.db.query(Notification).filter(
                Notification.id == notification_id).first()
            if not notification:
                logger.warning(
                    f"الإشعار بالمعرف {notification_id} غير موجود للإرسال")
                return

            channels = self.db.query(NotificationChannel).filter(
                NotificationChannel.notification_id == notification_id,
                NotificationChannel.status == "pending"
            ).all()

            for channel in channels:
                try:
                    if channel.channel == NOTIFICATION_CHANNELS[
                            "EMAIL"] and NOTIFICATIONS_CONFIG["EMAIL_NOTIFICATIONS_ENABLED"]:
                        self._send_email_notification(notification, channel)
                    elif channel.channel == NOTIFICATION_CHANNELS["IN_APP"] and NOTIFICATIONS_CONFIG["IN_APP_NOTIFICATIONS_ENABLED"]:
                        self._send_in_app_notification(notification, channel)
                    elif channel.channel == NOTIFICATION_CHANNELS["SMS"] and NOTIFICATIONS_CONFIG["SMS_NOTIFICATIONS_ENABLED"]:
                        self._send_sms_notification(notification, channel)
                    elif channel.channel == NOTIFICATION_CHANNELS["PUSH"] and NOTIFICATIONS_CONFIG["PUSH_NOTIFICATIONS_ENABLED"]:
                        self._send_push_notification(notification, channel)
                    elif channel.channel == NOTIFICATION_CHANNELS["WEBHOOK"] and NOTIFICATIONS_CONFIG["WEBHOOK_NOTIFICATIONS_ENABLED"]:
                        self._send_webhook_notification(notification, channel)
                    else:
                        channel.status = "skipped"
                        channel.error = "القناة غير مفعلة أو غير مدعومة"

                    channel.sent_at = datetime.utcnow()
                    channel.updated_at = datetime.utcnow()
                    self.db.commit()
                except Exception as e:
                    logger.error(
                        f"خطأ في إرسال الإشعار {notification_id} عبر قناة {channel.channel}: {str(e)}")
                    channel.status = "failed"
                    channel.error = str(e)
                    channel.updated_at = datetime.utcnow()
                    self.db.commit()
        except SQLAlchemyError as e:
            logger.error(f"خطأ في إرسال الإشعار {notification_id}: {str(e)}")
            self.db.rollback()

    def _send_email_notification(
            self,
            notification: Notification,
            channel: NotificationChannel) -> None:
        """
        إرسال إشعار عبر البريد الإلكتروني

        المعلمات:
            notification: كائن الإشعار
            channel: كائن قناة الإشعار
        """
        if not notification.user or not notification.user.email:
            channel.status = "failed"
            channel.error = "البريد الإلكتروني للمستخدم غير متوفر"
            return

        # الحصول على القالب
        template_code = notification.metadata.get(
            "template_code", notification.type)
        template = self.get_template_by_code(template_code)

        if not template or not template.content_html:
            # استخدام محتوى الإشعار مباشرة إذا لم يكن هناك قالب
            subject = notification.title
            jinja_env.get_template(template.content_html).render(
                {
                    "user": notification.user,
                    "notification": notification,
                    "title": notification.title,
                    "content": notification.content,
                    **(notification.metadata or {})
                }
            )
        else:
            subject = template.subject or notification.title
            # تعبئة القالب بالمتغيرات
            variables = {
                "user": notification.user,
                "notification": notification,
                "title": notification.title,
                "content": notification.content,
                **(notification.metadata or {})
            }
            # Generate HTML content using template
            jinja_env.get_template(template.content_html).render(variables)

        # إرسال البريد الإلكتروني (استخدام مكتبة مثل smtplib أو خدمة خارجية)
        # ... كود إرسال البريد الإلكتروني هنا ...
        logger.info(
            f"إرسال بريد إلكتروني إلى {notification.user.email} بعنوان: {subject}")

        channel.status = "sent"

    def _send_in_app_notification(
            self,
            notification: Notification,
            channel: NotificationChannel) -> None:
        """
        إرسال إشعار داخل النظام (لا يتطلب إجراء فعلي هنا، يتم عرضه في الواجهة)

        المعلمات:
            notification: كائن الإشعار
            channel: كائن قناة الإشعار
        """
        logger.info(
            f"إشعار داخل النظام للمستخدم {notification.user_id}: {notification.title}")
        channel.status = "sent"

    def _send_sms_notification(
            self,
            notification: Notification,
            channel: NotificationChannel) -> None:
        """
        إرسال إشعار عبر الرسائل القصيرة

        المعلمات:
            notification: كائن الإشعار
            channel: كائن قناة الإشعار
        """
        if not notification.user or not notification.user.phone:
            channel.status = "failed"
            channel.error = "رقم هاتف المستخدم غير متوفر"
            return

        # الحصول على القالب
        template_code = notification.metadata.get(
            "template_code", notification.type)
        template = self.get_template_by_code(template_code)

        if not template or not template.content_sms:
            # استخدام محتوى الإشعار مباشرة إذا لم يكن هناك قالب
            sms_content = f"{notification.title}: {notification.content}"
        else:
            # تعبئة القالب بالمتغيرات
            variables = {
                "user": notification.user,
                "notification": notification,
                "title": notification.title,
                "content": notification.content,
                **(notification.metadata or {})
            }
            sms_content = template.content_sms.format(**variables)

        # إرسال الرسالة القصيرة (استخدام خدمة مثل Twilio)
        # ... كود إرسال الرسالة القصيرة هنا ...
        logger.info(
            f"إرسال رسالة قصيرة إلى {notification.user.phone}: {sms_content}")

        channel.status = "sent"

    def _send_push_notification(
            self,
            notification: Notification,
            channel: NotificationChannel) -> None:
        """
        إرسال إشعار عبر تطبيقات الجوال

        المعلمات:
            notification: كائن الإشعار
            channel: كائن قناة الإشعار
        """
        # الحصول على رمز الجهاز للمستخدم
        # ... كود الحصول على رمز الجهاز هنا ...
        device_token = "..."

        if not device_token:
            channel.status = "failed"
            channel.error = "رمز الجهاز للمستخدم غير متوفر"
            return

        # TODO: Implement push notification content generation
        # template_code = notification.metadata.get("template_code", notification.type)
        # template = self.get_template_by_code(template_code)
        # if not template or not template.content_push:
        #     Use notification.content for push notification
        # else:
        # Use template.content_push.format(**variables) for push notification

        # إرسال الإشعار (استخدام خدمة مثل Firebase)
        # ... كود إرسال الإشعار هنا ...
        logger.info(
            f"إرسال إشعار Push إلى {device_token}: {notification.title}")

        channel.status = "sent"

    def _send_webhook_notification(
            self,
            notification: Notification,
            channel: NotificationChannel) -> None:
        """
        إرسال إشعار عبر Webhook

        المعلمات:
            notification: كائن الإشعار
            channel: كائن قناة الإشعار
        """
        # الحصول على اشتراكات Webhook ذات الصلة
        # ... كود الحصول على الاشتراكات هنا ...
        subscriptions = []

        for sub in subscriptions:
            try:
                # إرسال الطلب إلى Webhook
                # ... كود إرسال الطلب هنا ...
                logger.info(f"إرسال إشعار Webhook إلى {sub.url}")
            except Exception as e:
                logger.error(f"خطأ في إرسال Webhook إلى {sub.url}: {str(e)}")

        channel.status = "sent"

    # --- إدارة القوالب --- #

    def create_template(
            self,
            data: NotificationTemplateCreateSchema) -> NotificationTemplateSchema:
        """
        إنشاء قالب إشعار جديد

        المعلمات:
            data: بيانات القالب

        العائد:
            NotificationTemplateSchema: القالب الذي تم إنشاؤه
        """
        try:
            template = NotificationTemplate(**data.dict())
            self.db.add(template)
            self.db.commit()
            self.db.refresh(template)
            return NotificationTemplateSchema.from_orm(template)
        except SQLAlchemyError as e:
            logger.error(f"خطأ في إنشاء قالب الإشعار: {str(e)}")
            self.db.rollback()
            raise

    def get_templates(
            self,
            skip: int = 0,
            limit: int = 100) -> List[NotificationTemplateSchema]:
        """
        الحصول على قائمة قوالب الإشعارات

        المعلمات:
            skip: عدد السجلات لتخطيها
            limit: الحد الأقصى لعدد السجلات

        العائد:
            List[NotificationTemplateSchema]: قائمة القوالب
        """
        try:
            templates = self.db.query(NotificationTemplate).offset(
                skip).limit(limit).all()
            return [NotificationTemplateSchema.from_orm(t) for t in templates]
        except SQLAlchemyError as e:
            logger.error(f"خطأ في الحصول على قوالب الإشعارات: {str(e)}")
            raise

    def get_template_by_id(
            self,
            template_id: int) -> Optional[NotificationTemplateSchema]:
        """
        الحصول على قالب إشعار بواسطة المعرف

        المعلمات:
            template_id: معرف القالب

        العائد:
            Optional[NotificationTemplateSchema]: القالب أو None إذا لم يتم العثور عليه
        """
        try:
            template = self.db.query(NotificationTemplate).filter(
                NotificationTemplate.id == template_id).first()
            return NotificationTemplateSchema.from_orm(
                template) if template else None
        except SQLAlchemyError as e:
            logger.error(
                f"خطأ في الحصول على القالب بالمعرف {template_id}: {str(e)}")
            raise

    def get_template_by_code(
            self,
            template_code: str) -> Optional[NotificationTemplateSchema]:
        """
        الحصول على قالب إشعار بواسطة الرمز

        المعلمات:
            template_code: رمز القالب

        العائد:
            Optional[NotificationTemplateSchema]: القالب أو None إذا لم يتم العثور عليه
        """
        try:
            template = self.db.query(NotificationTemplate).filter(
                NotificationTemplate.code == template_code).first()
            return NotificationTemplateSchema.from_orm(
                template) if template else None
        except SQLAlchemyError as e:
            logger.error(
                f"خطأ في الحصول على القالب بالرمز {template_code}: {str(e)}")
            raise

    def update_template(
            self,
            template_id: int,
            data: NotificationTemplateCreateSchema) -> Optional[NotificationTemplateSchema]:
        """
        تحديث قالب إشعار

        المعلمات:
            template_id: معرف القالب
            data: بيانات القالب المحدثة

        العائد:
            Optional[NotificationTemplateSchema]: القالب المحدث أو None إذا لم يتم العثور عليه
        """
        try:
            template = self.db.query(NotificationTemplate).filter(
                NotificationTemplate.id == template_id).first()
            if template:
                for key, value in data.dict(exclude_unset=True).items():
                    setattr(template, key, value)
                template.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(template)
                return NotificationTemplateSchema.from_orm(template)
            return None
        except SQLAlchemyError as e:
            logger.error(f"خطأ في تحديث القالب {template_id}: {str(e)}")
            self.db.rollback()
            raise

    def delete_template(self, template_id: int) -> bool:
        """
        حذف قالب إشعار

        المعلمات:
            template_id: معرف القالب

        العائد:
            bool: صحيح إذا تم الحذف بنجاح
        """
        try:
            template = self.db.query(NotificationTemplate).filter(
                NotificationTemplate.id == template_id).first()
            if template:
                self.db.delete(template)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            logger.error(f"خطأ في حذف القالب {template_id}: {str(e)}")
            self.db.rollback()
            raise

    # --- إدارة التفضيلات --- #

    def get_user_preferences(
            self,
            user_id: int) -> List[NotificationPreferenceSchema]:
        """
        الحصول على تفضيلات الإشعارات للمستخدم

        المعلمات:
            user_id: معرف المستخدم

        العائد:
            List[NotificationPreferenceSchema]: قائمة التفضيلات
        """
        try:
            preferences = self.db.query(NotificationPreference).filter(
                NotificationPreference.user_id == user_id).all()
            return [NotificationPreferenceSchema.from_orm(
                p) for p in preferences]
        except SQLAlchemyError as e:
            logger.error(
                f"خطأ في الحصول على تفضيلات المستخدم {user_id}: {str(e)}")
            raise

    def update_user_preference(
            self,
            user_id: int,
            data: NotificationPreferenceCreateSchema) -> NotificationPreferenceSchema:
        """
        تحديث تفضيلات الإشعارات للمستخدم

        المعلمات:
            user_id: معرف المستخدم
            data: بيانات التفضيلات المحدثة

        العائد:
            NotificationPreferenceSchema: التفضيلات المحدثة
        """
        try:
            preference = self.db.query(NotificationPreference).filter(
                NotificationPreference.user_id == user_id,
                NotificationPreference.notification_type == data.notification_type).first()

            if preference:
                # تحديث التفضيل الحالي
                preference.email_enabled = data.email_enabled
                preference.in_app_enabled = data.in_app_enabled
                preference.sms_enabled = data.sms_enabled
                preference.push_enabled = data.push_enabled
                preference.updated_at = datetime.utcnow()
            else:
                # إنشاء تفضيل جديد
                preference = NotificationPreference(**data.dict())
                self.db.add(preference)

            self.db.commit()
            self.db.refresh(preference)
            return NotificationPreferenceSchema.from_orm(preference)
        except SQLAlchemyError as e:
            logger.error(f"خطأ في تحديث تفضيلات المستخدم {user_id}: {str(e)}")
            self.db.rollback()
            raise

    # --- إدارة الإشعارات المجدولة --- #

    def create_scheduled_notification(
            self, data: ScheduledNotificationCreateSchema) -> ScheduledNotificationSchema:
        """
        إنشاء إشعار مجدول

        المعلمات:
            data: بيانات الإشعار المجدول

        العائد:
            ScheduledNotificationSchema: الإشعار المجدول الذي تم إنشاؤه
        """
        try:
            scheduled_notification = ScheduledNotification(**data.dict())
            self.db.add(scheduled_notification)
            self.db.commit()
            self.db.refresh(scheduled_notification)
            return ScheduledNotificationSchema.from_orm(scheduled_notification)
        except SQLAlchemyError as e:
            logger.error(f"خطأ في إنشاء إشعار مجدول: {str(e)}")
            self.db.rollback()
            raise

    def process_scheduled_notifications(self) -> int:
        """
        معالجة الإشعارات المجدولة التي حان وقتها

        العائد:
            int: عدد الإشعارات التي تمت معالجتها
        """
        processed_count = 0
        try:
            now = datetime.utcnow()
            scheduled_notifications = self.db.query(ScheduledNotification).filter(
                ScheduledNotification.scheduled_at <= now,
                ScheduledNotification.is_processed.is_(False)).all()

            for sn in scheduled_notifications:
                try:
                    # إنشاء إشعار عادي
                    notification_data = NotificationCreateSchema(
                        user_id=sn.user_id,
                        title=sn.title,
                        content=sn.content,
                        type=sn.type,
                        priority=sn.priority,
                        channels=sn.channels,
                        metadata=sn.metadata
                    )
                    self.create_notification(notification_data)

                    # تحديث حالة الإشعار المجدول
                    sn.is_processed = True
                    sn.processed_at = now
                    sn.updated_at = now
                    self.db.commit()
                    processed_count += 1
                except Exception as e:
                    logger.error(
                        f"خطأ في معالجة الإشعار المجدول {sn.id}: {str(e)}")
                    # يمكن إضافة منطق لإعادة المحاولة أو تسجيل الخطأ بشكل دائم
                    self.db.rollback()

            return processed_count
        except SQLAlchemyError as e:
            logger.error(f"خطأ في معالجة الإشعارات المجدولة: {str(e)}")
            self.db.rollback()
            return processed_count

    # --- إدارة Webhooks --- #

    def create_webhook_subscription(
            self, data: WebhookSubscriptionCreateSchema) -> WebhookSubscriptionSchema:
        """
        إنشاء اشتراك Webhook جديد

        المعلمات:
            data: بيانات الاشتراك

        العائد:
            WebhookSubscriptionSchema: الاشتراك الذي تم إنشاؤه
        """
        try:
            subscription = WebhookSubscription(**data.dict())
            self.db.add(subscription)
            self.db.commit()
            self.db.refresh(subscription)
            return WebhookSubscriptionSchema.from_orm(subscription)
        except SQLAlchemyError as e:
            logger.error(f"خطأ في إنشاء اشتراك Webhook: {str(e)}")
            self.db.rollback()
            raise

    def get_webhook_subscriptions(
            self,
            skip: int = 0,
            limit: int = 100) -> List[WebhookSubscriptionSchema]:
        """
        الحصول على قائمة اشتراكات Webhook

        المعلمات:
            skip: عدد السجلات لتخطيها
            limit: الحد الأقصى لعدد السجلات

        العائد:
            List[WebhookSubscriptionSchema]: قائمة الاشتراكات
        """
        try:
            subscriptions = self.db.query(
                WebhookSubscription).offset(skip).limit(limit).all()
            return [WebhookSubscriptionSchema.from_orm(
                s) for s in subscriptions]
        except SQLAlchemyError as e:
            logger.error(f"خطأ في الحصول على اشتراكات Webhook: {str(e)}")
            raise

    def update_webhook_subscription(
            self,
            subscription_id: int,
            data: WebhookSubscriptionCreateSchema) -> Optional[WebhookSubscriptionSchema]:
        """
        تحديث اشتراك Webhook

        المعلمات:
            subscription_id: معرف الاشتراك
            data: بيانات الاشتراك المحدثة

        العائد:
            Optional[WebhookSubscriptionSchema]: الاشتراك المحدث أو None إذا لم يتم العثور عليه
        """
        try:
            subscription = self.db.query(WebhookSubscription).filter(
                WebhookSubscription.id == subscription_id).first()
            if subscription:
                for key, value in data.dict(exclude_unset=True).items():
                    setattr(subscription, key, value)
                subscription.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(subscription)
                return WebhookSubscriptionSchema.from_orm(subscription)
            return None
        except SQLAlchemyError as e:
            logger.error(
                f"خطأ في تحديث اشتراك Webhook {subscription_id}: {str(e)}")
            self.db.rollback()
            raise

    def delete_webhook_subscription(self, subscription_id: int) -> bool:
        """
        حذف اشتراك Webhook

        المعلمات:
            subscription_id: معرف الاشتراك

        العائد:
            bool: صحيح إذا تم الحذف بنجاح
        """
        try:
            subscription = self.db.query(WebhookSubscription).filter(
                WebhookSubscription.id == subscription_id).first()
            if subscription:
                self.db.delete(subscription)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            logger.error(
                f"خطأ في حذف اشتراك Webhook {subscription_id}: {str(e)}")
            self.db.rollback()
            raise

    def send_test_notification(
            self, data: NotificationSendTestSchema) -> Dict[str, Any]:
        """
        إرسال إشعار اختباري

        المعلمات:
            data: بيانات الإشعار الاختباري

        العائد:
            Dict[str, Any]: نتيجة الإرسال لكل قناة
        """
        results = {}
        template = self.get_template_by_code(data.template_code)

        if not template:
            raise ValueError(f"القالب بالرمز {data.template_code} غير موجود")

        # إنشاء كائن إشعار وهمي للاختبار
        dummy_notification = Notification(
            id=0,
            user_id=None,
            title=template.subject or "إشعار اختباري",
            content="هذا محتوى إشعار اختباري",
            type=NOTIFICATION_TYPES["SYSTEM"],
            priority=NOTIFICATION_PRIORITIES["MEDIUM"],
            metadata=data.variables or {},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # إنشاء كائن مستخدم وهمي للاختبار
        dummy_user = User(
            id=0,
            email=data.email,
            phone=data.phone
        )
        dummy_notification.user = dummy_user

        for channel_code in data.channels:
            try:
                dummy_channel = NotificationChannel(channel=channel_code)

                if channel_code == NOTIFICATION_CHANNELS["EMAIL"] and data.email:
                    self._send_email_notification(
                        dummy_notification, dummy_channel)
                elif channel_code == NOTIFICATION_CHANNELS["SMS"] and data.phone:
                    self._send_sms_notification(
                        dummy_notification, dummy_channel)
                # يمكن إضافة قنوات أخرى للاختبار
                else:
                    dummy_channel.status = "skipped"
                    dummy_channel.error = "القناة غير مدعومة للاختبار أو البيانات المطلوبة غير متوفرة"

                results[channel_code] = {
                    "status": dummy_channel.status,
                    "error": dummy_channel.error}
            except Exception as e:
                logger.error(
                    f"خطأ في إرسال إشعار اختباري عبر قناة {channel_code}: {str(e)}")
                results[channel_code] = {"status": "failed", "error": str(e)}

        return results
