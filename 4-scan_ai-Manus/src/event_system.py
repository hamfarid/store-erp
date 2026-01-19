# File: /home/ubuntu/clean_project/src/event_system.py
"""
مسار الملف: /home/ubuntu/clean_project/src/event_system.py

نظام الأحداث والإشعارات المتقدم - Observer Pattern
يوفر نظام أحداث مرن وقابل للتوسع لجميع أجزاء النظام
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import threading
import json
import logging
import uuid
from collections import defaultdict
import weakref

class EventPriority(Enum):
    """أولوية الأحداث"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4

class EventStatus(Enum):
    """حالة الحدث"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Event:
    """فئة الحدث الأساسية"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    source: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    priority: EventPriority = EventPriority.NORMAL
    status: EventStatus = EventStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3
    delay_seconds: float = 0
    expires_at: Optional[datetime] = None
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self) -> bool:
        """فحص انتهاء صلاحية الحدث"""
        return self.expires_at is not None and datetime.now() > self.expires_at

    def can_retry(self) -> bool:
        """فحص إمكانية إعادة المحاولة"""
        return self.retry_count < self.max_retries

    def to_dict(self) -> Dict[str, Any]:
        """تحويل الحدث إلى قاموس"""
        return {
            'id': self.id,
            'type': self.type,
            'data': self.data,
            'source': self.source,
            'timestamp': self.timestamp.isoformat(),
            'priority': self.priority.value,
            'status': self.status.value,
            'retry_count': self.retry_count,
            'max_retries': self.max_retries,
            'delay_seconds': self.delay_seconds,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'correlation_id': self.correlation_id,
            'metadata': self.metadata
        }

class EventObserver(ABC):
    """واجهة المراقب للأحداث"""
    
    @abstractmethod
    async def handle_event(self, event: Event) -> bool:
        """معالجة الحدث - يجب إرجاع True في حالة النجاح"""
        pass
    
    @abstractmethod
    def get_supported_events(self) -> List[str]:
        """الحصول على قائمة الأحداث المدعومة"""
        pass
    
    def get_priority(self) -> int:
        """أولوية المراقب (أقل رقم = أولوية أعلى)"""
        return 100

class EventFilter:
    """مرشح الأحداث"""
    
    def __init__(self, 
                 event_types: Optional[List[str]] = None,
                 sources: Optional[List[str]] = None,
                 priorities: Optional[List[EventPriority]] = None,
                 custom_filter: Optional[Callable[[Event], bool]] = None):
        self.event_types = event_types or []
        self.sources = sources or []
        self.priorities = priorities or []
        self.custom_filter = custom_filter
    
    def matches(self, event: Event) -> bool:
        """فحص تطابق الحدث مع المرشح"""
        if self.event_types and event.type not in self.event_types:
            return False
        
        if self.sources and event.source not in self.sources:
            return False
        
        if self.priorities and event.priority not in self.priorities:
            return False
        
        if self.custom_filter and not self.custom_filter(event):
            return False
        
        return True

class EventBus:
    """ناقل الأحداث الرئيسي"""
    
    def __init__(self, max_queue_size: int = 10000):
        self.observers: Dict[str, List[EventObserver]] = defaultdict(list)
        self.global_observers: List[EventObserver] = []
        self.event_queue: asyncio.Queue = asyncio.Queue(maxsize=max_queue_size)
        self.failed_events: List[Event] = []
        self.event_history: List[Event] = []
        self.filters: List[EventFilter] = []
        self.middleware: List[Callable[[Event], Event]] = []
        self.is_running = False
        self.worker_tasks: List[asyncio.Task] = []
        self.stats = {
            'total_events': 0,
            'processed_events': 0,
            'failed_events': 0,
            'retry_events': 0
        }
        
        # إعداد نظام السجلات
        self.logger = logging.getLogger('event_bus')
        handler = logging.FileHandler('events.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def subscribe(self, observer: EventObserver, event_types: Optional[List[str]] = None):
        """اشتراك مراقب في أحداث معينة"""
        if event_types is None:
            # اشتراك عام في جميع الأحداث
            self.global_observers.append(observer)
            self.global_observers.sort(key=lambda x: x.get_priority())
        else:
            # اشتراك في أحداث محددة
            for event_type in event_types:
                self.observers[event_type].append(observer)
                self.observers[event_type].sort(key=lambda x: x.get_priority())
        
        self.logger.info(f"Observer {observer.__class__.__name__} subscribed to {event_types or 'all events'}")
    
    def unsubscribe(self, observer: EventObserver, event_types: Optional[List[str]] = None):
        """إلغاء اشتراك مراقب"""
        if event_types is None:
            if observer in self.global_observers:
                self.global_observers.remove(observer)
        else:
            for event_type in event_types:
                if observer in self.observers[event_type]:
                    self.observers[event_type].remove(observer)
        
        self.logger.info(f"Observer {observer.__class__.__name__} unsubscribed from {event_types or 'all events'}")
    
    def add_filter(self, event_filter: EventFilter):
        """إضافة مرشح للأحداث"""
        self.filters.append(event_filter)
    
    def add_middleware(self, middleware: Callable[[Event], Event]):
        """إضافة وسطاء لمعالجة الأحداث"""
        self.middleware.append(middleware)
    
    async def publish(self, event: Event) -> bool:
        """نشر حدث"""
        try:
            # تطبيق الوسطاء
            for middleware in self.middleware:
                event = middleware(event)
            
            # فحص المرشحات
            for event_filter in self.filters:
                if not event_filter.matches(event):
                    self.logger.debug(f"Event {event.id} filtered out")
                    return False
            
            # إضافة الحدث إلى الطابور
            await self.event_queue.put(event)
            self.stats['total_events'] += 1
            
            self.logger.info(f"Event {event.id} of type {event.type} published")
            return True
            
        except asyncio.QueueFull:
            self.logger.error(f"Event queue full, dropping event {event.id}")
            return False
        except Exception as e:
            self.logger.error(f"Error publishing event {event.id}: {e}")
            return False
    
    async def publish_sync(self, event: Event) -> bool:
        """نشر حدث بشكل متزامن (معالجة فورية)"""
        try:
            # تطبيق الوسطاء
            for middleware in self.middleware:
                event = middleware(event)
            
            # معالجة فورية
            await self._process_event(event)
            return True
            
        except Exception as e:
            self.logger.error(f"Error in sync publish for event {event.id}: {e}")
            return False
    
    async def _process_event(self, event: Event):
        """معالجة حدث واحد"""
        event.status = EventStatus.PROCESSING
        success = True
        
        try:
            # الحصول على المراقبين المناسبين
            observers = []
            
            # المراقبين المخصصين لنوع الحدث
            if event.type in self.observers:
                observers.extend(self.observers[event.type])
            
            # المراقبين العامين
            observers.extend(self.global_observers)
            
            # معالجة الحدث مع كل مراقب
            for observer in observers:
                try:
                    result = await observer.handle_event(event)
                    if not result:
                        success = False
                        self.logger.warning(f"Observer {observer.__class__.__name__} failed to handle event {event.id}")
                except Exception as e:
                    success = False
                    self.logger.error(f"Observer {observer.__class__.__name__} error handling event {event.id}: {e}")
            
            if success:
                event.status = EventStatus.COMPLETED
                self.stats['processed_events'] += 1
                self.logger.info(f"Event {event.id} processed successfully")
            else:
                await self._handle_failed_event(event)
            
        except Exception as e:
            self.logger.error(f"Error processing event {event.id}: {e}")
            await self._handle_failed_event(event)
        
        # إضافة إلى التاريخ
        self.event_history.append(event)
        
        # تنظيف التاريخ القديم
        if len(self.event_history) > 1000:
            self.event_history = self.event_history[-500:]
    
    async def _handle_failed_event(self, event: Event):
        """معالجة الأحداث الفاشلة"""
        event.retry_count += 1
        
        if event.can_retry():
            event.status = EventStatus.PENDING
            # إعادة جدولة الحدث مع تأخير
            delay = min(2 ** event.retry_count, 300)  # تأخير تصاعدي حتى 5 دقائق
            
            async def retry_event():
                await asyncio.sleep(delay)
                await self.event_queue.put(event)
            
            asyncio.create_task(retry_event())
            self.stats['retry_events'] += 1
            self.logger.info(f"Event {event.id} scheduled for retry {event.retry_count}/{event.max_retries}")
        else:
            event.status = EventStatus.FAILED
            self.failed_events.append(event)
            self.stats['failed_events'] += 1
            self.logger.error(f"Event {event.id} failed permanently after {event.retry_count} retries")
    
    async def start(self, num_workers: int = 3):
        """بدء معالجة الأحداث"""
        if self.is_running:
            return
        
        self.is_running = True
        
        # إنشاء عمال المعالجة
        for i in range(num_workers):
            task = asyncio.create_task(self._worker(f"worker-{i}"))
            self.worker_tasks.append(task)
        
        self.logger.info(f"Event bus started with {num_workers} workers")
    
    async def stop(self):
        """إيقاف معالجة الأحداث"""
        self.is_running = False
        
        # إلغاء جميع المهام
        for task in self.worker_tasks:
            task.cancel()
        
        # انتظار انتهاء المهام
        await asyncio.gather(*self.worker_tasks, return_exceptions=True)
        self.worker_tasks.clear()
        
        self.logger.info("Event bus stopped")
    
    async def _worker(self, worker_name: str):
        """عامل معالجة الأحداث"""
        self.logger.info(f"Worker {worker_name} started")
        
        while self.is_running:
            try:
                # انتظار حدث جديد مع timeout
                event = await asyncio.wait_for(self.event_queue.get(), timeout=1.0)
                
                # فحص انتهاء صلاحية الحدث
                if event.is_expired():
                    event.status = EventStatus.CANCELLED
                    self.logger.info(f"Event {event.id} expired, skipping")
                    continue
                
                # معالجة الحدث
                await self._process_event(event)
                
            except asyncio.TimeoutError:
                # لا توجد أحداث، استمرار الحلقة
                continue
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Worker {worker_name} error: {e}")
        
        self.logger.info(f"Worker {worker_name} stopped")
    
    def get_stats(self) -> Dict[str, Any]:
        """الحصول على إحصائيات الأحداث"""
        return {
            'stats': self.stats.copy(),
            'queue_size': self.event_queue.qsize(),
            'failed_events_count': len(self.failed_events),
            'history_count': len(self.event_history),
            'observers_count': {
                'global': len(self.global_observers),
                'specific': {event_type: len(observers) for event_type, observers in self.observers.items()}
            },
            'is_running': self.is_running,
            'workers_count': len(self.worker_tasks)
        }
    
    def get_failed_events(self) -> List[Event]:
        """الحصول على الأحداث الفاشلة"""
        return self.failed_events.copy()
    
    def get_recent_events(self, limit: int = 100) -> List[Event]:
        """الحصول على الأحداث الأخيرة"""
        return self.event_history[-limit:]
    
    def clear_failed_events(self):
        """مسح الأحداث الفاشلة"""
        self.failed_events.clear()
        self.logger.info("Failed events cleared")

# مثيل عام لناقل الأحداث
event_bus = EventBus()

# أنواع الأحداث المحددة مسبقاً
class EventTypes:
    """أنواع الأحداث المحددة مسبقاً"""
    
    # أحداث المستخدمين
    USER_CREATED = "user.created"
    USER_UPDATED = "user.updated"
    USER_DELETED = "user.deleted"
    USER_LOGIN = "user.login"
    USER_LOGOUT = "user.logout"
    
    # أحداث التشخيص
    DIAGNOSIS_STARTED = "diagnosis.started"
    DIAGNOSIS_COMPLETED = "diagnosis.completed"
    DIAGNOSIS_FAILED = "diagnosis.failed"
    
    # أحداث الملفات
    FILE_UPLOADED = "file.uploaded"
    FILE_PROCESSED = "file.processed"
    FILE_DELETED = "file.deleted"
    
    # أحداث النظام
    SYSTEM_STARTUP = "system.startup"
    SYSTEM_SHUTDOWN = "system.shutdown"
    SYSTEM_ERROR = "system.error"
    SYSTEM_WARNING = "system.warning"
    
    # أحداث الأمان
    SECURITY_BREACH = "security.breach"
    SECURITY_LOGIN_FAILED = "security.login_failed"
    SECURITY_PERMISSION_DENIED = "security.permission_denied"
    
    # أحداث الذكاء الاصطناعي
    AI_MODEL_LOADED = "ai.model_loaded"
    AI_PREDICTION_MADE = "ai.prediction_made"
    AI_TRAINING_STARTED = "ai.training_started"
    AI_TRAINING_COMPLETED = "ai.training_completed"

# دوال مساعدة لإنشاء الأحداث
def create_user_event(event_type: str, user_id: int, **kwargs) -> Event:
    """إنشاء حدث مستخدم"""
    return Event(
        type=event_type,
        source="user_service",
        data={"user_id": user_id, **kwargs}
    )

def create_diagnosis_event(event_type: str, diagnosis_id: str, **kwargs) -> Event:
    """إنشاء حدث تشخيص"""
    return Event(
        type=event_type,
        source="diagnosis_service",
        data={"diagnosis_id": diagnosis_id, **kwargs}
    )

def create_system_event(event_type: str, message: str, **kwargs) -> Event:
    """إنشاء حدث نظام"""
    return Event(
        type=event_type,
        source="system",
        data={"message": message, **kwargs}
    )

def create_security_event(event_type: str, user_id: Optional[int], ip_address: str, **kwargs) -> Event:
    """إنشاء حدث أمني"""
    return Event(
        type=event_type,
        source="security_service",
        priority=EventPriority.HIGH,
        data={"user_id": user_id, "ip_address": ip_address, **kwargs}
    )

if __name__ == "__main__":
    # مثال على الاستخدام
    import asyncio
    
    class TestObserver(EventObserver):
        async def handle_event(self, event: Event) -> bool:
            print(f"Handling event: {event.type} - {event.data}")
            return True
        
        def get_supported_events(self) -> List[str]:
            return [EventTypes.USER_CREATED, EventTypes.DIAGNOSIS_COMPLETED]
    
    async def main():
        # إنشاء مراقب
        observer = TestObserver()
        
        # اشتراك في الأحداث
        event_bus.subscribe(observer, [EventTypes.USER_CREATED])
        
        # بدء ناقل الأحداث
        await event_bus.start()
        
        # نشر حدث
        event = create_user_event(EventTypes.USER_CREATED, user_id=1, username="test_user")
        await event_bus.publish(event)
        
        # انتظار قليل للمعالجة
        await asyncio.sleep(2)
        
        # عرض الإحصائيات
        stats = event_bus.get_stats()
        print(f"Event bus stats: {json.dumps(stats, indent=2)}")
        
        # إيقاف ناقل الأحداث
        await event_bus.stop()
    
    # تشغيل المثال
    asyncio.run(main())

