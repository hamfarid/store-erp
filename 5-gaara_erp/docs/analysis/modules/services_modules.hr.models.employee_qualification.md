# services_modules.hr.models.employee_qualification

## Imports
- datetime
- django.db
- django.utils
- django.utils.translation

## Classes
- EmployeeQualification
  - attr: `employee`
  - attr: `institution_name`
  - attr: `degree`
  - attr: `field_of_study`
  - attr: `start_date`
  - attr: `completion_date`
  - attr: `grade`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
  - method: `get_duration_years`
  - method: `is_recent`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`

## Functions
- __str__
- get_duration_years
- is_recent

## Class Diagram

```mermaid
classDiagram
    class EmployeeQualification {
        +employee
        +institution_name
        +degree
        +field_of_study
        +start_date
        +... (4 more)
        +__str__()
        +get_duration_years()
        +is_recent()
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    EmployeeQualification --> Meta
```
