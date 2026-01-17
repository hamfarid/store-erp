"""
Activity Log Models
سجل الأنشطة - تتبع جميع أنشطة المستخدمين والنظام والذكاء الصناعي
"""

from datetime import datetime
from typing import Optional, Dict, Any
import json


class ActivityLog:
    """
    نموذج سجل الأنشطة
    يسجل جميع الأنشطة في النظام بما في ذلك:
    - أنشطة المستخدمين
    - أنشطة الذكاء الصناعي
    - التواصل بين الوحدات
    - المسارات والعمليات
    """

    def __init__(self, db_connection=None):
        """تهيئة سجل الأنشطة"""
        self.db = db_connection
        self._create_tables()

    def _create_tables(self):
        """إنشاء جداول سجل الأنشطة"""
        if not self.db:
            return

        cursor = self.db.cursor()

        # جدول سجل أنشطة المستخدمين
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                activity_type TEXT NOT NULL,
                module_name TEXT,
                action TEXT NOT NULL,
                description TEXT,
                ip_address TEXT,
                user_agent TEXT,
                request_method TEXT,
                request_path TEXT,
                request_data TEXT,
                response_status INTEGER,
                duration_ms INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """
        )

        # جدول سجل أنشطة الذكاء الصناعي
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ai_activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT NOT NULL,
                agent_type TEXT NOT NULL,
                activity_type TEXT NOT NULL,
                module_name TEXT,
                action TEXT NOT NULL,
                input_data TEXT,
                output_data TEXT,
                confidence_score REAL,
                processing_time_ms INTEGER,
                success BOOLEAN DEFAULT 1,
                error_message TEXT,
                learning_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # جدول سجل التواصل بين الوحدات
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS module_communication_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_module TEXT NOT NULL,
                target_module TEXT NOT NULL,
                communication_type TEXT NOT NULL,
                message_type TEXT,
                message_data TEXT,
                status TEXT NOT NULL,
                response_data TEXT,
                duration_ms INTEGER,
                retry_count INTEGER DEFAULT 0,
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # جدول سجل المسارات والعمليات
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS system_path_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path_type TEXT NOT NULL,
                path_name TEXT NOT NULL,
                operation TEXT NOT NULL,
                status TEXT NOT NULL,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                duration_ms INTEGER,
                steps_completed INTEGER,
                total_steps INTEGER,
                metadata TEXT,
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # جدول سجل الأخطاء والاستثناءات
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS error_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_type TEXT NOT NULL,
                error_code TEXT,
                error_message TEXT NOT NULL,
                stack_trace TEXT,
                module_name TEXT,
                function_name TEXT,
                user_id INTEGER,
                severity TEXT NOT NULL,
                resolved BOOLEAN DEFAULT 0,
                resolution_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # إنشاء فهارس لتحسين الأداء
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_user_activity_user_id
            ON user_activity_log(user_id)
        """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_user_activity_created_at
            ON user_activity_log(created_at)
        """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_ai_activity_agent_name
            ON ai_activity_log(agent_name)
        """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_module_comm_source
            ON module_communication_log(source_module)
        """
        )

        self.db.commit()

    def log_user_activity(
        self,
        user_id: int,
        username: str,
        activity_type: str,
        action: str,
        module_name: Optional[str] = None,
        description: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        request_method: Optional[str] = None,
        request_path: Optional[str] = None,
        request_data: Optional[Dict] = None,
        response_status: Optional[int] = None,
        duration_ms: Optional[int] = None,
    ) -> int:
        """
        تسجيل نشاط المستخدم

        Args:
            user_id: معرف المستخدم
            username: اسم المستخدم
            activity_type: نوع النشاط (login, logout, create, update, delete, view, etc.)
            action: الإجراء المنفذ
            module_name: اسم الوحدة
            description: وصف النشاط
            ip_address: عنوان IP
            user_agent: معلومات المتصفح
            request_method: طريقة الطلب (GET, POST, etc.)
            request_path: مسار الطلب
            request_data: بيانات الطلب
            response_status: حالة الاستجابة
            duration_ms: مدة العملية بالميلي ثانية

        Returns:
            معرف السجل المُنشأ
        """
        if not self.db:
            return 0

        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO user_activity_log (
                user_id, username, activity_type, module_name, action,
                description, ip_address, user_agent, request_method,
                request_path, request_data, response_status, duration_ms
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                user_id,
                username,
                activity_type,
                module_name,
                action,
                description,
                ip_address,
                user_agent,
                request_method,
                request_path,
                json.dumps(request_data) if request_data else None,
                response_status,
                duration_ms,
            ),
        )
        self.db.commit()
        return cursor.lastrowid

    def log_ai_activity(
        self,
        agent_name: str,
        agent_type: str,
        activity_type: str,
        action: str,
        module_name: Optional[str] = None,
        input_data: Optional[Dict] = None,
        output_data: Optional[Dict] = None,
        confidence_score: Optional[float] = None,
        processing_time_ms: Optional[int] = None,
        success: bool = True,
        error_message: Optional[str] = None,
        learning_data: Optional[Dict] = None,
    ) -> int:
        """
        تسجيل نشاط الذكاء الصناعي

        Args:
            agent_name: اسم الوكيل
            agent_type: نوع الوكيل
            activity_type: نوع النشاط
            action: الإجراء المنفذ
            module_name: اسم الوحدة
            input_data: بيانات الإدخال
            output_data: بيانات الإخراج
            confidence_score: درجة الثقة
            processing_time_ms: وقت المعالجة
            success: نجاح العملية
            error_message: رسالة الخطأ
            learning_data: بيانات التعلم

        Returns:
            معرف السجل المُنشأ
        """
        if not self.db:
            return 0

        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO ai_activity_log (
                agent_name, agent_type, activity_type, module_name, action,
                input_data, output_data, confidence_score, processing_time_ms,
                success, error_message, learning_data
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                agent_name,
                agent_type,
                activity_type,
                module_name,
                action,
                json.dumps(input_data) if input_data else None,
                json.dumps(output_data) if output_data else None,
                confidence_score,
                processing_time_ms,
                success,
                error_message,
                json.dumps(learning_data) if learning_data else None,
            ),
        )
        self.db.commit()
        return cursor.lastrowid

    def log_module_communication(
        self,
        source_module: str,
        target_module: str,
        communication_type: str,
        message_type: Optional[str] = None,
        message_data: Optional[Dict] = None,
        status: str = "pending",
        response_data: Optional[Dict] = None,
        duration_ms: Optional[int] = None,
        retry_count: int = 0,
        error_message: Optional[str] = None,
    ) -> int:
        """تسجيل التواصل بين الوحدات"""
        if not self.db:
            return 0

        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO module_communication_log (
                source_module, target_module, communication_type, message_type,
                message_data, status, response_data, duration_ms, retry_count,
                error_message
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                source_module,
                target_module,
                communication_type,
                message_type,
                json.dumps(message_data) if message_data else None,
                status,
                json.dumps(response_data) if response_data else None,
                duration_ms,
                retry_count,
                error_message,
            ),
        )
        self.db.commit()
        return cursor.lastrowid

    def log_system_path(
        self,
        path_type: str,
        path_name: str,
        operation: str,
        status: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        duration_ms: Optional[int] = None,
        steps_completed: int = 0,
        total_steps: int = 0,
        metadata: Optional[Dict] = None,
        error_message: Optional[str] = None,
    ) -> int:
        """تسجيل مسار النظام والعمليات"""
        if not self.db:
            return 0

        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO system_path_log (
                path_type, path_name, operation, status, start_time, end_time,
                duration_ms, steps_completed, total_steps, metadata, error_message
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                path_type,
                path_name,
                operation,
                status,
                start_time.isoformat() if start_time else None,
                end_time.isoformat() if end_time else None,
                duration_ms,
                steps_completed,
                total_steps,
                json.dumps(metadata) if metadata else None,
                error_message,
            ),
        )
        self.db.commit()
        return cursor.lastrowid

    def log_error(
        self,
        error_type: str,
        error_message: str,
        severity: str = "error",
        error_code: Optional[str] = None,
        stack_trace: Optional[str] = None,
        module_name: Optional[str] = None,
        function_name: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> int:
        """تسجيل الأخطاء والاستثناءات"""
        if not self.db:
            return 0

        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO error_log (
                error_type, error_code, error_message, stack_trace,
                module_name, function_name, user_id, severity
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                error_type,
                error_code,
                error_message,
                stack_trace,
                module_name,
                function_name,
                user_id,
                severity,
            ),
        )
        self.db.commit()
        return cursor.lastrowid

    def get_user_activities(
        self,
        user_id: Optional[int] = None,
        activity_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
    ) -> list:
        """الحصول على أنشطة المستخدمين"""
        if not self.db:
            return []

        cursor = self.db.cursor()
        query = "SELECT * FROM user_activity_log WHERE 1=1"
        params = []

        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        if activity_type:
            query += " AND activity_type = ?"
            params.append(activity_type)
        if start_date:
            query += " AND created_at >= ?"
            params.append(start_date.isoformat())
        if end_date:
            query += " AND created_at <= ?"
            params.append(end_date.isoformat())

        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        return cursor.fetchall()

    def resolve_error(self, error_id: int, resolution_notes: str) -> bool:
        """تحديد خطأ كمحلول"""
        if not self.db:
            return False

        cursor = self.db.cursor()
        cursor.execute(
            """
            UPDATE error_log
            SET resolved = 1, resolution_notes = ?
            WHERE id = ?
        """,
            (resolution_notes, error_id),
        )
        self.db.commit()
        return cursor.rowcount > 0
