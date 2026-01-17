# services_modules.hr.attendance

## Imports
- django.conf
- django.db
- django.utils.translation
- employee
- leave

## Classes
- ReturnToWork
  - attr: `leave_request`
  - attr: `return_date`
  - attr: `notes`
  - attr: `recorded_by`
  - attr: `recorded_at`
- AttendanceRecord
  - attr: `ATTENDANCE_SOURCE`
  - attr: `employee`
  - attr: `attendance_date`
  - attr: `check_in_time`
  - attr: `check_out_time`
  - attr: `source`
  - attr: `latitude`
  - attr: `longitude`
  - attr: `notes`
- PenaltyRule
  - attr: `PENALTY_TYPES`
  - attr: `name`
  - attr: `penalty_type`
  - attr: `rate_multiplier`
  - attr: `unit`
  - attr: `is_active`
- OvertimeRule
  - attr: `name`
  - attr: `apply_before_hours`
  - attr: `apply_after_hours`
  - attr: `apply_weekends`
  - attr: `apply_holidays`
  - attr: `rate_multiplier`
  - attr: `is_active`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `unique_together`
  - attr: `ordering`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`

## Class Diagram

```mermaid
classDiagram
    class ReturnToWork {
        +leave_request
        +return_date
        +notes
        +recorded_by
        +recorded_at
    }
    class AttendanceRecord {
        +ATTENDANCE_SOURCE
        +employee
        +attendance_date
        +check_in_time
        +check_out_time
        +... (4 more)
    }
    class PenaltyRule {
        +PENALTY_TYPES
        +name
        +penalty_type
        +rate_multiplier
        +unit
        +... (1 more)
    }
    class OvertimeRule {
        +name
        +apply_before_hours
        +apply_after_hours
        +apply_weekends
        +apply_holidays
        +... (2 more)
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +unique_together
        +ordering
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
    }
    ReturnToWork --> Meta
    ReturnToWork --> Meta
    ReturnToWork --> Meta
    ReturnToWork --> Meta
    AttendanceRecord --> Meta
    AttendanceRecord --> Meta
    AttendanceRecord --> Meta
    AttendanceRecord --> Meta
    PenaltyRule --> Meta
    PenaltyRule --> Meta
    PenaltyRule --> Meta
    PenaltyRule --> Meta
    OvertimeRule --> Meta
    OvertimeRule --> Meta
    OvertimeRule --> Meta
    OvertimeRule --> Meta
```
