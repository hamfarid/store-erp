# File: /home/ubuntu/clean_project/src/notification_system.py
"""
مسار الملف: /home/ubuntu/clean_project/src/notification_system.py

نظام الإشعارات المتقدم
يوفر إشعارات فورية متعددة القنوات مع دعم الوقت الفعلي
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import json
import logging
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import websockets
import aiohttp
from event_system import EventObserver, Event, EventTypes, event_bus

class NotificationType(Enum):
    """أنواع الإشعارات"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    CRITICAL = "critical"

class NotificationChannel(Enum):
    """قنوات الإشعارات"""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    WEBSOCKET = "websocket"
    SLACK = "slack"
    TELEGRAM = "telegram"
    IN_APP = "in_app"

@dataclass
class Notification:
    """فئة الإشعار"""
    id: str
    title: str
    message: str
    type: NotificationType
    channels: List[NotificationChannel]
    recipients: List[str]
    data: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    scheduled_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    priority: int = 5  # 1-10 (10 = أعلى أولوية)
    template: Optional[str] = None
    attachments: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_expired(self) -> bool:
        """فحص انتهاء صلاحية الإشعار"""
        return self.expires_at is not None and datetime.now() > self.expires_at
    
    def is_ready_to_send(self) -> bool:
        """فحص جاهزية الإشعار للإرسال"""
        if self.is_expired():
            return False
        return self.scheduled_at is None or datetime.now() >= self.scheduled_at

class NotificationProvider(ABC):
    """واجهة مزود الإشعارات"""
    
    @abstractmethod
    async def send(self, notification: Notification) -> bool:
        """إرسال إشعار"""
        pass
    
    @abstractmethod
    def get_channel(self) -> NotificationChannel:
        """الحصول على قناة الإشعار"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """فحص توفر المزود"""
        pass

class EmailProvider(NotificationProvider):
    """مزود إشعارات البريد الإلكتروني"""
    
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str, use_tls: bool = True):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.logger = logging.getLogger('email_provider')
    
    async def send(self, notification: Notification) -> bool:
        """إرسال إشعار بريد إلكتروني"""
        try:
            # إنشاء الرسالة
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = ', '.join(notification.recipients)
            msg['Subject'] = notification.title
            
            # إضافة النص
            body = self._format_message(notification)
            msg.attach(MIMEText(body, 'html' if '<' in body else 'plain'))
            
            # إرسال الرسالة
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls(context=context)
                server.login(self.username, self.password)
                server.send_message(msg)
            
            self.logger.info(f"Email notification {notification.id} sent successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email notification {notification.id}: {e}")
            return False
    
    def _format_message(self, notification: Notification) -> str:
        """تنسيق رسالة البريد الإلكتروني"""
        if notification.template:
            # استخدام قالب مخصص
            return notification.template.format(**notification.data)
        
        # قالب افتراضي
        return f"""
        <html>
        <body>
            <h2>{notification.title}</h2>
            <p>{notification.message}</p>
            <hr>
            <p><small>تم الإرسال في: {notification.created_at.strftime('%Y-%m-%d %H:%M:%S')}</small></p>
        </body>
        </html>
        """
    
    def get_channel(self) -> NotificationChannel:
        return NotificationChannel.EMAIL
    
    def is_available(self) -> bool:
        return bool(self.smtp_server and self.username and self.password)

class WebSocketProvider(NotificationProvider):
    """مزود إشعارات WebSocket للوقت الفعلي"""
    
    def __init__(self):
        self.connections: Dict[str, websockets.WebSocketServerProtocol] = {}
        self.user_connections: Dict[str, List[str]] = {}  # user_id -> connection_ids
        self.logger = logging.getLogger('websocket_provider')
    
    async def send(self, notification: Notification) -> bool:
        """إرسال إشعار عبر WebSocket"""
        try:
            message = {
                'id': notification.id,
                'type': 'notification',
                'data': {
                    'title': notification.title,
                    'message': notification.message,
                    'type': notification.type.value,
                    'created_at': notification.created_at.isoformat(),
                    'data': notification.data
                }
            }
            
            sent_count = 0
            for recipient in notification.recipients:
                if recipient in self.user_connections:
                    for connection_id in self.user_connections[recipient]:
                        if connection_id in self.connections:
                            try:
                                await self.connections[connection_id].send(json.dumps(message))
                                sent_count += 1
                            except websockets.exceptions.ConnectionClosed:
                                # إزالة الاتصال المغلق
                                await self._remove_connection(connection_id)
            
            self.logger.info(f"WebSocket notification {notification.id} sent to {sent_count} connections")
            return sent_count > 0
            
        except Exception as e:
            self.logger.error(f"Failed to send WebSocket notification {notification.id}: {e}")
            return False
    
    async def add_connection(self, user_id: str, websocket: websockets.WebSocketServerProtocol):
        """إضافة اتصال WebSocket جديد"""
        connection_id = f"{user_id}_{datetime.now().timestamp()}"
        self.connections[connection_id] = websocket
        
        if user_id not in self.user_connections:
            self.user_connections[user_id] = []
        self.user_connections[user_id].append(connection_id)
        
        self.logger.info(f"WebSocket connection added for user {user_id}")
        return connection_id
    
    async def _remove_connection(self, connection_id: str):
        """إزالة اتصال WebSocket"""
        if connection_id in self.connections:
            del self.connections[connection_id]
        
        # إزالة من قائمة المستخدمين
        for user_id, connections in self.user_connections.items():
            if connection_id in connections:
                connections.remove(connection_id)
                if not connections:
                    del self.user_connections[user_id]
                break
        
        self.logger.info(f"WebSocket connection {connection_id} removed")
    
    def get_channel(self) -> NotificationChannel:
        return NotificationChannel.WEBSOCKET
    
    def is_available(self) -> bool:
        return True

class SlackProvider(NotificationProvider):
    """مزود إشعارات Slack"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.logger = logging.getLogger('slack_provider')
    
    async def send(self, notification: Notification) -> bool:
        """إرسال إشعار إلى Slack"""
        try:
            # تحديد لون الإشعار حسب النوع
            color_map = {
                NotificationType.INFO: "#36a64f",
                NotificationType.WARNING: "#ff9500",
                NotificationType.ERROR: "#ff0000",
                NotificationType.SUCCESS: "#00ff00",
                NotificationType.CRITICAL: "#8b0000"
            }
            
            payload = {
                "attachments": [{
                    "color": color_map.get(notification.type, "#36a64f"),
                    "title": notification.title,
                    "text": notification.message,
                    "footer": "Gaara Scan AI",
                    "ts": int(notification.created_at.timestamp())
                }]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status == 200:
                        self.logger.info(f"Slack notification {notification.id} sent successfully")
                        return True
                    else:
                        self.logger.error(f"Slack API returned status {response.status}")
                        return False
                        
        except Exception as e:
            self.logger.error(f"Failed to send Slack notification {notification.id}: {e}")
            return False
    
    def get_channel(self) -> NotificationChannel:
        return NotificationChannel.SLACK
    
    def is_available(self) -> bool:
        return bool(self.webhook_url)

class InAppProvider(NotificationProvider):
    """مزود الإشعارات داخل التطبيق"""
    
    def __init__(self):
        self.notifications: Dict[str, List[Notification]] = {}  # user_id -> notifications
        self.logger = logging.getLogger('in_app_provider')
    
    async def send(self, notification: Notification) -> bool:
        """حفظ إشعار داخل التطبيق"""
        try:
            for recipient in notification.recipients:
                if recipient not in self.notifications:
                    self.notifications[recipient] = []
                
                self.notifications[recipient].append(notification)
                
                # الاحتفاظ بآخر 100 إشعار فقط لكل مستخدم
                if len(self.notifications[recipient]) > 100:
                    self.notifications[recipient] = self.notifications[recipient][-100:]
            
            self.logger.info(f"In-app notification {notification.id} stored")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to store in-app notification {notification.id}: {e}")
            return False
    
    def get_notifications(self, user_id: str, unread_only: bool = False) -> List[Notification]:
        """الحصول على إشعارات المستخدم"""
        if user_id not in self.notifications:
            return []
        
        notifications = self.notifications[user_id]
        if unread_only:
            notifications = [n for n in notifications if not n.metadata.get('read', False)]
        
        return notifications
    
    def mark_as_read(self, user_id: str, notification_id: str) -> bool:
        """تمييز إشعار كمقروء"""
        if user_id in self.notifications:
            for notification in self.notifications[user_id]:
                if notification.id == notification_id:
                    notification.metadata['read'] = True
                    return True
        return False
    
    def get_channel(self) -> NotificationChannel:
        return NotificationChannel.IN_APP
    
    def is_available(self) -> bool:
        return True

class NotificationManager:
    """مدير الإشعارات الرئيسي"""
    
    def __init__(self):
        self.providers: Dict[NotificationChannel, NotificationProvider] = {}
        self.templates: Dict[str, str] = {}
        self.user_preferences: Dict[str, Dict[NotificationChannel, bool]] = {}
        self.notification_queue: asyncio.Queue = asyncio.Queue()
        self.is_running = False
        self.worker_task: Optional[asyncio.Task] = None
        self.stats = {
            'total_sent': 0,
            'total_failed': 0,
            'by_channel': {},
            'by_type': {}
        }
        
        # إعداد نظام السجلات
        self.logger = logging.getLogger('notification_manager')
        handler = logging.FileHandler('notifications.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def register_provider(self, provider: NotificationProvider):
        """تسجيل مزود إشعارات"""
        channel = provider.get_channel()
        self.providers[channel] = provider
        self.stats['by_channel'][channel.value] = {'sent': 0, 'failed': 0}
        self.logger.info(f"Provider for {channel.value} registered")
    
    def set_template(self, name: str, template: str):
        """تعيين قالب إشعار"""
        self.templates[name] = template
    
    def set_user_preferences(self, user_id: str, preferences: Dict[NotificationChannel, bool]):
        """تعيين تفضيلات المستخدم للإشعارات"""
        self.user_preferences[user_id] = preferences
    
    async def send_notification(self, notification: Notification) -> Dict[NotificationChannel, bool]:
        """إرسال إشعار عبر القنوات المحددة"""
        results = {}
        
        for channel in notification.channels:
            if channel not in self.providers:
                self.logger.warning(f"No provider registered for channel {channel.value}")
                results[channel] = False
                continue
            
            provider = self.providers[channel]
            if not provider.is_available():
                self.logger.warning(f"Provider for channel {channel.value} is not available")
                results[channel] = False
                continue
            
            # فحص تفضيلات المستخدم
            filtered_recipients = []
            for recipient in notification.recipients:
                user_prefs = self.user_preferences.get(recipient, {})
                if user_prefs.get(channel, True):  # افتراضياً مفعل
                    filtered_recipients.append(recipient)
            
            if not filtered_recipients:
                results[channel] = False
                continue
            
            # إنشاء نسخة من الإشعار مع المستلمين المفلترين
            filtered_notification = Notification(
                id=notification.id,
                title=notification.title,
                message=notification.message,
                type=notification.type,
                channels=[channel],
                recipients=filtered_recipients,
                data=notification.data,
                template=notification.template,
                metadata=notification.metadata
            )
            
            # إرسال الإشعار
            success = await provider.send(filtered_notification)
            results[channel] = success
            
            # تحديث الإحصائيات
            if success:
                self.stats['total_sent'] += 1
                self.stats['by_channel'][channel.value]['sent'] += 1
            else:
                self.stats['total_failed'] += 1
                self.stats['by_channel'][channel.value]['failed'] += 1
            
            # تحديث إحصائيات النوع
            type_key = notification.type.value
            if type_key not in self.stats['by_type']:
                self.stats['by_type'][type_key] = {'sent': 0, 'failed': 0}
            
            if success:
                self.stats['by_type'][type_key]['sent'] += 1
            else:
                self.stats['by_type'][type_key]['failed'] += 1
        
        return results
    
    async def send_notification_async(self, notification: Notification):
        """إضافة إشعار إلى طابور الإرسال غير المتزامن"""
        await self.notification_queue.put(notification)
    
    async def start(self):
        """بدء معالجة الإشعارات غير المتزامنة"""
        if self.is_running:
            return
        
        self.is_running = True
        self.worker_task = asyncio.create_task(self._worker())
        self.logger.info("Notification manager started")
    
    async def stop(self):
        """إيقاف معالجة الإشعارات"""
        self.is_running = False
        if self.worker_task:
            self.worker_task.cancel()
            try:
                await self.worker_task
            except asyncio.CancelledError:
                pass
        self.logger.info("Notification manager stopped")
    
    async def _worker(self):
        """عامل معالجة الإشعارات غير المتزامنة"""
        while self.is_running:
            try:
                notification = await asyncio.wait_for(self.notification_queue.get(), timeout=1.0)
                
                if notification.is_expired():
                    self.logger.info(f"Notification {notification.id} expired, skipping")
                    continue
                
                if not notification.is_ready_to_send():
                    # إعادة جدولة الإشعار
                    await asyncio.sleep(1)
                    await self.notification_queue.put(notification)
                    continue
                
                await self.send_notification(notification)
                
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Worker error: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """الحصول على إحصائيات الإشعارات"""
        return self.stats.copy()

# مراقب الأحداث للإشعارات التلقائية
class NotificationEventObserver(EventObserver):
    """مراقب الأحداث لإرسال الإشعارات التلقائية"""
    
    def __init__(self, notification_manager: NotificationManager):
        self.notification_manager = notification_manager
        self.logger = logging.getLogger('notification_observer')
    
    async def handle_event(self, event: Event) -> bool:
        """معالجة الأحداث وإرسال الإشعارات المناسبة"""
        try:
            notification = self._create_notification_from_event(event)
            if notification:
                await self.notification_manager.send_notification_async(notification)
                return True
            return True
            
        except Exception as e:
            self.logger.error(f"Error handling event {event.id}: {e}")
            return False
    
    def _create_notification_from_event(self, event: Event) -> Optional[Notification]:
        """إنشاء إشعار من حدث"""
        notification_map = {
            EventTypes.USER_CREATED: {
                'title': 'مستخدم جديد',
                'message': f'تم إنشاء مستخدم جديد: {event.data.get("username", "غير محدد")}',
                'type': NotificationType.INFO,
                'channels': [NotificationChannel.IN_APP, NotificationChannel.WEBSOCKET]
            },
            EventTypes.DIAGNOSIS_COMPLETED: {
                'title': 'اكتمل التشخيص',
                'message': f'تم إكمال التشخيص بنجاح: {event.data.get("diagnosis_id", "غير محدد")}',
                'type': NotificationType.SUCCESS,
                'channels': [NotificationChannel.IN_APP, NotificationChannel.WEBSOCKET, NotificationChannel.EMAIL]
            },
            EventTypes.SECURITY_BREACH: {
                'title': 'تحذير أمني',
                'message': f'تم اكتشاف خرق أمني: {event.data.get("message", "غير محدد")}',
                'type': NotificationType.CRITICAL,
                'channels': [NotificationChannel.EMAIL, NotificationChannel.SLACK, NotificationChannel.WEBSOCKET]
            },
            EventTypes.SYSTEM_ERROR: {
                'title': 'خطأ في النظام',
                'message': f'حدث خطأ في النظام: {event.data.get("message", "غير محدد")}',
                'type': NotificationType.ERROR,
                'channels': [NotificationChannel.SLACK, NotificationChannel.EMAIL]
            }
        }
        
        if event.type not in notification_map:
            return None
        
        config = notification_map[event.type]
        
        # تحديد المستلمين بناءً على نوع الحدث
        recipients = self._get_recipients_for_event(event)
        
        return Notification(
            id=f"notif_{event.id}",
            title=config['title'],
            message=config['message'],
            type=config['type'],
            channels=config['channels'],
            recipients=recipients,
            data=event.data
        )
    
    def _get_recipients_for_event(self, event: Event) -> List[str]:
        """تحديد المستلمين للحدث"""
        # يمكن تخصيص هذه الدالة حسب منطق التطبيق
        if event.type in [EventTypes.SECURITY_BREACH, EventTypes.SYSTEM_ERROR]:
            return ['admin']  # إشعار المدراء فقط
        elif event.type == EventTypes.DIAGNOSIS_COMPLETED:
            return [str(event.data.get('user_id', 'admin'))]  # إشعار المستخدم المحدد
        else:
            return ['admin']  # افتراضياً إشعار المدير
    
    def get_supported_events(self) -> List[str]:
        """الأحداث المدعومة"""
        return [
            EventTypes.USER_CREATED,
            EventTypes.DIAGNOSIS_COMPLETED,
            EventTypes.SECURITY_BREACH,
            EventTypes.SYSTEM_ERROR,
            EventTypes.USER_LOGIN,
            EventTypes.FILE_UPLOADED
        ]

# مثيل عام لمدير الإشعارات
notification_manager = NotificationManager()

# دوال مساعدة
def create_notification(title: str, message: str, recipients: List[str], 
                       notification_type: NotificationType = NotificationType.INFO,
                       channels: List[NotificationChannel] = None) -> Notification:
    """إنشاء إشعار بسيط"""
    if channels is None:
        channels = [NotificationChannel.IN_APP, NotificationChannel.WEBSOCKET]
    
    return Notification(
        id=f"notif_{datetime.now().timestamp()}",
        title=title,
        message=message,
        type=notification_type,
        channels=channels,
        recipients=recipients
    )

async def send_quick_notification(title: str, message: str, recipients: List[str],
                                notification_type: NotificationType = NotificationType.INFO):
    """إرسال إشعار سريع"""
    notification = create_notification(title, message, recipients, notification_type)
    return await notification_manager.send_notification(notification)

if __name__ == "__main__":
    # مثال على الاستخدام
    async def main():
        # إنشاء مزودي الإشعارات
        websocket_provider = WebSocketProvider()
        in_app_provider = InAppProvider()
        
        # تسجيل المزودين
        notification_manager.register_provider(websocket_provider)
        notification_manager.register_provider(in_app_provider)
        
        # بدء مدير الإشعارات
        await notification_manager.start()
        
        # إنشاء مراقب الأحداث
        observer = NotificationEventObserver(notification_manager)
        event_bus.subscribe(observer)
        
        # بدء ناقل الأحداث
        await event_bus.start()
        
        # إرسال إشعار تجريبي
        notification = create_notification(
            "إشعار تجريبي",
            "هذا إشعار تجريبي للنظام",
            ["user1", "admin"]
        )
        
        results = await notification_manager.send_notification(notification)
        print(f"Notification results: {results}")
        
        # عرض الإحصائيات
        stats = notification_manager.get_stats()
        print(f"Notification stats: {json.dumps(stats, indent=2)}")
        
        # إيقاف الخدمات
        await notification_manager.stop()
        await event_bus.stop()
    
    asyncio.run(main())

