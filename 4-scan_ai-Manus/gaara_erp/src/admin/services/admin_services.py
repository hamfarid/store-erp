"""
خدمات وحدة الإدارة
يحتوي هذا الملف على خدمات إدارة المستخدمين والشركات والإعدادات وحالة النظام
"""

from typing import List, Dict, Any, Optional, Union, Tuple
from datetime import datetime, date, timedelta
import uuid
import json
import os
import shutil
import logging
import psutil
import bcrypt

from ...core.database.db_manager import DatabaseManager
from ..models.admin_models import (
    User, UserRole, PermissionLevel, Country, Company, Branch,
    SystemLog, SystemSetting, ServerStatus, UserStatistics, BackupInfo
)


class UserService:
    """خدمة إدارة المستخدمين"""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        تهيئة خدمة المستخدمين
        
        المعاملات:
            db_manager: مدير قاعدة البيانات
        """
        self.db_manager = db_manager
    
    def create_user(self, user_data: Dict[str, Any]) -> User:
        """
        إنشاء مستخدم جديد
        
        المعاملات:
            user_data: بيانات المستخدم
            
        العائد:
            كائن المستخدم الجديد
        
        يرفع:
            ValueError: إذا كان اسم المستخدم أو البريد الإلكتروني موجودًا بالفعل
        """
        # التحقق من وجود اسم المستخدم أو البريد الإلكتروني
        if self._is_username_exists(user_data.get('username')):
            raise ValueError(f"اسم المستخدم '{user_data.get('username')}' موجود بالفعل")
        
        if self._is_email_exists(user_data.get('email')):
            raise ValueError(f"البريد الإلكتروني '{user_data.get('email')}' موجود بالفعل")
        
        # تشفير كلمة المرور
        if 'password' in user_data:
            password = user_data.pop('password')
            user_data['password_hash'] = self._hash_password(password)
        
        # إنشاء معرف فريد
        user_data['user_id'] = user_data.get('user_id', str(uuid.uuid4()))
        
        # تعيين تاريخ الإنشاء
        user_data['created_at'] = user_data.get('created_at', datetime.now())
        
        # إنشاء كائن المستخدم
        user = User(**user_data)
        
        # حفظ المستخدم في قاعدة البيانات
        self.db_manager.save_user(user)
        
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """
        الحصول على مستخدم بواسطة المعرف
        
        المعاملات:
            user_id: معرف المستخدم
            
        العائد:
            كائن المستخدم أو None إذا لم يتم العثور عليه
        """
        return self.db_manager.get_user(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        الحصول على مستخدم بواسطة اسم المستخدم
        
        المعاملات:
            username: اسم المستخدم
            
        العائد:
            كائن المستخدم أو None إذا لم يتم العثور عليه
        """
        return self.db_manager.get_user_by_username(username)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        الحصول على مستخدم بواسطة البريد الإلكتروني
        
        المعاملات:
            email: البريد الإلكتروني
            
        العائد:
            كائن المستخدم أو None إذا لم يتم العثور عليه
        """
        return self.db_manager.get_user_by_email(email)
    
    def get_all_users(
        self,
        company_id: Optional[str] = None,
        branch_id: Optional[str] = None,
        country_id: Optional[str] = None,
        role: Optional[Union[UserRole, str]] = None,
        is_active: Optional[bool] = None
    ) -> List[User]:
        """
        الحصول على جميع المستخدمين مع تصفية اختيارية
        
        المعاملات:
            company_id: معرف الشركة (اختياري)
            branch_id: معرف الفرع (اختياري)
            country_id: معرف الدولة (اختياري)
            role: دور المستخدم (اختياري)
            is_active: ما إذا كان المستخدم نشطًا (اختياري)
            
        العائد:
            قائمة بكائنات المستخدمين
        """
        # تحويل الدور إلى كائن UserRole إذا كان سلسلة نصية
        if role and isinstance(role, str):
            role = UserRole(role)
        
        return self.db_manager.get_all_users(company_id, branch_id, country_id, role, is_active)
    
    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Optional[User]:
        """
        تحديث مستخدم
        
        المعاملات:
            user_id: معرف المستخدم
            user_data: بيانات المستخدم المحدثة
            
        العائد:
            كائن المستخدم المحدث أو None إذا لم يتم العثور عليه
        
        يرفع:
            ValueError: إذا كان اسم المستخدم أو البريد الإلكتروني موجودًا بالفعل لمستخدم آخر
        """
        # الحصول على المستخدم الحالي
        user = self.get_user(user_id)
        if not user:
            return None
        
        # التحقق من وجود اسم المستخدم أو البريد الإلكتروني لمستخدم آخر
        if 'username' in user_data and user_data['username'] != user.username:
            if self._is_username_exists(user_data['username']):
                raise ValueError(f"اسم المستخدم '{user_data['username']}' موجود بالفعل")
        
        if 'email' in user_data and user_data['email'] != user.email:
            if self._is_email_exists(user_data['email']):
                raise ValueError(f"البريد الإلكتروني '{user_data['email']}' موجود بالفعل")
        
        # تشفير كلمة المرور إذا تم تغييرها
        if 'password' in user_data:
            password = user_data.pop('password')
            user_data['password_hash'] = self._hash_password(password)
        
        # تحديث بيانات المستخدم
        for key, value in user_data.items():
            if key != 'user_id' and hasattr(user, key):
                setattr(user, key, value)
        
        # حفظ المستخدم في قاعدة البيانات
        self.db_manager.update_user(user)
        
        return user
    
    def delete_user(self, user_id: str) -> bool:
        """
        حذف مستخدم
        
        المعاملات:
            user_id: معرف المستخدم
            
        العائد:
            True إذا تم الحذف بنجاح، False خلاف ذلك
        """
        return self.db_manager.delete_user(user_id)
    
    def authenticate_user(self, username_or_email: str, password: str) -> Optional[User]:
        """
        مصادقة المستخدم
        
        المعاملات:
            username_or_email: اسم المستخدم أو البريد الإلكتروني
            password: كلمة المرور
            
        العائد:
            كائن المستخدم إذا نجحت المصادقة، None خلاف ذلك
        """
        # البحث عن المستخدم بواسطة اسم المستخدم أو البريد الإلكتروني
        user = self.get_user_by_username(username_or_email)
        if not user:
            user = self.get_user_by_email(username_or_email)
        
        if not user or not user.is_active:
            return None
        
        # التحقق من كلمة المرور
        if self._verify_password(password, user.password_hash):
            # تحديث تاريخ آخر تسجيل دخول
            user.last_login = datetime.now()
            self.db_manager.update_user(user)
            return user
        
        return None
    
    def update_user_permissions(self, user_id: str, permissions: Dict[str, Union[PermissionLevel, str]]) -> Optional[User]:
        """
        تحديث صلاحيات المستخدم
        
        المعاملات:
            user_id: معرف المستخدم
            permissions: صلاحيات المستخدم
            
        العائد:
            كائن المستخدم المحدث أو None إذا لم يتم العثور عليه
        """
        # الحصول على المستخدم الحالي
        user = self.get_user(user_id)
        if not user:
            return None
        
        # تحويل الصلاحيات إلى كائنات PermissionLevel إذا كانت سلاسل نصية
        processed_permissions = {}
        for key, value in permissions.items():
            if isinstance(value, str):
                processed_permissions[key] = PermissionLevel(value)
            else:
                processed_permissions[key] = value
        
        # تحديث صلاحيات المستخدم
        user.permissions = processed_permissions
        
        # حفظ المستخدم في قاعدة البيانات
        self.db_manager.update_user(user)
        
        return user
    
    def change_user_password(self, user_id: str, new_password: str) -> Optional[User]:
        """
        تغيير كلمة مرور المستخدم
        
        المعاملات:
            user_id: معرف المستخدم
            new_password: كلمة المرور الجديدة
            
        العائد:
            كائن المستخدم المحدث أو None إذا لم يتم العثور عليه
        """
        # الحصول على المستخدم الحالي
        user = self.get_user(user_id)
        if not user:
            return None
        
        # تشفير كلمة المرور الجديدة
        user.password_hash = self._hash_password(new_password)
        
        # حفظ المستخدم في قاعدة البيانات
        self.db_manager.update_user(user)
        
        return user
    
    def get_user_statistics(self) -> UserStatistics:
        """
        الحصول على إحصائيات المستخدمين
        
        العائد:
            كائن إحصائيات المستخدمين
        """
        # الحصول على جميع المستخدمين
        all_users = self.get_all_users()
        
        # حساب الإحصائيات
        total_users = len(all_users)
        active_users = len([user for user in all_users if user.is_active])
        inactive_users = total_users - active_users
        
        # حساب المستخدمين النشطين حسب الفترة الزمنية
        now = datetime.now()
        daily_active_users = len([user for user in all_users if user.last_login and (now - user.last_login).days < 1])
        weekly_active_users = len([user for user in all_users if user.last_login and (now - user.last_login).days < 7])
        monthly_active_users = len([user for user in all_users if user.last_login and (now - user.last_login).days < 30])
        yearly_active_users = len([user for user in all_users if user.last_login and (now - user.last_login).days < 365])
        
        # حساب المستخدمين الجدد حسب الفترة الزمنية
        new_users_today = len([user for user in all_users if user.created_at and (now - user.created_at).days < 1])
        new_users_this_week = len([user for user in all_users if user.created_at and (now - user.created_at).days < 7])
        new_users_this_month = len([user for user in all_users if user.created_at and (now - user.created_at).days < 30])
        new_users_this_year = len([user for user in all_users if user.created_at and (now - user.created_at).days < 365])
        
        # حساب المستخدمين حسب الدور
        users_by_role = {}
        for user in all_users:
            role = user.role.value if isinstance(user.role, UserRole) else user.role
            users_by_role[role] = users_by_role.get(role, 0) + 1
        
        # حساب المستخدمين حسب الدولة
        users_by_country = {}
        for user in all_users:
            if user.country_id:
                users_by_country[user.country_id] = users_by_country.get(user.country_id, 0) + 1
        
        # حساب المستخدمين حسب الشركة
        users_by_company = {}
        for user in all_users:
            if user.company_id:
                users_by_company[user.company_id] = users_by_company.get(user.company_id, 0) + 1
        
        # إنشاء كائن إحصائيات المستخدمين
        stats = UserStatistics(
            stats_id=str(uuid.uuid4()),
            timestamp=now,
            total_users=total_users,
            active_users=active_users,
            inactive_users=inactive_users,
            daily_active_users=daily_active_users,
            weekly_active_users=weekly_active_users,
            monthly_active_users=monthly_active_users,
            yearly_active_users=yearly_active_users,
            new_users_today=new_users_today,
            new_users_this_week=new_users_this_week,
            new_users_this_month=new_users_this_month,
            new_users_this_year=new_users_this_year,
            users_by_role=users_by_role,
            users_by_country=users_by_country,
            users_by_company=users_by_company
        )
        
        return stats
    
    def _is_username_exists(self, username: str) -> bool:
        """
        التحقق مما إذا كان اسم المستخدم موجودًا
        
        المعاملات:
            username: اسم المستخدم
            
        العائد:
            True إذا كان اسم المستخدم موجودًا، False خلاف ذلك
        """
        return self.get_user_by_username(username) is not None
    
    def _is_email_exists(self, email: str) -> bool:
        """
        التحقق مما إذا كان البريد الإلكتروني موجودًا
        
        المعاملات:
            email: البريد الإلكتروني
            
        العائد:
            True إذا كان البريد الإلكتروني موجودًا، False خلاف ذلك
        """
        return self.get_user_by_email(email) is not None
    
    def _hash_password(self, password: str) -> str:
        """
        تشفير كلمة المرور
        
        المعاملات:
            password: كلمة المرور
            
        العائد:
            كلمة المرور المشفرة
        """
        # تشفير كلمة المرور باستخدام bcrypt
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """
        التحقق من كلمة المرور
        
        المعاملات:
            password: كلمة المرور
            hashed_password: كلمة المرور المشفرة
            
        العائد:
            True إذا كانت كلمة المرور صحيحة، False خلاف ذلك
        """
        # التحقق من كلمة المرور باستخدام bcrypt
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)


class CountryService:
    """خدمة إدارة الدول"""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        تهيئة خدمة الدول
        
        المعاملات:
            db_manager: مدير قاعدة البيانات
        """
        self.db_manager = db_manager
    
    def create_country(self, country_data: Dict[str, Any]) -> Country:
        """
        إنشاء دولة جديدة
        
        المعاملات:
            country_data: بيانات الدولة
            
        العائد:
            كائن الدولة الجديدة
        
        يرفع:
            ValueError: إذا كان رمز الدولة موجودًا بالفعل
        """
        # التحقق من وجود رمز الدولة
        if self._is_country_code_exists(country_data.get('code')):
            raise ValueError(f"رمز الدولة '{country_data.get('code')}' موجود بالفعل")
        
        # إنشاء معرف فريد
        country_data['country_id'] = country_data.get('country_id', str(uuid.uuid4()))
        
        # إنشاء كائن الدولة
        country = Country(**country_data)
        
        # حفظ الدولة في قاعدة البيانات
        self.db_manager.save_country(country)
        
        return country
    
    def get_country(self, country_id: str) -> Optional[Country]:
        """
        الحصول على دولة بواسطة المعرف
        
        المعاملات:
            country_id: معرف الدولة
            
        العائد:
            كائن الدولة أو None إذا لم يتم العثور عليها
        """
        return self.db_manager.get_country(country_id)
    
    def get_country_by_code(self, code: str) -> Optional[Country]:
        """
        الحصول على دولة بواسطة الرمز
        
        المعاملات:
            code: رمز الدولة
            
        العائد:
            كائن الدولة أو None إذا لم يتم العثور عليها
        """
        return self.db_manager.get_country_by_code(code)
    
    def get_all_countries(self, is_active: Optional[bool] = None) -> List[Country]:
        """
        الحصول على جميع الدول مع تصفية اختيارية
        
        المعاملات:
            is_active: ما إذا كانت الدولة نشطة (اختياري)
            
        العائد:
            قائمة بكائنات الدول
        """
        return self.db_manager.get_all_countries(is_active)
    
    def update_country(self, country_id: str, country_data: Dict[str, Any]) -> Optional[Country]:
        """
        تحديث دولة
        
        المعاملات:
            country_id: معرف الدولة
            country_data: بيانات الدولة المحدثة
            
        العائد:
            كائن الدولة المحدثة أو None إذا لم يتم العثور عليها
        
        يرفع:
            ValueError: إذا كان رمز الدولة موجودًا بالفعل لدولة أخرى
        """
        # الحصول على الدولة الحالية
        country = self.get_country(country_id)
        if not country:
            return None
        
        # التحقق من وجود رمز الدولة لدولة أخرى
        if 'code' in country_data and country_data['code'] != country.code:
            if self._is_country_code_exists(country_data['code']):
                raise ValueError(f"رمز الدولة '{country_data['code']}' موجود بالفعل")
        
        # تحديث بيانات الدولة
        for key, value in country_data.items():
            if key != 'country_id' and hasattr(country, key):
                setattr(country, key, value)
        
        # حفظ الدولة في قاعدة البيانات
        self.db_manager.update_country(country)
        
        return country
    
    def delete_country(self, country_id: str) -> bool:
        """
        حذف دولة
        
        المعاملات:
            country_id: معرف الدولة
            
        العائد:
            True إذا تم الحذف بنجاح، False خلاف ذلك
        """
        return self.db_manager.delete_country(country_id)
    
    def _is_country_code_exists(self, code: str) -> bool:
        """
        التحقق مما إذا كان رمز الدولة موجودًا
        
        المعاملات:
            code: رمز الدولة
            
        العائد:
            True إذا كان رمز الدولة موجودًا، False خلاف ذلك
        """
        return self.get_country_by_code(code) is not None


class CompanyService:
    """خدمة إدارة الشركات"""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        تهيئة خدمة الشركات
        
        المعاملات:
            db_manager: مدير قاعدة البيانات
        """
        self.db_manager = db_manager
    
    def create_company(self, company_data: Dict[str, Any]) -> Company:
        """
        إنشاء شركة جديدة
        
        المعاملات:
            company_data: بيانات الشركة
            
        العائد:
            كائن الشركة الجديدة
        
        يرفع:
            ValueError: إذا كان الرقم الضريبي موجودًا بالفعل
        """
        # التحقق من وجود الرقم الضريبي
        tax_number = company_data.get('tax_number')
        if tax_number and self._is_tax_number_exists(tax_number):
            raise ValueError(f"الرقم الضريبي '{tax_number}' موجود بالفعل")
        
        # إنشاء معرف فريد
        company_data['company_id'] = company_data.get('company_id', str(uuid.uuid4()))
        
        # تعيين تاريخ الإنشاء
        company_data['created_at'] = company_data.get('created_at', datetime.now())
        
        # إنشاء كائن الشركة
        company = Company(**company_data)
        
        # حفظ الشركة في قاعدة البيانات
        self.db_manager.save_company(company)
        
        return company
    
    def get_company(self, company_id: str) -> Optional[Company]:
        """
        الحصول على شركة بواسطة المعرف
        
        المعاملات:
            company_id: معرف الشركة
            
        العائد:
            كائن الشركة أو None إذا لم يتم العثور عليها
        """
        return self.db_manager.get_company(company_id)
    
    def get_all_companies(
        self,
        country_id: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[Company]:
        """
        الحصول على جميع الشركات مع تصفية اختيارية
        
        المعاملات:
            country_id: معرف الدولة (اختياري)
            is_active: ما إذا كانت الشركة نشطة (اختياري)
            
        العائد:
            قائمة بكائنات الشركات
        """
        return self.db_manager.get_all_companies(country_id, is_active)
    
    def update_company(self, company_id: str, company_data: Dict[str, Any]) -> Optional[Company]:
        """
        تحديث شركة
        
        المعاملات:
            company_id: معرف الشركة
            company_data: بيانات الشركة المحدثة
            
        العائد:
            كائن الشركة المحدثة أو None إذا لم يتم العثور عليها
        
        يرفع:
            ValueError: إذا كان الرقم الضريبي موجودًا بالفعل لشركة أخرى
        """
        # الحصول على الشركة الحالية
        company = self.get_company(company_id)
        if not company:
            return None
        
        # التحقق من وجود الرقم الضريبي لشركة أخرى
        tax_number = company_data.get('tax_number')
        if tax_number and tax_number != company.tax_number:
            if self._is_tax_number_exists(tax_number):
                raise ValueError(f"الرقم الضريبي '{tax_number}' موجود بالفعل")
        
        # تحديث بيانات الشركة
        for key, value in company_data.items():
            if key != 'company_id' and key != 'created_at' and hasattr(company, key):
                setattr(company, key, value)
        
        # حفظ الشركة في قاعدة البيانات
        self.db_manager.update_company(company)
        
        return company
    
    def delete_company(self, company_id: str) -> bool:
        """
        حذف شركة
        
        المعاملات:
            company_id: معرف الشركة
            
        العائد:
            True إذا تم الحذف بنجاح، False خلاف ذلك
        """
        return self.db_manager.delete_company(company_id)
    
    def create_branch(self, branch_data: Dict[str, Any]) -> Branch:
        """
        إنشاء فرع جديد
        
        المعاملات:
            branch_data: بيانات الفرع
            
        العائد:
            كائن الفرع الجديد
        
        يرفع:
            ValueError: إذا كانت الشركة غير موجودة
        """
        # التحقق من وجود الشركة
        company_id = branch_data.get('company_id')
        if not company_id:
            raise ValueError("معرف الشركة مطلوب")
        
        company = self.get_company(company_id)
        if not company:
            raise ValueError(f"الشركة بالمعرف '{company_id}' غير موجودة")
        
        # إنشاء معرف فريد
        branch_data['branch_id'] = branch_data.get('branch_id', str(uuid.uuid4()))
        
        # تعيين تاريخ الإنشاء
        branch_data['created_at'] = branch_data.get('created_at', datetime.now())
        
        # إنشاء كائن الفرع
        branch = Branch(**branch_data)
        
        # حفظ الفرع في قاعدة البيانات
        self.db_manager.save_branch(branch)
        
        return branch
    
    def get_branch(self, branch_id: str) -> Optional[Branch]:
        """
        الحصول على فرع بواسطة المعرف
        
        المعاملات:
            branch_id: معرف الفرع
            
        العائد:
            كائن الفرع أو None إذا لم يتم العثور عليه
        """
        return self.db_manager.get_branch(branch_id)
    
    def get_all_branches(
        self,
        company_id: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_main_branch: Optional[bool] = None
    ) -> List[Branch]:
        """
        الحصول على جميع الفروع مع تصفية اختيارية
        
        المعاملات:
            company_id: معرف الشركة (اختياري)
            is_active: ما إذا كان الفرع نشطًا (اختياري)
            is_main_branch: ما إذا كان الفرع الرئيسي (اختياري)
            
        العائد:
            قائمة بكائنات الفروع
        """
        return self.db_manager.get_all_branches(company_id, is_active, is_main_branch)
    
    def update_branch(self, branch_id: str, branch_data: Dict[str, Any]) -> Optional[Branch]:
        """
        تحديث فرع
        
        المعاملات:
            branch_id: معرف الفرع
            branch_data: بيانات الفرع المحدثة
            
        العائد:
            كائن الفرع المحدث أو None إذا لم يتم العثور عليه
        """
        # الحصول على الفرع الحالي
        branch = self.get_branch(branch_id)
        if not branch:
            return None
        
        # تحديث بيانات الفرع
        for key, value in branch_data.items():
            if key != 'branch_id' and key != 'created_at' and hasattr(branch, key):
                setattr(branch, key, value)
        
        # حفظ الفرع في قاعدة البيانات
        self.db_manager.update_branch(branch)
        
        return branch
    
    def delete_branch(self, branch_id: str) -> bool:
        """
        حذف فرع
        
        المعاملات:
            branch_id: معرف الفرع
            
        العائد:
            True إذا تم الحذف بنجاح، False خلاف ذلك
        """
        return self.db_manager.delete_branch(branch_id)
    
    def _is_tax_number_exists(self, tax_number: str) -> bool:
        """
        التحقق مما إذا كان الرقم الضريبي موجودًا
        
        المعاملات:
            tax_number: الرقم الضريبي
            
        العائد:
            True إذا كان الرقم الضريبي موجودًا، False خلاف ذلك
        """
        companies = self.get_all_companies()
        return any(company.tax_number == tax_number for company in companies)


class SystemSettingService:
    """خدمة إدارة إعدادات النظام"""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        تهيئة خدمة إعدادات النظام
        
        المعاملات:
            db_manager: مدير قاعدة البيانات
        """
        self.db_manager = db_manager
    
    def create_setting(self, setting_data: Dict[str, Any]) -> SystemSetting:
        """
        إنشاء إعداد جديد
        
        المعاملات:
            setting_data: بيانات الإعداد
            
        العائد:
            كائن الإعداد الجديد
        
        يرفع:
            ValueError: إذا كان مفتاح الإعداد موجودًا بالفعل
        """
        # التحقق من وجود مفتاح الإعداد
        key = setting_data.get('key')
        company_id = setting_data.get('company_id')
        branch_id = setting_data.get('branch_id')
        
        if self._is_setting_key_exists(key, company_id, branch_id):
            scope = "عام" if not company_id else f"للشركة '{company_id}'"
            if branch_id:
                scope += f" والفرع '{branch_id}'"
            raise ValueError(f"مفتاح الإعداد '{key}' موجود بالفعل {scope}")
        
        # إنشاء معرف فريد
        setting_data['setting_id'] = setting_data.get('setting_id', str(uuid.uuid4()))
        
        # تعيين تواريخ الإنشاء والتحديث
        now = datetime.now()
        setting_data['created_at'] = setting_data.get('created_at', now)
        setting_data['updated_at'] = setting_data.get('updated_at', now)
        
        # إنشاء كائن الإعداد
        setting = SystemSetting(**setting_data)
        
        # حفظ الإعداد في قاعدة البيانات
        self.db_manager.save_system_setting(setting)
        
        return setting
    
    def get_setting(self, setting_id: str) -> Optional[SystemSetting]:
        """
        الحصول على إعداد بواسطة المعرف
        
        المعاملات:
            setting_id: معرف الإعداد
            
        العائد:
            كائن الإعداد أو None إذا لم يتم العثور عليه
        """
        return self.db_manager.get_system_setting(setting_id)
    
    def get_setting_by_key(
        self,
        key: str,
        company_id: Optional[str] = None,
        branch_id: Optional[str] = None
    ) -> Optional[SystemSetting]:
        """
        الحصول على إعداد بواسطة المفتاح
        
        المعاملات:
            key: مفتاح الإعداد
            company_id: معرف الشركة (اختياري)
            branch_id: معرف الفرع (اختياري)
            
        العائد:
            كائن الإعداد أو None إذا لم يتم العثور عليه
        """
        return self.db_manager.get_system_setting_by_key(key, company_id, branch_id)
    
    def get_all_settings(
        self,
        category: Optional[str] = None,
        company_id: Optional[str] = None,
        branch_id: Optional[str] = None,
        is_global: Optional[bool] = None
    ) -> List[SystemSetting]:
        """
        الحصول على جميع الإعدادات مع تصفية اختيارية
        
        المعاملات:
            category: فئة الإعداد (اختياري)
            company_id: معرف الشركة (اختياري)
            branch_id: معرف الفرع (اختياري)
            is_global: ما إذا كان الإعداد عامًا (اختياري)
            
        العائد:
            قائمة بكائنات الإعدادات
        """
        return self.db_manager.get_all_system_settings(category, company_id, branch_id, is_global)
    
    def update_setting(self, setting_id: str, setting_data: Dict[str, Any]) -> Optional[SystemSetting]:
        """
        تحديث إعداد
        
        المعاملات:
            setting_id: معرف الإعداد
            setting_data: بيانات الإعداد المحدثة
            
        العائد:
            كائن الإعداد المحدث أو None إذا لم يتم العثور عليه
        
        يرفع:
            ValueError: إذا كان مفتاح الإعداد موجودًا بالفعل لإعداد آخر
        """
        # الحصول على الإعداد الحالي
        setting = self.get_setting(setting_id)
        if not setting:
            return None
        
        # التحقق من وجود مفتاح الإعداد لإعداد آخر
        key = setting_data.get('key')
        company_id = setting_data.get('company_id', setting.company_id)
        branch_id = setting_data.get('branch_id', setting.branch_id)
        
        if key and key != setting.key:
            if self._is_setting_key_exists(key, company_id, branch_id):
                scope = "عام" if not company_id else f"للشركة '{company_id}'"
                if branch_id:
                    scope += f" والفرع '{branch_id}'"
                raise ValueError(f"مفتاح الإعداد '{key}' موجود بالفعل {scope}")
        
        # تحديث بيانات الإعداد
        for key, value in setting_data.items():
            if key != 'setting_id' and key != 'created_at' and hasattr(setting, key):
                setattr(setting, key, value)
        
        # تحديث تاريخ التحديث
        setting.updated_at = datetime.now()
        
        # حفظ الإعداد في قاعدة البيانات
        self.db_manager.update_system_setting(setting)
        
        return setting
    
    def delete_setting(self, setting_id: str) -> bool:
        """
        حذف إعداد
        
        المعاملات:
            setting_id: معرف الإعداد
            
        العائد:
            True إذا تم الحذف بنجاح، False خلاف ذلك
        """
        return self.db_manager.delete_system_setting(setting_id)
    
    def get_setting_value(
        self,
        key: str,
        company_id: Optional[str] = None,
        branch_id: Optional[str] = None,
        default_value: Any = None
    ) -> Any:
        """
        الحصول على قيمة إعداد
        
        المعاملات:
            key: مفتاح الإعداد
            company_id: معرف الشركة (اختياري)
            branch_id: معرف الفرع (اختياري)
            default_value: القيمة الافتراضية إذا لم يتم العثور على الإعداد (اختياري)
            
        العائد:
            قيمة الإعداد أو القيمة الافتراضية إذا لم يتم العثور على الإعداد
        """
        # البحث عن الإعداد بالترتيب: فرع محدد، شركة محددة، عام
        setting = None
        
        # البحث عن إعداد الفرع
        if branch_id:
            setting = self.get_setting_by_key(key, company_id, branch_id)
        
        # البحث عن إعداد الشركة
        if not setting and company_id:
            setting = self.get_setting_by_key(key, company_id, None)
        
        # البحث عن الإعداد العام
        if not setting:
            setting = self.get_setting_by_key(key, None, None)
        
        # إرجاع القيمة أو القيمة الافتراضية
        if setting:
            return setting.get_typed_value()
        
        return default_value
    
    def set_setting_value(
        self,
        key: str,
        value: Any,
        company_id: Optional[str] = None,
        branch_id: Optional[str] = None,
        description: Optional[str] = None,
        category: Optional[str] = None,
        data_type: Optional[str] = None,
        is_sensitive: bool = False,
        created_by: Optional[str] = None
    ) -> SystemSetting:
        """
        تعيين قيمة إعداد
        
        المعاملات:
            key: مفتاح الإعداد
            value: قيمة الإعداد
            company_id: معرف الشركة (اختياري)
            branch_id: معرف الفرع (اختياري)
            description: وصف الإعداد (اختياري)
            category: فئة الإعداد (اختياري)
            data_type: نوع البيانات (اختياري)
            is_sensitive: ما إذا كان الإعداد حساسًا (اختياري، افتراضي: False)
            created_by: معرف المستخدم الذي أنشأ الإعداد (اختياري)
            
        العائد:
            كائن الإعداد
        """
        # البحث عن الإعداد الحالي
        setting = self.get_setting_by_key(key, company_id, branch_id)
        
        if setting:
            # تحديث الإعداد الحالي
            setting_data = {
                'value': value,
                'updated_by': created_by
            }
            
            # تحديث الحقول الاختيارية إذا تم توفيرها
            if description:
                setting_data['description'] = description
            
            if category:
                setting_data['category'] = category
            
            if data_type:
                setting_data['data_type'] = data_type
            
            if is_sensitive is not None:
                setting_data['is_sensitive'] = is_sensitive
            
            return self.update_setting(setting.setting_id, setting_data)
        else:
            # إنشاء إعداد جديد
            is_global = not company_id and not branch_id
            
            setting_data = {
                'key': key,
                'value': value,
                'company_id': company_id,
                'branch_id': branch_id,
                'is_global': is_global,
                'description': description,
                'category': category,
                'data_type': data_type,
                'is_sensitive': is_sensitive,
                'created_by': created_by,
                'updated_by': created_by
            }
            
            return self.create_setting(setting_data)
    
    def _is_setting_key_exists(
        self,
        key: str,
        company_id: Optional[str] = None,
        branch_id: Optional[str] = None
    ) -> bool:
        """
        التحقق مما إذا كان مفتاح الإعداد موجودًا
        
        المعاملات:
            key: مفتاح الإعداد
            company_id: معرف الشركة (اختياري)
            branch_id: معرف الفرع (اختياري)
            
        العائد:
            True إذا كان مفتاح الإعداد موجودًا، False خلاف ذلك
        """
        return self.get_setting_by_key(key, company_id, branch_id) is not None


class SystemLogService:
    """خدمة إدارة سجلات النظام"""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        تهيئة خدمة سجلات النظام
        
        المعاملات:
            db_manager: مدير قاعدة البيانات
        """
        self.db_manager = db_manager
    
    def log_action(
        self,
        action: str,
        user_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        module: Optional[str] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        company_id: Optional[str] = None,
        branch_id: Optional[str] = None,
        status: Optional[str] = None,
        duration_ms: Optional[int] = None
    ) -> SystemLog:
        """
        تسجيل إجراء في سجل النظام
        
        المعاملات:
            action: الإجراء المتخذ
            user_id: معرف المستخدم (اختياري)
            details: تفاصيل إضافية (اختياري)
            ip_address: عنوان IP (اختياري)
            module: الوحدة المتأثرة (اختياري)
            entity_type: نوع الكيان المتأثر (اختياري)
            entity_id: معرف الكيان المتأثر (اختياري)
            company_id: معرف الشركة (اختياري)
            branch_id: معرف الفرع (اختياري)
            status: حالة الإجراء (اختياري)
            duration_ms: مدة الإجراء بالميلي ثانية (اختياري)
            
        العائد:
            كائن سجل النظام
        """
        # إنشاء كائن سجل النظام
        log = SystemLog(
            log_id=str(uuid.uuid4()),
            action=action,
            user_id=user_id,
            timestamp=datetime.now(),
            details=details,
            ip_address=ip_address,
            module=module,
            entity_type=entity_type,
            entity_id=entity_id,
            company_id=company_id,
            branch_id=branch_id,
            status=status,
            duration_ms=duration_ms
        )
        
        # حفظ السجل في قاعدة البيانات
        self.db_manager.save_system_log(log)
        
        return log
    
    def get_log(self, log_id: str) -> Optional[SystemLog]:
        """
        الحصول على سجل بواسطة المعرف
        
        المعاملات:
            log_id: معرف السجل
            
        العائد:
            كائن السجل أو None إذا لم يتم العثور عليه
        """
        return self.db_manager.get_system_log(log_id)
    
    def get_logs(
        self,
        user_id: Optional[str] = None,
        action: Optional[str] = None,
        module: Optional[str] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        company_id: Optional[str] = None,
        branch_id: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[SystemLog], int]:
        """
        الحصول على سجلات النظام مع تصفية اختيارية
        
        المعاملات:
            user_id: معرف المستخدم (اختياري)
            action: الإجراء المتخذ (اختياري)
            module: الوحدة المتأثرة (اختياري)
            entity_type: نوع الكيان المتأثر (اختياري)
            entity_id: معرف الكيان المتأثر (اختياري)
            company_id: معرف الشركة (اختياري)
            branch_id: معرف الفرع (اختياري)
            status: حالة الإجراء (اختياري)
            start_date: تاريخ البداية (اختياري)
            end_date: تاريخ النهاية (اختياري)
            limit: عدد السجلات المراد إرجاعها (اختياري، افتراضي: 100)
            offset: عدد السجلات المراد تخطيها (اختياري، افتراضي: 0)
            
        العائد:
            زوج من قائمة بكائنات السجلات والعدد الإجمالي للسجلات
        """
        return self.db_manager.get_system_logs(
            user_id, action, module, entity_type, entity_id,
            company_id, branch_id, status, start_date, end_date,
            limit, offset
        )
    
    def delete_logs_older_than(self, days: int) -> int:
        """
        حذف السجلات الأقدم من عدد معين من الأيام
        
        المعاملات:
            days: عدد الأيام
            
        العائد:
            عدد السجلات المحذوفة
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        return self.db_manager.delete_system_logs_older_than(cutoff_date)


class ServerMonitorService:
    """خدمة مراقبة الخادم"""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        تهيئة خدمة مراقبة الخادم
        
        المعاملات:
            db_manager: مدير قاعدة البيانات
        """
        self.db_manager = db_manager
    
    def get_server_status(self) -> ServerStatus:
        """
        الحصول على حالة الخادم الحالية
        
        العائد:
            كائن حالة الخادم
        """
        # جمع معلومات النظام
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        disk = psutil.disk_usage('/')
        disk_usage = disk.percent
        system_uptime = int(time.time() - psutil.boot_time())
        
        # جمع معلومات قاعدة البيانات
        database_size = self.db_manager.get_database_size()
        database_connections = self.db_manager.get_database_connections()
        
        # جمع معلومات المستخدمين النشطين
        active_users = self._get_active_users_count()
        
        # جمع معلومات طلبات API
        api_stats = self._get_api_statistics()
        
        # جمع معلومات الأخطاء والتحذيرات
        error_count, warning_count = self._get_error_warning_counts()
        
        # إنشاء كائن حالة الخادم
        status = ServerStatus(
            status_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
            active_users=active_users,
            system_uptime=system_uptime,
            database_size=database_size,
            database_connections=database_connections,
            api_requests_count=api_stats.get('requests_count'),
            average_response_time=api_stats.get('average_response_time'),
            error_count=error_count,
            warning_count=warning_count,
            details={
                'memory_total': memory.total,
                'memory_available': memory.available,
                'disk_total': disk.total,
                'disk_free': disk.free,
                'network': self._get_network_stats(),
                'processes': self._get_top_processes()
            }
        )
        
        # حفظ حالة الخادم في قاعدة البيانات
        self.db_manager.save_server_status(status)
        
        return status
    
    def get_server_status_history(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[ServerStatus], int]:
        """
        الحصول على سجل حالة الخادم
        
        المعاملات:
            start_date: تاريخ البداية (اختياري)
            end_date: تاريخ النهاية (اختياري)
            limit: عدد السجلات المراد إرجاعها (اختياري، افتراضي: 100)
            offset: عدد السجلات المراد تخطيها (اختياري، افتراضي: 0)
            
        العائد:
            زوج من قائمة بكائنات حالة الخادم والعدد الإجمالي للسجلات
        """
        return self.db_manager.get_server_status_history(start_date, end_date, limit, offset)
    
    def get_server_status_by_id(self, status_id: str) -> Optional[ServerStatus]:
        """
        الحصول على حالة الخادم بواسطة المعرف
        
        المعاملات:
            status_id: معرف الحالة
            
        العائد:
            كائن حالة الخادم أو None إذا لم يتم العثور عليه
        """
        return self.db_manager.get_server_status(status_id)
    
    def delete_server_status_older_than(self, days: int) -> int:
        """
        حذف سجلات حالة الخادم الأقدم من عدد معين من الأيام
        
        المعاملات:
            days: عدد الأيام
            
        العائد:
            عدد السجلات المحذوفة
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        return self.db_manager.delete_server_status_older_than(cutoff_date)
    
    def _get_active_users_count(self) -> int:
        """
        الحصول على عدد المستخدمين النشطين
        
        العائد:
            عدد المستخدمين النشطين
        """
        # الحصول على عدد المستخدمين النشطين من قاعدة البيانات
        # هذا يعتمد على كيفية تتبع المستخدمين النشطين في النظام
        return self.db_manager.get_active_users_count()
    
    def _get_api_statistics(self) -> Dict[str, Any]:
        """
        الحصول على إحصائيات طلبات API
        
        العائد:
            قاموس يحتوي على إحصائيات طلبات API
        """
        # الحصول على إحصائيات طلبات API من قاعدة البيانات
        return {
            'requests_count': self.db_manager.get_api_requests_count(),
            'average_response_time': self.db_manager.get_average_response_time()
        }
    
    def _get_error_warning_counts(self) -> Tuple[int, int]:
        """
        الحصول على عدد الأخطاء والتحذيرات
        
        العائد:
            زوج من عدد الأخطاء وعدد التحذيرات
        """
        # الحصول على عدد الأخطاء والتحذيرات من قاعدة البيانات
        return (
            self.db_manager.get_error_count(),
            self.db_manager.get_warning_count()
        )
    
    def _get_network_stats(self) -> Dict[str, Any]:
        """
        الحصول على إحصائيات الشبكة
        
        العائد:
            قاموس يحتوي على إحصائيات الشبكة
        """
        # الحصول على إحصائيات الشبكة باستخدام psutil
        net_io = psutil.net_io_counters()
        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv,
            'errin': net_io.errin,
            'errout': net_io.errout,
            'dropin': net_io.dropin,
            'dropout': net_io.dropout
        }
    
    def _get_top_processes(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        الحصول على أعلى العمليات استخدامًا للموارد
        
        المعاملات:
            limit: عدد العمليات المراد إرجاعها (اختياري، افتراضي: 5)
            
        العائد:
            قائمة بقواميس تحتوي على معلومات العمليات
        """
        # الحصول على قائمة العمليات
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                pinfo = proc.info
                processes.append({
                    'pid': pinfo['pid'],
                    'name': pinfo['name'],
                    'username': pinfo['username'],
                    'cpu_percent': pinfo['cpu_percent'],
                    'memory_percent': pinfo['memory_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # ترتيب العمليات حسب استخدام وحدة المعالجة المركزية
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        
        return processes[:limit]


class BackupService:
    """خدمة النسخ الاحتياطي واستعادة النظام"""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        تهيئة خدمة النسخ الاحتياطي
        
        المعاملات:
            db_manager: مدير قاعدة البيانات
        """
        self.db_manager = db_manager
        self.backup_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'backups')
        
        # إنشاء مجلد النسخ الاحتياطي إذا لم يكن موجودًا
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_backup(
        self,
        backup_type: str = "full",
        description: Optional[str] = None,
        created_by: Optional[str] = None,
        includes_files: bool = True,
        includes_database: bool = True,
        is_encrypted: bool = False,
        encryption_key_id: Optional[str] = None,
        retention_days: Optional[int] = None,
        is_automatic: bool = False
    ) -> BackupInfo:
        """
        إنشاء نسخة احتياطية
        
        المعاملات:
            backup_type: نوع النسخة الاحتياطية (اختياري، افتراضي: "full")
            description: وصف النسخة الاحتياطية (اختياري)
            created_by: معرف المستخدم الذي أنشأ النسخة الاحتياطية (اختياري)
            includes_files: ما إذا كانت النسخة الاحتياطية تتضمن الملفات (اختياري، افتراضي: True)
            includes_database: ما إذا كانت النسخة الاحتياطية تتضمن قاعدة البيانات (اختياري، افتراضي: True)
            is_encrypted: ما إذا كانت النسخة الاحتياطية مشفرة (اختياري، افتراضي: False)
            encryption_key_id: معرف مفتاح التشفير (اختياري)
            retention_days: عدد أيام الاحتفاظ (اختياري)
            is_automatic: ما إذا كانت النسخة الاحتياطية تلقائية (اختياري، افتراضي: False)
            
        العائد:
            كائن معلومات النسخ الاحتياطي
        
        يرفع:
            ValueError: إذا لم يتم تحديد تضمين الملفات أو قاعدة البيانات
        """
        if not includes_files and not includes_database:
            raise ValueError("يجب تضمين الملفات أو قاعدة البيانات على الأقل")
        
        # إنشاء معرف فريد للنسخة الاحتياطية
        backup_id = str(uuid.uuid4())
        
        # إنشاء اسم الملف
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_{backup_type}_{timestamp}_{backup_id}.zip"
        
        # إنشاء مسار التخزين
        storage_path = os.path.join(self.backup_dir, filename)
        
        # تسجيل بدء عملية النسخ الاحتياطي
        start_time = datetime.now()
        
        # إنشاء كائن معلومات النسخ الاحتياطي
        backup_info = BackupInfo(
            backup_id=backup_id,
            filename=filename,
            created_at=start_time,
            created_by=created_by,
            backup_type=backup_type,
            status="in_progress",
            description=description,
            storage_path=storage_path,
            is_encrypted=is_encrypted,
            encryption_key_id=encryption_key_id,
            database_version=self.db_manager.get_database_version(),
            system_version=self._get_system_version(),
            includes_files=includes_files,
            includes_database=includes_database,
            retention_days=retention_days,
            is_automatic=is_automatic
        )
        
        # حفظ معلومات النسخ الاحتياطي في قاعدة البيانات
        self.db_manager.save_backup_info(backup_info)
        
        try:
            # إنشاء النسخة الاحتياطية
            self._perform_backup(backup_info)
            
            # تحديث حالة النسخة الاحتياطية
            completion_time = datetime.now()
            duration_seconds = int((completion_time - start_time).total_seconds())
            size_bytes = os.path.getsize(storage_path)
            
            backup_info.status = "completed"
            backup_info.completion_time = completion_time
            backup_info.duration_seconds = duration_seconds
            backup_info.size_bytes = size_bytes
            
            # حفظ معلومات النسخ الاحتياطي المحدثة في قاعدة البيانات
            self.db_manager.update_backup_info(backup_info)
            
            return backup_info
        except Exception as e:
            # تحديث حالة النسخة الاحتياطية في حالة الفشل
            backup_info.status = "failed"
            backup_info.details = {"error": str(e)}
            
            # حفظ معلومات النسخ الاحتياطي المحدثة في قاعدة البيانات
            self.db_manager.update_backup_info(backup_info)
            
            # إعادة رفع الاستثناء
            raise
    
    def restore_backup(
        self,
        backup_id: str,
        restore_files: bool = True,
        restore_database: bool = True,
        encryption_key: Optional[str] = None
    ) -> bool:
        """
        استعادة نسخة احتياطية
        
        المعاملات:
            backup_id: معرف النسخة الاحتياطية
            restore_files: ما إذا كان يجب استعادة الملفات (اختياري، افتراضي: True)
            restore_database: ما إذا كان يجب استعادة قاعدة البيانات (اختياري، افتراضي: True)
            encryption_key: مفتاح التشفير (اختياري)
            
        العائد:
            True إذا تمت الاستعادة بنجاح، False خلاف ذلك
        
        يرفع:
            ValueError: إذا لم يتم العثور على النسخة الاحتياطية أو إذا كانت النسخة الاحتياطية مشفرة ولم يتم توفير مفتاح التشفير
        """
        # الحصول على معلومات النسخة الاحتياطية
        backup_info = self.get_backup_info(backup_id)
        if not backup_info:
            raise ValueError(f"لم يتم العثور على النسخة الاحتياطية بالمعرف {backup_id}")
        
        # التحقق من حالة النسخة الاحتياطية
        if backup_info.status != "completed":
            raise ValueError(f"لا يمكن استعادة النسخة الاحتياطية بالحالة {backup_info.status}")
        
        # التحقق من وجود ملف النسخة الاحتياطية
        if not os.path.exists(backup_info.storage_path):
            raise ValueError(f"ملف النسخة الاحتياطية غير موجود: {backup_info.storage_path}")
        
        # التحقق من التشفير
        if backup_info.is_encrypted and not encryption_key:
            raise ValueError("النسخة الاحتياطية مشفرة ولم يتم توفير مفتاح التشفير")
        
        # استعادة النسخة الاحتياطية
        return self._perform_restore(backup_info, restore_files, restore_database, encryption_key)
    
    def get_backup_info(self, backup_id: str) -> Optional[BackupInfo]:
        """
        الحصول على معلومات النسخ الاحتياطي بواسطة المعرف
        
        المعاملات:
            backup_id: معرف النسخة الاحتياطية
            
        العائد:
            كائن معلومات النسخ الاحتياطي أو None إذا لم يتم العثور عليه
        """
        return self.db_manager.get_backup_info(backup_id)
    
    def get_all_backups(
        self,
        backup_type: Optional[str] = None,
        status: Optional[str] = None,
        created_by: Optional[str] = None,
        is_automatic: Optional[bool] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[BackupInfo], int]:
        """
        الحصول على جميع النسخ الاحتياطية مع تصفية اختيارية
        
        المعاملات:
            backup_type: نوع النسخة الاحتياطية (اختياري)
            status: حالة النسخة الاحتياطية (اختياري)
            created_by: معرف المستخدم الذي أنشأ النسخة الاحتياطية (اختياري)
            is_automatic: ما إذا كانت النسخة الاحتياطية تلقائية (اختياري)
            start_date: تاريخ البداية (اختياري)
            end_date: تاريخ النهاية (اختياري)
            limit: عدد النسخ الاحتياطية المراد إرجاعها (اختياري، افتراضي: 100)
            offset: عدد النسخ الاحتياطية المراد تخطيها (اختياري، افتراضي: 0)
            
        العائد:
            زوج من قائمة بكائنات معلومات النسخ الاحتياطي والعدد الإجمالي للنسخ الاحتياطية
        """
        return self.db_manager.get_all_backups(
            backup_type, status, created_by, is_automatic,
            start_date, end_date, limit, offset
        )
    
    def delete_backup(self, backup_id: str) -> bool:
        """
        حذف نسخة احتياطية
        
        المعاملات:
            backup_id: معرف النسخة الاحتياطية
            
        العائد:
            True إذا تم الحذف بنجاح، False خلاف ذلك
        
        يرفع:
            ValueError: إذا لم يتم العثور على النسخة الاحتياطية
        """
        # الحصول على معلومات النسخة الاحتياطية
        backup_info = self.get_backup_info(backup_id)
        if not backup_info:
            raise ValueError(f"لم يتم العثور على النسخة الاحتياطية بالمعرف {backup_id}")
        
        # حذف ملف النسخة الاحتياطية إذا كان موجودًا
        if os.path.exists(backup_info.storage_path):
            os.remove(backup_info.storage_path)
        
        # حذف معلومات النسخة الاحتياطية من قاعدة البيانات
        return self.db_manager.delete_backup_info(backup_id)
    
    def delete_backups_older_than(self, days: int) -> int:
        """
        حذف النسخ الاحتياطية الأقدم من عدد معين من الأيام
        
        المعاملات:
            days: عدد الأيام
            
        العائد:
            عدد النسخ الاحتياطية المحذوفة
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # الحصول على النسخ الاحتياطية القديمة
        backups, _ = self.get_all_backups(end_date=cutoff_date, limit=1000)
        
        # حذف النسخ الاحتياطية
        count = 0
        for backup in backups:
            # تخطي النسخ الاحتياطية التي لها فترة احتفاظ محددة ولم تنتهِ بعد
            if backup.retention_days and (datetime.now() - backup.created_at).days < backup.retention_days:
                continue
            
            # حذف النسخة الاحتياطية
            if self.delete_backup(backup.backup_id):
                count += 1
        
        return count
    
    def _perform_backup(self, backup_info: BackupInfo) -> None:
        """
        تنفيذ عملية النسخ الاحتياطي
        
        المعاملات:
            backup_info: كائن معلومات النسخ الاحتياطي
            
        يرفع:
            Exception: إذا فشلت عملية النسخ الاحتياطي
        """
        import zipfile
        import tempfile
        
        # إنشاء ملف مؤقت للنسخة الاحتياطية
        with tempfile.TemporaryDirectory() as temp_dir:
            # إنشاء مجلد للنسخة الاحتياطية
            backup_temp_dir = os.path.join(temp_dir, "backup")
            os.makedirs(backup_temp_dir, exist_ok=True)
            
            # نسخ الملفات إذا كان مطلوبًا
            if backup_info.includes_files:
                self._backup_files(backup_temp_dir)
            
            # نسخ قاعدة البيانات إذا كان مطلوبًا
            if backup_info.includes_database:
                self._backup_database(backup_temp_dir)
            
            # إنشاء ملف النسخة الاحتياطية
            with zipfile.ZipFile(backup_info.storage_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # إضافة الملفات إلى ملف الضغط
                for root, _, files in os.walk(backup_temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, backup_temp_dir)
                        zipf.write(file_path, arcname)
            
            # تشفير النسخة الاحتياطية إذا كان مطلوبًا
            if backup_info.is_encrypted:
                self._encrypt_backup(backup_info)
    
    def _backup_files(self, backup_dir: str) -> None:
        """
        نسخ الملفات إلى مجلد النسخة الاحتياطية
        
        المعاملات:
            backup_dir: مجلد النسخة الاحتياطية
        """
        # تحديد المجلدات التي يجب نسخها
        source_dirs = [
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads'),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static'),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config')
        ]
        
        # نسخ المجلدات
        for source_dir in source_dirs:
            if os.path.exists(source_dir):
                dest_dir = os.path.join(backup_dir, os.path.basename(source_dir))
                shutil.copytree(source_dir, dest_dir)
    
    def _backup_database(self, backup_dir: str) -> None:
        """
        نسخ قاعدة البيانات إلى مجلد النسخة الاحتياطية
        
        المعاملات:
            backup_dir: مجلد النسخة الاحتياطية
        """
        # إنشاء مجلد لقاعدة البيانات
        db_dir = os.path.join(backup_dir, 'database')
        os.makedirs(db_dir, exist_ok=True)
        
        # استخدام مدير قاعدة البيانات لإنشاء نسخة احتياطية
        db_file = os.path.join(db_dir, 'database_backup.sql')
        self.db_manager.backup_database(db_file)
    
    def _encrypt_backup(self, backup_info: BackupInfo) -> None:
        """
        تشفير ملف النسخة الاحتياطية
        
        المعاملات:
            backup_info: كائن معلومات النسخ الاحتياطي
        """
        # تنفيذ التشفير (هذا مثال بسيط، يجب استخدام طريقة تشفير أكثر أمانًا في الإنتاج)
        # في هذا المثال، نفترض أن مفتاح التشفير متاح من خلال معرف مفتاح التشفير
        pass
    
    def _perform_restore(
        self,
        backup_info: BackupInfo,
        restore_files: bool,
        restore_database: bool,
        encryption_key: Optional[str]
    ) -> bool:
        """
        تنفيذ عملية استعادة النسخة الاحتياطية
        
        المعاملات:
            backup_info: كائن معلومات النسخ الاحتياطي
            restore_files: ما إذا كان يجب استعادة الملفات
            restore_database: ما إذا كان يجب استعادة قاعدة البيانات
            encryption_key: مفتاح التشفير
            
        العائد:
            True إذا تمت الاستعادة بنجاح، False خلاف ذلك
        """
        import zipfile
        import tempfile
        
        # فك تشفير النسخة الاحتياطية إذا كانت مشفرة
        if backup_info.is_encrypted:
            self._decrypt_backup(backup_info, encryption_key)
        
        # استخراج النسخة الاحتياطية إلى مجلد مؤقت
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(backup_info.storage_path, 'r') as zipf:
                zipf.extractall(temp_dir)
            
            # استعادة الملفات إذا كان مطلوبًا
            if restore_files and backup_info.includes_files:
                self._restore_files(temp_dir)
            
            # استعادة قاعدة البيانات إذا كان مطلوبًا
            if restore_database and backup_info.includes_database:
                self._restore_database(temp_dir)
        
        return True
    
    def _restore_files(self, extract_dir: str) -> None:
        """
        استعادة الملفات من مجلد النسخة الاحتياطية
        
        المعاملات:
            extract_dir: مجلد استخراج النسخة الاحتياطية
        """
        # تحديد المجلدات التي يجب استعادتها
        source_dirs = [
            os.path.join(extract_dir, 'uploads'),
            os.path.join(extract_dir, 'static'),
            os.path.join(extract_dir, 'config')
        ]
        
        # استعادة المجلدات
        for source_dir in source_dirs:
            if os.path.exists(source_dir):
                dest_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), os.path.basename(source_dir))
                
                # حذف المجلد الحالي إذا كان موجودًا
                if os.path.exists(dest_dir):
                    shutil.rmtree(dest_dir)
                
                # نسخ المجلد من النسخة الاحتياطية
                shutil.copytree(source_dir, dest_dir)
    
    def _restore_database(self, extract_dir: str) -> None:
        """
        استعادة قاعدة البيانات من مجلد النسخة الاحتياطية
        
        المعاملات:
            extract_dir: مجلد استخراج النسخة الاحتياطية
        """
        # تحديد ملف قاعدة البيانات
        db_file = os.path.join(extract_dir, 'database', 'database_backup.sql')
        
        if os.path.exists(db_file):
            # استخدام مدير قاعدة البيانات لاستعادة قاعدة البيانات
            self.db_manager.restore_database(db_file)
    
    def _decrypt_backup(self, backup_info: BackupInfo, encryption_key: str) -> None:
        """
        فك تشفير ملف النسخة الاحتياطية
        
        المعاملات:
            backup_info: كائن معلومات النسخ الاحتياطي
            encryption_key: مفتاح التشفير
        """
        # تنفيذ فك التشفير (هذا مثال بسيط، يجب استخدام طريقة فك تشفير مناسبة في الإنتاج)
        pass
    
    def _get_system_version(self) -> str:
        """
        الحصول على إصدار النظام
        
        العائد:
            إصدار النظام
        """
        # الحصول على إصدار النظام من ملف التكوين أو متغير بيئي
        return "1.0.0"  # مثال
