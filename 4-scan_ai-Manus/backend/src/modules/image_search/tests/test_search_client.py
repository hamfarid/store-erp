# /home/ubuntu/image_search_integration/tests/test_search_client.py
"""
اختبارات وحدة عميل البحث عن صور الإصابات والآفات النباتية
Unit tests for plant disease and pest image search client
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

from search_client import WebSearchClient

# إضافة المجلد الأصلي إلى مسار البحث
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestWebSearchClient(unittest.TestCase):
    """اختبارات وحدة لفئة WebSearchClient."""

    def setUp(self):
        """إعداد بيئة الاختبار."""
        # تهيئة عميل البحث مع مفاتيح اختبار
        self.client = WebSearchClient(
            api_key="test_api_key",
            engine_id="test_engine_id",
            endpoint="https://test-api.example.com/search"
        )

    def test_init(self):
        """اختبار تهيئة عميل البحث."""
        self.assertEqual(self.client.api_key, "test_api_key")
        self.assertEqual(self.client.engine_id, "test_engine_id")
        self.assertEqual(
            self.client.endpoint,
            "https://test-api.example.com/search")

    @patch('search_client.requests.get')
    def test_search_images_success(self, mock_get):
        """اختبار البحث عن الصور بنجاح."""
        # إعداد استجابة وهمية
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "items": [
                {"link": "https://example.com/image1.jpg"},
                {"link": "https://example.com/image2.jpg"},
                {"link": "https://example.com/image3.jpg"}
            ]
        }
        mock_get.return_value = mock_response

        # تنفيذ البحث
        results = self.client.search_images("test query", count=3)

        # التحقق من النتائج
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0], "https://example.com/image1.jpg")
        self.assertEqual(results[1], "https://example.com/image2.jpg")
        self.assertEqual(results[2], "https://example.com/image3.jpg")

        # التحقق من استدعاء requests.get بالمعلمات الصحيحة
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], "https://test-api.example.com/search")
        self.assertEqual(kwargs["params"]["key"], "test_api_key")
        self.assertEqual(kwargs["params"]["cx"], "test_engine_id")
        self.assertEqual(kwargs["params"]["q"], "test query")
        self.assertEqual(kwargs["params"]["searchType"], "image")
        self.assertEqual(kwargs["params"]["num"], 3)

    @patch('search_client.requests.get')
    def test_search_images_no_results(self, mock_get):
        """اختبار البحث عن الصور بدون نتائج."""
        # إعداد استجابة وهمية بدون نتائج
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = {}  # لا توجد عناصر
        mock_get.return_value = mock_response

        # تنفيذ البحث
        results = self.client.search_images("test query", count=3)

        # التحقق من النتائج
        self.assertEqual(len(results), 0)

    @patch('search_client.requests.get')
    def test_search_images_api_error(self, mock_get):
        """اختبار البحث عن الصور مع خطأ في API."""
        # إعداد استجابة وهمية مع خطأ
        mock_get.side_effect = Exception("API Error")

        # تنفيذ البحث
        results = self.client.search_images("test query", count=3)

        # التحقق من النتائج (يجب أن تكون قائمة فارغة في حالة الخطأ)
        self.assertEqual(len(results), 0)

    def test_simulate_search_images(self):
        """اختبار محاكاة البحث عن الصور."""
        # تنفيذ البحث المحاكى
        results = self.client._simulate_search_images("test query", count=5)

        # التحقق من النتائج
        self.assertEqual(len(results), 5)
        for url in results:
            self.assertTrue(url.startswith("https://"))
            self.assertTrue("test_query" in url or "test" in url)

    @patch('search_client.requests.get')
    def test_search_images_by_disease(self, mock_get):
        """اختبار البحث عن صور المرض."""
        # إعداد استجابة وهمية
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "items": [
                {"link": "https://example.com/disease1.jpg"},
                {"link": "https://example.com/disease2.jpg"}
            ]
        }
        mock_get.return_value = mock_response

        # تنفيذ البحث
        results = self.client.search_images_by_disease("leaf rust", count=2)

        # التحقق من النتائج
        self.assertEqual(len(results), 2)

        # التحقق من استدعاء search_images بالمعلمات الصحيحة
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertTrue(
            "plant disease leaf rust symptoms" in kwargs["params"]["q"])

    @patch('search_client.requests.get')
    def test_search_images_by_pest(self, mock_get):
        """اختبار البحث عن صور الآفة."""
        # إعداد استجابة وهمية
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "items": [
                {"link": "https://example.com/pest1.jpg"},
                {"link": "https://example.com/pest2.jpg"}
            ]
        }
        mock_get.return_value = mock_response

        # تنفيذ البحث
        results = self.client.search_images_by_pest("aphid", count=2)

        # التحقق من النتائج
        self.assertEqual(len(results), 2)

        # التحقق من استدعاء search_images بالمعلمات الصحيحة
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertTrue("agricultural pest aphid" in kwargs["params"]["q"])

    @patch('search_client.requests.get')
    def test_search_images_by_crop(self, mock_get):
        """اختبار البحث عن صور المحصول."""
        # إعداد استجابة وهمية
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "items": [
                {"link": "https://example.com/crop1.jpg"},
                {"link": "https://example.com/crop2.jpg"}
            ]
        }
        mock_get.return_value = mock_response

        # تنفيذ البحث
        results = self.client.search_images_by_crop(
            "wheat", condition="healthy", count=2)

        # التحقق من النتائج
        self.assertEqual(len(results), 2)

        # التحقق من استدعاء search_images بالمعلمات الصحيحة
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertTrue(
            "wheat plant healthy condition" in kwargs["params"]["q"])


if __name__ == '__main__':
    unittest.main()
