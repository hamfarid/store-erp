"""
نماذج بيانات الموارد البشرية
يحتوي هذا الملف على تعريف نماذج بيانات الموارد البشرية في نظام Gaara ERP
"""

import uuid
from datetime import datetime, date
from typing import List, Dict, Any, Optional, Union
from enum import Enum


class EmploymentType(str, Enum):
    """أنواع التوظيف"""
    FULL_TIME = "دوام كامل"
    PART_TIME = "دوام جزئي"
    CONTRACT = "عقد مؤقت"
    SEASONAL = "موسمي"
    INTERNSHIP = "تدريب"


class EmployeeStatus(str, Enum):
    """حالات الموظف"""
    ACTIVE = "نشط"
    ON_LEAVE = "في إجازة"
    SUSPENDED = "موقوف"
    TERMINATED = "منتهي الخدمة"


class LeaveType(str, Enum):
    """أنواع الإجازات"""
    ANNUAL = "سنوية"
    SICK = "مرضية"
    MATERNITY = "أمومة"
    PATERNITY = "أبوة"
    UNPAID = "بدون راتب"
    EMERGENCY = "طارئة"
    OTHER = "أخرى"


class LeaveStatus(str, Enum):
    """حالات طلب الإجازة"""
    PENDING = "قيد الانتظار"
    APPROVED = "موافق عليها"
    REJECTED = "مرفوضة"
    CANCELLED = "ملغاة"


class AttendanceStatus(str, Enum):
    """حالات الحضور"""
    PRESENT = "حاضر"
    ABSENT = "غائب"
    LATE = "متأخر"
    HALF_DAY = "نصف يوم"
    ON_LEAVE = "في إجازة"


class Department:
    """قسم في المؤسسة"""
    
    def __init__(
        self,
        department_id: str,
        name: str,
        description: Optional[str] = None,
        manager_id: Optional[str] = None,
        parent_department_id: Optional[str] = None,
        company_id: str = "",
        branch_id: Optional[str] = None,
        creation_date: datetime = None,
        status: str = "نشط"
    ):
        """
        تهيئة قسم جديد
        
        المعاملات:
            department_id: معرف القسم
            name: اسم القسم
            description: وصف القسم
            manager_id: معرف مدير القسم
            parent_department_id: معرف القسم الأب
            company_id: معرف الشركة
            branch_id: معرف الفرع
            creation_date: تاريخ الإنشاء
            status: حالة القسم
        """
        self.department_id = department_id
        self.name = name
        self.description = description
        self.manager_id = manager_id
        self.parent_department_id = parent_department_id
        self.company_id = company_id
        self.branch_id = branch_id
        self.creation_date = creation_date or datetime.now()
        self.status = status
        self.employees: List['Employee'] = []
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Department':
        """
        إنشاء كائن قسم من قاموس
        
        المعاملات:
            data: قاموس يحتوي على بيانات القسم
            
        العائد:
            كائن قسم جديد
        """
        # تحويل تاريخ الإنشاء إلى كائن datetime إذا كان موجوداً
        creation_date = data.get('creation_date')
        if isinstance(creation_date, str):
            creation_date = datetime.fromisoformat(creation_date)
        
        return cls(
            department_id=data.get('department_id', str(uuid.uuid4())),
            name=data.get('name', ''),
            description=data.get('description'),
            manager_id=data.get('manager_id'),
            parent_department_id=data.get('parent_department_id'),
            company_id=data.get('company_id', ''),
            branch_id=data.get('branch_id'),
            creation_date=creation_date,
            status=data.get('status', 'نشط')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل كائن القسم إلى قاموس
        
        العائد:
            قاموس يحتوي على بيانات القسم
        """
        return {
            'department_id': self.department_id,
            'name': self.name,
            'description': self.description,
            'manager_id': self.manager_id,
            'parent_department_id': self.parent_department_id,
            'company_id': self.company_id,
            'branch_id': self.branch_id,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None,
            'status': self.status,
            'employees': [employee.to_dict() for employee in self.employees] if hasattr(self, 'employees') and self.employees else []
        }


class JobPosition:
    """منصب وظيفي"""
    
    def __init__(
        self,
        position_id: str,
        title: str,
        department_id: str,
        description: Optional[str] = None,
        requirements: Optional[str] = None,
        salary_range_min: Optional[float] = None,
        salary_range_max: Optional[float] = None,
        company_id: str = "",
        branch_id: Optional[str] = None,
        creation_date: datetime = None,
        status: str = "نشط"
    ):
        """
        تهيئة منصب وظيفي جديد
        
        المعاملات:
            position_id: معرف المنصب
            title: عنوان المنصب
            department_id: معرف القسم
            description: وصف المنصب
            requirements: متطلبات المنصب
            salary_range_min: الحد الأدنى لنطاق الراتب
            salary_range_max: الحد الأقصى لنطاق الراتب
            company_id: معرف الشركة
            branch_id: معرف الفرع
            creation_date: تاريخ الإنشاء
            status: حالة المنصب
        """
        self.position_id = position_id
        self.title = title
        self.department_id = department_id
        self.description = description
        self.requirements = requirements
        self.salary_range_min = salary_range_min
        self.salary_range_max = salary_range_max
        self.company_id = company_id
        self.branch_id = branch_id
        self.creation_date = creation_date or datetime.now()
        self.status = status
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JobPosition':
        """
        إنشاء كائن منصب وظيفي من قاموس
        
        المعاملات:
            data: قاموس يحتوي على بيانات المنصب
            
        العائد:
            كائن منصب وظيفي جديد
        """
        # تحويل تاريخ الإنشاء إلى كائن datetime إذا كان موجوداً
        creation_date = data.get('creation_date')
        if isinstance(creation_date, str):
            creation_date = datetime.fromisoformat(creation_date)
        
        return cls(
            position_id=data.get('position_id', str(uuid.uuid4())),
            title=data.get('title', ''),
            department_id=data.get('department_id', ''),
            description=data.get('description'),
            requirements=data.get('requirements'),
            salary_range_min=data.get('salary_range_min'),
            salary_range_max=data.get('salary_range_max'),
            company_id=data.get('company_id', ''),
            branch_id=data.get('branch_id'),
            creation_date=creation_date,
            status=data.get('status', 'نشط')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل كائن المنصب الوظيفي إلى قاموس
        
        العائد:
            قاموس يحتوي على بيانات المنصب
        """
        return {
            'position_id': self.position_id,
            'title': self.title,
            'department_id': self.department_id,
            'description': self.description,
            'requirements': self.requirements,
            'salary_range_min': self.salary_range_min,
            'salary_range_max': self.salary_range_max,
            'company_id': self.company_id,
            'branch_id': self.branch_id,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None,
            'status': self.status
        }


class Employee:
    """موظف"""
    
    def __init__(
        self,
        employee_id: str,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        position_id: str,
        department_id: str,
        hire_date: date,
        employment_type: Union[EmploymentType, str] = EmploymentType.FULL_TIME,
        status: Union[EmployeeStatus, str] = EmployeeStatus.ACTIVE,
        birth_date: Optional[date] = None,
        address: Optional[str] = None,
        national_id: Optional[str] = None,
        salary: Optional[float] = None,
        manager_id: Optional[str] = None,
        company_id: str = "",
        branch_id: Optional[str] = None,
        creation_date: datetime = None,
        profile_image: Optional[str] = None
    ):
        """
        تهيئة موظف جديد
        
        المعاملات:
            employee_id: معرف الموظف
            first_name: الاسم الأول
            last_name: الاسم الأخير
            email: البريد الإلكتروني
            phone: رقم الهاتف
            position_id: معرف المنصب
            department_id: معرف القسم
            hire_date: تاريخ التوظيف
            employment_type: نوع التوظيف
            status: حالة الموظف
            birth_date: تاريخ الميلاد
            address: العنوان
            national_id: رقم الهوية الوطنية
            salary: الراتب
            manager_id: معرف المدير
            company_id: معرف الشركة
            branch_id: معرف الفرع
            creation_date: تاريخ الإنشاء
            profile_image: مسار صورة الملف الشخصي
        """
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.position_id = position_id
        self.department_id = department_id
        self.hire_date = hire_date
        
        # التحقق من نوع التوظيف وتحويله إذا كان نصاً
        if isinstance(employment_type, str):
            try:
                self.employment_type = EmploymentType(employment_type)
            except ValueError:
                self.employment_type = EmploymentType.FULL_TIME
        else:
            self.employment_type = employment_type
        
        # التحقق من حالة الموظف وتحويلها إذا كانت نصاً
        if isinstance(status, str):
            try:
                self.status = EmployeeStatus(status)
            except ValueError:
                self.status = EmployeeStatus.ACTIVE
        else:
            self.status = status
        
        self.birth_date = birth_date
        self.address = address
        self.national_id = national_id
        self.salary = salary
        self.manager_id = manager_id
        self.company_id = company_id
        self.branch_id = branch_id
        self.creation_date = creation_date or datetime.now()
        self.profile_image = profile_image
        self.leaves: List['Leave'] = []
        self.attendances: List['Attendance'] = []
        self.documents: List['EmployeeDocument'] = []
        self.skills: List['EmployeeSkill'] = []
    
    @property
    def full_name(self) -> str:
        """
        الحصول على الاسم الكامل للموظف
        
        العائد:
            الاسم الكامل
        """
        return f"{self.first_name} {self.last_name}"
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Employee':
        """
        إنشاء كائن موظف من قاموس
        
        المعاملات:
            data: قاموس يحتوي على بيانات الموظف
            
        العائد:
            كائن موظف جديد
        """
        # تحويل تاريخ التوظيف إلى كائن date إذا كان موجوداً
        hire_date = data.get('hire_date')
        if isinstance(hire_date, str):
            hire_date = date.fromisoformat(hire_date)
        
        # تحويل تاريخ الميلاد إلى كائن date إذا كان موجوداً
        birth_date = data.get('birth_date')
        if isinstance(birth_date, str):
            birth_date = date.fromisoformat(birth_date)
        
        # تحويل تاريخ الإنشاء إلى كائن datetime إذا كان موجوداً
        creation_date = data.get('creation_date')
        if isinstance(creation_date, str):
            creation_date = datetime.fromisoformat(creation_date)
        
        return cls(
            employee_id=data.get('employee_id', str(uuid.uuid4())),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            position_id=data.get('position_id', ''),
            department_id=data.get('department_id', ''),
            hire_date=hire_date or date.today(),
            employment_type=data.get('employment_type', EmploymentType.FULL_TIME),
            status=data.get('status', EmployeeStatus.ACTIVE),
            birth_date=birth_date,
            address=data.get('address'),
            national_id=data.get('national_id'),
            salary=data.get('salary'),
            manager_id=data.get('manager_id'),
            company_id=data.get('company_id', ''),
            branch_id=data.get('branch_id'),
            creation_date=creation_date,
            profile_image=data.get('profile_image')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل كائن الموظف إلى قاموس
        
        العائد:
            قاموس يحتوي على بيانات الموظف
        """
        return {
            'employee_id': self.employee_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'position_id': self.position_id,
            'department_id': self.department_id,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'employment_type': self.employment_type.value if isinstance(self.employment_type, EmploymentType) else self.employment_type,
            'status': self.status.value if isinstance(self.status, EmployeeStatus) else self.status,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'address': self.address,
            'national_id': self.national_id,
            'salary': self.salary,
            'manager_id': self.manager_id,
            'company_id': self.company_id,
            'branch_id': self.branch_id,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None,
            'profile_image': self.profile_image,
            'leaves': [leave.to_dict() for leave in self.leaves] if hasattr(self, 'leaves') and self.leaves else [],
            'attendances': [attendance.to_dict() for attendance in self.attendances] if hasattr(self, 'attendances') and self.attendances else [],
            'documents': [document.to_dict() for document in self.documents] if hasattr(self, 'documents') and self.documents else [],
            'skills': [skill.to_dict() for skill in self.skills] if hasattr(self, 'skills') and self.skills else []
        }


class Leave:
    """إجازة موظف"""
    
    def __init__(
        self,
        leave_id: str,
        employee_id: str,
        leave_type: Union[LeaveType, str],
        start_date: date,
        end_date: date,
        status: Union[LeaveStatus, str] = LeaveStatus.PENDING,
        reason: Optional[str] = None,
        approved_by: Optional[str] = None,
        approval_date: Optional[datetime] = None,
        comments: Optional[str] = None,
        creation_date: datetime = None
    ):
        """
        تهيئة إجازة جديدة
        
        المعاملات:
            leave_id: معرف الإجازة
            employee_id: معرف الموظف
            leave_type: نوع الإجازة
            start_date: تاريخ البداية
            end_date: تاريخ النهاية
            status: حالة الإجازة
            reason: سبب الإجازة
            approved_by: معرف الموظف الذي وافق على الإجازة
            approval_date: تاريخ الموافقة
            comments: تعليقات
            creation_date: تاريخ الإنشاء
        """
        self.leave_id = leave_id
        self.employee_id = employee_id
        
        # التحقق من نوع الإجازة وتحويله إذا كان نصاً
        if isinstance(leave_type, str):
            try:
                self.leave_type = LeaveType(leave_type)
            except ValueError:
                self.leave_type = LeaveType.OTHER
        else:
            self.leave_type = leave_type
        
        self.start_date = start_date
        self.end_date = end_date
        
        # التحقق من حالة الإجازة وتحويلها إذا كانت نصاً
        if isinstance(status, str):
            try:
                self.status = LeaveStatus(status)
            except ValueError:
                self.status = LeaveStatus.PENDING
        else:
            self.status = status
        
        self.reason = reason
        self.approved_by = approved_by
        self.approval_date = approval_date
        self.comments = comments
        self.creation_date = creation_date or datetime.now()
    
    @property
    def duration(self) -> int:
        """
        حساب مدة الإجازة بالأيام
        
        العائد:
            عدد أيام الإجازة
        """
        if not self.start_date or not self.end_date:
            return 0
        
        delta = self.end_date - self.start_date
        return delta.days + 1  # نضيف 1 لتضمين يوم النهاية
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Leave':
        """
        إنشاء كائن إجازة من قاموس
        
        المعاملات:
            data: قاموس يحتوي على بيانات الإجازة
            
        العائد:
            كائن إجازة جديد
        """
        # تحويل تواريخ البداية والنهاية إلى كائنات date إذا كانت موجودة
        start_date = data.get('start_date')
        if isinstance(start_date, str):
            start_date = date.fromisoformat(start_date)
        
        end_date = data.get('end_date')
        if isinstance(end_date, str):
            end_date = date.fromisoformat(end_date)
        
        # تحويل تاريخ الموافقة إلى كائن datetime إذا كان موجوداً
        approval_date = data.get('approval_date')
        if isinstance(approval_date, str):
            approval_date = datetime.fromisoformat(approval_date)
        
        # تحويل تاريخ الإنشاء إلى كائن datetime إذا كان موجوداً
        creation_date = data.get('creation_date')
        if isinstance(creation_date, str):
            creation_date = datetime.fromisoformat(creation_date)
        
        return cls(
            leave_id=data.get('leave_id', str(uuid.uuid4())),
            employee_id=data.get('employee_id', ''),
            leave_type=data.get('leave_type', LeaveType.OTHER),
            start_date=start_date or date.today(),
            end_date=end_date or date.today(),
            status=data.get('status', LeaveStatus.PENDING),
            reason=data.get('reason'),
            approved_by=data.get('approved_by'),
            approval_date=approval_date,
            comments=data.get('comments'),
            creation_date=creation_date
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل كائن الإجازة إلى قاموس
        
        العائد:
            قاموس يحتوي على بيانات الإجازة
        """
        return {
            'leave_id': self.leave_id,
            'employee_id': self.employee_id,
            'leave_type': self.leave_type.value if isinstance(self.leave_type, LeaveType) else self.leave_type,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'duration': self.duration,
            'status': self.status.value if isinstance(self.status, LeaveStatus) else self.status,
            'reason': self.reason,
            'approved_by': self.approved_by,
            'approval_date': self.approval_date.isoformat() if self.approval_date else None,
            'comments': self.comments,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None
        }


class Attendance:
    """سجل حضور موظف"""
    
    def __init__(
        self,
        attendance_id: str,
        employee_id: str,
        date: date,
        status: Union[AttendanceStatus, str] = AttendanceStatus.PRESENT,
        check_in: Optional[datetime] = None,
        check_out: Optional[datetime] = None,
        working_hours: Optional[float] = None,
        late_hours: Optional[float] = None,
        overtime_hours: Optional[float] = None,
        notes: Optional[str] = None,
        creation_date: datetime = None
    ):
        """
        تهيئة سجل حضور جديد
        
        المعاملات:
            attendance_id: معرف سجل الحضور
            employee_id: معرف الموظف
            date: تاريخ الحضور
            status: حالة الحضور
            check_in: وقت تسجيل الدخول
            check_out: وقت تسجيل الخروج
            working_hours: ساعات العمل
            late_hours: ساعات التأخير
            overtime_hours: ساعات العمل الإضافي
            notes: ملاحظات
            creation_date: تاريخ الإنشاء
        """
        self.attendance_id = attendance_id
        self.employee_id = employee_id
        self.date = date
        
        # التحقق من حالة الحضور وتحويلها إذا كانت نصاً
        if isinstance(status, str):
            try:
                self.status = AttendanceStatus(status)
            except ValueError:
                self.status = AttendanceStatus.PRESENT
        else:
            self.status = status
        
        self.check_in = check_in
        self.check_out = check_out
        self.working_hours = working_hours
        self.late_hours = late_hours
        self.overtime_hours = overtime_hours
        self.notes = notes
        self.creation_date = creation_date or datetime.now()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Attendance':
        """
        إنشاء كائن سجل حضور من قاموس
        
        المعاملات:
            data: قاموس يحتوي على بيانات سجل الحضور
            
        العائد:
            كائن سجل حضور جديد
        """
        # تحويل التاريخ إلى كائن date إذا كان موجوداً
        attendance_date = data.get('date')
        if isinstance(attendance_date, str):
            attendance_date = date.fromisoformat(attendance_date)
        
        # تحويل أوقات تسجيل الدخول والخروج إلى كائنات datetime إذا كانت موجودة
        check_in = data.get('check_in')
        if isinstance(check_in, str):
            check_in = datetime.fromisoformat(check_in)
        
        check_out = data.get('check_out')
        if isinstance(check_out, str):
            check_out = datetime.fromisoformat(check_out)
        
        # تحويل تاريخ الإنشاء إلى كائن datetime إذا كان موجوداً
        creation_date = data.get('creation_date')
        if isinstance(creation_date, str):
            creation_date = datetime.fromisoformat(creation_date)
        
        return cls(
            attendance_id=data.get('attendance_id', str(uuid.uuid4())),
            employee_id=data.get('employee_id', ''),
            date=attendance_date or date.today(),
            status=data.get('status', AttendanceStatus.PRESENT),
            check_in=check_in,
            check_out=check_out,
            working_hours=data.get('working_hours'),
            late_hours=data.get('late_hours'),
            overtime_hours=data.get('overtime_hours'),
            notes=data.get('notes'),
            creation_date=creation_date
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل كائن سجل الحضور إلى قاموس
        
        العائد:
            قاموس يحتوي على بيانات سجل الحضور
        """
        return {
            'attendance_id': self.attendance_id,
            'employee_id': self.employee_id,
            'date': self.date.isoformat() if self.date else None,
            'status': self.status.value if isinstance(self.status, AttendanceStatus) else self.status,
            'check_in': self.check_in.isoformat() if self.check_in else None,
            'check_out': self.check_out.isoformat() if self.check_out else None,
            'working_hours': self.working_hours,
            'late_hours': self.late_hours,
            'overtime_hours': self.overtime_hours,
            'notes': self.notes,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None
        }


class EmployeeDocument:
    """مستند موظف"""
    
    def __init__(
        self,
        document_id: str,
        employee_id: str,
        document_type: str,
        title: str,
        file_path: str,
        description: Optional[str] = None,
        expiry_date: Optional[date] = None,
        upload_date: datetime = None,
        status: str = "نشط",
        notes: Optional[str] = None
    ):
        """
        تهيئة مستند موظف جديد
        
        المعاملات:
            document_id: معرف المستند
            employee_id: معرف الموظف
            document_type: نوع المستند
            title: عنوان المستند
            file_path: مسار الملف
            description: وصف المستند
            expiry_date: تاريخ انتهاء الصلاحية
            upload_date: تاريخ الرفع
            status: حالة المستند
            notes: ملاحظات
        """
        self.document_id = document_id
        self.employee_id = employee_id
        self.document_type = document_type
        self.title = title
        self.file_path = file_path
        self.description = description
        self.expiry_date = expiry_date
        self.upload_date = upload_date or datetime.now()
        self.status = status
        self.notes = notes
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EmployeeDocument':
        """
        إنشاء كائن مستند موظف من قاموس
        
        المعاملات:
            data: قاموس يحتوي على بيانات المستند
            
        العائد:
            كائن مستند موظف جديد
        """
        # تحويل تاريخ انتهاء الصلاحية إلى كائن date إذا كان موجوداً
        expiry_date = data.get('expiry_date')
        if isinstance(expiry_date, str):
            expiry_date = date.fromisoformat(expiry_date)
        
        # تحويل تاريخ الرفع إلى كائن datetime إذا كان موجوداً
        upload_date = data.get('upload_date')
        if isinstance(upload_date, str):
            upload_date = datetime.fromisoformat(upload_date)
        
        return cls(
            document_id=data.get('document_id', str(uuid.uuid4())),
            employee_id=data.get('employee_id', ''),
            document_type=data.get('document_type', ''),
            title=data.get('title', ''),
            file_path=data.get('file_path', ''),
            description=data.get('description'),
            expiry_date=expiry_date,
            upload_date=upload_date,
            status=data.get('status', 'نشط'),
            notes=data.get('notes')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل كائن مستند الموظف إلى قاموس
        
        العائد:
            قاموس يحتوي على بيانات المستند
        """
        return {
            'document_id': self.document_id,
            'employee_id': self.employee_id,
            'document_type': self.document_type,
            'title': self.title,
            'file_path': self.file_path,
            'description': self.description,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'status': self.status,
            'notes': self.notes
        }


class Skill:
    """مهارة"""
    
    def __init__(
        self,
        skill_id: str,
        name: str,
        category: Optional[str] = None,
        description: Optional[str] = None,
        company_id: str = "",
        creation_date: datetime = None
    ):
        """
        تهيئة مهارة جديدة
        
        المعاملات:
            skill_id: معرف المهارة
            name: اسم المهارة
            category: فئة المهارة
            description: وصف المهارة
            company_id: معرف الشركة
            creation_date: تاريخ الإنشاء
        """
        self.skill_id = skill_id
        self.name = name
        self.category = category
        self.description = description
        self.company_id = company_id
        self.creation_date = creation_date or datetime.now()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Skill':
        """
        إنشاء كائن مهارة من قاموس
        
        المعاملات:
            data: قاموس يحتوي على بيانات المهارة
            
        العائد:
            كائن مهارة جديد
        """
        # تحويل تاريخ الإنشاء إلى كائن datetime إذا كان موجوداً
        creation_date = data.get('creation_date')
        if isinstance(creation_date, str):
            creation_date = datetime.fromisoformat(creation_date)
        
        return cls(
            skill_id=data.get('skill_id', str(uuid.uuid4())),
            name=data.get('name', ''),
            category=data.get('category'),
            description=data.get('description'),
            company_id=data.get('company_id', ''),
            creation_date=creation_date
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل كائن المهارة إلى قاموس
        
        العائد:
            قاموس يحتوي على بيانات المهارة
        """
        return {
            'skill_id': self.skill_id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'company_id': self.company_id,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None
        }


class EmployeeSkill:
    """مهارة موظف"""
    
    def __init__(
        self,
        employee_skill_id: str,
        employee_id: str,
        skill_id: str,
        proficiency_level: int = 1,
        years_of_experience: Optional[float] = None,
        certification: Optional[str] = None,
        notes: Optional[str] = None,
        creation_date: datetime = None
    ):
        """
        تهيئة مهارة موظف جديدة
        
        المعاملات:
            employee_skill_id: معرف مهارة الموظف
            employee_id: معرف الموظف
            skill_id: معرف المهارة
            proficiency_level: مستوى الإتقان (1-5)
            years_of_experience: سنوات الخبرة
            certification: شهادة
            notes: ملاحظات
            creation_date: تاريخ الإنشاء
        """
        self.employee_skill_id = employee_skill_id
        self.employee_id = employee_id
        self.skill_id = skill_id
        
        # التحقق من مستوى الإتقان وضبطه ضمن النطاق المسموح (1-5)
        if proficiency_level < 1:
            self.proficiency_level = 1
        elif proficiency_level > 5:
            self.proficiency_level = 5
        else:
            self.proficiency_level = proficiency_level
        
        self.years_of_experience = years_of_experience
        self.certification = certification
        self.notes = notes
        self.creation_date = creation_date or datetime.now()
        self.skill: Optional[Skill] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EmployeeSkill':
        """
        إنشاء كائن مهارة موظف من قاموس
        
        المعاملات:
            data: قاموس يحتوي على بيانات مهارة الموظف
            
        العائد:
            كائن مهارة موظف جديد
        """
        # تحويل تاريخ الإنشاء إلى كائن datetime إذا كان موجوداً
        creation_date = data.get('creation_date')
        if isinstance(creation_date, str):
            creation_date = datetime.fromisoformat(creation_date)
        
        employee_skill = cls(
            employee_skill_id=data.get('employee_skill_id', str(uuid.uuid4())),
            employee_id=data.get('employee_id', ''),
            skill_id=data.get('skill_id', ''),
            proficiency_level=data.get('proficiency_level', 1),
            years_of_experience=data.get('years_of_experience'),
            certification=data.get('certification'),
            notes=data.get('notes'),
            creation_date=creation_date
        )
        
        # إضافة كائن المهارة إذا كان موجوداً في البيانات
        if 'skill' in data and data['skill']:
            employee_skill.skill = Skill.from_dict(data['skill'])
        
        return employee_skill
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل كائن مهارة الموظف إلى قاموس
        
        العائد:
            قاموس يحتوي على بيانات مهارة الموظف
        """
        result = {
            'employee_skill_id': self.employee_skill_id,
            'employee_id': self.employee_id,
            'skill_id': self.skill_id,
            'proficiency_level': self.proficiency_level,
            'years_of_experience': self.years_of_experience,
            'certification': self.certification,
            'notes': self.notes,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None
        }
        
        # إضافة بيانات المهارة إذا كانت موجودة
        if hasattr(self, 'skill') and self.skill:
            result['skill'] = self.skill.to_dict()
        
        return result


class Payroll:
    """كشف رواتب"""
    
    def __init__(
        self,
        payroll_id: str,
        employee_id: str,
        period_start: date,
        period_end: date,
        basic_salary: float,
        allowances: Optional[float] = 0.0,
        deductions: Optional[float] = 0.0,
        overtime_pay: Optional[float] = 0.0,
        bonus: Optional[float] = 0.0,
        tax: Optional[float] = 0.0,
        net_salary: Optional[float] = None,
        payment_date: Optional[date] = None,
        payment_method: Optional[str] = None,
        status: str = "قيد الإعداد",
        notes: Optional[str] = None,
        creation_date: datetime = None
    ):
        """
        تهيئة كشف رواتب جديد
        
        المعاملات:
            payroll_id: معرف كشف الرواتب
            employee_id: معرف الموظف
            period_start: تاريخ بداية الفترة
            period_end: تاريخ نهاية الفترة
            basic_salary: الراتب الأساسي
            allowances: البدلات
            deductions: الاستقطاعات
            overtime_pay: أجر العمل الإضافي
            bonus: المكافآت
            tax: الضريبة
            net_salary: صافي الراتب
            payment_date: تاريخ الدفع
            payment_method: طريقة الدفع
            status: حالة كشف الرواتب
            notes: ملاحظات
            creation_date: تاريخ الإنشاء
        """
        self.payroll_id = payroll_id
        self.employee_id = employee_id
        self.period_start = period_start
        self.period_end = period_end
        self.basic_salary = basic_salary
        self.allowances = allowances or 0.0
        self.deductions = deductions or 0.0
        self.overtime_pay = overtime_pay or 0.0
        self.bonus = bonus or 0.0
        self.tax = tax or 0.0
        
        # حساب صافي الراتب إذا لم يتم تحديده
        if net_salary is None:
            self.net_salary = self.calculate_net_salary()
        else:
            self.net_salary = net_salary
        
        self.payment_date = payment_date
        self.payment_method = payment_method
        self.status = status
        self.notes = notes
        self.creation_date = creation_date or datetime.now()
    
    def calculate_net_salary(self) -> float:
        """
        حساب صافي الراتب
        
        العائد:
            صافي الراتب
        """
        return self.basic_salary + self.allowances + self.overtime_pay + self.bonus - self.deductions - self.tax
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Payroll':
        """
        إنشاء كائن كشف رواتب من قاموس
        
        المعاملات:
            data: قاموس يحتوي على بيانات كشف الرواتب
            
        العائد:
            كائن كشف رواتب جديد
        """
        # تحويل تواريخ الفترة إلى كائنات date إذا كانت موجودة
        period_start = data.get('period_start')
        if isinstance(period_start, str):
            period_start = date.fromisoformat(period_start)
        
        period_end = data.get('period_end')
        if isinstance(period_end, str):
            period_end = date.fromisoformat(period_end)
        
        # تحويل تاريخ الدفع إلى كائن date إذا كان موجوداً
        payment_date = data.get('payment_date')
        if isinstance(payment_date, str):
            payment_date = date.fromisoformat(payment_date)
        
        # تحويل تاريخ الإنشاء إلى كائن datetime إذا كان موجوداً
        creation_date = data.get('creation_date')
        if isinstance(creation_date, str):
            creation_date = datetime.fromisoformat(creation_date)
        
        return cls(
            payroll_id=data.get('payroll_id', str(uuid.uuid4())),
            employee_id=data.get('employee_id', ''),
            period_start=period_start or date.today().replace(day=1),
            period_end=period_end or date.today(),
            basic_salary=data.get('basic_salary', 0.0),
            allowances=data.get('allowances', 0.0),
            deductions=data.get('deductions', 0.0),
            overtime_pay=data.get('overtime_pay', 0.0),
            bonus=data.get('bonus', 0.0),
            tax=data.get('tax', 0.0),
            net_salary=data.get('net_salary'),
            payment_date=payment_date,
            payment_method=data.get('payment_method'),
            status=data.get('status', 'قيد الإعداد'),
            notes=data.get('notes'),
            creation_date=creation_date
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل كائن كشف الرواتب إلى قاموس
        
        العائد:
            قاموس يحتوي على بيانات كشف الرواتب
        """
        return {
            'payroll_id': self.payroll_id,
            'employee_id': self.employee_id,
            'period_start': self.period_start.isoformat() if self.period_start else None,
            'period_end': self.period_end.isoformat() if self.period_end else None,
            'basic_salary': self.basic_salary,
            'allowances': self.allowances,
            'deductions': self.deductions,
            'overtime_pay': self.overtime_pay,
            'bonus': self.bonus,
            'tax': self.tax,
            'net_salary': self.net_salary,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'payment_method': self.payment_method,
            'status': self.status,
            'notes': self.notes,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None
        }


class Recruitment:
    """عملية توظيف"""
    
    def __init__(
        self,
        recruitment_id: str,
        position_id: str,
        title: str,
        description: str,
        requirements: Optional[str] = None,
        status: str = "مفتوح",
        opening_date: date = None,
        closing_date: Optional[date] = None,
        department_id: Optional[str] = None,
        company_id: str = "",
        branch_id: Optional[str] = None,
        hiring_manager_id: Optional[str] = None,
        number_of_vacancies: int = 1,
        notes: Optional[str] = None,
        creation_date: datetime = None
    ):
        """
        تهيئة عملية توظيف جديدة
        
        المعاملات:
            recruitment_id: معرف عملية التوظيف
            position_id: معرف المنصب
            title: عنوان الوظيفة
            description: وصف الوظيفة
            requirements: متطلبات الوظيفة
            status: حالة عملية التوظيف
            opening_date: تاريخ فتح الوظيفة
            closing_date: تاريخ إغلاق الوظيفة
            department_id: معرف القسم
            company_id: معرف الشركة
            branch_id: معرف الفرع
            hiring_manager_id: معرف مدير التوظيف
            number_of_vacancies: عدد الوظائف الشاغرة
            notes: ملاحظات
            creation_date: تاريخ الإنشاء
        """
        self.recruitment_id = recruitment_id
        self.position_id = position_id
        self.title = title
        self.description = description
        self.requirements = requirements
        self.status = status
        self.opening_date = opening_date or date.today()
        self.closing_date = closing_date
        self.department_id = department_id
        self.company_id = company_id
        self.branch_id = branch_id
        self.hiring_manager_id = hiring_manager_id
        self.number_of_vacancies = number_of_vacancies
        self.notes = notes
        self.creation_date = creation_date or datetime.now()
        self.candidates: List['Candidate'] = []
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Recruitment':
        """
        إنشاء كائن عملية توظيف من قاموس
        
        المعاملات:
            data: قاموس يحتوي على بيانات عملية التوظيف
            
        العائد:
            كائن عملية توظيف جديد
        """
        # تحويل تواريخ الفتح والإغلاق إلى كائنات date إذا كانت موجودة
        opening_date = data.get('opening_date')
        if isinstance(opening_date, str):
            opening_date = date.fromisoformat(opening_date)
        
        closing_date = data.get('closing_date')
        if isinstance(closing_date, str):
            closing_date = date.fromisoformat(closing_date)
        
        # تحويل تاريخ الإنشاء إلى كائن datetime إذا كان موجوداً
        creation_date = data.get('creation_date')
        if isinstance(creation_date, str):
            creation_date = datetime.fromisoformat(creation_date)
        
        return cls(
            recruitment_id=data.get('recruitment_id', str(uuid.uuid4())),
            position_id=data.get('position_id', ''),
            title=data.get('title', ''),
            description=data.get('description', ''),
            requirements=data.get('requirements'),
            status=data.get('status', 'مفتوح'),
            opening_date=opening_date,
            closing_date=closing_date,
            department_id=data.get('department_id'),
            company_id=data.get('company_id', ''),
            branch_id=data.get('branch_id'),
            hiring_manager_id=data.get('hiring_manager_id'),
            number_of_vacancies=data.get('number_of_vacancies', 1),
            notes=data.get('notes'),
            creation_date=creation_date
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل كائن عملية التوظيف إلى قاموس
        
        العائد:
            قاموس يحتوي على بيانات عملية التوظيف
        """
        return {
            'recruitment_id': self.recruitment_id,
            'position_id': self.position_id,
            'title': self.title,
            'description': self.description,
            'requirements': self.requirements,
            'status': self.status,
            'opening_date': self.opening_date.isoformat() if self.opening_date else None,
            'closing_date': self.closing_date.isoformat() if self.closing_date else None,
            'department_id': self.department_id,
            'company_id': self.company_id,
            'branch_id': self.branch_id,
            'hiring_manager_id': self.hiring_manager_id,
            'number_of_vacancies': self.number_of_vacancies,
            'notes': self.notes,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None,
            'candidates': [candidate.to_dict() for candidate in self.candidates] if hasattr(self, 'candidates') and self.candidates else []
        }


class Candidate:
    """مرشح للوظيفة"""
    
    def __init__(
        self,
        candidate_id: str,
        recruitment_id: str,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        status: str = "جديد",
        application_date: date = None,
        resume_path: Optional[str] = None,
        cover_letter_path: Optional[str] = None,
        interview_date: Optional[datetime] = None,
        interview_notes: Optional[str] = None,
        evaluation: Optional[str] = None,
        rating: Optional[int] = None,
        notes: Optional[str] = None,
        creation_date: datetime = None
    ):
        """
        تهيئة مرشح جديد
        
        المعاملات:
            candidate_id: معرف المرشح
            recruitment_id: معرف عملية التوظيف
            first_name: الاسم الأول
            last_name: الاسم الأخير
            email: البريد الإلكتروني
            phone: رقم الهاتف
            status: حالة المرشح
            application_date: تاريخ التقديم
            resume_path: مسار السيرة الذاتية
            cover_letter_path: مسار خطاب التقديم
            interview_date: تاريخ المقابلة
            interview_notes: ملاحظات المقابلة
            evaluation: تقييم المرشح
            rating: تقييم المرشح (1-5)
            notes: ملاحظات
            creation_date: تاريخ الإنشاء
        """
        self.candidate_id = candidate_id
        self.recruitment_id = recruitment_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.status = status
        self.application_date = application_date or date.today()
        self.resume_path = resume_path
        self.cover_letter_path = cover_letter_path
        self.interview_date = interview_date
        self.interview_notes = interview_notes
        self.evaluation = evaluation
        
        # التحقق من التقييم وضبطه ضمن النطاق المسموح (1-5)
        if rating is not None:
            if rating < 1:
                self.rating = 1
            elif rating > 5:
                self.rating = 5
            else:
                self.rating = rating
        else:
            self.rating = None
        
        self.notes = notes
        self.creation_date = creation_date or datetime.now()
    
    @property
    def full_name(self) -> str:
        """
        الحصول على الاسم الكامل للمرشح
        
        العائد:
            الاسم الكامل
        """
        return f"{self.first_name} {self.last_name}"
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Candidate':
        """
        إنشاء كائن مرشح من قاموس
        
        المعاملات:
            data: قاموس يحتوي على بيانات المرشح
            
        العائد:
            كائن مرشح جديد
        """
        # تحويل تاريخ التقديم إلى كائن date إذا كان موجوداً
        application_date = data.get('application_date')
        if isinstance(application_date, str):
            application_date = date.fromisoformat(application_date)
        
        # تحويل تاريخ المقابلة إلى كائن datetime إذا كان موجوداً
        interview_date = data.get('interview_date')
        if isinstance(interview_date, str):
            interview_date = datetime.fromisoformat(interview_date)
        
        # تحويل تاريخ الإنشاء إلى كائن datetime إذا كان موجوداً
        creation_date = data.get('creation_date')
        if isinstance(creation_date, str):
            creation_date = datetime.fromisoformat(creation_date)
        
        return cls(
            candidate_id=data.get('candidate_id', str(uuid.uuid4())),
            recruitment_id=data.get('recruitment_id', ''),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            status=data.get('status', 'جديد'),
            application_date=application_date,
            resume_path=data.get('resume_path'),
            cover_letter_path=data.get('cover_letter_path'),
            interview_date=interview_date,
            interview_notes=data.get('interview_notes'),
            evaluation=data.get('evaluation'),
            rating=data.get('rating'),
            notes=data.get('notes'),
            creation_date=creation_date
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        تحويل كائن المرشح إلى قاموس
        
        العائد:
            قاموس يحتوي على بيانات المرشح
        """
        return {
            'candidate_id': self.candidate_id,
            'recruitment_id': self.recruitment_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'status': self.status,
            'application_date': self.application_date.isoformat() if self.application_date else None,
            'resume_path': self.resume_path,
            'cover_letter_path': self.cover_letter_path,
            'interview_date': self.interview_date.isoformat() if self.interview_date else None,
            'interview_notes': self.interview_notes,
            'evaluation': self.evaluation,
            'rating': self.rating,
            'notes': self.notes,
            'creation_date': self.creation_date.isoformat() if self.creation_date else None
        }
