# services_modules.complaints_suggestions.models.complaint

## Imports
- complaint_category
- complaint_status
- datetime
- django.contrib.auth
- django.db
- django.utils
- django.utils.translation
- services_modules.core.models

## Classes
- Complaint
  - attr: `company`
  - attr: `branch`
  - attr: `category`
  - attr: `status`
  - attr: `title`
  - attr: `description`
  - attr: `submitted_by`
  - attr: `submission_date`
  - attr: `assigned_to`
  - attr: `resolution_date`
  - attr: `resolution_notes`
  - attr: `notes`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
  - method: `change_status`
  - method: `resolve`
  - method: `get_history`
  - method: `get_days_since_submission`
  - method: `get_resolution_time_days`
- ComplaintStatusHistory
  - attr: `complaint`
  - attr: `status`
  - attr: `changed_by`
  - attr: `change_date`
  - attr: `notes`
  - method: `__str__`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `app_label`
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`

## Functions
- __str__
- change_status
- resolve
- get_history
- get_days_since_submission
- get_resolution_time_days
- __str__

## Module Variables
- `User`

## Class Diagram

```mermaid
classDiagram
    class Complaint {
        +company
        +branch
        +category
        +status
        +title
        +... (9 more)
        +__str__()
        +change_status()
        +resolve()
        +get_history()
        +get_days_since_submission()
        +... (1 more)
    }
    class ComplaintStatusHistory {
        +complaint
        +status
        +changed_by
        +change_date
        +notes
        +__str__()
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +app_label
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    Complaint --> Meta
    Complaint --> Meta
    ComplaintStatusHistory --> Meta
    ComplaintStatusHistory --> Meta
```
