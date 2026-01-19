"""
خدمات إدارة الموارد البشرية
يحتوي هذا الملف على تنفيذ خدمات إدارة الموارد البشرية
"""

import uuid
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional, Tuple, Union

from ..models.hr_models import (
    Department, JobPosition, Employee, Leave, Attendance, EmployeeDocument,
    Skill, EmployeeSkill, Payroll, Recruitment, Candidate,
    EmploymentType, EmployeeStatus, LeaveType, LeaveStatus, AttendanceStatus
)


class DepartmentService:
    """خدمة إدارة الأقسام"""
    
    def __init__(self, db_manager):
        """
        تهيئة خدمة إدارة الأقسام
        
        المعاملات:
            db_manager: مدير قاعدة البيانات
        """
        self.db_manager = db_manager
        
    def create_department(self, department_data: Dict[str, Any]) -> Department:
        """
        إنشاء قسم جديد
        
        المعاملات:
            department_data: بيانات القسم
            
        العائد:
            كائن القسم الجديد
        """
        # إنشاء معرف فريد للقسم
        department_id = str(uuid.uuid4())
        department_data['department_id'] = department_id
        
        # إنشاء كائن القسم
        department = Department.from_dict(department_data)
        
        # حفظ القسم في قاعدة البيانات
        self._save_department(department)
        
        return department
    
    def update_department(self, department_id: str, department_data: Dict[str, Any]) -> Optional[Department]:
        """
        تحديث بيانات قسم
        
        المعاملات:
            department_id: معرف القسم
            department_data: بيانات القسم المحدثة
            
        العائد:
            كائن القسم المحدث أو None إذا لم يتم العثور على القسم
        """
        # البحث عن القسم
        department = self.get_department(department_id)
        if not department:
            return None
        
        # تحديث بيانات القسم
        department_data['department_id'] = department_id
        updated_department = Department.from_dict(department_data)
        
        # الحفاظ على الموظفين الحاليين
        updated_department.employees = department.employees
        
        # حفظ القسم المحدث في قاعدة البيانات
        self._save_department(updated_department)
        
        return updated_department
    
    def delete_department(self, department_id: str) -> bool:
        """
        حذف قسم
        
        المعاملات:
            department_id: معرف القسم
            
        العائد:
            True إذا تم الحذف بنجاح، False إذا لم يتم العثور على القسم
        """
        # البحث عن القسم
        department = self.get_department(department_id)
        if not department:
            return False
        
        # التحقق من وجود أقسام فرعية
        sub_departments = self.get_sub_departments(department_id)
        if sub_departments:
            # تحديث الأقسام الفرعية لتكون تابعة للقسم الأب للقسم المحذوف
            for sub_department in sub_departments:
                sub_department.parent_department_id = department.parent_department_id
                self._save_department(sub_department)
        
        # حذف القسم من قاعدة البيانات
        query = "DELETE FROM departments WHERE department_id = %s"
        self.db_manager.execute_query(query, (department_id,))
        
        return True
    
    def get_department(self, department_id: str) -> Optional[Department]:
        """
        الحصول على قسم بواسطة المعرف
        
        المعاملات:
            department_id: معرف القسم
            
        العائد:
            كائن القسم أو None إذا لم يتم العثور على القسم
        """
        # استعلام قاعدة البيانات للحصول على القسم
        query = "SELECT * FROM departments WHERE department_id = %s"
        result = self.db_manager.execute_query(query, (department_id,))
        
        if not result:
            return None
        
        # إنشاء كائن القسم
        department_data = result[0]
        department = Department.from_dict(department_data)
        
        # إضافة الموظفين
        department.employees = self._get_department_employees(department_id)
        
        return department
    
    def get_all_departments(self, company_id: Optional[str] = None, branch_id: Optional[str] = None) -> List[Department]:
        """
        الحصول على جميع الأقسام
        
        المعاملات:
            company_id: معرف الشركة (اختياري)
            branch_id: معرف الفرع (اختياري)
            
        العائد:
            قائمة بكائنات الأقسام
        """
        # بناء استعلام قاعدة البيانات
        query = "SELECT * FROM departments"
        params = []
        
        if company_id and branch_id:
            query += " WHERE company_id = %s AND branch_id = %s"
            params = [company_id, branch_id]
        elif company_id:
            query += " WHERE company_id = %s"
            params = [company_id]
        elif branch_id:
            query += " WHERE branch_id = %s"
            params = [branch_id]
        
        # تنفيذ الاستعلام
        results = self.db_manager.execute_query(query, tuple(params))
        
        # إنشاء قائمة الأقسام
        departments = []
        for department_data in results:
            department = Department.from_dict(department_data)
            department.employees = self._get_department_employees(department.department_id)
            departments.append(department)
        
        return departments
    
    def get_department_hierarchy(self, company_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        الحصول على التسلسل الهرمي للأقسام
        
        المعاملات:
            company_id: معرف الشركة (اختياري)
            
        العائد:
            قائمة بالأقسام الرئيسية مع الأقسام الفرعية
        """
        # الحصول على جميع الأقسام
        all_departments = self.get_all_departments(company_id)
        
        # تنظيم الأقسام في هيكل هرمي
        department_map = {dept.department_id: {"department": dept, "children": []} for dept in all_departments}
        
        # بناء الهيكل الهرمي
        root_departments = []
        for dept_id, dept_info in department_map.items():
            department = dept_info["department"]
            if department.parent_department_id and department.parent_department_id in department_map:
                # إضافة القسم كقسم فرعي للقسم الأب
                department_map[department.parent_department_id]["children"].append(dept_info)
            else:
                # إضافة القسم كقسم رئيسي
                root_departments.append(dept_info)
        
        # تحويل الهيكل الهرمي إلى قاموس
        return self._convert_hierarchy_to_dict(root_departments)
    
    def get_sub_departments(self, department_id: str) -> List[Department]:
        """
        الحصول على الأقسام الفرعية لقسم معين
        
        المعاملات:
            department_id: معرف القسم
            
        العائد:
            قائمة بالأقسام الفرعية
        """
        # استعلام قاعدة البيانات للحصول على الأقسام الفرعية
        query = "SELECT * FROM departments WHERE parent_department_id = %s"
        results = self.db_manager.execute_query(query, (department_id,))
        
        # إنشاء قائمة الأقسام الفرعية
        sub_departments = []
        for department_data in results:
            department = Department.from_dict(department_data)
            department.employees = self._get_department_employees(department.department_id)
            sub_departments.append(department)
        
        return sub_departments
    
    def get_department_statistics(self, department_id: str) -> Dict[str, Any]:
        """
        الحصول على إحصائيات القسم
        
        المعاملات:
            department_id: معرف القسم
            
        العائد:
            قاموس يحتوي على إحصائيات القسم
        """
        # الحصول على القسم
        department = self.get_department(department_id)
        if not department:
            return {}
        
        # الحصول على الأقسام الفرعية
        sub_departments = self.get_sub_departments(department_id)
        
        # حساب عدد الموظفين
        employee_count = len(department.employees)
        
        # حساب عدد الموظفين في الأقسام الفرعية
        sub_department_employee_count = sum(len(sub_dept.employees) for sub_dept in sub_departments)
        
        # حساب عدد الموظفين حسب الحالة
        employees_by_status = {}
        for employee in department.employees:
            status = employee.status.value if isinstance(employee.status, EmployeeStatus) else employee.status
            if status in employees_by_status:
                employees_by_status[status] += 1
            else:
                employees_by_status[status] = 1
        
        # حساب عدد الموظفين حسب نوع التوظيف
        employees_by_type = {}
        for employee in department.employees:
            emp_type = employee.employment_type.value if isinstance(employee.employment_type, EmploymentType) else employee.employment_type
            if emp_type in employees_by_type:
                employees_by_type[emp_type] += 1
            else:
                employees_by_type[emp_type] = 1
        
        # إنشاء قاموس الإحصائيات
        statistics = {
            "department_id": department_id,
            "department_name": department.name,
            "employee_count": employee_count,
            "sub_department_count": len(sub_departments),
            "sub_department_employee_count": sub_department_employee_count,
            "total_employee_count": employee_count + sub_department_employee_count,
            "employees_by_status": employees_by_status,
            "employees_by_type": employees_by_type
        }
        
        return statistics
    
    def _save_department(self, department: Department) -> None:
        """
        حفظ القسم في قاعدة البيانات
        
        المعاملات:
            department: كائن القسم
        """
        # تحويل كائن القسم إلى قاموس
        department_dict = department.to_dict()
        
        # حذف الموظفين من القاموس
        department_dict.pop('employees', None)
        
        # بناء استعلام الإدراج أو التحديث
        columns = ', '.join(department_dict.keys())
        placeholders = ', '.join(['%s'] * len(department_dict))
        values = tuple(department_dict.values())
        
        # تنفيذ استعلام الإدراج أو التحديث
        query = f"""
        INSERT INTO departments ({columns})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE
        {', '.join([f'{col} = VALUES({col})' for col in department_dict.keys() if col != 'department_id'])}
        """
        
        self.db_manager.execute_query(query, values)
    
    def _get_department_employees(self, department_id: str) -> List[Employee]:
        """
        الحصول على موظفي القسم
        
        المعاملات:
            department_id: معرف القسم
            
        العائد:
            قائمة بكائنات الموظفين
        """
        # استعلام قاعدة البيانات للحصول على موظفي القسم
        query = "SELECT * FROM employees WHERE department_id = %s"
        results = self.db_manager.execute_query(query, (department_id,))
        
        # إنشاء قائمة الموظفين
        employees = []
        for employee_data in results:
            employee = Employee.from_dict(employee_data)
            employees.append(employee)
        
        return employees
    
    def _convert_hierarchy_to_dict(self, departments_hierarchy: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        تحويل الهيكل الهرمي للأقسام إلى قاموس
        
        المعاملات:
            departments_hierarchy: الهيكل الهرمي للأقسام
            
        العائد:
            قائمة بالأقسام الرئيسية مع الأقسام الفرعية كقواميس
        """
        result = []
        for dept_info in departments_hierarchy:
            department = dept_info["department"]
            children = dept_info["children"]
            
            dept_dict = department.to_dict()
            if children:
                dept_dict["children"] = self._convert_hierarchy_to_dict(children)
            else:
                dept_dict["children"] = []
            
            result.append(dept_dict)
        
        return result


class JobPositionService:
    """خدمة إدارة المناصب الوظيفية"""
    
    def __init__(self, db_manager):
        """
        تهيئة خدمة إدارة المناصب الوظيفية
        
        المعاملات:
            db_manager: مدير قاعدة البيانات
        """
        self.db_manager = db_manager
        
    def create_job_position(self, position_data: Dict[str, Any]) -> JobPosition:
        """
        إنشاء منصب وظيفي جديد
        
        المعاملات:
            position_data: بيانات المنصب
            
        العائد:
            كائن المنصب الوظيفي الجديد
        """
        # إنشاء معرف فريد للمنصب
        position_id = str(uuid.uuid4())
        position_data['position_id'] = position_id
        
        # إنشاء كائن المنصب الوظيفي
        position = JobPosition.from_dict(position_data)
        
        # حفظ المنصب الوظيفي في قاعدة البيانات
        self._save_job_position(position)
        
        return position
    
    def update_job_position(self, position_id: str, position_data: Dict[str, Any]) -> Optional[JobPosition]:
        """
        تحديث بيانات منصب وظيفي
        
        المعاملات:
            position_id: معرف المنصب
            position_data: بيانات المنصب المحدثة
            
        العائد:
            كائن المنصب الوظيفي المحدث أو None إذا لم يتم العثور على المنصب
        """
        # البحث عن المنصب
        position = self.get_job_position(position_id)
        if not position:
            return None
        
        # تحديث بيانات المنصب
        position_data['position_id'] = position_id
        updated_position = JobPosition.from_dict(position_data)
        
        # حفظ المنصب المحدث في قاعدة البيانات
        self._save_job_position(updated_position)
        
        return updated_position
    
    def delete_job_position(self, position_id: str) -> bool:
        """
        حذف منصب وظيفي
        
        المعاملات:
            position_id: معرف المنصب
            
        العائد:
            True إذا تم الحذف بنجاح، False إذا لم يتم العثور على المنصب
        """
        # البحث عن المنصب
        position = self.get_job_position(position_id)
        if not position:
            return False
        
        # حذف المنصب من قاعدة البيانات
        query = "DELETE FROM job_positions WHERE position_id = %s"
        self.db_manager.execute_query(query, (position_id,))
        
        return True
    
    def get_job_position(self, position_id: str) -> Optional[JobPosition]:
        """
        الحصول على منصب وظيفي بواسطة المعرف
        
        المعاملات:
            position_id: معرف المنصب
            
        العائد:
            كائن المنصب الوظيفي أو None إذا لم يتم العثور على المنصب
        """
        # استعلام قاعدة البيانات للحصول على المنصب
        query = "SELECT * FROM job_positions WHERE position_id = %s"
        result = self.db_manager.execute_query(query, (position_id,))
        
        if not result:
            return None
        
        # إنشاء كائن المنصب الوظيفي
        position_data = result[0]
        position = JobPosition.from_dict(position_data)
        
        return position
    
    def get_all_job_positions(self, department_id: Optional[str] = None, company_id: Optional[str] = None) -> List[JobPosition]:
        """
        الحصول على جميع المناصب الوظيفية
        
        المعاملات:
            department_id: معرف القسم (اختياري)
            company_id: معرف الشركة (اختياري)
            
        العائد:
            قائمة بكائنات المناصب الوظيفية
        """
        # بناء استعلام قاعدة البيانات
        query = "SELECT * FROM job_positions"
        params = []
        
        if department_id and company_id:
            query += " WHERE department_id = %s AND company_id = %s"
            params = [department_id, company_id]
        elif department_id:
            query += " WHERE department_id = %s"
            params = [department_id]
        elif company_id:
            query += " WHERE company_id = %s"
            params = [company_id]
        
        # تنفيذ الاستعلام
        results = self.db_manager.execute_query(query, tuple(params))
        
        # إنشاء قائمة المناصب الوظيفية
        positions = []
        for position_data in results:
            position = JobPosition.from_dict(position_data)
            positions.append(position)
        
        return positions
    
    def _save_job_position(self, position: JobPosition) -> None:
        """
        حفظ المنصب الوظيفي في قاعدة البيانات
        
        المعاملات:
            position: كائن المنصب الوظيفي
        """
        # تحويل كائن المنصب الوظيفي إلى قاموس
        position_dict = position.to_dict()
        
        # بناء استعلام الإدراج أو التحديث
        columns = ', '.join(position_dict.keys())
        placeholders = ', '.join(['%s'] * len(position_dict))
        values = tuple(position_dict.values())
        
        # تنفيذ استعلام الإدراج أو التحديث
        query = f"""
        INSERT INTO job_positions ({columns})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE
        {', '.join([f'{col} = VALUES({col})' for col in position_dict.keys() if col != 'position_id'])}
        """
        
        self.db_manager.execute_query(query, values)


class EmployeeService:
    """خدمة إدارة الموظفين"""
    
    def __init__(self, db_manager):
        """
        تهيئة خدمة إدارة الموظفين
        
        المعاملات:
            db_manager: مدير قاعدة البيانات
        """
        self.db_manager = db_manager
        
    def create_employee(self, employee_data: Dict[str, Any]) -> Employee:
        """
        إنشاء موظف جديد
        
        المعاملات:
            employee_data: بيانات الموظف
            
        العائد:
            كائن الموظف الجديد
        """
        # إنشاء معرف فريد للموظف
        employee_id = str(uuid.uuid4())
        employee_data['employee_id'] = employee_id
        
        # إنشاء كائن الموظف
        employee = Employee.from_dict(employee_data)
        
        # حفظ الموظف في قاعدة البيانات
        self._save_employee(employee)
        
        return employee
    
    def update_employee(self, employee_id: str, employee_data: Dict[str, Any]) -> Optional[Employee]:
        """
        تحديث بيانات موظف
        
        المعاملات:
            employee_id: معرف الموظف
            employee_data: بيانات الموظف المحدثة
            
        العائد:
            كائن الموظف المحدث أو None إذا لم يتم العثور على الموظف
        """
        # البحث عن الموظف
        employee = self.get_employee(employee_id)
        if not employee:
            return None
        
        # تحديث بيانات الموظف
        employee_data['employee_id'] = employee_id
        updated_employee = Employee.from_dict(employee_data)
        
        # الحفاظ على البيانات المرتبطة
        updated_employee.leaves = employee.leaves
        updated_employee.attendances = employee.attendances
        updated_employee.documents = employee.documents
        updated_employee.skills = employee.skills
        
        # حفظ الموظف المحدث في قاعدة البيانات
        self._save_employee(updated_employee)
        
        return updated_employee
    
    def delete_employee(self, employee_id: str) -> bool:
        """
        حذف موظف
        
        المعاملات:
            employee_id: معرف الموظف
            
        العائد:
            True إذا تم الحذف بنجاح، False إذا لم يتم العثور على الموظف
        """
        # البحث عن الموظف
        employee = self.get_employee(employee_id)
        if not employee:
            return False
        
        # حذف البيانات المرتبطة
        self._delete_employee_leaves(employee_id)
        self._delete_employee_attendances(employee_id)
        self._delete_employee_documents(employee_id)
        self._delete_employee_skills(employee_id)
        
        # حذف الموظف من قاعدة البيانات
        query = "DELETE FROM employees WHERE employee_id = %s"
        self.db_manager.execute_query(query, (employee_id,))
        
        return True
    
    def get_employee(self, employee_id: str) -> Optional[Employee]:
        """
        الحصول على موظف بواسطة المعرف
        
        المعاملات:
            employee_id: معرف الموظف
            
        العائد:
            كائن الموظف أو None إذا لم يتم العثور على الموظف
        """
        # استعلام قاعدة البيانات للحصول على الموظف
        query = "SELECT * FROM employees WHERE employee_id = %s"
        result = self.db_manager.execute_query(query, (employee_id,))
        
        if not result:
            return None
        
        # إنشاء كائن الموظف
        employee_data = result[0]
        employee = Employee.from_dict(employee_data)
        
        # إضافة البيانات المرتبطة
        employee.leaves = self._get_employee_leaves(employee_id)
        employee.attendances = self._get_employee_attendances(employee_id)
        employee.documents = self._get_employee_documents(employee_id)
        employee.skills = self._get_employee_skills(employee_id)
        
        return employee
    
    def get_all_employees(self, department_id: Optional[str] = None, company_id: Optional[str] = None, branch_id: Optional[str] = None) -> List[Employee]:
        """
        الحصول على جميع الموظفين
        
        المعاملات:
            department_id: معرف القسم (اختياري)
            company_id: معرف الشركة (اختياري)
            branch_id: معرف الفرع (اختياري)
            
        العائد:
            قائمة بكائنات الموظفين
        """
        # بناء استعلام قاعدة البيانات
        query = "SELECT * FROM employees"
        params = []
        
        conditions = []
        if department_id:
            conditions.append("department_id = %s")
            params.append(department_id)
        if company_id:
            conditions.append("company_id = %s")
            params.append(company_id)
        if branch_id:
            conditions.append("branch_id = %s")
            params.append(branch_id)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        # تنفيذ الاستعلام
        results = self.db_manager.execute_query(query, tuple(params))
        
        # إنشاء قائمة الموظفين
        employees = []
        for employee_data in results:
            employee = Employee.from_dict(employee_data)
            employees.append(employee)
        
        return employees
    
    def search_employees(self, search_term: str, company_id: Optional[str] = None) -> List[Employee]:
        """
        البحث عن موظفين
        
        المعاملات:
            search_term: مصطلح البحث
            company_id: معرف الشركة (اختياري)
            
        العائد:
            قائمة بكائنات الموظفين المطابقة
        """
        # بناء استعلام البحث
        query = """
        SELECT * FROM employees
        WHERE (first_name LIKE %s OR last_name LIKE %s OR email LIKE %s OR phone LIKE %s OR national_id LIKE %s)
        """
        params = [f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"]
        
        if company_id:
            query += " AND company_id = %s"
            params.append(company_id)
        
        # تنفيذ الاستعلام
        results = self.db_manager.execute_query(query, tuple(params))
        
        # إنشاء قائمة الموظفين
        employees = []
        for employee_data in results:
            employee = Employee.from_dict(employee_data)
            employees.append(employee)
        
        return employees
    
    def get_employee_by_email(self, email: str) -> Optional[Employee]:
        """
        الحصول على موظف بواسطة البريد الإلكتروني
        
        المعاملات:
            email: البريد الإلكتروني
            
        العائد:
            كائن الموظف أو None إذا لم يتم العثور على الموظف
        """
        # استعلام قاعدة البيانات للحصول على الموظف
        query = "SELECT * FROM employees WHERE email = %s"
        result = self.db_manager.execute_query(query, (email,))
        
        if not result:
            return None
        
        # إنشاء كائن الموظف
        employee_data = result[0]
        employee = Employee.from_dict(employee_data)
        
        # إضافة البيانات المرتبطة
        employee.leaves = self._get_employee_leaves(employee.employee_id)
        employee.attendances = self._get_employee_attendances(employee.employee_id)
        employee.documents = self._get_employee_documents(employee.employee_id)
        employee.skills = self._get_employee_skills(employee.employee_id)
        
        return employee
    
    def get_employee_by_national_id(self, national_id: str) -> Optional[Employee]:
        """
        الحصول على موظف بواسطة رقم الهوية الوطنية
        
        المعاملات:
            national_id: رقم الهوية الوطنية
            
        العائد:
            كائن الموظف أو None إذا لم يتم العثور على الموظف
        """
        # استعلام قاعدة البيانات للحصول على الموظف
        query = "SELECT * FROM employees WHERE national_id = %s"
        result = self.db_manager.execute_query(query, (national_id,))
        
        if not result:
            return None
        
        # إنشاء كائن الموظف
        employee_data = result[0]
        employee = Employee.from_dict(employee_data)
        
        # إضافة البيانات المرتبطة
        employee.leaves = self._get_employee_leaves(employee.employee_id)
        employee.attendances = self._get_employee_attendances(employee.employee_id)
        employee.documents = self._get_employee_documents(employee.employee_id)
        employee.skills = self._get_employee_skills(employee.employee_id)
        
        return employee
    
    def get_subordinates(self, manager_id: str) -> List[Employee]:
        """
        الحصول على المرؤوسين لمدير معين
        
        المعاملات:
            manager_id: معرف المدير
            
        العائد:
            قائمة بكائنات الموظفين المرؤوسين
        """
        # استعلام قاعدة البيانات للحصول على المرؤوسين
        query = "SELECT * FROM employees WHERE manager_id = %s"
        results = self.db_manager.execute_query(query, (manager_id,))
        
        # إنشاء قائمة المرؤوسين
        subordinates = []
        for employee_data in results:
            employee = Employee.from_dict(employee_data)
            subordinates.append(employee)
        
        return subordinates
    
    def add_employee_leave(self, leave_data: Dict[str, Any]) -> Leave:
        """
        إضافة إجازة لموظف
        
        المعاملات:
            leave_data: بيانات الإجازة
            
        العائد:
            كائن الإجازة الجديد
        """
        # إنشاء معرف فريد للإجازة
        leave_id = str(uuid.uuid4())
        leave_data['leave_id'] = leave_id
        
        # إنشاء كائن الإجازة
        leave = Leave.from_dict(leave_data)
        
        # حفظ الإجازة في قاعدة البيانات
        self._save_employee_leave(leave)
        
        return leave
    
    def update_employee_leave(self, leave_id: str, leave_data: Dict[str, Any]) -> Optional[Leave]:
        """
        تحديث إجازة موظف
        
        المعاملات:
            leave_id: معرف الإجازة
            leave_data: بيانات الإجازة المحدثة
            
        العائد:
            كائن الإجازة المحدث أو None إذا لم يتم العثور على الإجازة
        """
        # البحث عن الإجازة
        leave = self.get_employee_leave(leave_id)
        if not leave:
            return None
        
        # تحديث بيانات الإجازة
        leave_data['leave_id'] = leave_id
        leave_data['employee_id'] = leave.employee_id
        updated_leave = Leave.from_dict(leave_data)
        
        # حفظ الإجازة المحدثة في قاعدة البيانات
        self._save_employee_leave(updated_leave)
        
        return updated_leave
    
    def get_employee_leave(self, leave_id: str) -> Optional[Leave]:
        """
        الحصول على إجازة بواسطة المعرف
        
        المعاملات:
            leave_id: معرف الإجازة
            
        العائد:
            كائن الإجازة أو None إذا لم يتم العثور على الإجازة
        """
        # استعلام قاعدة البيانات للحصول على الإجازة
        query = "SELECT * FROM leaves WHERE leave_id = %s"
        result = self.db_manager.execute_query(query, (leave_id,))
        
        if not result:
            return None
        
        # إنشاء كائن الإجازة
        leave_data = result[0]
        leave = Leave.from_dict(leave_data)
        
        return leave
    
    def approve_leave(self, leave_id: str, approved_by: str, comments: Optional[str] = None) -> Optional[Leave]:
        """
        الموافقة على إجازة
        
        المعاملات:
            leave_id: معرف الإجازة
            approved_by: معرف الموظف الذي وافق على الإجازة
            comments: تعليقات (اختياري)
            
        العائد:
            كائن الإجازة المحدث أو None إذا لم يتم العثور على الإجازة
        """
        # البحث عن الإجازة
        leave = self.get_employee_leave(leave_id)
        if not leave:
            return None
        
        # تحديث حالة الإجازة
        leave.status = LeaveStatus.APPROVED
        leave.approved_by = approved_by
        leave.approval_date = datetime.now()
        if comments:
            leave.comments = comments
        
        # حفظ الإجازة المحدثة في قاعدة البيانات
        self._save_employee_leave(leave)
        
        return leave
    
    def reject_leave(self, leave_id: str, approved_by: str, comments: Optional[str] = None) -> Optional[Leave]:
        """
        رفض إجازة
        
        المعاملات:
            leave_id: معرف الإجازة
            approved_by: معرف الموظف الذي رفض الإجازة
            comments: تعليقات (اختياري)
            
        العائد:
            كائن الإجازة المحدث أو None إذا لم يتم العثور على الإجازة
        """
        # البحث عن الإجازة
        leave = self.get_employee_leave(leave_id)
        if not leave:
            return None
        
        # تحديث حالة الإجازة
        leave.status = LeaveStatus.REJECTED
        leave.approved_by = approved_by
        leave.approval_date = datetime.now()
        if comments:
            leave.comments = comments
        
        # حفظ الإجازة المحدثة في قاعدة البيانات
        self._save_employee_leave(leave)
        
        return leave
    
    def add_attendance(self, attendance_data: Dict[str, Any]) -> Attendance:
        """
        إضافة سجل حضور
        
        المعاملات:
            attendance_data: بيانات سجل الحضور
            
        العائد:
            كائن سجل الحضور الجديد
        """
        # إنشاء معرف فريد لسجل الحضور
        attendance_id = str(uuid.uuid4())
        attendance_data['attendance_id'] = attendance_id
        
        # إنشاء كائن سجل الحضور
        attendance = Attendance.from_dict(attendance_data)
        
        # حفظ سجل الحضور في قاعدة البيانات
        self._save_attendance(attendance)
        
        return attendance
    
    def update_attendance(self, attendance_id: str, attendance_data: Dict[str, Any]) -> Optional[Attendance]:
        """
        تحديث سجل حضور
        
        المعاملات:
            attendance_id: معرف سجل الحضور
            attendance_data: بيانات سجل الحضور المحدثة
            
        العائد:
            كائن سجل الحضور المحدث أو None إذا لم يتم العثور على سجل الحضور
        """
        # البحث عن سجل الحضور
        attendance = self.get_attendance(attendance_id)
        if not attendance:
            return None
        
        # تحديث بيانات سجل الحضور
        attendance_data['attendance_id'] = attendance_id
        attendance_data['employee_id'] = attendance.employee_id
        updated_attendance = Attendance.from_dict(attendance_data)
        
        # حفظ سجل الحضور المحدث في قاعدة البيانات
        self._save_attendance(updated_attendance)
        
        return updated_attendance
    
    def get_attendance(self, attendance_id: str) -> Optional[Attendance]:
        """
        الحصول على سجل حضور بواسطة المعرف
        
        المعاملات:
            attendance_id: معرف سجل الحضور
            
        العائد:
            كائن سجل الحضور أو None إذا لم يتم العثور على سجل الحضور
        """
        # استعلام قاعدة البيانات للحصول على سجل الحضور
        query = "SELECT * FROM attendances WHERE attendance_id = %s"
        result = self.db_manager.execute_query(query, (attendance_id,))
        
        if not result:
            return None
        
        # إنشاء كائن سجل الحضور
        attendance_data = result[0]
        attendance = Attendance.from_dict(attendance_data)
        
        return attendance
    
    def get_employee_attendance_by_date(self, employee_id: str, attendance_date: date) -> Optional[Attendance]:
        """
        الحصول على سجل حضور موظف في تاريخ معين
        
        المعاملات:
            employee_id: معرف الموظف
            attendance_date: تاريخ الحضور
            
        العائد:
            كائن سجل الحضور أو None إذا لم يتم العثور على سجل الحضور
        """
        # استعلام قاعدة البيانات للحصول على سجل الحضور
        query = "SELECT * FROM attendances WHERE employee_id = %s AND date = %s"
        result = self.db_manager.execute_query(query, (employee_id, attendance_date.isoformat()))
        
        if not result:
            return None
        
        # إنشاء كائن سجل الحضور
        attendance_data = result[0]
        attendance = Attendance.from_dict(attendance_data)
        
        return attendance
    
    def get_employee_attendance_report(self, employee_id: str, start_date: date, end_date: date) -> Dict[str, Any]:
        """
        الحصول على تقرير حضور موظف
        
        المعاملات:
            employee_id: معرف الموظف
            start_date: تاريخ البداية
            end_date: تاريخ النهاية
            
        العائد:
            قاموس يحتوي على تقرير الحضور
        """
        # الحصول على الموظف
        employee = self.get_employee(employee_id)
        if not employee:
            return {}
        
        # استعلام قاعدة البيانات للحصول على سجلات الحضور
        query = "SELECT * FROM attendances WHERE employee_id = %s AND date BETWEEN %s AND %s ORDER BY date"
        results = self.db_manager.execute_query(query, (employee_id, start_date.isoformat(), end_date.isoformat()))
        
        # إنشاء قائمة سجلات الحضور
        attendances = []
        for attendance_data in results:
            attendance = Attendance.from_dict(attendance_data)
            attendances.append(attendance)
        
        # حساب إحصائيات الحضور
        total_days = (end_date - start_date).days + 1
        present_days = sum(1 for a in attendances if a.status == AttendanceStatus.PRESENT)
        absent_days = sum(1 for a in attendances if a.status == AttendanceStatus.ABSENT)
        late_days = sum(1 for a in attendances if a.status == AttendanceStatus.LATE)
        half_days = sum(1 for a in attendances if a.status == AttendanceStatus.HALF_DAY)
        leave_days = sum(1 for a in attendances if a.status == AttendanceStatus.ON_LEAVE)
        
        # حساب ساعات العمل والتأخير والعمل الإضافي
        total_working_hours = sum(a.working_hours or 0 for a in attendances)
        total_late_hours = sum(a.late_hours or 0 for a in attendances)
        total_overtime_hours = sum(a.overtime_hours or 0 for a in attendances)
        
        # إنشاء قاموس التقرير
        report = {
            "employee_id": employee_id,
            "employee_name": employee.full_name,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "total_days": total_days,
            "present_days": present_days,
            "absent_days": absent_days,
            "late_days": late_days,
            "half_days": half_days,
            "leave_days": leave_days,
            "total_working_hours": total_working_hours,
            "total_late_hours": total_late_hours,
            "total_overtime_hours": total_overtime_hours,
            "attendance_rate": (present_days / total_days) * 100 if total_days > 0 else 0,
            "attendances": [attendance.to_dict() for attendance in attendances]
        }
        
        return report
    
    def add_employee_document(self, document_data: Dict[str, Any]) -> EmployeeDocument:
        """
        إضافة مستند لموظف
        
        المعاملات:
            document_data: بيانات المستند
            
        العائد:
            كائن المستند الجديد
        """
        # إنشاء معرف فريد للمستند
        document_id = str(uuid.uuid4())
        document_data['document_id'] = document_id
        
        # إنشاء كائن المستند
        document = EmployeeDocument.from_dict(document_data)
        
        # حفظ المستند في قاعدة البيانات
        self._save_employee_document(document)
        
        return document
    
    def update_employee_document(self, document_id: str, document_data: Dict[str, Any]) -> Optional[EmployeeDocument]:
        """
        تحديث مستند موظف
        
        المعاملات:
            document_id: معرف المستند
            document_data: بيانات المستند المحدثة
            
        العائد:
            كائن المستند المحدث أو None إذا لم يتم العثور على المستند
        """
        # البحث عن المستند
        document = self.get_employee_document(document_id)
        if not document:
            return None
        
        # تحديث بيانات المستند
        document_data['document_id'] = document_id
        document_data['employee_id'] = document.employee_id
        updated_document = EmployeeDocument.from_dict(document_data)
        
        # حفظ المستند المحدث في قاعدة البيانات
        self._save_employee_document(updated_document)
        
        return updated_document
    
    def get_employee_document(self, document_id: str) -> Optional[EmployeeDocument]:
        """
        الحصول على مستند بواسطة المعرف
        
        المعاملات:
            document_id: معرف المستند
            
        العائد:
            كائن المستند أو None إذا لم يتم العثور على المستند
        """
        # استعلام قاعدة البيانات للحصول على المستند
        query = "SELECT * FROM employee_documents WHERE document_id = %s"
        result = self.db_manager.execute_query(query, (document_id,))
        
        if not result:
            return None
        
        # إنشاء كائن المستند
        document_data = result[0]
        document = EmployeeDocument.from_dict(document_data)
        
        return document
    
    def add_employee_skill(self, skill_data: Dict[str, Any]) -> EmployeeSkill:
        """
        إضافة مهارة لموظف
        
        المعاملات:
            skill_data: بيانات المهارة
            
        العائد:
            كائن مهارة الموظف الجديد
        """
        # إنشاء معرف فريد لمهارة الموظف
        employee_skill_id = str(uuid.uuid4())
        skill_data['employee_skill_id'] = employee_skill_id
        
        # إنشاء كائن مهارة الموظف
        employee_skill = EmployeeSkill.from_dict(skill_data)
        
        # حفظ مهارة الموظف في قاعدة البيانات
        self._save_employee_skill(employee_skill)
        
        return employee_skill
    
    def update_employee_skill(self, employee_skill_id: str, skill_data: Dict[str, Any]) -> Optional[EmployeeSkill]:
        """
        تحديث مهارة موظف
        
        المعاملات:
            employee_skill_id: معرف مهارة الموظف
            skill_data: بيانات المهارة المحدثة
            
        العائد:
            كائن مهارة الموظف المحدث أو None إذا لم يتم العثور على المهارة
        """
        # البحث عن مهارة الموظف
        employee_skill = self.get_employee_skill(employee_skill_id)
        if not employee_skill:
            return None
        
        # تحديث بيانات مهارة الموظف
        skill_data['employee_skill_id'] = employee_skill_id
        skill_data['employee_id'] = employee_skill.employee_id
        skill_data['skill_id'] = employee_skill.skill_id
        updated_employee_skill = EmployeeSkill.from_dict(skill_data)
        
        # حفظ مهارة الموظف المحدثة في قاعدة البيانات
        self._save_employee_skill(updated_employee_skill)
        
        return updated_employee_skill
    
    def get_employee_skill(self, employee_skill_id: str) -> Optional[EmployeeSkill]:
        """
        الحصول على مهارة موظف بواسطة المعرف
        
        المعاملات:
            employee_skill_id: معرف مهارة الموظف
            
        العائد:
            كائن مهارة الموظف أو None إذا لم يتم العثور على المهارة
        """
        # استعلام قاعدة البيانات للحصول على مهارة الموظف
        query = "SELECT * FROM employee_skills WHERE employee_skill_id = %s"
        result = self.db_manager.execute_query(query, (employee_skill_id,))
        
        if not result:
            return None
        
        # إنشاء كائن مهارة الموظف
        employee_skill_data = result[0]
        employee_skill = EmployeeSkill.from_dict(employee_skill_data)
        
        # إضافة كائن المهارة
        skill_service = SkillService(self.db_manager)
        employee_skill.skill = skill_service.get_skill(employee_skill.skill_id)
        
        return employee_skill
    
    def _save_employee(self, employee: Employee) -> None:
        """
        حفظ الموظف في قاعدة البيانات
        
        المعاملات:
            employee: كائن الموظف
        """
        # تحويل كائن الموظف إلى قاموس
        employee_dict = employee.to_dict()
        
        # حذف البيانات المرتبطة من القاموس
        employee_dict.pop('leaves', None)
        employee_dict.pop('attendances', None)
        employee_dict.pop('documents', None)
        employee_dict.pop('skills', None)
        employee_dict.pop('full_name', None)
        
        # بناء استعلام الإدراج أو التحديث
        columns = ', '.join(employee_dict.keys())
        placeholders = ', '.join(['%s'] * len(employee_dict))
        values = tuple(employee_dict.values())
        
        # تنفيذ استعلام الإدراج أو التحديث
        query = f"""
        INSERT INTO employees ({columns})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE
        {', '.join([f'{col} = VALUES({col})' for col in employee_dict.keys() if col != 'employee_id'])}
        """
        
        self.db_manager.execute_query(query, values)
    
    def _save_employee_leave(self, leave: Leave) -> None:
        """
        حفظ إجازة موظف في قاعدة البيانات
        
        المعاملات:
            leave: كائن الإجازة
        """
        # تحويل كائن الإجازة إلى قاموس
        leave_dict = leave.to_dict()
        
        # حذف الحقول المحسوبة من القاموس
        leave_dict.pop('duration', None)
        
        # بناء استعلام الإدراج أو التحديث
        columns = ', '.join(leave_dict.keys())
        placeholders = ', '.join(['%s'] * len(leave_dict))
        values = tuple(leave_dict.values())
        
        # تنفيذ استعلام الإدراج أو التحديث
        query = f"""
        INSERT INTO leaves ({columns})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE
        {', '.join([f'{col} = VALUES({col})' for col in leave_dict.keys() if col != 'leave_id'])}
        """
        
        self.db_manager.execute_query(query, values)
    
    def _save_attendance(self, attendance: Attendance) -> None:
        """
        حفظ سجل حضور في قاعدة البيانات
        
        المعاملات:
            attendance: كائن سجل الحضور
        """
        # تحويل كائن سجل الحضور إلى قاموس
        attendance_dict = attendance.to_dict()
        
        # بناء استعلام الإدراج أو التحديث
        columns = ', '.join(attendance_dict.keys())
        placeholders = ', '.join(['%s'] * len(attendance_dict))
        values = tuple(attendance_dict.values())
        
        # تنفيذ استعلام الإدراج أو التحديث
        query = f"""
        INSERT INTO attendances ({columns})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE
        {', '.join([f'{col} = VALUES({col})' for col in attendance_dict.keys() if col != 'attendance_id'])}
        """
        
        self.db_manager.execute_query(query, values)
    
    def _save_employee_document(self, document: EmployeeDocument) -> None:
        """
        حفظ مستند موظف في قاعدة البيانات
        
        المعاملات:
            document: كائن المستند
        """
        # تحويل كائن المستند إلى قاموس
        document_dict = document.to_dict()
        
        # بناء استعلام الإدراج أو التحديث
        columns = ', '.join(document_dict.keys())
        placeholders = ', '.join(['%s'] * len(document_dict))
        values = tuple(document_dict.values())
        
        # تنفيذ استعلام الإدراج أو التحديث
        query = f"""
        INSERT INTO employee_documents ({columns})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE
        {', '.join([f'{col} = VALUES({col})' for col in document_dict.keys() if col != 'document_id'])}
        """
        
        self.db_manager.execute_query(query, values)
    
    def _save_employee_skill(self, employee_skill: EmployeeSkill) -> None:
        """
        حفظ مهارة موظف في قاعدة البيانات
        
        المعاملات:
            employee_skill: كائن مهارة الموظف
        """
        # تحويل كائن مهارة الموظف إلى قاموس
        employee_skill_dict = employee_skill.to_dict()
        
        # حذف كائن المهارة من القاموس
        employee_skill_dict.pop('skill', None)
        
        # بناء استعلام الإدراج أو التحديث
        columns = ', '.join(employee_skill_dict.keys())
        placeholders = ', '.join(['%s'] * len(employee_skill_dict))
        values = tuple(employee_skill_dict.values())
        
        # تنفيذ استعلام الإدراج أو التحديث
        query = f"""
        INSERT INTO employee_skills ({columns})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE
        {', '.join([f'{col} = VALUES({col})' for col in employee_skill_dict.keys() if col != 'employee_skill_id'])}
        """
        
        self.db_manager.execute_query(query, values)
    
    def _get_employee_leaves(self, employee_id: str) -> List[Leave]:
        """
        الحصول على إجازات الموظف
        
        المعاملات:
            employee_id: معرف الموظف
            
        العائد:
            قائمة بكائنات الإجازات
        """
        # استعلام قاعدة البيانات للحصول على إجازات الموظف
        query = "SELECT * FROM leaves WHERE employee_id = %s"
        results = self.db_manager.execute_query(query, (employee_id,))
        
        # إنشاء قائمة الإجازات
        leaves = []
        for leave_data in results:
            leave = Leave.from_dict(leave_data)
            leaves.append(leave)
        
        return leaves
    
    def _get_employee_attendances(self, employee_id: str) -> List[Attendance]:
        """
        الحصول على سجلات حضور الموظف
        
        المعاملات:
            employee_id: معرف الموظف
            
        العائد:
            قائمة بكائنات سجلات الحضور
        """
        # استعلام قاعدة البيانات للحصول على سجلات حضور الموظف
        query = "SELECT * FROM attendances WHERE employee_id = %s"
        results = self.db_manager.execute_query(query, (employee_id,))
        
        # إنشاء قائمة سجلات الحضور
        attendances = []
        for attendance_data in results:
            attendance = Attendance.from_dict(attendance_data)
            attendances.append(attendance)
        
        return attendances
    
    def _get_employee_documents(self, employee_id: str) -> List[EmployeeDocument]:
        """
        الحصول على مستندات الموظف
        
        المعاملات:
            employee_id: معرف الموظف
            
        العائد:
            قائمة بكائنات المستندات
        """
        # استعلام قاعدة البيانات للحصول على مستندات الموظف
        query = "SELECT * FROM employee_documents WHERE employee_id = %s"
        results = self.db_manager.execute_query(query, (employee_id,))
        
        # إنشاء قائمة المستندات
        documents = []
        for document_data in results:
            document = EmployeeDocument.from_dict(document_data)
            documents.append(document)
        
        return documents
    
    def _get_employee_skills(self, employee_id: str) -> List[EmployeeSkill]:
        """
        الحصول على مهارات الموظف
        
        المعاملات:
            employee_id: معرف الموظف
            
        العائد:
            قائمة بكائنات مهارات الموظف
        """
        # استعلام قاعدة البيانات للحصول على مهارات الموظف
        query = "SELECT * FROM employee_skills WHERE employee_id = %s"
        results = self.db_manager.execute_query(query, (employee_id,))
        
        # إنشاء قائمة مهارات الموظف
        employee_skills = []
        for employee_skill_data in results:
            employee_skill = EmployeeSkill.from_dict(employee_skill_data)
            
            # إضافة كائن المهارة
            skill_service = SkillService(self.db_manager)
            employee_skill.skill = skill_service.get_skill(employee_skill.skill_id)
            
            employee_skills.append(employee_skill)
        
        return employee_skills
    
    def _delete_employee_leaves(self, employee_id: str) -> None:
        """
        حذف إجازات الموظف
        
        المعاملات:
            employee_id: معرف الموظف
        """
        # حذف إجازات الموظف
        query = "DELETE FROM leaves WHERE employee_id = %s"
        self.db_manager.execute_query(query, (employee_id,))
    
    def _delete_employee_attendances(self, employee_id: str) -> None:
        """
        حذف سجلات حضور الموظف
        
        المعاملات:
            employee_id: معرف الموظف
        """
        # حذف سجلات حضور الموظف
        query = "DELETE FROM attendances WHERE employee_id = %s"
        self.db_manager.execute_query(query, (employee_id,))
    
    def _delete_employee_documents(self, employee_id: str) -> None:
        """
        حذف مستندات الموظف
        
        المعاملات:
            employee_id: معرف الموظف
        """
        # حذف مستندات الموظف
        query = "DELETE FROM employee_documents WHERE employee_id = %s"
        self.db_manager.execute_query(query, (employee_id,))
    
    def _delete_employee_skills(self, employee_id: str) -> None:
        """
        حذف مهارات الموظف
        
        المعاملات:
            employee_id: معرف الموظف
        """
        # حذف مهارات الموظف
        query = "DELETE FROM employee_skills WHERE employee_id = %s"
        self.db_manager.execute_query(query, (employee_id,))


class SkillService:
    """خدمة إدارة المهارات"""
    
    def __init__(self, db_manager):
        """
        تهيئة خدمة إدارة المهارات
        
        المعاملات:
            db_manager: مدير قاعدة البيانات
        """
        self.db_manager = db_manager
        
    def create_skill(self, skill_data: Dict[str, Any]) -> Skill:
        """
        إنشاء مهارة جديدة
        
        المعاملات:
            skill_data: بيانات المهارة
            
        العائد:
            كائن المهارة الجديد
        """
        # إنشاء معرف فريد للمهارة
        skill_id = str(uuid.uuid4())
        skill_data['skill_id'] = skill_id
        
        # إنشاء كائن المهارة
        skill = Skill.from_dict(skill_data)
        
        # حفظ المهارة في قاعدة البيانات
        self._save_skill(skill)
        
        return skill
    
    def update_skill(self, skill_id: str, skill_data: Dict[str, Any]) -> Optional[Skill]:
        """
        تحديث بيانات مهارة
        
        المعاملات:
            skill_id: معرف المهارة
            skill_data: بيانات المهارة المحدثة
            
        العائد:
            كائن المهارة المحدث أو None إذا لم يتم العثور على المهارة
        """
        # البحث عن المهارة
        skill = self.get_skill(skill_id)
        if not skill:
            return None
        
        # تحديث بيانات المهارة
        skill_data['skill_id'] = skill_id
        updated_skill = Skill.from_dict(skill_data)
        
        # حفظ المهارة المحدثة في قاعدة البيانات
        self._save_skill(updated_skill)
        
        return updated_skill
    
    def delete_skill(self, skill_id: str) -> bool:
        """
        حذف مهارة
        
        المعاملات:
            skill_id: معرف المهارة
            
        العائد:
            True إذا تم الحذف بنجاح، False إذا لم يتم العثور على المهارة
        """
        # البحث عن المهارة
        skill = self.get_skill(skill_id)
        if not skill:
            return False
        
        # حذف المهارة من قاعدة البيانات
        query = "DELETE FROM skills WHERE skill_id = %s"
        self.db_manager.execute_query(query, (skill_id,))
        
        return True
    
    def get_skill(self, skill_id: str) -> Optional[Skill]:
        """
        الحصول على مهارة بواسطة المعرف
        
        المعاملات:
            skill_id: معرف المهارة
            
        العائد:
            كائن المهارة أو None إذا لم يتم العثور على المهارة
        """
        # استعلام قاعدة البيانات للحصول على المهارة
        query = "SELECT * FROM skills WHERE skill_id = %s"
        result = self.db_manager.execute_query(query, (skill_id,))
        
        if not result:
            return None
        
        # إنشاء كائن المهارة
        skill_data = result[0]
        skill = Skill.from_dict(skill_data)
        
        return skill
    
    def get_all_skills(self, company_id: Optional[str] = None, category: Optional[str] = None) -> List[Skill]:
        """
        الحصول على جميع المهارات
        
        المعاملات:
            company_id: معرف الشركة (اختياري)
            category: فئة المهارة (اختياري)
            
        العائد:
            قائمة بكائنات المهارات
        """
        # بناء استعلام قاعدة البيانات
        query = "SELECT * FROM skills"
        params = []
        
        conditions = []
        if company_id:
            conditions.append("company_id = %s")
            params.append(company_id)
        if category:
            conditions.append("category = %s")
            params.append(category)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        # تنفيذ الاستعلام
        results = self.db_manager.execute_query(query, tuple(params))
        
        # إنشاء قائمة المهارات
        skills = []
        for skill_data in results:
            skill = Skill.from_dict(skill_data)
            skills.append(skill)
        
        return skills
    
    def get_skill_categories(self, company_id: Optional[str] = None) -> List[str]:
        """
        الحصول على فئات المهارات
        
        المعاملات:
            company_id: معرف الشركة (اختياري)
            
        العائد:
            قائمة بفئات المهارات
        """
        # بناء استعلام قاعدة البيانات
        query = "SELECT DISTINCT category FROM skills WHERE category IS NOT NULL"
        params = []
        
        if company_id:
            query += " AND company_id = %s"
            params.append(company_id)
        
        # تنفيذ الاستعلام
        results = self.db_manager.execute_query(query, tuple(params))
        
        # إنشاء قائمة فئات المهارات
        categories = [result['category'] for result in results]
        
        return categories
    
    def _save_skill(self, skill: Skill) -> None:
        """
        حفظ المهارة في قاعدة البيانات
        
        المعاملات:
            skill: كائن المهارة
        """
        # تحويل كائن المهارة إلى قاموس
        skill_dict = skill.to_dict()
        
        # بناء استعلام الإدراج أو التحديث
        columns = ', '.join(skill_dict.keys())
        placeholders = ', '.join(['%s'] * len(skill_dict))
        values = tuple(skill_dict.values())
        
        # تنفيذ استعلام الإدراج أو التحديث
        query = f"""
        INSERT INTO skills ({columns})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE
        {', '.join([f'{col} = VALUES({col})' for col in skill_dict.keys() if col != 'skill_id'])}
        """
        
        self.db_manager.execute_query(query, values)


class PayrollService:
    """خدمة إدارة كشوف الرواتب"""
    
    def __init__(self, db_manager):
        """
        تهيئة خدمة إدارة كشوف الرواتب
        
        المعاملات:
            db_manager: مدير قاعدة البيانات
        """
        self.db_manager = db_manager
        
    def create_payroll(self, payroll_data: Dict[str, Any]) -> Payroll:
        """
        إنشاء كشف رواتب جديد
        
        المعاملات:
            payroll_data: بيانات كشف الرواتب
            
        العائد:
            كائن كشف الرواتب الجديد
        """
        # إنشاء معرف فريد لكشف الرواتب
        payroll_id = str(uuid.uuid4())
        payroll_data['payroll_id'] = payroll_id
        
        # إنشاء كائن كشف الرواتب
        payroll = Payroll.from_dict(payroll_data)
        
        # حفظ كشف الرواتب في قاعدة البيانات
        self._save_payroll(payroll)
        
        return payroll
    
    def update_payroll(self, payroll_id: str, payroll_data: Dict[str, Any]) -> Optional[Payroll]:
        """
        تحديث بيانات كشف رواتب
        
        المعاملات:
            payroll_id: معرف كشف الرواتب
            payroll_data: بيانات كشف الرواتب المحدثة
            
        العائد:
            كائن كشف الرواتب المحدث أو None إذا لم يتم العثور على كشف الرواتب
        """
        # البحث عن كشف الرواتب
        payroll = self.get_payroll(payroll_id)
        if not payroll:
            return None
        
        # تحديث بيانات كشف الرواتب
        payroll_data['payroll_id'] = payroll_id
        updated_payroll = Payroll.from_dict(payroll_data)
        
        # حفظ كشف الرواتب المحدث في قاعدة البيانات
        self._save_payroll(updated_payroll)
        
        return updated_payroll
    
    def delete_payroll(self, payroll_id: str) -> bool:
        """
        حذف كشف رواتب
        
        المعاملات:
            payroll_id: معرف كشف الرواتب
            
        العائد:
            True إذا تم الحذف بنجاح، False إذا لم يتم العثور على كشف الرواتب
        """
        # البحث عن كشف الرواتب
        payroll = self.get_payroll(payroll_id)
        if not payroll:
            return False
        
        # حذف كشف الرواتب من قاعدة البيانات
        query = "DELETE FROM payrolls WHERE payroll_id = %s"
        self.db_manager.execute_query(query, (payroll_id,))
        
        return True
    
    def get_payroll(self, payroll_id: str) -> Optional[Payroll]:
        """
        الحصول على كشف رواتب بواسطة المعرف
        
        المعاملات:
            payroll_id: معرف كشف الرواتب
            
        العائد:
            كائن كشف الرواتب أو None إذا لم يتم العثور على كشف الرواتب
        """
        # استعلام قاعدة البيانات للحصول على كشف الرواتب
        query = "SELECT * FROM payrolls WHERE payroll_id = %s"
        result = self.db_manager.execute_query(query, (payroll_id,))
        
        if not result:
            return None
        
        # إنشاء كائن كشف الرواتب
        payroll_data = result[0]
        payroll = Payroll.from_dict(payroll_data)
        
        return payroll
    
    def get_employee_payrolls(self, employee_id: str) -> List[Payroll]:
        """
        الحصول على كشوف رواتب موظف
        
        المعاملات:
            employee_id: معرف الموظف
            
        العائد:
            قائمة بكائنات كشوف الرواتب
        """
        # استعلام قاعدة البيانات للحصول على كشوف رواتب الموظف
        query = "SELECT * FROM payrolls WHERE employee_id = %s ORDER BY period_start DESC"
        results = self.db_manager.execute_query(query, (employee_id,))
        
        # إنشاء قائمة كشوف الرواتب
        payrolls = []
        for payroll_data in results:
            payroll = Payroll.from_dict(payroll_data)
            payrolls.append(payroll)
        
        return payrolls
    
    def generate_payroll(self, employee_id: str, period_start: date, period_end: date) -> Payroll:
        """
        إنشاء كشف رواتب لموظف
        
        المعاملات:
            employee_id: معرف الموظف
            period_start: تاريخ بداية الفترة
            period_end: تاريخ نهاية الفترة
            
        العائد:
            كائن كشف الرواتب الجديد
        """
        # الحصول على الموظف
        employee_service = EmployeeService(self.db_manager)
        employee = employee_service.get_employee(employee_id)
        if not employee:
            raise ValueError(f"لم يتم العثور على الموظف بالمعرف {employee_id}")
        
        # الحصول على سجلات الحضور للفترة المحددة
        attendance_report = employee_service.get_employee_attendance_report(employee_id, period_start, period_end)
        
        # حساب الراتب الأساسي
        basic_salary = employee.salary or 0.0
        
        # حساب أجر العمل الإضافي
        overtime_pay = attendance_report.get('total_overtime_hours', 0) * (basic_salary / 176)  # افتراض 22 يوم عمل × 8 ساعات
        
        # حساب الاستقطاعات (مثال: الغياب والتأخير)
        deductions = 0.0
        if 'absent_days' in attendance_report:
            deductions += (attendance_report['absent_days'] * (basic_salary / 30))  # افتراض 30 يوم في الشهر
        
        if 'total_late_hours' in attendance_report:
            deductions += (attendance_report['total_late_hours'] * (basic_salary / 176))
        
        # حساب الضريبة (مثال بسيط: 10% من الراتب الأساسي)
        tax = basic_salary * 0.1
        
        # إنشاء كشف الرواتب
        payroll_data = {
            'employee_id': employee_id,
            'period_start': period_start,
            'period_end': period_end,
            'basic_salary': basic_salary,
            'overtime_pay': overtime_pay,
            'deductions': deductions,
            'tax': tax,
            'status': 'قيد الإعداد'
        }
        
        return self.create_payroll(payroll_data)
    
    def generate_department_payrolls(self, department_id: str, period_start: date, period_end: date) -> List[Payroll]:
        """
        إنشاء كشوف رواتب لقسم
        
        المعاملات:
            department_id: معرف القسم
            period_start: تاريخ بداية الفترة
            period_end: تاريخ نهاية الفترة
            
        العائد:
            قائمة بكائنات كشوف الرواتب الجديدة
        """
        # الحصول على موظفي القسم
        department_service = DepartmentService(self.db_manager)
        department = department_service.get_department(department_id)
        if not department:
            raise ValueError(f"لم يتم العثور على القسم بالمعرف {department_id}")
        
        # إنشاء كشوف رواتب لكل موظف
        payrolls = []
        for employee in department.employees:
            try:
                payroll = self.generate_payroll(employee.employee_id, period_start, period_end)
                payrolls.append(payroll)
            except Exception as e:
                # تسجيل الخطأ وتجاهله للاستمرار مع الموظفين الآخرين
                print(f"خطأ في إنشاء كشف رواتب للموظف {employee.employee_id}: {str(e)}")
        
        return payrolls
    
    def approve_payroll(self, payroll_id: str) -> Optional[Payroll]:
        """
        الموافقة على كشف رواتب
        
        المعاملات:
            payroll_id: معرف كشف الرواتب
            
        العائد:
            كائن كشف الرواتب المحدث أو None إذا لم يتم العثور على كشف الرواتب
        """
        # البحث عن كشف الرواتب
        payroll = self.get_payroll(payroll_id)
        if not payroll:
            return None
        
        # تحديث حالة كشف الرواتب
        payroll.status = "معتمد"
        
        # حفظ كشف الرواتب المحدث في قاعدة البيانات
        self._save_payroll(payroll)
        
        return payroll
    
    def process_payroll(self, payroll_id: str, payment_method: str, payment_date: date = None) -> Optional[Payroll]:
        """
        معالجة كشف رواتب
        
        المعاملات:
            payroll_id: معرف كشف الرواتب
            payment_method: طريقة الدفع
            payment_date: تاريخ الدفع (اختياري)
            
        العائد:
            كائن كشف الرواتب المحدث أو None إذا لم يتم العثور على كشف الرواتب
        """
        # البحث عن كشف الرواتب
        payroll = self.get_payroll(payroll_id)
        if not payroll:
            return None
        
        # التحقق من حالة كشف الرواتب
        if payroll.status != "معتمد":
            raise ValueError("لا يمكن معالجة كشف رواتب غير معتمد")
        
        # تحديث بيانات كشف الرواتب
        payroll.status = "مدفوع"
        payroll.payment_method = payment_method
        payroll.payment_date = payment_date or date.today()
        
        # حفظ كشف الرواتب المحدث في قاعدة البيانات
        self._save_payroll(payroll)
        
        return payroll
    
    def _save_payroll(self, payroll: Payroll) -> None:
        """
        حفظ كشف الرواتب في قاعدة البيانات
        
        المعاملات:
            payroll: كائن كشف الرواتب
        """
        # تحويل كائن كشف الرواتب إلى قاموس
        payroll_dict = payroll.to_dict()
        
        # بناء استعلام الإدراج أو التحديث
        columns = ', '.join(payroll_dict.keys())
        placeholders = ', '.join(['%s'] * len(payroll_dict))
        values = tuple(payroll_dict.values())
        
        # تنفيذ استعلام الإدراج أو التحديث
        query = f"""
        INSERT INTO payrolls ({columns})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE
        {', '.join([f'{col} = VALUES({col})' for col in payroll_dict.keys() if col != 'payroll_id'])}
        """
        
        self.db_manager.execute_query(query, values)


class RecruitmentService:
    """خدمة إدارة التوظيف"""
    
    def __init__(self, db_manager):
        """
        تهيئة خدمة إدارة التوظيف
        
        المعاملات:
            db_manager: مدير قاعدة البيانات
        """
        self.db_manager = db_manager
        
    def create_recruitment(self, recruitment_data: Dict[str, Any]) -> Recruitment:
        """
        إنشاء عملية توظيف جديدة
        
        المعاملات:
            recruitment_data: بيانات عملية التوظيف
            
        العائد:
            كائن عملية التوظيف الجديدة
        """
        # إنشاء معرف فريد لعملية التوظيف
        recruitment_id = str(uuid.uuid4())
        recruitment_data['recruitment_id'] = recruitment_id
        
        # إنشاء كائن عملية التوظيف
        recruitment = Recruitment.from_dict(recruitment_data)
        
        # حفظ عملية التوظيف في قاعدة البيانات
        self._save_recruitment(recruitment)
        
        return recruitment
    
    def update_recruitment(self, recruitment_id: str, recruitment_data: Dict[str, Any]) -> Optional[Recruitment]:
        """
        تحديث بيانات عملية توظيف
        
        المعاملات:
            recruitment_id: معرف عملية التوظيف
            recruitment_data: بيانات عملية التوظيف المحدثة
            
        العائد:
            كائن عملية التوظيف المحدثة أو None إذا لم يتم العثور على عملية التوظيف
        """
        # البحث عن عملية التوظيف
        recruitment = self.get_recruitment(recruitment_id)
        if not recruitment:
            return None
        
        # تحديث بيانات عملية التوظيف
        recruitment_data['recruitment_id'] = recruitment_id
        updated_recruitment = Recruitment.from_dict(recruitment_data)
        
        # الحفاظ على المرشحين الحاليين
        updated_recruitment.candidates = recruitment.candidates
        
        # حفظ عملية التوظيف المحدثة في قاعدة البيانات
        self._save_recruitment(updated_recruitment)
        
        return updated_recruitment
    
    def delete_recruitment(self, recruitment_id: str) -> bool:
        """
        حذف عملية توظيف
        
        المعاملات:
            recruitment_id: معرف عملية التوظيف
            
        العائد:
            True إذا تم الحذف بنجاح، False إذا لم يتم العثور على عملية التوظيف
        """
        # البحث عن عملية التوظيف
        recruitment = self.get_recruitment(recruitment_id)
        if not recruitment:
            return False
        
        # حذف المرشحين المرتبطين بعملية التوظيف
        self._delete_recruitment_candidates(recruitment_id)
        
        # حذف عملية التوظيف من قاعدة البيانات
        query = "DELETE FROM recruitments WHERE recruitment_id = %s"
        self.db_manager.execute_query(query, (recruitment_id,))
        
        return True
    
    def get_recruitment(self, recruitment_id: str) -> Optional[Recruitment]:
        """
        الحصول على عملية توظيف بواسطة المعرف
        
        المعاملات:
            recruitment_id: معرف عملية التوظيف
            
        العائد:
            كائن عملية التوظيف أو None إذا لم يتم العثور على عملية التوظيف
        """
        # استعلام قاعدة البيانات للحصول على عملية التوظيف
        query = "SELECT * FROM recruitments WHERE recruitment_id = %s"
        result = self.db_manager.execute_query(query, (recruitment_id,))
        
        if not result:
            return None
        
        # إنشاء كائن عملية التوظيف
        recruitment_data = result[0]
        recruitment = Recruitment.from_dict(recruitment_data)
        
        # إضافة المرشحين
        recruitment.candidates = self._get_recruitment_candidates(recruitment_id)
        
        return recruitment
    
    def get_all_recruitments(self, company_id: Optional[str] = None, department_id: Optional[str] = None, status: Optional[str] = None) -> List[Recruitment]:
        """
        الحصول على جميع عمليات التوظيف
        
        المعاملات:
            company_id: معرف الشركة (اختياري)
            department_id: معرف القسم (اختياري)
            status: حالة عملية التوظيف (اختياري)
            
        العائد:
            قائمة بكائنات عمليات التوظيف
        """
        # بناء استعلام قاعدة البيانات
        query = "SELECT * FROM recruitments"
        params = []
        
        conditions = []
        if company_id:
            conditions.append("company_id = %s")
            params.append(company_id)
        if department_id:
            conditions.append("department_id = %s")
            params.append(department_id)
        if status:
            conditions.append("status = %s")
            params.append(status)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        # تنفيذ الاستعلام
        results = self.db_manager.execute_query(query, tuple(params))
        
        # إنشاء قائمة عمليات التوظيف
        recruitments = []
        for recruitment_data in results:
            recruitment = Recruitment.from_dict(recruitment_data)
            recruitment.candidates = self._get_recruitment_candidates(recruitment.recruitment_id)
            recruitments.append(recruitment)
        
        return recruitments
    
    def add_candidate(self, candidate_data: Dict[str, Any]) -> Candidate:
        """
        إضافة مرشح لعملية توظيف
        
        المعاملات:
            candidate_data: بيانات المرشح
            
        العائد:
            كائن المرشح الجديد
        """
        # إنشاء معرف فريد للمرشح
        candidate_id = str(uuid.uuid4())
        candidate_data['candidate_id'] = candidate_id
        
        # إنشاء كائن المرشح
        candidate = Candidate.from_dict(candidate_data)
        
        # حفظ المرشح في قاعدة البيانات
        self._save_candidate(candidate)
        
        return candidate
    
    def update_candidate(self, candidate_id: str, candidate_data: Dict[str, Any]) -> Optional[Candidate]:
        """
        تحديث بيانات مرشح
        
        المعاملات:
            candidate_id: معرف المرشح
            candidate_data: بيانات المرشح المحدثة
            
        العائد:
            كائن المرشح المحدث أو None إذا لم يتم العثور على المرشح
        """
        # البحث عن المرشح
        candidate = self.get_candidate(candidate_id)
        if not candidate:
            return None
        
        # تحديث بيانات المرشح
        candidate_data['candidate_id'] = candidate_id
        candidate_data['recruitment_id'] = candidate.recruitment_id
        updated_candidate = Candidate.from_dict(candidate_data)
        
        # حفظ المرشح المحدث في قاعدة البيانات
        self._save_candidate(updated_candidate)
        
        return updated_candidate
    
    def get_candidate(self, candidate_id: str) -> Optional[Candidate]:
        """
        الحصول على مرشح بواسطة المعرف
        
        المعاملات:
            candidate_id: معرف المرشح
            
        العائد:
            كائن المرشح أو None إذا لم يتم العثور على المرشح
        """
        # استعلام قاعدة البيانات للحصول على المرشح
        query = "SELECT * FROM candidates WHERE candidate_id = %s"
        result = self.db_manager.execute_query(query, (candidate_id,))
        
        if not result:
            return None
        
        # إنشاء كائن المرشح
        candidate_data = result[0]
        candidate = Candidate.from_dict(candidate_data)
        
        return candidate
    
    def schedule_interview(self, candidate_id: str, interview_date: datetime) -> Optional[Candidate]:
        """
        جدولة مقابلة لمرشح
        
        المعاملات:
            candidate_id: معرف المرشح
            interview_date: تاريخ ووقت المقابلة
            
        العائد:
            كائن المرشح المحدث أو None إذا لم يتم العثور على المرشح
        """
        # البحث عن المرشح
        candidate = self.get_candidate(candidate_id)
        if not candidate:
            return None
        
        # تحديث حالة المرشح وتاريخ المقابلة
        candidate.status = "مقابلة مجدولة"
        candidate.interview_date = interview_date
        
        # حفظ المرشح المحدث في قاعدة البيانات
        self._save_candidate(candidate)
        
        return candidate
    
    def evaluate_candidate(self, candidate_id: str, evaluation: str, rating: int, notes: Optional[str] = None) -> Optional[Candidate]:
        """
        تقييم مرشح
        
        المعاملات:
            candidate_id: معرف المرشح
            evaluation: تقييم المرشح
            rating: تقييم المرشح (1-5)
            notes: ملاحظات (اختياري)
            
        العائد:
            كائن المرشح المحدث أو None إذا لم يتم العثور على المرشح
        """
        # البحث عن المرشح
        candidate = self.get_candidate(candidate_id)
        if not candidate:
            return None
        
        # تحديث بيانات تقييم المرشح
        candidate.evaluation = evaluation
        candidate.rating = rating
        if notes:
            candidate.notes = notes
        
        # حفظ المرشح المحدث في قاعدة البيانات
        self._save_candidate(candidate)
        
        return candidate
    
    def hire_candidate(self, candidate_id: str) -> Optional[Employee]:
        """
        توظيف مرشح
        
        المعاملات:
            candidate_id: معرف المرشح
            
        العائد:
            كائن الموظف الجديد أو None إذا لم يتم العثور على المرشح
        """
        # البحث عن المرشح
        candidate = self.get_candidate(candidate_id)
        if not candidate:
            return None
        
        # البحث عن عملية التوظيف
        recruitment = self.get_recruitment(candidate.recruitment_id)
        if not recruitment:
            raise ValueError(f"لم يتم العثور على عملية التوظيف بالمعرف {candidate.recruitment_id}")
        
        # تحديث حالة المرشح
        candidate.status = "تم التوظيف"
        self._save_candidate(candidate)
        
        # إنشاء موظف جديد
        employee_data = {
            'first_name': candidate.first_name,
            'last_name': candidate.last_name,
            'email': candidate.email,
            'phone': candidate.phone,
            'position_id': recruitment.position_id,
            'department_id': recruitment.department_id,
            'hire_date': date.today(),
            'employment_type': EmploymentType.FULL_TIME,
            'status': EmployeeStatus.ACTIVE,
            'company_id': recruitment.company_id,
            'branch_id': recruitment.branch_id
        }
        
        # إنشاء الموظف
        employee_service = EmployeeService(self.db_manager)
        employee = employee_service.create_employee(employee_data)
        
        return employee
    
    def reject_candidate(self, candidate_id: str, reason: Optional[str] = None) -> Optional[Candidate]:
        """
        رفض مرشح
        
        المعاملات:
            candidate_id: معرف المرشح
            reason: سبب الرفض (اختياري)
            
        العائد:
            كائن المرشح المحدث أو None إذا لم يتم العثور على المرشح
        """
        # البحث عن المرشح
        candidate = self.get_candidate(candidate_id)
        if not candidate:
            return None
        
        # تحديث حالة المرشح
        candidate.status = "مرفوض"
        if reason:
            candidate.notes = reason
        
        # حفظ المرشح المحدث في قاعدة البيانات
        self._save_candidate(candidate)
        
        return candidate
    
    def close_recruitment(self, recruitment_id: str) -> Optional[Recruitment]:
        """
        إغلاق عملية توظيف
        
        المعاملات:
            recruitment_id: معرف عملية التوظيف
            
        العائد:
            كائن عملية التوظيف المحدثة أو None إذا لم يتم العثور على عملية التوظيف
        """
        # البحث عن عملية التوظيف
        recruitment = self.get_recruitment(recruitment_id)
        if not recruitment:
            return None
        
        # تحديث حالة عملية التوظيف
        recruitment.status = "مغلق"
        recruitment.closing_date = date.today()
        
        # حفظ عملية التوظيف المحدثة في قاعدة البيانات
        self._save_recruitment(recruitment)
        
        return recruitment
    
    def _save_recruitment(self, recruitment: Recruitment) -> None:
        """
        حفظ عملية التوظيف في قاعدة البيانات
        
        المعاملات:
            recruitment: كائن عملية التوظيف
        """
        # تحويل كائن عملية التوظيف إلى قاموس
        recruitment_dict = recruitment.to_dict()
        
        # حذف المرشحين من القاموس
        recruitment_dict.pop('candidates', None)
        
        # بناء استعلام الإدراج أو التحديث
        columns = ', '.join(recruitment_dict.keys())
        placeholders = ', '.join(['%s'] * len(recruitment_dict))
        values = tuple(recruitment_dict.values())
        
        # تنفيذ استعلام الإدراج أو التحديث
        query = f"""
        INSERT INTO recruitments ({columns})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE
        {', '.join([f'{col} = VALUES({col})' for col in recruitment_dict.keys() if col != 'recruitment_id'])}
        """
        
        self.db_manager.execute_query(query, values)
    
    def _save_candidate(self, candidate: Candidate) -> None:
        """
        حفظ مرشح في قاعدة البيانات
        
        المعاملات:
            candidate: كائن المرشح
        """
        # تحويل كائن المرشح إلى قاموس
        candidate_dict = candidate.to_dict()
        
        # حذف الحقول المحسوبة من القاموس
        candidate_dict.pop('full_name', None)
        
        # بناء استعلام الإدراج أو التحديث
        columns = ', '.join(candidate_dict.keys())
        placeholders = ', '.join(['%s'] * len(candidate_dict))
        values = tuple(candidate_dict.values())
        
        # تنفيذ استعلام الإدراج أو التحديث
        query = f"""
        INSERT INTO candidates ({columns})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE
        {', '.join([f'{col} = VALUES({col})' for col in candidate_dict.keys() if col != 'candidate_id'])}
        """
        
        self.db_manager.execute_query(query, values)
    
    def _get_recruitment_candidates(self, recruitment_id: str) -> List[Candidate]:
        """
        الحصول على مرشحي عملية توظيف
        
        المعاملات:
            recruitment_id: معرف عملية التوظيف
            
        العائد:
            قائمة بكائنات المرشحين
        """
        # استعلام قاعدة البيانات للحصول على مرشحي عملية التوظيف
        query = "SELECT * FROM candidates WHERE recruitment_id = %s"
        results = self.db_manager.execute_query(query, (recruitment_id,))
        
        # إنشاء قائمة المرشحين
        candidates = []
        for candidate_data in results:
            candidate = Candidate.from_dict(candidate_data)
            candidates.append(candidate)
        
        return candidates
    
    def _delete_recruitment_candidates(self, recruitment_id: str) -> None:
        """
        حذف مرشحي عملية توظيف
        
        المعاملات:
            recruitment_id: معرف عملية التوظيف
        """
        # حذف مرشحي عملية التوظيف
        query = "DELETE FROM candidates WHERE recruitment_id = %s"
        self.db_manager.execute_query(query, (recruitment_id,))
