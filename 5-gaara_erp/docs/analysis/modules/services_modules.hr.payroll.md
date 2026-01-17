# services_modules.hr.payroll

## Imports
- django.conf
- django.db
- django.utils.translation
- employee

## Classes
- PayrollPeriod
  - attr: `name`
  - attr: `start_date`
  - attr: `end_date`
  - attr: `is_closed`
  - method: `__str__`
- SalaryComponent
  - attr: `COMPONENT_TYPES`
  - attr: `name`
  - attr: `type`
  - attr: `is_taxable`
  - attr: `is_active`
  - method: `__str__`
- EmployeeSalaryStructure
  - attr: `employee`
  - attr: `component`
  - attr: `amount`
  - attr: `formula`
  - attr: `start_date`
  - attr: `end_date`
- PayrollRun
  - attr: `PAYROLL_RUN_STATUS_CHOICES`
  - attr: `payroll_period`
  - attr: `run_date`
  - attr: `status`
  - attr: `notes`
  - attr: `created_by`
  - attr: `approved_by`
  - attr: `paid_by`
  - attr: `paid_at`
- Payslip
  - attr: `payroll_run`
  - attr: `employee`
  - attr: `gross_salary`
  - attr: `total_deductions`
  - attr: `total_earnings`
  - attr: `net_salary`
  - attr: `payment_method`
- PayslipDetail
  - attr: `payslip`
  - attr: `component`
  - attr: `amount`
  - attr: `notes`
- EndOfServiceBenefit
  - attr: `employee`
  - attr: `calculation_date`
  - attr: `service_years`
  - attr: `last_salary`
  - attr: `benefit_amount`
  - attr: `notes`
  - attr: `is_paid`
  - attr: `payment_date`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `unique_together`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`

## Functions
- __str__
- __str__

## Class Diagram

```mermaid
classDiagram
    class PayrollPeriod {
        +name
        +start_date
        +end_date
        +is_closed
        +__str__()
    }
    class SalaryComponent {
        +COMPONENT_TYPES
        +name
        +type
        +is_taxable
        +is_active
        +__str__()
    }
    class EmployeeSalaryStructure {
        +employee
        +component
        +amount
        +formula
        +start_date
        +... (1 more)
    }
    class PayrollRun {
        +PAYROLL_RUN_STATUS_CHOICES
        +payroll_period
        +run_date
        +status
        +notes
        +... (4 more)
    }
    class Payslip {
        +payroll_run
        +employee
        +gross_salary
        +total_deductions
        +total_earnings
        +... (2 more)
    }
    class PayslipDetail {
        +payslip
        +component
        +amount
        +notes
    }
    class EndOfServiceBenefit {
        +employee
        +calculation_date
        +service_years
        +last_salary
        +benefit_amount
        +... (3 more)
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +unique_together
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
    }
    PayrollPeriod --> Meta
    PayrollPeriod --> Meta
    PayrollPeriod --> Meta
    PayrollPeriod --> Meta
    PayrollPeriod --> Meta
    PayrollPeriod --> Meta
    PayrollPeriod --> Meta
    SalaryComponent --> Meta
    SalaryComponent --> Meta
    SalaryComponent --> Meta
    SalaryComponent --> Meta
    SalaryComponent --> Meta
    SalaryComponent --> Meta
    SalaryComponent --> Meta
    EmployeeSalaryStructure --> Meta
    EmployeeSalaryStructure --> Meta
    EmployeeSalaryStructure --> Meta
    EmployeeSalaryStructure --> Meta
    EmployeeSalaryStructure --> Meta
    EmployeeSalaryStructure --> Meta
    EmployeeSalaryStructure --> Meta
    PayrollRun --> Meta
    PayrollRun --> Meta
    PayrollRun --> Meta
    PayrollRun --> Meta
    PayrollRun --> Meta
    PayrollRun --> Meta
    PayrollRun --> Meta
    Payslip --> Meta
    Payslip --> Meta
    Payslip --> Meta
    Payslip --> Meta
    Payslip --> Meta
    Payslip --> Meta
    Payslip --> Meta
    PayslipDetail --> Meta
    PayslipDetail --> Meta
    PayslipDetail --> Meta
    PayslipDetail --> Meta
    PayslipDetail --> Meta
    PayslipDetail --> Meta
    PayslipDetail --> Meta
    EndOfServiceBenefit --> Meta
    EndOfServiceBenefit --> Meta
    EndOfServiceBenefit --> Meta
    EndOfServiceBenefit --> Meta
    EndOfServiceBenefit --> Meta
    EndOfServiceBenefit --> Meta
    EndOfServiceBenefit --> Meta
```
