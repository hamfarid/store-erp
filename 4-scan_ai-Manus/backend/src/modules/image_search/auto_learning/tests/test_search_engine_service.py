# /home/ubuntu/image_search_integration/auto_learning/tests/test_search_engine_service.py
"""
اختبارات وحدة لخدمة إدارة محركات البحث

يحتوي هذا الملف على اختبارات وحدة لخدمة إدارة محركات البحث في مديول البحث الذاتي الذكي،
للتأكد من صحة عمليات إنشاء وتحديث وحذف محركات البحث وإدارة توزيع الحمل.
"""

from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.orm import Session

from modules.image_search.auto_learning.search_engine_management.models import (
    SearchEngine,
    SearchEngineUsage,
)
from modules.image_search.auto_learning.search_engine_management.schemas import (
    SearchEngineCreate,
    SearchEngineUpdate,
)
from modules.image_search.auto_learning.search_engine_management.service import (
    SearchEngineService,
)


class TestSearchEngineService:
    """اختبارات خدمة إدارة محركات البحث"""

    @pytest.fixture
    def db_session(self):
        """
        تجهيز جلسة قاعدة بيانات وهمية للاختبارات

        Returns:
            MagicMock: كائن وهمي لجلسة قاعدة البيانات
        """
        session = MagicMock(spec=Session)
        return session

    @pytest.fixture
    def search_engine_service(self, db_session):
        """
        تجهيز خدمة إدارة محركات البحث للاختبارات

        Args:
            db_session: جلسة قاعدة البيانات الوهمية

        Returns:
            SearchEngineService: كائن خدمة إدارة محركات البحث
        """
        return SearchEngineService(db_session)

    def test_create_search_engine(self, search_engine_service, db_session):
        """
        اختبار إنشاء محرك بحث جديد

        Args:
            search_engine_service: خدمة إدارة محركات البحث
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        engine_data = SearchEngineCreate(
            name="Google Custom Search",
            base_url="https://www.googleapis.com/customsearch/v1",
            api_key="test_api_key",
            description="محرك بحث جوجل المخصص",
            weight=10,
            is_active=True,
            rate_limit=100,
            timeout=5
        )

        # تجهيز السلوك المتوقع
        mock_engine = MagicMock(spec=SearchEngine)
        mock_engine.id = 1
        mock_engine.name = engine_data.name
        mock_engine.base_url = engine_data.base_url
        mock_engine.api_key = engine_data.api_key
        mock_engine.description = engine_data.description
        mock_engine.weight = engine_data.weight
        mock_engine.is_active = engine_data.is_active
        mock_engine.rate_limit = engine_data.rate_limit
        mock_engine.timeout = engine_data.timeout

        db_session.query.return_value.filter.return_value.first.return_value = None
        db_session.add.return_value = None
        db_session.commit.return_value = None
        db_session.refresh.return_value = None

        # تنفيذ الاختبار
        with patch('modules.image_search.auto_learning.search_engine_management.service.SearchEngine', return_value=mock_engine):
            result = search_engine_service.create_search_engine(engine_data)

        # التحقق من النتائج
        assert result is not None
        assert result.name == engine_data.name
        assert result.base_url == engine_data.base_url
        assert result.api_key == engine_data.api_key
        assert result.description == engine_data.description
        assert result.weight == engine_data.weight
        assert result.is_active == engine_data.is_active
        assert result.rate_limit == engine_data.rate_limit
        assert result.timeout == engine_data.timeout

        db_session.add.assert_called_once()
        db_session.commit.assert_called_once()
        db_session.refresh.assert_called_once()

    def test_create_search_engine_already_exists(
            self, search_engine_service, db_session):
        """
        اختبار إنشاء محرك بحث موجود بالفعل

        Args:
            search_engine_service: خدمة إدارة محركات البحث
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        engine_data = SearchEngineCreate(
            name="Google Custom Search",
            base_url="https://www.googleapis.com/customsearch/v1",
            api_key="test_api_key",
            description="محرك بحث جوجل المخصص",
            weight=10,
            is_active=True,
            rate_limit=100,
            timeout=5
        )

        # تجهيز السلوك المتوقع
        mock_existing_engine = MagicMock(spec=SearchEngine)
        db_session.query.return_value.filter.return_value.first.return_value = mock_existing_engine

        # تنفيذ الاختبار والتحقق من النتائج
        with pytest.raises(ValueError, match="محرك البحث موجود بالفعل"):
            search_engine_service.create_search_engine(engine_data)

    def test_get_search_engine(self, search_engine_service, db_session):
        """
        اختبار الحصول على محرك بحث محدد

        Args:
            search_engine_service: خدمة إدارة محركات البحث
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        engine_id = 1

        # تجهيز السلوك المتوقع
        mock_engine = MagicMock(spec=SearchEngine)
        mock_engine.id = engine_id
        mock_engine.name = "Google Custom Search"

        db_session.query.return_value.filter.return_value.first.return_value = mock_engine

        # تنفيذ الاختبار
        result = search_engine_service.get_search_engine(engine_id)

        # التحقق من النتائج
        assert result is not None
        assert result.id == engine_id
        assert result.name == "Google Custom Search"

    def test_update_search_engine(self, search_engine_service, db_session):
        """
        اختبار تحديث محرك بحث

        Args:
            search_engine_service: خدمة إدارة محركات البحث
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        engine_id = 1
        engine_update = SearchEngineUpdate(
            description="وصف محدث لمحرك البحث",
            weight=15,
            is_active=False
        )

        # تجهيز السلوك المتوقع
        mock_engine = MagicMock(spec=SearchEngine)
        mock_engine.id = engine_id
        mock_engine.name = "Google Custom Search"

        db_session.query.return_value.filter.return_value.first.return_value = mock_engine
        db_session.commit.return_value = None

        # تنفيذ الاختبار
        result = search_engine_service.update_search_engine(
            engine_id, engine_update)

        # التحقق من النتائج
        assert result is not None
        assert result.id == engine_id
        assert result.description == engine_update.description
        assert result.weight == engine_update.weight
        assert result.is_active == engine_update.is_active

        db_session.commit.assert_called_once()

    def test_delete_search_engine(self, search_engine_service, db_session):
        """
        اختبار حذف محرك بحث

        Args:
            search_engine_service: خدمة إدارة محركات البحث
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        engine_id = 1

        # تجهيز السلوك المتوقع
        mock_engine = MagicMock(spec=SearchEngine)
        db_session.query.return_value.filter.return_value.first.return_value = mock_engine
        db_session.delete.return_value = None
        db_session.commit.return_value = None

        # تنفيذ الاختبار
        result = search_engine_service.delete_search_engine(engine_id)

        # التحقق من النتائج
        assert result is True
        db_session.delete.assert_called_once_with(mock_engine)
        db_session.commit.assert_called_once()

    def test_get_next_search_engine_round_robin(
            self, search_engine_service, db_session):
        """
        اختبار الحصول على محرك البحث التالي باستخدام استراتيجية round robin

        Args:
            search_engine_service: خدمة إدارة محركات البحث
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        strategy = "round_robin"

        # تجهيز السلوك المتوقع
        mock_engines = [MagicMock(spec=SearchEngine) for _ in range(3)]
        for i, engine in enumerate(mock_engines):
            engine.id = i + 1
            engine.name = f"Engine {i + 1}"
            engine.is_active = True

        db_session.query.return_value.filter.return_value.all.return_value = mock_engines

        # تنفيذ الاختبار
        result1 = search_engine_service.get_next_search_engine(strategy)
        result2 = search_engine_service.get_next_search_engine(strategy)
        result3 = search_engine_service.get_next_search_engine(strategy)
        result4 = search_engine_service.get_next_search_engine(strategy)

        # التحقق من النتائج
        assert result1.id == 1
        assert result2.id == 2
        assert result3.id == 3
        assert result4.id == 1  # يعود للبداية بعد استنفاد جميع المحركات

    def test_record_search_engine_usage(
            self, search_engine_service, db_session):
        """
        اختبار تسجيل استخدام محرك بحث

        Args:
            search_engine_service: خدمة إدارة محركات البحث
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        engine_id = 1
        query = "تبقع أوراق الطماطم"
        result_count = 15
        response_time = 1.5
        success = True

        # تجهيز السلوك المتوقع
        mock_usage = MagicMock(spec=SearchEngineUsage)
        mock_usage.id = 1
        mock_usage.engine_id = engine_id
        mock_usage.query = query
        mock_usage.result_count = result_count
        mock_usage.response_time = response_time
        mock_usage.success = success

        db_session.add.return_value = None
        db_session.commit.return_value = None

        # تنفيذ الاختبار
        with patch('modules.image_search.auto_learning.search_engine_management.service.SearchEngineUsage', return_value=mock_usage):
            result = search_engine_service.record_search_engine_usage(
                engine_id, query, result_count, response_time, success
            )

        # التحقق من النتائج
        assert result is not None
        assert result.engine_id == engine_id
        assert result.query == query
        assert result.result_count == result_count
        # Use approximate comparison for floats
        assert abs(result.response_time - response_time) < 0.001
        assert result.success == success

        db_session.add.assert_called_once()
        db_session.commit.assert_called_once()


if __name__ == "__main__":
    pytest.main()
