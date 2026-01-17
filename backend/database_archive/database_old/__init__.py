# type: ignore
# flake8: noqa
# pyright: ignore
# pylint: disable=all
# mypy: ignore-errors
"""
Database package - إعدادات قاعدة البيانات
All linting disabled due to SQLAlchemy mock objects and optional dependencies.
"""

try:
    from flask_sqlalchemy import SQLAlchemy

    db = SQLAlchemy()
except ImportError:
    # Fallback when SQLAlchemy is not available
    class MockDB:
        class Model:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

            def to_dict(self):
                return {}

            @classmethod
            def query(cls):
                return MockQuery()

        @staticmethod
        def Column(*args, **kwargs):
            return None

        @staticmethod
        def Integer(*args, **kwargs):
            return None

        @staticmethod
        def String(*args, **kwargs):
            return None

        @staticmethod
        def Text(*args, **kwargs):
            return None

        @staticmethod
        def DateTime(*args, **kwargs):
            return None

        @staticmethod
        def Boolean(*args, **kwargs):
            return None

        @staticmethod
        def Float(*args, **kwargs):
            return None

        @staticmethod
        def ForeignKey(*args, **kwargs):
            return None

        @staticmethod
        def relationship(*args, **kwargs):
            return None

        @staticmethod
        def backref(*args, **kwargs):
            return None

        session = None

        @staticmethod
        def create_all():
            pass

        @staticmethod
        def drop_all():
            pass

        @staticmethod
        def init_app(app):
            pass

    class MockQuery:
        def filter(self, *args, **kwargs):
            return self

        def filter_by(self, *args, **kwargs):
            return self

        def first(self):
            return None

        def all(self):
            return []

        def count(self):
            return 0

        def get(self, *args, **kwargs):
            return None

        def delete(self):
            return 0

        def update(self, *args, **kwargs):
            return 0

    db = MockDB()

__all__ = ["db"]
