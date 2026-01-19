# /home/ubuntu/image_search_integration/auto_learning/tests/test_keyword_service.py
"""
اختبارات وحدة لخدمة إدارة الكلمات المفتاحية

يحتوي هذا الملف على اختبارات وحدة لخدمة إدارة الكلمات المفتاحية في مديول البحث الذاتي الذكي،
للتأكد من صحة عمليات إنشاء وتحديث وحذف الكلمات المفتاحية وإدارة العلاقات بينها.
"""

from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.orm import Session

from modules.image_search.auto_learning.keyword_management.models import (
    Keyword,
    KeywordRelation,
)
from modules.image_search.auto_learning.keyword_management.schemas import (
    KeywordCreate,
    KeywordRelationCreate,
    KeywordUpdate,
)
from modules.image_search.auto_learning.keyword_management.service import KeywordService


class TestKeywordService:
    """اختبارات خدمة إدارة الكلمات المفتاحية"""

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
    def keyword_service(self, db_session):
        """
        تجهيز خدمة إدارة الكلمات المفتاحية للاختبارات

        Args:
            db_session: جلسة قاعدة البيانات الوهمية

        Returns:
            KeywordService: كائن خدمة إدارة الكلمات المفتاحية
        """
        return KeywordService(db_session)

    def test_create_keyword(self, keyword_service, db_session):
        """
        اختبار إنشاء كلمة مفتاحية جديدة

        Args:
            keyword_service: خدمة إدارة الكلمات المفتاحية
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        keyword_data = KeywordCreate(
            text="تبقع أوراق",
            category="disease",
            plant_part="leaf",
            description="مرض فطري يصيب أوراق النباتات",
            importance=8
        )

        # تجهيز السلوك المتوقع
        mock_keyword = MagicMock(spec=Keyword)
        mock_keyword.id = 1
        mock_keyword.text = keyword_data.text
        mock_keyword.category = keyword_data.category
        mock_keyword.plant_part = keyword_data.plant_part
        mock_keyword.description = keyword_data.description
        mock_keyword.importance = keyword_data.importance

        db_session.query.return_value.filter.return_value.first.return_value = None
        db_session.add.return_value = None
        db_session.commit.return_value = None
        db_session.refresh.return_value = None

        # تنفيذ الاختبار
        with patch('modules.image_search.auto_learning.keyword_management.service.Keyword', return_value=mock_keyword):
            result = keyword_service.create_keyword(keyword_data)

        # التحقق من النتائج
        assert result is not None
        assert result.text == keyword_data.text
        assert result.category == keyword_data.category
        assert result.plant_part == keyword_data.plant_part
        assert result.description == keyword_data.description
        assert result.importance == keyword_data.importance

        db_session.add.assert_called_once()
        db_session.commit.assert_called_once()
        db_session.refresh.assert_called_once()

    def test_create_keyword_already_exists(self, keyword_service, db_session):
        """
        اختبار إنشاء كلمة مفتاحية موجودة بالفعل

        Args:
            keyword_service: خدمة إدارة الكلمات المفتاحية
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        keyword_data = KeywordCreate(
            text="تبقع أوراق",
            category="disease",
            plant_part="leaf",
            description="مرض فطري يصيب أوراق النباتات",
            importance=8
        )

        # تجهيز السلوك المتوقع
        mock_existing_keyword = MagicMock(spec=Keyword)
        db_session.query.return_value.filter.return_value.first.return_value = mock_existing_keyword

        # تنفيذ الاختبار والتحقق من النتائج
        with pytest.raises(ValueError, match="الكلمة المفتاحية موجودة بالفعل"):
            keyword_service.create_keyword(keyword_data)

    def test_get_keyword(self, keyword_service, db_session):
        """
        اختبار الحصول على كلمة مفتاحية محددة

        Args:
            keyword_service: خدمة إدارة الكلمات المفتاحية
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        keyword_id = 1

        # تجهيز السلوك المتوقع
        mock_keyword = MagicMock(spec=Keyword)
        mock_keyword.id = keyword_id
        mock_keyword.text = "تبقع أوراق"

        db_session.query.return_value.filter.return_value.first.return_value = mock_keyword

        # تنفيذ الاختبار
        result = keyword_service.get_keyword(keyword_id)

        # التحقق من النتائج
        assert result is not None
        assert result.id == keyword_id
        assert result.text == "تبقع أوراق"

    def test_get_keyword_not_found(self, keyword_service, db_session):
        """
        اختبار الحصول على كلمة مفتاحية غير موجودة

        Args:
            keyword_service: خدمة إدارة الكلمات المفتاحية
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        keyword_id = 999

        # تجهيز السلوك المتوقع
        db_session.query.return_value.filter.return_value.first.return_value = None

        # تنفيذ الاختبار
        result = keyword_service.get_keyword(keyword_id)

        # التحقق من النتائج
        assert result is None

    def test_update_keyword(self, keyword_service, db_session):
        """
        اختبار تحديث كلمة مفتاحية

        Args:
            keyword_service: خدمة إدارة الكلمات المفتاحية
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        keyword_id = 1
        keyword_update = KeywordUpdate(
            description="وصف محدث للكلمة المفتاحية",
            importance=9
        )

        # تجهيز السلوك المتوقع
        mock_keyword = MagicMock(spec=Keyword)
        mock_keyword.id = keyword_id
        mock_keyword.text = "تبقع أوراق"

        db_session.query.return_value.filter.return_value.first.return_value = mock_keyword
        db_session.commit.return_value = None

        # تنفيذ الاختبار
        result = keyword_service.update_keyword(keyword_id, keyword_update)

        # التحقق من النتائج
        assert result is not None
        assert result.id == keyword_id
        assert result.description == keyword_update.description
        assert result.importance == keyword_update.importance

        db_session.commit.assert_called_once()

    def test_update_keyword_not_found(self, keyword_service, db_session):
        """
        اختبار تحديث كلمة مفتاحية غير موجودة

        Args:
            keyword_service: خدمة إدارة الكلمات المفتاحية
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        keyword_id = 999
        keyword_update = KeywordUpdate(
            description="وصف محدث للكلمة المفتاحية",
            importance=9
        )

        # تجهيز السلوك المتوقع
        db_session.query.return_value.filter.return_value.first.return_value = None

        # تنفيذ الاختبار
        result = keyword_service.update_keyword(keyword_id, keyword_update)

        # التحقق من النتائج
        assert result is None

    def test_delete_keyword(self, keyword_service, db_session):
        """
        اختبار حذف كلمة مفتاحية

        Args:
            keyword_service: خدمة إدارة الكلمات المفتاحية
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        keyword_id = 1

        # تجهيز السلوك المتوقع
        mock_keyword = MagicMock(spec=Keyword)
        db_session.query.return_value.filter.return_value.first.return_value = mock_keyword
        db_session.delete.return_value = None
        db_session.commit.return_value = None

        # تنفيذ الاختبار
        result = keyword_service.delete_keyword(keyword_id)

        # التحقق من النتائج
        assert result is True
        db_session.delete.assert_called_once_with(mock_keyword)
        db_session.commit.assert_called_once()

    def test_delete_keyword_not_found(self, keyword_service, db_session):
        """
        اختبار حذف كلمة مفتاحية غير موجودة

        Args:
            keyword_service: خدمة إدارة الكلمات المفتاحية
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        keyword_id = 999

        # تجهيز السلوك المتوقع
        db_session.query.return_value.filter.return_value.first.return_value = None

        # تنفيذ الاختبار
        result = keyword_service.delete_keyword(keyword_id)

        # التحقق من النتائج
        assert result is False
        db_session.delete.assert_not_called()

    def test_add_keyword_relation(self, keyword_service, db_session):
        """
        اختبار إضافة علاقة بين كلمتين مفتاحيتين

        Args:
            keyword_service: خدمة إدارة الكلمات المفتاحية
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        source_id = 1
        relation_data = KeywordRelationCreate(
            target_id=2,
            relation_type="synonym"
        )

        # تجهيز السلوك المتوقع
        mock_source = MagicMock(spec=Keyword)
        mock_source.id = source_id

        mock_target = MagicMock(spec=Keyword)
        mock_target.id = relation_data.target_id

        mock_relation = MagicMock(spec=KeywordRelation)
        mock_relation.id = 1
        mock_relation.source_id = source_id
        mock_relation.target_id = relation_data.target_id
        mock_relation.relation_type = relation_data.relation_type

        db_session.query.side_effect = [
            MagicMock(
                filter=MagicMock(
                    return_value=MagicMock(
                        first=MagicMock(
                            return_value=mock_source)))), MagicMock(
                filter=MagicMock(
                    return_value=MagicMock(
                        first=MagicMock(
                            return_value=mock_target)))), MagicMock(
                filter=MagicMock(
                    return_value=MagicMock(
                        first=MagicMock(
                            return_value=None))))]

        db_session.add.return_value = None
        db_session.commit.return_value = None
        db_session.refresh.return_value = None

        # تنفيذ الاختبار
        with patch('modules.image_search.auto_learning.keyword_management.service.KeywordRelation', return_value=mock_relation):
            result = keyword_service.add_keyword_relation(
                source_id, relation_data)

        # التحقق من النتائج
        assert result is not None
        assert result.source_id == source_id
        assert result.target_id == relation_data.target_id
        assert result.relation_type == relation_data.relation_type

        db_session.add.assert_called_once()
        db_session.commit.assert_called_once()
        db_session.refresh.assert_called_once()

    def test_add_keyword_relation_source_not_found(
            self, keyword_service, db_session):
        """
        اختبار إضافة علاقة مع كلمة مفتاحية مصدر غير موجودة

        Args:
            keyword_service: خدمة إدارة الكلمات المفتاحية
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        source_id = 999
        relation_data = KeywordRelationCreate(
            target_id=2,
            relation_type="synonym"
        )

        # تجهيز السلوك المتوقع
        db_session.query.return_value.filter.return_value.first.return_value = None

        # تنفيذ الاختبار والتحقق من النتائج
        with pytest.raises(ValueError, match="الكلمة المفتاحية المصدر غير موجودة"):
            keyword_service.add_keyword_relation(source_id, relation_data)

    def test_get_keywords(self, keyword_service, db_session):
        """
        اختبار الحصول على قائمة الكلمات المفتاحية

        Args:
            keyword_service: خدمة إدارة الكلمات المفتاحية
            db_session: جلسة قاعدة البيانات الوهمية
        """
        # تجهيز البيانات
        skip = 0
        limit = 10
        category = "disease"
        plant_part = "leaf"
        search = "تبقع"

        # تجهيز السلوك المتوقع
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query

        mock_keywords = [MagicMock(spec=Keyword) for _ in range(3)]
        mock_query.all.return_value = mock_keywords

        db_session.query.return_value = mock_query

        # تنفيذ الاختبار
        result = keyword_service.get_keywords(
            skip, limit, category, plant_part, search)

        # التحقق من النتائج
        assert result is not None
        assert len(result) == 3
        mock_query.offset.assert_called_once_with(skip)
        mock_query.limit.assert_called_once_with(limit)


if __name__ == "__main__":
    pytest.main()
