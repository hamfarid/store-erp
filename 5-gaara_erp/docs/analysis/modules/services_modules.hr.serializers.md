# services_modules.hr.serializers

## Imports
- core_modules.organization.models
- django.contrib.auth
- models
- rest_framework

## Classes
- UserRepresentationSerializer
- DepartmentSerializer
  - attr: `company_id`
  - attr: `company`
  - attr: `parent_id`
  - attr: `parent`
  - attr: `manager_id`
  - attr: `manager`
- JobGradeSerializer
- PositionSerializer
  - attr: `department_id`
  - attr: `department`
  - attr: `job_grade_id`
  - attr: `job_grade`
  - attr: `reports_to_id`
  - attr: `reports_to`
- EmployeeDocumentSerializer
- EmployeeExperienceSerializer
- EmployeeQualificationSerializer
- EmployeeTrainingSerializer
- EmployeeAssetSerializer
- EmployeeSerializer
  - attr: `user`
  - attr: `user_id`
  - attr: `nationality`
  - attr: `nationality_id`
  - attr: `branch`
  - attr: `branch_id`
  - attr: `department`
  - attr: `department_id`
  - attr: `position`
  - attr: `position_id`
  - attr: `manager`
  - attr: `manager_id`
  - attr: `documents`
  - attr: `experience`
  - attr: `qualifications`
  - attr: `trainings`
  - attr: `assigned_assets`
- ContractSerializer
  - attr: `employee`
  - attr: `employee_id`
  - attr: `position`
  - attr: `position_id`
  - attr: `salary_currency`
  - attr: `salary_currency_id`
- AttendanceRecordSerializer
  - attr: `employee`
  - attr: `employee_id`
- LeaveTypeSerializer
- LeaveBalanceSerializer
  - attr: `employee`
  - attr: `employee_id`
  - attr: `leave_type`
  - attr: `leave_type_id`
- LeaveRequestSerializer
  - attr: `employee`
  - attr: `employee_id`
  - attr: `leave_type`
  - attr: `leave_type_id`
  - attr: `replacement_employee`
  - attr: `replacement_employee_id`
  - attr: `current_approver`
- PayrollPeriodSerializer
- SalaryComponentSerializer
- PayrollRunSerializer
  - attr: `payroll_period`
  - attr: `payroll_period_id`
  - attr: `created_by`
  - attr: `approved_by`
  - attr: `paid_by`
- PayslipDetailSerializer
  - attr: `component`
  - attr: `component_id`
- PayslipSerializer
  - attr: `employee`
  - attr: `employee_id`
  - attr: `payroll_run`
  - attr: `payroll_run_id`
  - attr: `details`
  - method: `create`
- HRSettingSerializer
- BonusRuleSerializer
- EndOfServiceBenefitSerializer
- LeaveCancellationRequestSerializer
  - attr: `leave_request`
  - attr: `leave_request_id`
- PenaltyRuleSerializer
- OvertimeRuleSerializer
- SalaryAdvanceRequestSerializer
  - attr: `employee`
  - attr: `employee_id`
  - attr: `approved_by`
- SalaryIncreaseRequestSerializer
  - attr: `employee`
  - attr: `employee_id`
  - attr: `approved_by`
- PromotionSerializer
  - attr: `employee`
  - attr: `employee_id`
  - attr: `old_position`
  - attr: `old_position_id`
  - attr: `new_position`
  - attr: `new_position_id`
  - attr: `approved_by`
- PerformanceReviewSerializer
  - attr: `employee`
  - attr: `employee_id`
  - attr: `reviewer`
  - attr: `reviewer_id`
- MissionSerializer
  - attr: `employee`
  - attr: `employee_id`
  - attr: `approved_by`
- MissionExpenseSerializer
  - attr: `mission`
  - attr: `mission_id`
  - attr: `approved_by`
- TaxBracketSerializer
- SocialInsuranceSettingSerializer
- EmployeeSalaryStructureSerializer
  - attr: `employee`
  - attr: `employee_id`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `exclude`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
  - attr: `read_only_fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`
- Meta
  - attr: `model`
  - attr: `fields`

## Functions
- create

## Module Variables
- `User`

## Class Diagram

```mermaid
classDiagram
    class UserRepresentationSerializer {
    }
    class DepartmentSerializer {
        +company_id
        +company
        +parent_id
        +parent
        +manager_id
        +... (1 more)
    }
    class JobGradeSerializer {
    }
    class PositionSerializer {
        +department_id
        +department
        +job_grade_id
        +job_grade
        +reports_to_id
        +... (1 more)
    }
    class EmployeeDocumentSerializer {
    }
    class EmployeeExperienceSerializer {
    }
    class EmployeeQualificationSerializer {
    }
    class EmployeeTrainingSerializer {
    }
    class EmployeeAssetSerializer {
    }
    class EmployeeSerializer {
        +user
        +user_id
        +nationality
        +nationality_id
        +branch
        +... (12 more)
    }
    class ContractSerializer {
        +employee
        +employee_id
        +position
        +position_id
        +salary_currency
        +... (1 more)
    }
    class AttendanceRecordSerializer {
        +employee
        +employee_id
    }
    class LeaveTypeSerializer {
    }
    class LeaveBalanceSerializer {
        +employee
        +employee_id
        +leave_type
        +leave_type_id
    }
    class LeaveRequestSerializer {
        +employee
        +employee_id
        +leave_type
        +leave_type_id
        +replacement_employee
        +... (2 more)
    }
    class PayrollPeriodSerializer {
    }
    class SalaryComponentSerializer {
    }
    class PayrollRunSerializer {
        +payroll_period
        +payroll_period_id
        +created_by
        +approved_by
        +paid_by
    }
    class PayslipDetailSerializer {
        +component
        +component_id
    }
    class PayslipSerializer {
        +employee
        +employee_id
        +payroll_run
        +payroll_run_id
        +details
        +create()
    }
    class HRSettingSerializer {
    }
    class BonusRuleSerializer {
    }
    class EndOfServiceBenefitSerializer {
    }
    class LeaveCancellationRequestSerializer {
        +leave_request
        +leave_request_id
    }
    class PenaltyRuleSerializer {
    }
    class OvertimeRuleSerializer {
    }
    class SalaryAdvanceRequestSerializer {
        +employee
        +employee_id
        +approved_by
    }
    class SalaryIncreaseRequestSerializer {
        +employee
        +employee_id
        +approved_by
    }
    class PromotionSerializer {
        +employee
        +employee_id
        +old_position
        +old_position_id
        +new_position
        +... (2 more)
    }
    class PerformanceReviewSerializer {
        +employee
        +employee_id
        +reviewer
        +reviewer_id
    }
    class MissionSerializer {
        +employee
        +employee_id
        +approved_by
    }
    class MissionExpenseSerializer {
        +mission
        +mission_id
        +approved_by
    }
    class TaxBracketSerializer {
    }
    class SocialInsuranceSettingSerializer {
    }
    class EmployeeSalaryStructureSerializer {
        +employee
        +employee_id
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +exclude
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
        +read_only_fields
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
    }
    class Meta {
        +model
        +fields
    }
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    UserRepresentationSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    DepartmentSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    JobGradeSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    PositionSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeDocumentSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeExperienceSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeQualificationSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeTrainingSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeAssetSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    EmployeeSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    ContractSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    AttendanceRecordSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveTypeSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveBalanceSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    LeaveRequestSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    PayrollPeriodSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    SalaryComponentSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayrollRunSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipDetailSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    PayslipSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    HRSettingSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    BonusRuleSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    EndOfServiceBenefitSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    LeaveCancellationRequestSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    PenaltyRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    OvertimeRuleSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryAdvanceRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    SalaryIncreaseRequestSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PromotionSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    PerformanceReviewSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    MissionExpenseSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    TaxBracketSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    SocialInsuranceSettingSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
    EmployeeSalaryStructureSerializer --> Meta
```
