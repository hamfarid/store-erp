# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
# ▓                                                                             ▓
# ▓                    GAARA ERP v12 - IMPLEMENTATION GUIDE                     ▓
# ▓                          دليل التنفيذ خطوة بخطوة                              ▓
# ▓                                                                             ▓
# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

**Version:** 1.0.0
**Created:** 2026-01-15
**Status:** READY FOR IMPLEMENTATION
**Priority:** Start with Phase 0 Tasks

---

# 🚀 QUICK START

```bash
# 1. Clone and setup
cd D:\Ai_Project\5-gaara_erp

# 2. Backend setup
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 5001

# 3. Frontend setup (new terminal)
cd frontend
npm install
npm run dev -- --port 5501

# 4. Access
# Backend: http://localhost:5001
# Frontend: http://localhost:5501
# Admin: admin / admin123
```

---

# 📋 TABLE OF CONTENTS

1. [Immediate Priority Tasks](#immediate)
2. [Error Fixing Guide](#error-fixing)
3. [Security Implementation](#security)
4. [HR Module Implementation](#hr-module)
5. [Contacts Module Implementation](#contacts-module)
6. [Projects Module Implementation](#projects-module)
7. [Design System Implementation](#design-system)
8. [Testing Implementation](#testing)
9. [Code Templates](#templates)

---

# 🔴 1. IMMEDIATE PRIORITY TASKS {#immediate}

## Implementation Order (Week 1)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    WEEK 1 IMPLEMENTATION PRIORITY                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Day 1-2: ERROR FIXING                                                      │
│  ═══════════════════════════════════════════════════════════════            │
│  □ Task 1.1: Fix F821 errors (68 undefined variables)                       │
│  □ Task 1.2: Fix E9 errors (24 syntax errors)                               │
│                                                                              │
│  Day 3: SECURITY HARDENING                                                  │
│  ═══════════════════════════════════════════════════════════════            │
│  □ Task 2.1: Remove hardcoded secrets                                       │
│  □ Task 2.2: Rotate exposed secrets                                         │
│  □ Task 2.3: Standardize JWT TTL                                            │
│                                                                              │
│  Day 4-5: QUALITY AUTOMATION                                                │
│  ═══════════════════════════════════════════════════════════════            │
│  □ Task 3.1: Configure pre-commit hooks                                     │
│  □ Task 3.2: Fix F811 errors (62 redefinitions)                             │
│  □ Task 3.3: Run full test suite                                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 🔧 2. ERROR FIXING GUIDE {#error-fixing}

## 2.1 Fix F821 Errors (Undefined Variables)

### Step 1: Identify all F821 errors

```bash
cd D:\Ai_Project\5-gaara_erp\backend
flake8 src/ --select=F821 --format='%(path)s:%(row)d:%(col)d: %(code)s %(text)s' > ../errors/f821_errors.txt
```

### Step 2: Common F821 fixes

**Pattern 1: Missing Import**
```python
# ❌ BEFORE (F821: undefined name 'datetime')
def get_timestamp():
    return datetime.now()

# ✅ AFTER
from datetime import datetime

def get_timestamp():
    return datetime.now()
```

**Pattern 2: Typo in Variable Name**
```python
# ❌ BEFORE (F821: undefined name 'usr')
user = User.query.get(id)
return usr.name

# ✅ AFTER
user = User.query.get(id)
return user.name
```

**Pattern 3: Missing Model Import**
```python
# ❌ BEFORE (F821: undefined name 'Product')
def get_products():
    return Product.query.all()

# ✅ AFTER
from src.models.product import Product

def get_products():
    return Product.query.all()
```

### Step 3: Automated fix script

```python
# scripts/fix_f821.py
"""
F821 Error Fixer - Adds missing imports automatically
"""
import re
import os
from pathlib import Path

# Common missing imports mapping
IMPORT_MAP = {
    'datetime': 'from datetime import datetime',
    'timedelta': 'from datetime import timedelta',
    'json': 'import json',
    'request': 'from flask import request',
    'jsonify': 'from flask import jsonify',
    'db': 'from src.database import db',
    'current_user': 'from flask_login import current_user',
}

def fix_f821_in_file(filepath):
    """Add missing imports to a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find undefined names
    # Add imports at top of file
    # Return modified content
    
    # Implementation here...
    pass

if __name__ == '__main__':
    backend_path = Path('D:/Ai_Project/5-gaara_erp/backend/src')
    for py_file in backend_path.rglob('*.py'):
        fix_f821_in_file(py_file)
```

## 2.2 Fix E9 Errors (Syntax Errors)

### Step 1: Identify all E9 errors

```bash
flake8 src/ --select=E9 --format='%(path)s:%(row)d: %(code)s %(text)s' > ../errors/e9_errors.txt
```

### Step 2: Common E9 fixes

**Pattern 1: IndentationError**
```python
# ❌ BEFORE (E901: IndentationError)
def process():
result = compute()
    return result

# ✅ AFTER
def process():
    result = compute()
    return result
```

**Pattern 2: SyntaxError - Missing Colon**
```python
# ❌ BEFORE (E901: SyntaxError)
if user.is_admin
    return True

# ✅ AFTER
if user.is_admin:
    return True
```

**Pattern 3: SyntaxError - Unclosed Bracket**
```python
# ❌ BEFORE (E901: SyntaxError)
data = {
    'name': user.name,
    'email': user.email

# ✅ AFTER
data = {
    'name': user.name,
    'email': user.email,
}
```

### Step 3: Verify fixes

```bash
# Check for remaining syntax errors
python -m py_compile src/models/*.py
python -m py_compile src/routes/*.py
python -m py_compile src/services/*.py
```

## 2.3 Fix F811 Errors (Redefinitions)

### Step 1: Identify all F811 errors

```bash
flake8 src/ --select=F811 --format='%(path)s:%(row)d: %(code)s %(text)s' > ../errors/f811_errors.txt
```

### Step 2: Common F811 fixes

**Pattern 1: Duplicate Function Definition**
```python
# ❌ BEFORE (F811: redefinition of 'get_user')
def get_user(id):
    return User.query.get(id)

def get_user(id):  # F811 error
    user = User.query.get(id)
    return user.to_dict()

# ✅ AFTER (remove duplicate or rename)
def get_user(id):
    return User.query.get(id)

def get_user_dict(id):
    user = User.query.get(id)
    return user.to_dict()
```

**Pattern 2: Duplicate Import**
```python
# ❌ BEFORE (F811: redefinition of 'json')
import json
from flask import json  # F811 error

# ✅ AFTER
from flask import json  # Use only one
```

---

# 🔒 3. SECURITY IMPLEMENTATION {#security}

## 3.1 Remove Hardcoded Secrets

### Step 1: Find hardcoded secrets

```bash
# Search for hardcoded passwords
grep -r "password=" --include="*.py" backend/src/
grep -r "secret=" --include="*.py" backend/src/
grep -r "api_key=" --include="*.py" backend/src/
```

### Step 2: Create secure configuration

```python
# backend/src/config/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings loaded from environment."""
    
    # Database
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///./gaara_erp.db')
    
    # Security - NEVER hardcode these
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY')
    
    # JWT Configuration - Standardized
    JWT_ACCESS_TOKEN_EXPIRES: int = 900  # 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES: int = 604800  # 7 days
    
    # Encryption
    ENCRYPTION_KEY: str = os.getenv('ENCRYPTION_KEY')
    
    def __init__(self):
        self._validate()
    
    def _validate(self):
        """Ensure all required secrets are set."""
        required = ['SECRET_KEY', 'JWT_SECRET_KEY']
        missing = [key for key in required if not getattr(self, key)]
        if missing:
            raise ValueError(f"Missing required environment variables: {missing}")

settings = Settings()
```

### Step 3: Create .env template

```bash
# .env.example (commit this)
# Copy to .env and fill in values (never commit .env)

# =============================================================================
# GAARA ERP v12 - Environment Configuration
# =============================================================================

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/gaara_erp

# Security Keys (generate with: python -c "import secrets; print(secrets.token_hex(32))")
SECRET_KEY=your-secret-key-here-min-32-chars
JWT_SECRET_KEY=your-jwt-secret-key-here-min-32-chars
ENCRYPTION_KEY=your-encryption-key-here

# JWT Configuration
JWT_ACCESS_TOKEN_EXPIRES=900
JWT_REFRESH_TOKEN_EXPIRES=604800

# Redis
REDIS_URL=redis://localhost:6379/0

# External Services (optional)
OPENAI_API_KEY=
TELEGRAM_BOT_TOKEN=
```

## 3.2 Implement MFA

### Step 1: Install dependencies

```bash
pip install pyotp qrcode[pil]
```

### Step 2: Create MFA models

```python
# backend/src/models/mfa.py

from datetime import datetime
from src.database import db
import pyotp

class MFADevice(db.Model):
    """Multi-Factor Authentication device for users."""
    
    __tablename__ = 'mfa_devices'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    secret = db.Column(db.String(32), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', backref='mfa_devices')
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.secret = pyotp.random_base32()
    
    def get_totp(self):
        """Get TOTP object for this device."""
        return pyotp.TOTP(self.secret)
    
    def verify_token(self, token: str) -> bool:
        """Verify a TOTP token."""
        totp = self.get_totp()
        return totp.verify(token)
    
    def get_provisioning_uri(self, email: str) -> str:
        """Get provisioning URI for QR code."""
        totp = self.get_totp()
        return totp.provisioning_uri(
            name=email,
            issuer_name='Gaara ERP'
        )
```

### Step 3: Create MFA routes

```python
# backend/src/routes/mfa.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import qrcode
import io
import base64

from src.models.mfa import MFADevice
from src.models.user import User
from src.database import db

mfa_bp = Blueprint('mfa', __name__, url_prefix='/api/auth/mfa')

@mfa_bp.route('/setup', methods=['POST'])
@jwt_required()
def setup_mfa():
    """
    Setup MFA for current user.
    Returns QR code for authenticator app.
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Check if MFA already exists
    existing = MFADevice.query.filter_by(
        user_id=user_id, 
        is_active=True
    ).first()
    
    if existing and existing.is_verified:
        return jsonify({
            'success': False,
            'message': 'MFA already configured'
        }), 400
    
    # Create new MFA device
    device = MFADevice(user_id=user_id)
    db.session.add(device)
    db.session.commit()
    
    # Generate QR code
    uri = device.get_provisioning_uri(user.email)
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return jsonify({
        'success': True,
        'data': {
            'qr_code': f'data:image/png;base64,{qr_base64}',
            'secret': device.secret,  # For manual entry
            'device_id': device.id
        }
    })

@mfa_bp.route('/verify', methods=['POST'])
@jwt_required()
def verify_mfa():
    """Verify MFA token and activate device."""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    token = data.get('token')
    device_id = data.get('device_id')
    
    if not token or not device_id:
        return jsonify({
            'success': False,
            'message': 'Token and device_id required'
        }), 400
    
    device = MFADevice.query.filter_by(
        id=device_id,
        user_id=user_id,
        is_active=True
    ).first()
    
    if not device:
        return jsonify({
            'success': False,
            'message': 'MFA device not found'
        }), 404
    
    if device.verify_token(token):
        device.is_verified = True
        device.verified_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'MFA enabled successfully'
        })
    
    return jsonify({
        'success': False,
        'message': 'Invalid token'
    }), 400

@mfa_bp.route('/disable', methods=['POST'])
@jwt_required()
def disable_mfa():
    """Disable MFA for current user."""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    token = data.get('token')
    
    device = MFADevice.query.filter_by(
        user_id=user_id,
        is_active=True,
        is_verified=True
    ).first()
    
    if not device:
        return jsonify({
            'success': False,
            'message': 'MFA not enabled'
        }), 400
    
    if device.verify_token(token):
        device.is_active = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'MFA disabled successfully'
        })
    
    return jsonify({
        'success': False,
        'message': 'Invalid token'
    }), 400
```

## 3.3 Implement Rate Limiting

```python
# backend/src/middleware/rate_limit.py

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["60 per minute"],
    storage_uri="redis://localhost:6379/1"
)

# Usage in routes:
# @limiter.limit("5 per minute")
# def login():
#     ...
```

---

# 👥 4. HR MODULE IMPLEMENTATION {#hr-module}

## 4.1 Directory Structure

```bash
# Create HR module structure
mkdir -p backend/src/modules/hr/{models,views,serializers,services,tests}

# Create files
touch backend/src/modules/hr/__init__.py
touch backend/src/modules/hr/models/__init__.py
touch backend/src/modules/hr/models/employee.py
touch backend/src/modules/hr/models/department.py
touch backend/src/modules/hr/models/attendance.py
touch backend/src/modules/hr/models/leave.py
touch backend/src/modules/hr/models/payroll.py
touch backend/src/modules/hr/views/__init__.py
touch backend/src/modules/hr/views/employee_views.py
touch backend/src/modules/hr/serializers/__init__.py
touch backend/src/modules/hr/serializers/employee_serializer.py
touch backend/src/modules/hr/services/__init__.py
touch backend/src/modules/hr/services/payroll_service.py
touch backend/src/modules/hr/urls.py
touch backend/src/modules/hr/permissions.py
```

## 4.2 Employee Model

```python
# backend/src/modules/hr/models/employee.py

"""
نموذج الموظف
Employee Model - Core HR entity
"""

from datetime import date, datetime
from decimal import Decimal
from src.database import db
from src.models.base import TimeStampedModel, TenantModel

class Employee(TimeStampedModel, TenantModel):
    """
    الموظف - يمثل موظفاً في المؤسسة
    
    Employee - Represents an employee in the organization.
    Links to User for authentication, Department for org structure.
    """
    
    __tablename__ = 'hr_employees'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Link to User (for login)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Personal Information
    employee_number = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    arabic_name = db.Column(db.String(200), nullable=True)
    national_id = db.Column(db.String(20), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)  # male, female
    marital_status = db.Column(db.String(20), nullable=True)
    nationality = db.Column(db.String(50), nullable=True)
    
    # Contact Information
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    mobile = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    
    # Employment Information
    department_id = db.Column(db.Integer, db.ForeignKey('hr_departments.id'))
    position_id = db.Column(db.Integer, db.ForeignKey('hr_positions.id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('hr_employees.id'))
    hire_date = db.Column(db.Date, nullable=False, default=date.today)
    termination_date = db.Column(db.Date, nullable=True)
    employment_type = db.Column(db.String(20), default='full_time')
    # full_time, part_time, contract, intern
    
    # Compensation
    base_salary = db.Column(db.Numeric(12, 2), default=Decimal('0.00'))
    currency = db.Column(db.String(3), default='EGP')
    
    # Status
    status = db.Column(db.String(20), default='active')
    # active, on_leave, suspended, terminated
    
    # Relationships
    user = db.relationship('User', backref='employee_profile')
    department = db.relationship('Department', backref='employees')
    position = db.relationship('Position', backref='employees')
    manager = db.relationship('Employee', remote_side=[id], backref='subordinates')
    
    class Meta:
        verbose_name = 'موظف'
        verbose_name_plural = 'الموظفين'
    
    def __repr__(self):
        return f'<Employee {self.employee_number}: {self.full_name}>'
    
    @property
    def full_name(self):
        """Get full name in English."""
        return f'{self.first_name} {self.last_name}'
    
    @property
    def full_name_ar(self):
        """Get full name in Arabic."""
        return self.arabic_name or self.full_name
    
    @property
    def years_of_service(self):
        """Calculate years of service."""
        end_date = self.termination_date or date.today()
        delta = end_date - self.hire_date
        return delta.days // 365
    
    def to_dict(self):
        """Serialize employee to dictionary."""
        return {
            'id': self.id,
            'employee_number': self.employee_number,
            'full_name': self.full_name,
            'full_name_ar': self.full_name_ar,
            'email': self.email,
            'phone': self.phone,
            'department': self.department.name if self.department else None,
            'position': self.position.title if self.position else None,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'status': self.status,
            'years_of_service': self.years_of_service,
        }
```

## 4.3 Department Model

```python
# backend/src/modules/hr/models/department.py

"""
نموذج القسم
Department Model - Organizational structure
"""

from src.database import db
from src.models.base import TimeStampedModel, TenantModel

class Department(TimeStampedModel, TenantModel):
    """
    القسم - يمثل قسماً في الهيكل التنظيمي
    
    Department - Represents a department in org structure.
    Supports hierarchical structure with parent department.
    """
    
    __tablename__ = 'hr_departments'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    name_ar = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    
    # Hierarchy
    parent_id = db.Column(db.Integer, db.ForeignKey('hr_departments.id'))
    parent = db.relationship('Department', remote_side=[id], backref='children')
    
    # Manager
    manager_id = db.Column(db.Integer, db.ForeignKey('hr_employees.id'))
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Department {self.code}: {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'name_ar': self.name_ar,
            'parent_id': self.parent_id,
            'manager_id': self.manager_id,
            'employee_count': len(self.employees),
            'is_active': self.is_active,
        }
```

## 4.4 Employee ViewSet

```python
# backend/src/modules/hr/views/employee_views.py

"""
عروض الموظفين
Employee Views - API endpoints for employee management
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import or_

from src.database import db
from src.modules.hr.models.employee import Employee
from src.modules.hr.serializers.employee_serializer import (
    EmployeeSerializer,
    EmployeeCreateSerializer
)
from src.decorators import require_permission

hr_bp = Blueprint('hr', __name__, url_prefix='/api/hr')

@hr_bp.route('/employees', methods=['GET'])
@jwt_required()
@require_permission('HR_READ')
def list_employees():
    """
    قائمة الموظفين
    List all employees with filtering and pagination.
    
    Query params:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20)
    - search: Search by name, email, employee_number
    - department_id: Filter by department
    - status: Filter by status
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    department_id = request.args.get('department_id', type=int)
    status = request.args.get('status', '')
    
    query = Employee.query
    
    # Search filter
    if search:
        query = query.filter(or_(
            Employee.first_name.ilike(f'%{search}%'),
            Employee.last_name.ilike(f'%{search}%'),
            Employee.email.ilike(f'%{search}%'),
            Employee.employee_number.ilike(f'%{search}%'),
        ))
    
    # Department filter
    if department_id:
        query = query.filter(Employee.department_id == department_id)
    
    # Status filter
    if status:
        query = query.filter(Employee.status == status)
    
    # Pagination
    pagination = query.order_by(Employee.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': {
            'items': [emp.to_dict() for emp in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages,
        }
    })

@hr_bp.route('/employees', methods=['POST'])
@jwt_required()
@require_permission('HR_CREATE')
def create_employee():
    """
    إنشاء موظف جديد
    Create a new employee.
    """
    data = request.get_json()
    
    # Validate with serializer
    serializer = EmployeeCreateSerializer()
    errors = serializer.validate(data)
    if errors:
        return jsonify({
            'success': False,
            'errors': errors
        }), 400
    
    # Check for duplicate employee number
    existing = Employee.query.filter_by(
        employee_number=data['employee_number']
    ).first()
    if existing:
        return jsonify({
            'success': False,
            'message': 'Employee number already exists'
        }), 409
    
    # Create employee
    employee = Employee(
        employee_number=data['employee_number'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        arabic_name=data.get('arabic_name'),
        national_id=data['national_id'],
        email=data['email'],
        phone=data.get('phone'),
        department_id=data.get('department_id'),
        position_id=data.get('position_id'),
        hire_date=data.get('hire_date'),
        base_salary=data.get('base_salary', 0),
    )
    
    db.session.add(employee)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': employee.to_dict(),
        'message': 'تم إنشاء الموظف بنجاح'
    }), 201

@hr_bp.route('/employees/<int:id>', methods=['GET'])
@jwt_required()
@require_permission('HR_READ')
def get_employee(id):
    """
    عرض تفاصيل موظف
    Get employee details by ID.
    """
    employee = Employee.query.get_or_404(id)
    
    return jsonify({
        'success': True,
        'data': employee.to_dict()
    })

@hr_bp.route('/employees/<int:id>', methods=['PUT'])
@jwt_required()
@require_permission('HR_UPDATE')
def update_employee(id):
    """
    تحديث بيانات موظف
    Update employee data.
    """
    employee = Employee.query.get_or_404(id)
    data = request.get_json()
    
    # Update fields
    for field in ['first_name', 'last_name', 'arabic_name', 'email', 
                  'phone', 'department_id', 'position_id', 'base_salary', 'status']:
        if field in data:
            setattr(employee, field, data[field])
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': employee.to_dict(),
        'message': 'تم تحديث بيانات الموظف بنجاح'
    })

@hr_bp.route('/employees/<int:id>', methods=['DELETE'])
@jwt_required()
@require_permission('HR_DELETE')
def delete_employee(id):
    """
    حذف موظف
    Delete (soft) employee.
    """
    employee = Employee.query.get_or_404(id)
    
    # Soft delete - just change status
    employee.status = 'terminated'
    employee.termination_date = date.today()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'تم حذف الموظف بنجاح'
    })

# Attendance endpoints
@hr_bp.route('/attendance/check-in', methods=['POST'])
@jwt_required()
def check_in():
    """تسجيل حضور - Check in."""
    # Implementation here
    pass

@hr_bp.route('/attendance/check-out', methods=['POST'])
@jwt_required()
def check_out():
    """تسجيل انصراف - Check out."""
    # Implementation here
    pass
```

## 4.5 HR Frontend Components

```jsx
// frontend/src/modules/hr/components/EmployeeList.jsx

import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { 
  Table, 
  Button, 
  Input, 
  Select, 
  Badge,
  Pagination 
} from '@/components/ui';
import { hrApi } from '../services/hrApi';
import { useNavigate } from 'react-router-dom';

/**
 * قائمة الموظفين
 * Employee List - Displays all employees with filtering and search
 */
export function EmployeeList() {
  const navigate = useNavigate();
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('');
  
  const { data, isLoading, error } = useQuery({
    queryKey: ['employees', { page, search, status }],
    queryFn: () => hrApi.getEmployees({ page, search, status }),
  });
  
  const columns = [
    { key: 'employee_number', title: 'رقم الموظف', titleEn: 'Employee #' },
    { key: 'full_name_ar', title: 'الاسم', titleEn: 'Name' },
    { key: 'department', title: 'القسم', titleEn: 'Department' },
    { key: 'position', title: 'المنصب', titleEn: 'Position' },
    { 
      key: 'status', 
      title: 'الحالة', 
      titleEn: 'Status',
      render: (value) => (
        <Badge variant={value === 'active' ? 'success' : 'warning'}>
          {value === 'active' ? 'نشط' : value}
        </Badge>
      )
    },
    {
      key: 'actions',
      title: 'الإجراءات',
      render: (_, row) => (
        <div className="flex gap-2">
          <Button size="sm" onClick={() => navigate(`/hr/employees/${row.id}`)}>
            عرض
          </Button>
          <Button size="sm" variant="outline" onClick={() => navigate(`/hr/employees/${row.id}/edit`)}>
            تعديل
          </Button>
        </div>
      )
    }
  ];
  
  if (isLoading) return <div>جاري التحميل...</div>;
  if (error) return <div>حدث خطأ: {error.message}</div>;
  
  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">إدارة الموظفين</h1>
        <Button onClick={() => navigate('/hr/employees/new')}>
          + إضافة موظف جديد
        </Button>
      </div>
      
      {/* Filters */}
      <div className="flex gap-4">
        <Input
          placeholder="بحث بالاسم أو الرقم..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-64"
        />
        <Select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          options={[
            { value: '', label: 'جميع الحالات' },
            { value: 'active', label: 'نشط' },
            { value: 'on_leave', label: 'في إجازة' },
            { value: 'terminated', label: 'منتهي' },
          ]}
        />
      </div>
      
      {/* Table */}
      <Table
        columns={columns}
        data={data?.data?.items || []}
        onRowClick={(row) => navigate(`/hr/employees/${row.id}`)}
      />
      
      {/* Pagination */}
      <Pagination
        currentPage={page}
        totalPages={data?.data?.pages || 1}
        onPageChange={setPage}
      />
    </div>
  );
}
```

---

# 🎨 5. DESIGN SYSTEM IMPLEMENTATION {#design-system}

## 5.1 Design Tokens

```javascript
// frontend/src/design-system/tokens/index.js

export const tokens = {
  colors: {
    // Brand - Gaara Green
    primary: {
      50: '#e8f5e9',
      100: '#c8e6c9',
      200: '#a5d6a7',
      300: '#81c784',
      400: '#66bb6a',
      500: '#4caf50',  // Main
      600: '#43a047',
      700: '#388e3c',
      800: '#2e7d32',
      900: '#1b5e20',
    },
    
    // Secondary - Blue
    secondary: {
      500: '#2196f3',
      600: '#1e88e5',
      700: '#1976d2',
    },
    
    // Neutral
    gray: {
      50: '#fafafa',
      100: '#f5f5f5',
      200: '#eeeeee',
      300: '#e0e0e0',
      400: '#bdbdbd',
      500: '#9e9e9e',
      600: '#757575',
      700: '#616161',
      800: '#424242',
      900: '#212121',
    },
    
    // Semantic
    success: '#4caf50',
    warning: '#ff9800',
    error: '#f44336',
    info: '#2196f3',
  },
  
  typography: {
    fontFamily: {
      arabic: "'Cairo', 'Noto Sans Arabic', sans-serif",
      english: "'Inter', 'Roboto', sans-serif",
    },
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
      '3xl': '2rem',
    },
  },
  
  spacing: {
    0: '0',
    1: '0.25rem',
    2: '0.5rem',
    3: '0.75rem',
    4: '1rem',
    5: '1.25rem',
    6: '1.5rem',
    8: '2rem',
    10: '2.5rem',
    12: '3rem',
  },
  
  borderRadius: {
    none: '0',
    sm: '0.25rem',
    md: '0.375rem',
    lg: '0.5rem',
    xl: '0.75rem',
    full: '9999px',
  },
};
```

## 5.2 Button Component

```jsx
// frontend/src/design-system/components/Button.jsx

import React from 'react';
import { cva } from 'class-variance-authority';
import { cn } from '@/utils/cn';

const buttonVariants = cva(
  // Base styles
  'inline-flex items-center justify-center rounded-md font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none',
  {
    variants: {
      variant: {
        primary: 'bg-primary-500 text-white hover:bg-primary-600 focus:ring-primary-500',
        secondary: 'bg-secondary-500 text-white hover:bg-secondary-600 focus:ring-secondary-500',
        outline: 'border border-gray-300 bg-transparent hover:bg-gray-50 focus:ring-gray-500',
        ghost: 'bg-transparent hover:bg-gray-100 focus:ring-gray-500',
        danger: 'bg-error text-white hover:bg-red-700 focus:ring-red-500',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4 text-base',
        lg: 'h-12 px-6 text-lg',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
);

export function Button({
  children,
  variant,
  size,
  className,
  isLoading,
  leftIcon,
  rightIcon,
  ...props
}) {
  return (
    <button
      className={cn(buttonVariants({ variant, size }), className)}
      disabled={isLoading}
      {...props}
    >
      {isLoading ? (
        <span className="animate-spin mr-2">⟳</span>
      ) : leftIcon ? (
        <span className="mr-2">{leftIcon}</span>
      ) : null}
      
      {children}
      
      {rightIcon && <span className="ml-2">{rightIcon}</span>}
    </button>
  );
}
```

---

# 🧪 6. TESTING IMPLEMENTATION {#testing}

## 6.1 Backend Unit Tests

```python
# backend/tests/modules/hr/test_employee_model.py

"""
اختبارات نموذج الموظف
Employee Model Tests
"""

import pytest
from datetime import date
from decimal import Decimal

from src.modules.hr.models.employee import Employee
from src.modules.hr.models.department import Department


class TestEmployeeModel:
    """Test cases for Employee model."""
    
    def test_create_employee(self, db_session):
        """Test creating a new employee."""
        employee = Employee(
            employee_number='EMP001',
            first_name='Ahmed',
            last_name='Mohamed',
            arabic_name='أحمد محمد',
            national_id='12345678901234',
            email='ahmed@example.com',
            hire_date=date(2024, 1, 1),
        )
        
        db_session.add(employee)
        db_session.commit()
        
        assert employee.id is not None
        assert employee.employee_number == 'EMP001'
        assert employee.full_name == 'Ahmed Mohamed'
        assert employee.status == 'active'
    
    def test_full_name_property(self):
        """Test full name property."""
        employee = Employee(
            employee_number='EMP002',
            first_name='Sara',
            last_name='Ali',
            national_id='98765432109876',
            email='sara@example.com',
        )
        
        assert employee.full_name == 'Sara Ali'
    
    def test_years_of_service(self):
        """Test years of service calculation."""
        employee = Employee(
            employee_number='EMP003',
            first_name='Test',
            last_name='User',
            national_id='11111111111111',
            email='test@example.com',
            hire_date=date(2020, 1, 1),
        )
        
        # Assuming current date is 2026
        assert employee.years_of_service >= 5
    
    def test_employee_with_department(self, db_session):
        """Test employee-department relationship."""
        department = Department(
            code='IT',
            name='Information Technology',
            name_ar='تقنية المعلومات',
        )
        db_session.add(department)
        db_session.flush()
        
        employee = Employee(
            employee_number='EMP004',
            first_name='Developer',
            last_name='One',
            national_id='22222222222222',
            email='dev@example.com',
            department_id=department.id,
        )
        db_session.add(employee)
        db_session.commit()
        
        assert employee.department.name == 'Information Technology'
        assert employee in department.employees
    
    def test_to_dict(self, db_session):
        """Test serialization to dictionary."""
        employee = Employee(
            employee_number='EMP005',
            first_name='Test',
            last_name='Dict',
            national_id='33333333333333',
            email='dict@example.com',
            hire_date=date(2024, 6, 1),
        )
        db_session.add(employee)
        db_session.commit()
        
        data = employee.to_dict()
        
        assert data['employee_number'] == 'EMP005'
        assert data['full_name'] == 'Test Dict'
        assert data['email'] == 'dict@example.com'
        assert 'id' in data
```

## 6.2 API Integration Tests

```python
# backend/tests/api/test_hr_api.py

"""
اختبارات API الموارد البشرية
HR API Integration Tests
"""

import pytest
from flask import url_for


class TestHRAPI:
    """Integration tests for HR API endpoints."""
    
    def test_list_employees(self, client, auth_headers):
        """Test GET /api/hr/employees."""
        response = client.get(
            '/api/hr/employees',
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'items' in data['data']
        assert 'total' in data['data']
    
    def test_create_employee(self, client, auth_headers):
        """Test POST /api/hr/employees."""
        payload = {
            'employee_number': 'EMP100',
            'first_name': 'New',
            'last_name': 'Employee',
            'national_id': '44444444444444',
            'email': 'new.employee@example.com',
        }
        
        response = client.post(
            '/api/hr/employees',
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['employee_number'] == 'EMP100'
    
    def test_create_employee_validation_error(self, client, auth_headers):
        """Test validation errors on create."""
        payload = {
            'first_name': 'Missing',
            # Missing required fields
        }
        
        response = client.post(
            '/api/hr/employees',
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'errors' in data
    
    def test_get_employee(self, client, auth_headers, sample_employee):
        """Test GET /api/hr/employees/{id}."""
        response = client.get(
            f'/api/hr/employees/{sample_employee.id}',
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['data']['id'] == sample_employee.id
    
    def test_update_employee(self, client, auth_headers, sample_employee):
        """Test PUT /api/hr/employees/{id}."""
        payload = {
            'first_name': 'Updated',
            'status': 'on_leave',
        }
        
        response = client.put(
            f'/api/hr/employees/{sample_employee.id}',
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['data']['first_name'] == 'Updated'
    
    def test_unauthorized_access(self, client):
        """Test access without authentication."""
        response = client.get('/api/hr/employees')
        
        assert response.status_code == 401


# Fixtures
@pytest.fixture
def auth_headers(client):
    """Get authentication headers."""
    response = client.post('/api/auth/login', json={
        'email': 'admin@example.com',
        'password': 'admin123',
    })
    token = response.get_json()['data']['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def sample_employee(db_session):
    """Create a sample employee for testing."""
    from src.modules.hr.models.employee import Employee
    
    employee = Employee(
        employee_number='TEST001',
        first_name='Test',
        last_name='Employee',
        national_id='99999999999999',
        email='test.emp@example.com',
    )
    db_session.add(employee)
    db_session.commit()
    return employee
```

## 6.3 E2E Tests with Playwright

```typescript
// frontend/e2e/hr/employees.spec.ts

import { test, expect } from '@playwright/test';

test.describe('HR Module - Employees', () => {
  
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login');
    await page.fill('[name="email"]', 'admin@example.com');
    await page.fill('[name="password"]', 'admin123');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');
  });
  
  test('should display employee list', async ({ page }) => {
    await page.goto('/hr/employees');
    
    // Check page title
    await expect(page.locator('h1')).toContainText('إدارة الموظفين');
    
    // Check table is visible
    await expect(page.locator('table')).toBeVisible();
    
    // Check add button exists
    await expect(page.locator('button:has-text("إضافة موظف")')).toBeVisible();
  });
  
  test('should search employees', async ({ page }) => {
    await page.goto('/hr/employees');
    
    // Type in search box
    await page.fill('input[placeholder*="بحث"]', 'Ahmed');
    
    // Wait for results
    await page.waitForTimeout(500);
    
    // Check results contain search term
    const rows = page.locator('table tbody tr');
    const count = await rows.count();
    
    for (let i = 0; i < count; i++) {
      const text = await rows.nth(i).textContent();
      expect(text?.toLowerCase()).toContain('ahmed');
    }
  });
  
  test('should create new employee', async ({ page }) => {
    await page.goto('/hr/employees/new');
    
    // Fill form
    await page.fill('[name="employee_number"]', 'EMP999');
    await page.fill('[name="first_name"]', 'Playwright');
    await page.fill('[name="last_name"]', 'Test');
    await page.fill('[name="national_id"]', '88888888888888');
    await page.fill('[name="email"]', 'playwright@test.com');
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Check success message
    await expect(page.locator('.toast-success')).toBeVisible();
    
    // Check redirect to list
    await expect(page).toHaveURL('/hr/employees');
  });
  
  test('should view employee details', async ({ page }) => {
    await page.goto('/hr/employees');
    
    // Click first employee row
    await page.locator('table tbody tr').first().click();
    
    // Check detail page loads
    await expect(page.locator('h1')).toContainText('تفاصيل الموظف');
    
    // Check employee info is displayed
    await expect(page.locator('[data-testid="employee-number"]')).toBeVisible();
  });
  
  test('should be RTL layout', async ({ page }) => {
    await page.goto('/hr/employees');
    
    // Check HTML dir attribute
    const dir = await page.getAttribute('html', 'dir');
    expect(dir).toBe('rtl');
    
    // Check Arabic font is applied
    const fontFamily = await page.locator('body').evaluate(
      el => getComputedStyle(el).fontFamily
    );
    expect(fontFamily).toContain('Cairo');
  });
});
```

---

# 📝 7. CODE TEMPLATES {#templates}

## 7.1 Model Template

```python
# templates/model_template.py

"""
نموذج [اسم النموذج]
[Model Name] Model

الوصف: [وصف بالعربية]
Description: [English description]
"""

from datetime import datetime
from decimal import Decimal
from src.database import db
from src.models.base import TimeStampedModel, TenantModel


class ModelName(TimeStampedModel, TenantModel):
    """
    [اسم النموذج بالعربية]
    
    [English description of what this model represents]
    
    Attributes:
        field1: Description
        field2: Description
    """
    
    __tablename__ = 'table_name'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Fields
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    # related = db.relationship('OtherModel', backref='this_model')
    
    class Meta:
        verbose_name = 'اسم النموذج'
        verbose_name_plural = 'اسماء النماذج'
        ordering = ['-created_at']
    
    def __repr__(self):
        return f'<ModelName {self.id}: {self.name}>'
    
    def to_dict(self):
        """Serialize to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
```

## 7.2 ViewSet Template

```python
# templates/viewset_template.py

"""
عروض [اسم المديول]
[Module Name] Views
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.database import db
from src.decorators import require_permission

module_bp = Blueprint('module', __name__, url_prefix='/api/module')


@module_bp.route('/items', methods=['GET'])
@jwt_required()
@require_permission('MODULE_READ')
def list_items():
    """
    قائمة العناصر
    List all items with pagination.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Query logic here
    
    return jsonify({
        'success': True,
        'data': {
            'items': [],
            'total': 0,
            'page': page,
            'per_page': per_page,
        }
    })


@module_bp.route('/items', methods=['POST'])
@jwt_required()
@require_permission('MODULE_CREATE')
def create_item():
    """
    إنشاء عنصر جديد
    Create a new item.
    """
    data = request.get_json()
    
    # Validation and creation logic here
    
    return jsonify({
        'success': True,
        'data': {},
        'message': 'تم الإنشاء بنجاح'
    }), 201


@module_bp.route('/items/<int:id>', methods=['GET'])
@jwt_required()
@require_permission('MODULE_READ')
def get_item(id):
    """Get item by ID."""
    # Get logic here
    
    return jsonify({
        'success': True,
        'data': {}
    })


@module_bp.route('/items/<int:id>', methods=['PUT'])
@jwt_required()
@require_permission('MODULE_UPDATE')
def update_item(id):
    """Update item."""
    data = request.get_json()
    
    # Update logic here
    
    return jsonify({
        'success': True,
        'data': {},
        'message': 'تم التحديث بنجاح'
    })


@module_bp.route('/items/<int:id>', methods=['DELETE'])
@jwt_required()
@require_permission('MODULE_DELETE')
def delete_item(id):
    """Delete item."""
    # Delete logic here
    
    return jsonify({
        'success': True,
        'message': 'تم الحذف بنجاح'
    })
```

## 7.3 React Component Template

```jsx
// templates/ComponentTemplate.jsx

import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { Button, Table, Input } from '@/components/ui';
import { moduleApi } from '../services/moduleApi';

/**
 * [اسم المكون]
 * [Component Name]
 * 
 * @description [وصف المكون]
 */
export function ComponentName() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  
  // Fetch data
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['module-items', { page, search }],
    queryFn: () => moduleApi.getItems({ page, search }),
  });
  
  // Mutations
  const createMutation = useMutation({
    mutationFn: moduleApi.createItem,
    onSuccess: () => {
      refetch();
      // Show success toast
    },
  });
  
  if (isLoading) {
    return <div className="animate-pulse">جاري التحميل...</div>;
  }
  
  if (error) {
    return <div className="text-error">حدث خطأ: {error.message}</div>;
  }
  
  return (
    <div className="space-y-4" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">عنوان الصفحة</h1>
        <Button onClick={() => createMutation.mutate({})}>
          + إضافة جديد
        </Button>
      </div>
      
      {/* Search */}
      <Input
        placeholder="بحث..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="w-64"
      />
      
      {/* Content */}
      <Table
        columns={[
          { key: 'name', title: 'الاسم' },
          { key: 'status', title: 'الحالة' },
        ]}
        data={data?.data?.items || []}
      />
    </div>
  );
}
```

---

# ✅ IMPLEMENTATION CHECKLIST

```
Week 1:
□ Fix all F821 errors (68)
□ Fix all E9 errors (24)
□ Remove hardcoded secrets
□ Fix all F811 errors (62)
□ Configure pre-commit hooks

Week 2-3:
□ Implement MFA
□ Add rate limiting
□ Standardize JWT TTL
□ Create .env template

Week 4-6:
□ Create HR module models
□ Create HR module API
□ Create HR frontend components
□ Write HR module tests

Week 7-9:
□ Create Contacts module
□ Create Projects module
□ Test all new modules

Week 10-12:
□ Implement Design System
□ Create component library
□ Document in Storybook
```

---

**Implementation Guide Version:** 1.0.0
**Created:** 2026-01-15
**Next Update:** After Week 1 completion

**END OF IMPLEMENTATION GUIDE**
