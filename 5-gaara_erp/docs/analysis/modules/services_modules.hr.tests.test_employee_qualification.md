# services_modules.hr.tests.test_employee_qualification

## Imports
- datetime
- django.db
- django.test
- django.utils
- models.department
- models.employee
- models.employee_qualification
- models.position
- services_modules.core.models.branch
- services_modules.core.models.company

## Classes
- EmployeeQualificationModelTest
  - method: `setUp`
  - method: `test_create_employee_qualification`
  - method: `test_get_duration_years`
  - method: `test_is_recent`
  - method: `test_str_representation`

## Functions
- setUp
- test_create_employee_qualification
- test_get_duration_years
- test_is_recent
- test_str_representation

## Class Diagram

```mermaid
classDiagram
    class EmployeeQualificationModelTest {
        +setUp()
        +test_create_employee_qualification()
        +test_get_duration_years()
        +test_is_recent()
        +test_str_representation()
    }
```
