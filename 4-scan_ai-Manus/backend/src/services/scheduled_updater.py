"""
نظام التحديث التلقائي المجدول
Scheduled Auto-Update System
"""

import logging
from datetime import datetime
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from ..core.database import SessionLocal
from .data_sources import get_data_source_manager
from .database_updater import get_database_updater

logger = logging.getLogger(__name__)


class ScheduledUpdater:
    """مدير التحديثات المجدولة"""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
        self.update_history = []

    def start(self):
        """بدء المجدول"""
        if not self.is_running:
            # تحديث قاعدة البيانات - أسبوعياً يوم الأحد 2 صباحاً
            self.scheduler.add_job(
                self._update_database_job,
                CronTrigger(day_of_week='sun', hour=2, minute=0),
                id='weekly_database_update',
                name='Weekly Database Update',
                replace_existing=True
            )

            # تحديث نقص العناصر - شهرياً في اليوم الأول 3 صباحاً
            self.scheduler.add_job(
                self._update_nutrients_job,
                CronTrigger(day=1, hour=3, minute=0),
                id='monthly_nutrients_update',
                name='Monthly Nutrients Update',
                replace_existing=True
            )

            # فحص المصادر - يومياً 4 صباحاً
            self.scheduler.add_job(
                self._check_sources_job,
                CronTrigger(hour=4, minute=0),
                id='daily_sources_check',
                name='Daily Sources Check',
                replace_existing=True
            )

            # تنظيف السجلات القديمة - أسبوعياً
            self.scheduler.add_job(
                self._cleanup_old_logs,
                CronTrigger(day_of_week='sat', hour=1, minute=0),
                id='weekly_cleanup',
                name='Weekly Cleanup',
                replace_existing=True
            )

            self.scheduler.start()
            self.is_running = True
            logger.info("Scheduled updater started successfully")

    def stop(self):
        """إيقاف المجدول"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("Scheduled updater stopped")

    async def _update_database_job(self):
        """مهمة تحديث قاعدة البيانات"""
        logger.info("Starting scheduled database update...")

        db = SessionLocal()
        try:
            updater = get_database_updater(db)
            stats = await updater.update_disease_database(
                force_update=False,
                update_images=True
            )

            self._log_update("database_update", stats)
            logger.info(f"Database update completed: {stats}")

        except Exception as e:
            logger.error(f"Database update failed: {e}")
            self._log_update("database_update", {"error": str(e)})
        finally:
            db.close()

    async def _update_nutrients_job(self):
        """مهمة تحديث نقص العناصر"""
        logger.info("Starting scheduled nutrients update...")

        db = SessionLocal()
        try:
            updater = get_database_updater(db)
            stats = await updater.update_nutrient_deficiencies()

            self._log_update("nutrients_update", stats)
            logger.info(f"Nutrients update completed: {stats}")

        except Exception as e:
            logger.error(f"Nutrients update failed: {e}")
            self._log_update("nutrients_update", {"error": str(e)})
        finally:
            db.close()

    async def _check_sources_job(self):
        """مهمة فحص المصادر"""
        logger.info("Starting scheduled sources check...")

        try:
            async with get_data_source_manager() as dsm:
                results = {}

                for source in dsm.sources:
                    is_available = await dsm.check_source_availability(source)
                    results[source.name] = {
                        "available": is_available,
                        "url": source.url,
                        "checked_at": datetime.utcnow().isoformat()
                    }

                # حساب الإحصائيات
                available_count = sum(1 for r in results.values() if r["available"])
                total_count = len(results)

                stats = {
                    "total_sources": total_count,
                    "available_sources": available_count,
                    "unavailable_sources": total_count - available_count,
                    "availability_rate": f"{(available_count/total_count)*100:.2f}%",
                    "results": results
                }

                self._log_update("sources_check", stats)
                logger.info(f"Sources check completed: {available_count}/{total_count} available")

        except Exception as e:
            logger.error(f"Sources check failed: {e}")
            self._log_update("sources_check", {"error": str(e)})

    async def _cleanup_old_logs(self):
        """تنظيف السجلات القديمة"""
        logger.info("Starting scheduled cleanup...")

        try:
            # الاحتفاظ بآخر 100 سجل فقط
            if len(self.update_history) > 100:
                removed_count = len(self.update_history) - 100
                self.update_history = self.update_history[-100:]
                logger.info(f"Cleaned up {removed_count} old log entries")

        except Exception as e:
            logger.error(f"Cleanup failed: {e}")

    def _log_update(self, update_type: str, stats: dict):
        """تسجيل التحديث"""
        log_entry = {
            "type": update_type,
            "timestamp": datetime.utcnow().isoformat(),
            "stats": stats
        }
        self.update_history.append(log_entry)

    def get_update_history(self, limit: int = 20) -> list:
        """الحصول على سجل التحديثات"""
        return self.update_history[-limit:]

    def get_next_run_times(self) -> dict:
        """الحصول على أوقات التشغيل التالية"""
        jobs = self.scheduler.get_jobs()
        return {
            job.id: {
                "name": job.name,
                "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None
            }
            for job in jobs
        }

    def trigger_manual_update(self, update_type: str = "database"):
        """تشغيل تحديث يدوي"""
        if update_type == "database":
            self.scheduler.add_job(
                self._update_database_job,
                'date',
                run_date=datetime.now(),
                id='manual_database_update'
            )
        elif update_type == "nutrients":
            self.scheduler.add_job(
                self._update_nutrients_job,
                'date',
                run_date=datetime.now(),
                id='manual_nutrients_update'
            )
        elif update_type == "sources":
            self.scheduler.add_job(
                self._check_sources_job,
                'date',
                run_date=datetime.now(),
                id='manual_sources_check'
            )

        logger.info(f"Manual {update_type} update triggered")


# مثيل عام للمجدول
_scheduler_instance: Optional[ScheduledUpdater] = None


def get_scheduled_updater() -> ScheduledUpdater:
    """الحصول على مثيل المجدول"""
    global _scheduler_instance

    if _scheduler_instance is None:
        _scheduler_instance = ScheduledUpdater()

    return _scheduler_instance


def start_scheduled_updates():
    """بدء التحديثات المجدولة"""
    updater = get_scheduled_updater()
    updater.start()


def stop_scheduled_updates():
    """إيقاف التحديثات المجدولة"""
    updater = get_scheduled_updater()
    updater.stop()
