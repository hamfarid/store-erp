#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار النماذج
Test models
"""

print("1. Importing database...")
from src.database import db

print("2. Importing User from models...")
from src.models import User

print("3. Checking User class...")
print(f"   User class: {User}")
print(f"   User.__tablename__: {User.__tablename__}")
print(f"   User.__module__: {User.__module__}")

print("4. Checking db.Model registry...")
from sqlalchemy import inspect
mapper = inspect(User)
print(f"   Mapper: {mapper}")
print(f"   Mapped class: {mapper.class_}")

print("5. Trying to query User...")
try:
    user = User.query.first()
    print(f"   Query successful: {user}")
except Exception as e:
    print(f"   Query failed: {e}")

print("\n✅ Test complete!")

