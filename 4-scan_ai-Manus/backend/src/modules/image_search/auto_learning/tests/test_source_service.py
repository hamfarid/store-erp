# /home/ubuntu/image_search_integration/auto_learning/tests/test_source_service.py
"""
اختبارات وحدة لخدمة إدارة المصادر الموثوقة

يحتوي هذا الملف على اختبارات وحدة لخدمة إدارة المصادر الموثوقة في مديول البحث الذاتي الذكي،
للتأكد من صحة عمليات إنشاء وتحديث وحذف المصادر وإدارة مستويات الثقة.
"""

from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.orm import Session

from modules.image_search.auto_learning.source_management.models import (
    Source,
    SourceVerification,
)
from modules.image_search.auto_learning.source_management.schemas import (
    SourceCreate,
    SourceVerificationCreate,
)
from modules.image_search.auto_learning.source_management.service import SourceService


class TestSourceService:
    """اختبارات خدمة إدارة المصادر الموثوقة"""

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
    def source_service(self, db_session):
        """
        تجهيز خدمة إدارة المصادر الموثوقة للاختبارات

        Args:
            db_session: جلسة قاعدة البيانات الوهمية

        Returns:
            SourceService: كائن خدمة إدارة المصادر الموثوقة
        """
        return SourceService(db_session)

    def test_create_source(self, source_service, db_session):
        """
        اختبار إنشاء مصدر موثوق جديد

        Args:
            source_service: خدمة إدارة المصادر الموثوقة
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        source_data = SourceCreate(
            name="موقع وزارة الزراعة",
            url="https://agriculture.gov.example",
            description="الموقع الرسمي لوزارة الزراعة",
            category="government",
            trust_level=9.5
        )

        # تجهيز السلوك المتوقع
        mock_source = MagicMock(spec=Source)
        mock_source.id = 1
        mock_source.name = source_data.name
        mock_source.url = source_data.url
        mock_source.description = source_data.description
        mock_source.category = source_data.category
        mock_source.trust_level = source_data.trust_level

        db_session.query.return_value.filter.return_value.first.return_value = None
        db_session.add.return_value = None
        db_session.commit.return_value = None
        db_session.refresh.return_value = None

        # تنفيذ الاختبار
        with patch('modules.image_search.auto_learning.source_management.service.Source', return_value=mock_source):
            result = source_service.create_source(source_data)

        # التحقق من النتائج
        assert result is not None
        assert result.name == source_data.name
        assert result.url == source_data.url
        assert result.description == source_data.description
        assert result.category == source_data.category
        assert abs(result.trust_level - source_data.trust_level) < 0.001

        db_session.add.assert_called_once()
        db_session.commit.assert_called_once()
        db_session.refresh.assert_called_once()

    def test_create_source_already_exists(self, source_service, db_session):
        """
        اختبار إنشاء مصدر موجود بالفعل

        Args:
            source_service: خدمة إدارة المصادر الموثوقة
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        source_data = SourceCreate(
            name="موقع وزارة الزراعة",
            url="https://agriculture.gov.example",
            description="الموقع الرسمي لوزارة الزراعة",
            category="government",
            trust_level=9.5
        )

        # تجهيز السلوك المتوقع
        mock_existing_source = MagicMock(spec=Source)
        db_session.query.return_value.filter.return_value.first.return_value = mock_existing_source

        # تنفيذ الاختبار والتحقق من النتائج
        with pytest.raises(ValueError, match="المصدر موجود بالفعل"):
            source_service.create_source(source_data)

    def test_get_source(self, source_service, db_session):
        """
        اختبار الحصول على مصدر محدد

        Args:
            source_service: خدمة إدارة المصادر الموثوقة
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        source_id = 1

        # تجهيز السلوك المتوقع
        mock_source = MagicMock(spec=Source)
        mock_source.id = source_id
        mock_source.name = "موقع وزارة الزراعة"

        db_session.query.return_value.filter.return_value.first.return_value = mock_source

        # تنفيذ الاختبار
        result = source_service.get_source(source_id)

        # التحقق من النتائج
        assert result is not None
        assert result.id == source_id
        assert result.name == "موقع وزارة الزراعة"

    def test_update_source_trust_level(self, source_service, db_session):
        """
        اختبار تحديث مستوى الثقة لمصدر

        Args:
            source_service: خدمة إدارة المصادر الموثوقة
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        source_id = 1
        new_trust_level = 8.5

        # تجهيز السلوك المتوقع
        mock_source = MagicMock(spec=Source)
        mock_source.id = source_id
        mock_source.name = "موقع وزارة الزراعة"
        mock_source.trust_level = 9.5

        db_session.query.return_value.filter.return_value.first.return_value = mock_source
        db_session.commit.return_value = None

        # تنفيذ الاختبار
        result = source_service.update_source_trust_level(
            source_id, new_trust_level)

        # التحقق من النتائج
        assert result is not None
        assert result.id == source_id
        assert abs(result.trust_level - new_trust_level) < 0.001

        db_session.commit.assert_called_once()

    def test_blacklist_source(self, source_service, db_session):
        """
        اختبار إضافة مصدر إلى القائمة السوداء

        Args:
            source_service: خدمة إدارة المصادر الموثوقة
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        source_id = 1
        reason = "معلومات غير دقيقة"

        # تجهيز السلوك المتوقع
        mock_source = MagicMock(spec=Source)
        mock_source.id = source_id
        mock_source.name = "موقع غير موثوق"
        mock_source.is_blacklisted = False

        db_session.query.return_value.filter.return_value.first.return_value = mock_source
        db_session.commit.return_value = None

        # تنفيذ الاختبار
        result = source_service.blacklist_source(source_id, reason)

        # التحقق من النتائج
        assert result is not None
        assert result.id == source_id
        assert result.is_blacklisted is True
        assert result.blacklist_reason == reason

        db_session.commit.assert_called_once()

    def test_verify_source(self, source_service, db_session):
        """
        اختبار التحقق من مصدر

        Args:
            source_service: خدمة إدارة المصادر الموثوقة
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        source_id = 1
        verification_data = SourceVerificationCreate(
            verified_by="admin",
            verification_method="manual",
            verification_notes="تم التحقق من المصدر يدوياً"
        )

        # تجهيز السلوك المتوقع
        mock_source = MagicMock(spec=Source)
        mock_source.id = source_id
        mock_source.name = "موقع وزارة الزراعة"
        mock_source.is_verified = False

        mock_verification = MagicMock(spec=SourceVerification)
        mock_verification.id = 1
        mock_verification.source_id = source_id
        mock_verification.verified_by = verification_data.verified_by
        mock_verification.verification_method = verification_data.verification_method
        mock_verification.verification_notes = verification_data.verification_notes

        db_session.query.return_value.filter.return_value.first.return_value = mock_source
        db_session.add.return_value = None
        db_session.commit.return_value = None
        db_session.refresh.return_value = None

        # تنفيذ الاختبار
        with patch('modules.image_search.auto_learning.source_management.service.SourceVerification', return_value=mock_verification):
            result = source_service.verify_source(source_id, verification_data)

        # التحقق من النتائج
        assert result is not None
        assert mock_source.is_verified is True

        db_session.add.assert_called_once()
        db_session.commit.assert_called_once()


if __name__ == "__main__":
    pytest.main()
