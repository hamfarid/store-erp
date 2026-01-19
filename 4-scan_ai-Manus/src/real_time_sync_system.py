# File: /home/ubuntu/clean_project/src/real_time_sync_system.py
"""
مسار الملف: /home/ubuntu/clean_project/src/real_time_sync_system.py

نظام مزامنة البيانات والإشعارات الفورية
يوفر مزامنة فورية للبيانات وإشعارات في الوقت الفعلي
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union, Callable, AsyncGenerator
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import json
import logging
import websockets
import aioredis
from pathlib import Path
import uuid
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor
import threading
from event_system import Event, EventTypes, event_bus, create_system_event
from notification_system import NotificationManager, NotificationChannel, NotificationPriority

class SyncEventType(Enum):
    """أنواع أحداث المزامنة"""
    DATA_CREATED = "data_created"
    DATA_UPDATED = "data_updated"
    DATA_DELETED = "data_deleted"
    SYNC_STARTED = "sync_started"
    SYNC_COMPLETED = "sync_completed"
    SYNC_FAILED = "sync_failed"
    CONFLICT_DETECTED = "conflict_detected"
    CONFLICT_RESOLVED = "conflict_resolved"

class NotificationType(Enum):
    """أنواع الإشعارات"""
    REAL_TIME_UPDATE = "real_time_update"
    SYSTEM_ALERT = "system_alert"
    USER_NOTIFICATION = "user_notification"
    SYNC_STATUS = "sync_status"
    ERROR_ALERT = "error_alert"
    SUCCESS_MESSAGE = "success_message"

class ConnectionStatus(Enum):
    """حالة الاتصال"""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    RECONNECTING = "reconnecting"
    ERROR = "error"

@dataclass
class SyncEvent:
    """حدث المزامنة"""
    id: str
    event_type: SyncEventType
    table_name: str
    record_id: str
    data: Dict[str, Any]
    timestamp: datetime
    user_id: Optional[str] = None
    source_node: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RealTimeNotification:
    """إشعار فوري"""
    id: str
    notification_type: NotificationType
    title: str
    message: str
    data: Dict[str, Any]
    timestamp: datetime
    user_id: Optional[str] = None
    channel: str = "general"
    priority: str = "normal"
    expires_at: Optional[datetime] = None

@dataclass
class ClientConnection:
    """اتصال العميل"""
    id: str
    user_id: str
    websocket: Any
    status: ConnectionStatus
    connected_at: datetime
    last_ping: datetime
    subscriptions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SyncConfiguration:
    """إعدادات المزامنة"""
    enable_real_time: bool = True
    enable_batch_sync: bool = True
    batch_size: int = 100
    sync_interval_seconds: int = 30
    max_retry_attempts: int = 3
    conflict_resolution_strategy: str = "timestamp_based"
    enable_compression: bool = True
    enable_encryption: bool = True
    priority_tables: List[str] = field(default_factory=list)

class WebSocketManager:
    """مدير WebSocket للاتصالات الفورية"""
    
    def __init__(self):
        self.connections: Dict[str, ClientConnection] = {}
        self.user_connections: Dict[str, List[str]] = {}  # user_id -> connection_ids
        self.room_connections: Dict[str, List[str]] = {}  # room -> connection_ids
        self.logger = logging.getLogger('websocket_manager')
        self.ping_interval = 30  # ثانية
        self.ping_task = None
    
    async def start_server(self, host: str = "0.0.0.0", port: int = 8765):
        """بدء خادم WebSocket"""
        try:
            self.logger.info(f"Starting WebSocket server on {host}:{port}")
            
            # بدء مهمة ping
            self.ping_task = asyncio.create_task(self._ping_clients())
            
            # بدء الخادم
            async with websockets.serve(self._handle_connection, host, port):
                self.logger.info("WebSocket server started successfully")
                await asyncio.Future()  # تشغيل دائم
                
        except Exception as e:
            self.logger.error(f"Failed to start WebSocket server: {e}")
            raise
    
    async def _handle_connection(self, websocket, path):
        """معالجة اتصال جديد"""
        connection_id = str(uuid.uuid4())
        
        try:
            # انتظار رسالة المصادقة
            auth_message = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            auth_data = json.loads(auth_message)
            
            if not self._authenticate_connection(auth_data):
                await websocket.send(json.dumps({
                    "type": "auth_error",
                    "message": "Authentication failed"
                }))
                return
            
            user_id = auth_data.get("user_id")
            
            # إنشاء اتصال جديد
            connection = ClientConnection(
                id=connection_id,
                user_id=user_id,
                websocket=websocket,
                status=ConnectionStatus.CONNECTED,
                connected_at=datetime.now(),
                last_ping=datetime.now()
            )
            
            self.connections[connection_id] = connection
            
            # إضافة إلى قائمة اتصالات المستخدم
            if user_id not in self.user_connections:
                self.user_connections[user_id] = []
            self.user_connections[user_id].append(connection_id)
            
            # إرسال رسالة ترحيب
            await self._send_to_connection(connection_id, {
                "type": "welcome",
                "connection_id": connection_id,
                "timestamp": datetime.now().isoformat()
            })
            
            self.logger.info(f"New connection established: {connection_id} for user {user_id}")
            
            # معالجة الرسائل
            async for message in websocket:
                await self._handle_message(connection_id, message)
                
        except websockets.exceptions.ConnectionClosed:
            self.logger.info(f"Connection {connection_id} closed")
        except asyncio.TimeoutError:
            self.logger.warning(f"Authentication timeout for connection {connection_id}")
        except Exception as e:
            self.logger.error(f"Error handling connection {connection_id}: {e}")
        finally:
            await self._cleanup_connection(connection_id)
    
    def _authenticate_connection(self, auth_data: Dict[str, Any]) -> bool:
        """مصادقة الاتصال"""
        # هنا يمكن إضافة منطق المصادقة الفعلي
        # مثل التحقق من JWT token
        return auth_data.get("token") is not None
    
    async def _handle_message(self, connection_id: str, message: str):
        """معالجة رسالة من العميل"""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            if message_type == "ping":
                await self._handle_ping(connection_id)
            elif message_type == "subscribe":
                await self._handle_subscribe(connection_id, data)
            elif message_type == "unsubscribe":
                await self._handle_unsubscribe(connection_id, data)
            elif message_type == "send_message":
                await self._handle_send_message(connection_id, data)
            else:
                self.logger.warning(f"Unknown message type: {message_type}")
                
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON message from {connection_id}")
        except Exception as e:
            self.logger.error(f"Error handling message from {connection_id}: {e}")
    
    async def _handle_ping(self, connection_id: str):
        """معالجة ping"""
        if connection_id in self.connections:
            self.connections[connection_id].last_ping = datetime.now()
            await self._send_to_connection(connection_id, {"type": "pong"})
    
    async def _handle_subscribe(self, connection_id: str, data: Dict[str, Any]):
        """معالجة الاشتراك في قناة"""
        channel = data.get("channel")
        if channel and connection_id in self.connections:
            connection = self.connections[connection_id]
            if channel not in connection.subscriptions:
                connection.subscriptions.append(channel)
                
                # إضافة إلى قائمة اتصالات القناة
                if channel not in self.room_connections:
                    self.room_connections[channel] = []
                self.room_connections[channel].append(connection_id)
                
                await self._send_to_connection(connection_id, {
                    "type": "subscribed",
                    "channel": channel
                })
                
                self.logger.info(f"Connection {connection_id} subscribed to {channel}")
    
    async def _handle_unsubscribe(self, connection_id: str, data: Dict[str, Any]):
        """معالجة إلغاء الاشتراك"""
        channel = data.get("channel")
        if channel and connection_id in self.connections:
            connection = self.connections[connection_id]
            if channel in connection.subscriptions:
                connection.subscriptions.remove(channel)
                
                # إزالة من قائمة اتصالات القناة
                if channel in self.room_connections:
                    if connection_id in self.room_connections[channel]:
                        self.room_connections[channel].remove(connection_id)
                
                await self._send_to_connection(connection_id, {
                    "type": "unsubscribed",
                    "channel": channel
                })
                
                self.logger.info(f"Connection {connection_id} unsubscribed from {channel}")
    
    async def _handle_send_message(self, connection_id: str, data: Dict[str, Any]):
        """معالجة إرسال رسالة"""
        target_type = data.get("target_type")  # "user", "channel", "broadcast"
        target = data.get("target")
        message = data.get("message")
        
        if target_type == "user":
            await self.send_to_user(target, message)
        elif target_type == "channel":
            await self.send_to_channel(target, message)
        elif target_type == "broadcast":
            await self.broadcast_message(message)
    
    async def _send_to_connection(self, connection_id: str, data: Dict[str, Any]):
        """إرسال رسالة إلى اتصال محدد"""
        if connection_id not in self.connections:
            return False
        
        connection = self.connections[connection_id]
        try:
            message = json.dumps(data, default=str)
            await connection.websocket.send(message)
            return True
        except Exception as e:
            self.logger.error(f"Failed to send message to {connection_id}: {e}")
            await self._cleanup_connection(connection_id)
            return False
    
    async def send_to_user(self, user_id: str, data: Dict[str, Any]) -> int:
        """إرسال رسالة إلى جميع اتصالات المستخدم"""
        sent_count = 0
        
        if user_id in self.user_connections:
            connection_ids = self.user_connections[user_id].copy()
            
            for connection_id in connection_ids:
                success = await self._send_to_connection(connection_id, data)
                if success:
                    sent_count += 1
        
        return sent_count
    
    async def send_to_channel(self, channel: str, data: Dict[str, Any]) -> int:
        """إرسال رسالة إلى جميع المشتركين في قناة"""
        sent_count = 0
        
        if channel in self.room_connections:
            connection_ids = self.room_connections[channel].copy()
            
            for connection_id in connection_ids:
                success = await self._send_to_connection(connection_id, data)
                if success:
                    sent_count += 1
        
        return sent_count
    
    async def broadcast_message(self, data: Dict[str, Any]) -> int:
        """بث رسالة لجميع الاتصالات"""
        sent_count = 0
        connection_ids = list(self.connections.keys())
        
        for connection_id in connection_ids:
            success = await self._send_to_connection(connection_id, data)
            if success:
                sent_count += 1
        
        return sent_count
    
    async def _ping_clients(self):
        """ping دوري للعملاء"""
        while True:
            try:
                current_time = datetime.now()
                timeout_threshold = current_time - timedelta(seconds=self.ping_interval * 2)
                
                # العثور على الاتصالات المنتهية الصلاحية
                expired_connections = []
                for connection_id, connection in self.connections.items():
                    if connection.last_ping < timeout_threshold:
                        expired_connections.append(connection_id)
                
                # تنظيف الاتصالات المنتهية الصلاحية
                for connection_id in expired_connections:
                    await self._cleanup_connection(connection_id)
                
                # إرسال ping لجميع الاتصالات النشطة
                ping_data = {"type": "ping", "timestamp": current_time.isoformat()}
                await self.broadcast_message(ping_data)
                
                await asyncio.sleep(self.ping_interval)
                
            except Exception as e:
                self.logger.error(f"Error in ping task: {e}")
                await asyncio.sleep(self.ping_interval)
    
    async def _cleanup_connection(self, connection_id: str):
        """تنظيف اتصال"""
        if connection_id not in self.connections:
            return
        
        connection = self.connections[connection_id]
        user_id = connection.user_id
        
        # إزالة من قائمة الاتصالات
        del self.connections[connection_id]
        
        # إزالة من قائمة اتصالات المستخدم
        if user_id in self.user_connections:
            if connection_id in self.user_connections[user_id]:
                self.user_connections[user_id].remove(connection_id)
            
            # إزالة المستخدم إذا لم تعد له اتصالات
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
        
        # إزالة من جميع القنوات
        for channel in connection.subscriptions:
            if channel in self.room_connections:
                if connection_id in self.room_connections[channel]:
                    self.room_connections[channel].remove(connection_id)
                
                # إزالة القناة إذا لم تعد تحتوي على اتصالات
                if not self.room_connections[channel]:
                    del self.room_connections[channel]
        
        self.logger.info(f"Connection {connection_id} cleaned up")
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """إحصائيات الاتصالات"""
        return {
            "total_connections": len(self.connections),
            "unique_users": len(self.user_connections),
            "active_channels": len(self.room_connections),
            "connections_by_status": {
                status.value: len([c for c in self.connections.values() if c.status == status])
                for status in ConnectionStatus
            }
        }

class RealTimeSyncEngine:
    """محرك المزامنة الفورية"""
    
    def __init__(self, config: SyncConfiguration):
        self.config = config
        self.redis_client = None
        self.websocket_manager = WebSocketManager()
        self.notification_manager = NotificationManager()
        self.sync_queue = asyncio.Queue()
        self.is_running = False
        self.sync_tasks = []
        self.logger = logging.getLogger('real_time_sync_engine')
    
    async def initialize(self, redis_url: str = "redis://localhost:6379"):
        """تهيئة المحرك"""
        try:
            # الاتصال بـ Redis
            self.redis_client = await aioredis.from_url(redis_url)
            
            # اختبار الاتصال
            await self.redis_client.ping()
            
            # تهيئة مدير الإشعارات
            await self.notification_manager.initialize()
            
            self.logger.info("Real-time sync engine initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize sync engine: {e}")
            return False
    
    async def start(self):
        """بدء المحرك"""
        try:
            if self.is_running:
                self.logger.warning("Sync engine already running")
                return
            
            self.is_running = True
            
            # بدء مهام المزامنة
            if self.config.enable_real_time:
                self.sync_tasks.append(asyncio.create_task(self._real_time_sync_worker()))
            
            if self.config.enable_batch_sync:
                self.sync_tasks.append(asyncio.create_task(self._batch_sync_worker()))
            
            # بدء مهمة معالجة الأحداث
            self.sync_tasks.append(asyncio.create_task(self._event_processor()))
            
            # بدء خادم WebSocket
            self.sync_tasks.append(asyncio.create_task(self.websocket_manager.start_server()))
            
            self.logger.info("Real-time sync engine started")
            
        except Exception as e:
            self.logger.error(f"Failed to start sync engine: {e}")
            self.is_running = False
            raise
    
    async def stop(self):
        """إيقاف المحرك"""
        try:
            self.is_running = False
            
            # إلغاء جميع المهام
            for task in self.sync_tasks:
                task.cancel()
            
            # انتظار انتهاء المهام
            await asyncio.gather(*self.sync_tasks, return_exceptions=True)
            
            # إغلاق الاتصالات
            if self.redis_client:
                await self.redis_client.close()
            
            self.logger.info("Real-time sync engine stopped")
            
        except Exception as e:
            self.logger.error(f"Error stopping sync engine: {e}")
    
    async def publish_sync_event(self, event: SyncEvent):
        """نشر حدث مزامنة"""
        try:
            # إضافة إلى قائمة الانتظار
            await self.sync_queue.put(event)
            
            # نشر في Redis للعقد الأخرى
            event_data = {
                "id": event.id,
                "event_type": event.event_type.value,
                "table_name": event.table_name,
                "record_id": event.record_id,
                "data": event.data,
                "timestamp": event.timestamp.isoformat(),
                "user_id": event.user_id,
                "source_node": event.source_node,
                "metadata": event.metadata
            }
            
            await self.redis_client.publish("sync_events", json.dumps(event_data, default=str))
            
            self.logger.debug(f"Sync event published: {event.id}")
            
        except Exception as e:
            self.logger.error(f"Failed to publish sync event: {e}")
    
    async def send_real_time_notification(self, notification: RealTimeNotification):
        """إرسال إشعار فوري"""
        try:
            # إرسال عبر WebSocket
            notification_data = {
                "type": "notification",
                "id": notification.id,
                "notification_type": notification.notification_type.value,
                "title": notification.title,
                "message": notification.message,
                "data": notification.data,
                "timestamp": notification.timestamp.isoformat(),
                "channel": notification.channel,
                "priority": notification.priority
            }
            
            if notification.user_id:
                # إرسال لمستخدم محدد
                await self.websocket_manager.send_to_user(notification.user_id, notification_data)
            else:
                # إرسال للقناة
                await self.websocket_manager.send_to_channel(notification.channel, notification_data)
            
            # إرسال عبر قنوات الإشعارات الأخرى
            await self.notification_manager.send_notification(
                user_id=notification.user_id,
                title=notification.title,
                message=notification.message,
                channel=NotificationChannel.PUSH,
                priority=NotificationPriority.NORMAL,
                data=notification.data
            )
            
            self.logger.debug(f"Real-time notification sent: {notification.id}")
            
        except Exception as e:
            self.logger.error(f"Failed to send real-time notification: {e}")
    
    async def _real_time_sync_worker(self):
        """عامل المزامنة الفورية"""
        while self.is_running:
            try:
                # انتظار حدث مزامنة
                event = await asyncio.wait_for(self.sync_queue.get(), timeout=1.0)
                
                # معالجة الحدث
                await self._process_sync_event(event)
                
                # تأكيد المعالجة
                self.sync_queue.task_done()
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.logger.error(f"Error in real-time sync worker: {e}")
                await asyncio.sleep(1)
    
    async def _batch_sync_worker(self):
        """عامل المزامنة المجمعة"""
        while self.is_running:
            try:
                await asyncio.sleep(self.config.sync_interval_seconds)
                
                # جمع الأحداث المتراكمة
                events = []
                try:
                    while len(events) < self.config.batch_size:
                        event = self.sync_queue.get_nowait()
                        events.append(event)
                except asyncio.QueueEmpty:
                    pass
                
                if events:
                    # معالجة الأحداث في مجموعة
                    await self._process_batch_events(events)
                    
                    # تأكيد المعالجة
                    for _ in events:
                        self.sync_queue.task_done()
                
            except Exception as e:
                self.logger.error(f"Error in batch sync worker: {e}")
                await asyncio.sleep(self.config.sync_interval_seconds)
    
    async def _event_processor(self):
        """معالج الأحداث من Redis"""
        try:
            pubsub = self.redis_client.pubsub()
            await pubsub.subscribe("sync_events")
            
            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        event_data = json.loads(message["data"])
                        
                        # تحويل إلى كائن SyncEvent
                        event = SyncEvent(
                            id=event_data["id"],
                            event_type=SyncEventType(event_data["event_type"]),
                            table_name=event_data["table_name"],
                            record_id=event_data["record_id"],
                            data=event_data["data"],
                            timestamp=datetime.fromisoformat(event_data["timestamp"]),
                            user_id=event_data.get("user_id"),
                            source_node=event_data.get("source_node"),
                            metadata=event_data.get("metadata", {})
                        )
                        
                        # معالجة الحدث
                        await self._handle_external_sync_event(event)
                        
                    except Exception as e:
                        self.logger.error(f"Error processing external sync event: {e}")
                        
        except Exception as e:
            self.logger.error(f"Error in event processor: {e}")
    
    async def _process_sync_event(self, event: SyncEvent):
        """معالجة حدث مزامنة"""
        try:
            # إرسال إشعار فوري للمستخدمين المهتمين
            notification = RealTimeNotification(
                id=str(uuid.uuid4()),
                notification_type=NotificationType.REAL_TIME_UPDATE,
                title=f"تحديث في {event.table_name}",
                message=f"تم {event.event_type.value} سجل في {event.table_name}",
                data={
                    "table_name": event.table_name,
                    "record_id": event.record_id,
                    "event_type": event.event_type.value
                },
                timestamp=datetime.now(),
                user_id=event.user_id,
                channel=f"table_{event.table_name}"
            )
            
            await self.send_real_time_notification(notification)
            
            # تسجيل الحدث
            await self._log_sync_event(event)
            
            self.logger.debug(f"Sync event processed: {event.id}")
            
        except Exception as e:
            self.logger.error(f"Error processing sync event {event.id}: {e}")
    
    async def _process_batch_events(self, events: List[SyncEvent]):
        """معالجة مجموعة من الأحداث"""
        try:
            # تجميع الأحداث حسب الجدول
            events_by_table = {}
            for event in events:
                if event.table_name not in events_by_table:
                    events_by_table[event.table_name] = []
                events_by_table[event.table_name].append(event)
            
            # معالجة كل جدول
            for table_name, table_events in events_by_table.items():
                # إرسال إشعار مجمع
                notification = RealTimeNotification(
                    id=str(uuid.uuid4()),
                    notification_type=NotificationType.SYNC_STATUS,
                    title=f"تحديث مجمع في {table_name}",
                    message=f"تم معالجة {len(table_events)} تحديث في {table_name}",
                    data={
                        "table_name": table_name,
                        "events_count": len(table_events),
                        "event_types": list(set(e.event_type.value for e in table_events))
                    },
                    timestamp=datetime.now(),
                    channel=f"table_{table_name}"
                )
                
                await self.send_real_time_notification(notification)
            
            # تسجيل الأحداث
            for event in events:
                await self._log_sync_event(event)
            
            self.logger.info(f"Batch of {len(events)} events processed")
            
        except Exception as e:
            self.logger.error(f"Error processing batch events: {e}")
    
    async def _handle_external_sync_event(self, event: SyncEvent):
        """معالجة حدث مزامنة خارجي"""
        try:
            # التحقق من أن الحدث ليس من نفس العقدة
            if event.source_node == self._get_node_id():
                return
            
            # معالجة الحدث
            await self._process_sync_event(event)
            
        except Exception as e:
            self.logger.error(f"Error handling external sync event: {e}")
    
    async def _log_sync_event(self, event: SyncEvent):
        """تسجيل حدث المزامنة"""
        try:
            log_data = {
                "event_id": event.id,
                "event_type": event.event_type.value,
                "table_name": event.table_name,
                "record_id": event.record_id,
                "timestamp": event.timestamp.isoformat(),
                "user_id": event.user_id,
                "source_node": event.source_node,
                "processed_at": datetime.now().isoformat()
            }
            
            # حفظ في Redis
            await self.redis_client.lpush("sync_event_log", json.dumps(log_data, default=str))
            
            # الاحتفاظ بآخر 10000 حدث فقط
            await self.redis_client.ltrim("sync_event_log", 0, 9999)
            
        except Exception as e:
            self.logger.error(f"Error logging sync event: {e}")
    
    def _get_node_id(self) -> str:
        """الحصول على معرف العقدة"""
        # يمكن استخدام hostname أو معرف فريد آخر
        import socket
        return socket.gethostname()
    
    async def get_sync_statistics(self) -> Dict[str, Any]:
        """إحصائيات المزامنة"""
        try:
            # إحصائيات الاتصالات
            connection_stats = self.websocket_manager.get_connection_stats()
            
            # إحصائيات الأحداث
            event_log_size = await self.redis_client.llen("sync_event_log")
            
            # إحصائيات قائمة الانتظار
            queue_size = self.sync_queue.qsize()
            
            return {
                "connections": connection_stats,
                "event_log_size": event_log_size,
                "queue_size": queue_size,
                "is_running": self.is_running,
                "config": {
                    "real_time_enabled": self.config.enable_real_time,
                    "batch_sync_enabled": self.config.enable_batch_sync,
                    "batch_size": self.config.batch_size,
                    "sync_interval": self.config.sync_interval_seconds
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting sync statistics: {e}")
            return {}

class DataChangeDetector:
    """كاشف تغييرات البيانات"""
    
    def __init__(self, sync_engine: RealTimeSyncEngine):
        self.sync_engine = sync_engine
        self.logger = logging.getLogger('data_change_detector')
        self.watched_tables = set()
        self.triggers_installed = False
    
    async def install_database_triggers(self, database_connection):
        """تثبيت triggers في قاعدة البيانات"""
        try:
            # مثال لـ PostgreSQL
            trigger_sql = """
            CREATE OR REPLACE FUNCTION notify_data_change()
            RETURNS TRIGGER AS $$
            BEGIN
                PERFORM pg_notify('data_change', json_build_object(
                    'table_name', TG_TABLE_NAME,
                    'operation', TG_OP,
                    'record_id', COALESCE(NEW.id, OLD.id),
                    'data', CASE 
                        WHEN TG_OP = 'DELETE' THEN row_to_json(OLD)
                        ELSE row_to_json(NEW)
                    END,
                    'timestamp', extract(epoch from now())
                )::text);
                RETURN NULL;
            END;
            $$ LANGUAGE plpgsql;
            """
            
            await database_connection.execute(trigger_sql)
            
            # تثبيت triggers للجداول المراقبة
            for table_name in self.watched_tables:
                trigger_name = f"sync_trigger_{table_name}"
                
                # حذف trigger إذا كان موجوداً
                await database_connection.execute(f"DROP TRIGGER IF EXISTS {trigger_name} ON {table_name}")
                
                # إنشاء trigger جديد
                create_trigger_sql = f"""
                CREATE TRIGGER {trigger_name}
                AFTER INSERT OR UPDATE OR DELETE ON {table_name}
                FOR EACH ROW EXECUTE FUNCTION notify_data_change()
                """
                
                await database_connection.execute(create_trigger_sql)
            
            self.triggers_installed = True
            self.logger.info("Database triggers installed successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to install database triggers: {e}")
            raise
    
    async def listen_for_changes(self, database_connection):
        """الاستماع لتغييرات قاعدة البيانات"""
        try:
            await database_connection.add_listener('data_change', self._handle_database_change)
            self.logger.info("Started listening for database changes")
            
        except Exception as e:
            self.logger.error(f"Failed to listen for database changes: {e}")
    
    async def _handle_database_change(self, connection, pid, channel, payload):
        """معالجة تغيير في قاعدة البيانات"""
        try:
            change_data = json.loads(payload)
            
            # إنشاء حدث مزامنة
            event = SyncEvent(
                id=str(uuid.uuid4()),
                event_type=SyncEventType(f"data_{change_data['operation'].lower()}"),
                table_name=change_data['table_name'],
                record_id=str(change_data['record_id']),
                data=change_data['data'],
                timestamp=datetime.fromtimestamp(change_data['timestamp']),
                source_node=self.sync_engine._get_node_id()
            )
            
            # نشر الحدث
            await self.sync_engine.publish_sync_event(event)
            
        except Exception as e:
            self.logger.error(f"Error handling database change: {e}")
    
    def add_watched_table(self, table_name: str):
        """إضافة جدول للمراقبة"""
        self.watched_tables.add(table_name)
        self.logger.info(f"Added table to watch list: {table_name}")
    
    def remove_watched_table(self, table_name: str):
        """إزالة جدول من المراقبة"""
        self.watched_tables.discard(table_name)
        self.logger.info(f"Removed table from watch list: {table_name}")

# مثيل عام لمحرك المزامنة
sync_config = SyncConfiguration()
real_time_sync_engine = RealTimeSyncEngine(sync_config)

# دوال مساعدة
async def initialize_real_time_sync():
    """تهيئة نظام المزامنة الفورية"""
    try:
        success = await real_time_sync_engine.initialize()
        if success:
            await real_time_sync_engine.start()
        return success
    except Exception as e:
        logging.error(f"Failed to initialize real-time sync: {e}")
        return False

async def create_sync_event(table_name: str, operation: str, record_id: str, 
                          data: Dict[str, Any], user_id: str = None) -> bool:
    """إنشاء حدث مزامنة"""
    try:
        event = SyncEvent(
            id=str(uuid.uuid4()),
            event_type=SyncEventType(f"data_{operation.lower()}"),
            table_name=table_name,
            record_id=record_id,
            data=data,
            timestamp=datetime.now(),
            user_id=user_id,
            source_node=real_time_sync_engine._get_node_id()
        )
        
        await real_time_sync_engine.publish_sync_event(event)
        return True
        
    except Exception as e:
        logging.error(f"Failed to create sync event: {e}")
        return False

async def send_instant_notification(user_id: str, title: str, message: str, 
                                  data: Dict[str, Any] = None) -> bool:
    """إرسال إشعار فوري"""
    try:
        notification = RealTimeNotification(
            id=str(uuid.uuid4()),
            notification_type=NotificationType.USER_NOTIFICATION,
            title=title,
            message=message,
            data=data or {},
            timestamp=datetime.now(),
            user_id=user_id
        )
        
        await real_time_sync_engine.send_real_time_notification(notification)
        return True
        
    except Exception as e:
        logging.error(f"Failed to send instant notification: {e}")
        return False

if __name__ == "__main__":
    # مثال على الاستخدام
    async def main():
        # تهيئة النظام
        await initialize_real_time_sync()
        
        # إنشاء حدث مزامنة
        await create_sync_event(
            table_name="users",
            operation="created",
            record_id="123",
            data={"name": "أحمد محمد", "email": "ahmed@example.com"},
            user_id="admin"
        )
        
        # إرسال إشعار فوري
        await send_instant_notification(
            user_id="123",
            title="مرحباً بك",
            message="تم إنشاء حسابك بنجاح",
            data={"welcome_bonus": 100}
        )
        
        # عرض الإحصائيات
        stats = await real_time_sync_engine.get_sync_statistics()
        print(f"Sync statistics: {json.dumps(stats, indent=2, default=str)}")
    
    asyncio.run(main())

